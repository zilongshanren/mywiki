---
title: MDN Web Docs evolves! Lowdown on the upcoming new platform – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2020/10/mdn-web-docs-evolves-lowdown-on-the-upcoming-new-platform/
author: Chris Mills
published: '2020-10-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The time has come for [Kuma](https://github.com/mdn/kuma) — the platform that powers MDN Web Docs — to evolve. For quite some time now, the MDN developer team has been planning a radical platform change, and we are ready to start sharing the details of it. The question on your lips might be “What does a Kuma evolve into? A KumaMaMa?”

![What? Kuma is evolving!](../../assets/ee4572c83e307e1e.png)


For those of you not so into Pokémon, the question might instead be “How exactly is MDN changing, and how does it affect MDN users and contributors”?

For general users, the answer is easy — there will be very little change to how we serve the great content you use everyday to learn and do your jobs.

For contributors, the answer is a bit more complex.

## The changes in a nutshell

In short, we are updating the platform to move the content from a MySQL database to being hosted in a GitHub repository (codename: Project [Yari](https://en.wikipedia.org/wiki/Yari)).

![Congratulations! Your Kuma evolved into Yari](../../assets/71431e24e920e08d.png)


The main advantages of this approach are:

- Less developer maintenance burden: The existing (Kuma) platform is complex and hard to maintain. Adding new features is very difficult. The update will vastly simplify the platform code — we estimate that we can remove a significant chunk of the existing codebase, meaning easier maintenance and contributions.
- Better contribution workflow: We will be using GitHub’s contribution tools and features, essentially moving MDN from a Wiki model to a pull request (PR) model. This is so much better for contribution, allowing for intelligent linting, mass edits, and inclusion of MDN docs in whatever workflows you want to add it to (you can edit MDN source files directly in your favorite code editor).
- Better community building: At the moment, MDN content edits are published instantly, and then reverted if they are not suitable. This is really bad for community relations. With a PR model, we can review edits and provide feedback, actually having conversations with contributors, building relationships with them, and helping them learn.
- Improved front-end architecture: The existing MDN platform has a number of front-end inconsistencies and accessibility issues, which we’ve wanted to tackle for some time. The move to a new, simplified platform gives us a perfect opportunity to fix such issues.

The exact form of the platform is yet to be finalized, and we want to involve you, the community, in helping to provide ideas and test the new contribution workflow! We will have a beta version of the new platform ready for testing on November 2, and the first release will happen on December 14.

## Simplified back-end platform

We are replacing the current MDN Wiki platform with a [JAMStack](https://jamstack.org/) approach, which publishes the content managed in a GitHub repo. This has a number of advantages over the existing Wiki platform, and is something we’ve been considering for a number of years.

Before we discuss our new approach, let’s review the Wiki model so we can better understand the changes we’re making.

### Current MDN Wiki platform


![workflow diagram of the old kuma platform](../../assets/5054b31c8f6bc934.png)


It’s important to note that both content contributors (writers) and content viewers (readers) are served via the same architecture. That architecture has to accommodate both use cases, even though more than 99% of our traffic comprises document page requests from readers. Currently, when a document page is requested, the latest version of the document is read from our MySQL database, rendered into its final HTML form, and returned to the user via the CDN.

That document page is stored and served from the CDN’s cache for the next 5 minutes, so subsequent requests — as long as they’re within that 5-minute window — will be served directly by the CDN. That caching period of 5 minutes is kept deliberately short, mainly due to the fact that we need to accommodate the needs of the writers. If we only had to accommodate the needs of the readers, we could significantly increase the caching period and serve our document pages more quickly, while at the same time reducing the workload on our backend servers.

You’ll also notice that because MDN is a Wiki platform, we’re responsible for managing all of the content, and tasks like storing document revisions, displaying the revision history of a document, displaying differences between revisions, and so on. Currently, the MDN development team maintains a large chunk of code devoted to just these kinds of tasks.

### New MDN platform


![workflow diagram of the new yari platform](../../assets/3dcde542961030e5.png)


With the new [JAMStack](https://jamstack.org/) approach, the writers are served separately from the readers. The writers manage the document content via [a GitHub repository](https://github.com/mdn/content) and pull request model, while the readers are served document pages more quickly and efficiently via pre-rendered document pages served from S3 via a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network) (which will have a much longer caching period). The document content from our GitHub repository will be rendered and deployed to S3 on a daily basis.

You’ll notice, from the diagram above, that even with this new approach, we still have a Kubernetes cluster with Django-based services relying on a relational database. The important thing to remember is that this part of the system is no longer involved with the document content. Its scope has been dramatically reduced, and it now exists solely to provide APIs related to user accounts (e.g. login) and search.

This separation of concerns has multiple benefits, the most important three of which are as follows:

- First, the document pages are served to readers in the simplest, quickest, and most efficient way possible. That’s really important, because 99% of MDN’s traffic is for readers, and worldwide performance is fundamental to the user experience.
- Second, because we’re using GitHub to manage our document content, we can take advantage of the world-class functionality that GitHub has to offer as a content management system, and we no longer have to support the large body of code related to our current Wiki platform. It can simply be deleted.
- Third, and maybe less obvious, is that this new approach brings more power to the platform. We can, for example, perform automated linting and testing on each content pull request, which allows us to better control quality and security.

## New contribution workflow

Because MDN content is soon to be contained in a GitHub repo, the contribution workflow will change significantly. You will no longer be able to click *Edit* on a page, make and save a change, and have it show up nearly immediately on the page. You’ll also no longer be able to do your edits in a WYSIWYG editor.

Instead, you’ll need to use git/GitHub tooling to make changes, submit pull requests, then wait for changes to be merged, the new build to be deployed, etc. For very simple changes such as fixing typos or adding new paragraphs, this may seem like a step back — Kuma is certainly convenient for such edits, and for non-developer contributors.

However, making a simple change is arguably no more complex with Yari. You can use the GitHub UI’s edit feature to directly edit a source file and then submit a PR, meaning that you don’t have to be a git genius to contribute simple fixes.

For more complex changes, you’ll need to use the git CLI tool, or a GUI tool like [GitHub Desktop](https://desktop.github.com/), but then again git is such a ubiquitous tool in the web industry that it is safe to say that if you are interested in editing MDN, you will probably need to know git to some degree for your career or course. You could use this as a good opportunity to learn git if you don’t know it already! On top of that there is a file system structure to learn, and some new tools/commands to get used to, but nothing terribly complex.

Another possible challenge to mention is that you won’t have a WYSIWYG to instantly see what the page looks like as you add your content, and in addition you’ll be editing raw HTML, at least initially (we are talking about converting the content to markdown eventually, but that is a bit of a ways off). Again, this sounds like a step backwards, but we are providing a tool inside the repo so that you can locally build and preview the finished page to make sure it looks right before you submit your pull request.

Looking at the advantages now, consider that making MDN content available as a GitHub repo is a very powerful thing. We no longer have spam content live on the site, with us then having to revert the changes after the fact. You are also free to edit MDN content in whatever way suits you best — your favorite IDE or code editor — and you can add MDN documentation into your preferred toolchain (and write your own tools to edit your MDN editing experience). A lot of engineers have told us in the past that they’d be much happier to contribute to MDN documentation if they were able to submit pull requests, and not have to use a WYSIWYG!

We are also looking into a powerful toolset that will allow us to enhance the reviewing process, for example as part of a CI process — automatically detecting and closing spam PRs, and as mentioned earlier on, linting pages once they’ve been edited, and delivering feedback to editors.

Having MDN in a GitHub repo also offers much easier mass edits; blanket content changes have previously been very difficult.

Finally, the “time to live” should be acceptable — we are aiming to have a quick turnaround on the reviews, and the deployment process will be repeated every 24 hours. We think that your changes should be live on the site in 48 hours as a worst case scenario.

## Better community building

Currently MDN is not a very lively place in terms of its community. We have a fairly active [learning forum](https://discourse.mozilla.org/c/mdn/learn/250) where people ask beginner coding questions and seek help with assessments, but there is not really an active place where MDN staff and volunteers get together regularly to discuss documentation needs and contributions.

Part of this is down to our contribution model. When you edit an MDN page, either your contribution is accepted and you don’t hear anything, or your contribution is reverted and you … don’t hear anything. You’ll only know either way by looking to see if your edit sticks, is counter-edited, or is reverted.

This doesn’t strike us as very friendly, and I think you’ll probably agree. When we move to a git PR model, the MDN community will be able to provide hands-on assistance in helping people to get their contributions right — offering assistance as we review their PRs (and offering automated help too, as mentioned previously) — and also thanking people for their help.

It’ll also be much easier for contributors to show how many contributions they’ve made, and we’ll be adding in-page links to allow people to file an issue on a specific page or even go straight to the source on GitHub and fix it themselves, if a problem is encountered.

In terms of finding a good place to chat about MDN content, you can join the discussion on the[ MDN Web Docs chat room](https://chat.mozilla.org/#/room/#mdn:mozilla.org) on[ Matrix](https://wiki.mozilla.org/Matrix).

## Improved front-end architecture

The old Kuma architecture has a number of front-end issues. Historically we have lacked a well-defined system that clearly describes the constraints we need to work within, and what our site features look like, and this has led to us ending up with a bloated, difficult to maintain front-end code base. Working on our current HTML and CSS is like being on a roller coaster with no guard-rails.

To be clear, this is not the fault of any one person, or any specific period in the life of the MDN project. There are many little things that have been left to fester, multiply, and rot over time.

Among the most significant problems are:

- Accessibility: There are a number of accessibility problems with the existing architecture that really should be sorted out, but were difficult to get a handle on because of Kuma’s complexity.
- Component inconsistency: Kuma doesn’t use a proper design system — similar items are implemented in different ways across the site, so implementing features is more difficult than it needs to be.

When we started to move forward with the back-end platform rewrite, it felt like the perfect time to again propose the idea of a design system. After many conversations leading to an acceptable compromise being reached, our design system — MDN Fiori — was born.

Front-end developer Schalk Neethling and UX designer Mustafa Al-Qinneh took a whirlwind tour through the core of MDN’s reference docs to identify components and document all the inconsistencies we are dealing with. As part of this work, we also looked for areas where we can improve the user experience, and introduce consistency through making small changes to some core underlying aspects of the overall design.

This included a defined color palette, simple, clean typography based on a well-defined type scale, consistent spacing, improved support for mobile and tablet devices, and many other small tweaks. This was never meant to be a redesign of MDN, so we had to be careful not to change too much. Instead, we played to our existing strengths and made rogue styles and markup consistent with the overall project.

Besides the visual consistency and general user experience aspects, our underlying codebase needed some serious love and attention — we decided on a complete rethink. Early on in the process it became clear that we needed a base library that was small, nimble, and minimal. Something uniquely MDN, but that could be reused wherever the core aspects of the MDN brand was needed. For this purpose we created [MDN-Minimalist](https://github.com/mdn/mdn-minimalist), a small set of core atoms that power the base styling of MDN, in a progressively enhanced manner, taking advantage of the beautiful new layout systems we have access to on the web today.

Each component that is built into Yari is styled with MDN-Minimalist, and also has its own style sheet that lives right alongside to apply further styles only when needed. This is an evolving process as we constantly rethink how to provide a great user experience while staying as close to the web platform as possible. The reason for this is two fold:

- First, it means less code. It means less reinventing of the wheel. It means a faster, leaner, less bandwidth-hungry MDN for our end users.
- Second, it helps address some of the accessibility issues we have begrudgingly been living with for some time, which are simply not acceptable on a modern web site. One of Mozilla’s accessibility experts, Marco Zehe, has given us a lot of input to help overcome these. We won’t fix everything in our first iteration, but our pledge to all of our users is that we will keep improving and we welcome your feedback on areas where we can improve further.

A wise person once said that the best way to ensure something is done right is to make doing the right thing the easy thing to do. As such, along with all of the work already mentioned, we are documenting our front-end codebase, design system, and pattern library in Storybook (see [Storybook files inside the yari repo](https://github.com/mdn/yari/tree/8dcbbd63aa5b75c2d4e08e39cd2ea65bb099a801/client/src/stories)) with companion design work in Figma ([see typography example](https://www.figma.com/file/YYVJ8uqG8UFBBvQhdI7fxR/MDN-Web-Docs?node-id=184%3A3)) to ensure there is an easy, public reference for anyone who wishes to contribute to MDN from a code or design perspective. This in itself is a large project that will evolve over time. More communication about its evolution will follow.

## The future of MDN localization

One important part of MDN’s content that we have talked about a lot during the planning phase is the localized content. As you probably already know, MDN offers facilities for translating the original English content and making the localizations available alongside it.

This is good in principle, but the current system has many flaws. When an English page is moved, the localizations all have to be moved separately, so pages and their localizations quite often go out of sync and get in a mess. And a bigger problem is that there is no easy way of signalling that the English version has changed to all the localizers.

General management is probably the most significant problem. You often get a wave of enthusiasm for a locale, and lots of translations done. But then after a number of months interest wanes, and no-one is left to keep the translations up to date. The localized content becomes outdated, which is often harmful to learning, becomes a maintenance time-suck, and as a result, is often considered worse than having no localizations at all.

**Note that we are not saying this is true of all locales on MDN, and we are not trying to downplay the amount of work volunteers have put into creating localized content. For that, we are eternally grateful. But the fact remains that we can’t carry on like this.**

We did a bunch of research, and talked to a lot of non-native-English speaking web developers about what would be useful to them. Two interesting conclusions were made:

- We stand to experience a significant but manageable loss of users if we remove or reduce our localization support. 8 languages cover 90% of the accept-language headers received from MDN users (en, zh, es, ja, fr, ru, pt, de), while 14 languages cover 95% of the accept-languages (en, zh, es, ja, fr, ru, pt, de, ko, zh-TW, pl, it, nl, tr). We predict that we would expect to lose at most 19% of our traffic if we dropped L10n entirely.
- Machine translations are an acceptable solution in most cases, if not a perfect one. We looked at the quality of translations provided by automated solutions such as Google Translate and got some community members to compare these translations to manual translations. The machine translations were imperfect, and sometimes hard to understand, but many people commented that a non-perfect language that is up-to-date is better than a perfect language that is out-of-date. We appreciate that some languages (such as CJK languages) fare less well than others with automated translations.

So what did we decide? With the initial release of the new platform, we are planning to include all translations of all of the current documents, but in a frozen state. Translations will exist in their own mdn/translated-content repository, to which we will not accept any pull requests. The translations will be shown with a special header that says “This is an archived translation. No more edits are being accepted.” This is a temporary stage until we figure out the next step.

**Note: In addition, the text of the UI components and header menu will be in English only, going forward. They will not be translated, at least not initially.**

After the initial release, we want to work with you, the community, to figure out the best course of action to move forward with for translations. We would ideally rather not lose localized content on MDN, but we need to fix the technical problems of the past, manage it better, and ensure that the content stays up-to-date.

We will be planning the next phase of MDN localization with the following guiding principles:

- We should never have outdated localized content on MDN.
- Manually localizing all MDN content in a huge range of locales seems infeasible, so we should drop that approach.
- Losing ~20% of traffic is something we should avoid, if possible.

We are making no promises about deliverables or time frames yet, but we have started to think along these lines:

- Cut down the number of locales we are handling to the top 14 locales that give us 95% of our recorded accept-language headers.
- Initially include non-editable Machine Learning-based automated translations of the “tier-1” MDN content pages (i.e. a set of the most important MDN content that excludes the vast long tail of articles that get no, or nearly no views). Ideally we’d like to use the existing manual translations to train the Machine Learning system, hopefully getting better results. This is likely to be the first thing we’ll work on in 2021.
- Regularly update the automated translations as the English content changes, keeping them up-to-date.
- Start to offer a system whereby we allow community members to improve the automated translations with manual edits. This would require the community to ensure that articles are kept up-to-date with the English versions as they are updated.

## Acknowledgements

I’d like to thank my colleagues Schalk Neethling, Ryan Johnson, Peter Bengtsson, Rina Tambo Jensen, Hermina Condei, Melissa Thermidor, and anyone else I’ve forgotten who helped me polish this article with bits of content, feedback, reviews, edits, and more.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 46 comments

LawrenceOctober 29th, 2020 at 09:31Chris MillsOctober 29th, 2020 at 09:52GUOctober 29th, 2020 at 21:07Gabriel FloritOctober 29th, 2020 at 10:11Chris MillsOctober 29th, 2020 at 10:320xjacOctober 29th, 2020 at 10:15chris jonesNovember 1st, 2020 at 15:10Chris MillsNovember 2nd, 2020 at 02:12BarisOctober 29th, 2020 at 10:27Chris MillsOctober 30th, 2020 at 10:18yeahOctober 29th, 2020 at 12:06Adam WilliamsOctober 29th, 2020 at 12:12Chris MillsOctober 30th, 2020 at 10:41robbawebaOctober 29th, 2020 at 14:39Chris MillsOctober 30th, 2020 at 10:44iamwillshepherdOctober 29th, 2020 at 14:43Chris MillsOctober 30th, 2020 at 10:49WilliamNovember 20th, 2020 at 05:17AslanOctober 29th, 2020 at 15:12Peter BengtssonNovember 3rd, 2020 at 17:14Philip WhitehouseOctober 29th, 2020 at 18:19Chris MillsOctober 30th, 2020 at 10:52Duncan LockOctober 29th, 2020 at 20:34Chris MillsOctober 30th, 2020 at 10:53voracityOctober 30th, 2020 at 05:48Chris MillsOctober 30th, 2020 at 10:56Rami YushuvaevOctober 30th, 2020 at 08:56Chris MillsOctober 30th, 2020 at 10:59Guillaume GrossetieOctober 30th, 2020 at 11:08Peter BengtssonNovember 2nd, 2020 at 05:27azuOctober 30th, 2020 at 20:23Outvi VOctober 30th, 2020 at 20:41Peter BengtssonNovember 2nd, 2020 at 06:45JesperOctober 30th, 2020 at 22:16Peter BengtssonNovember 2nd, 2020 at 05:43MaxOctober 31st, 2020 at 04:01Chris MillsOctober 31st, 2020 at 04:35Peter BengtssonNovember 2nd, 2020 at 05:30Peter BengtssonNovember 2nd, 2020 at 06:42YoungNovember 3rd, 2020 at 09:44Chris MillsNovember 3rd, 2020 at 10:09DennisNovember 5th, 2020 at 11:26Tom VanAntwerpNovember 6th, 2020 at 09:23Zac SvobodaNovember 8th, 2020 at 14:44xtyNovember 11th, 2020 at 17:18HenryNovember 17th, 2020 at 17:38