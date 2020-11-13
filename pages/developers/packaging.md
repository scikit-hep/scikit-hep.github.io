---
layout: page
title: Packaging
permalink: /developer/packaging
nav_order: 5
parent: Developer information
---

# Packaging

The libraries in Scikit-HEP have a variety of different packaging styles, but
this document is intended to outline a recommended style that new packages
should follow, and existing packages should slowly adopt. The reasoning for
each decision is outlined as well.

> #### Note
>
> Raw source lives in git and has a `setup.py`. You *can* install directly from
> git via pip, but normally users install from distributions hosted on PyPI. There
> are three options: **A)** A source package, which ends in `.tar.gz`. This is a copy
> of the GitHub repository, stripped of a few specifics like CI files, and possibly
> with submodules included (if there are any). **B)** A pure python wheel, which
> ends in `.whl` - this is only possible if there are no compiled extensions in the
> library. This does *not* contain a setup.py, but rather a `PKG_INFO` file that is
> rendered from setup.py (or from another build system). **C)** If not pure
> Python, a collection of wheels for every binary platform, generally one per
> supported Python version and OS as well.
>
> Developer requirements (users of A or git) are generally higher than the
> requirements to use B or C.

## Package structure (medium priority)

All packages *should* have a `src` folder, with the package code residing
inside it, such as `src/<package>/`.  This may seem like extra hassle; after
all, you can type "`python`" in the main directory and avoid installing it if
you don't have a `src` folder! However, this is a bad practice, and it causes
several common bugs, such as running `pytest` and getting the local version
instead of the installed version - this obviously tends to break if you build
parts of the library or if you access package metadata.

## PEP 517/518 support (high priority)

Packages should provide a `pyproject.toml` file that *at least* looks like this:

```toml
[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]

build-backend = "setuptools.build_meta"
```

This completely changes your build process if you have Pip 10 or later (you can
disable it with `--no-build-isolation` in special cases, like when writing
custom conda-forge recipes). When this file is present, Pip creates a virtual
environment, installs exactly what it sees here, then builds a wheel (as
described in PEP 518). It then discards that environment, and installs the
wheel.  This **a)** makes the build process reproducible and **b)** makes local
developer installs match the standard install procedure.  Also, **c)** the
build requirements do not leak into the dev or install environments -- you do
not need to have `wheel` installed in your dev environment, for example. It
also **d)** allows complete specification of the environment that `setup.py`
runs in, so you can add packages that can be imported in `setup.py`. You should
*not* be using `setup_requires`; it does not work properly and is deprecated.
If you want to have source builds that work in Pip 9 or earlier (not common),
you should have dev instructions on how to install requirements needed to run
`setup.py`.

You can also use this to select your entire build system; we use setuptools
above but you can also use others, such as [Flit][] or [Poetry][]. This is
possible due to the `build-backend` selection, as described in PEP 517. No
Scikit-HEP packages currently use these since they usually do not allow binary
packages to be created and a few common developer needs, like editable
installs, look slightly different (a way to include editable installs in PEP
517 is being worked on). Usage of these "[hypermodern][]" packaging tools are
generally not found in Scikit-HEP, but not discouraged; all tools build the
same wheels (and they often build setuptools compliant SDists, as well).

### Special additions: NumPy

You may want to build against NumPy (mostly for Cython packages, PyBind11 does
not need to access the NumPy headers). This is the recommendation for
Scikit-HEP:

```toml
requires = [
    "numpy==1.13.3; python_version<='3.6'",
    "numpy==1.14.5; python_version=='3.7'",
    "numpy==1.17.3; python_version=='3.8'",
    "numpy==1.19.4; python_version>='3.9'",
```

This ensures the wheels built work with all versions of NumPy supported by
Scikit-HEP. Whether you build the wheel locally or on CI, you can transfer it
to someone else and it will work as long as the user has NumPy 1.13.3 or later.

## Versioning (medium/high priority)

Packages in Scikit-HEP should use one of the following systems:

### Git tags: official PyPA method

One more section is very useful in your `pyproject.toml` file:

```toml
requires = [
    "setuptools>=42",
    "setuptools_scm[toml]>=3.4",
    # ...
]

[tool.setuptools_scm]
write_to = "src/<package>/version.py"
```

This will write a version file when you build from the GitHub repository. You
get the following benefits:

* No manual file to change with the version number - always in sync with Git
    * Simpler release procedure
    * No more mistakes / confusion
    * You can force a version with an environment variable
      `SETUPTOOLS_SCM_PRETEND_VERSION` without source code changes.
* A new version every commit (both commits since last tag and git hash encoded)
    * Binaries no longer incorrectly "cache" when installing from pip directly
      from git
    * You can always tell the exact commit of every sdist/wheel/install
    * If your working directory is "dirty" (changes/new files that are not
      ignored), you will get a version that indicates this.
* SDists and wheels contain the version file/number just like normal
    * Note that reading the version number for the SDist requires
      `setuptools_scm` and `toml` unless you add a workaround to `setup.py`.
      This is not required for wheels (`setup.py` is not even part of a wheel).


If you want to set a template, you can control the details of this file if
needed for historical compatibility, but it is better for new/young projects to
use the default layout and include this in your `__init__.py`:

```python
from .version import version as __version__
```

In docs, there are a few minor tweaks necessary to make sure the version is
picked up correctly; just make sure you install the package and access it from
there.

