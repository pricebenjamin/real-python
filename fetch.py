import bs4
import html2markdown
import itertools
import os
import pickle
import re
import requests
import requests_cache

import time

from datetime import datetime
from collections import namedtuple
from urllib.parse import urljoin

from typing import List, Union, Tuple, Dict, Optional, NewType
from bs4.element import Tag, NavigableString

bs4Element = Union[Tag, NavigableString]

ROOT_URL = "https://realpython.com"
GITHUB_URL = "https://github.com/pricebenjamin/real-python"

REQUESTS_CACHE_FILENAME = "requests_cache"


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


date_re = re.compile(r"([A-Za-z]{3} \d+, \d{4})")


def get_cards(soup) -> List[Tag]:
    return soup.findAll("div", {"class": "card border-0"})


def extract_card_info(card):
    body = card.find("div", {"class": "card-body"})
    title = body.find("h2").text
    url = body.find("a").attrs["href"]

    title = card.find("h2", "card-title")
    assert title
    title_str = title.text.strip()

    url = title.parent.attrs["href"]

    is_premium = bool(card.find("a", {"href": "/account/join/"}))

    match = date_re.search(card.text)
    date = datetime.strptime(match.group(0), "%b %d, %Y") if match else None

    tags = card.find_all("a", "badge badge-light text-muted")
    tags = tags if tags else None  # return None instead of empty list

    return title_str, url, is_premium, date, tags


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

        if links is not None:
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
