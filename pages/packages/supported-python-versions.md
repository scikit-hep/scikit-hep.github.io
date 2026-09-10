---
layout: page
title: Python version policy
permalink: /supported-python-versions/
parent: Packages
nav_order: 10
---

The maintainers of Matplotlib, scikit-learn, IPython, Jupyter, yt, SciPy,
NumPy, and scikit-image have come together and agreed on a plan for Python and
NumPy version support called [SPEC 0][] (previously [NEP 29][]). In light of
this plan, the Scikit-HEP developers have adopted the following guidelines for
the Scikit-HEP packages. The core difference is that the ultra short support
window of SPEC 0 assumes slow moving established packages, not that users don't
use old Python versions.

Support guideline:

- All packages in Scikit-HEP should at least support the versions specified in
  [SPEC 0][] (last 3 Python versions).
- Most packages in Scikit-HEP choose to support official Python EoL (last 5
  Python versions).
- Packages are highly recommended not to support more than the official EoL
  range. This can break downstream packages that do follow EoL.

General guidelines:

- Packages must set `requires-python` in `pyproject.toml`. Pip uses this to
  select an older release for users on an unsupported interpreter, so never
  drop a version from CI without updating it.
- Do not set an upper limit on `requires-python`. Older releases are not more
  likely to support a new Python, so the fallback that makes lower limits work
  does not apply, and users get a confusing error.
- Drop a version in at least a minor release, so that fixes can be backported
  in an emergency.
- After a drop, clean up with `pyupgrade` (usually through `ruff` in
  `pre-commit`), and look for remaining `sys.version_info` checks.

Users are highly recommended to use an interpreter that stays supported for the
lifetime of their project. A new project should not use a Python version that
is about to become unsupported. System interpreters are not ideal for analysis;
use `uv`, `pixi`, Conda, or a similar tool to build an environment.

For more detail, see the [Scientific Python Development Guide][].

[spec 0]: https://scientific-python.org/specs/spec-0000/
[nep 29]: https://numpy.org/neps/nep-0029-deprecation_policy.html
[scientific python development guide]: https://learn.scientific-python.org/development/
