import markdown
import os

from . import settings

from templater import fill_template

# def fill_template(new_page, template_page, **kwargs):
# 	with open(template_page, 'r') as template, open(new_page, 'w') as new:
# 		for count, text in enumerate(template):
# 			if "{{" in text:
# 				handle_statement(text, new, **kwargs)
# 				continue
# 			if "{%" in text:
# 				handle_block(text, new, **kwargs)
# 				continue
# 			new.write(text)

# def handle_statement(text, new, **kwargs):
# 	pre, temp = text.split("{{")
# 	variable, post = temp.split("}}")
# 	variable = variable.strip()

# 	indent = pre.count('\t') * '\t'
# 	if kwargs.get('indent'):
# 		indent += kwargs['indent']

# 	var = None
# 	if kwargs.get(variable) is not None:
# 		if isinstance(kwargs[variable], str):
# 			var = kwargs[variable]
# 		elif isinstance(kwargs[variable], list):
# 			var = f'{indent}'.join(kwargs[variable])
	
# 	if not new:
# 		if var is not None:
# 			return(pre + var + post)
# 		else:
# 			return(pre + post)
# 	else:
# 		if var is not None:
# 			new.write(pre + var + post)
# 		else:
# 			new.write(pre + post)

# def handle_block(text, new, **kwargs):
# 	"""Right now, blocks won't be able to have their own nested block
# 	"""
# 	pre, temp = text.split("{%")
# 	variable, post = temp.split("%}")
# 	variable = variable.strip()

# 	indent = pre.count('\t') * '\t'
# 	if kwargs.get('indent'):
# 		indent += kwargs['indent']

# 	with open('templates/' + variable + '.html', 'r') as block:
# 		for count, text in enumerate(block):

# 			if "{{" in text:
# 				handle_statement(text, new, indent = indent, **kwargs)
# 				continue
			
# 			new.write(f'{indent}{text}')
# 		new.write(post)

def navbar_needs_update():
	""" Check if the navbar should be re-built by 
	comparing which files are in the markdown folder
	to the list of files in the generated_html folder

	If the list of md files matches the list of html files, no update needed
	"""
	markdown_folder = 'markdown/'
	generated_html_folder = 'generated_html/'

	md_files = set()
	for file in os.listdir(markdown_folder):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			continue
		md_files.add(file_name)

	html_files = set()
	for file in os.listdir(generated_html_folder):
		file_name, ext = os.path.splitext(file)
		if ext != '.html':
			continue
		html_files.add(file_name)

	return(html_files != md_files)

def get_pages_to_update():
	markdown_folder = 'markdown/'
	generated_html_folder = 'generated_html/'
	
	needs_update = []
	for md_file in os.listdir(markdown_folder):
		file_name, ext = os.path.splitext(md_file)
		if ext not in {'.txt', '.md'}:
			continue

		html_file = os.path.join(generated_html_folder, file_name + '.html')
		if not os.path.isfile(html_file):
			needs_update.append(md_file)
			continue

		if os.path.getmtime(os.path.join(markdown_folder, md_file)) > os.path.getmtime(html_file):
			needs_update.append(md_file)

	print(f'needs update: {needs_update}')
	return(needs_update)

def capitalize_words(string):
	return(' '.join(s.capitalize() for s in string.split()))

def build_website():
	"""Build the entire website from all the files in
	the markdown folder"""
	markdown_folder = 'markdown/'
	generated_html_folder = 'generated_html/'
	templates = 'templates/'

	page_links = {}

	# Build the list of page links for the top navbar
	for file in os.listdir(markdown_folder):
		file_name, ext = os.path.splitext(file)
		if ext not in {'.txt', '.md'}:
			continue
		page_links[file_name] = f'<a href="{file_name}.html">{capitalize_words(file_name)}</a>\n'
		if file_name == 'about':
			page_links[file_name] = f'<a class="split" href="{file_name}.html">{capitalize_words(file_name)}</a>\n'

	# Build html pages based on the files in the Markdown folder
	for file in os.listdir(markdown_folder):
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


		with open(f'markdown/{file}') as input_file:
			text = input_file.read()
		content = markdown.markdown(text, extensions=['tables', 'nl2br']).splitlines(True)

		fill_template(f'generated_html/{file_name}.html', 'templates/base.html', 
					page_title = page_title,
					content = content,
					page_links = p)

if __name__ == '__main__':
	build_website()