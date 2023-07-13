require 'html-proofer'

task :test do
  sh "bundle exec jekyll build"
  options = {
    assume_extension: '.html',
    ignore_urls: [
      %r{^https://indico},
      %r{^http://lhcb},
      %r{^http://chep20},
      'https://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/',
      'https://drupal.star.bnl.gov/STAR/meetings/star-collaboration-meeting-september-2021/juniors-day',
    ],
    only_4xx: true,
  }
  HTMLProofer.check_directory('_site/', options).run
end
