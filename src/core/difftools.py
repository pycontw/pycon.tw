import difflib

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


def dump_equal(a, b, loa, lob, hia, hib):
    for line in a[loa:hia]:
        yield mark_safe(conditional_escape(line))


def dump_delete(a, b, loa, lob, hia, hib):
    for line in a[loa:hia]:
        yield mark_safe('<del>{}</del>'.format(conditional_escape(line)))


def dump_insert(a, b, loa, lob, hia, hib):
    for line in b[lob:hib]:
        yield mark_safe('<ins>{}</ins>'.format(conditional_escape(line)))


def dump_replace(a, b, loa, lob, hia, hib):
    # TODO: Character diff.
    yield from dump_delete(a, b, loa, lob, hia, hib)
    yield from dump_insert(a, b, loa, lob, hia, hib)


BLOCK_HANDLERS = {
    'replace': dump_replace,
    'equal': dump_equal,
    'delete': dump_delete,
    'insert': dump_insert,
}


def make_diff(a, b):
    cruncher = difflib.SequenceMatcher(None, a, b)
    for tag, loa, hia, lob, hib in cruncher.get_opcodes():
        yield from BLOCK_HANDLERS[tag](a, b, loa, lob, hia, hib)
