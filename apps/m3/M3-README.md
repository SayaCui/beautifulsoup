# Milestone-3
# Milestone 3 — SoupReplacer Technical Brief

## 1. Overview

In Milestone 2, we implemented a basic SoupReplacer API that allows users to replace one HTML tag name with another.

In Milestone 3, we extended SoupReplacer to support more flexible transformations using callback functions.

The goal is to make SoupReplacer more powerful while keeping the API simple and maintaining backward compatibility.

## 2. Milestone 2 API

The Milestone 2 API uses two parameters:

```python
SoupReplacer(og_tag="b", alt_tag="blockquote")
```

This API replaces a specified HTML tag with another tag during parsing.

**Advantages:**
- Simple and easy to understand.
- Requires very little code.
- Suitable for straightforward tag replacements.

**Limitations:**
- Only supports predefined tag replacements.
- Cannot easily modify attributes.
- Does not support more complex transformations.

## 3. Milestone 3 API

Milestone 3 introduces three optional callback parameters:

```python
SoupReplacer(
    name_xformer=None,
    attrs_xformer=None,
    xformer=None
)
```

Each callback has a different responsibility.

**name_xformer**

Takes a tag as input and returns a new tag name.

```python
SoupReplacer(
    name_xformer=lambda tag: "blockquote"
    if tag.name == "b" else tag.name
)
```

**attrs_xformer**

Takes a tag as input and returns replacement attributes.

**xformer**

Takes a tag as input and can modify the tag directly without returning a value.

For example:

```python
def remove_class_attr(tag):
    if "class" in tag.attrs:
        del tag.attrs["class"]

replacer = SoupReplacer(xformer=remove_class_attr)
```

This API supports more complex transformations without requiring users to modify BeautifulSoup's internal source code.

## 4. Comparison

| Feature | Milestone 2 | Milestone 3 |
|---|---|---|
| Simple tag replacement | Yes | Yes |
| Conditional tag replacement | Limited | Yes |
| Attribute transformation | No | Yes |
| Custom node modification | No | Yes |
| Ease of use | Very simple | More flexible |
| Complexity | Low | Higher |

Milestone 2 is easier for simple operations, while Milestone 3 is more useful for applications that need customized HTML transformations.

## 5. Performance and Maintainability

Both APIs perform transformations during parsing rather than requiring a separate traversal of the completed document.

This approach can avoid an additional pass through the document, although callback execution introduces some overhead.

Milestone 2 has a simpler interface and is suitable for basic replacements.

Milestone 3 offers greater flexibility, but users must write their own transformation functions.

Separating name, attribute, and general tag transformations also makes the API easier to understand and maintain.

## 6. Recommendation

I recommend keeping both APIs in BeautifulSoup.

The Milestone 2 API should remain available for simple tag replacements because it is easy to use.

The Milestone 3 API should be provided as an extension for users who need more advanced transformations.

Maintaining backward compatibility is important because existing applications should continue working after the API is extended.

I would also recommend documenting when callbacks are executed during parsing. Since the complete document may not be available yet, users should understand that callbacks can modify partially constructed tags.

Overall, supporting both interfaces provides a good balance between simplicity, flexibility, and maintainability.

## 7. Implementation and Testing

The implementation includes:

- `bs4/filter.py`: SoupReplacer implementation.
- `bs4/__init__.py`: Integration with the parsing process.
- `bs4/tests/test_soup_replacer_m3.py`: Six new test cases.
- `apps/m3/task7.py`: Application demonstrating the new API.

### Run Task 7

```bash
python3 -m apps.m3.task7
```

The application adds a new paragraph using the `xformer` callback.

### Run Existing Tests

```bash
python3 -m pytest bs4/tests/ -q
```

Result:

```text
737 passed, 107 skipped
```

### Run Milestone 3 Tests

```bash
python3 -m pytest bs4/tests/test_soup_replacer_m3.py -v
```

Result:

```text
6 passed
```

## 8. Conclusion

Milestone 3 extends SoupReplacer from a simple tag replacement API into a more flexible transformation API.

I recommend preserving the original interface while supporting the new callback-based interface. This gives developers more options without breaking existing applications.