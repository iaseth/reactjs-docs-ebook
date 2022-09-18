import json

import requests
import bs4


def main():
	getting_started_url = "https://reactjs.org/docs/getting-started.html"
	response = requests.get(getting_started_url)
	soup = bs4.BeautifulSoup(response.text, 'lxml')

	nav = soup.find('nav', class_='css-7stz2q')
	divs = nav.find_all('div', recursive=False)
	jo = {}; jo['sections'] = []
	for idx, div in enumerate(divs):
		section = {}
		section['title'] = div.find('button').find('div').text.strip()
		print(f"[{idx+1}/{len(divs)}] Found section: {section['title']}")

		pages = []
		for li in div.find_all('li'):
			a = li.find('a')
			page = {}
			page['title'] = a.text.strip()
			page['url'] = a['href'].strip()
			pages.append(page)

		print(f"\t-- added {len(pages)} pages.")
		section['pages'] = pages
		jo['sections'].append(section)

	output_json_name = 'pages.json'
	with open(output_json_name, 'w') as f:
		json.dump(jo, f, indent='\t')
		print(f"saved: ({output_json_name})")


if __name__ == '__main__':
	main()
