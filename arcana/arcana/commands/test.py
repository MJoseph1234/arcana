
from ..management import BaseCommand

class Command(BaseCommand):

	command_name = 'test_command'
	command_help = 'runs a test'

	def add_arguments(self, parser):

		parser.add_argument('text',
			help = 'text to display.')

	def run(self, args):

		print(args.text)