# Add metadata to output

## Target output

```markdown
# advanced, non-premium tutorials from Real Python

## [Your Guide to the CPython Source Code](https://realpython.com/cpython-source-code-guide/)
by [Anthony Shaw][1] on Aug 21, 2019 with tags: [advanced][2], [python][3] ([9 comments][4])

Are there certain parts of Python that just seem magic? Like how are dictionaries so much faster than looping over a list to find an item. How does a generator remember the state of the variables each time it yields a value and why do you never have to allocate memory like other languages? It turns out, CPython, the most popular Python runtime is written in human-readable C and Python code. This tutorial will walk you through the CPython source code. 

You’ll cover all the concepts behind the internals of CPython, how they work and visual explanations as you go.

__You’ll learn how to:__

*   Read and navigate the source code
*   Compile CPython from source code
*   Navigate and comprehend the inner workings of concepts like lists, dictionaries, and generators
*   Run the test suite
*   Modify or upgrade components of the CPython library to contribute them to future versions

Yes, this is a very long article. If you just made yourself a fresh cup of tea, coffee or your favorite beverage, it’s going to be cold by the end of Part 1. 

This tutorial is split into five parts. Take your time for each part and make sure you try out the demos and the interactive components. You can feel a sense of achievement that you grasp the core concepts of Python that can make you a better Python programmer.

[1]: https://realpython.com/cpython-source-code-guide/#author
[2]: https://realpython.com/tutorials/advanced/
[3]: https://realpython.com/tutorials/python/
[4]: https://realpython.com/cpython-source-code-guide/#reader-comments
```

## Metadata Objects

```python
Author = namedtuple('Author', 'name link')
Date = time.struct_time  # Must be parsed out of the html
Tag = namedtuple('Tag', 'name link')
Comments = namedtuple('Comments', 'count link')
Link = namedtuple('Link', 'id url')
```

## How do we generate the metadata string if some metadata is missing?

First, we might ask what are the possible combinations of metadata?

If we consider each object to be `missing := 0` or `not missing := 1`, then we can express each possibility as a string. For example, the string `1101` means
```
1 1 0 1
- - - -
| | | |
| | | ----- Comments: not missing
| | ------- Tags:     missing
| --------- Date:     not missing
----------- Author:   not missing
```

Instead of handling every possible combination, we should reduce the number of cases to those that we actually observe. We can query the cache of articles to determine the most common combinations, handle those cases, and ignore the rest.

## Extraction details

By inspecting a web page with all desired details, we find:

* premium tutorials are structured differently from non-premium ([example](https://realpython.com/courses/python-debugging-pdb/))

The following is a list of the first few children of `<div class="col-md-11 col-lg-8 article">` ([source](https://realpython.com/pygame-a-primer/))
```html
<figure class="embed-responsive embed-responsive-16by9">
    <img class="card-img-top m-0 p-0 embed-responsive-item rounded" style="object-fit: contain;" alt="..." src="..." width="1920" height="1080" srcset="..., ..., ..." sizes="75vw">
</figure>
<h1>PyGame: A Primer on Game Programming in Python</h1>
<p>
    <span class="text-muted">
        by 
        <a class="text-muted" href="#author">Jon Fincher</a>
        <span class="ml-2 fa fa-clock-o"></span> 
        Sep 16, 2019
        <span class="ml-2 mr-1 fa fa-comments"></span>
        <a class="text-muted" href="#reader-comments">
            <span class="disqus-comment-count" data-disqus-identifier="...">38 Comments</span>
        </a>
        <span class="ml-2 fa fa-tags"></span>
        <a href="/tutorials/intermediate/" class="badge badge-light text-muted">intermediate</a>
        <br>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-twitter text-light">
            <i class="mr-1 fa fa-twitter text-light"></i>
            Tweet
        </a>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-facebook text-light">
            <i class="mr-1 fa fa-facebook text-light"></i>
            Share
        </a>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-red text-light">
            <i class="mr-1 fa fa-envelope text-light"></i>
            Email
        </a>
    </span>
</p>
```

Q: What does an article look like when missing author / date / etc?
A: It appears that *all* articles have an author, but many say "by Real Python". However, not all articles include dates ([example](https://realpython.com/testing-in-django-part-2-model-mommy-vs-django-testing-fixtures/)).

Q: Do all articles contain exactly one `<span class="text-muted">`?
A: This appears to be the case. (Checked all cached articles.)

```html
<p>
    <span class="text-muted">
        by 
        <a class="text-muted" href="/">Real Python</a>
        <span class="ml-2 mr-1 fa fa-comments"></span>
        <a class="text-muted" href="#reader-comments">
            <span class="disqus-comment-count" data-disqus-identifier="...">11 Comments</span>
        </a>
        <span class="ml-2 fa fa-tags"></span>
        <a href="/tutorials/advanced/" class="badge badge-light text-muted">advanced</a>
        <a href="/tutorials/django/" class="badge badge-light text-muted">django</a>
        <a href="/tutorials/testing/" class="badge badge-light text-muted">testing</a>
        <a href="/tutorials/web-dev/" class="badge badge-light text-muted">web-dev</a>
        <br>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-twitter text-light">
            <i class="mr-1 fa fa-twitter text-light"></i>
            Tweet
        </a>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-facebook text-light">
            <i class="mr-1 fa fa-facebook text-light"></i>
            Share
        </a>
        <a target="_blank" rel="nofollow" href="..." class="mr-1 badge badge-red text-light">
            <i class="mr-1 fa fa-envelope text-light"></i>
            Email
        </a>
    </span>
</p>
```

## Find author

```python
def findAuthor(soup):
    article = soup.find('div', 'article')
    author = article.find('a', {'href': '#author'}) # Do all authors have links?
    return author # Note: may return None
```

## Check for types of metadata

```python
def hasDate(soup):
    return soup.find('span', 'fa-clock-o') # Note: returned element does not contain date text
```

```python
def hasComments(soup):
    return soup.find('span', 'fa-comments')
```

```python
def hasTags(soup):
    return soup.find('span', 'fa-tags')
```

```python
def hasAuthor(soup, url):
    article = soup.find('div', 'article')
    if not article:
        raise MissingArticle(url)
    tm_spans = article.findAll('span', 'text-muted')
    if len(tm_spans) != 1:
        msg = ("given article did not contain exactly one child of the "
               "form <span class=\"text-muted\">\n\n"
               "# spans: {len(tm_spans)}\n"
               "url: {url}")
        raise UnexpectedStructure(msg)
    first_child = next(metadata_soup)
    return first_child == 'by '
```

## Helper functions?

```python
def getMetadataElement(soup, url):
    """Find, validate, and return the metadata element within soup.

    This function expects to find a particular <span> element from within
    the given `soup`. We refer to this span element as "the metadata element"
    because it contains the article's metadata (author, date, tags).
    """
    article = soup.find('div', 'article')
    if not article:
        raise MissingArticle(url)

    # The first instance of <span class="text-muted"> is the desired element
    metadata = article.find('span', 'text-muted')
    if not metadata:
        raise MissingMetadata(url)

    # Ensure we've found the desired element by examining its first child
    first_child = next(metadata.children)
    if not first_child == 'by ':
        msg = (f"first_child={first_child} at {url}")
        raise UnexpectedFirstChild(msg)
    return metadata
```

## Known problems

The number of comments on a given article is determined after the page has loaded. As such, the content of `get_response(url)` will not contain this information. We may be able to load the full web page using `phantomJS` or the `webbrowser` libraries, but this would be costly.