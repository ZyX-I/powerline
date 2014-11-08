# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

try:
	import vim
except ImportError:
	vim = object()

from powerline.bindings.vim import create_ruby_dpowerline


initialized = False


def initialize():
	global initialized
	if initialized:
		return
	initialized = True
	create_ruby_dpowerline()
	vim.command((
		# When using :execute (vim.command uses the same code) one should not 
		# use << EOF.
		'''
		ruby
		def $powerline.initialize
			if @initialized or $command_t == nil
				return
			end
			@initialized = true
			if (not ($command_t.respond_to? 'active_finder'))
				def $command_t.active_finder
					@active_finder.class.name
				end
			end
			if (not ($command_t.respond_to? 'path'))
				def $command_t.path
					@path
				end
			end
			if (not ($command_t.respond_to? 'is_own_buffer'))
				def $command_t.is_own_buffer buffer_number
					if @match_window
						if (not (@match_window.respond_to? 'buffer_number'))
							def @match_window.buffer_number
								@@buffer and @@buffer.number
							end
						end
						return buffer_number == @match_window.buffer_number
					else
						return false
					end
				end
			end
		end
		def $powerline.commandt_set_active_finder
			$powerline.initialize
			::VIM::command "let g:powerline_commandt_reply = '#{$command_t.active_finder}'"
		end
		def $powerline.commandt_set_path
			$powerline.initialize
			::VIM::command "let g:powerline_commandt_reply = '#{$command_t.path.gsub(/'/, "''")}'"
		end
		def $powerline.commandt_set_own_buffer buffer_number
			$powerline.initialize
			::VIM::command "let g:powerline_commandt_reply = #{($command_t != nil and $command_t.is_own_buffer buffer_number) and 1 or 0}"
		end
		'''
	))


def commandt(matcher_info):
	initialize()
	vim.command('ruby $powerline.commandt_set_own_buffer ' + str(matcher_info['bufnr']))
	return int(vim.eval('g:powerline_commandt_reply'))
