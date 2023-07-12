#!/usr/bin/env pytest
# SPDX-License-Identifier: WTFPL

import os
from pathlib import Path
from subprocess import check_call
from shutil import copy
from uuid import uuid4

import vignette
import pytest


os.chdir(Path(__file__).parent)


@pytest.fixture()
def src_path(tmp_path):
    tmp_path.joinpath('foo').mkdir()
    copy(
        'test.png',
        str(tmp_path.joinpath('foo/1.png'))
    )
    yield tmp_path.joinpath('foo')


@pytest.fixture(params=[0, 1])
def dst_path(tmp_path, request):
    if request.param == 0:
        ret = tmp_path.joinpath('bar')
    else:
        ret = Path(f'/run/user/{os.getuid()}/test-{uuid4()}/bar')
        ret.parent.mkdir(parents=True)
    ret.mkdir()
    return ret


def test_file_file(src_path, dst_path):
    othumb = vignette.get_thumbnail(str(src_path / '1.png'), 'large')
    assert Path(othumb).exists()
    assert src_path.joinpath('1.png').exists()

    check_call([
        './mv-with-thumb',
        str(src_path / '1.png'),
        str(dst_path / '2.png'),
    ])
    assert not src_path.joinpath('1.png').exists()
    assert dst_path.joinpath('2.png').exists()

    assert not Path(othumb).exists()
    assert vignette.try_get_thumbnail(str(dst_path / '2.png'))


def test_file_dir(src_path, dst_path):
    othumb = vignette.get_thumbnail(str(src_path / '1.png'))
    assert Path(othumb).exists()
    assert src_path.joinpath('1.png').exists()

    check_call([
        './mv-with-thumb',
        str(src_path / '1.png'),
        str(dst_path),
    ])
    assert not src_path.joinpath('1.png').exists()
    assert dst_path.joinpath('1.png').exists()

    assert not Path(othumb).exists()
    assert vignette.try_get_thumbnail(str(dst_path / '1.png'))


def test_dir_name(src_path, dst_path):
    othumb = vignette.get_thumbnail(str(src_path / '1.png'))
    assert Path(othumb).exists()
    assert src_path.joinpath('1.png').exists()

    check_call([
        './mv-with-thumb',
        str(src_path),
        str(dst_path / 'quack'),
    ])
    assert not src_path.exists()
    assert dst_path.joinpath('quack').exists()
    assert dst_path.joinpath('quack/1.png').exists()

    assert not Path(othumb).exists()
    assert vignette.try_get_thumbnail(str(dst_path / 'quack/1.png'))


def test_dir_subdir(src_path, dst_path):
    othumb = vignette.get_thumbnail(str(src_path / '1.png'))

    check_call([
        './mv-with-thumb',
        str(src_path),
        str(dst_path),
    ])

    assert not Path(othumb).exists()
    assert dst_path.joinpath('foo/1.png').exists()
    assert vignette.try_get_thumbnail(str(dst_path.joinpath('foo/1.png')))
