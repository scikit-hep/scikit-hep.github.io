---
layout: page
title: Package requirements and guidelines
permalink: /guidelines
nav_order: 1
parent: Developer information
---

# Package requirements and guidelines

The below provides requirements and guidelines for Scikit-HEP packages,
which we hope help providing high-quality packages with some level of homogeneity across them.

### Package license

Every package is required to have a license.
As a  guideline, we try to be as open as possible with licensing,
following what most of the other packages use in the wide Python scientific community;
Scikit-HEP packages typically use the BSD-3 license.
It is acknowledged that exceptions are needed and "sticky licenses" such as GPL may be the only viable option.

### README

A `README.[md,rst]` file is required.
It should provide an overview of the package and at least a quick getting started section.
There are several examples on how to go about this in the various Scikit-HEP packages.

### Documentation

Documentation in the code is a must and so-called docstrings should permeate the code as much as possible.
It is suggested to provide documentation via [ReadTheDocs][].

### Code formatting.

We suggest as a guideline to use [Black][], which is rather popular these days.
See [/style][] for details.

### Tests ad continuous integration

A reasonable test suite is a requirement, and it is desirable to achieve high coverage with clever tests - naturally.
We recommend to use [pytest][] as a testing framework
and GitHub Actions (GHA) for how to run the tests in continuous integration (CI).


[Black]: https://black.readthedocs.io/en/latest/
[ReadTheDocs]: https://readthedocs.org/
[pytest]: https://docs.pytest.org/
