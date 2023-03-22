#!/bin/env python3

import markdown as markdown
import os, sys
from config import PREPEND, MD_ROOT, DEBUG, HTML_404

if DEBUG:
	from genhtml import debug_table
else:
	debug_table = lambda x: ''

APPLICATION='earth'
VERSION='0.1'
_500	= '500 Internal Server Error'
_500_MSG=b'500 Internal Server Error\n\nunable to load format pre-reqs'

def appver():
	return "%s %s" % (APPLICATION, VERSION)

def messageblock(l):
	s='<br /><hr /><br />'
	m = s
	for i in l:
		m += "<code>%s = %s</code><br />" % (str(i[0]), str(i[1]))
	m += s

	return m

def read_file(filename, mode='r'):
	output = ''
	with open(filename, mode) as f:
		output += f.read()
	return output

def application(env, SR):
	output=''
	try:
		for path in PREPEND:
			with open(path, 'r') as f:
				output += f.read()
	except Exception as e:
		SR(_500, [('Content-Type', 'text/plain')])
		return _500_MSG

	path_info = env.get('PATH_INFO', '/index.md')

	# response to request for directory
	# with index.md page within, it exists
	fname = '%s%s' % (MD_ROOT, path_info)
	if os.path.isdir(fname):
		fname += '/index.md'

	# return any .md file in MD_ROOT
	try:
		with open(fname, 'r', newline='') as f:
			output += markdown.markdown(f.read(), extensions=['tables'])
		status = '200 Ok'
	except Exception as e:
		output += HTML_404
		status = '404 Not Found'

	output += debug_table(fname)
	output += messageblock([('appver', appver())])

	SR(status, [('Content-Type', 'text/html')])
	return [bytes(output, "UTF-8")]
