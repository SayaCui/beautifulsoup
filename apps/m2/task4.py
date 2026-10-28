
import sys
from bs4 import BeautifulSoup, SoupStrainer


def main(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    only_id_tags = SoupStrainer(attrs={"id": True})

    soup = BeautifulSoup(
        html,
        "html.parser",
        parse_only=only_id_tags
    )

    for tag in soup.find_all(attrs={"id": True}):
        print(tag)


if __name__ == "__main__":
    main(sys.argv[1])
