from collections.abc import Iterable

import discord


def sanitise(
    string: str, *, limit: int = 2000, escape: bool = True, tag_escape=True
) -> str:
    """Sanitise string.

    Args:
        string: A text string to sanitise.
        limit: How many characters should be processed.
        escape: Whether to escape characters (to prevent unwanted markdown).

    Returns:
        Sanitised string.
    """
    if escape:
        string = discord.utils.escape_markdown(string)

    if tag_escape:
        return string.replace("@", "@\u200b")[:limit]
    else:
        return string[:limit]


def split(string: str, limit: int = 1990) -> list[str]:
    """Split text into multiple smaller ones.

    :param string: A text string to split.
    :param limit: How long the output strings should be.
    :return: A string split into a list of smaller lines with maximal length of
        ``limit``.
    """
    return [string[0 + i : limit + i] for i in range(0, len(string), limit)]


def split_lines(lines: list[str], limit: int = 1990) -> list[str]:
    """Split list of lines to bigger blocks.

    :param lines: List of lines to split.
    :param limit: How long the output strings should be.
    :return: A list of strings constructed from ``lines``.

    This works just as :meth:`split()` does; the only difference is that
    this guarantees that the line won't be split at half, instead of calling
    the :meth:`split()` on ``lines`` joined with newline character.
    """
    pages: list[str] = []
    page: str = ""

    for line in lines:
        if len(page) >= limit:
            pages.append(page.strip("\n"))
            page = ""
        page += line + "\n"
    pages.append(page.strip("\n"))
    return pages


def parse_bool(string: str) -> bool | None:
    """Parse string into a boolean.

    :param string: Text to be parsed.
    :return: Boolean result of the conversion.

    Pass strings ``1``, ``true``, ``yes`` for ``True``.

    Pass strings ``0``, ``false``, ``no`` for ``False``.

    Other keywords return ``None``.
    """
    if string.lower() in ("1", "true", "yes"):
        return True
    if string.lower() in ("0", "false", "no"):
        return False
    return None


def create_table(
    iterable: Iterable[object],
    header: dict[str, str],
    *,
    limit: int = 1990,
    rich: bool = True,
) -> list[str]:
    """Create table from any iterable.

    This is useful mainly for '<command> list' situations.

    Args:
        iterable: Any iterable of items to create the table from.
        header: Dictionary of item attributes and their translations.
        limit: Character limit, at which the table is split.
        rich:
            Color rows.
            Defaults to ``False`` until Discord properly supports ANSI
            escape codes on Android.
    """
    matrix: list[list[str]] = []
    pages: list[str] = []

    # Compute column widths, make sure all fields have non-None values
    matrix.append(list(header.values()))
    column_widths: list[int] = [len(v) for v in header.values()]
    for item in iterable:
        line: list[str] = []
        for i, attr in enumerate(header.keys()):
            line.append(str(getattr(item, attr, "")))

            item_width: int = len(line[i])
            if column_widths[i] < item_width:
                column_widths[i] = item_width

        matrix.append(line)

    P: str = ""
    H: str = ""
    A: str = ""
    R: str = ""
    if rich:
        P = "ansi\n"
        H = "\u001b[1;34m"  # bold blue
        A = "\u001b[36m"  # cyan
        R = "\u001b[0m"  # reset

    page: str = P
    for i, matrix_line in enumerate(matrix):
        mline: str = ""

        # Color heading & odd lines
        if i == 0:
            mline += H
        elif i % 2 == 0:
            mline += A

        # Add values
        for column_no, column_width in enumerate(column_widths):
            mline += matrix_line[column_no].ljust(column_width + 2)

        # End line
        mline = mline.rstrip()
        if i % 2 == 0:
            mline += R + "\n"
        else:
            mline += "\n"

        # Add line
        if len(page) + len(mline) > limit:
            pages.append(page)
            page = P
        page += mline

    # Add final non-complete page
    pages.append(page)

    return pages
