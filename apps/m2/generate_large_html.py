
def generate_html(filename, n):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("<html><body>\n")

        for i in range(n):
            file.write(
                f'<div id="item{i}">'
                f'<p>Paragraph {i}</p>'
                f'<a href="https://example.com/{i}">Link {i}</a>'
                f'</div>\n'
            )

        file.write("</body></html>")


if __name__ == "__main__":
    generate_html("apps/m2/large.html", 100000)
