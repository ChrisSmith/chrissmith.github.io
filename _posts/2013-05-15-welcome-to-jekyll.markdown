---
layout: post
title:  "An introduction to Jekyll"
date:   2013-05-15 23:54:52
categories: jekyll less javascript
---

So I've decided to start writing in hope that my ramblings may be of consolation to someone, even without resolution, at least I share your misery. 

Which brings me to Jekyll and blogs and blogging and setup and boilerplate and sane defaults and other nonsense that nobody has time for. Deciding to actually write something for the world to read is generally a pretty significant step for a mere moral like myself, but its also only the beginning of a rather tedious process that is 'setting up a blog.' Don't get me wrong there are a *lot* of options out there, and well, that's kinda the problem. Just off the top of my head: 
- Tumblr
- Wordpress
- Blogger
- Joomla
- Drupal
- Posterous
- Do it yourself 

Most of which I was able to find some fault with, the big CMS systems are *huge* complicated monstrosities with tons of 'features' I would never use, and like a DIY project I would need to setup and maintain a server for them to live on or fork over some cash for someone else to do it. Posterous was recently [acquired by Twitter](http://techcrunch.com/2013/02/15/posterous-will-shut-down-on-april-30th-co-founder-garry-tan-launches-posthaven-to-save-your-sites/), [Yahoo is buying up Tumblr](http://online.wsj.com/article/SB10001424127887324787004578493130789235150.html) and Google likes to [kill off products with no revenue stream](http://www.theverge.com/2013/3/13/4101144/google-shuts-down-reader-rss-aggregation-service) so basically the Internet is imploding and gosh darn it I better build myself a shelter.

## Enter Jekyll

A few things I like about Jekyll

- Generates content (html/css/js) which can be deployed and served statically 
- No database dependency
- You can still use templates and write code if necessary
- Posts can be written in [markdown](http://daringfireball.net/projects/markdown/)

Since Jekyll generates static html pages you can deploy your site however you like, common options being Amazon's S3 service, a Linux VM running Nginx/Apache or [Github Pages](http://pages.github.com/). For the time being I've chosen to use Github Pages, but I do have some reservations about using a third party service (especially a free one). Most of my concerns are about availability and performance and not so much as being locked into the platform, I'll write a post about it later. 


{% highlight bash %}
$ jekyll build
$ git commit -am "first post"
$ git push
$ echo "profit"
{% endhighlight %}

Learn more about [jekyll](http://jekyllrb.com)
