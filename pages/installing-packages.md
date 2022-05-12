---
layout: page
title: Installing Python packages with conda-forge
permalink: /installing-packages
nav_order: 35
---

# Avoiding the spaghetti installation

Many ways to install Python and Python packages have been developed over the years, and not all of them are compatible.

If you're having trouble installing Scikit-HEP packages (e.g. `pip install` fails with an error or you get an `ImportError`/`ModuleNotFoundError`), try following the instructions below to set up a conda-forge environment.

![A mess of Python environments](https://imgs.xkcd.com/comics/python_environment.png)

The instructions are at the bottom of this page, after describing what the installation is and what it will do to your computer.

# What is conda-forge?

[conda-forge](https://conda-forge.org/) is a "channel" for the [conda](https://docs.conda.io/) package manager containing the Scientific Python ecosystem, Scikit-HEP, and even ROOT (MacOS and Linux) with carefully aligned package versions to ensure that you get a consistent, working system. Within a conda environment, you can still use pip to install packages that are not in this channel, thereby getting access to everything in the [Python Package Index](https://pypi.org/), and everything in the conda environment is kept isolated from any other Python environments, so that you don't disturb any applications that rely on a version of Python that ships with your operating system.

The software in conda-forge are not subject to Anaconda's licensing restrictions, and the conda package manager is free software, so both can be used without any legal restrictions in national labs and universities.

Until recently, the (relatively) [hard part](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge) had been to ensure that you're using conda-forge, rather than an Anaconda default channel. The instructions below describe how to install [Miniforge](https://github.com/conda-forge/miniforge), which is conda-forge without the Anaconda default channel.

You likely have a package manager for your operating system, such as Homebrew, apt-get, or yum. Use conda for your Python packages and your operating system's package manager for applications (web browsers, text editors, etc.).*

(* I'm doing conda a disservice by describing conda as a Python package manager, though [it does much more](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/#Myth-#2:-Conda-is-a-Python-package-manager), for the sake of keeping this simple.)

# What is "mamba"?

We recommend using "mamba", which is a drop-in replacement for "conda" that is many times faster. You particularly notice it when a package has many dependencies or complex version constraints on its dependencies.

In fact, the conda developers are [incorporating mamba into conda](https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community), though at the time of this writing, that integration is still experimental. These instructions will describe how to use mamba directly.

# Where will the files go?

The entire Python distribution, with all packages and the shared libraries that support them, will go in a new directory, most likely in your home directory and named `mambaforge`. All of the files in it are installed with your own user permissions (i.e. not superuser/`sudo`).

## How to get rid of them if you change your mind

  1. Delete that directory with `rm -rf ~/mambaforge`.
  2. Delete a file named `~/.condarc`, if you have one.
  3. Check your shell configuration file, probably named `~/.bashrc`, for a "`>>> conda initialize`" section. If you have one, delete it.

Those three steps will remove any vestige of the conda installation.

## How to save an old package list before deleting it

If you already have a conda installation, you can bundle your current environment into an environment file with

```bash
conda env export --from-history > old-environment.yml
```

After reinstalling, you can reconstruct it with

```bash
conda env create -f old-environment.yml
```

# Installing Miniforge

Miniforge is [distributed on GitHub](https://github.com/conda-forge/miniforge).

The steps of the installation procedure are (1) download an installer script, (2) run it, and (3) answer interactive prompts.

Of the four combinations Miniforge gives you (conda vs mamba, Python vs PyPy), [we recommend mamba with Python, which is this table](https://github.com/conda-forge/miniforge#mambaforge).

Within each table is a list of architectures. On Mac and Linux, you can get the name of your architecture from

```bash
uname -i
```

It is very likely `x86_64`. Select the installation script for your architecture by clicking or right-clicking the link on the Miniforge page.

On Mac or Linux, run the script with

```bash
bash filename-of-the-script-you-just-downloaded.sh
```

Windows has a `start` command; see [Miniforge's instructions](https://github.com/conda-forge/miniforge#windows).

The interactive prompts will ask you where you want to install it (default is `~/mambaforge`) and whether you want to have it enabled whenever you start a new terminal or shell (probably yes). Saying "yes" to the latter inserts a "`>>> conda initialize`" section in your shell configuration (probably `~/.bashrc`).

## Using Miniforge

Now you're ready to go. Instructions online tell you how to install packages, like `conda install package-name`. Since you installed "mamba", you can replace `conda install` with `mamba install` to make the dependency resolution much faster. There are no other differences, and you can always fall back on using the `conda` command.

One of the first commands you'll probably want to do is

```bash
mamba update --all
```

Do this approximately once a week, and you'll stay up-to-date on all of your packages. (This updates to the latest _stable_ versions. Bleeding-edge versions would have to be explicitly requested by version number.)

Another good command is

```bash
mamba clean --all   # or mamba
```

which removes cached package files (which are not needed, now that they've been installed). Sometimes, you can get gigabytes of disk space back.

## Keeping environments isolated

One of conda's major features is that it allows you to have completely separate Python versions and packages in different "environments." [See conda's documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) on how to use this feature, especially if you need one project to stay fixed at a specified set of version numbers ("pinned") and another to keep up with the latest updates.
