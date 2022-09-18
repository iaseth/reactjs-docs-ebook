import json
import os

import bs4
import requests


BAD_TAGS = ['img', 'svg', 'script', 'iframe', 'audio', 'meta', 'figure']


def get_file_size_string(path):
	if os.path.isfile(path):
		s = os.stat(path).st_size
		return f"{round(s/1000, 1)}kB"
	return "0kB"

def clean_soup(soup):
	soup.attrs = {}
	comments = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
	[comment.extract() for comment in comments]

	appendix = soup.find('div', class_='jPSzpJ')
	if appendix: appendix.decompose()

	styled_container = soup.find('div', class_='eFRJQn')
	if styled_container: styled_container.decompose()

	for tag in soup.find_all():
		if tag.name in BAD_TAGS:
			tag.decompose()
			continue
		elif tag.name in ['a', 'div']:
			tag.attrs = {}
		elif tag.name is None:
			continue

def get_html_from_url(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text, 'lxml')
	content = soup.find('div', class_='css-6nf64v')
	clean_soup(content)
	return str(content)

def main():
	json_filename = 'pages.json'
	if not os.path.isfile(json_filename):
		print(f"File NOT found: ({json_filename})")
		return

	jo = json.load(open(json_filename))
	sections = jo['sections']
	for sidx, section in enumerate(sections):
		print(f"---- [{sidx+1}/{len(sections)}] New section: '{section['title']}':")
		pages = section['pages']
		for pidx, page in enumerate(pages):
			page_url = "https://reactjs.org" + page['url']
			html_path = f"data/html/{page['filename']}.html"
			print(f"\t---- [{pidx+1}/{len(pages)}] New page: '{page['title']}':")

			if os.path.isfile(html_path):
				print(f"\t\t---- already downloaded ({html_path})")
				continue

			print(f"\t\t---- downloading ({page_url}) ...")
			html_text = get_html_from_url(page_url)
			with open(html_path, 'w') as f:
				f.write(html_text)
			print(f"\t\t---- saved to ({html_path}) [{get_file_size_string(html_path)}]")
			# break
		# break

if __name__ == '__main__':
	main()
