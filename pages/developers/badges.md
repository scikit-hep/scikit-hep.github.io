---
layout: page
title: Badges
permalink: /badges
nav_order: 20
parent: Developer information
---

<!-- prettier-ignore -->
## Scikit-HEP projects

In your README, you should have a Scikit-HEP project badge: [![Scikit-HEP][sk-badge]](https://scikit-hep.org/){:.badge}

<div class="skhep-bar d-flex m-2" style="justify-content:center;">
  <button class="skhep-bar-item btn m-2 btn-purple" onclick="openTab('md')" id='md-btn'>Markdown</button>
  <button class="skhep-bar-item btn m-2" onclick="openTab('rst')" id='rst-btn'>reStructuredText</button>
</div>

<div class="skhep-tab" markdown="1" id="md">
```md
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)

[sk-badge]: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

```
</div>
<div class="skhep-tab" markdown="1" id="rst" style="display:none;">
```

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
:target: https://scikit-hep.org

````
</div>

Or an affiliated package badge if you are an affiliated package: [![Scikit-HEP][sk-badge-aff]](https://scikit-hep.org/){:.badge}

<div class="skhep-bar d-flex m-2" style="justify-content:center;">
  <button class="skhep-bar-item btn m-2 btn-purple" onclick="openTab('md')" id='md-btn'>Markdown</button>
  <button class="skhep-bar-item btn m-2" onclick="openTab('rst')" id='rst-btn'>reStructuredText</button>
</div>

<div class="skhep-tab" markdown="1" id="md">
```md
[![Scikit-HEP][sk-badge-aff]](https://scikit-hep.org/)

[sk-badge-aff]: https://scikit-hep.org/assets/images/Scikit--HEP-Affiliated-blue.svg
````

</div>
<div class="skhep-tab" markdown="1" id="rst" style="display:none;">
```
.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Affiliated-blue.svg
   :target: https://scikit-hep.org
```
</div>

[sk-badge]: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
[sk-badge-aff]: https://scikit-hep.org/assets/images/Scikit--HEP-Affiliated-blue.svg

To recreate this badge, you can use:

```bash
wget -O Scikit--HEP-Project-blue.svg 'https://img.shields.io/badge/Scikit--HEP-Project-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAcCAYAAAB/E6/TAAAACXBIWXMAAAEZAAABGQHyCY1sAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImdlktonFUUx/930kQ0nYo2JX5NUqSghSq2oIgvcCFaC0EEH2AXUh9FEV1UUaGIC924qY8igo+FQi26sWp8gDS24qOgCOIiKCVomLlnZpxk7Dh2GjMz389F7tgv4zfNJGdzh/M/5/zuud/ch9MKDFgnaUjSnHOu2kuOmb0h6brMMoVHgceBY8ApSVVJ05JOAnXga+BJ4OK0fO/9PZL2AL91AwwBLwLz9GYLwKvAcLtGLpcbMbM5MyuXy+UoDXI14BNFcsABYBy4DLgojDvDZH5PxJaAG4CM937SzCgUCnemQcaB0yFpDngMGFhmefuBh4E/Qt4/tVrtoJlhZq+nJWwHaiH4F2DL2QAp+SPA9wBxHDM7O5svl8vZzqBzgOkAOQGsXwmkbbVabUOj0Wh/1xIw+J+Yy+UuBJ4O4jywdTUQSSoUCgdKpRJxHC+Ees8mxVKr1WoGYf9qId77m80sNrNvgedDvb+A8yQpMzg4OJHJZPoAVavVQ6uBmNmQc+4dSfVWq7Vb0n5JC5KyknZIUiabzdYlqdFoqF6vTxSLxctXwXpNUuSce3RsbOyEc+6kpKNBG5ekjKRLguMTSUNxHE/m8/ntvRK89w9IukvS4SiK3k5Ix8N4aRu0UZIGBgaOAHdIWpfJZI56769fDlIqlTY7515yzlkcx3s65xDGjW1Qf3A0R0ZGJpxzOyX1Oee+MLMd3SDAmjiOD0paK+nB0dHRuY6QhTD2t0EWHJEkRVF0zDl3k6TTkj5OPUIkmdkzwLWSXomi6POUkNFkZxlJM8GxrR0RRdEPzrkbnXOzwHve+/s7IFc55/ZJmmq1Wvu6NH1FGGfaS3B3YrMuOTJKpdJmM5sO+2OvJBWLxUEz+9XM5vP5/DalWDhpqqHu7rYzmzhI96Ys0aZQmEKh8IKZvRV+P9GlEwEPhXoNYCgpvByE2SXCmc6GzeyncCLjvZ8EUi9N4HygEOq92SmuB/4M4pdAf2eBmZmZC7z3lQDb1AXSB3wW6vwNpF54twOtEPQBsLYzplgsfmhmpHUDnAscCvkxsCttMu3gpzhjPwNLNq2ZHU4DsXgr/5jIfa4rJJF0H0vfCp8C9wLDSRCwAdgFfBQ6gMW3wyPLQhKwK4Gv+L81m80mwKkU7Tvgmp4hHcBbgXcTf5ROqwLvA7cBblWQDmA/sLVSqXxTqVQAbmHxJXTWh0vS1vQS5JxrSJoys3JwHXHOxSuZbE+ghE1J2rJSiCT9CxJT5EBIY81lAAAAAElFTkSuQmCC.svg'
```

## Other projects

It is highly recommended you have the PyPI and Conda-Forge badges (if applicable). Tests, docs, and Zenodo DOI are generally recommended as well.

<script>
function openTab(tabName) {
  var tab = document.getElementsByClassName("skhep-tab");
  for (const t of tab) {
    t.style.display = t.id == tabName ? "block" : "none";
  }
  var btn = document.getElementsByClassName("skhep-bar-item");
  for (const b of btn) {
    if(b.id == tabName.concat("-btn"))
      b.classList.add("btn-purple");
    else
      b.classList.remove("btn-purple");
  }
}
function ready() {
  const urlParams = new URLSearchParams(window.location.search);
  const tabs = urlParams.getAll("tabs");

  for (const tab of tabs) {
    openTab(tab);
  }
}

document.addEventListener("DOMContentLoaded", ready, false);
</script>