The one place where the pep518 requirements do not get picked up is when you
manually run `setup.py`, such as when doing `python setup.py sdist`. If you
are missing `setuptools_scm` or `toml`, you will get silently get version 0.0.0.
To make this a much more helpful error, add this to your `setup.py`:

```python
import setuptools_scm  # noqa: F401
import toml  # noqa: F401
```

If you want to create artifacts for use in-between versions, then you should
disable shallow checkouts in your CI, since a non-tagged version cannot be
computed correctly from a checkout that is too shallow. For GitHub Actions,
either use `actions/checkout@v1` or `with: fetch-depth: 0` on `v2`.

For GitHub actions, you can add a few lines that will enable you to manually
trigger builds with custom versions:

{% raw %}
```yaml
on:
  workflow_dispatch:
    inputs:
      overrideVersion:
        description: Manually force a version
env:
  SETUPTOOLS_SCM_PRETEND_VERSION: ${{ github.event.inputs.overrideVersion }}
```
{% endraw %}

If you fill in the override version setting when triggering a manual workflow
run, that version will be forced, otherwise, it works as normal.

> Note: Make sure you have a good gitignore, probably starting from [GitHub's
> Python one](https://github.com/github/gitignore/blob/master/Python.gitignore)
> or using a [generator site](https://www.toptal.com/developers/gitignore).

### Classic in-source versioning

Recent versions of `setuptools` have improved in-source versioning. If you have
a simple file that includes a line with a simple PEP 440 style version, like
`version = "2.3.4.beta1"`, then you can use a line like this in your
`setup.cfg`:

```ini
[metadata]
version = attr: package._version.version
```

Setuptools will look in the AST of `_verison.py` for a simple assignment; if
that works, it will not actually import your package during the setup phase
(which is bad). Older versions of setuptools or complex version files will
import your package; if it is not importable with the pyproject.toml
requirements only, this will fail.

Flit will always look for `package.__version__`, and so will always import your
package; you just have to deal with that if you use Flit.

### pyhf Versioning system

pyhf has a [custom version
system](https://scikit-hep.org/pyhf/development.html#publishing) based on
GitHub actions and bumpversion. At least one other package in Scikit-HEP is
using this, as well.

## Setup configuration (medium priority)

You should put as much as possible in your `setup.cfg`, and leave `setup.py`
for *only* parts that need custom logic or binary building. This keeps your
`setup.py` cleaner, and many things that normally require a bit of custom code
can be written without it, such as importing version and descriptions. Here's
an example:

```ini
[metadata]
name = package
author = My Name
author_email=me@email.com
maintainer = Scikit-HEP
maintainer_email = scikit-hep-admins@googlegroups.com
url = https://github.com/scikit-hep/package
description = A great package.
long_description = file: README.md
long_description_content_type = text/markdown
license = BSD 3-Clause License
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    Intended Audience :: Science/Research
    License :: OSI Approved :: BSD License
    Operating System :: Microsoft :: Windows
    Operating System :: MacOS
    Operating System :: POSIX
    Operating System :: Unix
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: C++
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Information Analysis
    Topic :: Scientific/Engineering :: Mathematics
    Topic :: Scientific/Engineering :: Physics
    Topic :: Software Development
    Topic :: Utilities

[options]
python_requires = >=2.7, !=3.0, !=3.1, !=3.2, !=3.3, !=3.4
packages = find:
package_dir =
    =src
install_requires =
    numpy >=1.13.3

[options.packages.find]
where = src
# Not needed unless not following the src layout
# exclude =
#     tests
#     extern

[tool:pytest]
junit_family=xunit2
testpaths =
    tests
```

And, a possible `setup.py`:

```python
#!/usr/bin/env python
# Copyright (c) 2020, My Name
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/package for details.

from setuptools import setup

setup()
```

Note that we do not recommend overriding or changing the behavior of `python
setup.py test` or `python setup.py pytest`; the test command through `setup.py`
is deprecated and discouraged - anything that directly calls `setup.py` assumes a
`setup.py` is present, which is not true for [Flit][] packages and other systems.[^1]
Instead, assume users call pytest directly.

## Extras (low/medium priority)

It is recommended to use extras instead of or in addition to making requirement
files. These extras a) correctly interact with install requires and other
built-in tools, b) are available directly when installing via PyPI, and c) are
allowed in `requirements.txt`, `install_requires`, `pyproject.toml`, and most other
places requirements are passed.

Here is an example of a simple extras, placed in setup.cfg:

```ini
[options.extras_require]
test =
  pytest >=4.6
mpl =
  matplotlib >=2.0
```

And a complex one, that does some logic (like combining the requirements into
an "all" extra), placed in setup.py:

```python
extras = {
    "test": ["pytest"],
    "docs": [
        "Sphinx>=2.0.0",
        "recommonmark>=0.5.0",
        "sphinx_rtd_theme",
        "nbsphinx",
        "sphinx_copybutton",
    ],
    "examples": ["matplotlib", "numba"],
    "dev": ["pytest-sugar", "ipykernel"],
}
extras["all"] = sum(extras.values(), [])

setup(extras_require=extras)
```

[^1]: Actually, Flit produces a backward-compatible `setup.py` by default when
      making an SDist - it's only "missing" from the GitHub repository.

[Flit]:  https://flit.readthedocs.io
[Poetry]: https://python-poetry.org
[hypermodern]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
