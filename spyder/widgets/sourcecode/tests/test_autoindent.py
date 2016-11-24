# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""
Tests for the autoindent features
"""

# Third party imports
from qtpy.QtGui import QTextCursor
import pytest

# Local imports
from spyder.utils.qthelpers import qapplication
from spyder.py3compat import to_text_string
from spyder.widgets.sourcecode.codeeditor import CodeEditor


# --- Fixtures
# -----------------------------------------------------------------------------
def get_indent_fix(text, indent_chars=" " * 4):
    app = qapplication()
    editor = CodeEditor(parent=None)
    editor.setup_editor(language='Python', indent_chars=indent_chars)

    editor.set_text(text)
    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.End)
    editor.setTextCursor(cursor)
    editor.fix_indent()
    return to_text_string(editor.toPlainText())


# --- Tests
# -----------------------------------------------------------------------------
def test_simple_tuple():
    text = get_indent_fix("this_tuple = (1, 2)\n")
    assert text == "this_tuple = (1, 2)\n"


def test_def_with_newline():
    text = get_indent_fix("\ndef function():\n")
    assert text == "\ndef function():\n    ", repr(text)


def test_def_with_indented_comment():
    text = get_indent_fix("def function():\n    # Comment\n")
    assert text == "def function():\n    # Comment\n    ", repr(text)


def test_brackets_alone():
    text = get_indent_fix("def function():\n    print []\n")
    assert text == "def function():\n    print []\n    ", repr(text)


def test_open_parenthesis():
    text = get_indent_fix("open_parenthesis(\n")
    assert text == "open_parenthesis(\n        ", repr(text)


def test_simple_def():
    text = get_indent_fix("def function():\n")
    assert text == "def function():\n    ", repr(text)


# --- Failing tests
# -----------------------------------------------------------------------------
@pytest.mark.xfail
def test_def_with_unindented_comment():
    text = get_indent_fix("def function():\n# Comment\n")
    assert text == "def function():\n# Comment\n    ", repr(text)


# --- Tabs tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text_input, expected, test_text",
    [
        ("this_tuple = (1, 2)\n", "this_tuple = (1, 2)\n", "simple tuple"),
        ("\ndef function():\n", "\ndef function():\n\t", "def with new line"),
        ("def function():\n\t# Comment\n", "def function():\n\t# Comment\n\t",
         "test with indented comment"),
        ("def function():\n\tprint []\n", "def function():\n\tprint []\n\t",
         "test brackets alone"),
        ("\na = {\n", "\na = {\n\t ", "indentation after opening bracket"),
        ("def function():\n", "def function():\n\t", "test simple def"),

        # Failing test
        pytest.mark.xfail(
            ("def function():\n# Comment\n", "def function():\n# Comment\n\t",
             "test_def_with_unindented_comment")),
        pytest.mark.xfail(("open_parenthesis(\n", "open_parenthesis(\n\t\t\t\ŧ ",
                           "open parenthesis")),
    ])
def test_indentation_with_tabs(text_input, expected, test_text):
    text = get_indent_fix(text_input, indent_chars="\t")
    assert text == expected, test_text


if __name__ == "__main__":
    pytest.main()
