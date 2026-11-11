
from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer


def test_name_xformer():
    html = "<div><b>Hello</b><p>World</p></div>"

    replacer = SoupReplacer(
        name_xformer=lambda tag: (
            "blockquote" if tag.name == "b" else tag.name
        )
    )

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    assert soup.find("blockquote") is not None
    assert soup.find("blockquote").get_text() == "Hello"
    assert soup.find("p") is not None
    assert soup.find("p").get_text() == "World"



def test_attrs_xformer():
    html = '<p class="hello" id="test">Hi</p>'

    replacer = SoupReplacer(
        attrs_xformer=lambda tag: {
            k: v for k, v in tag.attrs.items()
            if k != "class"
        }
    )

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    assert soup.p is not None
    assert "class" not in soup.p.attrs
    assert soup.p.get("id") == "test"
    assert soup.p.get_text() == "Hi"



def test_xformer():
    html = "<div><p>Hello</p></div>"

    def add_attribute(tag):
        if tag.name == "p":
            tag.attrs["data-test"] = "yes"

    replacer = SoupReplacer(xformer=add_attribute)

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    assert soup.p is not None
    assert soup.p.get("data-test") == "yes"
    assert soup.p.get_text() == "Hello"
    assert soup.div is not None



def test_old_api_compatibility():
    html = "<div><b>Hello</b><p>World</p></div>"

    replacer = SoupReplacer("b", "blockquote")

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    assert soup.find("blockquote") is not None
    assert soup.find("blockquote").get_text() == "Hello"
    assert soup.find("b") is None
    assert soup.find("p") is not None
    assert soup.find("p").get_text() == "World"


def test_combined_transformers():
    html = '<div><b class="bold" id="title">Hello</b></div>'

    replacer = SoupReplacer(
        name_xformer=lambda tag: (
            "blockquote" if tag.name == "b" else tag.name
        ),
        attrs_xformer=lambda tag: {
            k: v for k, v in tag.attrs.items()
            if k != "class"
        }
    )

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    tag = soup.find("blockquote")

    assert tag is not None
    assert tag.get_text() == "Hello"
    assert "class" not in tag.attrs
    assert tag.get("id") == "title"
    assert soup.find("b") is None


def test_nested_html():
    html = "<div><section><b>Hello</b></section><p>World</p></div>"

    replacer = SoupReplacer(
        name_xformer=lambda tag: (
            "blockquote" if tag.name == "b" else tag.name
        )
    )

    soup = BeautifulSoup(
        html, "html.parser", replacer=replacer
    )

    assert soup.div is not None
    assert soup.section is not None
    assert soup.find("blockquote") is not None
    assert soup.find("blockquote").get_text() == "Hello"
    assert soup.find("b") is None
    assert soup.find("p").get_text() == "World"
    assert soup.div.section.blockquote is not None



