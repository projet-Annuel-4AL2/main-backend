from bs4 import BeautifulSoup
import sys


def clean_html_file(filename):
    with open(filename, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    clean_html = soup.prettify()

    with open(filename, 'w') as file:
        file.write(clean_html)


if __name__ == "__main__":
    html_files = sys.argv[1:]
    for html_file in html_files:
        clean_html_file(html_file)
