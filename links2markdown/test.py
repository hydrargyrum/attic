#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

from unittest.mock import patch

import pytest

import links2markdown


@pytest.mark.parametrize(
    "input,expected",
    [
        ("foo bar", "foo bar"),
        ("foo https://example.com", "foo [first title](https://example.com)"),
        ("foo [bar](https://example.com)", "foo [bar](https://example.com)"),
        ("foo <https://example.com>", "foo <https://example.com>"),
        ("[foo]: https://example.com", "[foo]: https://example.com"),
    ]
)
@patch.object(links2markdown, "fetch_metadata")
def test_basic(fetch_mock, input, expected):
    fetch_mock.side_effect = [
        links2markdown.Metadata("first title"),
        links2markdown.Metadata("2nd title"),
    ]
    got = links2markdown.LINK_RE.sub(links2markdown.link_to_markdown, input)
    assert got == expected


@patch.object(links2markdown, "fetch_metadata")
def test_img(fetch_mock):
    fetch_mock.side_effect = [
        links2markdown.Metadata("first title", "https://example.com/img"),
        links2markdown.Metadata("2nd title"),
    ]
    got = links2markdown.LINK_RE.sub(
        lambda m: links2markdown.link_to_markdown(m, True),
        "foo https://example.org"
    )
    assert got == "foo [![first title](https://example.com/img) first title](https://example.org)"


@patch.object(links2markdown, "fetch_metadata")
def test_no_title(fetch_mock):
    input = "foo https://example.com"
    expected = "foo <https://example.com>"
    fetch_mock.return_value = None
    got = links2markdown.LINK_RE.sub(links2markdown.link_to_markdown, input)
    assert got == expected
