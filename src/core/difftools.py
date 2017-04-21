import difflib

from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from core.utils import html_join


def dump_replace(a, b, alo, blo, ahi, bhi):
    # Based on `difflib.Differ._fancy_replace`.
    # When replacing one block of lines with another, search the blocks
    # for *similar* lines; the best-matching pair (if any) is used as a
    # sync point, and intraline difference marking is done on the
    # similar pair. Lots of work, but often worth it.
    best_ratio = 0
    cutoff = 0.8
    cruncher = difflib.SequenceMatcher(difflib.IS_CHARACTER_JUNK)
    eqi, eqj = None, None

    # Search for the first sync point.
    for j in range(blo, bhi):
        bj = b[j]
        cruncher.set_seq2(bj)
        for i in range(alo, ahi):
            ai = a[i]
            if ai == bj:
                if eqi is None:
                    eqi, eqj = i, j
                continue
            cruncher.set_seq1(ai)
            if (cruncher.real_quick_ratio() > best_ratio and
                    cruncher.quick_ratio() > best_ratio and
                    cruncher.ratio() > best_ratio):
                best_ratio, best_i, best_j = cruncher.ratio(), i, j

    # No "pretty close" pair.
    if best_ratio < cutoff:
        if eqi is None:     # No identical pairs. Just dump.
            yield from dump_delete(a, b, alo, blo, ahi, bhi)
            yield from dump_insert(a, b, alo, blo, ahi, bhi)
            return
        # There's an identical pair. Use that.
        best_i, best_j, best_ratio = eqi, eqj, 1.0
    else:
        eqi = None

    # Dump things before the sync point.
    yield from replace_helper(a, alo, best_i, b, blo, best_j)

    # Intraline marking.
    aelt, belt = a[best_i], b[best_j]
    if eqi is None:
        atags = []
        btags = []
        cruncher.set_seqs(aelt, belt)
        for tag, ai1, ai2, bj1, bj2 in cruncher.get_opcodes():
            acon, bcon = aelt[ai1:ai2], belt[bj1:bj2]
            if tag == 'replace':
                atags.append(format_html('<del>{}</del>', acon))
                btags.append(format_html('<ins>{}</ins>', bcon))
            elif tag == 'delete':
                atags.append(format_html('<del>{}</del>', acon))
            elif tag == 'insert':
                btags.append(format_html('<ins>{}</ins>', bcon))
            else:   # Equal.
                atags.append(acon)
                btags.append(bcon)
        yield format_html('<del>{}</del>', html_join('', atags))
        yield format_html('<ins>{}</ins>', html_join('', btags))
    else:   # Identical.
        yield aelt

    # Dump things after the sync point.
    yield from replace_helper(a, best_i + 1, ahi, b, best_j + 1, bhi)


def replace_helper(a, alo, ahi, b, blo, bhi):
    if alo < ahi:
        if blo < bhi:
            yield from dump_replace(a, alo, ahi, b, blo, bhi)
        else:
            yield from dump_delete(a, b, alo, blo, ahi, bhi)
    elif blo < bhi:
        yield from dump_insert(a, b, alo, blo, ahi, bhi)


def dump_equal(a, b, loa, lob, hia, hib):
    for line in a[loa:hia]:
        yield mark_safe(conditional_escape(line))


def dump_delete(a, b, loa, lob, hia, hib):
    for line in a[loa:hia]:
        yield mark_safe('<del>{}</del>'.format(conditional_escape(line)))


def dump_insert(a, b, loa, lob, hia, hib):
    for line in b[lob:hib]:
        yield mark_safe('<ins>{}</ins>'.format(conditional_escape(line)))


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
