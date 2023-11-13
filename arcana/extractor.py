""" Extract from markdown
Extract structured structured data from markdown files
"""

import re
import json

def main(file):
	current_chunk = []
	with open(file) as in_file:
		for line, text in enumerate(in_file):

			if text.startswith('# '):
				if current_chunk:
					process_feat(current_chunk)
				continue

			if text.startswith('## '):
				if current_chunk:
					process_feat(current_chunk)
				current_chunk = [text.strip()]
				continue

			current_chunk.append(text.strip())


def process_chunk(chunk):
	for line, text in enumerate(chunk):
		print(f'{line}: {text}')

def process_feat(chunk):	
	assert(chunk[0].startswith('##'))
	title = chunk.pop(0).replace('## ', '').strip()

	prereq = re.match('^\*Prerequisite: ([a-zA-Z 0-9]+)\*', chunk[0])
	if prereq:
		prereq = prereq.group(1)
		chunk.pop(0)

	assert(chunk[-1].strip() == '')
	chunk.pop()
	match = re.fullmatch('^(Tasha\'s Cauldron of Everything|Player\'s Handbook) pg. ([0-9]+)', chunk.pop())
	assert(match)
	page = match.group(2)
	book = match.group(1)

	description = [line.strip() for line in chunk if line.strip() != '']

	feat = {'title': title,
		'description': description,
		'book': book,
		'page': page}

	if prereq:
		feat['prerequisite'] = prereq
	
	print(json.dumps(feat, sort_keys=True, indent = 4))


if __name__ == '__main__':
	main('markdown/feats.md')