---
layout: page
title: Style
permalink: /developer/style
nav_order: 6
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

Here is a minimal `.pre-commit-config.yaml` file with some handy options:

```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.1.0
  hooks:
  - id: check-added-large-files
  - id: check-case-conflict
  - id: check-merge-conflict
  - id: check-symlinks
  - id: check-yaml
  - id: debug-statements
  - id: end-of-file-fixer
  - id: mixed-line-ending
  - id: requirements-txt-fixer
  - id: trailing-whitespace
```

For a Python 2+3 codebase, the following is also useful:

```yaml
  - id: fix-encoding-pragma
```

**Helpful tip**: Pre-commit runs top-to-bottom, so put checks that modify content
(like the several of the pre-commit-hooks above, or Black) above
checks that might be more likely to pass after the modification (like flake8).

**Keeping pinned versions fresh**: You can use `pre-commit autoupdate` to move your
tagged versions forward to the latest tags!

## Black

[Black](https://black.readthedocs.io/en/latest/) is a popular auto-formatter
from the Python Software Foundation. One of the main features of Black is that
it is "opinionated"; that is, it is almost completely unconfigurable. Instead of
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
easier. The style choices in Black were explicitly made to optimize git diffs!

There are a *few* options, mostly to enable/disable certain files and to change
the line length, and those go in your `pyproject.toml` file.

Here is the snippet to add Black to your `.pre-commit-config.yml`:

```yaml
- repo: https://github.com/psf/black
  rev: 19.10b0
  hooks:
  - id: black
```

You can add a Black badge to your repo as well if you want.

```md
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

```rst
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
```

In *very* specific situations, you may want to retain special formatting. After
carefully deciding that it is a special use case, you can use `# fmt: on` and
`#fmt: off` around a code block to have it keep custom formatting. *Always*
consider refactoring before you try this option! Most of the time, you can find
a way to make the Blacked code look better by rewriting your code; factor out
long unreadable portions into a variable, avoid writing matrices as 1D lists,
etc.

## Check-Manifest

[Check-manifest](https://pypi.org/project/check-manifest/) is a fantastic,
highly recommended tool that verifies you have working SDists. You can install
it from PyPI. Run it on your repository and see what it says. If you want to ignore
files (like test folders, example folders, docs, etc) you can add these into your config
files, either `pyproject.toml` or `setup.cfg`:

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
  rev: "0.42"
  hooks:
  - id: check-manifest
```

**Warning**: For a complex package, this may be slow. You can optionally set
`stages: [manual]` just below the id, and then only run this explicitly
(probably in CI only).  In GHA, you would add, placed just below the normal
check:

```yaml
    - name: Check manifest
      uses: pre-commit/action@v2.0.0
      with:
        extra_args: --hook-stage manual check-manifest
```

## Type checking (new)

One of the most exciting advancements in Python in the last 10 years has been
static type hints. Scikit-HEP is just beginning to make sure packages are
type-hint ready.  One of the challenges for providing static type hints is that
it was developed in the Python 3 era and it really shines in a Python 3.7+
codebase (due to `from __future__ import annotations`, which turns annotations
into strings and allows you to use future Python features in Python 3.7+
annotations as long as your type checker supports them). For now, it is
recommended that you make an attempt to support type checking through your
public API in the best way that you can (based on your supported Python
versions). Stub files or type comments allow Python 2 or Python 3.5 to be
supported.  [MyPy](https://mypy.readthedocs.io/en/stable/) is suggested for
type checking, though there are several other good options to try, as well. If
you have built-in support for type checking, you need to add empty `py.typed`
files to all packages/subpackages to indicate that you support it.

The MyPy addition for pre-commit:

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v0.782
  hooks:
  - id: mypy
    files: src
```

You can also add items to the virtual environment setup for mypy by pre-commit, for example:

```yaml
    additional_dependencies: [attrs==19.3.0]
```

MyPy has a config section in `setup.cfg` that looks like this:


```ini
[mypy]
files = src
pretty = True
python_version = 3.6
warn_unused_configs = True
warn_unused_ignores = True

[mypy-numpy]
ignore_missing_imports = True
```

There are a lot of options, and you can start with only typing global code and
functions with at least one type annotation (the default) and enable more
checks as you go. You can ignore missing imports on libraries as shown above,
on section each. And you can disable MyPy on a line with `# type: ignore`. Once
you are ready to start checking more, you can look at adding
`check_untyped_defs`, `disallow_untyped_defs`, `disallow_incomplete_defs`, and
more, up until `strict`. You can add these *per file* by adding a `# mypy:
strict` (or any other less stringent check) at the top of the file.


## Flake8

[Flake8][] can check a collection of good practices for you, ranging from
simple style to things that might confuse or detract users, such as unused
imports, named values that are never used, mutable default arguments, and more.
Unlike black and some other tools, flake8 does not correct problems, it just
reports them. Some of the checks could have had automated fixes, sadly (which
is why Black is nice).  Here is a suggested `setup.cfg` to enable compatibility
with Black:

```ini
[flake8]
ignore = E203, E231, E501, W503
select = C,E,F,W
```

One recommended plugin for flake8 is `flake8-bugbear`, which catches many
common bugs.  It is highly opinionated and can be made more so with the `B9`
setting. You can also set a max complexity, which bugs you when you have
complex functions that should be broken up. Here is an opinionated config:

```ini
[flake8]
max-complexity = 12
ignore = E203, E231, E501, E722, W503
select = C,E,F,W,B,B9
```

(Error E722 is identical to B001.) Here is the flake8 addition for pre-commit, with the `bugbear` plugin:

```yaml
- repo: https://gitlab.com/pycqa/flake8
  rev: 3.8.3
  hooks:
  - id: flake8
    additional_dependencies: [flake8-bugbear]
```

This *will* be too much at first, so you can disable or enable any test by it's
label. You can also disable a check or a list of checks inline with
`# noqa: X###` (where you list the check label(s)). Over time, you can fix
and enable more checks. A few interesting plugins:

* [`flake8-bugbear`](https://pypi.org/project/flake8-bugbear/): Fantastic checker that catches common situations that tend to create bugs.
* [`flake8-docstrings`](https://pypi.org/project/flake8-docstrings/): Docstring checker.
* [`flake8-spellcheck`](https://pypi.org/project/flake8-spellcheck/): Spelling checker.
* [`flake8-import-order`](https://pypi.org/project/flake8-import-order/): Enforces PEP8 grouped imports (which are quite nice).
* [`pep8-naming`](https://pypi.org/project/pep8-naming/): Enforces PEP8 naming rules


## Python warnings

Python hides important warnings by default, mostly because it's trying to be
nice to users. You are a developer, you don't want it to be "nice". You want to
find and fix warnings before they cause user errors! Always either run
Python/PyTest with `-Wd`, or set `export PYTHONWARNINGS=d` in your environment.
You can also add the following to your `setup.cfg` file:

```ini
[tool:pytest]
addopts = -Wd
```

## Clang-format (C++ only)

If you have C++ code, you should have a `.clang-format` file and use the
following pre-commit config:

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
so only the above recipe is guaranteed to work identically to CI. The local one
would look like this:

```yaml
- repo: local
  hooks:
  - id: clang-format
    name: Clang Format
    language: system
    types:
    - c++
    entry: clang-format
    args:
    - -style=file
    - -i
```

[Flake8]: https://gitlab.com/pycqa/flake8
