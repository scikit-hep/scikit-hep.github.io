---
layout: page
title: Developer information
permalink: /developer/
nav_order: 30
has_children: true
---

The pages here are intended for developers who are making or maintaining a
package and want to follow modern best practices in Python.

{: .note }

If you are here to propose a new package for Scikit-HEP, please read [package
requirements][guidelines] for a list of minimum Scikit-HEP requirements for
packages joining the organization. We also have [badge recommendations][badges]
for your README, including the Scikit-HEP badge!

{: .highlight }

The developer pages have been moved to [Scientific-Python][]! The remaining
pages here will redirect to the new site.

New developers can start with an [introductory tutorial][intro] before moving
on to the guide.

Following that, there are recommendations for [style][], intended to promote
good practices and to ensure continuity across the packages. There is a
[dedicated page for static type checking with MyPy][mypy]. There is then a guide on
[simple packaging][] or [compiled][] / [classic][] packaging, which should help
in ensuring a consistent developer and user experience when working with distribution.

A section on CI follows, with a [general setup guide][gha_basic], and then two
choices for using CI to distribute your package, on for [pure
Python][gha_pure], and one for [compiled extensions][gha_wheels]. You can read
about setting up good tests on the [pytest page][pytest], including
[coverage][], and [docs][]. You can also see how to set up a [task runner][] to
simplify tasks and help new contributors.

{: .highlight-title }

> New project template
>
> Once you have completed the guidelines, there is a
> [copier][]/[cookiecutter][]/[cruft][] project, [scientific-python/cookie][],
> that implements these guidelines and lets you setup a new package from a
> template in less than 60 seconds! Twelve build backends including compiled
> backends, generation tested in Nox, and kept in-sync with the guide.

{: .important-title }

> Checking an existing project
>
> We provide [sp-repo-review][], a set of [repo-review][] checks for comparing
> your repository with the guidelines, runnable right in the guide via
> WebAssembly! All checks point to a linked badge in the guide.

[guidelines]: {% link pages/packages/guidelines.md %}
[badges]: {% link pages/developers/badges.md %}
[intro]: https://learn.scientific-python.org/development/tutorials/dev-environment/
[style]: https://learn.scientific-python.org/development/guides/style/
[coverage]: https://learn.scientific-python.org/development/guides/coverage/
[task runner]: https://learn.scientific-python.org/development/guides/tasks/
[mypy]: https://learn.scientific-python.org/development/guides/mypy/
[simple packaging]: https://learn.scientific-python.org/development/guides/packaging-simple/
[compiled]: https://learn.scientific-python.org/development/guides/packaging-compiled/
[classic]: https://learn.scientific-python.org/development/guides/packaging-classic/
[gha_basic]: https://learn.scientific-python.org/development/guides/gha-basic/
[gha_pure]: https://learn.scientific-python.org/development/guides/gha-pure/
[gha_wheels]: https://learn.scientific-python.org/development/guides/gha-wheels/
[pytest]: https://learn.scientific-python.org/development/guides/pytest/
[docs]: https://learn.scientific-python.org/development/guides/docs/
[sp-repo-review]: https://learn.scientific-python.org/development/guides/repo-review/
[scientific-python]: https://learn.scientific-python.org/development
[cookiecutter]: https://cookiecutter.readthedocs.io
[copier]: https://copier.readthedocs.io
[cruft]: https://cruft.github.io/cruft
[repo-review]: https://repo-review.readthedocs.io
[scientific-python/cookie]: https://github.com/scientific-python/cookie
