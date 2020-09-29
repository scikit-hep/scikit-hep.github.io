---
layout: page
title: Python Version Policy
permalink: /supported-python-versions
nav_order: 60
---

Supported Python Versions
=========================

The maintainers of Matplotlib, scikit-learn, IPython, Jupyter, yt, SciPy, NumPy, and scikit-image have come together and agreed on a plan for Python and NumPy version support called [NEP 29][]. In light of this plan, the Scikit-HEP developers have adopted the following guidelines for the Scikit-HEP packages.


* All packages in Scikit-HEP must support Python 3, with minimum Python 3 versions listed in [NEP 29][].
* New packages in Scikit-HEP are *allowed* to have one complete release (1.0 or equivalent) for Python 2.7. If users request fixes/patches be available for Python 2.7, they can be applied to a branch on top of this release (this can be viewed as an LTS release, similar to IPython 5). Users of Python 2.7 can pin this version; `python_requires` will ensure this version is selected, as well.
* All packages in Scikit-HEP are required to add `python_required` to `setup.cfg` or `setup.py`, or the equivelent setting for other PEP 517 build systems.
    - Pip tries to install the latest package, but checks `python_required`. If it fails, it tries the next oldest version, until it finds one that matches. Never drop a version from your CI without also changing `python_requires`.
* After this point, packages in Scikit-HEP are recommended to drop Python 2 support for all future versions, starting immediately (unless they have not reached the 1.0 status yet).
* New packages introduced into Scikit-HEP are *not required* to have a Python 2 compatible release.

Beyond these guidelines, NEP 29 can be followed exactly. We do not expect to be able to maintain anything NumPy does not.

Individual packages within Scikit-HEP may have user communities or needs that require specific support to be maintained. Package maintainers can choose to be more lenient than this plan recommends, though they will have to take on the required burden of doing so.

Users are *highly recommended* to use Python 3.7 or newer when starting a new project.

Statement on Python 2
---------------------

Python 2 has reached [end of life as of January 1st, 2020][py2clock]. No more code changes to fix bugs and security flaws will be made past that point (the final 2.7 release was in April 2020). Numpy, IPython, Matplotlib, Pandas, and other major packages have already dropped support for Python 2, and many more packages have made a [pledge to do so][py3statement].

The above plan currently deviates from [NEP 29][] primarily in the support of Python 2 (LTS releases for Python 2, and some packages continuing support for Python 2).
This is currently necessary due to the prevalence of Python 2 in our field.
However, since the versions of all dependencies are becoming locked to legacy versions for Python 2, including Python itself, we can do the same.
Legacy code is just that, and can use legacy versions of our software too.
Users starting analysis with our tools, or developing new tools, do not need to be using Python 2.


[NEP 29]: https://numpy.org/neps/nep-0029-deprecation_policy.html
[py2clock]: https://pythonclock.org
[py3statement]: https://python3statement.org
