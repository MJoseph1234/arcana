
from arcana.settings import ProjectSettings
from arcana.autoreload import Autoreloader
from arcana.management import BaseCommand

class Command(BaseCommand):

	command_name = 'autoreload'
	command_help = 'watch content pages for changes and update HTML'

	def run(self, args):
		x = Autoreloader(ProjectSettings(directory = '.'))
		print(f'Monitoring files in {x.site.settings.content}')
		print('Press CTRL+C to exit')
		x.run()