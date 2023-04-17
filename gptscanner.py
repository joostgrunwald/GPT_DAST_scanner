import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urljoin
import os  
import openai  
  
openai.api_type = "azure"  
openai.api_base = "replaceme"  
openai.api_version = "2023-03-15-preview"  
openai.api_key = "replaceme"

  
def get_source_code(url):  
    response = requests.get(url)  
    if response.status_code == 200:  
        return response.text  
    else:  
        return None  
  
def get_js_files(url, source_code):  
    js_files = []  
    soup = BeautifulSoup(source_code, 'html.parser')  
    script_tags = soup.find_all('script', src=True)  
    for tag in script_tags:  
        js_url = urljoin(url, tag['src'])  
        js_files.append(js_url)  
    return js_files  
  
def get_file_content(url):  
    response = requests.get(url)  
    if response.status_code == 200:  
        return response.text  
    else:  
        return None  
  
def divide_content(content, token_limit=5500):  
    tokens = content.split()  
    parts = []  
    current_part = []  
    current_count = 0  
    for token in tokens:  
        current_count += len(token)  
        if current_count > token_limit:  
            parts.append(" ".join(current_part))  
            current_part = [token]  
            current_count = len(token)  
        else:  
            current_part.append(token)  
    if current_part:  
        parts.append(" ".join(current_part))  
    return parts

def analyze_code_with_openai(part):  
    response = openai.ChatCompletion.create(  
        engine="fourtopai4",  
        messages=[{  
            "role": "system",  
            "content": "You are a web vulnerability scanning Artificial Intelligence. You get source code from a website as input and you then identify weaknesses in the code, you identify possible secrets, you identify all possible version numbers and you identify vulnerabilities related to these version numbers. You also look for other kind of vulnerabilities that are present in this specific code. Note that you focus only on cybersecurity related issues."  
        }, {  
            "role": "user",  
            "content": part  
        }],  
        temperature=0.7,  
        max_tokens=1200,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None  
    )  

    #print(response)
    # Extract the useful part of the response  
    useful_response = response.choices[0].message.content.strip()  
    return useful_response  
  
def main():  
    url = input("enter a url to audit please: ")  
    source_code = get_source_code(url)  
    if source_code:  
        js_files = get_js_files(url, source_code)  
        print(f"Found {len(js_files)} JS files:")  
        for js_file in js_files:  
            print(js_file)  
  
        source_parts = divide_content(source_code)  
        print(f"\nSource code divided into {len(source_parts)} parts:")  
        for i, part in enumerate(source_parts):  
            print(f"Part {i+1}: {part[:100]}...")  
            useful_response = analyze_code_with_openai(part)  
            print(f"Analysis result for part {i+1}: {useful_response}")  
  
        for js_file in js_files:  
            js_content = get_file_content(js_file)  
            if js_content:  
                js_parts = divide_content(js_content)  
                print(f"\nJS file '{js_file}' divided into {len(js_parts)} parts:")  
                for i, part in enumerate(js_parts):  
                    print(f"Part {i+1}: {part[:100]}...")  
                    useful_response = analyze_code_with_openai(part)  
                    print(f"Analysis result for part {i+1}: {useful_response}")  
            else:  
                print(f"Could not fetch content from {js_file}")  
  
    else:  
        print("Could not fetch source code from the URL")  
  
if __name__ == '__main__':  
    main()  

  
if __name__ == '__main__':  
    main()  
