
import sys
from bs4 import BeautifulSoup, SoupStrainer

def main(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    only_links = SoupStrainer("a")

    soup = BeautifulSoup(
        html,
        "html.parser",
        parse_only=only_links
    )

    for link in soup.find_all("a"):
        print(link)

if __name__ == "__main__":
    main(sys.argv[1])
