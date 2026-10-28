
import time
from bs4 import BeautifulSoup, SoupStrainer

with open("apps/m2/large.html", "r", encoding="utf-8") as file:
    html = file.read()

# Normal parsing
start = time.perf_counter()

normal_soup = BeautifulSoup(html, "html.parser")
normal_links = normal_soup.find_all("a")

normal_time = time.perf_counter() - start

print("Normal parsing:", normal_time)
print("Normal links:", len(normal_links))


# SoupStrainer parsing
start = time.perf_counter()

only_links = SoupStrainer("a")

filtered_soup = BeautifulSoup(
    html,
    "html.parser",
    parse_only=only_links
)

filtered_links = filtered_soup.find_all("a")

filtered_time = time.perf_counter() - start

print("SoupStrainer parsing:", filtered_time)
print("Filtered links:", len(filtered_links))

print("Speedup:", normal_time / filtered_time)
