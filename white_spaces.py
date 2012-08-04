# -*- coding: utf-8 -*-

"""
White Spaces

Plugin for Sublime Text 2 to manage white spaces issues

Copyright (c) 2012 Frédéric Massart - FMCorz.net

Licensed under The MIT License
Redistributions of files must retain the above copyright notice.

http://github.com/FMCorz/WhiteSpaces
"""

from os.path import split
import sublime, sublime_plugin
import threading

class WhiteSpaces():

	def __init__(self, view):
		self.settings = sublime.load_settings('Settings.sublime-settings')
		self.view = view

	def canInSyntax(self):
		"""Validates the syntax against the user's preferences"""
		syntax = self.view.settings().get('syntax')
		syntax = split(syntax)[0].replace('Packages/', '')
		allowed = self.settings.get('limit_to_syntax')
		if '*' in allowed or syntax in allowed:
			return True
		return False

	def display(self, modes = None):
		"""Displays the white spaces"""

		# Prevents from running in context Find, Quick command, etc...
		if self.view.file_name() == None:
			return

		# This if means we are in event mode
		if type(modes) != list:
			if not self.canInSyntax():
				return
			modes = self.settings.get('auto_display')

		if 'eof' in modes:
			self.displayEof()
		if 'extra' in modes:
			callback = lambda: self.displayExtra()
			self.setTimeout(callback)
		if 'trailing' in modes:
			callback = lambda: self.displayTrailing()
			self.setTimeout(callback)

	def displayEof(self):
		"""Show a missing line at the end of the document"""
		self.view.erase_regions('trim_spaces_eof')
		if self.view.substr(self.view.size()-1) != "\n":
			region = [ sublime.Region(self.view.size()-1, self.view.size()) ]
			self.view.add_regions('trim_spaces_eof', region, 'invalid')

	def displayExtra(self, regions = None):
		"""Displays multiplied spaces"""
		# Experimental memory/process saving
		if regions != None:
			mark = []
			lines = []

			# Find white spaces
			for region in self.view.sel():
				l = self.view.line(region)
				lines.append(l)
				seek = l.begin()

				# Search loop within the line
				while seek:

					# TODO Fix overlapping regions issue
					find = self.view.find('\S[ ]{2,}\S', seek)

					# No result, we can leave the loop
					if find == None:
						seek = None
						continue

					mark.append(sublime.Region(find.begin()+1, find.end()-1))

					# Restart the search
					if find.end()-1 < l.end():
						seek = find.end()-1
					else:
						seek = None

			# Reconstruct region list removing any region in working lines
			for l in lines:
				for x in self.view.get_regions('trim_spaces_extra'):
					if not l.contains(x):
						mark.append(x)

		else:
			mark = self.view.find_all('\S[ ]{2,}\S')
			# TODO fix the \S which is considered as a character and kills some matches
			for i in xrange(len(mark)-1, -1, -1):
				r = mark[i]
				if self.view.score_selector(r.begin(), 'string.quoted'):
					# Delete if in a string scope
					del mark[i]
				else:
					# Recreate the region to exclude first and last chars
					mark[i] = sublime.Region(r.begin()+1, r.end()-1)

		self.view.add_regions('trim_spaces_extra', mark, 'invalid')

	def displayTrailing(self, regions = None):
		"""Displays trailing spaces"""
		# Experimental memory/process saving
		if regions:
			mark = []
			lines = []

			# Adds regions from current working lines
			for region in self.view.sel():
				l = self.view.line(region)
				lines.append(l)
				find = self.view.find('[ \t]+$', l.begin())
				if find != None:
					mark.append(find)

			# Reconstruct region list removing any region in working lines
			for l in lines:
				for x in self.view.get_regions('trim_spaces'):
					if not l.contains(x):
						mark.append(x)

		else:
			mark = self.view.find_all("[\t ]+$")

		self.view.add_regions('trim_spaces', mark, 'invalid')

	def fix(self, edit, modes):
		"""Triggers the fix actions"""
		# This if means we are in event mode
		if type(modes) != list:
			if not self.canInSyntax():
				return
			modes = self.settings.get('fix_on_save')

		if 'eof' in modes:
			self.fixEof(edit)
		if 'extra' in modes:
			self.fixExtra(edit)
		if 'trailing' in modes:
			self.fixTrailing(edit)

	def fixEof(self, edit):
		"""Fix the missing new line at the end of line"""
		if len(self.view.get_regions('trim_spaces_eof')) > 0:
			self.view.insert(edit, self.view.size(), "\n")
			self.view.erase_regions('trim_spaces_eof')

	def fixExtra(self, edit):
		"""Fix extra white spaces"""
		regions = self.view.get_regions('trim_spaces_extra')
		regions.reverse()
		for region in regions:
			self.view.replace(edit, region, ' ')

	def fixTrailing(self, edit):
		"""Fix trailing white spaces"""
		regions = self.view.get_regions('trim_spaces')
		regions.reverse()
		for region in regions:
			self.view.erase(edit, region)

	def setTimeout(self, command):
		"""Experimental way of not blocking the process"""
		time = 10
		sublime.set_timeout(command, time)

class WhiteSpacesEvent(sublime_plugin.EventListener):
	"""Events are handled in this class"""

	def on_load(self, view):
		ws = WhiteSpaces(view)
		ws.display()

	def on_modified(self, view):
		ws = WhiteSpaces(view)
		ws.display()

	def on_pre_save(self, view):
		view.run_command('white_spaces_fix', None)

class WhiteSpacesDisplayCommand(sublime_plugin.TextCommand):
	"""Command to display the white spaces"""

	def run(self, edit, modes = None):
		ws = WhiteSpaces(self.view)
		ws.display(modes)

class WhiteSpacesFixCommand(sublime_plugin.TextCommand):
	"""Command to fix the white spaces issues"""

	def run(self, edit, modes = None):
		ws = WhiteSpaces(self.view)
		ws.fix(edit, modes)
