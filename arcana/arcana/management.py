# Main CLI controls for arcana site management

import pkgutil
import sys

from importlib import import_module
from argparse import ArgumentParser
from pathlib import Path

def main():
	parser = build_parser()

	args = parser.parse_args()

	args.command.run(args)

def get_arcana_path():
	"""
	if __path__ is not set, this is likely being used
	as the source code instead of as a pip module, so use
	the file path of this management script as the directory
	for finding the core management commands
	"""
	try:
		arcana_path = Path(__path__[0])
	except NameError:
		arcana_path = Path(__file__).parent
	return(arcana_path)

def get_project_path():
	"""
	projects can have their own commands. This gets the project's
	root directory and then searches for a 'commands' folder
	
	for now we'll assume Arcana is being run from the project 
	directory. in the future we may want to allow arcana to be 
	run with a specific directory given as an argument
	"""
	sys.path.append('.')
	# sys.path.append(Path.cwd().joinpath('commands'))
	# for x in sys.path:
	# 	print(x)
	
	return(Path.cwd())


def build_parser():
	# Load the core arcana subcommands
	subcommands = {name: load_command(name) for name in find_commands(get_arcana_path())}

	# Load any project-specific subcommands
	for name in find_commands(get_project_path()):
		subcommands.update({name: load_project_command(name)})

	parser = ArgumentParser(
		prog = 'arcana',
		description = 'Arcana static site generator')

	subparsers = parser.add_subparsers(title = 'commands',
		description = 'Arcana commands',
		required = True,
		dest = 'command')

	for name, subcommand in subcommands.items():
		subcommand.add_parser(subparsers)

	return(parser)


def find_commands(base_dir):
	command_dir = Path(base_dir).joinpath('commands')
	return([
		name 
		for _, name, is_pkg in pkgutil.iter_modules([command_dir])
		if not is_pkg and not name.startswith("_")
	])

def load_command(name):
	module = import_module(f'arcana.commands.{name}')
	return(module.Command())

def load_project_command(name):
	module = import_module(f'commands.{name}')
	return(module.Command())

class BaseCommand():
	def __init__(self):
		if getattr(self, 'command_name') is None:
			self.command_name = self.__name__
		if getattr(self, 'command_help') is None:
			self.command_help = 'an Arcana subcommand'

	def add_parser(self, subparsers):
		subparser = subparsers.add_parser(
			name = self.command_name,
			help = self.command_help)

		self.add_arguments(subparser)

		subparser.set_defaults(command = self)
	
	def add_arguments(self, parser):
		pass

	def run(self, *args):
		pass

if __name__ == "__main__":
	main()