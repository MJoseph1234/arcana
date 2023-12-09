import markdown
import os
import shutil

from . import settings

from .templater import fill_template

class MarkdownPage():
	def __init__(self, file, directory):
		self.file = file
		self.name, self.ext = os.path.splitext(file)
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
		with open(self.md_file) as input_file:
			head = [next(input_file) for _ in range(metadata_lines)]
		
		md_converter = markdown.Markdown(extensions=['meta'])
		html = md_converter.convert(''.join(head))
		self._meta = md_converter.Meta
		return(self._meta)

	@property
	def title(self):
		if self.meta.get('title'):
			return(self.meta['title'][0])
		else:
			return(f'Scroll of {capitalize_words(self.name)}')

	@property
	def link_text(self):
		if self.meta.get('linktext'):
			return(self.meta['linktext'][0])
		else:
			return(f'{capitalize_words(self.name)}')

	@property
	def content_as_html(self):
		with open(self.md_file) as input_file:
			text = input_file.read()
		md_converter = markdown.Markdown(extensions=['tables', 'nl2br', 'meta'])
		return(md_converter.convert(text).splitlines(True))

	@property
	def is_draft(self):
		draft = self.meta.get('draft', 'false')[0]
		return(draft.lower() in {'true', 'yes', 't'})
	

	def __str__(self):
		return(self.md_file)

class Site():
	def __init__(self, settings):
		self.settings = settings
		self.refresh_page_list()

	def exclude_file(self, file):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			return(True)

		if MarkdownPage(file, self.settings.content).meta.get('exclude') == ['true']:
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
		for file in os.listdir(self.settings.content):
			if self.exclude_file(file):
				continue

			self._pages.append(MarkdownPage(file, self.settings.content))

	def build_navbar_for_page(self, page):
		"""
		The navbar is page-specific (so we can add the 'active' class),
		but requires details of the entire site
		"""
		navbar = []
		for pg in self.pages:
			if pg.is_draft:
				continue
			html_class_list = []
			html_class_str = ''

			if pg == page:
				html_class_list.append('active')

			if pg.meta.get('align') == ['Right']:
				html_class_list.append('split')

			if html_class_list:
				x = ' '.join(html_class_list)
				html_class_str = f' class="{x}"'

			html = f'<a href="{pg.name}.html"{html_class_str}>{pg.link_text}</a>'
			navbar.append(html)
		return(navbar)

	def build_site(self, include_drafts = False):
		base = os.path.join(self.settings.layouts, 'base.html')
		
		for page in self.pages:
			if page.is_draft and not include_drafts:
				continue
			output_file = os.path.join(self.settings.public, page.name + '.html')

			fill_template(output_file, base, 
				page_title = f'{page.title}{self.settings.title_suffix}',
				navbar_links = self.build_navbar_for_page(page),
				content = page.content_as_html)

		self.add_static_files()

	def add_static_files(self):
		for file in os.listdir(self.settings.static):
			shutil.copy(os.path.join(self.settings.static, file), self.settings.public)

	def update_single_page(self, page):
		"""updates HTML file for given page

		if file names or metadata on other pages have changed,
		the navbar may be incorrect

		Designed for fixing a typo in the content of one page
		"""
		base = os.path.join(self.settings.layouts, 'base.html')
		output_file = os.path.join(self.settings.public, page.name + '.html')

		fill_template(output_file, base, 
			page_title = f'{page.title}{self.settings.title_suffix}',
			navbar_links = self.build_navbar_for_page(page),
			content = page.content_as_html)

def capitalize_words(string):
	return(' '.join(s.capitalize() for s in string.split()))