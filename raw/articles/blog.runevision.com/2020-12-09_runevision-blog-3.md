---
title: runevision blog
url: https://blog.runevision.com/2020_12_09_archive.html
published: '2020-12-09'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

You can skip to the header below for the actual guide. Or stay here for a rambling preamble.

I'm a skilled programmer, but I'm not a technical person. I'm not *good with computers*. Or at least I highly prefer if things just work, and I don't have to fiddle with settings and configurations.

This is one reason I strongly prefer Mercurial for source control over Git. It has a higher degree of just working. (I don't want to get into an argument over this. You can question my assertion, but my preference is my preference in any case.)

Unfortunately Mercurial has become a niche choice as Git has achieved overwhelming popularity, largely due to GitHub. I wouldn't really have cared about that, except it made BitBucket close down their support for Mercurial some time ago. And BitBucket was a hosting solution for Mercurial that was affordable and also *just worked*.

I and many other Mercurial lovers have then had to find alternative hosting. And I ended up with choosing [SourceHut](https://sourcehut.org/). SourceHut is the opposite of "it just works". It's made for people who identify with hacking and tinkering and knowing all the technical stuff. Why did I choose it then? The "just works" alternatives had pricing that just did not work for a game development use case.

Now, SourceHut has been a pain to use in *many* ways for a non-technical person like me, but I've had the most pain at all trying to get SSH authentication to work. Unlike BitBucket, SourceHut does not allow HTTPS authentication, so you have to use SSH, and nobody ever sat down and made SSH easy to use on Windows.

Getting SSH to work involved juggling things like multiple types of SSH keys and formats all placed in a hidden folder, many different helper tools, and reading dozens of half-baked how-to guides that all contradict each other, often assume prior knowledge, and that are all for slightly different use cases which means they didn't quite work for me.

I got it all to work around a year ago, but I recently wiped my hard drive and needed to do it all over. I couldn't remember anything, so had to figure it all out all over again. So now I'm writing my *own* half-baked guide, mostly for my future self in case I need it again, but others might stumble over it and maybe find it useful too I guess.

When you read this guide, you might think it doesn't sound that complicated after all. But remember the guide omits all the things I read I should do and which I thus attempted, but it didn't work, and eventually turned out not to be needed anyway. Like running the main PuTTy application, or running tortoiseplink, or editing your mercurial.ini file. Anyway, on to the guide.