# vim:fileencoding=utf-8:noet

from __future__ import unicode_literals

from copy import deepcopy

from powerline import Powerline
import powerline as powerline_module

from tests import TestCase
from tests.lib import replace_item
from tests.lib.config_mock import swap_attributes, get_config_loader


config = {
	'config': {
		'common': {
			'dividers': {
				'left': {
					'hard': '>>',
					'soft': '>',
				},
				'right': {
					'hard': '<<',
					'soft': '<',
				},
			},
			'spaces': 0,
		},
		'ext': {
			'shell': {
				'theme': 'default',
				'colorscheme': 'default',
			},
		},
	},
	'colors': {
		'colors': {
			'col1': 1,
			'col2': 2,
			'col3': 3,
			'col4': 4,
			'col5': 5,
			'col6': 6,
			'grad1': 7,
			'grad2': 8,
		},
		'gradients': {
			'grad1': [list(range(256))],
			'grad2': [list(range(255, -1, -1))],
		},
	},
	'colorschemes/shell/default': {
		'groups': {
			'str1': {'fg': 'col1', 'bg': 'col2', 'attr': ['bold']},
			'str2': {'fg': 'col3', 'bg': 'col4', 'attr': ['underline']},
			'id': {'fg': 'col5', 'bg': 'col6'},
			'id_si': {'fg': 'grad1', 'bg': 'col1', 'attr': ['italic']},
			'grfg': {'fg': 'grad1', 'bg': 'col3'},
			'grbg': {'fg': 'col2', 'bg': 'grad2'},
			'grfb': {'fg': 'grad2', 'bg': 'grad1'},
		},
	},
	'themes/shell/default': {
		'segment_data': {
			'name': {
				'before': 'B',
				'after': 'A',
				'contents': 's',
			},
			'id': {
				'args': {
					'result': 'jkl',
				},
			},
			'id_si': {
				'args': {
					'result': 'str(len(segment_info))',
				},
			},
			'tests.lib.config_mock.id_si': {
				'args': {
					'result': 'str(-len(segment_info))',
				},
			},
		},
		'segments': {
			'left': [
				{
					'type': 'string',
					'name': 'name',
					'highlight_group': ['str1'],
				},
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': [{
							'contents': 'abc',
							'highlight_group': 'str1',
						}],
					}
				},
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': [{
							'contents': 'def',
							'highlight_group': 'grfb',
						}, {
							'contents': 'ghi',
							'highlight_group': 'grfb',
							'gradient_level': 400.0 / 256.0,
						}],
					}
				},
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': [{
							'contents': '',
							'highlight_group': 'str2',
						}],
					}
				},
				{
					'type': 'string',
					'contents': 'g',
					'highlight_group': ['str2'],
				},
			],
			'right': [
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': 'abc',
					},
				},
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': None,
					}
				},
				{
					'name': 'id_si',
					'module': 'tests.lib.config_mock',
					'args': {
						'result': '",".join(sorted(segment_info.keys()))',
					},
				},
				{
					'name': 'id',
					'module': 'tests.lib.config_mock',
				},
				{
					'name': 'id_si',
					'module': 'tests.lib.config_mock',
				},
			],
		},
	},
}


def get_powerline(**kwargs):
	return Powerline(
		config_loader=get_config_loader(),
		**kwargs
	)


class TestRenderer(TestCase):
	def test_rendering(self):
		with replace_item(globals(), 'config', deepcopy(config)):
			with get_powerline(ext='shell', renderer_module='zsh_prompt', run_once=True) as powerline:
				self.maxDiff = None
				self.assertEqual(powerline.render(), '%{\x1b[0;38;5;1;48;5;2;1m%}\xa0BsA%{\x1b[0;38;5;1;48;5;2;22m%}>%{\x1b[0;38;5;1;48;5;2;1m%}abc%{\x1b[0;38;5;2;48;5;7;22m%}>>%{\x1b[0;38;5;8;48;5;7m%}def%{\x1b[0;38;5;7;48;5;4;22m%}>>%{\x1b[0;38;5;251;48;5;4m%}ghi%{\x1b[0;38;5;251;48;5;4;22m%}>%{\x1b[0;38;5;3;48;5;4;4m%}%{\x1b[0;38;5;3;48;5;4;22m%}>%{\x1b[0;38;5;3;48;5;4;4m%}g%{\x1b[0;38;5;4;48;5;6;22m%}>>%{\x1b[0;38;5;6;48;5;4;22m%}<<%{\x1b[0;38;5;5;48;5;6m%}abc%{\x1b[0;38;5;1;48;5;6;22m%}<<%{\x1b[0;38;5;7;48;5;1;3m%}environ,getcwd,home%{\x1b[0;38;5;6;48;5;1;22m%}<<%{\x1b[0;38;5;5;48;5;6m%}jkl%{\x1b[0;38;5;1;48;5;6;22m%}<<%{\x1b[0;38;5;7;48;5;1;3m%}-3\xa0%{\x1b[0m%}')
				# Exact copy of the above. It used to produce different results 
				# on first and subsequent runs
				self.assertEqual(powerline.render(), '%{\x1b[0;38;5;1;48;5;2;1m%}\xa0BsA%{\x1b[0;38;5;1;48;5;2;22m%}>%{\x1b[0;38;5;1;48;5;2;1m%}abc%{\x1b[0;38;5;2;48;5;7;22m%}>>%{\x1b[0;38;5;8;48;5;7m%}def%{\x1b[0;38;5;7;48;5;4;22m%}>>%{\x1b[0;38;5;251;48;5;4m%}ghi%{\x1b[0;38;5;251;48;5;4;22m%}>%{\x1b[0;38;5;3;48;5;4;4m%}%{\x1b[0;38;5;3;48;5;4;22m%}>%{\x1b[0;38;5;3;48;5;4;4m%}g%{\x1b[0;38;5;4;48;5;6;22m%}>>%{\x1b[0;38;5;6;48;5;4;22m%}<<%{\x1b[0;38;5;5;48;5;6m%}abc%{\x1b[0;38;5;1;48;5;6;22m%}<<%{\x1b[0;38;5;7;48;5;1;3m%}environ,getcwd,home%{\x1b[0;38;5;6;48;5;1;22m%}<<%{\x1b[0;38;5;5;48;5;6m%}jkl%{\x1b[0;38;5;1;48;5;6;22m%}<<%{\x1b[0;38;5;7;48;5;1;3m%}-3\xa0%{\x1b[0m%}')


replaces = {}


def setUpModule():
	global replaces
	replaces = swap_attributes(globals(), powerline_module, replaces)


tearDownModule = setUpModule


if __name__ == '__main__':
	from tests import main
	main()
