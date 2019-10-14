---
layout: page
title: Affiliated packages
permalink: /affiliated
nav_order: 6
---


Affiliated Packages {#affiliated_packages}
====================

In the following, projects that work closely together with scikit-hep are described. They extend the Python ecosystem in HEP and remain, due to their size and scope, generally independent of scikit-hep.


zfit: scalable pythonic fitting
-------------------------------

[![img-zfit]][zfit]

The [zfit](https://zfit.github.io/zfit/) project brings together the different efforts of fitting in Python by providing a stable model
fitting API and workflow. This comes together with an implementation of the fitting library that is based on TensorFlow, a deep learning framework built for high performance computing on modern architectures. While traditional functionalities such as loading ROOT-files or using the Minuit minimizer are integrated (thanks to scikit-hep packages), it is completely independent of the ROOT project and has no dependency on it.

The core of zfit is a class-based approach for model building, composition and customization capabilities.

The project consists of additional libraries which extend the capabilities of the core.

[zfit]: https://github.com/zfit
[img-zfit]: {{ site.baseurl }}{% link /assets/images/projusers/logo_zfit.png %}
{: width="70px"}
