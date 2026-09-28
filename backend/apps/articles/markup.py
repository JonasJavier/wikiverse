"""Pure Markdown helpers for the wiki markup dialect.

Deliberately free of Django imports: these functions are used by the model
layer, by the seed corpus validator and by ``manage.py`` repair commands, and
they are unit-tested in isolation.

The dialect is CommonMark plus two wiki extensions:

* ``[[Target Title]]`` / ``[[Target Title|display text]]`` internal links,
  optionally with an ``#anchor`` on the target.
* ``[^refkey]`` footnote markers, resolved against ``Reference.key`` rows.

Both are ignored inside fenced code blocks and inside inline code spans, and
both honour backslash escaping (``\\[[not a link]]``).

Known, deliberate limitation: four-space indented code blocks are *not*
treated as code, because indentation is ambiguous with nested list content and
the corpus uses fences everywhere.
"""

from __future__ import annotations

import re

__all__ = [
    "count_footnotes",
    "count_words",
    "extract_footnotes",
    "extract_wikilinks",
    "mask_code",
    "strip_markup",
]

#: Characters that a backslash may escape in Markdown.
ESCAPABLE = "\\`*_{}[]()#+-.!>|~^"

#: Markup characters protected inside an inline code span. The delimiting
#: backticks are deliberately absent so they are still stripped.
_CODE_PROTECTED = "*_{}[]()#+-.!>|~^"

#: Private-use code points used to hide escaped punctuation from the other
#: passes. Markdown text never contains these.
_ESCAPE_BASE = 0xE000

MAX_TARGET_LENGTH = 200
MAX_DISPLAY_LENGTH = 200
MAX_KEY_LENGTH = 60

_FENCE_OPEN_RE = re.compile(r"^(?P<indent>[ \t]{0,3})(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)$")

_WIKILINK_RE = re.compile(
    rf"(?<!\\)\[\["
    rf"(?P<target>[^\[\]|\n]{{1,{MAX_TARGET_LENGTH}}}?)"
    rf"(?:\|(?P<display>[^\[\]\n]{{0,{MAX_DISPLAY_LENGTH}}}?))?"
    rf"\]\]"
)

_FOOTNOTE_RE = re.compile(
    rf"(?<!\\)\[\^(?P<key>[A-Za-z0-9][A-Za-z0-9_.:-]{{0,{MAX_KEY_LENGTH}}})\]"
)

_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_HTML_TAG_RE = re.compile(r"</?[A-Za-z][^<>\n]{0,300}?>")
_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]\n]*)\]\([^)\n]*\)")
_INLINE_LINK_RE = re.compile(r"\[(?P<text>[^\]\n]*)\]\([^)\n]*\)")
_REF_LINK_RE = re.compile(r"\[(?P<text>[^\]\n]*)\]\[[^\]\n]*\]")
_LINK_DEF_RE = re.compile(r"^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*\S+[^\n]*$", re.M)
_HEADING_RE = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]*", re.M)
_SETEXT_RE = re.compile(r"^[ \t]{0,3}(=+|-{2,})[ \t]*$", re.M)
_QUOTE_RE = re.compile(r"^[ \t]{0,3}>[ \t]?", re.M)
_BULLET_RE = re.compile(r"^[ \t]*(?:[-*+]|\d{1,9}[.)])[ \t]+", re.M)
_RULE_RE = re.compile(r"^[ \t]{0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$", re.M)
_TABLE_DIVIDER_RE = re.compile(r"^[ \t]{0,3}\|?[ \t:|-]*\|[ \t:|-]*$", re.M)
_BACKTICK_RE = re.compile(r"`+")
_STAR_RE = re.compile(r"(?<!\s)\*+|\*+(?!\s)")
_TILDE_RE = re.compile(r"~~+")
_UNDERSCORE_RE = re.compile(r"(?<![0-9A-Za-z])_+|_+(?![0-9A-Za-z])")
_BLANK_LINES_RE = re.compile(r"\n{3,}")
_TRAILING_SPACE_RE = re.compile(r"[ \t]+$", re.M)
_SPACE_RUN_RE = re.compile(r"[ \t]{2,}")


# --------------------------------------------------------------------------- #
# Escapes
# --------------------------------------------------------------------------- #
def _hide_escapes(text: str) -> str:
    """Replace ``\\x`` with a private-use placeholder for ``x``."""
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char == "\\" and index + 1 < length and text[index + 1] in ESCAPABLE:
            out.append(chr(_ESCAPE_BASE + ord(text[index + 1])))
            index += 2
            continue
        out.append(char)
        index += 1
    return "".join(out)


