from .utils import HtmlBaseclass



class ReactOrgPage(HtmlBaseclass):
	def __init__(self, section, jo):
		self.section = section
		self.app = section.app
		self.jo = jo
		self.title = jo['title']
		self.filepath = f"data/html/{jo['filename']}.html"
		self.template = self.app.article_page_template.template
		self.pages = []

	def getIdref(self):
		return f"x_section_{self.section.index}_page_{self.index}"

	def get_content_html(self):
		return open(self.filepath).read()

	def __str__(self):
		return f"ReactOrgPage '{self.title}'"
