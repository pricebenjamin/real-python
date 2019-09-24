import bs4
import html2markdown
import itertools
import os
import pickle
import re
import requests
import time

from datetime import datetime
from collections import namedtuple

from typing import List, Union, Tuple, Dict, Optional, NewType
from bs4.element import Tag, NavigableString

bs4Element = Union[Tag, NavigableString]

ROOT_URL = "https://realpython.com"
GITHUB_URL = "https://github.com/pricebenjamin/real-python"

CACHE_FILENAME = "cached_responses.pickle"
CACHED_RESPONSES = {}


class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class TopicNotFound(Exception):
    """The requested topic was not found. Is the cache up-to-date?"""


class ExtractTutorialError(Error):
    """Base-class for errors relating to the extraction of tutorials."""


class MissingCardText(ExtractTutorialError):
    """The card provided is missing a paragraph with class 'card-text'."""


class ExtractIntroductionError(Error):
    """Base-class for errors relating to extracting introductions."""


class MissingH2(ExtractIntroductionError):
    """The article provided does not contain an <h2> element."""


class UnexpectedNavigableString(ExtractIntroductionError):
    """The navigable string provided does not match what was expected."""


class GetResponseError(Error):
    """Base-class for errors raised by the get_response function."""


class UnsuccessfulGet(GetResponseError):
    """Received an unexpected reponse code."""


class MetadataError(Error):
    """Base class for errors relating to metadata."""


class MissingArticle(MetadataError):
    """Could not find <div class="article"> tag when searching for metadata."""


class MissingMetadata(MetadataError):
    """Could not find <span class="text-muted"> tag when searching for metadata."""


class UnexpectedFirstChild(MetadataError):
    """First child of metadata tag was not NavigableString('by ')."""


# Cache
def load_cached_responses(filename):
    """Populate CACHED_RESPONSES by reading from a file.

    Args:
        filename (str): name of the file to unpic

    Returns:
        None

    Modifies:
        CACHED_RESPONSES (dict[url, requests.response])"""
    global CACHED_RESPONSES
    try:
        with open(filename, "rb") as f:
            prev_cache = pickle.load(f)
    except IOError as e:
        print(f"Cache not loaded. ({e})")
    else:
        CACHED_RESPONSES.update(prev_cache)


def save_cached_responses(filename):
    global CACHED_RESPONSES
    with open(filename, "wb") as f:
        pickle.dump(CACHED_RESPONSES, f)


# Helpers
default_headers = requests.utils.default_headers()
default_headers["User-Agent"] += f" ({GITHUB_URL})"
session = requests.Session()


def get_response(url):
    global CACHED_RESPONSES, session
    if url in CACHED_RESPONSES:
        print(f"Loading cached response: {url}")
        response = CACHED_RESPONSES[url]
        return response
    response = session.get(url, headers=default_headers)
    if response.status_code == 200:
        print(f"Successful get: {url}")
        print(f"    content length: {len(response.content)}")
        CACHED_RESPONSES[url] = response
        print(f"    cached: True")
        return response
    elif response.status_code == 429:
        print("Received status code 429: Too many requests.")
        retry_after = response.headers.get("Retry-After", "")
        try:
            count = int(retry_after)
        except ValueError:
            count = 10
        sleep_for(count)  # TODO: implement more robust rate-limiting
        return get_response(url)
    else:
        print("Error: unsuccessful get")
        print(f"    url: {url}")
        print(f"    status: {response.status_code}")
        raise UnsuccessfulGet(url)


def get_soup(response):
    return bs4.BeautifulSoup(response.content, "html5lib")


def sleep_for(count):
    for i in range(count, 0, -1):
        msg = f"    Sleeping for {i} more second{'s' if i != 1 else ''}..."
        msg = f"{msg: <40}"
        # https://docs.python.org/3/library/string.html#format-examples
        print(msg, end="\r")
        time.sleep(1)
    print()


def fetch_tutorial_topics():
    print("Fetching list of available tutorial topics...")
    response = get_response(ROOT_URL)
    soup = get_soup(response)
    topics_div = soup.find(
        "div", {"class": "sidebar-module sidebar-module-inset border"}
    )
    topic_anchors = topics_div.findAll("a", {"class": "badge badge-light text-muted"})

    topics = {anchor.text: ROOT_URL + anchor.attrs["href"] for anchor in topic_anchors}

    return topics


def get_cards(soup) -> List[Tag]:
    return soup.findAll("div", {"class": "card border-0"})


def extract_card_info(card) -> Tuple[str, str]:
    body = card.find("div", {"class": "card-body"})
    title = body.find("h2").text
    url = body.find("a").attrs["href"]
    return title, url


def is_premium(card) -> bool:
    card_text = card.find("p", {"class": "card-text"})

    if card_text is None:
        raise MissingCardText()

    result = card_text.find("a", {"href": "/account/join/"})
    # Note: this assumes /account/join/ will always be the first anchor
    # within the card-text paragraph

    if result is None:
        return False  # Did not find hyperlink to /account/join/
    else:
        return True  # Found hyperlink to /account/join/


