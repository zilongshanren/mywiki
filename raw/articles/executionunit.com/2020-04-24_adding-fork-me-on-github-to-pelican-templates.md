---
title: Adding “Fork Me on Github” to Pelican Templates
url: https://www.executionunit.com/blog/2020/04/24/adding-fork-me-on-github-to-pelican-templates/
published: '2020-04-24'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I just wrote a blog about a project I uploaded to GitHub and I wanted to have a “Fork Me On GitHub ribbon” in the top right of the page. This is the cool thing to do nowadays after all.

I write my blog using a static website generator called [Pelican](https://blog.getpelican.com/). One of the advantages of Pelican is that
the templates used to generate the static site are easily modifiable. Here
is what I did.

Firstly I found someone who had done the dirty work of creating a CSS
[ribbon](https://simonwhitaker.github.io/github-fork-ribbon-css/),
Thank you Simon. For Simon’s ribbon to appear I needed to add one CSS
file and an anchor to any page with a GitHub link in it.

Adding metadata to articles in Pelican is very easy. For any article
that needed a GitHub ribbon I add some metadata named `githuburl`

. Here
is the meta data for my article:

1 2 3 4 5 6 |
|

So now when processing an article and generating HTML the article object will have a member called githuburl.

The blogposts are rendered using the `article.html`

template. I added

1 2 3 4 5 |
|

to the top and at the bottom.

1 2 3 4 5 |
|

This code creates two new blocks and if `article.githuburl`

has a value
the `extracss`

block will contain the CSS `link`

and the `endbody`

block
will contain the link to the GitHub page.

To make these blocks rendering in to the output HTML I need to tell the
template engine where to put them. So I modified `base.html`

which all
templates inherit from.

1 2 3 4 5 6 7 8 9 |
|

After that I rebuilt my site and now I can have a little GitHub ribbon on any page just by adding some meta data to an article. Pretty cool.

[You can see the article here](https://www.executionunit.com/blog/2020/04/24/csgjs-cpp-on-github/) complete with
a lovely GitHub ribbon.

I hope that makes sense.

dazza.

## Comments