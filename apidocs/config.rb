###
# Page options, layouts, aliases and proxies
###

# Per-page layout changes:
#
# With no layout
page '/*.xml', layout: false
page '/*.json', layout: false
page '/*.txt', layout: false

# With alternative layout
# page "/path/to/file.html", layout: :otherlayout

# Proxy pages (http://middlemanapp.com/basics/dynamic-pages/)
# proxy "/this-page-has-no-template.html", "/template-file.html", locals: {
#  which_fake_page: "Rendering a fake page with a local variable" }

# General configuration

set :css_dir, 'static/stylesheets'
set :js_dir, 'static/javascripts'
set :images_dir, 'static/images'
set :fonts_dir, 'static/fonts'

activate :syntax
activate :directory_indexes
activate :asciidoc, :asciidoc_attributes => %w(showtitle= idprefix= toc= toclevels=1)

set :markdown_engine, :kramdown
set :markdown, :toc_levels => [2]

# Reload the browser automatically whenever files change
configure :development do
  activate :livereload
end

###
# Helpers
###

# Methods defined in the helpers block are available in templates
# helpers do
#   def some_helper
#     "Helping"
#   end
# end

# Build-specific configuration
configure :build do
  # Minify CSS on build
  activate :minify_css

  # Minify Javascript on build
  activate :minify_javascript
end
