---
layout: page
title: Developer information
permalink: /developer
nav_order: 80
has_children: true
---

Developer Information
=====================

The pages here are intended for developers who [are making][guidelines] or maintaining a package,
especially one that is part of Scikit-HEP or being proposed to become part.

New developers are encouraged to read the following pages.
Veteran developers should still check out [introduction][intro], as it has a guide on recommendations for your `CONTRIBUTING.md`.

Following that, there are recommendations for [style][], intended to promote
good practices and to ensure continuity across the packages. There is a
[dedicated page for static type checking with MyPy][mypy]. There is then a guide on
[packaging][], which should help in ensuring a consistent developer and user
experience when working with distribution.

A section on CI follows, with a [general setup guide][gha_basic], and then two
choices for using CI to distribute your package, on for [pure
Python][gha_pure], and one for [compiled extensions][gha_wheels]. You can read
about setting up good tests on the [pytest page][pytest].

Finally, there are [badge recommendations][badges] for your readme, including the Scikit-HEP badge!

Once you have completed the guidelines, there is a [cookiecutter][] project, [Scikit-HEP/cookie][], that implements these guidelines and lets you setup a new package from a template in less than 60 seconds!

[guidelines]: {{ site.baseurl }}{% link pages/developers/guidelines.md %}
[intro]: {{ site.baseurl }}{% link pages/developers/intro.md %}
[style]: {{ site.baseurl }}{% link pages/developers/style.md %}
[mypy]: {{ site.baseurl }}{% link pages/developers/mypy.md %}
[packaging]: {{ site.baseurl }}{% link pages/developers/packaging.md %}
[gha_basic]: {{ site.baseurl }}{% link pages/developers/gha_basic.md %}
[gha_pure]: {{ site.baseurl }}{% link pages/developers/gha_pure.md %}
[gha_wheels]: {{ site.baseurl }}{% link pages/developers/gha_wheels.md %}
[pytest]: {{ site.baseurl }}{% link pages/developers/pytest.md %}
[badges]: {{ site.baseurl }}{% link pages/developers/badges.md %}

[cookiecutter]: https://cookiecutter.readthedocs.io
[Scikit-HEP/cookie]: https://github.com/scikit-hep/cookie
