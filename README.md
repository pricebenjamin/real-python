# Aggregating all non-premium, intermediate tutorials on Real Python

## Goal
Create a collection of URLs to tutorials on [Real Python](https://realpython.com)
that are tagged as `intermediate` but not marked for premium users.

## Strategy
1. Use the `requests` library to crawl across all pages in the [intermediate](https://realypython.com/tutorials/intermediate) category.
2. Navigate the HTML, finding rows whose `card-text` does not contain a hyperlink to `/account/join/`.
3. Extract `card-titles` and URLs.