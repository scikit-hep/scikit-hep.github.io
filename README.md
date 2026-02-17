# Scikit-HEP project website

GitHub pages for the website of the Scikit-HEP project.

The site contains:

- General inforomation on the project.
- Basic documentation on the packages.
- Information for contributors and developers.

## Developer information

To build locally, install rbenv (remember to run `rbenv init` after installing, and `rbenv install 2.7.1`). Then:

```bash
rbenv local 2.7.1
bundle install
bundle exec jekyll serve --livereload
```

The pages are in Markdown in `pages/`. Images and datafiles are in `assets/`.

The packages are stored in YAML files in `_data/`. The `categories.yaml` file provides ordering, as well as provides titles for each category. The projects are in `_data/projects/<category>/<project>.yml`. Each one has a `name`, `description`, homepage `url`, and `readme` url link. They can also have `docs` for documentation URLs, and can have a `repo` url if that is different from the main url. Affiliated packages can eventually be added with `affiliated: true`.
