---
title: 20 years of blogging
url: https://anteru.net/blog/2025/20-years-of-blogging
published: '2025-01-13'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Time flies, as people say, and this blog has been around now for **twenty** years. Trying to do a retrospective on the past twenty years turns out to be actually much harder than anticipated - I’ll get to the *technical* details in a minute, but the primary bottleneck here is my own memory. Which is funny considering this blog is somewhat a diary, but it’s missing the context as to why something was written, and how I did go about it. You only see the finished product. It’s an interesting exercise to try to figure out a certain trend tens years later - kind of like being the detective and the murderer at the same time.

## Non-tech

That said, the motivation as to why I’m blogging did definitely change over the years, and it’s not hard to see how and why. At the beginning, I’ve used my blog for personal “status updates” and what I thought were interesting news. Mind you, this was the time before social media was taking off and before there were more convenient ways to share “small news”. These days, you get enough “news” that I don’t feel there’s any value add from me posting about them. As for personal stuff – it’s hard to have any kind of privacy these days even when not being on social media directly as you still get indirectly tagged, photographed, and what not. So personal updates also got sparse over time until they dried up completely.

I also used to have comments enabled back in the day so I could have some kind of relationship with my readership, but turns out, that never was a thing. It was fairly clear to me early on (while I still had stats running) that nobody was reading the blog because of me, but because of technical content that they found via a search engine. Would have things gone differently if I had seen more engagement? I can’t tell. I was never looking for much praise or approval from my audience, so it’s really not clear to me in hindsight that the blog would me markedly different had I seen a community form around it.

The other major trend is that I’ve become much more deliberate in what I’m posting about; or, one could say, professional? I would always proof-read a blog post, so that’s not it, but I wouldn’t always set up a list of “goals” I want to get across in a blog post. The bar to post went up a lot - which may have prevented a few “good enough” blog posts from coming out, but hopefully also resulted in a much better reading experience. Some more technical blog posts in recent years have definitely done extremely well as a result.

One experiment I did a few times was to write a blog series, like the series about build systems, or the advent series. While this definitely does help to get a lot more content written than usual, it’s also fairly time-consuming. I don’t know if the series will have much of a future as a result.

## Tech

Technology wise, I used Wordpress for around half of the duration of this blog, and I got increasingly frustrated with it. After a brief stint using Nikola I ended up with my own static page generator – actually the successor to the tool I wrote for the website of a small company. Looking back, I do regret that I didn’t carefully track the state of the blog over the years; there are a few theme changes I don’t recall at all that I can’t reproduce, and much of the Wordpress configuration was a “live installation” with no backup and no version control. Since switching to a static page generator things are much better, I can reasonably reconstruct the state of my blog in the last couple of years, but not having an archive of theme screenshots that I can review is kind of a bummer in retrospective. Not to mention it also means I always looked at the last and the current design when doing things; not at “how did I end up with this in the first place” as the history was lost.

The stack today is incredibly simple. A web server hosting static files, a repository holding the blog content, and a `cron`

job (actually, a `systemd`

timer) which deploys the blog once every hour (if changed) to said server. This has served me reliably for a few years now, with I think less than 15 minutes of total maintenance needed. Very much the kind of system I like to have, especially as I want to keep the overhead of writing/maintaining this blog to a minimum so I use all the time I spend on this blog on adding content.

## Other thoughts

With all that said, where is this going? Spare time to blog has definitely been in decline, but I try to use this blog to “not repeat myself” and write down things I end up looking up every time I need them (like, how to write a `systemd`

timer.) At the same time, I’m fairly disappointed by the fact that “AI companies” suck up the knowledge and insights from blogs like the very one you’re reading and serve it to their customers, bypassing the source. The original deal when I started blogging was that a search engine would point you at it, you would read it, and form your opinion yourself, seeing the full unaltered blog post with my references as you read it. These days, you get a potentially incorrect summary, without attribution, and you can’t figure out where the information came from. Even if it gets attributed, there’s no guarantee the summary you see is correct, in which case you may think that I made the mistakes the large language model added – and there’s no way for me to step in and correct it.

This is definitely one factor which discourages me from blogging. I’m sure in the “big scheme of things” me blogging less or more is not going to help the overall situation, but it’s one of those things “out there” that quietly causes harm even if you don’t actually see the harm being done. That said, I still reference my blog myself, so I’ll keep using it as a notepad for *my* problems.

One last thought before I wrap this up: Link stability on the internet! I’ve been going to great lengths to make sure my blog has stable links; with hundreds of redirections in place to make sure old Wordpress-style links work (before I switched to slug-like links.) I’m also regularly running a script to make sure that outgoing links work, and sadly, the stories about “the internet never forgets” are quite exaggerated. A lot of links are gone, and despite me trying sometimes quite hard to find the referenced document, things are really gone. It’s actually quite surprising how much “stuff” is no longer available after 5, let alone 10 years on the internet. I haven’t found a good way to prevent this – I guess trying to get the link into archive.org is one way, but it won’t work for software where even if you would find the download link, it’s no longer supported, the activation server is down, or whatever. Certainly not surprising, but disappointing that a lot of our “digital heritage” is just disappearing.

So, what does the future hold? I’m not sure. Hopefully a few more blog posts about technical things, if I find the time to figure out some things 😀