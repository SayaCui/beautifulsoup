# Milestone 2 — BeautifulSoup Extension

## Overview

In this milestone, I explored the BeautifulSoup source code and implemented a new API called `SoupReplacer`.

The milestone contains three parts:

- **Part 1:** Use `SoupStrainer` to complete Milestone 1 Tasks 2, 3, and 4, and test performance on a large HTML file.
- **Part 2:** Locate the original source code definitions of the BeautifulSoup APIs used in Milestone 1 and Milestone 2 Part 1.
- **Part 3:** Implement `SoupReplacer` to replace HTML tags during parsing and test the new API.

## Project Structure

```text
beautifulsoup/
├── apps/
│   └── m2/
│       ├── task2.py
│       ├── task3.py
│       ├── task4.py
│       ├── task6.py
│       ├── generate_large_html.py
│       ├── compare.py
│       ├── test.html
│       ├── large.html
│       ├── task6_output.html
│       └── M2-README.md
├── bs4/
│   ├── __init__.py
│   ├── filter.py
│   └── tests/
│       └── test_soup_replacer.py
└── README.md
```

Only files relevant to this milestone are shown.

---

# Part 1 — SoupStrainer

## 1.1 Implementation

`SoupStrainer` allows BeautifulSoup to parse only selected parts of an HTML document. This can improve performance when the application does not need the entire parse tree.

I created three separate Python applications:

| File | Task | SoupStrainer Usage |
|---|---|---|
| `task2.py` | Find all hyperlinks | `SoupStrainer("a")` |
| `task3.py` | Find all HTML tags | `SoupStrainer(name=True)` |
| `task4.py` | Find tags with an `id` attribute | `SoupStrainer(attrs={"id": True})` |

For example, Task 2 uses:

```python
from bs4 import BeautifulSoup, SoupStrainer

soup = BeautifulSoup(
    html,
    "html.parser",
    parse_only=SoupStrainer("a")
)
```

For Task 3, I experimented with `SoupStrainer(name=True)`. However, because this task requires all HTML tags, there is less opportunity to improve performance through selective parsing.

This helped me understand that SoupStrainer is most useful when only a small portion of the document is needed.

## 1.2 Large File Testing

I created `generate_large_html.py` to generate a large HTML file named `large.html`.

The generated document contains approximately **300,002 HTML tags**, including **100,000 hyperlinks**.

I tested all three applications using this file.

| Application | Execution Time |
|---|---|
| Task 2 | 2.077 seconds |
| Task 3 | 2.648 seconds |
| Task 4 | 3.435 seconds |

I also created `compare.py` to compare normal BeautifulSoup parsing with SoupStrainer when extracting hyperlinks.

| Method | Time | Links Found |
|---|---|---|
| Normal BeautifulSoup | 2.383 seconds | 100,000 |
| SoupStrainer | 1.755 seconds | 100,000 |

Both methods found the same number of hyperlinks.

The speedup was:

`2.383 / 1.755 ≈ 1.36`

The execution time reduction was approximately:

`(2.383 - 1.755) / 2.383 × 100% ≈ 26.4%`

In this experiment, SoupStrainer was approximately **1.36 times faster**, reducing execution time by **26.4%**.

These results suggest that selective parsing can improve performance when only certain elements are needed.

However, the improvement depends on the HTML structure and filtering conditions. These measurements were taken from individual runs, so repeated experiments would provide more reliable results.

## 1.3 How to Run

Run the following commands from the repository root:

```bash
python3 apps/m2/generate_large_html.py

python3 apps/m2/task2.py apps/m2/large.html
python3 apps/m2/task3.py apps/m2/large.html
python3 apps/m2/task4.py apps/m2/large.html

python3 apps/m2/compare.py
```

---

# Part 2 — BeautifulSoup Source Code Analysis

## 2.1 Overview

For Part 2, I examined the original BeautifulSoup source code to locate the definitions of all BeautifulSoup API functions used in my Milestone 1 applications and Milestone 2 Part 1.

