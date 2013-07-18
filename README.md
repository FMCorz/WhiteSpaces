White Spaces
============

Plugin for Sublime Text. Display white spaces issues such as trailing spaces, missing line at the end of file and extra spaces, and fix them.

Usage
-----

The following commands are accessible via the command palette:

- White Spaces: Display current issues
- White Spaces: Fix current issues

See the sublime-command file to edit the commands parameters as you like. 

See the settings for automatic display and fix.

Requirements
------------

Sublime Text 2 or 3.

Installation
------------

Simply clone this repository into the Packages directory.

	Preferences > Browse Packages...

Alternatively, add the URL of this repository to the Package Control.

	Command palette > Package Control: Add Repository

Settings
--------

### auto_display

A list of type of white spaces to display as you type. Possible values are:

- eof: Missing line at the end of the file
- extra: In line extra white spaces
- trailing: Trailing white spaces

### fix_on_save

A list of type of white spaces to fix upon saving. The possibles values are the same than for auto_display

### limit_to_syntax

A list of the syntaxes you want to limit the plugin to. This does not apply when you manually execute the commands via the palette. Values understood are the syntax from its package name (Python, LaTeX, JavaScript, ...) or '*' to enable them all.

License
-------

Licensed under the [MIT License](http://www.opensource.org/licenses/mit-license.php)