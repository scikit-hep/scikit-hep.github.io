---
layout: page
title: Affiliated packages
permalink: /affiliated
nav_order: 6
---


Affiliated packages {#affiliated_packages}
====================

In the following, projects that work closely together with Scikit-HEP are described. They extend the Python ecosystem in HEP and remain, due to their size and scope, generally independent of Scikit-HEP.


zfit: scalable pythonic fitting
-------------------------------

[![img-zfit]][zfit]

The [zfit](https://zfit.github.io/zfit/) project brings together the different model fitting efforts in Python for HEP by providing a stable API and workflow. The implementation of the fitting library is based on [TensorFlow], a deep learning framework built for high performance computing on modern architectures, which is mostly hidden to the user. While traditional functionalities such as loading [ROOT]-files or using the [Minuit] minimizer are integrated in zfit, the library is completely independent of the ROOT project and has no dependency on it thanks to Scikit-HEP packages.

zfit uses a class-based approach for every part in the workflow and contains convenient base classes that allow for simple customization. Moreover, zfit offers extensive model building, composition and customization capabilities.

The project consists of additional libraries extending the capabilities of the core package.

[zfit]: https://github.com/zfit
[img-zfit]: {{ site.baseurl }}{% link /assets/images/projusers/logo_zfit.png %}
{: width="70px"}
[ROOT]: https://root.cern.ch/
[Minuit]: https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/
[TensorFlow]: https://www.tensorflow.org/