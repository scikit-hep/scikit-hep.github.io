---
layout: page
title: Python version policy
permalink: /supported-python-versions/
parent: Packages
nav_order: 10
---

Scikit-HEP packages follow [SPEC 0][], the Scientific Python recommendation
that replaced [NEP 29][]. Packages support Python versions for three years
after release, and other core dependencies (like NumPy) for two years.

- Packages must set `requires-python` in `pyproject.toml`. Pip uses this to
  select an older release for users on an unsupported interpreter, so never
  drop a version from CI without updating it.
- Do not set an upper limit on `requires-python`. Older releases are not more
  likely to support a new Python, so the fallback that makes lower limits work
  does not apply, and users get a confusing error.
- Foundational packages under rapid development _may_ drop versions sooner,
  and packages with a specific user community _may_ support them longer. The
  maintainers choose, and take on the burden.
- Drop a version in at least a minor release, so that fixes can be backported
  in an emergency.
- After a drop, clean up with `pyupgrade` (usually through `ruff` in
  `pre-commit`), and look for remaining `sys.version_info` checks.

Users are highly recommended to use an interpreter that stays supported for
the lifetime of their project. System interpreters are not ideal for analysis;
use `uv`, `pixi`, Conda, or a similar tool to build an environment.

For more detail, see the [Scientific Python Development Guide][].

[spec 0]: https://scientific-python.org/specs/spec-0000/
[nep 29]: https://numpy.org/neps/nep-0029-deprecation_policy.html
[scientific python development guide]: https://learn.scientific-python.org/development/
