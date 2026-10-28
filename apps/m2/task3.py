
import sys
from bs4 import BeautifulSoup, SoupStrainer


def main(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    all_tags = SoupStrainer(name=True)

    soup = BeautifulSoup(
        html,
        "html.parser",
        parse_only=all_tags
    )

    for tag in soup.find_all(True):
        print(tag.name)


if __name__ == "__main__":
    main(sys.argv[1])
