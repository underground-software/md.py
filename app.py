#!/bin/env python3

import markdown as markdown
import os, sys

from orbit import appver, messageblock, ROOT

HTML_404 = '<h1> 404: PAGE NOT FOUND </h1>'
_500	= '500 Internal Server Error'
_500_MSG=b'500 Internal Server Error\n\nunable to load format pre-reqs'

def read_file(filename, mode='r'):
	output = ''
	with open(filename, mode) as f:
		output += f.read()
	return output

def application(env, SR):
	output=''
	try:
                with open(ROOT + '/data/header', 'r') as f:
                        output += f.read()
	except Exception as e:
		SR(_500, [('Content-Type', 'text/plain')])
		return _500_MSG

	path_info = env.get('PATH_INFO', '/index.md')

	# response to request for directory
	# with index.md page within, it exists
	fname = '%s%s' % (ROOT + '/md', path_info)
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

	output += messageblock([('appver', appver())])

	SR(status, [('Content-Type', 'text/html')])
	return [bytes(output, "UTF-8")]
