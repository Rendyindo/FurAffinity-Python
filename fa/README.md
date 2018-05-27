# FurAffinity-Python

An API-like wrapper for FurAffinity, written in Python 3.6.

## Dependencies

- `requests`
- `bs4`
- `selenium` - Chrome

## Getting Started

1. [Set up Selenium using Chromedriver](http://selenium-python.readthedocs.io/installation.html)
2. Install FA-Python from repository
    ```sh
    pip install https://github.com/Rendyindo/yippi/archive/master.zip
    ```
3. Run some examples above to try.

## Examples

```python
>>> import fa
>>> fur = fa.FurAffinity()
>>> result = fur.search("@keywords femboy") // Search for Femboy in FurAffinity
<fa.object.SearchResults object at 0x0000000003B33128>
>>> result.posts // Show posts result
>>> post = result.posts[0] // Open post #1
>>> post
<title> by <artist>
>>> post.imglink // Get image link for the post
>>> result.next // Press the next result button
>>> result.close() // Close Chrome browser
```

More details are going to be added in wiki, soon(tm).