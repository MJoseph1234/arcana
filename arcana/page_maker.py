import markdown
import os
import shutil

import settings

from templater import fill_template

class MarkdownPage():
	def __init__(self, file, directory = settings.MARKDOWN):
		self.file = file
		self.file_name, self.file_ext = os.path.splitext(self.file)
		self.directory = directory
		self.md_file = os.path.join(directory, file)
		self._meta = {}

	@property
	def meta(self):
		"""
		Get the metadata tags from the beginning of the markdown file
		
		Assumes there's a maximum of five lines of metadata at the beginning of
		the file so that we're not parsing the entire thing just for the few
		lines at the beginning
		"""
		if self._meta != {}:
			return(self._meta)

		metadata_lines = 6
		md_converter = markdown.Markdown(extensions=['meta'])

		with open(self.md_file) as input_file:
			head = [next(input_file) for _ in range(metadata_lines)]
		
		html = md_converter.convert(''.join(head))
		self._meta = md_converter.Meta
		return(self._meta)

	@property
	def title(self):
		if self.meta.get('title'):
			return(self.meta['title'][0])
		else:
			return(f'Scroll of {capitalize_words(self.file_name)}')

	@property
	def link_text(self):
		if self.meta.get('link text'):
			return(self.meta['link text'][0])
		else:
			return(f'{capitalize_words(self.file_name)}')

	@property
	def content_as_html(self):
		with open(self.md_file) as input_file:
			text = input_file.read()
		md_converter = markdown.Markdown(extensions=['tables', 'nl2br', 'meta'])
		return(md_converter.convert(text).splitlines(True))

	def __str__(self):
		return(self.md_file)

class Site():
	def __init__(self):
		self.title_suffix = settings.TITLE_SUFFIX
		self.input_directory = settings.MARKDOWN
		self.refresh_page_list()

	def exclude_file(self, file):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			return(True)

		if MarkdownPage(file).meta.get('exclude') == ['true']:
			return(True)

		return(False)

	@property
	def pages(self):
		if self._pages:
			return(self._pages)
		else:
			return(None)

	def refresh_page_list(self):
		self._pages = []
		for file in os.listdir(self.input_directory):
			if self.exclude_file(file):
				continue

			self._pages.append(MarkdownPage(file))

	def build_navbar_for_page(self, page):
		"""
		The navbar is page-specific (so we can add the 'active' class),
		but requires details of the entire site
		"""
		navbar = []
		for pg in self.pages:
			html_class_list = []
			html_class_str = ''

			if pg == page:
				html_class_list.append('active')

			if pg.meta.get('align') == ['Right']:
				html_class_list.append('split')

			if html_class_list:
				x = ', '.join(html_class_list)
				html_class_str = f' class="{x}"'

			html = f'<a href="{pg.file_name}.html"{html_class_str}>{pg.link_text}</a>'
			navbar.append(html)
		return(navbar)

	def build_site(self):
		base = os.path.join(settings.TEMPLATES, 'base.html')
		
		for page in self.pages:
			output_file = os.path.join(settings.OUTPUT, page.file_name + '.html')

			fill_template(output_file, base, 
				page_title = f'{page.title}{self.title_suffix}',
				navbar_links = self.build_navbar_for_page(page),
				content = page.content_as_html)

		for file in os.listdir(settings.STATIC):
			shutil.copy(os.path.join(settings.STATIC, file), settings.OUTPUT)

	def update_single_page(self, page):
		"""updates HTML file for given page

		if file names or metadata on other pages have changed,
		the navbar may be incorrect

		Designed for fixing a typo in the content of one page
		"""
		base = os.path.join(settings.TEMPLATES, 'base.html')
		output_file = os.path.join(settings.OUTPUT, page.file_name + '.html')

		fill_template(output_file, base, 
			page_title = f'{page.title}{self.title_suffix}',
			navbar_links = self.build_navbar_for_page(page),
			content = page.content_as_html)

def capitalize_words(string):
	return(' '.join(s.capitalize() for s in string.split()))