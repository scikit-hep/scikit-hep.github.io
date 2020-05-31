---
layout: page
title: GitHub Actions
permalink: /developer/gha_basic
nav_order: 7
parent: Developer information
---

# GitHub Actions

The recommended CI for Scikit-HEP is GitHub Actions (GHA), although its
predecessor Azure is also in heavy usage, and other popular services (Travis,
Appveyor, and Circle CI) may be found in a few packages. GHA is preferred due
to the flexible, extensible design and the tight integration with the GitHub
permissions model (and UI). Here is a guide in setting up a new package with GHA.

GHA is made up of workflows which consist of actions. Here are some of the
workflows you will probably want in your package. These should be in a file
named `.github/workflows/main.yml` or similar.

## Header

Your main CI workflow file should begin something like this:

```yaml
name: CI

on:
  pull_request:
  push:
    branches: master
    tags:
    - 'v*'

jobs:
```

This gives the workflow a nice name, and defines the conditions under which it
runs. This will run on pull requests or pushes to master, and on version tags. If
you use a develop branch, you probably will want to include that.

## Pre-commit

If you use [pre-commit](https://pre-commit.com) (and you should), this is a job that will check pre-commit for you:

{% raw %}
```yaml
  pre-commit:
    name: Format
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - name: set PY
      run: echo "::set-env name=PY::$(python -c 'import hashlib, sys;print(hashlib.sha256(sys.version.encode()+sys.executable.encode()).hexdigest())')"
    - uses: actions/cache@v1
      with:
        path: ~/.cache/pre-commit
        key: pre-commit|${{ env.PY }}|${{ hashFiles('.pre-commit-config.yaml') }}
    - uses: pre-commit/action@v1.1.0
```
{% endraw %}

## Unit tests

Implementing unit tests is also easy. Since you should be following best
practices listed in the previous sections, this becomes an almost directly
copy-and-paste formula, regardless of the package details. You might need
to adjust the Python versions to suit your taste.


{% raw %}
```yaml
  checks:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version:
        - 2.7
        - 3.6
        - 3.8
    name: Check Python ${{ matrix.python-version }}
    steps:
    - uses: actions/checkout@v1

    - name: Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install package
      run: python -m pip install -e .[test]

    - name: Test package
      run: python -m pytest
```
{% endraw %}

A few things to note from above:

The matrix should contain the versions you are interested in. You can also test
on other OS's if you are building any extensions or are worried about your
package on macOS or Windows. Fail-fast is optional.

It currently is still simplest to use version 1 of the checkout, since version
2 strips too much from the repository for `setuptools_scm` to work. Recently,
using `with: fetch-depth: 0` started recovering tag history (it didn't originally).

The formula here for installing should be identical for all users; and using
[PEP 517](https://www.python.org/dev/peps/pep-0517/)/[518](https://www.python.org/dev/peps/pep-0518/)
builds, you are even guaranteed a consistent wheel will be produced just as if
you were building a final package.

## Distribution: Pure Python wheels

We will cover binary wheels later, but for a simple universal (pure Python)
package, the procedure is simple.

{% raw %}
```yaml
  dist:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - uses: actions/setup-python@v1
      with:
        python-version: 3.8

    - name: Install wheel and SDist requirements
      run: python -m pip install "setuptools>=42.0" "setuptools_scm[toml]>=4.1" "wheel"

    - name: Build SDist
      run: python setup.py sdist

    - name: Build wheel
      run: >
        python -m pip wheel . -w wheels &&
        ls -lh wheels &&
        mkdir -p dist &&
        cp wheels/<packagename>*any.whl dist/

    - uses: actions/upload-artifact@v2
      with:
        path: dist

    - uses: pypa/gh-action-pypi-publish@master
      with:
        user: __token__
        password: ${{ secrets.pypi_password }}
      if: github.event_name == 'push' && startsWith(github.event.ref, 'refs/tags')
```
{% endraw %}

A few things to note that are new to this job:

We install SDist requirements by hand since `python setup.py sdist` does not
get the benefits of having pip install things. If you have any special
requirements in your `pyproject.toml`, you'll need to list them here. This is
special just for the SDist, not for making wheels (which should be done by the
PEP 517/518 process for you).

You need to put your base package name in for `<packagename>` in the copy
command; pip will put all wheels needed in the directory you specify, and you
need to just pick out your wheels for upload. You don't want to upload NumPy or
some other wheel it had to build (not common anymore, but can happen).

We upload the artifact just to make it available via the GitHub PR/Checks API.
You can download a file to test locally if you want without making a release.

Finally, only  on release tags, we publish to PyPI. You'll need to go to PyPI,
generate a token for your project, and put it into `pypi_password` on your
repo's secrets page.

## Advanced: Testing against the latest development Python

If you want to add development versions of python, such as `3.9-dev`, add it to your matrix and then use this
instead of the `setup-python` action above:

{% raw %}
```yaml
- uses: actions/setup-python@v2
  if: "!endswith(matrix.python-version, 'dev')"
  with:
    python-version: ${{ matrix.python-version }}
- uses: deadsnakes/action@v1.0.0
  if: "endswith(matrix.python-version, 'dev')"
  with:
    python-version: ${{ matrix.python-version }}
```
{% endraw %}

Warning, though; changes in Python 3.9 are currently incompatible with PyBind11.


