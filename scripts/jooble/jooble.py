#!/usr/bin/env python3

import sys
import json
import argparse
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

WHITESPACE = '\r\t\n '
PROVIDED_BY = 'provided by '
TOR_SOCKS_PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


class JoobleClient():
    def __init__(self):
        self.url = 'https://jooble.org/'
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Brave Brave Chrome/79.0.3945.74 Safari/537.36'
        }
        self.params = {}
        print(requests.get('http://ident.me').text)
        print(requests.get('http://ident.me', proxies=TOR_SOCKS_PROXIES).text)
        response = requests.get(self.url,
                                headers=self.headers,
                                proxies=TOR_SOCKS_PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        self.action = form.get('action')
        self.method = form.get('method')
        for field in form.find_all('input'):
            if field.get('type') not in ['text', 'hidden']:
                continue
            self.params.update({field.get('name'): field.get('value')})

    def search(self, keywords, location):
        if keywords:
            self.params.update({'Position': keywords})
        if location:
            self.params.update({'Region': location})
        response = requests.request(self.method,
                                    urljoin(self.url, self.action),
                                    params=self.params)
        if not response:
            return None
        results = []
        soup = BeautifulSoup(response.text, 'html.parser')
        for div in soup.find_all('div', id='jobs_list__page'):
            for ahref in div.find_all('a', href=True):
                r = self.__parse_job(ahref.get('href'))
                if r:
                    results.append(r)
        return results

    def __parse_job(self, url):
        response = requests.get(url)
        if not response:
            return None
        job_info = {'url': url}
        soup = BeautifulSoup(response.text, 'html.parser')
        desc_info = soup.find('div', 'vacancy-desc_info')
        h1 = desc_info.find('h1', 'desc_info-header')
        job_info.update({'title': h1.text.strip(WHITESPACE)})
        rows = desc_info.find('table', 'jdp_info-table').find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            label = cells[0].text.strip(WHITESPACE)
            value = cells[1].text.strip(WHITESPACE)
            if label == 'Company:':
                job_info.update({'company': value})
            elif label == 'Location:':
                job_info.update({'location': value})
            elif label == 'Job Type:':
                job_info.update({'job_type': value})
            elif label == 'Salary:':
                job_info.update({'salary': value})
            else:
                print('Unhandled label: {}'.format(label))
                sys.exit(1)
        desc_text = soup.find('div', 'vacancy-desc_text_wrapper')
        summary = desc_text.text.strip(WHITESPACE)
        job_info.update({'summary': desc_text.text.strip(WHITESPACE)})
        if PROVIDED_BY in summary:
            offset = summary.index(PROVIDED_BY)
            job_info.update({'provider': summary[offset + len(PROVIDED_BY):]})
        add_date = soup.find('p', 'vacancy-add_date vacancy-add_date__bottom')
        job_info.update({'add_date': add_date.text.strip(WHITESPACE)})
        return json.loads(json.dumps(job_info))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords")
    parser.add_argument("--location")
    args = parser.parse_args()
    jooble = JoobleClient()
    jobs = jooble.search(keywords=args.keywords, location=args.location)
    print(json.dumps(jobs, indent=4))
