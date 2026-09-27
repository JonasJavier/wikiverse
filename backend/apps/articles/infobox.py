"""Validation for ``Article.infobox``.

The schema is deliberately tiny and closed (DECISIONS §1). Nothing validates a
``JSONField`` by itself, so this validator is attached to the model field *and*
called by the seed corpus validator, which means malformed data fails at write
time instead of at render time.

The only valid shape::

    {
      "title": str,                                  # optional
      "subtitle": str,                               # optional
      "rows": [
        {"kind": "header", "value": str},            # section break
        {"kind": "row", "label": str, "value": str},
        {"kind": "full", "value": str},              # full-width, no label
      ],
    }

Every ``value`` is a plain string. It may contain ``[[wikilinks]]``,
``*emphasis*`` and ``[^footnote]`` markers, which the renderer resolves; it is
never an object, a list or raw HTML. The infobox **never** carries an image:
the lead image lives on the ``Article.lead_image_*`` columns.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

__all__ = [
    "MAX_LABEL",
    "MAX_ROWS",
    "MAX_TEXT",
    "MAX_VALUE",
    "ROW_KINDS",
    "TOP_LEVEL_KEYS",
    "validate_infobox",
]

#: The only keys allowed at the top level. ``caption``/``image`` are not among
#: them: image metadata belongs to the Article columns.
TOP_LEVEL_KEYS = ("title", "subtitle", "rows")

ROW_KINDS = ("header", "row", "full")

#: Keys allowed per row kind. ``header`` and ``full`` carry ``value``, never
#: ``label``.
ROW_KEYS: dict[str, tuple[str, ...]] = {
    "header": ("kind", "value"),
    "row": ("kind", "label", "value"),
    "full": ("kind", "value"),
}

MAX_ROWS = 40
MAX_LABEL = 60
MAX_VALUE = 400
MAX_TEXT = 200

_IMAGE_HINT = (
    "infobox.{key} is not supported: the lead image lives on the Article "
    "columns lead_image_url / lead_image_alt / lead_image_caption / "
    "lead_image_credit / lead_image_license / lead_image_source_url."
)


def validate_infobox(value: object) -> None:
    """Raise :class:`~django.core.exceptions.ValidationError` unless ``value``
    matches the closed schema above.

    Every message names the offending path (``infobox.rows[3].label``) so the
    editor, the API error body and the corpus validator all point at the same
    place. An empty infobox (``None``, ``{}`` or ``""``) is valid and means
    "this article has no infobox".
    """
    if value is None or value == {} or value == "":
        return
    if not isinstance(value, dict):
        raise ValidationError(f"infobox must be an object, not {_type_name(value)}.")

    for key in ("image", "image_url", "caption"):
        if key in value:
            raise ValidationError(_IMAGE_HINT.format(key=key))

    unknown = sorted(set(value) - set(TOP_LEVEL_KEYS))
    if unknown:
        raise ValidationError(f"Unknown infobox keys: {unknown}. Allowed: {list(TOP_LEVEL_KEYS)}.")

    for key in ("title", "subtitle"):
        if key not in value:
            continue
        text = value[key]
        if not isinstance(text, str):
            raise ValidationError(f"infobox.{key} must be a string, not {_type_name(text)}.")
        if len(text) > MAX_TEXT:
            raise ValidationError(f"infobox.{key} exceeds {MAX_TEXT} characters.")

    rows = value.get("rows", [])
    if not isinstance(rows, list):
        raise ValidationError(f"infobox.rows must be a list, not {_type_name(rows)}.")
    if len(rows) > MAX_ROWS:
        raise ValidationError(f"infobox.rows may hold at most {MAX_ROWS} rows, got {len(rows)}.")

    for index, row in enumerate(rows):
        _validate_row(index, row)


def _validate_row(index: int, row: object) -> None:
    path = f"infobox.rows[{index}]"
    if not isinstance(row, dict):
        raise ValidationError(f"{path} must be an object, not {_type_name(row)}.")

    kind = row.get("kind", "row")
    if kind not in ROW_KINDS:
        raise ValidationError(f"{path}.kind must be one of {list(ROW_KINDS)}, got {kind!r}.")

    allowed = ROW_KEYS[kind]
    extra = sorted(set(row) - set(allowed))
    if extra:
        raise ValidationError(
            f"{path} has keys not allowed for kind={kind!r}: {extra}. Allowed: {list(allowed)}."
        )

    if "value" not in row:
        raise ValidationError(f"{path}.value is required.")
    text = row["value"]
    if not isinstance(text, str):
        raise ValidationError(f"{path}.value must be a string, not {_type_name(text)}.")
    if not text.strip():
        raise ValidationError(f"{path}.value must not be empty.")
    if len(text) > MAX_VALUE:
        raise ValidationError(f"{path}.value exceeds {MAX_VALUE} characters.")

    if kind != "row":
        return

    if "label" not in row:
        raise ValidationError(f"{path}.label is required for kind='row'.")
    label = row["label"]
    if not isinstance(label, str):
        raise ValidationError(f"{path}.label must be a string, not {_type_name(label)}.")
    if not label.strip():
        raise ValidationError(f"{path}.label must not be empty.")
    if len(label) > MAX_LABEL:
        raise ValidationError(f"{path}.label exceeds {MAX_LABEL} characters.")


def _type_name(value: object) -> str:
    return type(value).__name__
