from jinja2 import Template



class ReactOrgTemplate:
	def __init__(self, env, path):
		self.env = env
		self.path = path
		self.template = self.env.get_template(self.path)


class HtmlBaseclass:
	def __init__(self):
		pass

	def getHtmlFilename(self):
		return self.getIdref() + ".html"

	def getLocalHtmlFilepath(self):
		return "text/" + self.getHtmlFilename()

	def getHtmlPath(self):
		return self.book.get_oebps_filepath(self.getLocalHtmlFilepath())

	def saveHtml(self):
		html_path = self.getHtmlPath()
		with open(html_path, "w") as f:
			f.write(Template.render(self.template,
				page=self, counter=Counter(0)))
			# print(f"\tsaved: ({html_path})")

	def getPaddedIndex(self):
		return self.index + 1

	def length(self):
		return len(self.pages)

	def getIndex(self):
		return self.index + 1

	def getTitle(self):
		return self.title

	def __lt__(self, other):
		return self.length() < other.length()


class Counter():
	def __init__(self, counter):
		self.counter = counter

	def count(self):
		self.counter += 1
		return self.counter


def sanitizeName(name):
	ln = list(name.lower())
	for i, c in enumerate(ln):
		if not c.isalnum():
			ln[i] = '_'
	return "".join(ln)

def setIndex(arr):
	for index, element in enumerate(arr):
		element.index = index

def setNextPrevious(arr):
	n = len(arr)
	for index, element in enumerate(arr):
		if index is 0:
			element.previous = None
		else:
			element.previous = arr[index - 1]

		if index < n-1:
			element.next = arr[index + 1]
		else:
			element.next = None


