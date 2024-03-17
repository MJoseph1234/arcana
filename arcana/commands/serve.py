import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type

from arcana.management import BaseCommand
from arcana.settings import settings
from arcana.core import Site, Page


class Command(BaseCommand):
	"""Set command_name and command_help"""

	command_name = 'serve'
	command_help = 'Run a small web server for your arcana site'

	def add_arguments(self, parser):
		"""Add each of the command arguments here
		
		parser.add_argument behaves the same as in the argparse
		library
		"""

		parser.add_argument('-d', '--include-drafts',
		help = 'Include draft pages',
		action = 'store_true')

		parser.add_argument('-a', '--address',
			help = 'IP and port number for the development server. Written as an IP:PortNumber pair',
			default = '127.0.0.1:8080')

	def run(self, args):
		"""Add the main logic of this command here"""

		addr, port = args.address.split(':')
		request_handler = build_request_handler(args)
		webserver = HTTPServer((addr, int(port)), request_handler)
		
		print(f'Server started http://{addr}:{port}')
		try:
			webserver.serve_forever()
		except KeyboardInterrupt:
			pass

		webserver.server_close()
		print('\nServer stopped')

def build_request_handler(args):
	class ArcanaRequestHandler(BaseHTTPRequestHandler):
		def do_GET(self):
			self.resolve_path_to_file()

		def resolve_path_to_file(self):
			# site = Site(include_drafts = args.include_drafts)

			(mime_type, encoding) = guess_type(self.path, strict = False)

			if mime_type in {'application/javascript', 'text/css'}:
				return(self.handle_static(mime_type))
			
			segments = [piece for piece in self.path.split('/') if piece != '']
			path = ''
			if len(segments) == 0:
				resource = settings['home']
			elif len(segments) == 1:
				resource = segments[0]
			else:
				resource = segments[-1]
				path = Path('.').joinpath(*segments[0:-1])

			if resource.endswith('.html'):
				resource = resource.replace('.html', '')

			self.send_response(200)
			self.send_header('Content-type', mime_type)
			self.end_headers()

			for file in os.listdir(Path(settings['dirs']['content']).joinpath(path)):
				if file == resource + '.md': # Otherwise, we should also check Page.slug for a match
					page = Page(file, path)
					for line in Site().build_page(page):
						self.wfile.write(bytes(line, 'utf-8'))

		def handle_static(self, mime_type):

			segments = [piece for piece in self.path.split('/') if piece != '']
			resource = segments[-1]

			with open(Path(settings['dirs']['static']).joinpath(resource), 'r') as static:
				self.send_response(200)
				self.send_header('Content-type', mime_type)
				self.end_headers()
				for line in static:
					self.wfile.write(bytes(line, 'utf-8'))
			return

	return ArcanaRequestHandler



