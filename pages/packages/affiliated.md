---
layout: page
title: Affiliated packages
permalink: /affiliated
nav_order: 1
parent: Packages
title: Affiliated projects and packages
---

{% include toc.html %}

In the following, projects that work closely together with Scikit-HEP are described. They extend the Python ecosystem in HEP and remain, due to their size and scope, generally independent of Scikit-HEP. In most cases, at least one Scikit-HEP core developer is on the maintainer team or regularly contributes to these packages. These packages are highly recommended for Scikit-HEP developers and users.

{% for cat in site.data.categories -%}
{% for item in site.data.projects[cat.name] -%}
{%- assign project = item[1] -%}
{%- if project.affiliated -%}
{%- if project.image -%}

---

[![{{project.name}} logo]({{ project.image | relative_url }}){: style="{{ project.image-style | default: "height:64px;"}}"}]({{project.url}}){: .largelogo }
{%- else -%}

---

{%- endif %}

## [{{project.name}}]({{project.url}}): {{project.description}}

{{project.longdescription}}

{%- endif %}
{% endfor -%}
{%- endfor %}
