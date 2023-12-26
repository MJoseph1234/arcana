from pathlib import Path

from arcana.management import BaseCommand

class Command(BaseCommand):

	command_name = 'new'
	command_help = 'Start a new Arcana project'

	def add_arguments(self, parser):

		subparser = parser.add_subparsers(title = 'entity',
			description = 'New thing to create',
			required = True,
			dest = 'entity')

		# New Project command for starting a brand new arcana project
		new_project = subparser.add_parser(
			name = 'project',
			help = 'start a new Arcana project')

		new_project.add_argument('path',
			help = 'relative path to new directory')

		# New Post command for creating a new file for the current
		# arcana project
		new_post = subparser.add_parser(
			name = 'post',
			help = 'create a new post or document in the project content directory')
		new_post.add_argument('name',
			help = 'Name or page title for the new post')

		new_command = subparser.add_parser(
			name = 'command',
			help = 'create a new arcana CLI command for your project')

		# parser.add_argument('path',
		# 	help = 'relative path to new directory')

	def run(self, args):
		raise NotImplementedError

	def new_project(self, args):
		path = Path(args.path)
		if path.is_dir():
			print('that path already exists, exiting and doing nothing')
			return

		path.mkdir()
		path.joinpath('content').mkdir()
		path.joinpath('layouts').mkdir()
		path.joinpath('public').mkdir()
		path.joinpath('static').mkdir()

		config = path.joinpath(f'{path.name}.toml')

		with config.open(mode = 'w') as f:
			f.write('# site details\n')
			f.write(f'site_name = \"{path.name}\"\n')

	def new_post(self, args):
		"""
		If we're making a new post, we better be able
		to find the settings file
		"""
		from arcana.settings import settings

		settings.content

new_project_config = '''
# Site Details
site_name = \"{path.name}\"
language = \"en-us\"

# Directories
root = "."
'''

new_command = '''
from arcana.management import BaseCommand

class Command(BaseCommand):
	"""Set command_name and command_help

	"""

	command_name = 'myNewCommand'
	command_help = 'This command does some cool stuff'

	def add_arguments(self, parser):
		"""Add each of the command arguments here
		
		parser.add_argument behaves the same as in the argparse
		library
		"""

		parser.add_argument('arg1',
			help = 'the first argument to your command')

	def run(self, args):
		"""Add the main logic of this command here"""

'''

new_content = '''
---
Title = $$title
Draft = $$draft
---

<!--- Add your content here -->
'''



