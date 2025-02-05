---
layout: page
title: Installing conda
permalink: /user/installing-conda/
nav_order: 30
parent: User information
---

## Avoiding the spaghetti installation

Many ways to install Python and Python packages have been developed over the years, and not all of them are compatible with each other. Scikit-HEP supports users of the two major systems: (a) pip with virtual environments and (b) conda-forge. For a newcomer, conda-forge is usually the simplest and most reliable way to get started, so we describe that.

This page is for everyone, but especially newcomers to Python or package management. If, for instance, you're having trouble installing Scikit-HEP packages—e.g. `pip install` fails with an error or you get an `ImportError`/`ModuleNotFoundError` after you think you've installed it—then this page is for you.

<img src="https://imgs.xkcd.com/comics/python_environment.png" alt="A mess of Python environments" style="border: solid white 3px; display: block; margin-left: auto; margin-right: auto;">

<details markdown="1"><summary>What is conda-forge?</summary>

[conda-forge](https://conda-forge.org/) is a "channel" for the [conda](https://docs.conda.io/) package manager containing the Scientific Python ecosystem, Scikit-HEP, and even [ROOT](https://iris-hep.org/projects/rootconda.html) with carefully aligned package versions to ensure that you get a consistent, working system. Within a conda environment, you can still use pip to install packages that are not in this channel, thereby getting access to everything in the [Python Package Index (PyPI)](https://pypi.org/), and everything in the conda environment is kept isolated from all other Python environments, so that you don't disturb any applications that rely on a version of Python that ships with your operating system.

The software in conda-forge are not subject to Anaconda's licensing restrictions, and the conda package manager is free software, so both can be used without any legal restrictions in national labs and universities.

Until recently, the (relatively) [hard part](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge) had been to ensure that you're using conda-forge, rather than an Anaconda default channel. The instructions below describe how to install [Miniforge](https://github.com/conda-forge/miniforge), which is conda-forge without the Anaconda default channel.

You likely have a package manager for your operating system, such as Homebrew, apt-get, or yum. Use conda for Python and its packages and your operating system's package manager for applications (web browsers, text editors, etc.).

</details>

<details markdown="1"><summary>Where will the files go?</summary>

The entire Python distribution, with all packages and the binary shared libraries that support them, will go into a new directory, most likely in your home directory and named `miniforge3`. All of the files in it are installed with your own user permissions (i.e. not superuser, not requiring `sudo`).

</details>

<details markdown="1"><summary>How to remove conda cleanly.</summary>

1. Delete that directory with `rm -rf ~/miniforge3`.
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

Pick your distribution from the first table (CPython, not PyPy), which is [here](https://github.com/conda-forge/miniforge#miniforge3). Your computer's "architecture" depends on the type of CPU and operating system; the most common are Mac OS X with x64_64 (old) or Apple Silicon (new), Linux with x86_64, and Windows with x86_64. On Mac and Linux, you can verify the type of CPU with the `uname -i` command. Select the installation script for your architecture by clicking or right-clicking the link on the Miniforge page.

On Mac or Linux, run the script with

```bash
bash filename-of-the-script-you-just-downloaded.sh
```

Windows has a `start` command; see [Miniforge's instructions](https://github.com/conda-forge/miniforge#windows).

The interactive prompts will ask you where you want to install it (default is `~/miniforge3`) and whether you want to have it enabled whenever you start a new terminal or shell (probably "yes"). Saying "yes" to the latter inserts a "`>>> conda initialize`" section in your shell configuration (probably `~/.bashrc`). If you're installing this non-interactively, pass the `-b` option to automatically answer "yes" to all questions:

```bash
bash filename-of-the-script-you-just-downloaded.sh -b
```

<details markdown="1"><summary>Should you allow conda to take over your shell?</summary>

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

If you say "no" to not let the installer script modify your shell configuration, then you will have to manually find the path to the `conda` executable, which is in `~/miniforge3/bin/conda`.

Should you do it? It's generally a good idea, since you, the user, should use the Python that is installed in a controlled conda environment. Any system utilities and applications that use the operating system's Python know how to get the right one.

</details>

## Regular maintenance of the environment

Now you're ready to go. [Instructions online](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html) tell you how to install packages, like

```bash
conda install name-of-package
```

One of the first commands you should do after installation is

```bash
conda update --all
```

to get the newest versions of all the installed packages (newer than the installation script). Then do this approximately once a week to stay up-to-date on all of your packages. (This command updates to the latest _stable_ versions, not bleeding-edge versions unless you explicitly request them by version number.)

Another good command is

```bash
conda clean --all
```

which removes cached package files (which are not needed, now that they've been installed). Sometimes, you can get gigabytes of disk space back.

## Leveling up

<details markdown="1"><summary>Multiple environments</summary>

One of conda's major features is that it allows you to have completely separate Python versions and packages in different "environments." See [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) in the conda documentation on how to use this feature, especially if you need to switch between projects with different package or version requirements.

Maintaining separate environments for separate projects is one of our recommended "best practices", whether you're using conda or pip with virtualenv. Since they both provide the same functionality, use can use one _or_ the other: in a conda installation, use conda environments to keep different sets of packages and their versions separate from each other.

</details>

<details markdown="1"><summary>Mixing conda and pip</summary>

In a conda environment, even the `pip` command is confined to that environment: `pip install name-of-package` installs into the current environment only. When both options are available, you may wonder whether you should `conda install` or `pip install` a package that exists in both. The best practice is to keep each environment either mostly conda (default to conda if you have a choide) or mostly pip (default to pip if you have a choice) because each installer can correctly satisfy its own dependency constraints, but not the other installer's dependency constraints. An environment that freely mixes conda and pip might include two packages whose versions are incompatible with each other.

As a best practice, try to use `conda install` whenever a package is available in both repositories and fall back on `pip install` if it isn't available in conda-forge (`conda install` says it "couldn't solve" because the package you're asking for "does not exist").

Some machine learning libraries have complicated dependencies and are developed with only pip in mind. For these, the best practice is to make a basic conda environment (only Python) and use pip exclusively within that environment.

</details>

<details markdown="1"><summary>Packages that depend on CUDA (Nvidia GPUs)</summary>

At the time of writing, there is no _reliable_ way to install CUDA using conda or pip, though many important packages require it. For now, the best thing is to install CUDA as a system-wide package, either directly from Nvidia ([Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) or [Windows](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html)) or an Ubuntu package like [nvidia-cuda-toolkit](https://packages.ubuntu.com/source/noble/nvidia-cuda-toolkit) (which keeps itself up-to-date in each `apt upgrade`).

In conda-forge, there is a package named `cudatoolkit` that connects conda packages that require CUDA with the system CUDA, and its version needs to be aligned with the system CUDA's version, and that needs to be aligned with the version of the video card itself (hardware).

Aligning versions gets complicated—we don't have a set of "best practices" to recommend yet. However, the Numba package has a built-in tool for these problems: `conda install numba cudatoolkit` and then run

```bash
numba -s
```

to see all the relevant versions, in particular, the section called `__CUDA Information__`.

</details>
