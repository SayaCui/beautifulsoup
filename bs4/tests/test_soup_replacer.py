from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer


def test_basic_replacement():
    html = "<p>Hello <b>World</b></p>"

    soup = BeautifulSoup(
        html, "html.parser",
        replacer=SoupReplacer("b", "blockquote")
    )

    assert soup.find("b") is None
    assert soup.blockquote.get_text() == "World"


def test_nested_replacement():
    html = "<div><b>Outer <b>Inner</b></b></div>"

    soup = BeautifulSoup(
        html, "html.parser",
        replacer=SoupReplacer("b", "blockquote")
    )

    tags = soup.find_all("blockquote")

    assert len(tags) == 2
    assert tags[0].find("blockquote") is tags[1]