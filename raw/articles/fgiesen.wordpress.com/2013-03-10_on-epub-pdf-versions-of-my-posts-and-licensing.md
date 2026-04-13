---
title: On ePub/PDF versions of my posts and licensing
url: https://fgiesen.wordpress.com/2013/03/10/on-epubpdf-versions-of-my-posts-and-licensing/
published: '2013-03-10'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# On ePub/PDF versions of my posts and licensing

I’ve been asked several times about this, so I wanted to make an “official” statement:

No, I will not prepare ePub/PDF (“book”) versions of posts, particularly the “[A trip through the Graphics Pipeline 2011](https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/)” and “[Optimizing Software Occlusion Culling](https://fgiesen.wordpress.com/2013/02/17/optimizing-sw-occlusion-culling-index/)” series. However, should someone be willing to prepare such a thing, I’d be very happy to provide them with a WordPress extended RSS dump of the site contents (with your comments and all other emails / personal data removed, don’t worry) and host the results. If you’re interested in helping, please write a comment with a valid email address and I’ll get in touch with you.

To clarify the legal situation, I have put both these series into the public domain (using the CC-0 “license” waiver). *This means you may do with these posts whatever you want*. You may edit them, update them or add additional information; you may turn them into an eBook, PDF, or hardcopy book; you may use it as a starting point for a graphics pipeline Wiki, if you are so inclined – I don’t have the energy or web development chops to set that kind of thing up, but I’d be happy to contribute to it if it existed! You may also claim that you wrote them yourself, sell it to a publisher for a million bucks, and invest the proceeds in land mines you bury in a public park. I would rather that you not do these things, but it boils down to this: if you were to do it, would I want to make the whole affair even more unpleasant for myself than it would already be by engaging in complicated and expensive legal proceedings? And my answer to that question is a clear “no”.

In fact, my reasons for not preparing eBook versions and for releasing the texts in the public domain are basically the same: I enjoy writing these posts, and I enjoy seeing people read them. I do not enjoy wrestling with publication formats or blogging frameworks, and I certainly don’t enjoy dealing with legal issues. The reason I can manage to write a few thousand words of technical content a week despite having a full-time job is because I’ve structured the experience to be as enjoyable and low-friction for me as possible. Last year, I tried editing the “A trip through the Graphics Pipeline 2011” series into a book format, and progress was excruciatingly slow, because ultimately it was not a fun task for me; it felt like an unpaid part-time job, so at some point I just stopped.

So this is the deal: I’m a professional software developer that happens to like writing. But the writing is a pure “bonus”; I do it because I enjoy it, but only as long as it’s on my terms – I write what I feel like writing, on whatever schedule pleases me, and without any additional process beyond hitting “Publish” once I’m done. I’ll be happy to help anyone who wants to do more than that, but I’m not going to do it myself.

Hello,

I really enjoyed reading the trip down the graphics pipeline back then and I would love to see a pdf version of it. It would be a good start for students to dive into the details of graphics hardware but for that I would prefer one document with a complete list of sources and citations, some more graphics etc. Some parts might get an update (e.g. OpenGL 4.3 also has compute shaders now) but to get an overview of what exactly I would have to re-read the posts first ;-)

I have to confess that I didn’t read the software occlusion culling series yet but I guess that some parts of it might also help understanding the rasterization process and might be merged into the pipeline-series.

It will be quite some work but I’m willing to participate and I’m also open for ideas of what to add to it.

Well I did start this: trip_gfx repository it’s just a start though, but hey, pull requests welcome! :)

Well, I guess the problem is the minimum quality you’re expecting from the edit… I’ve made a quick test with “anthologize” pdf export, and got those two docs:

https://docs.google.com/file/d/0BxcU4v5PTg5pUXZIVkloWGJacTQ/edit?usp=sharing

https://docs.google.com/file/d/0BxcU4v5PTg5pTUZ4OVE3aWhHTGc/edit?usp=sharing

Seems to keep most formatting details, and graphics.

Have to proof read it in more details, for now, the only problem are the “fomula does not parse” pdf bug.

Looks OK to me, but there’s definitely some problems; e.g. the occlusion culling one has some missing code and subsequent parsing errors on page 86. How’d you make this?

It’s http://wordpress.org/extend/plugins/anthologize/ / https://github.com/chnm/anthologize plugin on a local wordpress copy of your blog.

Only pdf export gave results, but anyway “calibre” ( http://calibre-ebook.com/ ) can convert to any other ebook format perfectly from that pdf. (tried here and got nice results on a sony ereader). So really just a publish button but the parsing errors.

“You may also claim that you wrote them yourself, sell it to a publisher for a million bucks, and invest the proceeds in land mines you bury in a public park. I would rather that you not do these things […]” well said,I personal;y enjoyed your “Optimizing Software Occlusion” series and are simply grateful that such interesting and insightful writing is available.

Keep up the good work!

For me the important thing is the idea and I find the blog format completely adequate. If you don’t enjoy the tedium of editing into other form don’t bother, I would father rather you continued with what you enjoy. Thanks as always for sharing.

Nice to know about VeryPDF software. It seems quite interesting and useful for

PDF to ePub conversion. I was looking for software like this for long time. That’s a good feature of this software that it keeps all the original text, layout tables and images are retains in ePub file.Admiring the dedication you put into your website and in depth information you provide.

It’s good to come across a blog every once in a while that isn’t the same old rehashed

material. Great read! I’ve saved your site and I’m including your RSS feeds to my Google

account.