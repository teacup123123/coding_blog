---
layout: post
title: How this site was created under Ubuntu
author: Tikai Chang
tags: [web, jekyll, "Hello world!"]
---
How this site was created under Ubuntu: 
1. Follow the instructions [here]({ post.url }}), notably the steps *Requirements*, *Step 2* and *Step 3*

2. errors were encountered during the `bundle install` and it's post-install verification
	1. *commonmarker*
	2. *nokogiri*
	3. querying the version of *jekyll* with `jekyll -v`

3. Use of the theme [minimal](https://github.com/pages-themes/minimal), supported by github pages and, the key is to copy the `_layout` files for things to work, especially `default.html`.

4. `bundle exec jekyll serve` and enjoy!

## problems and solutions after some googling
In the following the dependencies were solved and then the command `bundle install` rerun.

### commonmarker problem:

```
Installing commonmarker 0.17.13 with native extensions
Gem::Ext::BuildError: ERROR: Failed to build gem native extension.

...
mkmf.rb can't find header files for ruby at /usr/lib/ruby/include/ruby.h
...
```
		
Solved using `sudo apt-get install ruby2.5-dev`, (replace 2.5 by appropriate version)

### nokogiri problem:

```
Fetching nokogiri 1.10.3
Installing nokogiri 1.10.3 with native extensions
Gem::Ext::BuildError: ERROR: Failed to build gem native extension.

...
...
An error occurred while installing nokogiri (1.10.3), and Bundler
cannot continue.
Make sure that `gem install nokogiri -v '1.10.3' --source
'https://rubygems.org/'` succeeds before bundling.

In Gemfile:
  github-pages was resolved to 198, which depends on
    jekyll-mentions was resolved to 1.4.1, which depends on
      html-pipeline was resolved to 2.11.0, which depends on
	nokogiri
```

Solved according to [this page](https://github.com/flapjack/omnibus-flapjack/issues/72], by installing `zlib1g-dev `(used synaptic package manager but could have used `apt-get install`)

*nokogiri* was installed seperately via `sudo gem install nokogiri` instead of the `bundle install`

### `jekyll -v` not working
This is the command to see the jekyll version. The error when querying it gave:
```
Traceback (most recent call last):
	13: from /usr/local/bin/jekyll:23:in `<main>'
	12: from /usr/local/bin/jekyll:23:in `load'
	11: from /var/lib/gems/2.5.0/gems/jekyll-3.8.5/exe/jekyll:11:in `<top (required)>'
	10: from /var/lib/gems/2.5.0/gems/jekyll-3.8.5/lib/jekyll/plugin_manager.rb:50:in `require_from_bundler'
	 9: from /usr/lib/ruby/vendor_ruby/bundler.rb:101:in `setup'
	 8: from /usr/lib/ruby/vendor_ruby/bundler.rb:135:in `definition'
	 7: from /usr/lib/ruby/vendor_ruby/bundler/definition.rb:35:in `build'
	 6: from /usr/lib/ruby/vendor_ruby/bundler/dsl.rb:13:in `evaluate'
	 5: from /usr/lib/ruby/vendor_ruby/bundler/dsl.rb:218:in `to_definition'
	 4: from /usr/lib/ruby/vendor_ruby/bundler/dsl.rb:218:in `new'
	 3: from /usr/lib/ruby/vendor_ruby/bundler/definition.rb:83:in `initialize'
	 2: from /usr/lib/ruby/vendor_ruby/bundler/definition.rb:83:in `new'
	 1: from /usr/lib/ruby/vendor_ruby/bundler/lockfile_parser.rb:95:in `initialize'
/usr/lib/ruby/vendor_ruby/bundler/lockfile_parser.rb:108:in `warn_for_outdated_bundler_version': You must use Bundler 2 or greater with this lockfile. (Bundler::LockfileError)
```

according to the reply by *DirtyF* in [this post](https://github.com/jekyll/jekyll/issues/7463)
These steps did the trick:
1. update Rubygems using `gem update --system`
2. update bundler using `gem install bundler`
3. update Gemfile.lock in your project using `bundler update --bundler`

Worked wonders!

## Adjust Gemfile and _config.yaml
Apparently the line `gem "github-pages", group: :jekyll_plugins` in the `Gemfile` is required to test on a local server. I suppose it installs the theme-files by itself.
Then point the `theme` to `minima` in the `_config.yaml` file

## Test and upload
To test locally: `bundle exec jekyll serve`
Otherwise upload(push) final product to github pages, in my case I used the `docs` folder in my github root (adjustable in project settings)
