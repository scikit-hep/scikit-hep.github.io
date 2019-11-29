---
layout: page
title: Documentation
permalink: /documentation
nav_order: 3
---

Documentation
=============

Please refer to the documentation provided by the individual packages.
The table below provides direct links \... Note that in
some cases the README files are the actual documentation. For certain
packages where ReadTheDocs style of documentation is available, the
READMEs still contain handy \"getting started\" sections.


| Package | README | Documentation |
|---------|--------|---------------|
{% for items in site.data.projects -%}
{% for item in items[1] %}
{%- assign project = item[1] -%}
{%- if project.docs  -%}
{%- capture docs -%} [Read the Docs]({{project.docs}}) {%- endcapture -%}
{%- else -%}
{%- assign docs="" -%}
{%- endif -%}
| [{{project.name}}]({{project.url}}) | [README]({{project.readme}}) | {{docs}} |
{% endfor -%}
{%- endfor %}
