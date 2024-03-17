import markdown
import os
import shutil

from pathlib import Path
from string import Template, capwords

from arcana.settings import settings
from arcana.templater import Layout

class Page():
	def __init__(self, file, directory = ''):
		self.file = file
		self.name, self.ext = os.path.splitext(file)
		self.directory = directory
		self.md_file = Path(settings['dirs']['content']).joinpath(directory, file)
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
			title_str = Template(settings['page_title_template'])
			return(title_str.substitute(
				title = self.name))

	@property
	def link_text(self):
		if self.meta.get('linktext'):
			return(self.meta['linktext'][0])
		else:
			return(f'{capwords(self.name)}')

	@property
	def content_as_html(self):
		with open(self.md_file, 'r') as input_file:
			text = input_file.read()
		md_converter = markdown.Markdown(extensions=['tables', 'nl2br', 'meta'])
		return(md_converter.convert(text).splitlines(True))

	@property
	def is_draft(self):
		draft = self.meta.get('draft', 'false')[0]
		return(draft.lower() in {'true', 'yes', 't'})

	@property
	def layout(self):
		if self.meta.get('layout'):
			return(self.meta['layout'][0])
		else:
			return(None)

	@property
	def slug(self):
		return(self.name.replace(' ', '-').replace('_', '-'))

	def __str__(self):
		return(self.md_file)

class Site():
	def __init__(self, include_drafts = False):
		#self.refresh_page_list()
		self.include_drafts = include_drafts

	def exclude_file(self, file, subdir = ''):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			return(True)

		if Page(file, subdir).meta.get('exclude') == ['true']:
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
		for file in os.listdir(settings['dirs']['content']):
			if self.exclude_file(file):
				continue

			self._pages.append(Page(file))

	def build_site(self):
		# Clobber the public path

		with os.scandir(settings['dirs']['content']) as content:
			for entry in content:
				if entry.is_dir():
					self.build_site_subdir(entry)
				elif entry.is_file() and not self.exclude_file(entry.name):
					page = Page(entry.name)
					if page.is_draft and not self.include_drafts:
						continue
					output_file = self.get_public_filename_for_page(page)
					self.build_page(page, output_file)

		self.add_static_files()

	def build_site_subdir(self, sub_dir):
		# in the public folder, make a subdirectory with name from path
		
		os.mkdir(Path(settings['dirs']['public']).joinpath(sub_dir.name))

		with os.scandir(sub_dir) as subcontent:
			for entry in subcontent:
				if entry.is_dir():
					pass
					#Only allowing one level of directory depth at the moment
				elif entry.is_file() and not self.exclude_file(entry.name, sub_dir.name):
					page = Page(entry.name, sub_dir.name)
					if page.is_draft and not self.include_drafts:
						continue
					output_file = self.get_public_filename_for_page(page)
					self.build_page(page, output_file)

	def build_navbar_for_page(self, page):
		navbar = []
		path = Path(settings['dirs']['content']).joinpath(page.directory)
		
		for file in os.listdir(path):
			if self.exclude_file(file, page.directory):
				continue
			if Page(file, page.directory).is_draft and not self.include_drafts:
				continue

			html_class_list = []
			html_class_str = ''

			pg = Page(file, page.directory)

			if pg == page:
				html_class_list.append('active')

			if pg.meta.get('align') == ['Right']:
				html_class_list.append('split')

			if html_class_list:
				x = ' '.join(html_class_list)
				html_class_str = f' class="{x}"'

			Path(pg.directory).joinpath(pg.slug)
			html = f'<a href="/{Path(pg.directory).joinpath(pg.slug)}.html"{html_class_str}>{pg.link_text}</a>\n'
			navbar.append(html)
		return(navbar)

	def old_build_navbar_for_page(self, page):
		"""
		The navbar is page-specific (so we can add the 'active' class),
		but requires details of the entire site
		"""
		navbar = []
		for pg in self.pages:
			if pg.is_draft and not self.include_drafts:
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

			html = f'<a href="{pg.slug}.html"{html_class_str}>{pg.link_text}</a>\n'
			navbar.append(html)
		return(navbar)

	def build_site_old(self):
		# base = os.path.join(settings.layouts, 'base.html')
		
		for page in self.pages:
			if page.is_draft and not self.include_drafts:
				continue

			output_file = self.get_public_filename_for_page(page)
			self.build_page(page, output_file)
			# base = self.get_layout_for_page(page)
			# output_file = Path(settings.public).joinpath(page.name + '.html')

			# context = {
			# 	'page_title': f'{page.title}{settings.title_suffix}',
			# 	'navbar_links': self.build_navbar_for_page(page, include_drafts),
			# 	'content': page.content_as_html
			# }

			# with open(output_file, 'w') as out:
			# 	for text in Layout(base, context).fill():
			# 		out.write(text)

		self.add_static_files()

	def add_static_files(self):
		for file in os.listdir(settings['dirs']['static']):
			shutil.copy(os.path.join(settings['dirs']['static'], file), settings['dirs']['public'])

	def get_layout_for_page(self, page):
		layouts = Path(settings['dirs']['layouts'])

		if page.layout is not None:
			return(layouts.joinpath(page.layout))
		elif layouts.joinpath(settings['default_layout']).exists():
			return(layouts.joinpath(settings['default_layout']))
		else:
			return("{{content}}")

	def get_public_filename_for_page(self, page):
		return(Path(settings['dirs']['public']).joinpath(page.directory, page.slug + '.html'))

	def build_page(self, page, target = None):
		"""Generate the HTML for a given page

		If iarget is a file descriptor, write the html to target. 
		Otherwise, return the html to the caller
		"""
		base = self.get_layout_for_page(page)

		context = {
			'page_title': f'{page.title}{settings["title_suffix"]}',
			'navbar_links': self.build_navbar_for_page(page),
			'content': page.content_as_html
		}

		if target is None:
			return(Layout(base, context).render())

		with open(target, 'w') as out:
			for text in Layout(base, context).render():
				out.write(text)