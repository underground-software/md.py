#!/bin/env python3

import os

def h(v, c):
	return '<h%d>%s</h%d>' % (v, c, v)

def h1(c):
	return h(1, c)

def h2(c):
	return h(2, c)

def h3(c):
	return h(2, c)

def t_i(i):
	return ''.join(['\t' for x in range(i)])

def o(i, c):
	return '%s%s\n' % (t_i(i), c)

def ooo(i, c, d, e, j=0):
	return '%s%s%s' % (o(i, c), o(i+j, d), o(i, e))

def oOo(i, c, d, e):
	return ooo(i, c, d, e, j=1)

def oxo(i, c, d, e):
	return '%s%s%s' % (o(i, c), d, o(i, e))

def table_data(c, h=False, i=0):
	d = 'd'
	if h:
		d = 'h'
	a, b = '<t%s>' % d, '</t%s>' % d
	return oOo(i, a, c, b)

def table_row(c, h=False, i=0):
	d = ''.join([table_data(d, h=h, i=i+1) for d in c])
	return oxo(i, '<tr>', d, '</tr>')

def table(c, i=0):
	t=''
	h=True
	for r in c:
		t += table_row(r, h, i=i+1)
		h=False
	return oxo(i, '<table>', t, '</table>')

def debug_table(fname):
	tc = [('key', 'value')]
	found =''
	try:
		if os.path.exists(fname):
			tc += [('fname', fname)]
			tc += [('exists', str(True))]
			tc += [('isfile', str(os.path.isfile(fname)))]
			tc += [('isdir', str(os.path.isdir(fname)))]
		else:
			tc += [('fname', fname)]
			tc += [('exists', str(False))]

		if os.path.isdir(fname):
			fname += '/index.md'
			tc += [('isdir =>', fname)]
			tc += [('isfile', str(os.path.isfile(fname)))]
			tc += [('isdir', str(os.path.isdir(fname)))]
			tc += [('exists', str(os.path.exists(fname)))]
	except FileNotFoundEror as e:
		tc += [(fname, 'error')]

	return table(tc)
