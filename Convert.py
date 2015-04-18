#!/usr/bin/python3
import os,sys
import getopt
import re

class Convert:
	# contents of stdin or file
	contents		= None

	def __init__(self):
		# No file or stdin, then exit
		if 2 <= len(sys.argv):
			self.contents = open(sys.argv[1]).readlines()
			return
		
		if not sys.stdin.isatty():
			self.contents = sys.stdin.readlines()
			return

		self.usage()
		sys.exit(1)

	def usage(self):
		print("Usage: please specify file or stdin.")
		print("Example: echo \"some mediawiki format text\" | " + sys.argv[0])
		print("Example: " + sys.argv[0] + " Mediawiki.txt")
		print("Example: " + sys.argv[0] + " << '__EOF__'")
		print("mediawiki format text")
		print("with some breaks")
		print("__EOF__")

	# convert contents
	def convert(self):

		self.replace_type_definishion(self.contents)

		self.contents = "".join(self.contents)

		self.contents = self.replace_code_tag(self.contents)
		self.contents = self.replace_headers(self.contents)

		print(self.contents)
		return 0

	# replacing...
	# ";" -> <dt>
	# ":" -> <dd>
	def replace_type_definishion(self, text_list):
		last_match = None
		current_match = None

		for i,line in enumerate(text_list):
			current_match = re.search('^[;:].*', line)
			if current_match:
				# Convert mediawiki definishon format to Quiita definishon format.
				if last_match:
					text_list[i] = re.sub('^;(.*)', '  <dt>\\1</dt>', text_list[i])
					text_list[i] = re.sub('^:(.*)', '  <dd>\\1</dd>', text_list[i])
				else:
					text_list[i] = re.sub('^;(.*)', '<dl>\n  <dt>\\1</dt>', text_list[i])

			else:
				if last_match:
					# If end of <dl> section, close this section
					text_list[i] = '</dl>\n' + text_list[i]

			last_match = current_match

		if last_match:
			text_list.append('</dl>')

		return text_list

	# replacing...
	# "<code>"  -> "`"
	# "</code>" -> "`"
	def replace_code_tag(self, text):
		return re.sub('</?code>', '`', text)

	# replacing...
	# = text =            -> # text
	# == text ==          -> ## text
	# .......
	# ====== text ======  -> ###### text
	def replace_headers(self, text):
		text = re.sub('======(.*)======', '######\\1', text)
		text = re.sub('=====(.*)=====', '#####\\1', text)
		text = re.sub('====(.*)====', '####\\1', text)
		text = re.sub('===(.*)===', '###\\1', text)
		text = re.sub('==(.*)==', '##\\1', text)
		text = re.sub('=(.*)=', '#\\1', text)
		return text

if __name__ == "__main__":
	Convert().convert()
