import argparse

import page_maker

def main():
	parser = build_parser()

	args = parser.parse_args()

	args.func(args)

def build_parser():
	parser = argparse.ArgumentParser(
		prog = 'arcana',
		description = 'static site generator')

	subparsers = parser.add_subparsers(required = True,
		help = 'Arcana command to run')

	rebuild_parser = subparsers.add_parser('rebuild', 
		help = 'Rebuild a page or the entire site')
	rebuild_parser.add_argument('-p', '--page',
		help = 'The filename of the page to rebuild.')
	rebuild_parser.add_argument('--all',
		help = 'Rebuild the entire site',
		action = 'store_true')
	rebuild_parser.set_defaults(func=rebuild)

	return(parser)

def rebuild(args):
	if args.all:
		page_maker.SiteGenerator().build_site()
		return

	if args.page:
		pagename = args.page
		gen = page_maker.SiteGenerator()
		for page in gen.pages:
			if pagename in {page.file_name, page.file}:
				gen.update_single_page(page)

if __name__ == '__main__':
	main()