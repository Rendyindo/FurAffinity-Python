# FurAffinity-Python

An API-like wrapper for FurAffinity, written in Python 3.6.

## Dependencies

- `requests`
- `bs4`

## Getting Started

1. Install FA-Python from repository
    ```sh
    pip install https://github.com/Rendyindo/yippi/archive/master.zip
    ```
2. Run some examples above to try.

## Examples

```python
>>> import fa
>>> fur = fa.FurAffinity()
>>> result = fur.search("@keywords femboy") // Search for Femboy in FurAffinity
<fa.object.SearchResults object at >
>>> result.posts                            // Show posts result
>>> post = result.posts[0]                  // Open post #1
>>> post
<title> by <artist>
>>> post.imglink                            // Get image link for the post
>>> result.next                             // Press the next result button
>>> result.close()                          // Close Chrome browser
```

More details are going to be added in wiki, soon(tm).  
Also take a note to **not** violate any FA's [ToS](http://www.furaffinity.net/tos/) using this module!
