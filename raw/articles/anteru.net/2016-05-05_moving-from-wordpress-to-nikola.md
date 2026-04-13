---
title: Moving from Wordpress to Nikola
url: https://anteru.net/blog/2016/moving-from-wordpress-to-nikola
published: '2016-05-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you’re a regular reader, you will have noticed that this blog looks remarkably different since today. What happened? Well, I moved the blog from [Wordpress](https://wordpress.org) to a static page generator – [Nikola](https://getnikola.com). That might come as a surprise as I’ve been using Wordpress for 11 years now, so let’s dig into the reasons.

## Quo vadis, Wordpress?

The most important one for me is that I often add code snippets into my blog posts, and the experience of adding code to Wordpress is horrible. I ended up writing my own plugin for Wordpress to teach it code highlighting the way I wanted, but even then, moving between the “visual” and the “text” editor would mess up source formatting. Also, I would frequently run into HTML escaping problems, where my code would end up being full of `>`

.

The other issue I had is backing up my blog. Sure, there’s the Export as XML function, which does work, but it doesn’t backup your images and so on, so you need to grab a dump of the `wp-content`

folder in addition to the XML export. I’m not sure how many of you do this regularly – for me it was just a hassle.

Next up is theming. Wordpress used to be an easy to theme system when I started – but over time, making a theme became more and more complicated. With any update, Wordpress would add minor tweaks which required upgrading the theme again. Eventually, I ended up using the sub-theming capabilities, but even then, theme development in Wordpress remained complicated. My “solution” was a local docker installation of Wordpress and MySQL. That worked, but it was not very comfortable to use. Frankly, at that point, I lost all motivation to do theme related changes.

The final nail in the coffin were encoding issues which left a lot of my posts with `â€œ`

and other funny errors. Fixing this in Wordpress turned out to be a huge pain, especially as there is no easy way to bulk-process your posts, or for the matter, do anything with your posts.

Not everything is bad with Wordpress though. The visual editor is pretty slick, and when you stick to the WSYIWYG part of Wordpress, it is actually an awesome tool. It’s just failing short on **my** use cases, and judging from the last years of development, it’s moving further away into a direction which has very little value add for me. Recently, they added for instance another REST based web-editor, so you have now two visual editors for Wordpress. Unfortunately, source code is still not a “solved” issue, as is authoring files in something else than HTML.

## Going static

All of those problems became big enough over time to make me bite the bullet and go to a static page generator. I do like static page generation – having even written my own static page generator a couple of years back. What I didn’t want to do though is to write an importer for Wordpress, deal with auto-updating, theming, and so on, so I looked for a static page generator which would suite me. I’m partial to reStructuredText, and Python, so I ended up with Nikola, which is a Python based static page generator with first-class support for reStructuredText.

It comes with an `import_wordpress`

command, which seemed easy enough, but it turns out you need a bit more post-processing before you can call it a day. Let’s start with the importing!

### Import & cleanup

Ingesting everything through `import_wordpress`

will give you the content as HTML. Even though the files are called `.md`

, they just contain plain HTML (which is valid Markdown …). To convert them to “proper” Markdown, I used [pandoc](http://pandoc.org):

```
find . -name *.md | xargs -I {} pandoc --from html --to markdown_strict {} -o {}
```


That cleanups up most of it, but you’ll end up with weird source code. My source code was marked up with `[source lang=""]`

, so I had to go through all files with source code and fix them up manually. Sounds like a lot of work, but it’s usually quite straightforward as you can just copy & paste from your existing page.

In retrospective, converting everything to reStructuredText might have been a better solution, but frankly, I don’t care too much about the “old” content. For new content, I’m using reStructuredText, for old content – I don’t care.

### Redirections

Next up is redirecting your whole blog so your old links continue to work. I like to have “pretty” urls, that is, for a post named `/my-awesome-post`

, I want an URL like `/blog/my-awesome-post`

. This means there has to be a `/blog/my-awesome-post/index.html`

page. By default, the imports will be however `/posts/my-awesome-post.html`

. In order to solve this, you need to do two things:

- Turn on pretty URLs using:
`PRETTY_URLS = True`

- Fix up the redirection table, which is stored in
`REDIRECTIONS`

in`conf.py`


To fix the redirections table, I used a small Python script to make sure that old URLs like `/my-awesome-post`

were redirected to `/blog/my-awesome-post`

– I also used the chance to move all blog posts to a `/blog`

subdirectory. Nikola will then generate `/my-awesome-post/index.html`

with a redirection to the new URL.

### Comments

Finally, the comments - I had a couple hundred in Wordpress, and Nikola, being a static page generator, doesn’t have any idea of comments. The solution here is to import them to [Disqus](https://disqus.com) which is straightforward. First, you create an account at Disqus, install the Disqus Wordpress plugin, and import your comments into Disqus. Be aware: This will take a while. Finally, you need to teach Disqus the new URLs. This is done using an URL remapping, which is a simple CSV file that contains the original URL and the new one. Again, same exercise as above – you’ll probably want to reuse the `REDIRECTIONS`

for this and dump it out into a CSV.

## Closing remarks

Voilà, there you go – you’ve ported your blog from Wordpress to Nikola. The remaining steps you’ll want to do:

- Set up some revision control for your blog. I just imported it wholesale into
[Mercurial](https://mercurial-scm.org)with the`largefiles`

extension to store all attachments. Backups: Check! - Set up a
`rsync`

to upload the blog. By its nature, Nikola generates all files, and you need to synchronize – some scripting will be handy for this. - Fix up all URLs to use
`/`

as the prefix. I just did a search-and-replace for everything`https://anteru.net/`

which didn’t continue with`wp-content`

, redirected that to`/blog/`

, and then fixed up the`/wp-content`

ones.

That’s it – let’s see if Nikola will serve me for the next 11 years, just like Wordpress did :)