---
layout: page
title: "QR codes"
permalink: /packages/qr_codes/
nav_order: 200
parent: Packages
---

Project and package QR codes are made available for presentations, see the list below.

<div class="text-center">
{% for image in site.static_files %}
    {% if image.path contains 'images/projqrcode' %}
        <a href="{{ image.path | relative_url }}">
            <img src="{{ image.path | relative_url }}" alt="QR code" />
        </a>
    {% endif %}
{% endfor %}
</div>
