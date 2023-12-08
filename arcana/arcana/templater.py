"""
Basic templating system allows {{ content }} or {% block %}

{{ content }} expects a variable to be passed in
{% block %} expects to find a file named 'block' of which to pull in the contents
"""

def fill_template(new_page, template_page, **kwargs):
	with open(template_page, 'r') as template, open(new_page, 'w') as new:
		for count, text in enumerate(template):
			if "{{" in text:
				handle_statement(text, new, **kwargs)
				continue
			if "{%" in text:
				handle_block(text, new, **kwargs)
				continue
			new.write(text)

def handle_statement(text, new, **kwargs):
	pre, temp = text.split("{{")
	variable, post = temp.split("}}")
	variable = variable.strip()

	indent = pre.count('\t') * '\t'
	if kwargs.get('indent'):
		indent += kwargs['indent']

	var = None
	if kwargs.get(variable) is not None:
		if isinstance(kwargs[variable], str):
			var = kwargs[variable]
		elif isinstance(kwargs[variable], list):
			var = f'{indent}'.join(kwargs[variable])
	
	if not new:
		if var is not None:
			return(pre + var + post)
		else:
			return(pre + post)
	else:
		if var is not None:
			new.write(pre + var + post)
		else:
			new.write(pre + post)

def handle_block(text, new, **kwargs):
	"""Right now, blocks won't be able to have their own nested block
	"""
	pre, temp = text.split("{%")
	variable, post = temp.split("%}")
	variable = variable.strip()

	indent = pre.count('\t') * '\t'
	if kwargs.get('indent'):
		indent += kwargs['indent']

	with open('layouts/' + variable + '.html', 'r') as block:
		for count, text in enumerate(block):

			if "{{" in text:
				handle_statement(text, new, indent = indent, **kwargs)
				continue
			
			new.write(f'{indent}{text}')
		new.write(post)