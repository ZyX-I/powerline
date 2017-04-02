#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

import os
import sys

from time import sleep
from subprocess import check_call
from difflib import ndiff
from glob import glob1

from powerline.lib.unicode import u
from powerline.lib.dict import updated

from tests.lib.terminal import ExpectProcess


VTERM_TEST_DIR = os.path.abspath('tests/vterm_vim')


def test_expected_result(p, expected_result, rows, row, print_logs):
	expected_text, attrs = expected_result
	attempts = 1
	while attempts:
		actual_text, all_attrs = p.get_row(row, attrs)
		if actual_text == expected_text:
			return True
		attempts -= 1
		print('Actual result does not match expected. Attempts left: {0}.'.format(attempts))
		sleep(2)
	print('Result:')
	print(actual_text)
	print('Expected:')
	print(expected_text)
	print('Attributes:')
	print(all_attrs)
	print('Screen:')
	screen, screen_attrs = p.get_screen(attrs)
	print(screen)
	print(screen_attrs)
	print('_' * 80)
	print('Diff:')
	print('=' * 80)
	print(''.join((u(line) for line in ndiff([actual_text], [expected_text]))))
	if print_logs:
		for f in glob1(VTERM_TEST_DIR, '*.log'):
			print('_' * 80)
			print(os.path.basename(f) + ':')
			print('=' * 80)
			with open(f, 'r') as F:
				for line in F:
					sys.stdout.write(line)
			os.unlink(f)
	return False


def test_one(env={}, vimrc_contents=None, input=None, addargs=[], attempts=3):
	vterm_path = os.path.join(VTERM_TEST_DIR, 'path')
	rows = 20
	cols = 50

	vim_exe = os.path.join(vterm_path, 'vim')

	if os.path.exists('tests/bot-ci/deps/libvterm/libvterm.so'):
		lib = 'tests/bot-ci/deps/libvterm/libvterm.so'
	else:
		lib = os.environ.get('POWERLINE_LIBVTERM', 'libvterm.so')

	vimrc = os.path.join(VTERM_TEST_DIR, 'init.vim')

	vimrc_contents = vimrc_contents or '''
		set laststatus=2
		set runtimepath=powerline/bindings/vim
	'''

	with open(vimrc, 'w') as vd:
		vd.write(vimrc_contents)

	while attempts > 0:
		try:
			p = ExpectProcess(
				lib=lib,
				rows=rows,
				cols=cols,
				cmd=vim_exe,
				args=[
					'-u', vimrc,
					'-i', 'NONE',
				] + addargs,
				env=updated({
					'TERMINFO': os.path.join(VTERM_TEST_DIR, 'terminfo'),
					'TERM': 'st-256color',
					'PATH': vterm_path,
					'SHELL': os.path.join(VTERM_TEST_DIR, 'path', 'bash'),
					'POWERLINE_CONFIG_PATHS': os.path.abspath('powerline/config_files'),
					'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', ''),
					'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
				}, env),
			)
			p.start()
			sleep(5)
			if input:
				p.send(input)
				sleep(2)
			ret = None
			if not test_expected_result(p, ('', {}), rows, rows - 2, not attempts):
				if attempts:
					pass
					# Will rerun main later.
				else:
					ret = False
			elif ret is not False:
				ret = True
			if ret is not None:
				return ret
		finally:
			p.send('\x1C\x0E:qa!\n')  # <C-\><C-n>:qa!<CR>
		attempts -= 1


def main():
	test_one(env={'LANG': 'en_US.UTF-8'})


if __name__ == '__main__':
	if main():
		raise SystemExit(0)
	else:
		raise SystemExit(1)