def extract_introduction(soup, article_url) -> List[bs4Element]:
    article_body = soup.find("div", {"class": "article-body"})

    if article_body.find("h2") == None:
        raise MissingH2()

    # Introductory text is nested between divs at the beginning of the body.
    # As such, we begin by skipping over blank lines and divs:
    children = article_body.children
    while True:
        child = next(children)
        if isinstance(child, NavigableString) or child.name == "div":
            continue
        else:
            break

    # Store all remaining non-div elements until we hit the next div
    intro = [child]
    while True:
        child = next(children)
        if child == "\n":
            continue
        elif child.name == "div" or child.name == "h2":
            break
        else:
            intro.append(child)

    return intro


def format_introduction(tag_list) -> List[str]:
    intro = []
    for tag in tag_list:
        if isinstance(tag, bs4.element.NavigableString):
            if tag != "\n":
                raise UnexpectedNavigableString(f"tag == {tag}")
            else:
                continue
        for line in tag.decode().splitlines():
            intro.append(line)

    return intro


def found_new_tutorials(original: dict, to_append: dict) -> bool:
    """Check if all keys of `to_append` are in `original`. If not, update original."""
    difference = to_append.keys() - original.keys()  # Set difference
    if difference != set():
        original.update(to_append)
        return True
    else:
        return False


def get_metadata_element(soup, url) -> Tag:
    """Find, validate, and return the metadata element within soup.

    This function expects to find a particular <span> element from within
    the given `soup`. We refer to this span element as "the metadata element"
    because it contains the article's metadata (author, date, tags).
    """
    article = soup.find("div", "article")
    if not article:
        raise MissingArticle(f"{url!r}")

    # The first instance of <span class="text-muted"> is the desired element
    metadata = article.find("span", "text-muted")
    if not metadata:
        raise MissingMetadata(f"{url!r}")

    # Ensure we've found the desired element by examining its first child
    first_child = next(metadata.children)
    if not first_child == "by ":
        msg = f"first_child={first_child!r} at {url!r}"
        raise UnexpectedFirstChild(msg)
    return metadata


def generate_count_query_url(article_url):
    # Real Python uses a disqus query to count comments on a given article
    disqus_url = "https://realpython.disqus.com/count-data.js"
    return disqus_url + "?1=" + requests.utils.quote(article_url, safe="")


def generate_metadata_string_and_append_links(
    author, date, tags, comments, links=None
) -> str:
    if author and tags and comments:
        tag_links = ", ".join([f"[{tag.name}][{tag.link.id}]" for tag in tags])

        comment_link = (
            f"[{comments.count} comments]" if comments.count != 1 else "[1 comment]"
        )
        comment_link += f"[{comments.link.id}]"

        metadata_string = (
            f"by [{author.name}][{author.link.id}] "
            + (f"on {date.strftime('%a, %d %b %Y')} " if date else "")
            + f"with tags: {tag_links} "
            + f"({comment_link})"
        )

        if links:
            links.append(author.link)
            links.extend([tag.link for tag in tags])
            links.append(comments.link)
        return metadata_string
    else:
        return None


# Processing
Title, URL = NewType("Title", str), NewType("URL", str)
TutorialDict = Dict[Title, URL]


def extract_tutorials(soup, root_url="") -> Tuple[TutorialDict, TutorialDict]:
    premium_tutorials = {}
    non_premium_tutorials = {}

    cards = get_cards(soup)

    for card in cards:
        title, url = extract_card_info(card)
        if is_premium(card):
            premium_tutorials[title] = root_url + url
        else:
            if "/courses/" in url:
                # TODO: Fix this edge case by creating a separate metadata
                # extractor for "courses".
                continue
            non_premium_tutorials[title] = root_url + url

    return premium_tutorials, non_premium_tutorials


Author = namedtuple("Author", "name link")
Date = datetime
Tag = namedtuple("Tag", "name link")
Comments = namedtuple("Comments", "count link")
Link = namedtuple("Link", "id url")

Metadata = namedtuple("Metadata", "author date tags comments")


def extract_metadata(soup, article_url, link_counter) -> Metadata:
    metadata = get_metadata_element(soup, article_url)

    # Author
    author = (
        metadata.find("a", {"href": "#author"})
        or metadata.find("a", {"href": "#team"})
        or metadata.find("a", {"class": "text-muted", "href": "/"})
    )
    if author:
        name = author.text.strip()
        url = ROOT_URL if author.attrs["href"] == "/" else article_url
        link = Link(id=next(link_counter), url=(url + author.attrs["href"]))
        author = Author(name, link)

    # Date
    above_date = metadata.find("span", "fa-clock-o")
    date = above_date.nextSibling if above_date else None
    if date:
        date = date.strip()
        date = datetime.strptime(date, "%b %d, %Y")

    # Tags
    tags = metadata.findAll("a", "badge badge-light text-muted")
    if tags:
        tags = [
            Tag(
                tag.text.strip(),
                Link(id=next(link_counter), url=(ROOT_URL + tag.attrs["href"])),
            )
            for tag in tags
        ]

    # Comments
    comments = metadata.find("a", {"href": "#reader-comments"})
    if comments:
        # Real Python uses a disqus query to count the comments on a given article
        disqus = metadata.find("span", "disqus-comment-count")
        query_url = generate_count_query_url(disqus.attrs["data-disqus-identifier"])
        response = get_response(query_url)
        count = extract_comment_count(response)
        link = Link(id=next(link_counter), url=(article_url + comments.attrs["href"]))
        comments = Comments(count, link)

    return Metadata(author, date, tags, comments)


