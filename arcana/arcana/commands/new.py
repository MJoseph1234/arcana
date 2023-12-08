from pathlib import Path

from arcana.management import BaseCommand

class Command(BaseCommand):

	command_name = 'new'
	command_help = 'Start a new Arcana project'

	def add_arguments(self, parser):

		parser.add_argument('path',
			help = 'relative path to new directory')

	def run(self, args):

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