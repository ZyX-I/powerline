# -*- coding: utf-8 -*-

import importlib
import json
import os
import sys

from powerline.colorscheme import Colorscheme
from powerline.matcher import Matcher
from powerline.lib import underscore_to_camelcase
from powerline.config import CommonConfig, search_paths


class Powerline(object):
	def __init__(self, ext, renderer_module=None, segment_info=None):
		self.config = CommonConfig()
		sys.path[:0] = search_paths

		# Load and initialize extension renderer
		renderer_module_name = renderer_module or ext
		renderer_module_import = 'powerline.renderers.{0}'.format(renderer_module_name)
		renderer_class_name = '{0}Renderer'.format(underscore_to_camelcase(renderer_module_name))
		try:
			Renderer = getattr(importlib.import_module(renderer_module_import), renderer_class_name)
		except ImportError as e:
			sys.stderr.write('Error while importing renderer module: {0}\n'.format(e))
			sys.exit(1)
		self.renderer = Renderer(config, getattr(config.ext, ext))

	def add_local_theme(self, key, config):
		'''Add local themes at runtime (e.g. during vim session).

		Accepts key as first argument (same as keys in config.json:
		ext/*/local_themes) and configuration dictionary as the second (has
		format identical to themes/*/*.json)

		Returns True if theme was added successfully and False if theme with
		the same matcher already exists
		'''
		return
		key = self.get_matcher(key)
		try:
			self.renderer.add_local_theme(key, {'config': config})
		except KeyError:
			return False
		else:
			return True
