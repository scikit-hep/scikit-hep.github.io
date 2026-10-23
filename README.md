# Scikit-HEP project website

GitHub pages for the website of the Scikit-HEP project.

The site contains:

- General information on the project.
- Basic documentation on the packages.
- Information for contributors and developers.

## Developer information

To build locally, you need Ruby 3.1 or newer (CI uses 3.4). Then:

```bash
bundle install
bundle exec jekyll serve --livereload
```

To check links, run `bundle exec rake check` (internal links only) or
`bundle exec rake test` (internal and external links).

The pages are in Markdown in `pages/`. Images and datafiles are in `assets/`.

The packages are stored in YAML files in `_data/`. The `categories.yml` file provides ordering, as well as provides titles for each category. The projects are in `_data/projects/<category>/<project>.yml`. Each one has a `name`, `description`, homepage `url`, and `readme` url link. They can also have `docs` for documentation URLs, and can have a `repo` url if that is different from the main url. Affiliated packages can eventually be added with `affiliated: true`.
