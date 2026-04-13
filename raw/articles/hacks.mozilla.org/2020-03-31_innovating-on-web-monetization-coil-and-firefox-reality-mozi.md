---
title: 'Innovating on Web Monetization: Coil and Firefox Reality – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2020/03/web-monetization-coil-and-firefox-reality/
author: Anselm Hook
published: '2020-03-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introducing Coil

In the coming weeks, Mozilla will roll out a Web Monetization experiment using [Coil](https://coil.com/about) to support payments to creators in the [Firefox Reality](https://mixedreality.mozilla.org/firefox-reality/) ecosystem. Web Monetization is an alternative approach to payments that doesn’t rely on advertising or stealing your data and attention. We wrote about [Web Monetization for game developers](https://hacks.mozilla.org/2019/10/from-js13kgames-to-mozfest-arcade-a-game-dev-web-monetization-story/) back in the autumn, and now we’re excited to invite more of you to participate, first as creators and soon as consumers of all kinds of digital and virtual content.

![Innovation: Web Monetization](../../assets/243c848a959b9e14.png)

*Problem: Now more than ever, digital content creators need new options for earning money from their work in a fast-changing world. Solution: Mozilla is testing Coil as an alternative to credit card or Paypal payments for authors and independent content creators.*


If you’ve developed a 3D experience, a game, a 360 video, or if you’re thinking of building something new, you’re invited to participate in this experiment. I encourage you as well to contact us directly at [creator_payments at mozilla dot com](mailto:creator_payments@mozilla.com) to showcase your work in the Firefox Reality content feed.

You’ll find details on how to participate below. I will also share answers and observations, from my own perspective as an implementer and investigator on the Mixed Reality team.

## A note about timing

Tangentially, the COVID-19 pandemic is dominating our attention. Just to be clear: This project is not a promise to create revenue for you during a planetary crisis. We support people where they are emotionally in their lives at this time and we do feel that real-world concerns are far more important. Also, we send thanks to everybody at Coil and Mozilla and all of you who are supporting this work when we’re all juggling family, chores, and our own lives.

## In closing

We know that many of you are looking for solutions to make money from your creative work online. We are here for you and we want you to create, share, and thrive on the net. Take a look the details on how to participate below. I will also share answers to other questions and observations from my own perspective as an implementer and investigator on the Mixed Reality team. Please let us know how this works for you!

## FAQ: How to participate

### How do I participate as a Creator?

Do you have a piece of content—a blog post, an interactive experience, a 360 video, a WebXR game—that you want to share with people in Firefox Reality? Here’s how you can web monetize this content:

The first step is to [add a meta tag](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/The_head_metadata_in_HTML) to the top of your site which will define a payment pointer (an email address for money). This article walks you through the process in detail:

Alternatively, this article is also good:

[Web Monetization: Quick Start Guide](https://webmonetization.org/docs/getting-started)

If you have a WordPress blog here’s [another way to add a payment pointer](https://xrpcommunity.blog/coil-wordpress/).

The second step is to simply please let us know! You can message us at [creator_payments@mozilla.com](mailto:creator_payments@mozilla.com) and we’ll make sure that your work is showcased in the Firefox Reality Content feed.

### What is this Coil thing anyway?

[Coil](https://coil.com) is a for-profit membership service that charges users $5.00 a month and streams micropayments to creators based on member attention. Coil uses the [Interledger network](https://interledger.org/) to move money, allowing creators to work in any currency they like.

Effectively you get paid for user attention—assuming those users are set up with web monetization. Web Monetization consists of an HTML tag, a JavaScript API, and uses the [Interledger](https://interledger.org) protocol for actually moving the money and enabling payments in many different currencies.

And just to be clear, Interledger is not a blockchain and there is no “Interledger token”. Interledger functions more like the Internet, in that it routes packets. Except the packets also represent money instead of just carrying data. You can find out more about how it works on [interledger.org](https://interledger.org).

### Why Coil?

Coil is an example of how open standards help foster healthy ecosystems. Coil can be thought of as a user-facing appliance running on top of the emerging [Web Monetization and Payment Pointers](https://webmonetization.org/specification.html) standard. As Coil succeeds, the possibilities for other payment services to succeed also increases. Once creators set up a payment pointer, they themselves are not tied to Coil. Anybody or any new service can send money to that creator—without using Coil itself. By lowering the “activation energy” this opens up the door for new payment services. Also, at the same time, we at Mozilla stay true to our values—fostering open standards, working internationally, and protecting user privacy.

### From a user perspective, if I install Coil how do I know it is working?

On a desktop browser, if you have a Coil subscription you can visit [Hubs by Mozilla](https://hubs.mozilla.com) right now, and by clicking on the Coil plugin you can see that it is being monetized.

For testing Coil in Firefox Reality, you can [visit this test site](https://testwebmonetization.com/) to see if you are Coil enabled. (Note: Personally, I’m not a big fan of the depiction of gender and the rags to riches narrative at that URL. But the site works for testing.)

### From a creator perspective if I install Coil how do I know it is working?

If you [visit this Coil Checker site](https://fudbingo.com/coilchecker) and enter the URL of your own site, it will report if your Coil implementation is working.

### Can I offer different content based on if patrons are paying or not?

As a creator, you can detect if patrons are Coil-enabled using javaScript. The recommended practice is called the “100+20” rule: offer special content for visitors who are paying, but do not disable the site or user experience for other guests. Please see the following links:

### Can I share revenue with other creators?

Ben has a [great article on Probabilistic Revenue Sharing](https://coil.com/p/sharafian/Probabilistic-Revenue-Sharing/8aQDSPsw) and Sabine has another one about a [Web Monetized Image Gallery](https://coil.com/p/sabinebertram/Web-Monetized-Image-Gallery-Intersection-Observer-Demo-/HY5nl9NT), showing how you can change where revenue is flowing based on which content is being examined.

### If I enable Coil on my sites how do I get cash out of the system?

If you are in the United States you can get an account at [Stronghold](https://stronghold.co/post/how-to-set-up-your-stronghold-payment-pointer). There are [other web wallets](https://webmonetization.org#wallets) that support Interledger and can convert payments to local currencies. This varies depending on which country you are in. Note that in the U.S, the Securities and Exchange Commission (SEC) has important [Know Your Customer (KYC) requirements](https://www.investopedia.com/terms/k/knowyourclient.asp), which means you’ll need to provide a driver’s license or passport.

Of course, Web Monetization will work better once it is adopted by a large number of users, built into most browsers, and so on, but the goal of this phase is less to generate a cash-out for you today and more about gathering data and feedback. So please keep in mind that this is an experiment! Also, again, we are especially interested in hearing how this works for you. Please make sure to contact us at [creator_payments at mozilla dot com](mailto:creator_payments@mozilla.com) once you set this up.

### How will Mozilla encourage users to participate in this experiment?

Stay tuned for a follow-up announcement in the not too distant future. In broad strokes, we will issue free Coil memberships to qualified users in the Firefox Reality ecosystem.

### How does this experiment with Coil differ from Mozilla’s partnership with Scroll.com?

Astute observers will notice that [Mozilla recently partnered with Scroll](https://techcrunch.com/2020/03/24/mozilla-scroll-partnership/), a new ad-free subscription service. So how is this different from Scroll and why do we need both things?

The main difference today is that our collaboration with Coil today is to test adoption.

These two membership services are aimed at different use cases. Coil lets anybody be a content creator and get paid out of user attention. Because the payout rate is something like $0.36 per hour per user, Coil becomes useful if you have hundreds of people looking at your site. In contrast, [Scroll](http://scroll.com) partners with specific and often larger organizations such as publishers and media outlets with reporters, editors, and higher overheads. Their fees reflect the value of news in terms of quality and reputation.

Notably there are also other services such as [Comixology](https://www.comixology.com/), ([also described here](https://www.polygon.com/comics/2018/12/26/18104852/where-to-buy-read-download-digital-comics-apps-subscription-services)), [Flattr](https://flattr.com/), and [Unlock](https://unlock-protocol.com/blog/its-time-to-unlock-the-web/). Each of these caters to different audience needs.

We can even imagine future services that have much higher payment rates, such as charging $30.00 an hour to allow a foreign language teacher in a virtual [Hubs](https://hubs.mozilla.com) room to teach a small class of students and have a sustainable business. There will never be a single silver bullet that covers all consumer needs.

### Does “Grant for the Web” relate to this?

[Grant for the Web](https://www.grantfortheweb.org/) is a separate series of grants that are definitely worth applying for. This initiative plans to distribute 100 million dollars to support creators on the web. This is especially suitable for web projects that require up-front funding.

## Payment Challenges and Solutions

### Why are we looking at payment solutions?

Last year we interviewed web developers and creatives, asking them about how they monetized content on the web. They reported several challenges. These are two of the largest issues:

*Payment Frictions:*Many developers reported that they simply didn’t have good ways to charge money—especially small amounts of money.[Solutions](https://www.webfx.com/blog/web-design/online-payment-systems/)were[fragmented](https://websitesetup.org/33-ways-to-monetize-website/)and[complex](https://www.corbettbarr.com/online-business-revenue-models-for-lifestyle-entrepreneurs/). Their patrons didn’t have a way to pay even if they wanted to.*Funding Up Front:*Beyond payments, there was a specific issue around simply needing more money before starting development. Historically, smaller web developers were often able to incrementally grow their revenue. Yet because the web is becoming more powerful there are now higher up-front costs to build compelling experiences.

Note that there were many other related issues such as discoverability of content, consumer trust in content, defending intellectual property, better tools for building content and so on. But payments is one area that seems to require a known and trusted neutral third-party. And so, we believe that Mozilla is uniquely qualified to help with this.

### A look at the digital content ecosystem

If we step back and look beyond the web, digital content ecosystems are exploding. Social apps such as Facebook are a [$50 billion dollar a year industry](https://www.digitalinformationworld.com/2019/05/how-tech-giants-make-billions-infographic.html), driven by advertising. Mobile app subscription revenue is [$4 billion dollars a year](https://techcrunch.com/2020/01/23/u-s-mobile-app-subscription-revenue-jumped-21-in-2019-to-4-6b-across-the-top-100-apps/). Mobile native games were forecast to [capture over $70 billion dollars in 2019](https://www.mobilemarketer.com/news/mobile-games-sparked-60-of-2019-global-game-revenue-study-finds/569658/).

Experiences on app stores such as [Google Play](https://www.mobiloud.com/help/knowledge-base/what-are-apple-and-googles-fees-and-revenue-share-percentage-on-in-app-purchases-and-subscriptions/) or the [Apple App Store](https://www.apple.com/ios/app-store/principles-practices/) can capture up to 30% of that energy in transaction fees. (Admittedly, they provide other valuable services mentioned above, such as [quality](https://developer.apple.com/app-store/review/), [trust](https://insights.dice.com/2018/10/23/apple-app-notarization-macos-apps/), [discovery](https://remysharp.com/2016/04/11/the-webapp-discovery-problem), and [recourse](https://support.google.com/googleplay/answer/2853570?co=GENIE.Platform%3DAndroid&hl=en)).

Although [the boundary between native and web is somewhat porous](https://www.nngroup.com/articles/mobile-native-apps/), some developers we spoke to were [packaging their web apps as native apps](https://www.electronjs.org/) and releasing them into [app stores such as itch.io](https://itch.io/) just to get cash out of the system for their labor.

However, the web is unique. The web is open and accessible to all parties, not owned or controlled by any one party. Content can be shared with a URL. Because of this, the web has become the place of the “great conversation” – where we can all talk freely about issues all over the world.

Thanks to the work of many engineers, [the web has many of the rich visual capabilities of native apps](https://blog.mozvr.com/webxr-1-0-is-here/) delivered via open standards. Technologies like [WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly) and [high-performance languages such as Rust](https://www.rust-lang.org/) make it possible for a game like [Candy Crush Saga](https://venturebeat.com/2019/01/09/sensor-tower-candy-crush-players-spent-an-average-of-4-2-million-a-day-in-2018/) to become a web experience.

And yet, even though you can share a web experience with somebody halfway around the planet, there’s no way for them to tip you a quarter if they like their experience. If money is a form of communication, then it makes sense to fix money as well—in an open, scalable way that is fair, and that discourages bad actors.

### Why not just stick with advertising?

Right now [advertising dominates on the web as a revenue model](https://www.investopedia.com/ask/answers/041015/how-important-advertising-revenue-internet-sector.asp). Ads are important and valuable as a form of social signaling in a noisy landscape. However, this means creators may be beholden to advertisers more so than to their patrons.

There are strong market incentives today to profile, segment, and target users. Targeting can even become a vector for bad actors, such as we saw with [Cambridge Analytica](https://www.theguardian.com/news/series/cambridge-analytica-files). Cross-site tracking in particular is a concern. As a result, browser vendors such as [Apple](https://www.theverge.com/2020/3/24/21192830/apple-safari-intelligent-tracking-privacy-full-third-party-cookie-blocking), [Microsoft](https://docs.microsoft.com/en-us/microsoft-edge/web-platform/tracking-prevention) and [Mozilla are working to reduce cross-site tracking](https://support.mozilla.org/en-US/kb/trackers-and-scripts-firefox-blocks-enhanced-track). This is reducing the effectiveness of advertising as a whole.

[But nature abhors a vacuum](https://digiday.com/media/arms-race-publishers-prepare-anti-tracking-dominant-future/). We need to do more. From an ecosystem perspective, if we can support alternative revenue options and protect user privacy this feels like a win.

### Don’t users expect content on the web to be free?

There is some argument that services like [Patreon](https://patreon.com) and [Kickstarter](https://kickstarter.com) exist because people who enjoy online content want to think of themselves as patrons of the arts; not merely consumers. We are doing this experiment in part to test that idea.

### Why not invent some other digital currency or wallet solution?

Payments on the web is [a complex topic](https://www.w3.org/blog/wpwg/2019/10/28/the-evolution-of-payment-request-api/). There are creator needs, user and patron needs, privacy concerns, international boundaries, payment frictions and costs, [regulatory issues](https://www.investopedia.com/news/how-sec-regs-will-change-cryptocurrency-markets/) and so on. Consider even just the issue of people who don’t have credit cards; or artists, story-tellers, and creators around the world who don’t have bank accounts at all—[especially women](https://globalfindex.worldbank.org/sites/globalfindex/files/chapters/2017%20Findex%20full%20report_chapter2.pdf).

We’ve seen ideas over the years ranging from [Beenz](https://en.wikipedia.org/wiki/Beenz.com) (now defunct) to [Libra](https://libra.org/en-US/), and every imaginable point system and scheme. We see [Brave](https://brave.com/) and [Puma](https://www.pumabrowser.com/) providing browser-bound solutions. Industry-wide, we have working methods for purchases online for adults with credit cards such as through [Stripe](https://hackernoon.com/how-to-integrate-stripe-payments-in-web-application-2c72d5c67454) or [Paypal](https://www.paypal.com/uk/webapps/mpp/micropayments). But there aren’t widely available solutions for smaller low-friction payments that hit all our criteria.

We will continue to explore a variety of options, but we want options like Web Monetization that are available today. We value options that have low activation energy; are transparent and easy to test; don’t require industry changes; handle small transactions; work over international boundaries; are abuse-resistant; help the unbanked; and protect user privacy.

### Doesn’t Web Payments solve this problem?

We’re all familiar with the Error code 404 – page not found warning on the web. But probably not a single one of us has seen an “[Error code 402 – payment required](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/402)” warning. Payments are not something we as consumers use yet or encounter routinely in the wild.

![402 Payment Required from girlie mac on flickr](../../assets/8090117b423956e9.jpg)

*Until we see “402 Payment Required” on the web it’s probably likely that we have not solved web payments.*


Yes, we have [W3C Web Payments](https://www.w3.org/Payments/)—and this may become the right answer. There are some options from Paypal for micropayments, as well as a bewildering number of cryptocurrency solutions. Still, we have our work cut out for us.

### Long-Term Trajectories: A Vision

Welcome to the future. It is August 1st, 2022. You’re surfing the web and you come across an [amazing recipe site](https://smittenkitchen.com/recipe-collection/best-of-smitten-kitchen/?format=photo) or blog post you really like, perhaps a [kid-friendly indie game](https://constructarca.de/game/barista-express/) or [photos of the northern lights](https://www.hurtigruten.com/inspiration/experiences/northern-lights/10-photography-tips-for-beginners/), captured and shared by somebody in a different country. Or perhaps you’ve been watching a [campaign to protect forests in Romania](https://www.euronatur.org/en/what-we-do/campaigns-and-initiatives/save-paradise-forests/) and you want to donate. Now imagine being able to easily send them money as a token of your appreciation.

Maybe you’ve become a fan of a new virtual reality [interactive journalism](https://ochre.is/inspiration/you-become-a-witness-nonny-de-la-pena-immersive-journalism/) site. Rather than subscribing to them specifically you use a service that streams background micropayments while you are on their site. As you and your friends join in, the authors get more and more support over time. The creator is directly supported in their work, and directly responsive to you, rather than having to chase grants. They’re able to vet their sources better and extend their reach.

This is the kind of vision that we want to support. Let’s get there together. If you have any other questions or comments please reach out!

## About Anselm Hook

Reach me on Twitter at @anselm. Grew up in the Canadian Rockies and I still very much love the outdoors and find it grounding. If I had to pick one thing I'd say I'm especially interested in "helping people to see better" - to signal to each other across noisy digital landscapes and to make informed decisions better together.

## 3 comments

MarkApril 2nd, 2020 at 09:56Oliver FeiApril 4th, 2020 at 11:10Havi HoffmanApril 13th, 2020 at 10:51