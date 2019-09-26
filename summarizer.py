import itertools
import bs4
import html2markdown
import textwrap

import fetch  # TODO: move functions out of `fetch.py` and into `utils.py`

from collections import namedtuple
from datetime import datetime
from typing import Optional


class TopicsError(Exception):
    default_message = textwrap.dedent(
        """\n
        Key-word argument `selected_topics` must be either
            (1) a list of valid topic strings OR
            (2) the string "all"

        A list of valid topics can be obtained with

            Summarizer.fetch_available_topics()
        """
    )


Author = namedtuple("Author", "name link")
Date = datetime
Tag = namedtuple("Tag", "name link")
Comments = namedtuple("Comments", "count link")
Link = namedtuple("Link", "id url")

# Metadata = namedtuple("Metadata", "author date tags comments")


class Summarizer:

    available_topics = None

    def __init__(self, selected_topics="all", include_premium=True):
        self.selected_topics: List[str] = Summarizer.validate_topics(selected_topics)
        self.include_premium: bool = include_premium

    @property
    def topics(self):
        return self.topic_generator()

    def topic_generator(self):
        for topic in self.selected_topics:
            yield Topic(
                name=topic,
                url=self.available_topics[topic],
                include_premium=self.include_premium,
            )

    # TODO: Write tests for static methods!
    @staticmethod
    def validate_topics(topic_list):
        if topic_list == "all" or isinstance(topic_list, list):  # Fail early
            if Summarizer.available_topics is None:
                Summarizer.fetch_available_topics()
            if topic_list == "all":
                return list(Summarizer.available_topics.keys())
            if all(t in Summarizer.available_topics for t in topic_list):
                return topic_list
        raise TopicsError(TopicsError.default_message)

    @staticmethod
    def fetch_available_topics():
        if Summarizer.available_topics is None:
            Summarizer.available_topics = fetch.fetch_tutorial_topics()
            # TODO: should this function continue to return a dictionary?
        return list(Summarizer.available_topics.keys())


class Topic:
    def __init__(self, name, url, include_premium):
        self.name: str = name
        self.url: str = url
        self._link_counter = itertools.count(start=1)
        self.include_premium: bool = include_premium

    @property
    def tutorials(self):
        return self.tutorial_generator()

    @property
    def link_counter(self):
        return self._link_counter

    def tutorial_generator(self):
        response = fetch.get_response(self.url)
        soup = fetch.get_soup(response)
        cards = fetch.get_cards(soup)

        for card in cards:
            title, url = fetch.extract_card_info(card)
            premium = fetch.is_premium(card)
            if not premium or self.include_premium:
                yield Tutorial(
                    title=title,
                    url=(fetch.ROOT_URL + url),
                    is_premium=premium,
                    parent_topic=self,
                )


