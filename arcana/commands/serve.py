from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type

from arcana.management import BaseCommand
from arcana.core import Site


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

		parser.add_argument('-p', '--port',
		help = 'Port number to use',
		default = '8080',
		type = int)

	def run(self, args):
		"""Add the main logic of this command here"""

		host_name = 'localhost'
		port = args.port
		request_handler = build_request_handler(args)
		webserver = HTTPServer((host_name, port), request_handler)
		
		print(f'Server started http://{host_name}:{port}')
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
			site = Site(include_drafts = args.include_drafts)

			(mime_type, encoding) = guess_type(self.path)

			segments = [piece for piece in self.path.split('/') if piece != '']
			if len(segments) == 0:
				# TODO handle default page/index.html
				pass
			elif len(segments) == 1:
				resource = url[0]
				path = 'content'
			else:
				resource = url[-1]
				path = '/'.join(segments[0:-1])

			if resource.endswith('.html'):
				resource = resource.replace('.html', '')

			if path == 'static/':
				self.send_response(200)
				self.send_header('Content-type', mime_type)
				self.end_headers()
				with open(Path('static/').joinpath(resource), 'r') as static:
					for line in static:
						self.wfile.write(bytes(line, 'utf-8'))
				return

			self.send_response(200)
			self.send_header('Content-type', mime_type)
			self.end_headers()
			for page in site.pages:
				if rq == page.slug:
					for line in site.build_page(page):
						self.wfile.write(bytes(line, 'utf-8'))

	return ArcanaRequestHandler



