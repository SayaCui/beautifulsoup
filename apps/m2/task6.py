import sys
from bs4 import BeautifulSoup
from bs4.filter import SoupReplacer

input_file = sys.argv[1]

with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

soup = BeautifulSoup(
    content,
    "html.parser",
    replacer=SoupReplacer("b", "blockquote")
)

with open("task6_output.html", "w", encoding="utf-8") as output:
    output.write(soup.prettify())