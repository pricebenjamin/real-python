# Rewrite `fetch.py` for maintainability

I'm not an expert on how to write maintainable code, but you tend to get better at things by practicing. I'll try to include citations to books or articles that talk about maintainability and best practices.


## Add type hints

Some functions do not have obvious return type, e.g. `format_introduction`, `extract_tutorials`


## Untangle the spaghetti

Currently, the call graph looks like this.
```
CACHED_RESPONSES = {}
session = requests.Session()

main
  ├ load_cached_responses     # updates global CACHED_RESPONSES dict
  ├ scrape_tutorial_topics
  │   ├ fetch_tutorial_topics
  │   │   ├ get_response      # updates CACHED_RESPONSES
  │   │   └ get_soup
  │   ├ get_response
  │   ├ get_soup
  │   ├ extract_tutorials
  │   │   ├ get_cards
  │   │   ├ extract_card_info
  │   │   └ is_premium
  │   ├ found_new_tutorials   # confusingly named, probably
  │   └ write_to_markdown
  │       ├ get_response
  │       ├ get_soup
  │       ├ extract_metadata
  │       │   ├ get_metadata_element
  │       │   ├ generate_count_query_url
  │       │   ├ get_response
  │       │   └ extract_comment_count
  │       ├ generate_metadata_string_and_append_links
  │       └ extract_introduction
  ├ save_cached_responses
  └ session.close()
```

Honestly, the call graph could be *much* worse. However, some functions are not used outside of a particular scope.

Example 1: `get_cards` and `extract_card_info` are only ever called from within `extract_tutorials`. Perhaps these two functions should be *methods* of some callable `TutorialExtractor` class.

Example 2: `extract_introduction` and `format_introduction` are only ever called from within `write_to_markdown`.

Encapsulating these functions will help clean up the top-level of the script when folded.

However, `scrape_tutorial_topics` has the opposite problem. It does not provide *meaningful* encapsulation. In fact it gets in the way; in order to understand what `main` *does*, you must follow the call. ~I believe I did this because the code within `scrape_tutorial_topics` was ugly. However, instead of making it better, I hid it away...*tsk tsk*~ Actually, the main motivation for moving this logic into a separate function was to enable fetching of a particular topic list, e.g.
```python
scrape_tutorial_topics('advanced', 'intermediate')
```
This lays some ground work for later enabling command-line arguments.


## Create cache context manager

Currently...
```python
def main():
    # Populate global dictionary CACHED_RESPONSES
    load_cached_responses(CACHE_FILENAME)

    try:
        scrape_tutorial_topics() # makes calls that access global dict
    finally:
        save_cached_responses(CACHE_FILENAME)
```

Considering...
```python
with Scraper() as scraper:
    scraper.scrape_tutorial_topics('all')
```

where the Scraper class looks something like...
```python
class Scraper:
    __init__(self, cache_filename='cached_responses.pickle'):
        self.cache = {}
        self.cache_filename = cache_filename
        self.sess = None

    def __enter__(self):
        try:
            with open(self.cache_filename, 'r') as f:
                prev_cache = pickle.load(f)
        except IOError as e:
            print(f"Cache not loaded. ({e})")
        else:
            self.cache.update(prev_cache)
        self.sess = requests.Session()
        return self

    def __exit__(self):
        with open(self.cache_filename, 'w') as f:
            pickle.dump(self.cache, f)
        self.sess.close()

    def get_response(self, url):
        if url in self.cache:
            return self.cache[url]
        response = self.sess.get(url)

        # Check that response is good or raise error
        ...

        self.cache[url] = response
        return response

    # All the other methods...
```

Try to find examples of context managers serving as a cache.
