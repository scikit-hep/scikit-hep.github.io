# Scikit-HEP project website

GitHub pages for the website of the Scikit-HEP project.

It contains:

- General info on the project.
- Basic documentation on the Python packages.
- Information for contributors and developers.

## Developer info

To build locally, install rbenv (remember to run `rbenv init` after installing, and `rbenv install 2.7.1`). Then:

```bash
rbenv local 2.7.1
bundle install
bundle exec jekyll serve --livereload
```

The pages are in markdown in `pages/`. Images and datafiles are in `assets/`.

The packages are stored in yaml files in `_data/`. The `categories.yaml` file provides ordering, as well as provides titles for each category. The projects are in `_data/projects/<category>/<project>.yml`. Each one has a `name`, `description`, homepage `url`, and `readme` url link. They can also have `docs` for documentation URLs, and can have a `repo` url if that is different from the main url. Affiliated packages can eventually be added with `affiliated: true`.

The primary branch is now `main`.
