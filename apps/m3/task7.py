
from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer
from bs4.element import Tag

html = """
<html>
    <body>
        <h1>My Web Page</h1>
        <p>This is the original paragraph.</p>
    </body>
</html>
"""


def add_comment(tag):
    if tag.name == "body":
        new_p = Tag(name="p")
        new_p.string = "This paragraph was added by SoupReplacer."
        tag.append(new_p)


replacer = SoupReplacer(xformer=add_comment)

soup = BeautifulSoup(
    html,
    "html.parser",
    replacer=replacer
)

print(soup.prettify())
