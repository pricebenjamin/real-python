import textwrap


class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class CommentCountError(Error):
    """utils.extract_comment_count
    The data returned by disqus could not be parsed."""


class TopicsError(Error):
    """Summarizer.validate_topics
    Invalid value passed to `selected_topics` parameter."""

    default_message = textwrap.dedent(
        """\n
        Key-word argument `selected_topics` must be either
            (1) a list of valid topic strings OR
            (2) the string "all"

        A list of valid topics can be obtained with

            Summarizer.fetch_available_topics()
        """
    )


class GetResponseError(Error):
    """Base-class for errors raised by the Summarizer.get_response function."""


class UnsuccessfulGet(GetResponseError):
    """Summarizer.get_response
    Received an unexpected response code."""
