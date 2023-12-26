"""
Basic templating system allows {{ variable }} or {% block %}

{{ variable }} expects a variable to be passed in
{% block %} expects to find a file named 'block' of which to pull in the contents
"""

from pathlib import Path
from io import StringIO

from arcana.settings import settings

class Layout():
	def __init__(self, base, context):
		self.indent = 0
		self.base = base
		self.context = context

	# def get_layout_dir(self):
	# 	return(Path('.').joinpath('layouts'))

	def render(self):
		if isinstance(self.base, Path):
			base = open(self.base, 'r')
		elif isinstance(self.base, str):
			base = StringIO(self.base)

		for line, text in enumerate(base):
			if "{{" in text:
				yield(self.handle_variable(text))
			elif "{%" in text:
				yield(self.handle_block(text))
			else:
				yield(text)

		base.close()

	def handle_variable(self, text):
		pre, temp = text.split("{{")
		variable, post = temp.split("}}")
		variable = variable.strip()

		self.indent += pre.count('\t')

		if self.context.get(variable) is not None:
			if isinstance(self.context[variable], str):
				var = self.context[variable]
			elif isinstance(self.context[variable], list):
				tmp = "\t" * self.indent
				var = tmp.join(self.context[variable])
		else:
			raise KeyError(f'Template variable "{variable}" not found in template context')
		
		self.indent -= pre.count('\t')

		return(pre + var + post)

	def handle_block(self, text):
		pre, temp = text.split("{%")
		variable, post = temp.split("%}")
		variable = variable.strip()

		layout = Path(settings.layouts).joinpath(variable + '.html')

		self.indent += pre.count('\t')

		template = Layout(layout, self.context)
		template.indent += self.indent

		self.indent -= pre.count('\t')
		
		return(pre + ''.join([text for text in template.render()]) + post)
