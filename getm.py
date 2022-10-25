from bs4 import BeautifulSoup
import requests
target = input('URL: ')
url_list = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/50.0.2661.102 Safari/537.36'}

web_page = requests.get(target, headers=headers)
soup = BeautifulSoup(web_page.text, 'html.parser')
a_element = soup.find_all('div', class_='thumbnail')
for link in a_element:
    urls = link.a.get('href')
    url_list.append(urls)


for link in url_list:
    web_page = requests.get(link, headers=headers)
    soup = BeautifulSoup(web_page.text, 'html.parser')
    content_divs = soup.find("div", {"class": "entry-content"})
    if content_divs == None:
        continue
    block_quote = content_divs.find("blockquote" , recursive=False)
    if block_quote == None:
        continue
    p_element = block_quote.find('p')
    print (p_element.text)
    with open('monolouges.csv', 'a', encoding='utf-8-sig') as file:
        file.writelines(p_element.text)
        file.write('\n')
        file.close
