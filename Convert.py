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

		self.replace_code_segment(self.contents)
		self.replace_type_definishion(self.contents)

		self.contents = "".join(self.contents)

		self.contents = self.remove_br_tag(self.contents)
		self.contents = self.replace_code_tag(self.contents)
		self.contents = self.replace_headers(self.contents)

		print(self.contents, end="")
		return 0

	# replacing...
	# ";" -> <dt>
	# ":" -> <dd>
	def replace_type_definishion(self, text_list):
		last_match = None
		current_match = None
		beginning_blank = None

		for i,line in enumerate(text_list):
			current_match = re.search('^[;:].*', line)
			if current_match:
				# Convert mediawiki definishon format to Quiita definishon format.
				if last_match:
					text_list[i] = re.sub('^;(.*)', '  <dt>\\1</dt>', text_list[i])
					text_list[i] = re.sub('^:(.*)', '  <dd>\\1</dd>', text_list[i])
				else:
					text_list[i] = re.sub('^;(.*)', '<dl>\n  <dt>\\1</dt>', text_list[i])
					text_list[i] = re.sub('^:(.*)', '<dl>\n  <dd>\\1</dd>', text_list[i])

			else:
				if last_match:
					# If end of <dl> section, close this section
					text_list[i] = '</dl>\n' + text_list[i]

			last_match = current_match

		if last_match:
			text_list.append("</dl>\n")

		return text_list

	# replacing...
	# <syntaxhighlight lang="langname">
	# ~~~~~~~
	# </syntaxhighlight>
	def replace_code_segment(self, text_list):
		syntax_blank_start_match = None
		syntax_start_tag_match = None
		syntax_finish_tag_match = None

		syntax_blank_match_area = False
		syntax_tag_match_nest_count = 0

		for i,line in enumerate(text_list):
			# replace </syntaxhighlight> tag
			syntax_finish_tag_match = re.search('^</syntaxhighlight>$', line)
			if syntax_finish_tag_match:
				if syntax_tag_match_nest_count == 1:
					text_list[i] = "```\n"

				if (syntax_tag_match_nest_count > 0):
					syntax_tag_match_nest_count -= 1
				continue

			# replace <syntaxhighlight> tag segment
			syntax_start_tag_match = re.search('^<syntaxhighlight lang="?(.*?)"?>$', line)
			if syntax_start_tag_match:

				if syntax_tag_match_nest_count == 0:
					code_title = ""

					if i > 0:
						# format title that in my own rule in mediawiki to code segment title of quiita.
						#
						# * File.txt
						# <syntaxhighlight lang="...">
						my_rule_title = re.search('^\* (.*)', text_list[i - 1])
						if my_rule_title:
							text_list[i - 1] = ""
							code_title = ":" + my_rule_title.group(1)

					text_list[i] = "```" + syntax_start_tag_match.group(1) + code_title + "\n"

				syntax_tag_match_nest_count += 1
				continue

			# replace code segment in a tail of blank
			syntax_blank_start_match = re.search('^ {1}(.*)', line)
			if syntax_blank_start_match:
				if syntax_tag_match_nest_count == 0:
					if not syntax_blank_match_area:
						text_list[i] = "```text\n" + syntax_blank_start_match.group(1) + "\n"
						syntax_blank_match_area = True
					else:
						text_list[i] = syntax_blank_start_match.group(1) + "\n"
			else:
				if syntax_tag_match_nest_count == 0 and syntax_blank_match_area:
					syntax_blank_match_area = False

		if syntax_blank_match_area:
			text_list.append("```\n")

		return

	# replacing...
	# <br /> -> ""
	def remove_br_tag(self, text):
		return  re.sub('<br ?/?>', '', text)

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
