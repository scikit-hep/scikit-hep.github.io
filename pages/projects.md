---
layout: page
title: Projects
permalink: /projects
nav_order: 2
---

Projects {#projects}
========

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
