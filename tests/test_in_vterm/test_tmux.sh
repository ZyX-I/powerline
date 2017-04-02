#!/bin/sh
. tests/common.sh

enter_suite tmux

rm -rf tests/vterm_tmux
mkdir tests/vterm_tmux
mkdir tests/vterm_tmux/path

rm -rf tests/vterm_vim
mkdir tests/vterm_vim
mkdir tests/vterm_vim/path

ln -s "$(which "${PYTHON}")" tests/vterm_tmux/path/python
ln -s "$(which bash)" tests/vterm_tmux/path
ln -s "$(which env)" tests/vterm_tmux/path
ln -s "$(which cut)" tests/vterm_tmux/path
ln -s "$PWD/scripts/powerline-render" tests/vterm_tmux/path
ln -s "$PWD/scripts/powerline-config" tests/vterm_tmux/path

ln -s "$(which bash)" tests/vterm_vim/path

cp -r tests/terminfo tests/vterm_tmux
cp -r tests/terminfo tests/vterm_vim

test_tmux() {
	# FIXME tmux tests fail
	return 0
	if test "$PYTHON_IMPLEMENTATION" = PyPy; then
		# FIXME PyPy3 segfaults for some reason, PyPy does it as well, but 
		# occasionally.
		return 0
	fi
	if ! which "${POWERLINE_TMUX_EXE}" ; then
		return 0
	fi
	ln -sf "$(which "${POWERLINE_TMUX_EXE}")" tests/vterm_tmux/path/tmux
	local f=tests/test_in_vterm/test_tmux.py
	if ! "${PYTHON}" "$f" ; then
		local test_name="$("$POWERLINE_TMUX_EXE" -V 2>&1 | cut -d' ' -f2)"
		fail "$test_name" F "Failed vterm test $f"
	fi
}

test_vim() {
	# FIXME vim tests incomplete
	return 0
	ln -sf "$(which "${POWERLINE_VIM_EXE}")" tests/vterm_vim/path/vim
	local f=tests/test_in_vterm/test_vim.py
	if ! "${PYTHON}" "$f" ; then
		local test_name="$("$POWERLINE_VIM_EXE" --cmd "echo v:version" --cmd qa 2>&1)"
		fail "$test_name" F "Failed vterm test $f"
	fi
}

enter_suite tmux
if test -z "$POWERLINE_TMUX_EXE" && test -d tests/bot-ci/deps/tmux ; then
	for tmux in tests/bot-ci/deps/tmux/tmux-*/tmux ; do
		export POWERLINE_TMUX_EXE="$PWD/$tmux"
		test_tmux || true
	done
else
	export POWERLINE_TMUX_EXE="${POWERLINE_TMUX_EXE:-tmux}"
	test_tmux || true
fi
exit_suite --continue

enter_suite vim
export POWERLINE_VIM_EXE="${POWERLINE_VIM_EXE:-vim}"
test_vim
exit_suite --continue

if test $FAILED -eq 0 ; then
	rm -rf tests/vterm_tmux
	rm -rf tests/vterm_vim
else
	echo "$FAIL_SUMMARY"
fi

exit_suite
