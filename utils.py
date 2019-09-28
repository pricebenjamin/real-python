import bs4
import re
import requests
import time

from bs4.element import Tag
from datetime import datetime
from typing import List

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
