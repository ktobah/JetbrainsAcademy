import argparse
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init
init()


# write your code here
def get_file_name(url):
    dot_count = url.count(".")
    if dot_count == 1:
        return url.split('.')[0].split('//')[-1]
    else:
        return url.split('//')[-1].split('.')[1]


def write_url_file(filename, path, content):
    with open(f'{path}/{filename}', 'w') as f:
        f.write(content)


def check_file_exist(filename, path):
    if os.path.isfile(f'{path}/{filename}'):
        return f'{path}/{filename}'
    else:
        return False


def get_url(url):
    url_content = requests.get(url).text
    soup = BeautifulSoup(url_content, 'html.parser')
    for i in soup.find_all("a"):
        i.insert(0, "Fore.BLUE")
    return soup.get_text()


def print_text(content):
    for i in content.splitlines():
        if i != "":
            if "Fore.BLUE" in i:
                print(Fore.BLUE + i.replace("Fore.BLUE", ""))
            else:
                print(Fore.BLACK + i.replace("Fore.BLUE", ""))


def process_url(url, output_dir):
    print("")
    page_content = get_url(url)
    print_text(page_content)
    page_name = get_file_name(url)
    write_url_file(page_name, output_dir, page_content)
    pages_visited.append(page_name)


parser = argparse.ArgumentParser()
parser.add_argument("output_dir", help='output directory')
args = parser.parse_args()

if args.output_dir:
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

pages_visited = deque()
while True:
    url = input()
    if url == "exit":
        break
    elif url == "back":
        if not pages_visited:
            continue
        else:
            pages_visited.pop()
            with open(f'{args.output_dir}/{pages_visited.pop()}', 'r') as f:
                print_text(f.read())
    elif "." not in url:
        file_exists = check_file_exist(url.split('.')[0], args.output_dir)
        if file_exists:
            with open(file_exists, 'r') as f:
                print_text(f.read())
        else:
            print('Error: Incorrect URL')
        continue
    elif "https://" not in url:
        url = "https://" + url
        process_url(url, args.output_dir)
    else:
        process_url(url, args.output_dir)