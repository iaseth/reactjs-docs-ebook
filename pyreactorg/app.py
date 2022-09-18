import json

from .section import ReactOrgSection



class ReactOrgApp:
	def __init__(self):
		self.jo = json.load(open('pages.json'))
		self.sections = []
		self.pages = []
		for sj in self.jo['sections']:
			section = ReactOrgSection(self, sj)
			self.sections.append(section)
			self.pages += section.pages

	def print(self):
		print(f"ReactOrgApp:")
		print(f"---- {len(self.sections)} sections")
		print(f"---- {len(self.pages)} pages")
