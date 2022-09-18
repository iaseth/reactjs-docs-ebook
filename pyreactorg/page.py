from .utils import HtmlBaseclass



class ReactOrgPage(HtmlBaseclass):
	def __init__(self, section, jo):
		self.section = section
		self.jo = jo
		self.jo = jo['title']
		# self.template = self.book.topic_page_template.template

	def getIdref(self):
		return f"x_page_{self.name}"

	def __str__(self):
		return f"ReactOrgPage '{self.title}'"
