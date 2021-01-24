---
layout: page
title: "GHA: Pure Python wheels"
permalink: /developer/gha_pure
nav_order: 8
parent: Developer information
---



We will cover binary wheels [on the next page][], but if you do not have a
compiled extension, this is called a universal (pure Python) package, and the
procedure to make a "built" wheel is simple. At the end of this page, there is
a recipe that can often be used exactly for pure Python wheels (if the previous
recommendations were followed).

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
> * You can look in the `.whl` (it's a `.zip`, really) and see where everything is going to go


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

    - name: Build SDist and wheel
      run: pipx run --spec build pyproject-build

    - uses: actions/upload-artifact@v2
      with:
        path: dist/*

    - name: Check metadata
      run: pipx run twine check dist/*

```
{% endraw %}

We use [PyPA-Build](https://pypa-build.readthedocs.io/en/latest/), a
new build tool designed to make building wheels and SDists easy. It run a [PEP
517][] backend and can get [PEP 518][] requirements even for making SDists.

By default this will make an SDist and a wheel from the package in the current
directory, and they will be placed in `./dist`. You can only build SDist
(`-s`), only build wheel (`-w`), change the output folder (`-o <dir>`) or give
a different input folder if you want.

You could use the setup-python action, install `build` and `twine` with `pip`,
and then use `python -m build` or `pyproject-build`, but it's better to use
`pipx` to install and run python applications. Pipx is provided by default by
Github Actions (in fact, they use it to setup other applications).

Also, we currently have to use `pipx run --spec build pyproject-build` because
the module name (`build`) and the program `pyproject-build` do not match. A
future update to pipx and build may fix this so `pipx run build` will be enough.

<details><summary>Breaking up or classic SDist buils (Click to expand)</summary>

{%- capture "mymarkdown" -%}

If you don't have a pyproject.toml, you might need to use the raw `setup.py` commands.
This is the classic way to do things, though you should consider direct usage of setup.py
to be an implementation detail, and setup.py is not even required in modern packages.

You must install SDist requirements by hand since `python setup.py sdist` does not
get the benefits of having pip install things. If you have any special
requirements in your `pyproject.toml` (and still don't want to use `build`),
you'll need to list them. This is special just for the SDist, not for making wheels
(which should be done by the PEP 517/518 process for you because you will use
`build` or `pip`).

To build the wheel, you can use `python -m pip wheel . -w wheelhouse`. Unlike build,
this is a wheelhouse, not the output wheel; any wheels it makes during the process
will be put here, not just the one you wanted to upload. Be sure to use something
like `wheelhouse/my_package*.whl` when you pick your items from this folder so as
not to pick a random dependency that didn't have a binary wheel already. Or just
use PyPA-Build.

{%- endcapture -%}

{{ mymarkdown | markdownify }}
</details>

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

    - uses: pypa/gh-action-pypi-publish@v1.4.1
      with:
        user: __token__
        password: ${{ secrets.pypi_password }}
```
{% endraw %}

When you make a GitHub release in the web UI, we publish to PyPI. You'll need
to go to PyPI, generate a token for your project, and put it into
`pypi_password` on your repo's secrets page.

<details><summary>Complete recipe (click to expand)</summary>

This can be used on almost any package with a standard
`.github/workflows/cd.yml` recipe. This works because `pyproject.toml`
describes exactly how to build your package, hence all packages build exactly via
the same interface:

{%- capture "mymarkdown" -%}
{% raw %}
```yaml
name: CD

on:
  workflow_dispatch:
  push:
    branches:
      - master
  release:
    types:
    - published

jobs:
  dist:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1

    - name: Build wheel and SDist
      run: pipx run --spec build pyproject-build

    - name: Check metadata
      run: pipx run twine check dist/*

    - uses: actions/upload-artifact@v2
      with:
        path: dist/*


  publish:
    needs: [dist]
    runs-on: ubuntu-latest
    if: github.event_name == 'release' && github.event.action == 'published'

    steps:
    - uses: actions/download-artifact@v2
      with:
        name: artifact
        path: dist

    - uses: pypa/gh-action-pypi-publish@v1.4.1
      with:
        password: ${{ secrets.pypi_password }}
```
{% endraw %}
{%- endcapture -%}

{{ mymarkdown | markdownify }}

</details>

[PEP 517]: https://www.python.org/dev/peps/pep-0517/
[PEP 518]: https://www.python.org/dev/peps/pep-0518/
