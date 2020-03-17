---
layout: home
title: Home
nav_order: 1
---

# Scikit-HEP project - welcome!

The Scikit-HEP project is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with an ecosystem for data
analysis in Python.

To get started, have a look at our [GitHub repository][].

[![Gitter badge][gitter-skhep-badge]][gitter-skhep-link] (see also related rooms [HSF/PyHEP][] and [HSF/PyHEP-newcomers][])

The list of presently available packages follows, together with a very
short description of their goals:

---

{% for cat in site.data.categories -%}
{%-  assign listing = site.data.projects[cat.name] | sort -%}
### {{cat.title}}:

{%   for item in listing -%}
{%-    assign project = item[1] -%}
{%-    if project.projlogo -%}
{{" "}}[![{{project.name}} logo]({{site.baseurl}}{{ project.projlogo | link }}){: style="{{ project.projlogo-style | default: "height:48px;"}}"}]({{project.url}}){:.logo}<br/>{{" "}}
{%-    endif -%}
[{{project.name}}]({{project.url}}){:.package}
 :
    {{" "}}{{project.description}}
{%-    if project.affiliated -%}
         {{" "}}🤝 *Affiliated package*{:.affiliated} 
{%-    endif %}

{%   endfor %}

---

{% endfor %}

In some cases, the packages provide a bridge between different
technologies and/or popular packages from the Python scientific software
stack.

[GitHub repository]: https://github.com/scikit-hep/
[gitter-skhep-link]:   https://gitter.im/Scikit-HEP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
[gitter-skhep-badge]:  https://badges.gitter.im/Scikit-HEP/community.svg
[HSF/PyHEP]:           https://gitter.im/HSF/PyHEP
[HSF/PyHEP-newcomers]: https://gitter.im/HSF/PyHEP-newcomers
