import requests
import os
#import BeautifulSoup4


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def getHtml(url):
    try:
        req = requests.get(url)
        return req
    except requests.exceptions.RequestException as e:
        print("error", e.errno)
        return False

srcUrlBase = "https://4chan.org/o/catalog"

if __name__ == '__main__':
    htmlFile = getHtml(srcUrlBase)
    print(htmlFile)
    open("catalog2.html", "wb").write(htmlFile.content)

