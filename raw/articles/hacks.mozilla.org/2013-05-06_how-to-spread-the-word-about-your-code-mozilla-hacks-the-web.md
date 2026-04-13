---
title: How to Spread The Word About Your Code – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/05/how-to-spread-the-word-about-your-code/
author: Peter Cooper
published: '2013-05-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You spent an entire weekend building a library, jQuery plugin, build tool, or other great piece of code you wanted to share far and wide, but after some tweets and a failed attempt to make the front page of [Hacker News](https://news.ycombinator.com/), your creation languished, unloved, in a GitHub repo. A common situation for many developers nowadays, but one you can avoid.

As the editor of several programming newsletters, I frequently get two types of e-mails from developers. Those reaching out to ask if I can mention their projects, and those expressing surprise and excitement that their work has been featured. If you’re a developer doing good work but feel more like you’d be in that second group, the three steps in this article are for you.

Before we get started, there’s a stumbling block we need to kick away. Terms like ‘marketing’ and ‘advertising’ are dirty words for many developers and it’s not uncommon for developers to be reluctant to do much promotion. ‘Build it and they will come’ used to work when exciting open source projects were few and far between but now everyone seems to be working on something and making a noise about it. Few of the successes you see come through pure luck but because developers are actively promoting their work or, at least, making it *discoverable*. It’s time to join them!

## Step 1: Get your project ready

Before you can promote your project, you need to make it attractive to potential users and evangelists (including general wellwishers, the media, and other developers).

### A good name

