---
layout: page
title: "GHA: GitHub Actions intro"
permalink: /developer/gha_basic
nav_order: 10
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
    - main

jobs:
```

This gives the workflow a nice name, and defines the conditions under which it
runs. This will run on all pull requests, or pushes to master. If you use a
develop branch, you probably will want to include that.  You can also specify
specific branches for pull requests instead of running on all PRs (will run on
PRs targeting those branches only).

## Pre-commit

If you use [pre-commit](https://pre-commit.com) (and you should), and you don't
want to / can't use [pre-commit.ci](https://pre-commit.ci) yet,
then this is a job that will check pre-commit for you:

{% raw %}
```yaml
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - uses: pre-commit/action@v2.0.3
```
{% endraw %}

If you do use [pre-commit.ci](https://pre-commit.ci), but you
need this job to run a manual check, like check-manifest, then you can keep it
but just use `with: extra_args: --all-files --hook-stage manual check-manifest`
to run just this one check. You can also use `needs: lint` in your other jobs
to keep them from running if the lint check does not pass.

## Unit tests

Implementing unit tests is also easy. Since you should be following best
practices listed in the previous sections, this becomes an almost directly
copy-and-paste formula, regardless of the package details. You might need to
adjust the Python versions to suit your taste; you can also test on different
OS's if you'd like by adding them to the matrix and inputting them into
`runs-on`.


{% raw %}
```yaml
  tests:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version:
        - 2.7
        - 3.6
        - 3.9
    name: Check Python ${{ matrix.python-version }}
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0  # Only needed if using setuptools-scm

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

The formula here for installing should be identical for all users; and using
[PEP 517](https://www.python.org/dev/peps/pep-0517/)/[518](https://www.python.org/dev/peps/pep-0518/)
builds, you are even guaranteed a consistent wheel will be produced just as if
you were building a final package.


## Updating

If you use non-default actions in your repository (you will see some in the
following pages), then it's a good idea to keep them up to date. GitHub
provided a way to do this with dependabot. Just add the following file as
`.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Maintain dependencies for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    ignore:
      # Official actions have moving tags like v1
      # that are used, so they don't need updates here
      - dependency-name: "actions/*"
```

As shown above, you can ignore certain dependencies - this file ignores any
official action, because they are very reliable in keeping a `vX` tag that
moves and points at the latests `vX.Y.Z` release, and API is stable between
major versions. For all other actions, this will check to see if there are
updates to the action daily, and will make a PR if there are updates, including
the changelog and commit summary in the PR.

You can use this for other ecosystems too, including Python.

## Common needs

### Single OS steps

If you need to have a step run only on a specific OS, use an if on that step with `runner.os`:

```yaml
      if: runner.os != 'Windows' # also 'macOS' and 'Linux'
```

Using `runner.os` is better than `matrix.<something>`. You also have an
environment variable `$RUNNER_OS` as well. Single quotes are required here.

### Changing the environment in a step

If you need to change environment variables for later steps, such combining
with an if condition for only for one OS, then you add it to a special file:

```yaml
      run: echo "MY_VAR=1" >> $GITHUB_ENV
```

Later steps will see this environment variable.

### Common useful actions

There are a variety of useful actions. There are GitHub supplied ones:

* [actions/checkout](https://github.com/actions/checkout): Almost always the first action. v2 does not keep Git history unless `with: fetch-depth: 0` is included.
* [actions/setup-python](https://github.com/actions/setup-python): Always use v2, as that can setup any Python, including uninstalled ones and pre-releases.
* [actions/cache](https://github.com/actions/cache): Can store files and restore them on future runs, with a settable key. Use v2.
* [actions/upload-artifact](https://github.com/actions/upload-artifact): Upload a file to be accessed from the UI or from a later job. Use v2.
* [actions/download-artifact](https://github.com/actions/download-artifact): Download a file that was previously uploaded, often for releasing. Match upload-artifact version.

And many other useful ones:

* [ilammy/msvc-dev-cmd](https://github.com/ilammy/msvc-dev-cmd): Setup MSVC compilers.
* [jwlawson/actions-setup-cmake](https://github.com/jwlawson/actions-setup-cmake): Setup any version of CMake on almost any image.
* [excitedleigh/setup-nox](https://github.com/excitedleigh/setup-nox): Setup all versions of Python and provide nox.
* [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish): Publish Python packages to PyPI.
* [pre-commit/action](https://github.com/pre-commit/action): Run pre-commit with built-in caching.
* [conda-incubator/setup-miniconda](https://github.com/conda-incubator/setup-miniconda): Setup conda or mamba on GitHub Actions.
* [peaceiris/actions-gh-pages](https://github.com/peaceiris/actions-gh-pages): Deploy built files to to GitHub Pages
* [ruby/setup-miniconda](https://github.com/ruby/setup-ruby) Setup Ruby if you need it for something.

There are also a few useful tools installed which can really simplify your workflow or adding custom actions:

* [pipx](https://github.com/pypy/pipx): This is pre-installed on all runners (GitHub uses to set up other things), and is kept up to date. It enables you to use any PyPI application in a single line with `pipx run <app>`.


### Custom actions

You can [write your own actions](https://docs.github.com/en/actions/creating-actions) locally or in a shared GitHub repo in either a shell (called "composite", but they only support shell steps and merge the outputs - so basically a shell action), JavaScript, or Docker. Combined with pipx, shell actions are very easy to write!
