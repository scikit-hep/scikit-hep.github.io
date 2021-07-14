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
git pre-commit hook (which is where it gets its name). It's worth trying, even
if you've tried and failed to set up a custom pre-commit hook before; it's quite
elegant and does not add or commit the changes, it just makes the changes and
allows you to check and add them. You can always override the hook with `-n`.

[pre-commit]: https://pre-commit.com

Here is a minimal `.pre-commit-config.yaml` file with some handy options:

```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.0.1
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
tagged versions forward to the latest tags! Due to the design of pre-commit's
caching system, these _must_ point at fixed tags, never put a branch here.

**Checking in CI**: You can have this checked and often automatically corrected
for you using [pre-commit.ci](https://pre-commit.ci). It will even
update your `rev:` versions every week or so if your checks update!

To use, just go to [pre-commit.ci](https://pre-commit.ci), click
"Log in with GitHub", click "Add an Installation" if adding for the first time
for an org or user, or "Manage repos on GitHub" for an existing installation
(like Scikit-HEP), then add your repository from the list in GitHub's interface.

Now there will be a new check, and pre-commit.ci will commit changes if the
pre-commit check made any changes. Note that there are a couple of missing features:
Docker based checks will not work (pre-commit.ci already runs in docker), you
cannot enable a `--manual` flag, so extra checks will not run, and jobs should not
download packages (use `additional-dependencies:` to add what you need).


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
  rev: 21.5b2
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
files (like test folders, example folders, docs, etc) you can add these into your
`pyproject.toml` file:

```toml
[tool.check-manifest]
ignore = [
    ".travis.yml",
]
```


Add the following to your pre-commit config:

```yaml
- repo: https://github.com/mgedmin/check-manifest
  rev: "0.46"
  hooks:
  - id: check-manifest
```

If you use `setuptools_scm`, you might want to add:

```yaml
    additional-dependencies: [setuptools_scm, toml]
```

<details><summary>If this is too slow: (click here)</summary>

{%- capture "mymarkdown" -%}

**Warning**: For a complex package, this may be slow. You can optionally set
`stages: [manual]` just below the id, and then only run this explicitly
(probably in CI only).  In GHA, you should enable the manual stage, which will
run all checks:

```yaml
    - uses: pre-commit/action@v2.0.3
      with:
        extra_args: --all-files --hook-stage manual
```

{%- endcapture -%}

{{ mymarkdown | markdownify }}

</details>


## Type checking

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

Read more about type checking on the [dedicated page][mypy page].

The MyPy addition for pre-commit:

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v0.901
  hooks:
  - id: mypy
    files: src
```

You can also add items to the virtual environment setup for mypy by pre-commit,
for example:

```yaml
    additional_dependencies: [attrs==21.2.0]
```

MyPy has a config section in `pyproject.toml` that looks like this:


```ini
[mypy]
files = "src"
python_version = "3.6"
warn_unused_configs = true

# Currently (0.812) identical to --strict
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
no_implicit_reexport = true
strict_equality = true

# You can disable imports or control per-module/file settings here
[[tool.mypy.overrides]]
module = [ "numpy.*", ]
ignore_missing_imports = true
```

There are a lot of options, and you can start with only typing global code and
functions with at least one type annotation (the default) and enable more
checks as you go (possibly by slowly uncommenting items in the list above).
You can ignore missing imports on libraries as shown above, one section each.
And you can disable MyPy on a line with `# type: ignore`.  One strategy would
be to enable `check_untyped_defs` first, followed by `disallow_untyped_defs`
then `disallow_incomplete_defs`.  You can add these *per file* by adding a `#
mypy: <option>` at the top of a file. You can also pass `--strict` on the
command line.

[mypy page]: {{ site.baseurl }}{% link pages/developers/mypy.md %}

## Flake8

[Flake8][] can check a collection of good practices for you, ranging from
simple style to things that might confuse or detract users, such as unused
imports, named values that are never used, mutable default arguments, and more.
Unlike black and some other tools, flake8 does not correct problems, it just
reports them. Some of the checks could have had automated fixes, sadly (which
is why Black is nice).  Here is a suggested `.flake8` or `setup.cfg` to enable
compatibility with Black (flake8 does not support pyproject.toml configuration,
sadly):

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
ignore = E203, E231, E501, E722, W503, B950
select = C,E,F,W,B,B9
```

(Error E722 is identical to B001.) Here is the flake8 addition for pre-commit, with the `bugbear` plugin:

```yaml
- repo: https://gitlab.com/pycqa/flake8
  rev: 3.9.2
  hooks:
  - id: flake8
    additional_dependencies: [flake8-bugbear]
```

This *will* be too much at first, so you can disable or enable any test by it's
label. You can also disable a check or a list of checks inline with
`# noqa: X###` (where you list the check label(s)). Over time, you can fix
and enable more checks. A few interesting plugins:

