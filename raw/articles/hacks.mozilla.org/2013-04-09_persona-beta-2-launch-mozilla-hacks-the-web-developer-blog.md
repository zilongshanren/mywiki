---
title: Persona Beta 2 launch – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/04/persona-beta-2-launch/
author: Mozilla
published: '2013-04-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Mozilla Persona is an open authentication system that lets you implement sign-in on your site in an afternoon. Today, Persona Beta 2 was released, including a feature called "Identity Bridging" that lets hundreds of millions of users sign into sites supporting Persona with no new username and no new password. The announcement video gives you a good overview of the Beta 2 release:

## What's New

In addition to "Identity Bridging", a couple important new features have landed, and we've started to see significant adoption of the service. Details about these features and new websites using Persona are provided in the announcement on the [Mozilla Identity Blog](http://identity.mozilla.com/post/47541633049/persona-beta-2).

## Persona, The Full Story

Beyond the code and features, we've really made an effort to tell the full story behind Persona to help people understand how it works, and why we believe it's an important improvement to how people log into websites. You can read [an interview with lead developer Lloyd](https://blog.mozilla.org/beyond-the-code/2013/04/09/persona-beta2/) to get a feel for some of Mozilla's motivations and goals for Persona.

Identity on the web is complex, and the full story can't be captured in a single conversation. To address this, leading up to this beta, we've published several articles on the identity blog which [compare Persona to social sign-in](http://identity.mozilla.com/post/45842909320/users-dont-like-social-login), [give an overview of Persona on FirefoxOS](http://identity.mozilla.com/post/47114516102/persona-on-firefox-os-phones), and dig into [why the distributed nature of Persona matters](http://identity.mozilla.com/post/46374271364/persona-is-distributed-today).

Beyond the philosophy, we've detailed the technology behind Persona. This has resulted in [several articles that present tools and learnings](https://hacks.mozilla.org/category/a-node-js-holiday-season/as/title/) we hope are relevant to anyone building massive scale services with Node.JS.

## How Identity Bridging Works

Identity Bridging is the most important feature of today's release, so let's take a minute to get beyond the emphatic language of a press release and down to how it actually works.

The motivating idea is that checking your email and clicking a link during the sign-in process is jarring and can cause a drop in the number of people who sign up. A significant portion of our UX refinements have been targeted at this problem. So, what can you do to eliminate this step completely?

Most popular webmail providers nowadays offer either [OpenID](http://en.wikipedia.org/wiki/OpenID) or [OAuth](http://en.wikipedia.org/wiki/OAuth) as a means for other websites to build authentication using the provider's existing user base (and hence, let people log in faster). On the Persona side we have support for any domain to become a [Persona enabled identity provider](https://developer.mozilla.org/en-US/docs/Persona/Identity_Provider_Overview) and allow address verification without sending email.

So we built a bridge – a server that speaks the Persona IdP protocol on one side and OpenID or OAuth on the other – to use these existing services. The project's codename is "BigTent", and, as with everything we do, the [codebase is open source](https://github.com/mozilla/browserid-bigtent).

To start, we've enabled this bridge for anyone with a yahoo.com email address. In the coming months, we'll turn on support for other major email providers. We expect to cover over half of the worldwide internet population.

Identity bridging is a huge win. It's significantly more convenient for users by eliminating the need to verify emails. Developers get the convenience of social sign-in just by supporting Persona. And finally, it's better for user privacy: Identity Bridging keeps the sites a user visits out of the purview of their identity provider. This is one of those rare and wonderful cases where we can improve both usability and security at the same time!

## Try Persona Today!

Implementing Persona on your site should take about an afternoon. To do so, you:

- Include a javascript library in your page
- Add javascript code to handle login events
- Invoke
`navigator.id.request()`

when a user clicks your login button - Implement a server-side handler to verify users and start their session

Each of these steps is described in more detail in our [quick setup guide](https://developer.mozilla.org/en-US/docs/Persona/Quick_Setup), and if for whatever reason things go awry, we're here to help!

## What's Next?

We have a couple clear new features planned, but mostly our roadmap is going to determined by the people who use Persona. If you haven't tried Persona on your website yet, spend an afternoon and give it a whirl. Let us know what you think [on our public mailing list](https://lists.mozilla.org/listinfo/dev-identity), and help us get rid of the password.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 26 comments

Josh TumathApril 9th, 2013 at 09:32Lloyd HilaielApril 9th, 2013 at 10:35CleanCode PoliceApril 9th, 2013 at 10:49Robert Nyman [Editor]April 9th, 2013 at 10:53penangApril 9th, 2013 at 18:40Lloyd HilaielApril 10th, 2013 at 06:50Matthew PiggottApril 9th, 2013 at 19:08Lloyd HilaielApril 10th, 2013 at 06:52thinsoldierApril 12th, 2013 at 21:27Caspy7April 14th, 2013 at 23:54Lloyd HilaielApril 15th, 2013 at 08:11DBApril 9th, 2013 at 21:46Lloyd HilaielApril 10th, 2013 at 07:10MarkApril 10th, 2013 at 03:51Dan CallahanApril 10th, 2013 at 09:52tonyApril 10th, 2013 at 07:32Caspy7April 11th, 2013 at 08:17Simon BApril 10th, 2013 at 13:25SokratisApril 11th, 2013 at 02:53Lloyd HilaielApril 12th, 2013 at 10:42robyzApril 11th, 2013 at 03:21Lloyd HilaielApril 12th, 2013 at 10:48AnonymousApril 11th, 2013 at 04:06Lloyd HilaielApril 15th, 2013 at 08:22FrançoisApril 11th, 2013 at 08:48Lloyd HilaielApril 15th, 2013 at 08:19