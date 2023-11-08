"""
formatting helper tools

catches *many* of the things i find when I copy and paste stuff
from the books. Each thing still needs manual review
"""

def main(infile, outfile):
	with open(infile, 'r') as in_file, open(outfile, 'w') as out_file:
		for line, text in enumerate(in_file):
			text = text.strip()
			if text == '':
				continue

			if text.isupper() and "|" not in text:
				out_file.write(f'\n## {capitalize_words(text)}\n')
				title = line
				table = 0
			elif line == title+1:
				out_file.write(f'*{text}*\n')
				table = 0
			elif text.startswith('|'):
				if table == 1:
					out_file.write(f'{text}\n')
				else:
					out_file.write(f'\n{text}\n')
					table = 1
			elif text.startswith('>'):
				if table == 1:
					out_file.write(f'{text}\n')
				else:
					out_file.write(f'\n{text}\n')
					table = 1
			else:
				if text.split(' ', 1)[0].endswith('.'):
					text = f'**{text.split(" ", 1)[0]}** {text.split(" ", 1)[1]}'
				text = text.replace(' , ', ', ')
				out_file.write(f'\n{text}\n')
				table = 0


def capitalize_words(string):
	return(' '.join(s.capitalize() if s.lower() not in {'of', 'a', 'if', 'is', 'as', 'the'} else s.lower() for s in string.split()))

if __name__ == "__main__":
	main("raw_magic_weapons.txt", "magic_weapons_formatted.md")