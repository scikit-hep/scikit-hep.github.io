---
layout: page
title: Style
permalink: /developer/style
nav_order: 5
parent: Developer information
---

# Style Guide

## Pre-commit

Scikit-HEP uses [pre-commit][] to check code style. It can be installed through
`brew` (macOS) or `pip` (anywhere). There are two modes to use it locally; you
can check manually with `pre-commit run` (changes only) or `pre-commit run
--all-files` (all). You can also run `pre-commit install` to add checks as a
git precommit hook (which is where it gets its name). It's worth trying, even
if you've tried and failed to set up a custom precommit hook before; it's quite
elegant and does not add or commit the changes, it just makes the changes and
allows you to check and add them. You can always override the hook with `-n`.

[pre-commit]: https://pre-commit.com

Here is a minimal `.pre-commit-config.yaml` file:

```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v2.5.0
  hooks:
  - id: check-added-large-files
  - id: mixed-line-ending
  - id: trailing-whitespace
  - id: check-merge-conflict
  - id: check-case-conflict
  - id: check-symlinks
  - id: check-yaml
```

## Black

[Black](https://black.readthedocs.io/en/latest/) is a popular auto-formatter
from the Python Software Foundation. One of the main features of Black is that
is "opinionated"; that is, it is almost completely unconfigurable. Instead of
allowing you to come up with your own format, it enforces one on you. While I
am quite sure you can come up with a better format, having a single standard
makes it possible to learn to read code very fast - you can immediately see
nested lists, matching brackets, etc. There also is a faction of developers
that dislikes all auto-formatting tools, but inside a system like pre-commit,
auto-formatters are ideal. They also speed up the writing of code because you
can ignore formatting your code when you write it. By imposing a standard,
all Scikit-HEP developers can quickly read any package's code.

Also, properly formatted code has other benefits, such as if two developers
make the same change, they get the same formatting, and merge requests are
easier.

There are a *few* options, mostly to enable/disable certain files and to change
the line length, and those go in your pyproject.toml file.

Here is the snippet to add Black to your pre-commit config:

```yaml
- repo: https://github.com/psf/black
  rev: 19.10b0
  hooks:
  - id: black
```

And you can add a Black badge to your repo as well if you want.

```md
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

```rst
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
```

## Check-Manifest

[Check-manifest](https://pypi.org/project/check-manifest/) is a fantastic,
highly recommended tool that verifies you have working SDists. You can install
it from PyPI. Run it on your repository and see what it says. If you want to ignore
files (like test folders, example folders, docs, etc) you can add these into your config
files, either pyproject.toml or setup.cfg:

```
# pyproject.toml
[tool.check-manifest]
ignore = [".travis.yml"]

# setup.cfg or tox.ini
[check-manifest]
ignore =
    .travis.yml    
```


Add the following to your pre-commit config:

```yaml
- repo: https://github.com/mgedmin/check-manifest
  rev: "0.39"
  hooks:
  - id: check-manifest
```

## Clang-format (C++ only)

If you have C++ code, you should have a .clang-format file and use the following pre-commit config:

```yaml
- repo: local
  hooks:
  - id: docker-clang-format
    name: Docker Clang Format
    language: docker_image
    types:
    - c++
    entry: unibeautify/clang-format:latest
    args:
    - -style=file
    - -i
```

You can make a similar non-docker file, but that should sit beside the docker
one for use on CI. You can install this non-docker file locally if you want it
and have clang already installed. Note that formatting changes between versions,
so only the above recipe is guaranteed to work identically to CI.
