# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

try:
	import vim
except ImportError:
	vim = object()


def finder(pl):
	'''Display Command-T finder name

	Requires $command_t.active_finder and .path methods (code above may 
	monkey-patch $command_t to add them).
	'''
	vim.command('ruby $powerline.commandt_set_active_finder')
	return [{
		'highlight_group': ['commandt:finder'],
		'contents': vim.eval('g:powerline_commandt_reply').replace('CommandT::', '')
	}]


FINDERS_WITHOUT_PATH = set((
	'CommandT::MRUBufferFinder',
	'CommandT::BufferFinder',
	'CommandT::TagFinder',
	'CommandT::JumpFinder',
))


def path(pl):
	vim.command('ruby $powerline.commandt_set_active_finder')
	finder = vim.eval('g:powerline_commandt_reply')
	if finder in FINDERS_WITHOUT_PATH:
		return None
	vim.command('ruby $powerline.commandt_set_path')
	return [{
		'highlight_group': ['commandt:path'],
		'contents': vim.eval('g:powerline_commandt_reply')
	}]
