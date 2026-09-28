"""Two-stage, word-level revision diffing.

Deliberately free of Django imports — not even ``django.db`` typing — so the
engine is unit-testable with plain pytest (no database, no settings) and can
carry the 100 % coverage gate that ``pyproject.toml`` puts on this one file.
The view layer (``GET /api/articles/{slug}/diff/?from=&to=``) wraps the payload
below with the article stub, the two revision headers and ``prev_id`` /
``next_id``; none of that belongs here.

Why two stages
--------------
A naive ``SequenceMatcher`` over the whole document's *word* tokens is not
viable: ``difflib`` is not Myers, it degrades toward quadratic on prose, and the
infrastructure survey measured a 15 KB body (the normal case for this corpus) at
~300 ms and a 120 KB body at ~43 s. Diffing *lines* first and then word-diffing
only the lines that actually changed measured 0.9 ms and 77 ms for the same two
bodies — 300× to 560× faster — because the line list is short (~70–400 lines
for a 5–20 KB article) and each word diff runs over one line's worth of tokens
instead of the whole body's. ``autojunk`` is off everywhere: with word tokens it
would class every space and every occurrence of "the" as junk and silently
produce chunkier, wrong-looking diffs. An explicit ``isjunk`` predicate does
the bounded, lossless part of that job instead — see ``_is_blank``, which is
what keeps the worst realistic case in milliseconds.

Payload shape
-------------
``diff_revisions()`` returns a plain JSON-serialisable ``dict``::

    {
      "created": False,          # old side was the empty document (page creation)
      "truncated": False,        # a safety valve fired; see "Truncation" below
      "stats": {
        "lines_added": 3,        # lines present only on the new side
        "lines_removed": 1,      # lines present only on the old side
        "lines_changed": 2,      # lines paired old<->new by the line diff
        "bytes_added": 112,      # UTF-8 bytes of every added or changed new line
        "bytes_removed": 47      # UTF-8 bytes of every removed or changed old line
      },
      "hunks": [
        {
          "a_start": 48,         # 1-based first old line in the hunk
          "a_lines": 3,          # rows in this hunk that exist on the old side
          "b_start": 48,         # 1-based first new line in the hunk
          "b_lines": 3,          # rows in this hunk that exist on the new side
          "rows": [
            {"t": "=", "a": 48, "b": 48, "ops": [["=", "## History"]]},
            {"t": "~", "a": 49, "b": 49, "ops": [
                ["=", "PostgreSQL began as the "],
                ["-", "POSTGRES"],
                ["+", "**POSTGRES**"],
                ["=", " project at Berkeley in "],
                ["-", "1986"],
                ["+", "1986, led by Michael Stonebraker"],
                ["=", "."]
            ]},
            {"t": "+", "a": None, "b": 50, "ops": [["+", "It was renamed in 1996."]]},
            {"t": "-", "a": 51, "b": None, "ops": [["-", "Obsolete sentence."]]}
          ]
        }
      ]
    }

Contract, all of it load-bearing for the renderer:

* ``hunks`` is ordered by position in the document and only covers changed
  regions plus ``context`` (default 3) unchanged lines either side. Everything
  between two hunks is unchanged; the UI collapses it ("42 unchanged lines")
  from ``next.a_start - (prev.a_start + prev.a_lines)``.
* ``rows[].t`` is ``"="`` (context), ``"~"`` (modified, carries word-level ops),
  ``"+"`` (line added) or ``"-"`` (line removed).
* ``rows[].a`` / ``rows[].b`` are **1-based** line numbers in the old / new
  document, and ``None`` where the line does not exist on that side.
* ``ops`` is a list of ``[kind, text]`` pairs with ``kind`` in ``"="``, ``"+"``,
  ``"-"``. **Round-trip invariant:** joining the ``"="`` and ``"-"`` texts of a
  row reproduces the old line exactly, and joining its ``"="`` and ``"+"`` texts
  reproduces the new line exactly. That is what lets one payload render a
  side-by-side view, an inline view or either side alone.
* ``ops`` never contains an empty string, so a blank line is ``"ops": []`` —
  joining nothing still satisfies the invariant.
* ``a_start`` is the 1-based number of the hunk's first old line; when the hunk
  adds lines without consuming any (a pure insertion), it is the number of the
  old line the insertion sits before and ``a_lines`` is ``0``. ``b_start`` /
  ``b_lines`` mirror that on the new side.
* ``created`` is ``True`` when the old side is empty and the new side is not —
  the ``from=0`` case that Recent changes uses for page creation. The hunks are
  still complete (one hunk, every row a ``"+"``), so a client may render either
  "page created" or the full listing.

Line handling
-------------
``\\r\\n`` and bare ``\\r`` are folded to ``\\n`` before anything else, so an
edit saved from a Windows editor does not read as a whole-file rewrite. One
trailing newline is dropped (``"a\\nb\\n"`` is two lines, ``"a\\nb\\n\\n"`` is
three, the last one empty); ``str.splitlines`` is deliberately *not* used
because it also breaks on ``\\x0b``, ``\\x0c`` and ``\\u2028``, which would make
the diff disagree with every editor's idea of a line.

Tokenisation is ``\\w+|\\s+|[^\\w\\s]``: whitespace is its own token, so
re-rendering is lossless and accented text does not explode into one token per
byte. Known limitation: ``\\w+`` treats an unspaced CJK run as a single token,
so word-level highlighting inside CJK prose degrades to whole-run highlighting.

Truncation
----------
Bodies in this corpus are 5–20 KB, but nothing stops a client POSTing 2.5 MB of
single-character lines, so five independent valves bound the work. Any of them
firing sets ``truncated: True`` and nothing else about the payload's shape
changes:

===================  ==================================================
``max_chars``        per side, cut the text (may cut mid-line)
``max_lines``        per side, drop the tail of the line list
``max_rows``         stop emitting rows, keep the hunks already built
``max_ops``          stop emitting rows once the payload is large enough
``max_row_tokens``   one changed line pair over the token budget falls
                     back to whole-line ``[["-", old], ["+", new]]`` ops
===================  ==================================================

``stats`` is computed from the full line-level opcode stream, so it stays
accurate even when ``max_rows`` or ``max_ops`` cuts the rendered hunks short.

Measured on this machine at the default settings, against a 20 KB / 73-line
Markdown fixture shaped like the corpus (one paragraph per line): three edited
paragraphs, 8 ms and a 6.1 KB payload; the same body fully rewritten, 4 ms and
34 KB; created from empty, 0.1 ms and 23 KB; reflowed to one word per line,
2.4 ms and 146 KB; every word changed, 2.2 ms and 43 KB. The deliberately
hostile shapes — a 200 KB single line, 200 000 single-character lines, a 200 KB
body with every word changed, 2 500 blank-heavy lines — all land under 25 ms and
under 425 KB, and the first three report ``truncated``.

``PAYLOAD_VERSION`` participates in the view's Redis key (``diff:v1:{from}:{to}``,
cached forever because revisions are immutable). Bump it whenever the shape
above changes.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Final

__all__ = [
    "CONTEXT_LINES",
    "MAX_DOC_CHARS",
    "MAX_LINES",
    "MAX_ROWS",
    "MAX_ROW_TOKENS",
    "PAYLOAD_VERSION",
    "diff_revisions",
    "normalise_newlines",
    "split_lines",
    "tokenise",
    "word_ops",
]

#: Bump when the payload shape changes; the view's cache key embeds it.
PAYLOAD_VERSION: Final = 1

#: Unchanged lines kept either side of a change, MediaWiki/GitHub style.
CONTEXT_LINES: Final = 3

#: Per-side character ceiling. ~13× the largest body the corpus produces.
MAX_DOC_CHARS: Final = 200_000

#: Per-side line ceiling. ~6× the line count of the longest feature article.
MAX_LINES: Final = 2_500

#: Ceiling on rendered rows across all hunks.
MAX_ROWS: Final = 4_000

#: Ceiling on rendered ops across all rows. Bounds the serialised payload at
#: roughly 500 KB whatever the input does; a realistic full rewrite of a 20 KB
#: article emits ~650.
MAX_OPS: Final = 20_000

#: Combined old+new token ceiling for one word-diffed line pair. The valve
#: against an article written as a single unwrapped line.
MAX_ROW_TOKENS: Final = 4_000

#: Whitespace is its own token so re-joining a token list is lossless.
_TOKEN_RE = re.compile(r"\w+|\s+|[^\w\s]", re.UNICODE)

#: ``[kind, text]``, JSON-serialised as a two-element array.
DiffOp = list[str]
DiffRow = dict[str, object]
DiffHunk = dict[str, object]
DiffPayload = dict[str, object]
Opcode = tuple[str, int, int, int, int]


def normalise_newlines(text: str | None) -> str:
    """Fold CRLF and bare CR to LF. ``None`` and ``""`` both yield ``""``."""
    if not text:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_lines(text: str | None) -> list[str]:
    """Split into logical lines, dropping at most one trailing newline.

    The empty document is zero lines, not one empty line — that is what makes
    the page-creation diff a pure insertion.
    """
    body = normalise_newlines(text)
    if not body:
        return []
    if body.endswith("\n"):
        body = body[:-1]
    return body.split("\n")


def tokenise(text: str) -> list[str]:
    """Split a line into words, whitespace runs and single punctuation marks."""
    return _TOKEN_RE.findall(text)


def _is_blank(value: str) -> bool:
    """``isjunk`` predicate: an element too ubiquitous to anchor a match.

    This is the single most important performance decision in the module, and it
    is a correctness no-op: ``difflib`` only refuses to *start* a matching block
    on a junk element, and a block still extends over junk whenever the elements
    compare equal, so no text is ever lost or mismatched.

    Without it, every blank line (at line level) and every single space (at word
    level) is a candidate anchor, which is precisely the input shape that drives
    ``difflib``'s recursive longest-match search toward quadratic. Measured on
    this machine: a 4 000-line body with the usual Markdown blank lines takes
    **8 500 ms** to diff at line level and **351 ms** with this predicate; one
    120-word paragraph line in which every word changed takes **32.5 ms** to
    word-diff and **0.08 ms** with it, for byte-identical output on realistic
    edits. ``autojunk`` stays off — it would drop real words.
    """
    return not value.strip()


def word_ops(
    old_line: str,
    new_line: str,
    *,
    max_tokens: int = MAX_ROW_TOKENS,
) -> tuple[list[DiffOp], bool]:
    """Word-level ops for one changed line pair, plus whether the valve fired.

    Returns ``(ops, truncated)``. When the two lines together carry more than
    ``max_tokens`` tokens the pair degrades to whole-line ops rather than
    burning quadratic time on a line nobody wrapped.
    """
    old_tokens = tokenise(old_line)
    new_tokens = tokenise(new_line)
    ops: list[DiffOp] = []

    if len(old_tokens) + len(new_tokens) > max_tokens:
        _append(ops, "-", old_line)
        _append(ops, "+", new_line)
        return ops, True

    matcher = SequenceMatcher(_is_blank, old_tokens, new_tokens, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            _append(ops, "=", "".join(old_tokens[i1:i2]))
            continue
        if tag in {"replace", "delete"}:
            _append(ops, "-", "".join(old_tokens[i1:i2]))
        if tag in {"replace", "insert"}:
            _append(ops, "+", "".join(new_tokens[j1:j2]))
    return ops, False


def diff_revisions(
    old_text: str | None,
    new_text: str | None,
    *,
    context: int = CONTEXT_LINES,
    max_chars: int = MAX_DOC_CHARS,
    max_lines: int = MAX_LINES,
    max_rows: int = MAX_ROWS,
    max_ops: int = MAX_OPS,
    max_row_tokens: int = MAX_ROW_TOKENS,
) -> DiffPayload:
    """Diff two revision bodies. See the module docstring for the payload shape.

    ``old_text`` may be ``""`` or ``None`` — that is the ``from=0`` page-creation
    case and it sets ``created: True``. Identical bodies produce zero hunks. The
    keyword arguments exist so the valves can be exercised without building a
    multi-megabyte fixture; production callers pass none of them.
    """
    old_body, old_cut = _clamp_chars(normalise_newlines(old_text), max_chars)
    new_body, new_cut = _clamp_chars(normalise_newlines(new_text), max_chars)

    old_lines, old_dropped = _clamp_lines(split_lines(old_body), max_lines)
    new_lines, new_dropped = _clamp_lines(split_lines(new_body), max_lines)

    # Page creation: the old side is the empty document. difflib renders this as
    # a single `insert` opcode, which is exactly right; the flag is what lets the
    # UI say "page created" instead of "everything changed".
    created = not old_lines and bool(new_lines)

    matcher = SequenceMatcher(_is_blank, old_lines, new_lines, autojunk=False)
    # Copy: get_grouped_opcodes() mutates the list get_opcodes() caches.
    opcodes = list(matcher.get_opcodes())
    stats = _stats(old_lines, new_lines, opcodes)
    hunks, rows_cut = _build_hunks(
        matcher,
        old_lines,
        new_lines,
        context=context,
        max_rows=max_rows,
        max_ops=max_ops,
        max_row_tokens=max_row_tokens,
    )

    return {
        "created": created,
        "truncated": any((old_cut, new_cut, old_dropped, new_dropped, rows_cut)),
        "stats": stats,
        "hunks": hunks,
    }


def _append(ops: list[DiffOp], kind: str, text: str) -> None:
    """Record one op, skipping empty text so a blank line is ``ops: []``.

    ``difflib`` never emits two adjacent non-equal opcodes, so no two ops in a
    row can share a kind and there is nothing to merge.
    """
    if text:
        ops.append([kind, text])


def _one_op(kind: str, text: str) -> list[DiffOp]:
    """The op list for a whole line that is entirely added, removed or context."""
    ops: list[DiffOp] = []
    _append(ops, kind, text)
    return ops


def _row(kind: str, a_index: int | None, b_index: int | None, ops: list[DiffOp]) -> DiffRow:
    return {
        "t": kind,
        "a": None if a_index is None else a_index + 1,
        "b": None if b_index is None else b_index + 1,
        "ops": ops,
    }


def _clamp_chars(body: str, max_chars: int) -> tuple[str, bool]:
    if len(body) <= max_chars:
        return body, False
    return body[:max_chars], True


def _clamp_lines(lines: list[str], max_lines: int) -> tuple[list[str], bool]:
    if len(lines) <= max_lines:
        return lines, False
    return lines[:max_lines], True


def _byte_len(lines: list[str]) -> int:
    return sum(len(line.encode("utf-8")) for line in lines)


def _stats(
    old_lines: list[str],
    new_lines: list[str],
    opcodes: list[Opcode],
) -> dict[str, int]:
    """Document-wide counts, derived from the ungrouped line-level opcodes."""
    added = removed = changed = 0
    bytes_added = bytes_removed = 0
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        old_count = i2 - i1
        new_count = j2 - j1
        paired = min(old_count, new_count)
        changed += paired
        added += new_count - paired
        removed += old_count - paired
        bytes_removed += _byte_len(old_lines[i1:i2])
        bytes_added += _byte_len(new_lines[j1:j2])
    return {
        "lines_added": added,
        "lines_removed": removed,
        "lines_changed": changed,
        "bytes_added": bytes_added,
        "bytes_removed": bytes_removed,
    }


def _build_hunks(
    matcher: SequenceMatcher,
    old_lines: list[str],
    new_lines: list[str],
    *,
    context: int,
    max_rows: int,
    max_ops: int,
    max_row_tokens: int,
) -> tuple[list[DiffHunk], bool]:
    hunks: list[DiffHunk] = []
    truncated = False
    rows_left = max_rows
    ops_left = max_ops

    for group in matcher.get_grouped_opcodes(context):
        if rows_left <= 0 or ops_left <= 0:
            # More changes remain than the row or op budget allows.
            truncated = True
            break

        rows: list[DiffRow] = []
        for tag, i1, i2, j1, j2 in group:
            if tag == "equal":
                for offset in range(i2 - i1):
                    rows.append(
                        _row("=", i1 + offset, j1 + offset, _one_op("=", old_lines[i1 + offset]))
                    )
            elif tag == "insert":
                rows.extend(_added_rows(new_lines, j1, j2))
            elif tag == "delete":
                rows.extend(_removed_rows(old_lines, i1, i2))
            else:  # replace
                paired = min(i2 - i1, j2 - j1)
                pairs = zip(
                    old_lines[i1 : i1 + paired],
                    new_lines[j1 : j1 + paired],
                    strict=True,
                )
                for offset, (old_line, new_line) in enumerate(pairs):
                    ops, valve = word_ops(old_line, new_line, max_tokens=max_row_tokens)
                    truncated = truncated or valve
                    rows.append(_row("~", i1 + offset, j1 + offset, ops))
                rows.extend(_removed_rows(old_lines, i1 + paired, i2))
                rows.extend(_added_rows(new_lines, j1 + paired, j2))

        kept, ops_spent = _fit_budget([len(row["ops"]) for row in rows], rows_left, ops_left)
        if kept < len(rows):
            del rows[kept:]
            truncated = True
        rows_left -= kept
        ops_left -= ops_spent
        if not rows:
            # The first row alone overruns the op budget: emit nothing further
            # rather than an empty hunk.
            break

        hunks.append(
            {
                "a_start": group[0][1] + 1,
                "a_lines": sum(1 for row in rows if row["a"] is not None),
                "b_start": group[0][3] + 1,
                "b_lines": sum(1 for row in rows if row["b"] is not None),
                "rows": rows,
            }
        )

    return hunks, truncated


def _fit_budget(counts: list[int], rows_left: int, ops_left: int) -> tuple[int, int]:
    """How many leading rows fit both budgets, and how many ops they spend.

    ``counts`` is the per-row op count, in row order.
    """
    kept = 0
    spent = 0
    for count in counts:
        if kept + 1 > rows_left or spent + count > ops_left:
            break
        kept += 1
        spent += count
    return kept, spent


def _added_rows(new_lines: list[str], start: int, stop: int) -> list[DiffRow]:
    return [_row("+", None, index, _one_op("+", new_lines[index])) for index in range(start, stop)]


def _removed_rows(old_lines: list[str], start: int, stop: int) -> list[DiffRow]:
    return [_row("-", index, None, _one_op("-", old_lines[index])) for index in range(start, stop)]
