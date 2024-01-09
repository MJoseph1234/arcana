from pathlib import Path
from string import Template

from arcana.settings import settings
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
		new_project.set_defaults(func = self.new_project)

		# New Post command for creating a new file for the current
		# arcana project
		new_post = subparser.add_parser(
			name = 'post',
			help = 'create a new post or document in the project content directory')
		new_post.add_argument('name',
			help = 'Name or page title for the new post')
		new_post.set_defaults(func = self.new_post)

		new_command = subparser.add_parser(
			name = 'command',
			help = 'create a new arcana CLI command for your project')
		new_command.add_argument('name',
			help = 'Name or page title for the new command')
		new_command.set_defaults(func = self.new_command)

	def run(self, args):
		args.func(args)

	def new_project(self, args):
		project_root = Path(args.path)
		if project_root.is_dir():
			print('that path already exists, exiting and doing nothing')
			return

		project_root.mkdir()
		for directory in settings['dirs']:
			project_root.joinpath(directory).mkdir()

		config_file = project_root.joinpath(f'{project_root.name}.toml')
		config_str = Template(settings['new']['config_file_template'])

		with open(config_file, mode = 'w') as f:
			f.write(config_str.substitute(
				site_name = project_root.name,
				site_language = settings['language']
			))

	def new_post(self, args):
		"""
		If we're making a new post, we better be able
		to find the settings file
		"""
		content_dir = Path(settings['dirs']['content'])
		file_path = content_dir.joinpath(args.name)
		new_post_str = Template(settings['new']['post_template'])

		with open(file_path, 'w') as f:
			f.write(new_post_str.substitute(
				title = args.name,
				draft = settings['new_post_as_draft']
			))


	def new_command(self, args):
		"""
		Get the command folder from settings
		if it's not there, create it based on defaults
		create a new <command>.py file and fill it with the
		new command string
		"""
		command_dir = Path(settings['dirs']['commands'])
		command_name = args.name.replace(' ', '').lower()
		file_path = command_dir.joinpath(command_name)

		if file_path.exists():
			print(f'{file_path} already exists. Doing nothing')
			return
		
		if not command_dir.is_dir():
			command_dir.mkdir()

		with open(file_path, 'w') as f:
			f.write(settings['new']['command_template'])




