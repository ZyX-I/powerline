# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline.editors import EditorBufferNameBase


gundo = EditorBufferNameBase().equals('__Gundo__')
gundo_preview = EditorBufferNameBase().equals('__Gundo_Preview__')
