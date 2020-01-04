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

{%  assign items = "" | split: "," -%}
{%- for cat in site.data.categories -%}
{%-   for item in site.data.projects[cat.name] -%}
{%-     assign items = items | push: item[1] -%}
{%-   endfor -%}
{%- endfor -%}
{%- assign items = items | sort_natural: "name" -%}

| Package | README | Documentation |
|---------|--------|---------------|
{% for project in items %}
{%- if project.docs  -%}
{%- capture docs -%} [Read the Docs]({{project.docs}}) {%- endcapture -%}
{%- else -%}
{%- assign docs="" -%}
{%- endif -%}
| [{{project.name}}]({{project.url}}) | [README]({{project.readme}}) | {{docs}} |
{% endfor %}
