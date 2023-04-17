import re  
import requests  
from bs4 import BeautifulSoup  
  
url = input("give a url to test")
  
# Fetch the content of the URL  
response = requests.get(url)  
content = response.text  
  
# Parse the HTML  
soup = BeautifulSoup(content, 'html.parser')  
  
# Find all the hrefs  
hrefs = [a['href'] for a in soup.find_all('a', href=True)]  
  
# Define a regex pattern to identify possible version numbers  
version_pattern = re.compile(r'\b\d+\.\d+(\.\d+)?\b')  
  
# Find all the lines containing version numbers  
lines_with_versions = set()  
for href in hrefs:  
    for line_number, line in enumerate(content.split('\n')):  
        if href in line and version_pattern.search(line):  
            lines_with_versions.add((line_number, line))  
  
# Find all HTML and script comments  
comment_pattern = re.compile(r'<!--(.*?)-->|/\*(.*?)\*/', re.DOTALL)  
comments = comment_pattern.findall(content)  
  
# Check for possible version regex matches in comments  
comments_with_versions = set()  
for comment in comments:  
    comment_text = comment[0].strip() if comment[0] else comment[1].strip()  
    if version_pattern.search(comment_text):  
        comments_with_versions.add(comment_text)  
  
# Print the lines containing version numbers  
print("Lines with version numbers:")  
for line_number, line in lines_with_versions:  
    match = version_pattern.search(line)  
    start = max(0, match.start() - 55)  
    end = min(len(line), match.end() + 25)  
    print(f"Line {line_number}: ...{line[start:end]}...")  
  
# Print all HTML and script comments with version regex matches  
print("\nHTML and script comments with version regex matches:")  
for comment in comments_with_versions:  
    print(comment)  
  
# Find lines containing the word 'version'  
lines_with_version_word = set()  
for line_number, line in enumerate(content.split('\n')):  
    if 'vers' in line.lower():  
        lines_with_version_word.add((line_number, line))  
  
# Print the lines containing the word 'version'  
print("\nLines containing the word 'version':")  
for line_number, line in lines_with_version_word:  
    index = line.lower().index('vers')  
    start = max(0, index - 35)  
    end = min(len(line), index + len('version') + 35)  
    print(f"Line {line_number}: ...{line[start:end]}...")  
