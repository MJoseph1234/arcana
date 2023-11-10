import time
import os

from page_maker import Site

class Autoreloader():
	SLEEP_TIME = 1

	def __init__(self):
		self.site = Site()

	def run(self):
		ticker = self.tick()
		while True:
			try:
				next(ticker)
			except StopIteration:
				break
			except KeyboardInterrupt:
				print('\nExiting Autoreloader')
				break

	def tick(self):
		mtimes = {}
		while True:
			for page, mtime in self.snapshot_files():
				old_time = mtimes.get(page)
				mtimes[page] = mtime

				if old_time is None:
					continue

				if mtime > old_time:
					print(f'Updating {page.title} from {page.file}')
					self.site.update_single_page(page)

			time.sleep(self.SLEEP_TIME)
			yield

	def snapshot_files(self):
		for page in self.site.pages:
			mtime = os.path.getmtime(page.md_file)
			yield page, mtime