The following file names and line numbers refer to the **original source code before my modifications**.

## 2.2 API Definition Locations

| API | Original Source File | Line |
|---|---|---|
| `BeautifulSoup.__init__()` | `bs4/__init__.py` | 209 |
| `Tag.find()` | `bs4/element.py` | 2684 |
| `Tag.find_all()` | `bs4/element.py` | 2715 |
| `PageElement.find_parent()` | `bs4/element.py` | 992 |
| `PageElement.get_text()` | `bs4/element.py` | 524 |
| `Tag.prettify()` | `bs4/element.py` | 2601 |
| `SoupStrainer` class | `bs4/filter.py` | 313 |
| `SoupStrainer.__init__()` | `bs4/filter.py` | 345 |

## 2.3 APIs Used in Milestone 1

I reviewed all eight Milestone 1 application files and identified the following API usage:

| Milestone 1 Task | BeautifulSoup APIs Used |
|---|---|
| Task 1 | `BeautifulSoup()`, `prettify()` |
| Task 2 | `BeautifulSoup()`, `find_all()` |
| Task 3 | `BeautifulSoup()`, `find_all()` |
| Task 4 | `BeautifulSoup()`, `find_all()` |
| Task 5 | `BeautifulSoup()`, `find()`, `find_parent()` |
| Task 6 | `BeautifulSoup()`, `find_all()`, `prettify()` |
| Task 7 | `BeautifulSoup()`, `find_all()`, `prettify()` |
| Task 8 | `BeautifulSoup()`, `get_text()` |

Milestone 2 Part 1 additionally uses `SoupStrainer` through the `parse_only` argument of the BeautifulSoup constructor.

The `parse_only` argument is not a separate API function.

In Milestone 1, I also modified tag names and attributes directly:

```python
tag.name = "blockquote"
paragraph["class"] = "test"
```

These operations modify properties of existing tags rather than calling separate BeautifulSoup API functions.

By examining the source code, I learned more about how BeautifulSoup organizes its parsing, searching, navigation, and modification functionality.

This was useful when implementing the new SoupReplacer API in Part 3.

---

# Part 3 — SoupReplacer

## 3.1 API Design

In this part, I implemented a new API called `SoupReplacer`.

The purpose of SoupReplacer is to replace specified HTML tag names **during parsing**, instead of searching and modifying the completed parse tree afterward.

The constructor is:

```python
SoupReplacer(og_tag, alt_tag)
```

The parameters are:

- `og_tag`: The original tag name.
- `alt_tag`: The replacement tag name.

For example:

```python
from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer

html = "<p>Hello <b>World</b></p>"

soup = BeautifulSoup(
    html,
    "html.parser",
    replacer=SoupReplacer("b", "blockquote")
)

print(soup.prettify())
```

This replaces `<b>` with `<blockquote>` while preserving the text content.

## 3.2 Source Code Modifications

I modified two BeautifulSoup source files:

| File | Modification |
|---|---|
| `bs4/filter.py` | Added the `SoupReplacer` class |
| `bs4/__init__.py` | Added the optional `replacer` argument and integrated replacement into parsing |

The new class is:

```python
class SoupReplacer:
    def __init__(self, og_tag, alt_tag):
        self.og_tag = og_tag
        self.alt_tag = alt_tag
```

I updated the BeautifulSoup constructor to accept an optional `replacer` argument and store the provided object.

I also modified `handle_starttag()` to replace matching tag names during parsing.

Finally, I updated `handle_endtag()` so that closing tags are handled consistently after replacement.

This was important when processing nested elements such as:

```html
<div><b>Outer <b>Inner</b></b></div>
```

The goal was to replace both `<b>` elements while preserving their nested structure.

## 3.3 Comparison with Milestone 1

In Milestone 1 Task 6, I first parsed the complete document and then modified matching tags:

