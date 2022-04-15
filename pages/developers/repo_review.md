---
layout: page
title: Repo Review
permalink: /developer/reporeview
nav_order: 110
parent: Developer information
interactive_repo_review: true
---

# Scikit-HEP Repo Review

You can check the style of a GitHub repository below. Enter any repository, such
as `scikit-hep/hist`, and the branch you want to check, such as `main` (it must
exist). This will produce a list of results - green checkmarks mean this rule is
followed, red x's mean the rule is not. A yellow warning sign means that the
check was skipped because a previous required check failed. Some checks will
fail, that's okay - the goal is bring all possible issues to your attention, not
to force compliance with arbitrary checks.

You can also run [this tool](https://github.com/henryiii/scikit-hep-repo-review)
locally:

```bash
pipx run scikit-hep-repo-review <path to repo>
```

---

{% include interactive_repo_review.html %}

[Open in new page](https://henryiii.github.io/scikit-hep-repo-review/).