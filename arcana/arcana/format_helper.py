"""
formatting helper tools

catches *many* of the things i find when I copy and paste stuff
from the books. Each thing still needs manual review
"""

import settings

def main(infile, outfile):
	title = 0
	with open(infile, 'r') as in_file, open(outfile, 'w') as out_file:
		for line, text in enumerate(in_file):
			text = text.strip()
			if text == '':
				continue

			if text.isupper() and "|" not in text and '#' not in text:
				out_file.write(f'\n## {capitalize_words(text)}\n')
				title = line
				table = 0
			elif line == title+1:
				text = check_common_replacements(text)
				out_file.write(f'*{text}*\n')
				table = 0
			elif text.startswith('|'):
				text = check_common_replacements(text)
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
				try:
					text = check_common_replacements(text)
					if '.' in text and text.split('.')[0].count(' ') <= 2:
						text = f'**{text.split(".")[0]}.** {text.split(".", 1)[1]}'
					out_file.write(f'\n{text}\n')

					table = 0
				except:
					print(f'error in line {line}: {text}')



def check_common_replacements(text):
	if text.startswith('- '):
		text = ' - ' + text[2:]
	text = text.replace(' , ', ', ')
	text = text.replace('dlOO', 'd100')
	text = text.replace('dlO', 'd10')
	text = text.replace('ld3', '1d3')
	text = text.replace('ld6', '1d6')
	text = text.replace('ld8', '1d8')
	text = text.replace('­ ', '')
	text = text.replace('+l', '+1')
	text = text.replace('• ', ' - ')
	text = text.replace(' ifyou', ' if you')
	text = text.replace('Ifyou', 'If you')
	text = text.replace('speJJ', 'spell')
	text = text.replace('SpeJJ', 'Spell')
	text = text.replace(' ofthe ', ' of the')
	text = text.replace(' ofyou', ' of you')
	text = text.replace(' ofjewel', ' of jewel')
	text = text.replace(' offorce', ' of force')
	text = text.replace(' ofdeath', ' of death')
	return(text)

def capitalize_words(string):
	return(' '.join(s.capitalize() if s.lower() not in {'of', 'a', 'if', 'is', 'as', 'the'} else s.lower() for s in string.split()))

if __name__ == "__main__":
	main("raw_magic_weapons.txt", "magic_weapons_formatted.md")