```python
soup = BeautifulSoup(content, "html.parser")

for tag in soup.find_all("b"):
    tag.name = "blockquote"
```

This required searching the parse tree after parsing.

In Milestone 2, the replacement happens during parsing:

```python
soup = BeautifulSoup(
    content,
    "html.parser",
    replacer=SoupReplacer("b", "blockquote")
)
```

The new implementation avoids an additional `find_all()` traversal after parsing.

## 3.4 Application — Task 6

I created `apps/m2/task6.py` to reproduce Milestone 1 Task 6 using the new SoupReplacer API.

The program:

1. Reads an HTML file from the command line.
2. Uses `SoupReplacer("b", "blockquote")` during parsing.
3. Writes the modified HTML document to an output file.

Run:

```bash
python3 apps/m2/task6.py apps/m2/test.html
```

The test input included:

```html
<p>This is <b>bold text</b>.</p>
```

The generated output contained:

```html
<p>
 This is
 <blockquote>
  bold text
 </blockquote>
 .
</p>
```

This confirmed that the application replaced the tag and preserved its text content.

## 3.5 Manual Testing

I manually tested four different cases:

| Test Case | Expected Behavior | Result |
|---|---|---|
| Basic replacement | Replace `<b>` with `<blockquote>` | Passed |
| Nested tags | Replace nested tags and preserve structure | Passed |
| No matching tags | Leave unrelated tags unchanged | Passed |
| Multiple matching tags | Replace all matching tags | Passed |

All four manual tests produced the expected results.

## 3.6 New Automated Tests

I created `bs4/tests/test_soup_replacer.py` with two new automated tests.

**Test 1 — `test_basic_replacement`**

Checks that a `<b>` tag is replaced with `<blockquote>`, the original `<b>` tag no longer exists, and the text content is preserved.

**Test 2 — `test_nested_replacement`**

Checks that two nested `<b>` tags are replaced and that the parent-child relationship is preserved.

Run the new tests:

```bash
python3 -m pytest bs4/tests/test_soup_replacer.py -v
```

Results:

```text
test_basic_replacement PASSED
test_nested_replacement PASSED

2 passed in 0.06s
```

Both new tests passed.

## 3.7 Full Regression Testing

After implementing SoupReplacer, I ran the complete BeautifulSoup test suite to check for compatibility problems.

Command:

```bash
python3 -m pytest bs4/tests -q
```

Results:

| Result | Count |
|---|---|
| Passed | 731 |
| Skipped | 107 |
| Failed | 0 |
| Execution Time | 0.40 seconds |

Before adding the two new tests, the suite reported 729 passed and 107 skipped.

After adding them, the result increased to **731 passed, 107 skipped, and 0 failed**.

All executed tests passed, suggesting that the changes did not introduce failures in the existing tested functionality.

## 3.8 Challenges and Limitations

The main challenge was handling closing tags correctly after replacing opening tags.

Changing only the opening tags could affect the nested structure, so I updated the closing-tag handling logic and tested nested replacements.

Another challenge was adding the optional constructor argument without breaking existing BeautifulSoup functionality.

The current implementation supports one tag replacement rule at a time. Additional testing would be useful for malformed HTML and different parser backends.

---

# Conclusion

In this milestone, I learned how to use SoupStrainer for selective parsing, explore the original BeautifulSoup source code, and implement a new API.

In Part 1, I tested SoupStrainer using a large generated HTML document and observed a performance improvement when extracting hyperlinks.

In Part 2, I located the original source code definitions of the APIs used in my Milestone 1 and Milestone 2 Part 1 applications.

In Part 3, I implemented SoupReplacer to replace HTML tags during parsing and used it to complete Milestone 1 Task 6.

I also added two automated tests and ran the complete BeautifulSoup test suite, obtaining **731 passed, 107 skipped, and 0 failed**.

Overall, this milestone helped me better understand HTML parsing, API design, source code modification, and software testing.