import bs4
import html2markdown
import itertools
import os
import requests
import requests_cache

from bs4.element import NavigableString, Tag
from collections import namedtuple
from datetime import datetime
from typing import Optional, List
from urllib.parse import urljoin

# Local imports
import utils
from exceptions import UnsuccessfulGet, TopicsError


Author = namedtuple("Author", "name url")
Date = datetime
Tag = namedtuple("Tag", "name url")
Comments = namedtuple("Comments", "count url")


REQUESTS_CACHE_FILE = "requests_cache"
requests_cache.install_cache(REQUESTS_CACHE_FILE)
default_headers = requests.utils.default_headers()


class Summarizer:

    BASE_URL = "https://realpython.com"
    GITHUB_URL = "https://github.com/pricebenjamin/real-python"
    available_topics = None
    user_agent = " ".join([default_headers["User-Agent"], GITHUB_URL])

    def __init__(self, selected_topics="all", include_premium=True, output_dir=None):
        self.selected_topics = self.validate_topics(selected_topics)
        self.include_premium = include_premium

        if output_dir is not None:
            assert isinstance(output_dir, str)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        self.output_dir = output_dir

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    @property
    def topics(self):
        return self.topic_generator()

    def topic_generator(self):
        for topic in self.selected_topics:
            yield Topic(
                name=topic,
                url=self.available_topics[topic],
                summarizer=self,  # Topics need access to Summarizer's get_response method
            )

    def get_response(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            print(f"Successful get: {url}")
            print(f"    content length: {len(response.content)}")
            print(f"    from cache: {response.from_cache}")
            return response
        elif response.status_code == 429:
            print("Received status code 429: Too many requests.")
            retry_after = response.headers.get("Retry-After", "")
            try:
                count = int(retry_after)
            except ValueError:
                count = 10
            utils.sleep_for(count)  # TODO: implement more robust rate-limiting
            return self.get_response(url)
        else:
            print("Error: unsuccessful get")
            print(f"    url: {url}")
            print(f"    status: {response.status_code}")
            raise UnsuccessfulGet(url)

    # TODO: Write tests for class methods!
    @classmethod
    def validate_topics(cls, topic_list):
        if topic_list == "all" or isinstance(topic_list, list):  # Fail early
            if cls.available_topics is None:
                cls.fetch_available_topics()
            if topic_list == "all":
                return list(cls.available_topics.keys())
            if all(t in cls.available_topics for t in topic_list):
                return topic_list
        raise TopicsError(TopicsError.default_message)

    @classmethod
    def fetch_available_topics(cls):
        if cls.available_topics is None:
            with requests.Session() as sess:
                response = sess.get(cls.BASE_URL)
                assert (
                    response.status_code == 200
                )  # TODO: Re-implement get_response as static/class method?
            soup = utils.get_soup(response)

            topics_div = soup.find("div", "sidebar-module sidebar-module-inset border")
            assert topics_div  # TODO: consider raising helpful exceptions

            topic_anchors = topics_div.find_all("a", "badge badge-light text-muted")
            assert topic_anchors  # TODO: consider raising helpful exceptions

            cls.available_topics = {
                anchor.text.strip(): urljoin(cls.BASE_URL, anchor.attrs["href"])
                for anchor in topic_anchors
            }
        return list(cls.available_topics.keys())

    def __del__(self):
        self.session.close()


class Topic:
    def __init__(self, name, url, summarizer):
        self.name: str = name
        self.url: str = url
        self.summarizer: Summarizer = summarizer

    @property
    def tutorials(self):
        return self.tutorial_generator()

    def tutorial_generator(self):
        response = self.summarizer.get_response(self.url)
        soup = utils.get_soup(response)
        cards = utils.get_cards(soup)

        for card in cards:
            title, url, premium, date, tags = utils.extract_card_info(card)
            if not premium or self.summarizer.include_premium:
                yield Tutorial(
                    title=title,
                    url=urljoin(self.summarizer.BASE_URL, url),
                    is_premium=premium,
                    date=date,
                    tags=tags,
                    topic=self,
                )


class Tutorial:
    def __init__(
        self,
        title: str,
        url: str,
        is_premium: bool,
        date: Optional[datetime],
        tags: Optional[List[bs4.element.Tag]],
        topic: Topic,
    ):
        # Already known attributes
        self.title = title
        self.url = url
        self.is_premium = is_premium
        self.topic = topic  # Allows access to topic.summarizer.get_response
        self.BASE_URL = self.topic.summarizer.BASE_URL  # alias to save typing

        self.markdown_title = f"## [{self.title}]({self.url})"

        if date is not None:
            self._has_date = True
            self._date = date
        else:
            self._has_date = False
            self._date = None

        # Partially determined properties
        if tags is not None:
            self._has_tags = True
            self._raw_tags = tags
        else:
            self._has_tags = False
        self._tags = None

        # Lazily determined properties
        self._soup = None
        self._behind_paywall = None
        self._metadata_element = None

        self._has_author = None
        self._author = None
        self._has_comments = None
        self._comments = None
        self._has_metadata_string = None
        self._markdown_metadata_string = None
        self._markdown_introduction = None
        self._toc = None

    @property
    def soup(self):
        if self._soup is None:
            response = self.topic.summarizer.get_response(self.url)
            self._soup = utils.get_soup(response)
        assert self._soup
        return self._soup

    @property
    def behind_paywall(self):
        if self._behind_paywall is None:
            self._behind_paywall = "Membership" in self.soup.find("title").text
        return self._behind_paywall

    @property
    def metadata_element(self):
        if self._metadata_element is None:
            tags = self.soup.find("span", "fa-tags")
            assert tags
            self._metadata_element = tags.parent
        assert self._metadata_element
        return self._metadata_element

    @property
    def has_author(self):
        if self.behind_paywall:
            self._has_author = False
        elif self._has_author is None:
            metadata = self.metadata_element
            author = (
                metadata.find("a", {"href": "#author"})
                or metadata.find("a", {"href": "#team"})
                or metadata.find("a", {"class": "text-muted", "href": "/"})
            )
            if author:
                self._has_author = True
                name = author.text.strip()
                url = urljoin(self.url, author.attrs["href"])
                self._author = Author(name, url)
            else:
                self._has_author = False
        return self._has_author

    @property
    def author(self):
        if self.has_author:
            return self._author
        raise AttributeError(f"{self!s} does not have an author")

    @property
    def has_date(self):
        return self._has_date

    @property
    def date(self):
        if self._has_date:
            return self._date
        raise AttributeError(f"{self!s} does not have a date")

    @property
    def has_tags(self):
        return self._has_tags

    @property
    def tags(self):
        if self._has_tags:
            if self._tags is None:
                # Generate list of tags from _raw_tags
                self._tags = [
                    Tag(name=tag.text, url=urljoin(self.url, tag.attrs["href"]))
                    for tag in self._raw_tags
                ]
            return self._tags
        raise AttributeError(f"{self!s} does not have any tags")

    @property
    def has_comments(self):
        if self._has_comments is None:
            if "/courses/" in self.url or self.is_premium:
                # Note: we do not need to check self.behind_paywall
                # because checking self.is_premium is sufficient
                # to know that comments are not available
                self._has_comments = False
            else:
                comments = self.metadata_element.find("a", {"href": "#reader-comments"})
                self._has_comments = bool(comments)
        return self._has_comments

    @property
    def comments(self):
        if self.has_comments:
            if self._comments is None:
                comments = self.metadata_element.find("a", {"href": "#reader-comments"})
                disqus = self.metadata_element.find("span", "disqus-comment-count")
                query_url = utils.generate_count_query_url(
                    disqus.attrs["data-disqus-identifier"]
                )
                response = self.topic.summarizer.get_response(query_url)
                count = utils.extract_comment_count(response)
                url = urljoin(self.url, comments.attrs["href"])
                self._comments = Comments(count, url)
            return self._comments
        raise AttributeError(f"{self!s} does not have any comments")

    @property
    def has_metadata_string(self):
        # TODO: make work with courses (i.e., premium tutorials)
        if self._has_metadata_string is None:
            self._has_metadata_string = (
                self.has_author and self.has_tags and self.has_comments
            )
        return self._has_metadata_string

    @property
    def markdown_metadata_string(self):
        if self.has_metadata_string:
            if self._markdown_metadata_string is None:
                tag_links = ", ".join([f"[{tag.name}]({tag.url})" for tag in self.tags])

                comments_text = (
                    "{} comments" if self.comments.count != 1 else "{} comment"
                )
                comments_text = comments_text.format(self.comments.count)
                comments_link = f"[{comments_text}]({self.comments.url})"

                metadata_string = (
                    f"by [{self.author.name}]({self.author.url}) "
                    + (
                        f"on {self.date.strftime('%a, %d %b %Y')} "
                        if self.has_date
                        else ""
                    )
                    + f"with tags: {tag_links} "
                    + f"({comments_link})"
                )

                self._markdown_metadata_string = metadata_string
            return self._markdown_metadata_string
        raise AttributeError(f"{self!s} does not have a metadata string")

    @property
    def markdown_introduction(self):
        if self._markdown_introduction is None:
            if self.behind_paywall:
                self._markdown_introduction = (
                    "> No introduction available (behind paywall)"
                )
                return self._markdown_introduction

            article_body = self.soup.find("div", "article-body")
            if "/courses/" in self.url or self.is_premium:
                mb4 = article_body.find("div", "mb-4")
                assert mb4
                intro = [
                    child
                    for child in mb4.children
                    if not isinstance(child, NavigableString)
                ]
            else:
                inside_intro = False
                ab_children = article_body.children
                while not inside_intro:
                    child = next(ab_children)
                    if isinstance(child, NavigableString) or child.name != "p":
                        continue
                    else:
                        inside_intro = True
                intro = [child]
                while inside_intro:
                    child = next(ab_children)
                    if child.name == "div" or (child.name == "p" and child.attrs):
                        # Note: checking if child.attrs is empty is an attempt to catch
                        # interview articles such as
                        # https://realpython.com/interview-katrina-durance/
                        inside_intro = False
                    elif not isinstance(child, NavigableString):
                        intro.append(child)

            self._markdown_introduction = "\n\n".join(
                [html2markdown.convert(tag.decode()) for tag in intro]
            )
        return self._markdown_introduction

    @property
    def toc(self):
        if self._toc is None:
            # TODO: implement + compute
            pass
        return self._toc

    def __str__(self):
        cls = type(self).__name__
        short_title = self.title.split(" ")[:5]
        return f"{cls}(title={' '.join(short_title)}...)"

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}(title={self.title!r}, url={self.url!r})"
