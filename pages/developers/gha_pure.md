---
layout: page
title: "GHA: Pure Python wheels"
permalink: /developer/gha_pure
nav_order: 8
parent: Developer information
---



We will cover binary wheels [on the next page][], but if you do not have a compiled
extension, this is called a universal (pure Python) package, and the procedure
to make a "built" wheel is simple.

> Note: Why make a wheel when there is nothing to compile? There are a multitude of reasons
> that a wheel is better than only providing an sdist:
>
> * Wheels do not run setup.py, but simply install files into locations
>   - Lower install requirements - users don't need your setup tools
>   - Faster installs
>   - Safer installs - no arbitrary code execution
>   - Highly consistent installs
> * Wheels pre-compile bytecode when they install
>   - Initial import is not slower than subsequent import
>   - Less chance of a permission issue
> * You can look in the `.whl` (it's a `.tar.gz`, really) and see where everything is going to go


[on the next page]: {{ site.baseurl }}{% link pages/developers/gha_wheels.md %}

## Job setup

```yaml
name: CD

on:
  workflow_dispatch:
  release:
    types:
    - published

jobs:

```

This will run when you manually trigger a build ([`workflow_dispatch`][]), or
when you publish a release. Later, we will make sure that the actual publish
step requires the event to be a publish event, so that manual triggers (and
branches/PRs, if those are enabled).

If you want tags instead of releases, you can add the `on: push: tags: "v*"`
key instead of the releases - however, *please* remember to make a GitHub
release of your tag! It shows up in the GUI and it notifies anyone watching
releases(-only). You will also need to change the event filter below.

You can merge the CI job and the CD job if you want. To do that, preferably
with the name "CI/CD", you can just combine the two `on` dicts.

[`workflow_dispatch`]: https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/

## Distribution: Pure Python wheels


{% raw %}
```yaml
  dist:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install wheel and SDist requirements
      run: python -m pip install "setuptools>=42.0" "setuptools_scm[toml]>=4.1" "wheel" "twine"

    - name: Build SDist
      run: python setup.py sdist

    - uses: actions/upload-artifact@v2
      with:
        path: dist/*

    - name: Build wheel
      run: >
        python -m pip wheel . -w wheels

    - uses: actions/upload-artifact@v2
      with:
        path: wheels/<packagename>-*.whl

    - name: Check metadata
      run: twine check dist/* wheels/*

```
{% endraw %}

A few things to note that are new to this job:

We install SDist requirements by hand since `python setup.py sdist` does not
get the benefits of having pip install things. If you have any special
requirements in your `pyproject.toml`, you'll need to list them here. This is
special just for the SDist, not for making wheels (which should be done by the
PEP 517/518 process for you).

You need to put your base package name in for `<packagename>` in the upload
command; pip will put all wheels needed in the directory you specify, and you
need to just pick out your wheels for upload. You don't want to upload NumPy or
some other wheel it had to build (not common anymore, but can happen).

> You can also use `pep518.build` here instead of pip.

We upload the artifact just to make it available via the GitHub PR/Checks API.
You can download a file to test locally if you want without making a release.

We also add an optional check using twine for the metadata (it will be tested
later in the upload action for the release job, as well).

And then, you need a release job:

{% raw %}
```yaml
  publish:
    needs: [dist]
    runs-on: ubuntu-latest
    if: github.event_name == 'release' && github.event.action == 'published'

    steps:
    - uses: actions/download-artifact@v2
      with:
        name: artifact
        path: dist

    - uses: pypa/gh-action-pypi-publish@v1.2.2
      with:
        user: __token__
        password: ${{ secrets.pypi_password }}
```
{% endraw %}

When you make a GitHub release in the web UI, we publish to PyPI. You'll need
to go to PyPI, generate a token for your project, and put it into
`pypi_password` on your repo's secrets page.