# Compile regular expression for searching disqus count query response
count_query_response_re = re.compile(r'"comments":(\d+)')


def extract_comment_count(disqus_response) -> int:
    match = count_query_response_re.search(disqus_response.text)
    if match:
        count, = match.groups()
        count = int(count)
    else:
        msg = (
            f"Failed to parse comment count query response;\n\n"
            f"regexp == {count_query_response_re!r}\n\n"
            f"disqus_response.text == {disqus_response.text!r}"
        )
        raise CommentCountError(msg)
    return count


def write_to_markdown(url_dict, filename, title, is_premium) -> None:
    subdirectory = "generated_markdown"
    if not os.path.exists(subdirectory):
        os.mkdir(subdirectory)
    path = os.path.join(subdirectory, filename)

    with open(path, "w") as file:
        lines = [title, "\n"]
        link_counter = itertools.count(start=1)
        for title, url in url_dict.items():
            response = get_response(url)
            soup = get_soup(response)

            if is_premium:
                lines.append(f"## [{title}]({url})\n\n")
            else:
                article_links = []
                article_links.append(Link(id=next(link_counter), url=url))
                lines.append(f"## [{title}][{article_links[0].id}]\n")
                # Write the introduction to the file
                metadata = extract_metadata(soup, url, link_counter)
                metadata_string = generate_metadata_string_and_append_links(
                    author=metadata.author,
                    date=metadata.date,
                    tags=metadata.tags,
                    comments=metadata.comments,
                    links=article_links,
                )
                if metadata_string:
                    lines.append(metadata_string + "\n\n")

                try:
                    intro = extract_introduction(soup, url)
                except MissingH2:
                    lines.append("> No introduction available.\n\n")
                except ExtractIntroductionError as e:
                    print("Unable to extract introduction for")
                    print(f"    title: {title}")
                    print(f"    url: {url}")
                    print(f"    error: {e}")
                    continue
                else:
                    for tag in intro:
                        md = html2markdown.convert(tag.decode()) + "\n\n"
                        lines.append(md)
                finally:
                    article_links.sort(key=lambda link: link.id)
                    for link in article_links:
                        lines.append(f"[{link.id}]: {link.url}\n")
                    lines.append("\n\n")

        file.writelines(lines)


def scrape_tutorial_topics(*topics):
    if not topics:
        raise ValueError(f"at least one topic must be specified")

    available_topics = fetch_tutorial_topics()

    if "all" in topics:
        topics = available_topics.keys()

    for topic in topics:
        if topic not in available_topics:
            msg = (
                f"'{topic}' is not in the list of available topics\n\n"
                f"Available topics include {set(available_topics.keys())!r}"
            )
            raise TopicNotFound(msg)

        print(f"Crawling `{topic}` tutorial pages...")

        premium = {}
        non_premium = {}

        # Iterate through all available pages until we cannot find new tutorials
        for i in itertools.count(start=1):
            link = available_topics[topic] + f"page/{i}/"
            try:
                response = get_response(link)
            except UnsuccessfulGet:
                break

            soup = get_soup(response)
            p, np = extract_tutorials(soup, root_url=ROOT_URL)

            if found_new_tutorials(premium, p) or found_new_tutorials(non_premium, np):
                print(f"    # Premium tutorials:     {len(premium):3d}")
                print(f"    # Non-Premium tutorials: {len(non_premium):3d}")
                continue
            else:
                print("    No new tutorials found.")
                break

        print(f"Saving `{topic}` URLs into markdown...")

        write_to_markdown(
            premium,
            filename=f"{topic}_premium_tutorials.md",
            title=f"# {topic}, premium tutorials from Real Python\n",
            is_premium=True,
        )

        write_to_markdown(
            non_premium,
            filename=f"{topic}_non_premium_tutorials.md",
            title=f"# {topic}, non-premium tutorials from Real Python\n",
            is_premium=False,
        )


def main():
    load_cached_responses(CACHE_FILENAME)

    # TODO(ben): accept command line arguments to specify topics
    try:
        scrape_tutorial_topics("all")
    finally:
        print("Saving cached responses...")
        save_cached_responses(CACHE_FILENAME)
        session.close()


if __name__ == "__main__":
    main()
