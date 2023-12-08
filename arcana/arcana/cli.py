"""
This should be depricated
	need to move Serve command
	need to move extract commands to arcana-check's project specific commands
"""

import argparse
import os
from pathlib import Path

import page_maker
import format_helper
from settings import ProjectSettings
from autoreload import Autoreloader
from server import run_webserver
import commands

def main():
	parser = build_parser()

	args = parser.parse_args()

	if args.directory == '.':
		args.directory = Path.cwd()
	elif not Path(args.directory).is_dir():
		return
	else:
		if not Path(args.directory).is_absolute():
			args.directory = Path.cwd().joinpath(args.directory)
		else:
			args.directory = Path(args.directory)

	s = ProjectSettings(directory = args.directory)

	args.func(args)

def build_parser():
	parser = argparse.ArgumentParser(
		prog = 'arcana',
		description = 'Arcana static site generator')

	parser.add_argument('directory',
		nargs = '?',
		default = '.',
		help = 'directory in which to run Arcana')

	subparsers = parser.add_subparsers(title = 'commands',
		description = 'Arcana commands',
		required = True,
		dest = 'command')

	rebuild_parser = subparsers.add_parser('rebuild', 
		help = 'Rebuild a page or the entire site')
	rebuild_parser.add_argument('-p', '--page',
		help = 'The filename of the page to rebuild.')
	rebuild_parser.add_argument('--all',
		help = 'Rebuild the entire site',
		action = 'store_true')
	rebuild_parser.add_argument('-s', '--static',
		help = 'Update only static files',
		action = 'store_true')
	rebuild_parser.set_defaults(func=rebuild)

	formatter_parser = subparsers.add_parser('format',
		help = 'Fix basic formatting issues from pasted text')
	formatter_parser.add_argument('infile',
		help = "input file to format")
	formatter_parser.add_argument('outfile',
		help = 'output file. Will be overwritten if it already exists')
	formatter_parser.set_defaults(func=do_format)

	monitor_parser = subparsers.add_parser('autoreload',
		help = 'Watch markdown pages for updates and regenerate HTML as needed')
	monitor_parser.set_defaults(func=run_autoreload)

	server_parser = subparsers.add_parser('serve',
		help = 'Watch markdown pages for updates and regenerate HTML as needed')
	server_parser.set_defaults(func=serve)

	return(parser)


def rebuild(args):
	if args.all:
		page_maker.Site().build_site()
		return

	if args.page:
		pagename = args.page
		gen = page_maker.Site()
		for page in gen.pages:
			if pagename in {page.file_name, page.file}:
				gen.update_single_page(page)

	if args.static:
		page_maker.Site().add_static_files()

def do_format(args):
	base = settings.root
	in_file = os.path.join(base, 'old_stuff', args.infile)
	out_file = os.path.join(base, 'old_stuff', args.outfile)
	format_helper.main(in_file, out_file)

def run_autoreload(args):
	x = Autoreloader()
	print(f'Monitoring files in {x.site.input_directory}')
	print('Press CTRL+C to exit')
	x.run()

def serve(args):
	s = ProjectSettings(directory = args.directory)
	path = Path(s.root).joinpath(s.public)
	print(path)
	run_webserver(path)

if __name__ == '__main__':
	main()