* [`flake8-bugbear`](https://pypi.org/project/flake8-bugbear/): Fantastic checker that catches common situations that tend to create bugs. Codes: `B`, `B9`
* [`flake8-docstrings`](https://pypi.org/project/flake8-docstrings/): Docstring checker. `--docstring-convention=pep257` is default, `numpy` and `google` also allowed.
* [`flake8-spellcheck`](https://pypi.org/project/flake8-spellcheck/): Spelling checker. Code: `SC`
* [`flake8-import-order`](https://pypi.org/project/flake8-import-order/): Enforces PEP8 grouped imports (you may prefer isort). Code: `I`
* [`pep8-naming`](https://pypi.org/project/pep8-naming/): Enforces PEP8 naming rules. Code: `N`
* [`flake8-print`](https://pypi.org/project/pep8-naming/): Makes sure you don't have print statements that sneak in. Code: `T`

<details><summary>Flake8-print details: (click here)</summary>

{%- capture "mymarkdown" -%}

Having something verify you don't add a print statement by mistake is _very_
useful.  A common need for the print checker would be to add it to a single
directory (`src` if you are following the convention recommended). You can do
the next best thing by removing directories and file just for this check (`T`)
in your flake8 config:

```ini
[flake8]
select = C,E,F,W,T
per-file-ignores =
    tests/*: T
    examples/*: T
```
{%- endcapture -%}

{{ mymarkdown | markdownify }}

</details>


## isort (extra)

You can have your imports sorted automatically by [isort][]. This will sort your
imports, and is black compatible. One reason to have sorted imports is to
reduce merge conflicts. Another is to clarify where imports come from -
standard library imports are in a group above third party imports, which are
above local imports. All this is configurable, as well. To use isort, the
following pre-commit config will work:

[isort]: https://pycqa.github.io/isort/


```yaml
- repo: https://github.com/PyCQA/isort
  rev: 5.8.0
  hooks:
  - id: isort
```

In order to use it, you need to add some configuration. You can add it to
either `pyproject.toml`:

```ini
[tool.isort]
profile = "black"
multi_line_output = 3
```

[isort]: https://pycqa.github.io/isort/

<!-- TODO: let's have a toggle here and show both forms for tools that support it -->

## PyUpgrade (extra)

Another useful tool is [PyUpgrade][], which monitors your codebase for "old" style
syntax. Most useful to keep Python 2 outdated constructs out, it can even do
some code updates for different versions of Python 3, like adding f-strings
when clearly better (please always use them, they are faster) if you set
`--py36-plus` (for example). This is a recommended addition when you drop
Python 2.6 support, 2.7 support, and especially once you drop 3.6 support.

```yaml
- repo: https://github.com/asottile/pyupgrade
  rev: v2.19.1
  hooks:
  - id: pyupgrade
    args: ["--py36-plus"]
```

[PyUpgrade]: https://github.com/asottile/pyupgrade:


## Setup.cfg format (extra)

There is a tool that keeps your `setup.cfg` organized, and makes sure that
important parts (like Python classifiers) are in sync. This tool,
`setup-cfg-fmt`, has native support for pre-commit:

```yaml
- repo: https://github.com/asottile/setup-cfg-fmt
  rev: v1.17.0
  hooks:
  - id: setup-cfg-fmt
```

## Python warnings (extra)

Python hides important warnings by default, mostly because it's trying to be
nice to users. You are a developer, you don't want it to be "nice". You want to
find and fix warnings before they cause user errors! Always run with `-Wd`, or
set `export PYTHONWARNINGS=d` in your environment.
You can also add the following to your `pyproject.toml` file for pytest:

```ini
[tool.pytest]
addopts = "-Wd"
```

## Spelling (extra)

You can and should check for spelling errors in your code too. If you want
to add this, you can use `codespell` for common spelling mistakes. For example:

```yaml
- repo: https://github.com/codespell-project/codespell
  rev: v2.1.0
  hooks:
  - id: codespell
    args: ["-L", "sur"]
```

You can list allowed spellings in a comma separated string passed to `-L` (or
`--ignore-words-list` - usually it is better to use long options when you are
not typing things live). The example above will allow "Big Sur".

You can also use a local pygrep check to eliminate common capitalization
errors, such as the one below:

```yaml
- repo: local
  hooks:
  - id: disallow-caps
    name: Disallow improper capitalization
    language: pygrep
    entry: PyBind|Numpy|Cmake|CCache|Github|PyTest
    exclude: .pre-commit-config.yaml
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


<details><summary>For a non-docker version: (click here)</summary>

{%- capture "mymarkdown" -%}

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

{%- endcapture -%}

{{ mymarkdown | markdownify }}

</details>

[Flake8]: https://gitlab.com/pycqa/flake8
