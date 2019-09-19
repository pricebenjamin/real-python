import requests
import bs4
import pickle
from itertools import count

ROOT_URL = 'https://realpython.com'

CACHE_FILENAME = 'cached_responses.pickle'
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
        with open(filename, 'rb') as f:
            prev_cache = pickle.load(f)
    except IOError as e:
        print(f"Cache not loaded. ({e.__class__!r}: {e})")
    else:
        CACHED_RESPONSES.update(prev_cache)

def save_cached_responses(filename):
    global CACHED_RESPONSES
    with open(filename, 'wb') as f:
        pickle.dump(CACHED_RESPONSES, f)

def get_response(url):
    global CACHED_RESPONSES
    if url in CACHED_RESPONSES:
        print(f"Loading cached response: {url}")
        response = CACHED_RESPONSES[url]
        return response
    else:
        with requests.Session() as session:
            response = session.get(url)

        if response.status_code == 200:
            print(f"Successful get: {url}")
            print(f"    content length: {len(response.content)}")
            CACHED_RESPONSES[url] = response
            print(f"    cached: True")
            return response
        else:
            print("Error: unsuccessful get")
            print(f"    url: {url}")
            print(f"    status: {response.status_code}")
            return None
            # TODO(ben): Should this raise an exception instead?

def get_soup(response):
    return bs4.BeautifulSoup(response.content, 'html5lib')

def extract_tutorials(soup, root_url=""):
    premium_tutorials = {}
    non_premium_tutorials = {}

    cards = get_cards(soup)

    for card in cards:
        title, url = extract_card_info(card)
        if is_premium(card):
            premium_tutorials[title] = root_url + url
        else:
            non_premium_tutorials[title] = root_url + url

    return premium_tutorials, non_premium_tutorials

def get_cards(soup):
    return soup.findAll("div", {"class": "card border-0"})

def extract_card_info(card):
    body = card.find("div", {"class": "card-body"})
    title = body.find("h2").text
    url = body.find("a").attrs['href']
    return title, url

def extract_introduction(article_url):
    response = get_response(article_url)

    if response is not None:
        soup = get_soup(response)
        article_body = soup.find('div', {'class': 'article-body'})

        if article_body.find('h2') == None:
            raise MissingH2()

        # Introductory text is nested between divs at the beginning of the body.
        # As such, we begin by skipping over blank lines and divs:
        children = article_body.children
        while True:
            child = next(children)
            if isinstance(child, bs4.element.NavigableString) or child.name == 'div':
                continue
            else: break

        # Store all remaining non-div elements until we hit the next div
        intro = [child]
        while True:
            child = next(children)
            if child == '\n':
                continue
            elif child.name == 'div' or child.name == 'h2':
                break
            else:
                intro.append(child)

        return intro
    else:
        return None

def format_introduction(tag_list):
    intro = []
    for tag in tag_list:
        if isinstance(tag, bs4.element.NavigableString):
            if tag != '\n':
                raise UnexpectedNavigableString(f"tag == {tag}")
            else: continue
        for line in tag.decode().splitlines():
            intro.append(line)

    return intro

def is_premium(card):
    card_text = card.find("p", {"class": "card-text"})

    if card_text is None:
        raise MissingCardText()

    result = card_text.find("a", {"href": "/account/join/"})
    # Note: this assumes /account/join/ will always be the first anchor
    # within the card-text paragraph

    if result is None:
        return False   # Did not find hyperlink to /account/join/
    else:
        return True    # Found hyperlink to /account/join/

def write_to_markdown(url_dict, filename="file.md", title="# Title\n", is_premium=False):
    with open(filename, 'w') as file:
        lines = [title, '\n']
        
        for title, url in url_dict.items():
            lines.append(f"### [{title}]({url})\n")
            if not is_premium:
                # Write the introduction to the file
                lines.append('\n')
                try:
                    intro = extract_introduction(url)
                except MissingH2:
                    lines.append('> <p>No introduction available.</p>\n')
                else:
                    for line in format_introduction(intro):
                        lines.append('> ' + line + '\n')
                finally:
                    lines.append('\n')

        file.writelines(lines)

def fetch_tutorial_topics():
    response = get_response(ROOT_URL)
    soup = get_soup(response)
    topics_div = soup.find("div", {"class": "sidebar-module sidebar-module-inset border"})
    topic_anchors = topics_div.findAll("a", {"class": "badge badge-light text-muted"})

    topics = {
        anchor.text: ROOT_URL + anchor.attrs['href'] 
        for anchor in topic_anchors
    }

    return topics

def scrape_tutorial_topics(topic_list='all'):
    available_topics = fetch_tutorial_topics()

    if topic_list == 'all':
        topic_list = available_topics.keys()
    
    for topic in topic_list:
        if topic not in available_topics:
            raise TopicNotFound()

        print(f"Crawling `{topic}` tutorial pages...")

        premium = {}
        non_premium = {}

        # Iterate through all available pages until we cannot find new tutorials
        for i in count(start = 1):
            link = available_topics[topic] + f"page/{i}/"
            response = get_response(link)

            if response is not None: # TODO(ben): exception may be raised in the future
                soup = get_soup(response)
                p, np = extract_tutorials(soup, root_url=ROOT_URL)

                if found_new_tutorials(premium, p) or found_new_tutorials(non_premium, np):
                    print(f"    # Premium tutorials:     {len(premium):3d}")
                    print(f"    # Non-Premium tutorials: {len(non_premium):3d}")
                    continue
                else:
                    print("    No new tutorials found.")
                    break
            else:
                break

        print(f"Saving `{topic}` URLs into markdown...")

        write_to_markdown(
            premium, 
            filename=f"{topic}_premium_tutorials.md",
            title=f"# {topic}, premium tutorials from Real Python\n",
            is_premium=True)

        write_to_markdown(
            non_premium,
            filename=f"{topic}_non_premium_tutorials.md",
            title=f"# {topic}, non-premium tutorials from Real Python\n",
            is_premium=False)

def found_new_tutorials(original: dict, to_append: dict):
    """Check if all keys of `to_append` are in `original`. If not, update original."""
    difference = to_append.keys() - original.keys() # Set difference
    if difference != set():
        original.update(to_append)
        return True
    else:
        return False
    
def main():
    load_cached_responses(CACHE_FILENAME)

    # TODO(ben): accept command line arguments to specify topics
    try:
        scrape_tutorial_topics()
    finally:
        print("Saving cached responses...")
        save_cached_responses(CACHE_FILENAME)

if __name__ == "__main__":
    main()