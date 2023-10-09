from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
This Python script fetches data from a specified URL, removes script and style elements from the HTML content, and extracts text content from the webpage.

It uses the following libraries:
- urllib.request for making an HTTP request to the URL.
- BeautifulSoup from the bs4 library for parsing HTML content.

The steps in the code are as follows:
1. Import necessary modules: urlopen from urllib.request and BeautifulSoup from bs4.
2. Define the URL to fetch data from.
3. Use urlopen to fetch the HTML content from the URL and read it.
4. Create a BeautifulSoup object to parse the HTML content using the 'html.parser' parser.
5. Remove script and style elements from the HTML content to clean it.
6. Get the text content from the cleaned HTML.
7. Split the text into lines, remove leading and trailing spaces on each line, and split multi-headlines into separate lines.
8. Join the cleaned lines to form the final text content.
9. Print the cleaned text content.

Note: This script assumes that the URL specified is "https://www.myfitnesspal.com/" and is subject to change if the URL is different.

Usage:
- Run the script to fetch and clean the text content from the specified URL.
"""

#TODO - Use STDIN for input


url = "https://www.myfitnesspal.com/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)