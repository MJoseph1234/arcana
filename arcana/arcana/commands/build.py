
from arcana.settings import ProjectSettings
from arcana.page_maker import Site
from arcana.management import BaseCommand

class Command(BaseCommand):

	command_name = 'build'
	command_help = 'Build a single page or the entire site'

	def add_arguments(self, parser):

		parser.add_argument('-p', '--page',
			help = 'The name of the specific page to build.')
		parser.add_argument('--all',
			help = 'Build the entire site',
			action = 'store_true')
		parser.add_argument('-s', '--static',
			help = 'Update only static files',
			action = 'store_true')

	def run(self, args):
		settings = ProjectSettings(directory = '.')
		if args.all:
			print('building all pages')
			Site(settings).build_site()
			return

		elif args.page:
			pagename = args.page
			gen = Site(settings)
			for page in gen.pages:
				if pagename in {page.name, page.file}:
					print(f'building {page.name}')
					gen.update_single_page(page)

		elif args.static:
			print('compiling static files')
			Site(settings).add_static_files()

		else:
			print('no file or site specified. Doing Nothing.')
			self.print_help()


