import itertools
import textwrap

import fetch  # TODO: move functions out of `fetch.py` and into `utils.py`

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


class Tutorial:
    def __init__(self, title, url):
        self.title: str = title
        self.url: str = url
        self.soup = None  # TODO: implement + use this attribute
        self._has_author = None
        self._author = None
        self._has_date = None
        self._date = None
        self._has_tags = None
        self._tags = None
        self._has_comment_count = None
        self._comment_count = None
        self._has_metadata_string = None
        self._markdown_metadata_string = None
        self._markdown_introduction = None
        self._toc = None

    @property
    def has_author(self):
        if self._has_author is None:
            # TODO: Compute
            # define self._author
            pass
        return self._has_author

    @property
    def author(self):
        if self.has_author:
            return self._author
        raise AttributeError(f"{repr(self)} does not have an author")

    @property
    def has_date(self):
        if self._has_date is None:
            # TODO: Compute
            # define self._date
            pass
        return self._has_date

    @property
    def date(self):
        if self.has_date:
            return self._date
        raise AttributeError(f"{repr(self)} does not have a date")

    @property
    def has_comment_count(self):
        if self._has_comment_count is None:
            # TODO: Compute
            # define self._comment_count
            pass
        return self._has_comment_count

    @property
    def comment_count(self):
        if self.has_comment_count:
            return self._comment_count
        raise AttributeError(f"{repr(self)} does not have a comment count")

    @property
    def has_metadata_string(self):
        if self._has_metadata_string is None:
            if self._has_author and self._has_tags and self._has_comment_count:
                self._has_metadata_string = True
            else:
                self._has_metadata_string = False
            # Computation of the string is delegated to the
            # markdown_metatdata_string getter (below)
        return self._has_metadata_string

    @property
    def markdown_metadata_string(self):
        if self.has_metadata_string:  # If true, then self is known to have
            # author, tags, and comment count.
            # See `has_metadata_string` getter (above)
            if self._markdown_metadata_string is None:
                self._markdown_metadata_string = (
                    # TODO: Tutorial must be able to requests link id's from Topic
                    # in order to make this function work...
                    generate_metadata_string(
                        self._author,
                        self._date,
                        self._tags,
                        self._comments,
                        self._links,  # TODO: self._links does not yet exist...
                    )
                )
            return self._markdown_metadata_string
        raise AttributeError(f"{repr(self)} does not have a metadata string")

    @property
    def markdown_introduction(self):
        if self._markdown_introduction is None:
            # TODO: Compute
            # TODO: figure out metadata + intro for premium articles...
            pass
        return self._markdown_introduction

    @property
    def toc(self):
        if self._toc is None:
            # TODO: implement + compute
            pass
        return self._toc

    def __repr__(self):
        # TODO
        pass


class Topic:
    def __init__(self, name, url, include_premium):
        self.name: str = name
        self.url: str = url
        self.link_counter = itertools.count(start=1)
        self.include_premium: bool = include_premium

    @property
    def tutorials(self):
        return self.tutorial_generator()

    def tutorial_generator(self):
        response = fetch.get_reponse(self.url)
        soup = fetch.get_soup(response)
        cards = fetch.get_cards(soup)

        for card in cards:
            title, url = fetch.extract_card_info(card)
            premium = fetch.is_premium(card)
            if not premium:
                yield Tutorial(title=title, url=url, topic=self)
                # Tutorials must be able to access their Topic's link_counter
            elif include_premium:
                yield Tutorial(title=title, url=url, topic=self)


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
                url=available_topics[topic],
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
