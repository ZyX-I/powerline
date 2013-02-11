# -*- coding: utf-8 -*-

import os
import json
from powerline.matcher import Matcher

config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
config_path = os.path.join(config_home, 'powerline')
plugin_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'config_files')
search_paths = [config_path, plugin_path]

def load_json_config(config_file, paths=search_paths):
	config_file += '.json'
	for path in paths:
		config_file_path = os.path.join(path, config_file)
		if os.path.isfile(config_file_path):
			with open(config_file_path, 'r') as config_file_fp:
				return json.load(config_file_fp)
	raise IOError('Config file not found in search path: {0}'.format(config_file))

def get_config_value(value, key=None, override=None):
	return SimpleConfig(value, get_override(override, key)) if isinstance(value, dict) else value

empty_override = {}

def get_override(override, key):
	return override.get(key) if override else empty_override

class SimpleConfig(object):
	def __init__(self, config, override):
		self._config = config
		self._override = override

	def __getattr__(self, attr):
		if attr in self._override:
			value = get_config_value(self._override[attr])
		elif attr in self._config:
			value = get_config_value(self._config[attr], attr, self._override)
		else:
			value = None

		self.__dict__[attr] = value
		return value

	def __getitem__(self, key):
		return getattr(self, key)

	def __contains__(self, key):
		return hasattr(self, key) or (key in self._override) or (key in self._config)

class LazyConfig(SimpleConfig):
	def __init__(self, filename, override):
		self._filename = filename
		self._override = override

	def __getattr__(self, attr):
		if self._filename:
			SimpleConfig.__init__(self, load_json_config(self._filename), self._override)
			self._filename = None
		return super(LazyConfig, self).__getattr__(attr)

class ThemeConfig(LazyConfig):
	def __init__(self, ext, name, override):
		filename = os.path.join('themes', ext, name)
		override = get_override(override, name)
		super(ThemeConfig, self).__init__(filename, override)

class ColorschemeConfig(LazyConfig):
	def __init__(self, ext, name, override):
		filename = os.path.join('colorschemes', ext, name)
		super(ColorschemeConfig, self).__init__(filename, override)

class LocalThemesConfig(object):
	def __init__(self, ext, config, override, common_config):
		self.ext = ext
		self.config = config
		self.override = get_override(override, 'local_themes')
		self.themes_override = get_override(override, 'themes')
		self.matchers = {}
		self.paths = common_config.paths
		self._get_matcher = None

	def get_matcher(self, key):
		if key in self.matchers:
			return self.matchers[key]
		matcher = self._get_matcher(key)
		self.matchers[key] = matcher
		return matcher

	def __iter__(self):
		if not self._get_matcher:
			self._get_matcher = Matcher(self.ext, self.paths).get
		for key, value in self.override.items():
			yield self.get_matcher(key), ThemeConfig(self.ext, value, self.themes_override)
		if self.config:
			for key, value in self.config.items():
				if key not in self.override:
					yield self.get_matcher(key), ThemeConfig(self.ext, value, self.themes_override)

class ExtensionConfig(object):
	def __init__(self, ext, config, override, common_config):
		self.colorscheme = ColorschemeConfig(ext, config.colorscheme, get_override(override, 'colorscheme'))
		themes_override = get_override(override, 'themes')
		self.theme = ThemeConfig(ext, config.theme, themes_override)
		if hasattr(config, 'local_themes'):
			self.local_themes = LocalThemesConfig(ext, config.local_themes, override, common_config)

class ExtensionsConfig(object):
	def __init__(self, config, override, common_config):
		self._config = config
		self._override = override
		self._common_config = common_config

	def __getattr__(self, attr):
		self.__dict__[attr]=ExtensionConfig(attr, getattr(self._config, attr), get_override(self._override, attr), self._common_config)
		return self.__dict__[attr]

	def __getitem__(self, key):
		return getattr(self, key)

class CommonConfig(LazyConfig):
	def __init__(self, override):
		filename = 'config'
		super(CommonConfig, self).__init__(filename, override)

	def __getattr__(self, attr):
		super(CommonConfig, self).__getattr__(attr)
		if attr == 'ext':
			self.ext = ExtensionsConfig(self.ext, self._override.get('ext'), self)
		elif attr == 'paths':
			if self.paths:
				self.paths = [os.path.expanduser(path) for path in self.paths]
			else:
				self.paths = []
		return self.__dict__[attr]
