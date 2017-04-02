#!/bin/sh
# FIXME vim tests incomplete
exit 0
. tests/common.sh

enter_suite vim

rm -rf tests/vterm_vim
mkdir tests/vterm_vim
mkdir tests/vterm_vim/path

ln -s "$(which bash)" tests/vterm_vim/path

cp -r tests/terminfo tests/vterm_vim

test_vim() {
	ln -sf "$(which "${POWERLINE_VIM_EXE}")" tests/vterm_vim/path/vim
	local f=tests/test_in_vterm/test_vim.py
	if ! "${PYTHON}" "$f" ; then
		local test_name="$("$POWERLINE_VIM_EXE" --cmd "echo v:version" --cmd qa 2>&1)"
		fail "$test_name" F "Failed vterm test $f"
	fi
}

export POWERLINE_VIM_EXE="${POWERLINE_VIM_EXE:-vim}"
test_vim

if test $FAILED -eq 0 ; then
	rm -rf tests/vterm_vim
else
	echo "$FAIL_SUMMARY"
fi

exit_suite


