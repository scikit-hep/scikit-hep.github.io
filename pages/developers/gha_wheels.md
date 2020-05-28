---
layout: page
title: GitHub Actions for Binary Wheels
permalink: /developer/gha_wheels
nav_order: 8
parent: Developer information
---

# GitHub Actions for Binary Wheels

Building binary wheels is a bit more involved, but can still be done
effectively with GHA. This document will introduce
[cibuildwheel][] for use in
Scikit-HEP, replacing our in-house
[azure-wheel-helpers][].  The
benefits of cibuildwheel are a larger user base, fast fixes from CI and pip,
works on all major CI vendors (no lock-in), and covers cases we were not able
to cover (like ARM). We will focus on GHA below.

## Header

Wheel building should only happen rarely, so you will want to limit it to
releases, and maybe a rarely moving branch or other special tag (such as
`master` if you mostly update `develop`. Unlike Azure, you cannot trigger a
build at any time via the web interface.

```yaml
name: Wheels

on:
  push:
    branches:
      - wheels
    tags:
      - "v*"
  release:
```

This will run on version tags and releases. If you use a develop branch, you
probably will want to include `pull_request: branch: master`. Since GHA does not
have manual triggers, this adds a "wheels" branch - just make a wheels branch
to trigger a build. Remove the branch when done.

### Useful suggestion:

Since these variables will be used by all jobs, you could make them available on all steps:

```yaml
env:
  CIBW_TEST_EXTRAS: test
  CIBW_TEST_COMMAND: pytest {project}/tests
  CIBW_BUILD_VERBOSITY: 1
```

The `CIBW_TEST_EXTRAS` will cause the pip install to use `[test]`. The
`CIBW_TEST_COMMAND` will use pytest to run your tests. You can also set the
build verbosity (`-v` in pip) if you want to.

## Making an SDist

You probably should not forget about making an SDist! A simple job, like before, will work:

```yaml
  build_sdist:
    name: Build SDist
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
      with:
        submodules: true    # Optional if you have submodules

    - name: Setup Python 3.7
      uses: actions/setup-python@v2
      with:
        python-version: '3.7'

    - name: Install deps
      run: python -m pip install "setuptools>=42" "setuptools_scm[toml]>=4.1.0"

    - name: Build SDist
      run: python setup.py sdist

    - uses: actions/upload-artifact@v2
      with:
        path: dist/*.tar.gz
```


## The core job (3 main OS's)

The core of the work is down here:

{% raw %}
```yaml
  build_wheels:
    name: Wheel on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-18.04, windows-latest, macos-latest]

    steps:
    - uses: actions/checkout@v1
      with:
        submodules: true

    - name: Setup Python 3.7
      uses: actions/setup-python@v2
      with:
        python-version: '3.7'

    - name: Install cibuildwheel
      run: python -m pip install cibuildwheel==1.4.2

    - name: Build wheel
      run: python -m cibuildwheel --output-dir wheelhouse
      env:
        CIBW_SKIP: pp* cp27-win* cp35-win*

    - name: Upload wheels
      uses: actions/upload-artifact@v2
      with:
        path: wheelhouse/*.whl
```
{% endraw %}

There are several things to note here. First, one of the reasons this works is
because you followed the suggestions in the previous sections, and your package
builds nicely into a wheel without strange customizations (if you *really* need
them, check out [`CIBW_BEFORE_BUILD`][] and [`CIBW_ENVIRONMENT`][].


This lists all three OS's; if you do not support Windows, you can remove that
here.

After Python is prepared, cibuildwheel is installed. This is a normal Python
package, however, do not run it locally, just in a container or on CI, since it
installs the Python versions it needs to global locations. Python 3.6+ should
be fine, but we are following the official example and using Python 3.7. The
Python version running cibuildwheel does not affect the wheels created.

The build step is controlled almost exclusively through environment variables,
which makes it easier (usually) to setup in CI. The main variable needed here
is `CIBW_SKIP`, which filters the build identifiers based on simple
expressions. You can use `pp*` to filter PyPy, and you should probably filter
`cp27-win*` if you use C++11 (more on that below). You can also use
`CIBW_BUILD` to select the platforms you want to build for - see the [docs
here][cibw custom] for
all the identifiers. Note that the ARM and other alternative architectures need
support from the CI, (so basically Travis for now) to run. Windows Python 3.5
seems to be buggy in PEP 517 support.

You can also select different base images (the *default* is manylinux2010).
If you want manylinux1, just do:

```yaml
      env:
        CIBW_MANYLINUX_X86_64_IMAGE: manylinux1
        CIBW_MANYLINUX_I686_IMAGE: manylinux1
```

You can even put any docker image here, including [Scikit-HEP's
`skhep/manylinuxgcc-*`][manylinuxgcc] images.

## Windows 2.7 (why?)

If you have to support Python 2.7 on Windows, you can use a custom job:

```yaml
  build_win27_wheels:
    name: Py 2.7 wheels on Windows
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v1
      with:
        submodules: true

    - uses: actions/setup-python@v2
      with:
        python-version: '3.7'

    - name: Install cibuildwheel
      run: python -m pip install cibuildwheel==1.4.2

    - uses: ilammy/msvc-dev-cmd@v1

    - name: Build 64-bit wheel
      run: python -m cibuildwheel --output-dir wheelhouse
      env:
        CIBW_BUILD: cp27-win_amd64
        DISTUTILS_USE_SDK: 1
        MSSdk: 1

    - uses: ilammy/msvc-dev-cmd@v1
      with:
        arch: x86

    - name: Build 32-bit wheel
      run: python -m cibuildwheel --output-dir wheelhouse
      env:
        CIBW_BUILD: cp27-win32
        DISTUTILS_USE_SDK: 1
        MSSdk: 1

    - uses: actions/upload-artifact@v2
      with:
        path: wheelhouse/*.whl
```

Users will need the current redistributable for Visual Studio. This is a good
example though of how flexible this is; you can split up jobs however you like.
However, keep in mind there is a setup cost for starting/ending a job, so one
job per wheel would be overkill!

## Publishing

{% raw %}
```yaml
  upload_all:
    needs: [build_wheels, build_win27_wheels, build_sdist]
    runs-on: ubuntu-latest

    steps:
    - uses: actions/setup-python@v2
      with:
        python-version: "3.8"

    - name: Install dependencies
      run: python -m pip install twine "setuptools>=42" "setuptools_scm[toml]>=4.1.0"

    - uses: actions/download-artifact@v2
      with:
        name: artifact
        path: dist

    - run: twine check dist/*

    - uses: pypa/gh-action-pypi-publish@master
      with:
        user: __token__
        password: ${{ secrets.pypi_password }}
      if: github.event_name == 'release' && github.event.action == 'published'
```
{% endraw %}

If you have multiple jobs, you will want to collect your artifacts from above.
If you only have one job, you can combine this into a single job like we did
for pure Python wheels, using dist instead of wheelhouse.

Remember to set `pypi_password` to your token in secrets.


> On Travis, cibuildwheel even has the ability to create ARM and PowerPC
> builds. IBM Z builds are also available but in beta.


[azure-wheel-helpers]: https://github.com/scikit-hep/azure-wheel-helpers
[`CIBW_BEFORE_BUILD`]: https://cibuildwheel.readthedocs.io/en/stable/options/#before-build
[`CIBW_ENVIRONMENT`]: https://cibuildwheel.readthedocs.io/en/stable/options/#environment
[manylinuxgcc]: https://github.com/scikit-hep/manylinuxgcc
[cibw custom]: https://cibuildwheel.readthedocs.io/en/stable/options/#build-skip
[cibuildwheel]: https://cibuildwheel.readthedocs.io/en/stable/
