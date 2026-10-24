require 'html-proofer'

OPTIONS = {
  assume_extension: '.html',
  ignore_urls: [
    %r{^https://indico},
    'https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/',
    'https://drupal.star.bnl.gov/STAR/meetings/star-collaboration-meeting-september-2021/juniors-day',
  ],
  only_4xx: true,
}.freeze

task :build do
  sh "bundle exec jekyll build"
end

desc "Check internal links"
task check: :build do
  HTMLProofer.check_directory('_site/', OPTIONS.merge(disable_external: true)).run
end

desc "Check internal and external links"
task test: :build do
  HTMLProofer.check_directory('_site/', OPTIONS).run
end
