from bs4 import BeautifulSoup


def test_nested_html():
    html = "<div><p>Hello</p></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = list(soup)

    assert len(nodes) == 3
    assert nodes[0].name == "div"
    assert nodes[1].name == "p"
    assert str(nodes[2]) == "Hello"


def test_empty_html():
    soup = BeautifulSoup("", "html.parser")

    nodes = list(soup)

    assert len(nodes) == 0

def test_sibling_tags():
    html = "<div><p>Apple</p><span>Banana</span></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = list(soup)

    assert len(nodes) == 5
    assert nodes[0].name == "div"
    assert nodes[1].name == "p"
    assert str(nodes[2]) == "Apple"
    assert nodes[3].name == "span"
    assert str(nodes[4]) == "Banana"

def test_html_comment():
    html = "<div>Hello<!-- This is a comment --></div>"
    soup = BeautifulSoup(html, "html.parser")

    nodes = list(soup)

    assert len(nodes) == 3
    assert nodes[0].name == "div"
    assert str(nodes[1]) == "Hello"
    assert str(nodes[2]) == " This is a comment "

def test_lazy_iteration():
    html = "<div><p>Hello</p><span>World</span></div>"
    soup = BeautifulSoup(html, "html.parser")

    iterator = iter(soup)

    assert iter(iterator) is iterator
    assert next(iterator).name == "div"
    assert next(iterator).name == "p"
    assert str(next(iterator)) == "Hello"
    assert next(iterator).name == "span"
    assert str(next(iterator)) == "World"