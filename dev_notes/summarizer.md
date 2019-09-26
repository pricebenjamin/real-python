# The ``Summarizer`` API

The ``Summarizer`` API is an adapter to the core logic contained within
``fetch.py``. It should enable me to modify and mangle the current code while
maintaining a consistent user interface.

## Target interface

```python
from operator import attrgetter
from summarizer import Summarizer

def main():
    summarizer = Summarizer(
        selected_topics='all',
        include_premium=False,
    )

    for topic in summarizer.topics:
        # Create a filename using the topic string
        with open(f"{topic}_tutorials.md", 'w') as dest:

            markdown_title = f"# {topic.capitalize()} tutorials from Real Python"
            dest.write(markdown_title + '\n\n')

            # Remove tutorials that are missing dates / comment counts
            # (This is only necessary if you wish to sort by date)
            tutorials = (
                t for t in topic.tutorials if t.has_date and t.has_comment_count
            )

            # Sort tutorials before writing to file
            for tutorial in sorted(
                tutorials,
                key=attrgetter('date', 'comment_count'),
                reverse=True
            ):
                # metadata string includes author, date, tags, and comment count
                dest.write(tutorial.markdown_metadata_string + '\n\n')

                dest.write(tutorial.markdown_introduction + '\n\n')

                # write table of contents, if available
                dest.write(tutorial.toc + '\n\n') if tutorial.has_toc

if __name__ == "__main__":
    main()
```


### Concept: ``selected_topics`` can accept special value ``"all"``

The following are both valid
```python
s1 = Summarizer(selected_topics="all")
s2 = Summarizer(selected_topics=["advanced", "intermediate"])
```

But what should happen in the following cases?
```python
s3 = Summarizer(selected_topics=["all"])
s4 = Summarizer(selected_topics=["all", "advanced", "intermediate"])
s5 = Summarizer(selected_topics=("all",))
s6 = Summarizer(selected_topics=("advanced", "intermediate"))
```

Be strict and fail fast.

```python
class Summarizer:
    available_topics = None
    def __init__(self, selected_topics="all", include_premium=True):
        self.topics = Summarizer.validate_topics(selected_topics)
        ...

    @staticmethod
    def validate_topics(topic_list):
        if topic_list == "all" or isinstance(topic_list, list):  # Fail fast
            if Summarizer.available_topics is None:
                Summarizer.fetch_available_topics()
            if topic_list == "all":
                return Summarizer.available_topics
            if all((t in Summarizer.available_topics) for t in topic_list):
                return topic_list
        raise TopicsError()  # TODO
```

We'll reject everything else and raise an exception with a helpful message.
```
TopicsError: Key-word argument `topics` must be either
    (1) a list of valid topic strings OR
    (2) the string "all".

A list of valid topics can be obtained with

    Summarizer.fetch_available_topics()
```

***

## Idea: Search for articles with certain attributes
What if I want to fetch articles with the following properties
* ``'advanced', 'django' in article.tags``
* ``article.date.year >= 2018``
* ``article.author = "Anthony Shaw" or artile.author == "Realy Python``

In that case, maybe it makes sense to start with the default object
```python
s = Summarizer()
```
Then add some criteria
```python
s.search_criteria.append(
    lambda article:
        'advanced' in article.tags
        and 'django' in article.tags
        and article.date >= 2018
        and (
            article.author == "Anthony Shaw"
            or article.author == "Real Python"
        )
)
```
Here, ``search_criteria`` is a list of functions of the form ``(article) -> bool``.
