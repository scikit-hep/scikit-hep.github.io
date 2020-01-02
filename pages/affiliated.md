---
layout: page
title: Affiliated packages
permalink: /affiliated
nav_order: 5
---


Affiliated projects and packages {#affiliated_packages}
================================

In the following, projects that work closely together with Scikit-HEP are described. They extend the Python ecosystem in HEP and remain, due to their size and scope, generally independent of Scikit-HEP.

{% for cat in site.data.categories -%}
{% for item in site.data.projects[cat.name] -%}
{%- assign project = item[1] -%}
{%- if project.affiliated -%}
[![{{project.name}} logo]({{site.baseurl}}{{ project.image | link }})]({{project.url}})

### [{{project.name}}]({{project.url}}): {{project.description}}

{{project.longdescription}}

{%- endif %}
{% endfor -%}
{%- endfor %}

