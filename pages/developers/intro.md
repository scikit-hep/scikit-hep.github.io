---
layout: page
title: Intro to development
permalink: /developer/intro
nav_order: 1
parent: Developer information
---

# Intro to development

The libraries in Scikit-HEP try to follow best practices in the community
for development and deployment (though some packages in Scikit-HEP are still
being converted to use best practices). The following outlines the basics for setting
up a development environment. It is recommended as a basis for `CONTRIBUTING.md` or
`.github/CONTRIBUTING.md` in the packages.


## Development environment: Pip

If you want to work on Python software, you should *always* have a virtual environment.
You do not want to risk breaking your main system environment, you want full control over
versions of libraries, and you want to avoid "leaking" your main environment in, causing
you to not notice when you have extra dependencies. Virtual environments are disposable,
while it is very hard to cleanup or update a main system environment.

Any common modern system to create environments should be fine. Here is the most basic
one that comes by default with Python 3:

```bash
python3 -m venv .env
```

This creates a new virtual environment in a local folder, named `.env`. There are a few options,
but usually they are not necessary.

To activate the virtual environment, type:

```bash
. .env/bin/activate
```

The `.` is short for `source`, which runs the script `activate` in your current
shell. If you like a different shell, like fish, there are several activate
scripts; the default one expects a bash-like shell. You need to run this
command any time you want to use the development environment. The activation
script installs a function `deactivate`; type that at any time to leave the
environment (or just close your shell). It also adds a bit of text to your
prompt so you don't forget that you are in an environment.

Finally, you need to install the package. Most packages support several extra options when
installing; for development, you may want `[test]`, `[dev]`, or `[all]`. Here is an example:

```bash
pip install -e .[dev]
```

The `-e` installs the package in "editable" mode, meaning the files are not copied to
your site-packages folder, so you can edit and work with the package locally. You need
to rerun `pip install -e .` if there are binary components and you edit those.

Never edit your `PATH` or `PYTHONPATH` manually, or depend on the current
directory for library development.

## Development environment: Conda

You can also develop in Conda. For some packages, such as those that work with ROOT,
you need to be using Conda, and it is a great way to have control over the version
of Python you are using. If so, then the creation of an environment looks like this:

```bash
conda create -n env_name python=3.8 
```

You can use `-n name` or `-p path` to specify the environment by name or
location.  The following assume you used a name, but just replace names with
paths if you choose a path.

Some packages provide an environment file, either for CI or developer use. If they
do, you can use `conda env create -f filename.yml` to create (or `update` to update)
the provided environment. You can override name or location as above. And if the file
is called `environment.yml`, you can leave off the `-f filename` entirely.

To activate an environment:

```bash
conda activate env_name
```

To deactivate, use `conda deactivate`, or leave your shell.
