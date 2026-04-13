---
title: Posting items to my blog using wplatex
url: https://divisbyzero.com/2010/02/14/posting-items-to-my-blog-using-wplatex-2/
author: Dave Richeson
published: '2010-02-14'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

This blog post is aimed at other mathematicians who write on WordPress blogs.

I’m writing this blog post completely in TexShop on my Mac!

Recently I discovered that Eric Finster at [Curious Reasoning](http://curiousreasoning.wordpress.com/) wrote a Python script called wplatex that converts LaTeX documents to HTML that is WordPress compatible. Then it posts the files directly to your WordPress blog, complete with title, tags, and categories. From what I can tell, it is based on [LaTeX to WordPress (LaTeX2WP.sty)](http://lucatrevisan.wordpress.com/latex-to-wordpress/). For more information, look the following posts at the Curious Reasoning blog: [1](http://curiousreasoning.wordpress.com/2010/01/30/overview-of-wplatex-4/) – [2](http://curiousreasoning.wordpress.com/2010/01/28/more-on-blogging-in-latex/) – [3](http://curiousreasoning.wordpress.com/2010/01/22/blogging-screenshots/).

Once you get the various files installed, it is very easy to use. Write the LaTeX document as usual, using the document class *wpblogentry*. It compiles just like any other LaTeX document. Then, when you are ready to post it, navigate the the appropriate directory and type:

wplpost -u myloginname -b divisbyzero blogpost.tex (to post it immediately)

or

wplpost -u myloginname -b divisbyzero -d blogpost.tex (to post it as a draft)

Obviously, you should replace myloginname with your WordPress.com login name, divisbyzero by your blog name ([http://blogname.wordpress.com](http://blogname.wordpress.com)), and blogpost.tex with the name of your LaTeX file. When you do, it will prompt you for your WordPress password.

There are so many great things about this development. Ordinary LaTeX is so much easier to work with than WordPress LaTeX, so mathematically-intensive posts will be much quicker to write. I can copy-and-paste from my many LaTeX documents. I’ll have all of my blogposts stored locally on my computer in proper LaTeX. And if I ever decide to reuse any of my blog posts in another setting, it will be easy to do.

I look forward to exploring wplatex further.