def _reveal_escapes(text: str) -> str:
    """Undo :func:`_hide_escapes`."""
    if not text:
        return text
    return "".join(
        chr(ord(char) - _ESCAPE_BASE) if _ESCAPE_BASE <= ord(char) < _ESCAPE_BASE + 0x80 else char
        for char in text
    )


# --------------------------------------------------------------------------- #
# Code spans
# --------------------------------------------------------------------------- #
def _fence_spans(text: str) -> list[tuple[int, int]]:
    """Return ``(start, end)`` offsets of every fenced code block."""
    spans: list[tuple[int, int]] = []
    offset = 0
    open_at: int | None = None
    fence_char = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if open_at is None:
            match = _FENCE_OPEN_RE.match(stripped)
            if match:
                open_at = offset
                fence_char = match.group("fence")[0]
                fence_length = len(match.group("fence"))
        else:
            closer = stripped.strip()
            if (
                closer
                and closer[0] == fence_char
                and set(closer) == {fence_char}
                and len(closer) >= fence_length
            ):
                spans.append((open_at, offset + len(line)))
                open_at = None
        offset += len(line)
    if open_at is not None:
        # An unterminated fence runs to the end of the document.
        spans.append((open_at, len(text)))
    return spans


def _inline_code_spans(text: str, skip: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return ``(start, end)`` offsets of inline code spans outside ``skip``."""
    spans: list[tuple[int, int]] = []
    blocked = _Blocked(skip)
    index = 0
    length = len(text)
    while index < length:
        if blocked.contains(index):
            index = blocked.end_of(index)
            continue
        if text[index] != "`":
            index += 1
            continue
        run = _BACKTICK_RE.match(text, index)
        assert run is not None  # text[index] == "`"
        ticks = run.end() - run.start()
        cursor = run.end()
        closed = False
        while cursor < length:
            if text[cursor] != "`":
                cursor += 1
                continue
            closing = _BACKTICK_RE.match(text, cursor)
            assert closing is not None
            if closing.end() - closing.start() == ticks:
                spans.append((index, closing.end()))
                index = closing.end()
                closed = True
                break
            cursor = closing.end()
        if not closed:
            # An unmatched backtick run is literal text, not a code span.
            index = run.end()
    return spans


class _Blocked:
    """Membership test over a sorted list of non-overlapping spans."""

    def __init__(self, spans: list[tuple[int, int]]) -> None:
        self._spans = sorted(spans)

    def contains(self, index: int) -> bool:
        return any(start <= index < end for start, end in self._spans)

    def end_of(self, index: int) -> int:
        for start, end in self._spans:
            if start <= index < end:
                return end
        return index + 1


def _blank(text: str, spans: list[tuple[int, int]]) -> str:
    """Replace every character inside ``spans`` with a space, keeping newlines.

    Offsets are preserved so that positions computed on the masked string are
    valid in the original.
    """
    if not spans:
        return text
    chars = list(text)
    for start, end in spans:
        for index in range(max(0, start), min(len(chars), end)):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def mask_code(markdown: str) -> str:
    """Return ``markdown`` with fenced blocks and inline code blanked out.

    Length and line structure are preserved, so anything extracted from the
    result maps back onto the original offsets.
    """
    text = markdown or ""
    fences = _fence_spans(text)
    spans = fences + _inline_code_spans(text, fences)
    return _blank(text, spans)


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #
def extract_wikilinks(markdown: str) -> list[tuple[str, str]]:
    """Return ``[(target_title, display)]`` for every ``[[wikilink]]``.

    Order of appearance is preserved and duplicates are kept, so callers can
    count occurrences. ``[[A#Section]]`` yields the target ``A`` and the
    display ``A#Section`` (MediaWiki behaviour); ``[[A|B]]`` yields ``("A",
    "B")``. Links inside code, and links escaped with a backslash, are ignored.
    """
    text = mask_code(_hide_escapes(markdown or ""))
    links: list[tuple[str, str]] = []
    for match in _WIKILINK_RE.finditer(text):
        raw_target = _reveal_escapes(match.group("target") or "")
        raw_display = match.group("display")
        target = " ".join(raw_target.split())
        if not target:
            continue
        anchor_free = target.split("#", 1)[0].strip()
        if not anchor_free:
            continue
        if raw_display is None:
            display = target
        else:
            display = " ".join(_reveal_escapes(raw_display).split()) or anchor_free
        links.append((anchor_free, display))
    return links


def extract_footnotes(markdown: str) -> list[str]:
    """Return footnote keys in first-appearance order, deduplicated.

    Footnote *definitions* (``[^key]: text`` at the start of a line) are not
    citations and are ignored; the corpus never hand-writes them because the
    citation list is rendered from :class:`~apps.articles.models.Reference`.
    """
    return list(count_footnotes(markdown))


def count_footnotes(markdown: str) -> dict[str, int]:
    """Return ``{key: number of in-text markers}`` in first-appearance order."""
    text = mask_code(_hide_escapes(markdown or ""))
    counts: dict[str, int] = {}
    for match in _FOOTNOTE_RE.finditer(text):
        if _is_definition(text, match):
            continue
        key = match.group("key")
        counts[key] = counts.get(key, 0) + 1
    return counts


def _is_definition(text: str, match: re.Match[str]) -> bool:
    """True when the marker is a ``[^key]: …`` definition rather than a use."""
    if text[match.end() : match.end() + 1] != ":":
        return False
    line_start = text.rfind("\n", 0, match.start()) + 1
    return text[line_start : match.start()].strip() == ""


# --------------------------------------------------------------------------- #
# Plain text
# --------------------------------------------------------------------------- #
def strip_markup(markdown: str) -> str:
    """Return ``markdown`` as readable plain text.

    Used for ``word_count``, for the SQLite search fallback and for meta
    descriptions. Fenced code blocks are dropped entirely (they are not prose);
    inline code keeps its content. Link and wikilink *display* text survives,
    URLs and footnote markers do not.
    """
    text = (markdown or "").replace("\r\n", "\n").replace("\r", "\n")
    text = _hide_escapes(text)

    # Fenced code blocks are not prose: remove them outright.
    for start, end in reversed(_fence_spans(text)):
        text = text[:start] + text[end:]

    # Inline code keeps its literal content, so hide the markup characters in
    # it from the passes below instead of letting them be interpreted.
    text = _protect_inline_code(text)

    text = _HTML_COMMENT_RE.sub("", text)
    text = _LINK_DEF_RE.sub("", text)

    text = _WIKILINK_RE.sub(_wikilink_text, text)
    text = _IMAGE_RE.sub(lambda m: m.group("alt"), text)
    text = _INLINE_LINK_RE.sub(lambda m: m.group("text"), text)
    text = _REF_LINK_RE.sub(lambda m: m.group("text"), text)
    text = _FOOTNOTE_RE.sub("", text)
    text = _HTML_TAG_RE.sub("", text)

    text = _RULE_RE.sub("", text)
    text = _TABLE_DIVIDER_RE.sub("", text)
    text = _HEADING_RE.sub("", text)
    text = _SETEXT_RE.sub("", text)
    text = _QUOTE_RE.sub("", text)
    text = _BULLET_RE.sub("", text)

    text = _BACKTICK_RE.sub("", text)
    text = _STAR_RE.sub("", text)
    text = _TILDE_RE.sub("", text)
    text = _UNDERSCORE_RE.sub("", text)
    text = text.replace("|", " ")

    text = _reveal_escapes(text)
    text = _TRAILING_SPACE_RE.sub("", text)
    text = _SPACE_RUN_RE.sub(" ", text)
    text = _BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()


def _protect_inline_code(text: str) -> str:
    """Hide markup characters inside inline code spans behind placeholders."""
    spans = _inline_code_spans(text, [])
    if not spans:
        return text
    pieces: list[str] = []
    cursor = 0
    for start, end in spans:
        pieces.append(text[cursor:start])
        pieces.append(
            "".join(
                chr(_ESCAPE_BASE + ord(char)) if char in _CODE_PROTECTED else char
                for char in text[start:end]
            )
        )
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces)


def _wikilink_text(match: re.Match[str]) -> str:
    display = match.group("display")
    if display is not None and display.strip():
        return display
    target = match.group("target") or ""
    return target.split("#", 1)[0]


def count_words(markdown: str) -> int:
    """Number of prose words in ``markdown``, markup excluded."""
    return len(strip_markup(markdown).split())
