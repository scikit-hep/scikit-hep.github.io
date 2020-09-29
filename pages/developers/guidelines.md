---
layout: page
title: Package requirements
permalink: /developer/guidelines
nav_order: 1
parent: Developer information
---

# Package requirements and guidelines

The guidelines on this page provide minimum requirements for Scikit-HEP
packages, which we hope help providing high-quality packages with some level of
homogeneity across them.  New packages should adhere to these minimum
requirements. Further optional suggestions and assistance are provided in the
following pages.

### Package license (required)

Every package is required to have a license.  As a guideline, we try to be as
open as possible with licensing, following what most of the other packages use
in the wide Python scientific community; Scikit-HEP packages typically use the
BSD-3 license.  It is acknowledged that exceptions are needed and "sticky
licenses" such as GPL may be the only viable option.

### README (required)

A `README.[md,rst]` file is required.  It should provide an overview of the
package and at least a quick getting started section.  There are several
examples on how to go about this in the various Scikit-HEP packages.

### Documentation (required)

Documentation in the code is a must and  docstrings should permeate the code as
much as possible.  It is suggested to also provide documentation via
[ReadTheDocs][].

### Code formatting (optional)

We highly recommend but do not require [Black][], which is supported by the
Python Software Foundation and provides a consistent style across many
different packages. For special cases, you can disable formatting for that
line/section only. It is also recommended that you use pre-commit to control
these checks with a standard interface. See [Style]({{ site.baseurl }}{% link
pages/developers/style.md %}) for details.

### Tests and continuous integration (required)

A reasonable test suite is a requirement, and it is desirable to achieve high
coverage.  We require at least some tests, with [pytest][] being our recommended framework.
You should run your tests in CI; see [our GitHub Actions (GHA) page]({{ site.baseurl }}{% link
pages/developers/gha_basic.md %}) for a simple introduction to setting up CI.

### Packaging (required)

You must have a `pyproject.toml`, and if you use setuptools, a `setup.cfg` and/or a `setup.py`.
You should have basic information filled out about your project. A minimal `pyproject.toml` for
setuptools is:

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

This will enable build-isolation, consistant build environments, and will keep build tools from
triggering `setuptools.build_meta:__legacy__`, which is probably not what you want.

You must have a `python_requires` (or equivelent for non-Setuptools builds). You must always
test the lowest item in your `python_requires`; if you drop a version, change your `python_requires`
before release.

### Wheels (required)

Except in special circumstances, you must provide SDists and wheels on PyPI.
This also means your package must be "installable", and therefore should be
using a [PEP 517][] compliant packaging framework. Since many Scikit-HEP packages
have [a binary component]({{ site.baseurl }}{% link
pages/developers/gha_wheels.md %}), we recommend setuptools. It is highly recommended you
automate the building and uploading process so that other Scikit-HEP admins can
make emergency (patch) releases if the need arises; non-standard/non-trivial
processes should be avoided and documented if unavoidable.

If you have a pure Python package, `pip install build; python -m build` will build your
package's SDist and wheel using the specified PEP 517 backend in `pyproject.toml`.


[Black]: https://black.readthedocs.io/en/latest/
[ReadTheDocs]: https://readthedocs.org/
[pytest]: https://docs.pytest.org/
[PEP 517]: https://www.python.org/dev/peps/pep-0517/
