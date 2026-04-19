---
title: runevision blog
url: https://blog.runevision.com/2011_08_10_archive.html
published: '2011-08-10'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

I just upgraded from Firefox 3 to 5 and find that my blog is shown without a stylesheet at all. It still works fine in Firefox 3, and latest Chrome and Safari and I assume other browsers too. And the rest of my site still works fine in Firefox 5 too; it's only the blog part that's broken.

**Update:** It appears it was the stylesheet that was not recognized. I had my stylesheet inside an .asp file to be able to execute server-side code in it. That has always worked just fine but it appears to break when the browser is Firefox 5 AND the site linking to the stylesheet is on Google's Blogger service. When the same stylesheet is linked to from the part of my website that's hosted on my own server, it works fine. The stylesheet is hosted on my own server in both cases, so how it can make any difference where the html page is hosted I do not understand. In either case, baking the stylesheet into a static .css file and linking to that instead seems to have fixed the problem.