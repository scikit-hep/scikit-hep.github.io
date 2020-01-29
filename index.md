---
layout: home
title: Home
nav_order: 1
---

# Scikit-HEP project - welcome!

The Scikit-HEP project is a community-driven and
community-oriented project with the aim of providing Particle Physics at
large with an ecosystem for data analysis in Python. The project started
in Autumn 2016 and is in full swing.

It is not just about providing core and common tools for the community.
It is also about improving the interoperability between HEP tools and
the scientific ecosystem in Python, and about improving on
discoverability of utility packages and projects.

For what concerns the project grand structure, it should be seen as a
*toolset* rather than a *toolkit*. The project defines a set of five
*pillars*, which are seen to embrace all major topics involved in a
physicist\'s work. These are:

- **Datasets**: data in various sources, such as ROOT, Numpy/Pandas,
  databases, wrapped in a common interface.
- **Aggregations**: e.g. histograms that summarize or project a
  dataset.
- **Modeling**: data models and fitting utilities.
- **Simulation**: wrappers for Monte Carlo engines and other
  generators of simulated data.
- **Visualization**: interface to graphics engines, from ROOT and
  Matplotlib to even beyond.

# Toolset packages {#index_toolset_packages}

To get started, have a look at our [GitHub repository][]. The list of presently available packages follows, together with a very
short description of their goals:

{% for cat in site.data.categories -%}
{%-  assign listing = site.data.projects[cat.name] | sort -%}
## {{cat.title}}:

{%   for item in listing -%}
{%-    assign project = item[1] -%}
{%-    if project.projlogo -%}
{{" "}}[![{{project.name}} logo]({{site.baseurl}}{{ project.projlogo | link }}){: style="{{ project.projlogo-style | default: "height:48px;"}}"}]({{project.url}}){:.logo}<br/>{{" "}}
{%-    endif -%}
[{{project.name}}]({{project.url}}){:.package}
 :
    {{" "}}{{project.description}}
{%-    if project.badges -%}
<br/>{{" "}}
{%-      if project.badges.pypi -%}
           {{" "}}[![PyPI](https://img.shields.io/pypi/v/{{project.badges.pypi}}?color=blue&logo=PyPI&logoColor=white)](https://pypi.org/project/{{project.badges.pypi}}){:.badge}
{%-      endif -%}
{%-      if project.badges.conda-forge -%}
           {{" "}}[![PyPI](https://img.shields.io/conda/vn/conda-forge/{{ project.badges.conda-forge}}.svg?logo=Conda-Forge&color=green&logoColor=white)](https://github.com/conda-forge/{{ project.badges.conda-forge-feedstock | default: project.badges.conda-forge}}-feedstock){:.badge}
{%-      endif -%}
{%-    endif -%}
{%-    if project.affiliated -%}
         {{" "}}🤝 *Affiliated package*{:.affiliated} 
{%-    endif %}

{%   endfor %}

---

{::comment} Badge fury instead:
           {{" "}}[![PyPI](https://badge.fury.io/py/{{project.badges.pypi}}.svg)](https://pypi.org/project/{{project.badges.pypi}}/){:.badge}
           Add these for interesting info:
           {{" "}}[![PyPI](https://img.shields.io/pypi/wheel/{{project.badges.pypi}})](https://pypi.org/project/{{project.badges.pypi}}/){:.badge}
           {{" "}}[![PyPI](https://img.shields.io/pypi/pyversions/{{project.badges.pypi}})](https://pypi.org/project/{{project.badges.pypi}}/){:.badge}
           {{" "}}[![PyPI](https://img.shields.io/pypi/status/{{project.badges.pypi}})](https://pypi.org/project/{{project.badges.pypi}}/){:.badge}
{:/comment}

{% endfor %}

In some cases, the packages provide a bridge between different
technologies and/or popular packages from the Python scientific software
stack.

[GitHub repository]: https://github.com/scikit-hep/
