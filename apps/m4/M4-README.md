# Milestone-4
# Milestone 4 — BeautifulSoup Iteration

## 1. Overview

In this milestone, I made the `BeautifulSoup` object iterable so users can traverse all nodes in an HTML document using a simple `for` loop.

## 2. Implementation

I added the `__iter__()` method to the `BeautifulSoup` class in `bs4/__init__.py`.

```python
def __iter__(self):
    return self.descendants
```

The implementation reuses the existing `descendants` generator to traverse the tree one node at a time, including nested tags and text nodes.

It does not collect all nodes into a list before iteration, so it follows the milestone's memory requirement.

## 3. Unit Tests

I created `bs4/tests/test_m4_iteration.py` with five tests:

1. Nested HTML elements
2. Empty HTML documents
3. Sibling tags
4. HTML comments
5. Lazy iteration using `iter()` and `next()`

All five tests passed.

## 4. Compatibility Testing

I also ran the existing Milestone 2 and Milestone 3 tests to check that the new iteration behavior did not break the earlier SoupReplacer functionality.

All eight selected regression tests passed.

## 5. Conclusion

Milestone 4 adds a simple way to iterate through all nodes of a BeautifulSoup document while preserving the existing API and avoiding unnecessary memory usage.