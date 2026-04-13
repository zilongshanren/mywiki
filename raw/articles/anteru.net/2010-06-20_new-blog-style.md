---
title: New blog style
url: https://anteru.net/blog/2010/new-blog-style
published: '2010-06-20'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m working a new blog style. Please report any problems you encounter!

![](../../assets/21daa260985d2b8f.png)

Right now, there are some issues with Opera and Chrome, while Firefox 3.6 works correctly. For the best viewing experience, please try Firefox for the time being while I iron out the issues with Chrome/Opera. **Update**:I think I’ve fixed the issues with Chrome.[/**Update**]

![](../../assets/0064f763be2d9407.png)

The theme uses CSS3 for all shadows (specifically, [text-shadow](http://www.w3.org/TR/css3-text/#text-shadow) and [box-shadow](http://www.w3.org/TR/css3-background/#the-box-shadow) is used.) This keeps the load time pretty low and still provides some very nice effects. The menu uses the [:last-child](http://www.w3.org/TR/css3-selectors/#last-child-pseudo) selector, and thus does not work with Internet Explorers before IE9. Overall, it’s a pretty tiny theme, as I finally got round to create it as a [child theme](http://codex.wordpress.org/Child_Themes) instead of rebuilding most from scratch. The parent theme used here is [twentyten](http://2010dev.wordpress.com/) ([Wordpress 3.0](http://wordpress.org) default.)