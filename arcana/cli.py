import argparse
import os

import page_maker
import format_helper
import settings
from autoreload import Autoreloader

def main():
	parser = build_parser()

	args = parser.parse_args()


	args.func(args)

def build_parser():
	parser = argparse.ArgumentParser(
		prog = 'arcana',
		description = 'Arcana static site generator')

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
	base = settings.BASE
	in_file = os.path.join(base, 'old_stuff', args.infile)
	out_file = os.path.join(base, 'old_stuff', args.outfile)
	format_helper.main(in_file, out_file)

def run_autoreload(args):
	x = Autoreloader()
	print(f'Monitoring files in {x.site.input_directory}')
	print('Press CTRL+C to exit')
	x.run()

if __name__ == '__main__':
	main()