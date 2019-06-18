#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gdb
from subprocess import getoutput

ADDR_DETAIL = True
SYMBOL_SECTION = False

class CheckSymbol(gdb.Command):
	def __init__(self):
		super(self.__class__, self).__init__('checksymbol', gdb.COMMAND_USER)

	def invoke(self, para_str, from_tty):
		paras = gdb.string_to_argv(para_str)
		if len(paras) != 2:
			print('need 2 para, address length')
			return

		addr = gdb.parse_and_eval(paras[0])
		_len = paras[1]

		raw_out = gdb.execute('x/{}xb {}'.format(_len, addr), to_string=True)
		for line in raw_out.split('\n'):
			if not line:
				continue
			one_line = line.split('\t')
			addr_detail = getoutput('echo \'' + one_line[0] + '\' | c++filt') if ADDR_DETAIL else one_line[0]
			symbol_addr = '0x' + ''.join([i.replace('0x', '') for i in one_line[-1:0:-1]])
			symbol_detail = gdb.execute('info symbol ' + symbol_addr, to_string=True).rstrip('\n')
			if not SYMBOL_SECTION:
				symbol_detail = symbol_detail.split(' in section')[0]
			print(addr_detail, '\t', symbol_addr, '\t', symbol_detail)

CheckSymbol()
