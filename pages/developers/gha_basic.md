---
layout: page
title: "GHA: GitHub Actions intro"
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
    branches:
    - master

jobs:
```

This gives the workflow a nice name, and defines the conditions under which it
runs. This will run on all pull requests, or pushes to master. If you use a
develop branch, you probably will want to include that.  You can also specify
specific branches for pull requests instead of running on all PRs (will run on
PRs targeting those branches only).

## Pre-commit

If you use [pre-commit](https://pre-commit.com) (and you should), this is a job
that will check pre-commit for you:

{% raw %}
```yaml
  pre-commit:
    name: Format
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - uses: pre-commit/action@v2.0.0
```
{% endraw %}

## Unit tests

Implementing unit tests is also easy. Since you should be following best
practices listed in the previous sections, this becomes an almost directly
copy-and-paste formula, regardless of the package details. You might need to
adjust the Python versions to suit your taste; you can also test on different
OS's if you'd like by adding them to the matrix and inputting them into
`runs-on`.


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
        - 3.9.0-beta.4  # Optional!
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
