# -*- coding: utf-8 -*-

import os
import json

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

class SimpleConfig(object):
	def __init__(self, config):
		self._config = config

	def __getattr__(self, attr):
		if attr in self._config:
			value = self._config[attr]
			if isinstance(value, dict):
				value = SimpleConfig(value)
		else:
			value = None
		self.__dict__[attr] = value
		return value

class AutoloadConfig(SimpleConfig):
	def __init__(self, filename):
		self._filename = filename

	def __getattr__(self, attr):
		if not self._filename:
			return super(AutoloadConfig, self).__getattr__(attr)
		SimpleConfig.__init__(self, load_json_config(self._filename))
		self._filename = None
		return self.__dict__[attr]

class ThemeConfig(AutoloadConfig):
	def __init__(self, ext, name):
		filename = os.path.join('themes', ext, name)
		super(ThemeConfig, self).__init__(filename)

class ColorschemeConfig(AutoloadConfig):
	def __init__(self, ext, name):
		filename = os.path.join('colorschemes', ext, name)
		super(ColorschemeConfig, self).__init__(filename)

class LocalThemesConfig(object):
	def __init__(self, ext, config):
		self._ext = ext
		self._config = config

	def __getattr__(self, attr):
		self.__dict__[attr] = ThemeConfig(self._ext, getattr(self._config, attr))
		return self.__dict__[attr]

class ExtensionConfig(object):
	def __init__(self, ext, config):
		self.colorscheme = ColorschemeConfig(ext, config.colorscheme)
		self.theme = ThemeConfig(ext, config.theme)
		if hasattr(config, 'local_themes'):
			self.local_themes = LocalThemesConfig(ext, config.local_themes)

class ExtensionsConfig(object):
	def __init__(self, config):
		self._config = config

	def __getattr__(self, attr):
		self.__dict__[attr]=ExtensionConfig(attr, getattr(self._config, attr))
		return self.__dict__[attr]

class CommonConfig(AutoloadConfig):
	def __init__(self):
		filename = 'config'
		super(CommonConfig, self).__init__(filename)

	def __getattr__(self, attr):
		super(CommonConfig, self).__getattr__(attr)
		if attr == 'ext':
			self.ext = ExtensionsConfig(self.ext)
		elif attr == 'paths' and self.paths:
			self.paths = [os.path.expanduser(path) for path in self.paths]
		return self.__dict__[attr]
