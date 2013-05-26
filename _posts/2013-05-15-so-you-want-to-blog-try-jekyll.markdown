---
layout: post
title:  "So you want to blog, try Jekyll!"
date:   2013-05-15 23:54:52
tags: jekyll less javascript
---

So I've decided to start writing in hope that my ramblings may serve some utility to someone, and this is the meta post that describes how this blog come into existence. Deciding to actually write something that the world could read is a pretty significant step for a introvert like myself, but its only the beginning of the rather tedious process that is 'setting up a blog.' Don't get me wrong, there are a **ton** of options out there, and well, that's kinda the problem. Just off the top of my head: 

- Tumblr
- Wordpress
- Blogger
- Joomla
- Drupal
- Posterous
- DIY Random linux box hosted someplace

Many of which I picked some fault with and decided I couldn't use. The big CMS systems are **huge** complicated monstrosities with tons of 'features' I would never use, and like a DIY project I would need to setup and maintain a server or fork over some cash for someone else to do it for me. On the services side of blogging: Posterous was recently [acquired by Twitter](http://techcrunch.com/2013/02/15/posterous-will-shut-down-on-april-30th-co-founder-garry-tan-launches-posthaven-to-save-your-sites/), Yahoo is [buying up Tumblr](http://online.wsj.com/article/SB10001424127887324787004578493130789235150.html) and Google has been [killing off products with no revenue stream](http://www.theverge.com/2013/3/13/4101144/google-shuts-down-reader-rss-aggregation-service) so basically the Internet is imploding and gosh darn it I better build myself a shelter. No way am I spending valuable time composing my thoughts into something cohesive only to have them fade into the ether in a few years when your hot awesome startup gets aquihired (because let's face it, your team is better than your business model). 

## Enter Jekyll

Convinced I shouldn't rely on an external service and refused to write plain html, I took a closer look at Jekyll. 

- Posts are written in a simple format, I chose [markdown](http://daringfireball.net/projects/markdown/)
- Template based reuse 
- html/css/js is generated at 'build' time
- No database dependency
- Additional functionality via plugins (ruby code)

Since Jekyll generates static html pages you can host your site however you like, typically either Amazon's S3 service, a Linux VM running Nginx/Apache or [Github Pages](http://pages.github.com/). For the time being I've chosen Github Pages, but I do have some reservations about using a third party service; mostly availability of the site and page performance. However, given that Jekyll only generates static pages and is not necessary to serve the website, I'm happy to make these compromises until they're a real problem and I'm forced to administer my own server.

The build process is completely painless and you can even setup a continuous build that runs everytime a file changes; this is the --watch flag. **jekyll build** to build the site only, or **jekyll serve --watch** to run the site on localhost (via WEBrick). Jekyll alone doesn't handle any css preprocessors or javascript compilers so you'll want to find or write a suitable plugin that handles your assets. I tried a few but the one I setted on is [jekyll_asset_pipeline](https://github.com/ryanaghdam/jekyll-asset-pipeline) and does everything I need right now: javascript minification, less preprocessing and asset bundling. In addition to asset management there are other things to consider plugins for like sitemaps and localization, there is a list of some in the [jekyll docs](http://jekyllrb.com/docs/plugins/).


Learn more about [jekyll](http://jekyllrb.com), its really awesome!

{% highlight bash %}
$ jekyll build 
$ git commit -am "first post"
$ git push
$ echo "profit"
{% endhighlight %}

