import markdown
import os
import shutil

import settings

from templater import fill_template

def navbar_needs_update():
	""" Check if the navbar should be re-built by 
	comparing which files are in the markdown folder
	to the list of files in the generated_html folder

	If the list of md files matches the list of html files, no update needed
	"""
	md_files = set()
	for file in os.listdir(settings.MARKDOWN):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			continue
		md_files.add(file_name)

	html_files = set()
	for file in os.listdir(settings.OUTPUT):
		file_name, ext = os.path.splitext(file)
		if ext != '.html':
			continue
		html_files.add(file_name)

	return(html_files != md_files)

def get_pages_to_update():
	needs_update = []
	for md_file in os.listdir(settings.MARKDOWN):
		file_name, ext = os.path.splitext(md_file)
		if ext not in {'.txt', '.md'}:
			continue

		html_file = os.path.join(settings.OUTPUT, file_name + '.html')
		if not os.path.isfile(html_file):
			needs_update.append(md_file)
			continue

		if os.path.getmtime(os.path.join(settings.MARKDOWN, md_file)) > os.path.getmtime(html_file):
			needs_update.append(md_file)

	print(f'needs update: {needs_update}')
	return(needs_update)

def capitalize_words(string):
	return(' '.join(s.capitalize() for s in string.split()))

def add_static_files_to_output():
	for file in os.listdir(settings.STATIC):
		shutil.copy(os.path.join(settings.STATIC, file), settings.OUTPUT)

def build_website():
	"""Build the entire website from all the files in
	the markdown folder"""

	page_links = {}

	# Build the list of page links for the top navbar
	for file in os.listdir(settings.MARKDOWN):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			continue
		page_links[file_name] = f'<a href="{file_name}.html">{capitalize_words(file_name)}</a>\n'
		if file_name == 'about':
			page_links[file_name] = f'<a class="split" href="{file_name}.html">{capitalize_words(file_name)}</a>\n'

	# Build html pages based on the files in the Markdown folder
	for file in os.listdir(settings.MARKDOWN):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			continue
		if file_name == 'about':
			page_title = 'About'
		elif file_name == 'spells':
			page_title = 'Scroll of All Spells'
		else:
			page_title = f'Scroll of {capitalize_words(file_name)}'

		# Add 'active' class to navbar page links for this page
		p = []
		for line in page_links:
			if line == file_name:
				if line == 'about':
					p.append(f'<a class="active split" href="{file_name}.html">{capitalize_words(file_name)}</a>\n')
				else:
					p.append(f'<a class="active" href="{file_name}.html">{capitalize_words(file_name)}</a>\n')
			else:
				p.append(page_links[line])

		markdown_file = os.path.join(settings.MARKDOWN, file)
		with open(markdown_file) as input_file:
			text = input_file.read()
		content = markdown.markdown(text, extensions=['tables', 'nl2br']).splitlines(True)

		output_file = os.path.join(settings.OUTPUT, file_name + '.html')
		base_template = os.path.join(settings.TEMPLATES, 'base.html')

		fill_template(output_file, base_template, 
					page_title = page_title,
					content = content,
					page_links = p)

	add_static_files_to_output()

if __name__ == '__main__':
	build_website()