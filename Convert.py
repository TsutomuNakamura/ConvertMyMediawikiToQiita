#!/usr/bin/python3
import os,sys
import getopt
import re

class Convert:
	# contents of stdin or file
	contents		= None

	def __init__(self):
		# No file or no stdin, then exit
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
		self.replace_type_definition(self.contents)
		self.replace_table_definition(self.contents)

		self.contents = "".join(self.contents)

		self.contents = self.remove_br_tag(self.contents)
		self.contents = self.replace_code_tag(self.contents)
		self.contents = self.replace_headers(self.contents)

		print(self.contents, end="")
		return 0

	# replacing...
	# ";" -> <dt>
	# ":" -> <dd>
	def replace_type_definition(self, text_list):
		last_match = None
		current_match = None
		beginning_blank = None

		for i,line in enumerate(text_list):
			current_match = re.search('^[;:].*', line)
			if current_match:
				# Convert definition format
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
			text_list.append("</dl>\n")

		return text_list

	# Convert table definition
	def replace_table_definition(self, text_list):
		is_table_segment = False
		close_tr_tag = ""

		head_start_tag_map	= {"|": "    <td>", "!": "    <th>"}
		head_end_tag_map	= {"|": "</td>", "!": "</th>"}
		tag_start_map		= {"||": "<td>", "!!": "<th>"}
		tag_end_map			= {"||": "</td>", "!!": "</th>"}

		for i,line in enumerate(text_list):
			if not is_table_segment:
				is_table_segment = re.search('^\{\|.*', line)
				if is_table_segment:
					text_list[i] = "\n<table><tbody>\n"

					# check next line
					match_title_line = re.search('^\|\+.*\|\'\'(.*)\'\'', text_list[i + 1])
					if match_title_line:
						text_list[i] = "\n" + "* " + match_title_line.group(1) + text_list[i]
						text_list[i + 1] = ""
			else:
					
				# 
				ignore_line = re.search('^\|\-.*', line)
				if ignore_line:
					text_list[i] = close_tr_tag + "  <tr>\n"
					close_tr_tag = "  </tr>\n"
					continue
				
				# end of table segment
				is_end_of_table_segment = re.search('\|\}$',line)
				if is_end_of_table_segment:
					text_list[i] = close_tr_tag + "</tbody></table>\n"
					is_table_segment = False
					continue

				tag_start_line = re.search('^(\!|\|){1}(.*)', line)
				if tag_start_line:
					# replacing... | -> <td>, ! -> <th>
					text_list[i] = head_start_tag_map[tag_start_line.group(1)] \
							+ tag_start_line.group(2)
					# replacing... | -> </td>, ! -> </th>
					next_close_tag = head_end_tag_map[tag_start_line.group(1)]
					
					match_line = re.search('(\|\||\!\!)', text_list[i])
					while match_line:
						# || -> <td>, !! -> <th>
						text_list[i] = re.sub(r'(\|\||\!\!)', next_close_tag + tag_start_map[match_line.group(1)], text_list[i], 1)
						# || -> </td>, !! -> </th>
						next_close_tag = tag_end_map[match_line.group(1)]

						match_line = re.search('(\|\||\!\!)', text_list[i])

					text_list[i] = text_list[i] + next_close_tag + "\n"
					continue

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
					text_list[i] = "```\n\n"

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

					text_list[i] = "\n```" + syntax_start_tag_match.group(1) + code_title + "\n"

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
			text_list.append("```\n\n")

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

