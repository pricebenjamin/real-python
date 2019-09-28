import bs4
import re
import requests
import time

from collections import namedtuple
from datetime import datetime
from typing import List, Generator

# Local imports
from exceptions import CommentCountError


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


Card = namedtuple("Card", "title url is_premium date topic_tags")


def get_cards(soup: bs4.BeautifulSoup) -> Generator[Card, None, None]:
    tags = soup.find_all("div", "card border-0")
    for tag in tags:
        yield build_card_from_tag(tag)


date_re = re.compile(r"([A-Za-z]{3} \d+, \d{4})")


def build_card_from_tag(bs4_tag: bs4.element.Tag) -> Card:
    title = bs4_tag.find("h2", "card-title").text.strip()
    assert title

    url = bs4_tag.find("a").get("href")
    assert url

    is_premium = bool(bs4_tag.find("a", {"href": "/account/join/"}))

    match = date_re.search(bs4_tag.text)
    date = datetime.strptime(match.group(0), "%b %d, %Y") if match else None

    topic_tags = bs4_tag.find_all("a", "badge badge-light text-muted")
    topic_tags = tuple(topic_tags) if topic_tags else None
    # Above, we convert the bs4.element.ResultSet (the return value of find_all)
    # to a tuple in order to support hashing of the resulting Card object.

    return Card(title, url, is_premium, date, topic_tags)


def generate_count_query_url(article_url):
    # Real Python uses a disqus query to count comments on a given article
    disqus_url = "https://realpython.disqus.com/count-data.js"
    return disqus_url + "?1=" + requests.utils.quote(article_url, safe="")


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


def has_multiple_pages(soup) -> bool:
    return bool(soup.find("nav", {"aria-label": "Page Navigation"}))
