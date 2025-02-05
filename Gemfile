# frozen_string_literal: true

source 'https://rubygems.org'

ruby '>= 3.1'

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
gem 'jekyll'

# This is needed for GitHub Flavored Markdown
gem 'kramdown-parser-gfm'

# This is the default theme for new Jekyll sites. You may change this to anything you like.
# Using remote theme instead
# gem 'just-the-docs'
gem 'rake'

# Used to be in the stdlib
gem 'logger'

# This is the theme
gem "just-the-docs"

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem 'jekyll-feed'
  gem 'jekyll-redirect-from'
  gem 'jekyll-seo-tag'
  gem 'jekyll-sass-converter', '~> 3.1.0'
end

# Checkers and such
group :test do
  gem 'html-proofer'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: %i[mingw mswin x64_mingw jruby]

# Performance-booster for watching directories on Windows
gem 'wdm' if Gem.win_platform?

gem 'webrick'
