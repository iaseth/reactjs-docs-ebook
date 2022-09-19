import json
import shutil

from jinja2 import Environment, FileSystemLoader, Template

from .section import ReactOrgSection
from .utils import Counter, ReactOrgTemplate, setIndex, setNextPrevious



class ReactOrgApp:
	def __init__(self):
		self.name = "React.org"
		self.setup_templates()
		self.preferences = json.load(open('preferences.json'))
		self.jo = json.load(open('pages.json'))
		self.sections = []
		self.pages = []
		for sj in self.jo['sections']:
			section = ReactOrgSection(self, sj)
			self.sections.append(section)
			self.pages += section.pages

		setIndex(self.sections)
		setNextPrevious(self.sections)
		setIndex(self.pages)
		setNextPrevious(self.pages)


	def setup_templates(self):
		self.env = Environment(loader=FileSystemLoader('src/templates'))
		self.content_opf_template = ReactOrgTemplate(self.env, 'content_opf.html')
		self.toc_ncx_template = ReactOrgTemplate(self.env, 'toc_ncx.html')
		self.toc_page_template = ReactOrgTemplate(self.env, 'toc_page.html')

		self.article_page_template = ReactOrgTemplate(self.env, 'article_page.html')
		self.section_page_template = ReactOrgTemplate(self.env, 'section_page.html')


	def get_oebps_filepath(self, filepath):
		return f"data/ebookbase/OEBPS/{filepath}"

	def produce_ebook(self):
		self.produce_meta()
		self.produce_content()
		self.produce_epub()

	def produce_meta(self):
		self.save_toc_ncx()
		self.save_content_opf()
		self.save_css()
		self.save_inline_toc()

	def produce_content(self):
		self.save_sections()
		self.save_pages()

	def produce_epub(self):
		bookname = self.name
		zipname = f"{bookname}.zip"
		epubname = f"{bookname}.epub"
		shutil.make_archive(bookname, 'zip', 'data/ebookbase')
		shutil.move(zipname, epubname)
		print(f"\tsaved: ({epubname})")

	def save_toc_ncx(self):
		ncx_path = self.get_oebps_filepath("toc.ncx")
		with open(ncx_path, "w") as f:
			f.write(Template.render(self.toc_ncx_template.template,
				book=self, counter=Counter(0)))
			print(f"\tsaved: ({ncx_path})")

	def save_content_opf(self):
		opf_path = self.get_oebps_filepath("content.opf")
		with open(opf_path, "w") as f:
			f.write(Template.render(self.content_opf_template.template,
				book=self, counter=Counter(0)))
			print(f"\tsaved: ({opf_path})")

	def save_css(self):
		css_path = self.get_oebps_filepath("styles/main.css")
		print(f"\t kept: ({css_path})")

	def save_inline_toc(self):
		toc_path = self.get_oebps_filepath("text/x_inline_toc.html")
		with open(toc_path, "w") as f:
			f.write(Template.render(self.toc_page_template.template,
				book=self, counter=Counter(0)))
			print(f"\tsaved: ({toc_path})")


	def save_sections(self):
		for section in self.sections:
			section.saveHtml()

	def save_pages(self):
		for page in self.pages:
			page.saveHtml()


	def print(self):
		print(f"ReactOrgApp:")
		print(f"---- {len(self.sections)} sections")
		print(f"---- {len(self.pages)} pages")
