"""
Loads the project settings from a config.toml file in the 
project directory.

Any unspecified project settings are set to an arcana default
here

Load settings from arcana defaults
check for and load settings from site defaults
compile settings (but still allow access to what settings came from where)
"""

import tomllib

from pathlib import Path
from collections import ChainMap

import arcana

# Find the toml file
# read the toml file into a settings global
# add defaults into the settings global

def read_toml(toml_file):
	with open(toml_file, 'rb') as toml:
		data = tomllib.load(toml)

	return(data)

def load_arcana_config(directory = None):
	"""Get the absolute defaults for all arcana
	These can be overridden for a project by that project's
	project.toml file
	"""

	if directory:
		return(read_toml(Path(directory).joinpath('defaults.toml')))
	else:
		try:
			arcana_path = Path(arcana.__path__[0])
		except NameError:
			arcana_path = Path(__file__).parent

		return(read_toml(arcana_path.joinpath('defaults.toml')))

def load_project_config(directory = '.'):
	file = find_project_config_file(directory)
	return(read_toml(file))

def find_project_config_file(directory):
	"""
	directory/*.toml
	directory/*.config
	directory/config/*.toml
	directory/config/*.config
	"""
	p = Path(directory)
	files = [file for file in p.iterdir() if file.is_file()]

	for suffix in ['.toml', '.config']:
		for file in files:
			if file.suffix == suffix:
				return file

def compile_config():
	return(ChainMap(load_project_config(), load_arcana_config(),))


class ProjectSettings():
	def __init__(self, directory = None, toml_file = None, **kwargs):
		if directory and not toml_file:
			toml_file = find_project_config_file(directory)
			self.root = directory

		if toml_file:
			self.from_toml(toml_file)

		self.set_defaults(**kwargs)

	def from_toml(self, toml_file):
		data = read_toml(toml_file)
		for k, v in data.items():
			setattr(self, k, v)

	def set_defaults(self, **kwargs):
		
		if getattr(self, 'root', None) is None:
			if 'cwd' in kwargs:
				self.root = kwargs.get('cwd')
			else:
				self.root = Path.cwd()

		# Set the default directory structure
		dirs = ['content', 'assets', 'layouts', 'public', 
		'templates', 'data', 'static']
		for directory in dirs:
			if getattr(self, directory, None) is None:
				setattr(self, directory, directory)

		if getattr(self, 'site_name', None) is None:
			if 'cwd' in kwargs:
				self.site_name = kwargs.get('cwd').name
			else:
				self.site_name = Path.cwd().name

		# if getattr(self, 'title_suffix', None) is None:
		# 	self.title_suffix = ' - ' + self.site_name.replace('-', ' ').title()

settings = compile_config()