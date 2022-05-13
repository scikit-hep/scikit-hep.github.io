---
layout: page
title: Installing conda
permalink: /user/installing-conda
nav_order: 10
parent: User information
---

## Avoiding the spaghetti installation

Many ways to install Python and Python packages have been developed over the years, and not all of them are compatible with each other. Scikit-HEP supports users of the two major systems: (a) pip with virtual environments and (b) conda-forge. For a newcomer, conda-forge is usually the simplest and most reliable way to get started, so we describe that. Also, we describe how to replace `conda` with `mamba` because it is the fastest way to install packages into that environment.

This page is for everyone, but especially newcomers to Python or package management. If, for instance, you're having trouble installing Scikit-HEP packages—e.g. `pip install` fails with an error or you get an `ImportError`/`ModuleNotFoundError` after you think you've installed it—then this page is for you.

![A mess of Python environments](https://imgs.xkcd.com/comics/python_environment.png)

<details markdown="1"><summary>What is conda-forge?</summary>

[conda-forge](https://conda-forge.org/) is a "channel" for the [conda](https://docs.conda.io/) package manager containing the Scientific Python ecosystem, Scikit-HEP, and even [ROOT](https://iris-hep.org/projects/rootconda.html) with carefully aligned package versions to ensure that you get a consistent, working system. Within a conda environment, you can still use pip to install packages that are not in this channel, thereby getting access to everything in the [Python Package Index (PyPI)](https://pypi.org/), and everything in the conda environment is kept isolated from all other Python environments, so that you don't disturb any applications that rely on a version of Python that ships with your operating system.

The software in conda-forge are not subject to Anaconda's licensing restrictions, and the conda package manager is free software, so both can be used without any legal restrictions in national labs and universities.

Until recently, the (relatively) [hard part](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge) had been to ensure that you're using conda-forge, rather than an Anaconda default channel. The instructions below describe how to install [Miniforge](https://github.com/conda-forge/miniforge), which is conda-forge without the Anaconda default channel.

You likely have a package manager for your operating system, such as Homebrew, apt-get, or yum. Use conda for your Python packages and your operating system's package manager for applications (web browsers, text editors, etc.).\*

(\* We're doing conda a disservice by describing conda as a Python package manager, though [it does much more](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/#Myth-#2:-Conda-is-a-Python-package-manager), for the sake of keeping this description simple.)

</details>

<details markdown="1"><summary>What is "mamba"?</summary>

We recommend using `mamba`, which is a drop-in replacement for `conda` that is [many times faster](https://wolfv.medium.com/making-conda-fast-again-4da4debfb3b7) (in the "Solving environment: ..." step). You particularly notice it when a package has many dependencies or complex version constraints on its dependencies.

In fact, the conda developers are [incorporating mamba into conda](https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community). At the time of this writing, however, that integration is still experimental. These instructions will describe how to use `mamba` directly.

</details>

<details markdown="1"><summary>Where will the files go?</summary>

The entire Python distribution, with all packages and the binary shared libraries that support them, will go into a new directory, most likely in your home directory and named `mambaforge`. All of the files in it are installed with your own user permissions (i.e. not superuser/requiring `sudo`).

</details>

<details markdown="1"><summary>How to remove conda/mamba cleanly.</summary>

1. Delete that directory with `rm -rf ~/mambaforge`.
2. Delete a file named `~/.condarc`, if you have one.
3. Check your shell configuration file, probably named `~/.bashrc`, for a "`>>> conda initialize`" section. If you have one, delete it.

Those three steps will remove any vestige of the conda installation.

</details>

<details markdown="1"><summary>How to save an old package list before deleting it.</summary>

If you already have a conda installation, you can bundle your current environment into an environment file (a list of names and versions of packages) with

```bash
conda env export --from-history > old-environment.yml
```

After setting up a new conda system, you can reinstall all of those packages/versions with

```bash
conda env create -f old-environment.yml
```

</details>

## Installing a Python environment

We'll be using Miniforge to install the Python environment, which is [distributed here on GitHub](https://github.com/conda-forge/miniforge).

The steps of the installation procedure are (1) download an installer script, (2) run it, and (3) answer interactive prompts.

Of the four combinations Miniforge gives you (`conda` vs `mamba`, Python vs PyPy), [we recommend mamba with Python, which is this table](https://github.com/conda-forge/miniforge#mambaforge). (Open that link in a new window.)

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

The interactive prompts will ask you where you want to install it (default is `~/mambaforge`) and whether you want to have it enabled whenever you start a new terminal or shell (probably "yes"). Saying "yes" to the latter inserts a "`>>> conda initialize`" section in your shell configuration (probably `~/.bashrc`).

<details markdown="1"><summary>Deciding whether conda should take over your shell?</summary>

If you say "yes" to let the installer script modify your shell configuration, then the next terminal you open will be in the conda environment. For instance,

```bash
python
```

will run the conda environment's Python, rather than any other Python you have installed on your computer. This is what conda calls the "base" environment (though you can create more environments that are independent of this one).

If, instead, you want to explicitly opt-into conda environments by calling a command, use

```bash
conda config --set auto_activate_base false
```

to prevent the "base" environment from being automatically loaded in each new terminal. Now all environments, including "base", have to be explicitly activated with

```bash
conda activate name-of-environment
```

See [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) in the conda documentation for more.

If you say "no" to not let the installer script modify your shell configuration, then you will have to manually find the path to the `conda` executable, which is in `~/mambaforge/bin/conda`. All of the above applies, but your shell might not be able to find `conda` or `python`.

</details>

## Regular maintenance of the environment

Now you're ready to go. [Instructions online](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) tell you how to install packages, like

```bash
conda install name-of-package
```

Since you installed `mamba`, you can replace `conda install` with `mamba install` to make the dependency resolution much faster.

```bash
mamba install name-of-package   # fast!
```

There are no other differences, and you can always fall back on using the `conda` command. (Necessary, for instance, in `conda activate name-of-environment`.)

One of the first commands you should do after installation is

```bash
mamba update --all
```

to get the newest versions of all the installed packages (newer than the installation script). Then do this approximately once a week to stay up-to-date on all of your packages. (This command updates to the latest _stable_ versions, not bleeding-edge versions unless you explicitly request them by version number.)

Another good command is

```bash
mamba clean --all
```

which removes cached package files (which are not needed, now that they've been installed). Sometimes, you can get gigabytes of disk space back.

## Leveling up: multiple environments

One of conda's major features is that it allows you to have completely separate Python versions and packages in different "environments." See [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) in the conda documentation on how to use this feature, especially if you need to switch between projects with different package or version requirements.

Maintaining separate environments for separate projects is one of our recommended "best practices", whether you're using conda or pip with virtualenv.
