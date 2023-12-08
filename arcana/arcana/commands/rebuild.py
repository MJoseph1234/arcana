
from arcana.settings import ProjectSettings
from arcana.page_maker import Site
from arcana.management import BaseCommand

class Command(BaseCommand):

	command_name = 'rebuild'
	command_help = 'Rebuild a single page or the entire site'

	def add_arguments(self, parser):

		parser.add_argument('-p', '--page',
			help = 'The filename of the page to rebuild.')
		parser.add_argument('--all',
			help = 'Rebuild the entire site',
			action = 'store_true')
		parser.add_argument('-s', '--static',
			help = 'Update only static files',
			action = 'store_true')

	def run(self, args):
		settings = ProjectSettings(directory = '.')
		if args.all:
			Site(settings).build_site()
			return

		if args.page:
			pagename = args.page
			gen = Site(settings)
			for page in gen.pages:
				if pagename in {page.file_name, page.file}:
					gen.update_single_page(page)

		if args.static:
			Site(settings).add_static_files()