Ensure your project has a palatable name. It doesn’t need to be clever or even descriptive, but it’s worth avoiding innuendos that may present a problem down the line. For example, the popular Testacular and Authgasm projects, are now named [Karma](https://github.com/karma-runner) and [Authlogic](https://github.com/binarylogic/authlogic) respectively after users raised a fuss.

You should perform a search for the name you choose to be sure you’re not clashing with anything else that’s popular or trademarked (did you know [Firefox was called](http://en.wikipedia.org/wiki/History_of_Firefox#Naming) *Phoenix* and *Firebird* prior to *Firefox*?). The US Patent and Trademark Office [has an online trademark search facility](http://tess2.uspto.gov/).

A benefit of having a relatively unique or uncommon name is so you can search for it over time (or even set up a [Google Alerts](http://www.google.co.uk/alerts) notification for the name) and find mentions of your project without many irrelevant results popping up. If you want to have something descriptive but unique, consider joining two words together. For example, when I created a Ruby library to do natural language detection, I called it *WhatLanguage* and it’s easy to search for.

### An official homepage or project URL

The term ‘homepage’ is a bit outdated but you ideally need a single ‘home’ URL that you can promote and point people to in relation to your project. You don’t need to splash out on a fancy template or even a domain name, but your project needs a focal point. That could be an entire site with its own domain, such as those for [Yeoman](http://yeoman.io/) or [HTML5 Boilerplate](http://html5boilerplate.com/), a simple single page on an existing domain, such as that for [RoughDraft.js](http://ndreckshage.github.io/roughdraft.js/), or even a regular GitHub repo, such as for [vague.js](https://github.com/GianlucaGuarini/vague.js).

If you have the freedom to do so, make sure your site looks good on the major browsers (including mobile), hook up some analytics to your page and ensure the <title> tag is well written. Use a title like *“MyProject – A JavaScript Library to X, Y and Z”* instead of just *“MyProject – About”* or a blank title. With social bookmarking, this matters as you can’t guarantee your evangelists will write a good title of their own.

If you’re not a Web designer, don’t have the time to spend making a complete design, but still want a complete site rather than just a GitHub repo and README, consider using a framework like [Bootstrap](http://twitter.github.io/bootstrap/) as it’ll provide a clean layout out of the box and you can forget about many cross browser and device issues.

### Documentation and copywriting

It’s only *just* a cliché that developers don’t like to write documentation, but you need *something* for potential users to fall back on, and time invested in producing useful documentation up front will pay dividends later.

At a cynically bare minimum, you need to write enough documentation that someone will be confident about sharing your link or promoting your project and not feel like they’re sending their own followers into a black hole of misunderstanding. This means your homepage or README needs to cover a few angles. You’ll need to:

-
**Prominently feature a “[noun] is” paragraph.**An alarming number of project homepages don’t explain, in simple terms, what the project is actually for or does. If you’ve built a JavaScript library that does language detection, say, you have to say so. For example:*“LanguageDetect is a JavaScript library for detecting the natural language of text.”*An excellent example of this in action is on

[libcinder.org](http://libcinder.org/)where it states right up front:*“Cinder is a community-developed, free and open source library for professional-quality creative coding in C++.”*Perfect! -
**Write clear titles, subheadings, and support copy.**At a bare minimum, ensure titles, subtitles, and*any*sort of writing on your homepage are straightforward and clear. Write for the lowest common denominator on your homepage. You can get more advanced elsewhere. -
**Write a beginner’s tutorial and link to it from your home page.**Unless everything’s simple enough to explain on a single page, quickly write a tutorial that covers basic installation and usage and either include it in your README file or put it on the Web and link to it from your README and/or homepage. -
**State dependencies and requirements clearly.**Does your library only work on a specific version of Node? Is it a browser extension for Firefox? Does your code require PostgreSQL, Redis, or another specific database? Be sure to include a bulletpoint list of dependencies and requirements for your project to be usable so as not to disappoint potential users. -
**Specify the license for your code.**While you*could*get away with keeping your licensing information tucked away in a LICENSE file in your GitHub repo, specifying what license your code is released under up front and center will help put many developers at ease. Likewise, if your project is commercial is nature and costs money, don’t hide that detail away and mislead visitors. -
**If your project is a library or API, feature some example code on the homepage.**Unless your library is particularly complex, let visitors see an example of its usage on the project homepage. If your API is good, this could be a great way to get an ‘easy sale.’ I’m not a huge fan of the code example chosen but the[homepage for Ruby](http://www.ruby-lang.org/en/)shows off this technique.

### Extra materials

A blog post is a great way to introduce a project that might need more background or have more of a story than it’s practical to tell on a homepage or within documentation. If there’s any sort of story behind your project, a blog post is a great way to tell it. Be sure to link to the post from your project’s homepage and consider promoting the blog post separately to relevant sites within your niche.

If you have the ability, recording a screencast or other sort of video can help. Could you put together a simple 5 minute screencast of how to install and use your library? Or have you built a game that could be demonstrated in a few minutes of gameplay? Record a simple video, put it on YouTube, and embed it on your homepage. Your accent *doesn’t* have to be as crisp as a newsreader’s and you don’t even have to appear within the video. All that matters is you get to the point quickly and your audio is tolerable (not muffled, clipping, or drowned in background music).

As the editor of several programming newsletters, I look at thousands of projects each year, and it’s still uncommon to see simple screencasts, yet they certainly help a project stand out and, as a consequence, make it more likely for me to talk about it. You can see a perfect example on [Punch’s homepage](http://laktek.github.io/punch/). The early popularity of Ruby on Rails also depended upon a popular ‘build a blog engine in 15 minutes’ video, back when the concept of using video to promote an open source project was very novel.

If you’re sticking to the straight up, GitHub README approach (and it’s certainly not a bad idea for a simple library), a bonus tip is to create a tiny screencast of your code in action and convert it to an animated GIF for inclusion in your README. Richard Schneeman outlines this technique in [Use GIFs in your Pull Request for Good, not Evil](http://schneems.com/post/41104255619/use-gifs-in-your-pull-request-for-good-not-evil). The result is striking and could help your README stand out.

For further ideas on how to make your project stand out before you begin promoting it, check out the great [How to Make Your Open Source Project Really Awesome](http://blog.clojurewerkz.org/blog/2013/04/20/how-to-make-your-open-source-project-really-awesome/) by Michael Klishin. It digs into more detail about versioning, announcements, having a changelog and writing good documentation.

## Step 2: Get the word out

You’ve polished your project, got a URL to promote, and you’re ready to get the news out.

A word of caution, however. Don’t use every technique on day one. You could overload your site with traffic or, worse, be subjected to a barrage of online criticism if your work or site is broken. With something like a library or tool, a gentler approach will work well and building up small streams of visitors and users over time will give you a much better time.

### Social networking

Your own social networking profiles are always a good place to start if you have them. You’ll get more immediate feedback from people who actually know you and if your project is particularly interesting, it could go viral even from a single mention.

A great example of a simple project going viral was [YouTube Instant](http://en.wikipedia.org/wiki/YouTube_Instant) by Feross Aboukhadijeh. Feross built YouTube Instant quickly, mentioned it on Facebook before going to bed, and [woke up to a flood](https://github.com/feross/feross.org/blob/master/_posts/2010-09-11-youtube-instant-media-frenzy.md) of traffic and press mentions.

If you like to experiment and have several bucks going spare, you could also consider paying for a [promoted post](https://www.facebook.com/help/promote) on Facebook. This will give your post more visibility in your news feed, but is best reserved for if your Facebook friends are mostly developers or people likely to be interested in your project. If not, and you’d still like to spend some money, consider an ad on Reddit or a relevant programming blog instead.

### Influencers, bloggers, and niche media

Whether you’re working on a JavaScript library, Firefox extension, backend app in Rails, or a theme for Bootstrap, your code will fit into one or more niches and every technical niche has a variety of ‘influencers’, people and publications who are popular and well known for the topic at hand.

Getting a tweet, retweet, or even an entire blog post from an influencer could have a significant impact on your project, as could being invited to blog elsewhere (Mozilla Hacks, for example!). If Brendan Eich tweeted about your JavaScript library, Lea Verou wrote a blog post about a CSS trick you discovered, or Paul Irish mentioned a Web development tool you built in a talk, you would attract a lot of interest quickly. It is key, however, to realize there are many great influencers in every space and you’ll achieve nothing by hounding any one person so be prepared to move on.

Spend some time working out who the influencers and key publications are in your niche. For Twitter, [Followerwonk](http://followerwonk.com/bio/) is a handy tool that searches Twitter biographies for certain words. If you search for *“javascript”* the first page includes several users who would be useful to reach out to if you had a particularly interesting JavaScript-related release to promote. Reaching out on Twitter can be as simple as a single tweet and many busy folks prefer Twitter as it takes less time to reply than an e-mail. A single tweet from [@smashingmag](https://twitter.com/smashingmag) could drive thousands of visitors your way, so consider tweeting them, and other similar accounts, when you have something relevant.

I’d also advise looking for blogs and e-mail newsletters in your niche. Start with something as simple as Googling for *“javascript blog”*, *“javascript newsletter”*, *“css blog”* or whatever’s relevant to your project. Most bloggers or e-mail newsletter publishers will not be offended by you sending them a quick note (emphasis on *quick*) letting them know about your work. Indeed, some weeks there can be a shortage of interesting things to write about and you might be doing them a huge favor.

If you choose to e-mail people (and your project will probably be more substantial than a few hours’ work to justify this), take care not to make demands or to even expect a reply. Many bloggers and influential people have overflowing inboxes and struggle to reply to everything they receive. Make your e-mail as easy to process as possible by including a single URL (to your now superb homepage or README) and include your *“[noun] is”* paragraph. Don’t take a non-response as an insult but keep moving on to the next most relevant person. You might even consider taking a *“Here’s my project that does X, Y and Z. No reply needed, I just thought you might like it”* approach. Softly, softly works here, as long as you get to the point quickly.

[How to get attention from internet celebrities](http://blog.asmartbear.com/email-pick-brain.html) by Jason Cohen and [How to Write the Perfect Outreach Email](http://www.sparringmind.com/perfect-email/) by Gregory Ciotti go into more detail about e-mail etiquette when promoting your work to influencers. While you might not need to contact any ‘celebrities’ in your niche, the principles of keeping it short, including a call to action, and ensuring your work is appropriate to the person are really true for anyone you’re sending unsolicited messages to.

Podcasters are an often forgotten source of promotion opportunities too. While some podcasts don’t cover news or new releases at all, many do, and being on the radar of their hosts could help you get a mention on a show. Smashing Magazine has [put together a list of tech podcasts](http://www.smashingmagazine.com/2013/04/19/podcasts-for-designers-developers/) covering the areas of design, user experience, and Web development in general. Again, keep your e-mails short and sweet with no sense of expectation to get the best results.

### User curated social news sites

As well as reaching influencers and niche media, sometimes reaching the public ‘firehose’ of news can work too, and there are few better examples of these in the modern world of development than [Hacker News](https://news.ycombinator.com/) or [Reddit](http://www.reddit.com/).

Hacker News in particular is notoriously hard to reach the front page on and ‘gaming’ it by getting other people to vote up your post can backfire. (Indeed, it will backfire if you link people to your post on Hacker News and encourage them to upvote. They have ways of detecting this behavior. Get people to manually find your post instead.) If you do reach the front page of Hacker News, of course, you can certainly expect an audience of many thousands of developers to be exposed to your work, so be sure to try.

With Reddit, the key isn’t to dive straight into a huge sub-Reddit like [/r/programming](http://www.reddit.com/r/programming) but to look for sub-Reddits more directly related to your project. For a JavaScript library, I’d post to [/r/javascript](http://www.reddit.com/r/javascript) or possibly [/r/webdev](http://www.reddit.com/r/webdev). Reddit ads can also perform well if you’re OK with spending some money and these can be targeted to specific sub-Reddits too.

There are many similar sites that are less well known but which are respected in their niches and can drive a lot of interested visitors, including [Designer News](https://news.layervault.com/stories) (mobile and Web design), [DZone](http://www.dzone.com/) (general developer stuff), [EchoJS](http://www.echojs.com/) (JavaScript), [RubyFlow](http://rubyflow.com/) (Ruby and Rails), and [Lobste.rs](https://lobste.rs/) (general hacker and developer stuff). Finding the right site like this and taking time to make an on-topic, well written post will help a lot.

### The mass media / press

This article is primarily focused on the promotion of open source and front-end projects and these are typically not frequently covered in print or on the TV or radio. If, however, you think the mass media *would* be relevant for your project, here are some other articles packed with handy tips:

[How to PR Like a Pro: A Guide to Getting Media Attention](http://www.shopify.com/blog/4404772-how-to-pr-like-a-pro-a-guide-to-getting-media-attention)[How To Get Media Coverage For Your Startup: A Complete Guide](http://onstartups.com/tabid/3339/bid/80121/How-To-Get-Media-Coverage-For-Your-Startup-A-Complete-Guide.aspx)[Getting Press for Your Website, Application, or Service](http://www.shoemoney.com/2010/09/14/getting-press-for-your-website-application-or-service)[How to Get Major Media Coverage For Your Business with No Connections](http://socialtriggers.com/get-press-with-no-connections/)[How to Contact Press (And Increase Changes To Get Press Coverage)](http://www.pixelprospector.com/how-to-contact-press/)(oriented around promoting indie games but the essentials are there)

## Step 3: Maintain momentum

You’ve built up some interest, your GitHub stars, Reddit votes, and pageviews are all rocketing up, but now you want to capitalize on the attention and maintain some momentum.

### User support

Whether you’ve built an open source project or a cool tool, you’re going to end up with users or fellow developers who want to provide feedback, get help, or point out issues with your work. On GitHub, the common way to do this is through the built-in ‘issues’ tracker, but you might also find people start to e-mail you too.

Be sure to define a policy, whatever it is. Users won’t feel good about opening issues on your GitHub repo if there are already many unresolved issues there and your project could stagnate. Ensure you respond to your audience or at least make your policy clear within your README or on your site. If you don’t want issues raised or code contributions, make this clear up front.

### Extending your reach

For many projects, create a dedicated Twitter account, blog, Facebook page, or Google+ page in advance is overkill, but if your project starts to take off, consider these things. They’ll provide an extra way not only for users to remain in touch with your project but also a way for them to help promote it by retweeting things you post or by directing potential new users your way.

You can also extend your reach in person by going to user groups and conferences and, if you’re really lucky, you can speak about your work too. This is a great way to get new users as people are much more likely to look into your work if they’ve met you in person.

### Avoid being defensive

If your project does well on sites like Hacker News or Reddit, you’ll be tempted to read all of the comments your peers leave, but be careful. Comments about your work will, naturally, seem magnified in their intensity and critical comments that might not actually be mean spirited may seem as if they are to you.

It’s hard, but the best policy is to not let any overtly mean comments get to you, duly correct any observations that are wrong, and to thank anyone who goes out of their way to compliment your work. Even if you’re in the right, with the lack of body language and verbal cues, being too defensive can look bad online and result in the post becoming a lightning rod for drama. Engage as best you can, but if it feels wrong to reply to something, listen to your gut.

Be careful if you go into a new community to promote your work and get negative feedback. Most communities have rules or expectations and merely entering a community to promote your work is frequently considered a *faux pas.* Be sensitive to people’s environments and try to abide by a community’s rules at all times.

### The long term

If your project does particularly well, you could be presented with the opportunity of turning it into a business in its own right. Many simple open source projects, often started by a single developer, have turned into long term work or even entire companies for their creators.

Back in 2010, Mitchell Hashimoto released [Vagrant](http://www.vagrantup.com/), a Ruby-based tool for building a deploying VirtualBox-based virtualized development environments. In late 2012, Mitchell launched [Hashicorp](http://techcrunch.com/2012/11/28/vagrant-founder-launches-hashicorp-to-support-his-open-source-developer-management-tool/), a company providing Vagrant consulting services to enterprise customers. An even higher profile example is [Puppet Labs](http://en.wikipedia.org/wiki/Puppet_Labs), a company built around the Puppet open-source configuration management tool and which has taken total funding of $45.5 million so far.

If your project becomes respected and heavily used within its field, you might also be approached to write a book or article about it or even speak at a conference. This is a good sign that your project has ‘made it’ to some extent as publishers and event organizers are in the business of working out what it makes business sense to present.

## Putting it all together: A checklist

This has only been a basic introduction to promoting your work and with practice you’ll come up with tons of tips of your own (it’d be excellent if you could share some in the comments here). Based on all of the ideas above, here’s a basic checklist to run through next time you release a new project and want to get some added exposure:

- Focus most of your efforts on your project’s homepage or README.
- Check your project’s name doesn’t clash with anything else and is unique enough to find references to your work later.
- Promote your work to your closest social group first to unbury any problems with your work.
- Record a screencast or write a blog post about your project if some extra background would be useful for others.
- Work out a perfect *”[project name] is”* sentence to describe what your project is or does.
- Use your *”[project name] is”* sentence to give your page a descriptive title.
- Find influential people, blogs, podcasts, and e-mail newsletters in your niche and send them a short, pleasant note.
- Post to social news and bookmarking sites. Ensure your title is descriptive.
- Use your *”[project name] is”* sentence in e-mails and contacts with influencers.
- Take a positive, “look on the good side” approach to responding to comments about your work.

Good luck!

## About
[
Peter Cooper ](http://peterc.org)

Peter Cooper is the chair of O'Reilly's Fluent JavaScript and HTML5 conference and founder of Cooper Press. He's responsible for publishing several programming newsletters to over 100,000 developers each week, including JavaScript Weekly, HTML5 Weekly, and The Modern Web Observer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

Eric LawrenceMay 6th, 2013 at 10:03VenantiusMay 6th, 2013 at 11:26CatincanMay 6th, 2013 at 13:18Joe McTeeMay 6th, 2013 at 20:06Dor LaorMay 7th, 2013 at 01:26Catherine BullardMay 7th, 2013 at 09:05Khanh NguyenMay 7th, 2013 at 15:28Stephen8601May 7th, 2013 at 16:47lindaMay 9th, 2013 at 05:02GeorgeMay 13th, 2013 at 23:41David HigginsMay 14th, 2013 at 09:48Mathew PorterMay 18th, 2013 at 05:36jacob tolosiJune 4th, 2013 at 01:23