class Tutorial:
    def __init__(
        self, title: str, url: str, is_premium: bool = None, parent_topic: Topic = None
    ):
        # Already known attributes
        self.title = title
        self.url = url
        self.parent_topic = parent_topic  # Allows access to link_counter
        self.is_premium = is_premium

        # Lazily determined properties
        self._has_soup = None
        self._soup = None
        self._has_author = None
        self._author = None
        self._has_date = None
        self._date = None
        self._has_tags = None
        self._tags = None
        self._has_comments = None
        self._comments = None
        self._has_metadata_element = None
        self._metadata_element = None
        self._has_metadata_string = None
        self._markdown_metadata_string = None
        self._markdown_introduction = None
        self._toc = None
        self._markdown_references = []

    @property
    def has_soup(self):
        if self._has_soup is None:
            response = fetch.get_response(self.url)
            self._soup = fetch.get_soup(response)
            self._has_soup = True
        return self._has_soup

    @property
    def soup(self):
        if self.has_soup:
            return self._soup
        raise AttributeError(f"{self!s} does not have any soup")

    @property
    def has_author(self):
        if self._has_author is None:
            metadata = self.metadata_element
            author = (
                metadata.find("a", {"href": "#author"})
                or metadata.find("a", {"href": "#team"})
                or metadata.find("a", {"class": "text-muted", "href": "/"})
            )
            if author:
                self._has_author = True
                name = author.text.strip()
                url = fetch.ROOT_URL if author.attrs["href"] == "/" else self.url
                link = Link(
                    id=next(self.parent_topic.link_counter),
                    url=(url + author.attrs["href"]),
                )
                self._author = Author(name, link)
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
        if self._has_date is None:
            above_date = self.metadata_element.find("span", "fa-clock-o")
            date = above_date.nextSibling if above_date else None
            if date:
                self._has_date = True
                date = date.strip()
                date = datetime.strptime(date, "%b %d, %Y")
                self._date = date
            else:
                self._has_date = False
        return self._has_date

    @property
    def date(self):
        if self.has_date:
            return self._date
        raise AttributeError(f"{self!s} does not have a date")

    @property
    def has_tags(self):
        if self._has_tags is None:
            tags = self.metadata_element.findAll("a", "badge badge-light text-muted")
            if tags:
                self._has_tags = True
                self._tags = [
                    Tag(
                        name=tag.text.strip(),
                        link=Link(
                            id=next(self.parent_topic.link_counter),
                            url=fetch.ROOT_URL + tag.attrs["href"],
                        ),
                    )
                    for tag in tags
                ]
            else:
                self._has_tags = False
        return self._has_tags

    @property
    def tags(self):
        if self.has_tags:
            return self._tags
        raise AttributeError(f"{self!s} does not have any tags")

    @property
    def has_comments(self):
        if self._has_comments is None:
            comments = self.metadata_element.find("a", {"href": "#reader-comments"})
            if comments:
                self._has_comments = True
                disqus = self.metadata_element.find("span", "disqus-comment-count")
                query_url = fetch.generate_count_query_url(
                    disqus.attrs["data-disqus-identifier"]
                )
                response = fetch.get_response(query_url)
                count = fetch.extract_comment_count(response)
                link = Link(
                    id=next(self.parent_topic.link_counter),
                    url=(self.url + comments.attrs["href"]),
                )
                self._comments = Comments(count, link)
            else:
                self._has_comments = False
        return self._has_comments

    @property
    def comments(self):
        if self.has_comments:
            return self._comments
        raise AttributeError(f"{self!s} does not have any comments")

    @property
    def has_metadata_element(self):
        if self._has_metadata_element is None:
            try:
                self._metadata_element = fetch.get_metadata_element(self.soup, self.url)
            except fetch.MetadataError as e:
                print(e)
                self._has_metadata_element = False
            else:
                self._has_metadata_element = True
        return self._has_metadata_element

    @property
    def metadata_element(self):
        if self.has_metadata_element:
            return self._metadata_element
        raise AttributeError(f"{self!s} does not have a metadata element")

    @property
    def has_metadata_string(self):
        if self._has_metadata_string is None:
            if self.has_author and self.has_tags and self.has_comments:
                self._has_metadata_string = True
            else:
                self._has_metadata_string = False
            # Computation of the string is delegated to the
            # markdown_metadata_string getter (below)
        return self._has_metadata_string

    @property
    def markdown_metadata_string(self):
        if self.has_metadata_string:
            # If true, then self is known to have author, tags, and comment count.
            # See `has_metadata_string` getter (above)
            if self._markdown_metadata_string is None:

                if self.has_date:
                    # Ensures that self._date has been computed, if it exists
                    pass

                self._markdown_metadata_string = fetch.generate_metadata_string_and_append_links(
                    self._author,
                    self._date,
                    self._tags,
                    self._comments,
                    self._markdown_references,
                )
            return self._markdown_metadata_string
        raise AttributeError(f"{self!s} does not have a metadata string")

    @property
    def markdown_introduction(self):
        if self._markdown_introduction is None:
            try:
                intro = fetch.extract_introduction(self.soup, self.url)
            except fetch.MissingH2:
                self._markdown_introduction = ["> No introduction available."]
            else:
                self._markdown_introduction = [
                    html2markdown.convert(tag.decode()) + "\n\n" for tag in intro
                ]
            # TODO: figure out metadata + intro for premium articles...
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
