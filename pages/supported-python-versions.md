---
layout: page
title: Python version policy
permalink: /supported-python-versions
nav_order: 60
---

The maintainers of Matplotlib, scikit-learn, IPython, Jupyter, yt, SciPy,
NumPy, and scikit-image have come together and agreed on a plan for Python and
NumPy version support called [NEP 29][]. In light of this plan, the Scikit-HEP
developers have adopted the following guidelines for the Scikit-HEP packages.

- All packages in Scikit-HEP must support the Python versions listed in [NEP 29][].
- All packages in Scikit-HEP are required to add `python_requires` to
  `setup.cfg` or `setup.py`, or the equivalent setting for other PEP 517 build
  systems.
  - Pip tries to install the latest package, but checks `python_requires`. If
    it fails, it tries the next oldest version until it finds one that
    matches. Never drop a version from your CI without also changing
    `python_requires`. If it's not tested, assume it is broken.
  - In general, never set an upper limit for `python_requires`. The point of
    `python_requires` is to fill the appropriate slot in the metadata. When
    pip finds a package, it selects the most recent version possible, then
    checks `python_requires`. If it does not match, it checks the next oldest
    version until it finds one that matches. This is invalid behavior for
    an upper limit, as older versions are not _more_ likely to be support a
    new Python! You do not get a nice error message if you do this.
  - If you do not support Python 2, do not set `[bdist_wheel] universal=1`;
    this adds a `py2` identifier to the name and can confuse users and pip.
- Foundational packages in Scikit-HEP _may_ chose to match Python EOL instead of NEP 29. A key feature of [NEP 29][] is that it targets mature, slowly developing libraries.
  If a user is on Python 3.6 or 3.7, they get an older version of NumPy, but that is
  likely sufficient.
- It is not recommended for any package in Scikit-HEP to support older versions
  of Python than EOL versions (Python 3.5 or less).
- Dropping a Python version should be followed by cleanup using the features of the
  new version; using `pyupgrade` (often via `pre-commit`) is a good start. Also search
  for sys.version_info comparisons. Add mypy checks and static typing were possible, etc.
- Dropping a Python version should always be at least a minor release. This makes
  backporting fixes possible in an emergency.

Beyond these guidelines, [NEP 29][] can be followed exactly. We do not expect to be
able to maintain anything NumPy does not. System interpreters are not ideal for analysis;
Conda, brew, pyenv, or other tools should be used to build an environment for analysis.

Individual packages within Scikit-HEP may have user communities or needs that
require specific support to be maintained. Package maintainers can choose to be
more lenient than this plan recommends, though they will have to take on the
required burden of doing so. Community maintenance will strongly gravitate to the
above plan.

Users are _highly recommended_ to use an interpreter that will be supported by
NEP 29 during the lifetime of their project (or be willing to upgrade interpreters
once a year for projects that span more than 42 months).

## Statement on Python 2

Python 2 has reached [end of life as of January 1st, 2020][py2clock]. No more
code changes to fix bugs and security flaws will be made (the final 2.7 release
was in April 2020). Pip, Packaging, manylinux2010, NumPy, IPython, Matplotlib,
Pandas, and other major packages have already dropped support for Python 2, and
many more packages have made a [pledge to do so][py3statement]. Supporting Python
2 makes API design weaker, static typing harder, and burns extra CI time and
developer cycles that are better put into developing software for Python 3.

Users starting analysis with our tools, or developing new tools, do not need to
be using Python 2. Legacy code is just that, and can use legacy versions of our
software too.

## Statement on Python 3.6

This was a very popular version of Python, and is the "default" version of
Python on CentOS 7, Ubuntu 18.04, and even CentOS 8 (though not well supported,
you should use streams there). However, it is at EOL, [NEP 29][] has already
dropped it, and it really limits use of static typing (`from __future__ import annotations`, `__class_getitem__`, and more). Many "foundational" Scikit-HEP
libraries have not yet dropped 3.6 support since we are in more active
development than the libraries that prompted NEP 29, but some packages already
are dropping support and more will follow. Users should make an effort to always
use at least Python 3.7 in analysis, and preferably the highest version
possible. Note that due to usage of "internal" bytecode, Numba can take up to 5
months to update after a Python release.

[nep 29]: https://numpy.org/neps/nep-0029-deprecation_policy.html
[py2clock]: https://pythonclock.org
[py3statement]: https://python3statement.org
