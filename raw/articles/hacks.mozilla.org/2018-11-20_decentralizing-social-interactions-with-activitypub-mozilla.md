---
title: Decentralizing Social Interactions with ActivityPub – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2018/11/decentralizing-social-interactions-with-activitypub/
author: Darius Kazemi
published: '2018-11-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*In the Dweb series, we are covering projects that explore what is possible when the web becomes decentralized or distributed. These projects aren’t affiliated with Mozilla, and some of them rewrite the rules of how we think about a web browser. What they have in common: These projects are open source and open for participation, and they share Mozilla’s mission to keep the web open and accessible for all.*

*Social websites first got us talking and sharing with our friends online, then turned into echo-chamber content silos, and finally emerged in their mature state as surveillance capitalist juggernauts, powered by the effluent of our daily lives online. The tail isn’t just wagging the dog, it’s strangling it. However, there just might be a way forward that puts users back in the driver seat: A new set of specifications for decentralizing social activity on the web. Today you’ll get a helping hand into that world from from Darius Kazemi, renowned bot-smith and Mozilla Fellow.*

*– Dietrich Ayala*

## Introducing ActivityPub

Hi, I’m [Darius Kazemi](https://tinysubversions.com/). I’m a Mozilla Fellow and decentralized web enthusiast. In the last year I’ve become really excited about [ActivityPub](https://activitypub.rocks/), a W3C standard protocol that describes ways for different social network sites (loosely defined) to talk to and interact with one another. You might remember the heyday of RSS, when a user could subscribe to almost any content feed in the world from any number of independently developed feed readers. ActivityPub aims to do for social network interactions what RSS did for content.

## Architecture

ActivityPub enables a decentralized social web, where a network of servers interact with each other on behalf of individual users/clients, very much like email operates at a macro level. On an ActivityPub compliant server, individual user accounts have an inbox and an outbox that accept HTTP GET and POST requests via API endpoints. They usually live somewhere like `https://social.example/users/dariusk/inbox`

and `https://social.example/users/dariusk/outbox`

, but they can really be anywhere as long as they are at a valid URI. Individual users are represented by an Actor object, which is just a [JSON-LD](https://json-ld.org/) file that gives information like username and where the inbox and outbox are located so you can talk to the Actor. Every message sent on behalf of an Actor has the link to the Actor’s JSON-LD file so anyone receiving the message can look up all the relevant information and start interacting with them.

## A simple server to send ActivityPub messages

One of the most popular social network sites that uses ActivityPub is [Mastodon](https://joinmastodon.org/), an open source community-owned and ad-free alternative to social network services like Twitter. But Mastodon is a huge, complex project and not the best introduction to the ActivityPub spec as a developer. So I started with [a tutorial written by Eugen Rochko](https://blog.joinmastodon.org/2018/07/how-to-make-friends-and-verify-requests/) (the principal developer of Mastodon) and created a partial reference implementation written in Node.js and Express.js called the [Express ActivityPub server](https://github.com/dariusk/express-activitypub).

The purpose of the software is to serve as the simplest possible starting point for developers who want to build their own ActivityPub applications. I picked what seemed to me like the smallest useful subset of ActivityPub features: the ability to publish an ActivityPub-compliant feed of posts that any ActivityPub user can subscribe to. Specifically, this is useful for non-interactive bots that publish feeds of information.

To get started with Express ActivityPub server in a local development environment, install

```
git clone https://github.com/dariusk/express-activitypub.git
cd express-activitypub/
npm i
```


In order to truly test the server it needs to be associated with a valid, https-enabled domain or subdomain. For local testing I like to use [ngrok](https://ngrok.com/) to test things out on one of the temporary domains that they provide. First, install ngrok using their instructions (you have to sign in but there is a free tier that is sufficient for local debugging). Next run:

```
ngrok http 3000
```


This will show a screen on your console that includes a domain like `abcdef.ngrok.io`

. Make sure to note that down, as it will serve as your temporary test domain as long as ngrok is running. Keep this running in its own terminal session while you do everything else.

Then go to your `config.json`

in the `express-activitypub`

directory and update the `DOMAIN`

field to whatever `abcdef.ngrok.io`

domain that ngrok gave you (don’t include the `http://`

), and update `USER`

to some username and `PASS`

to some password. These will be the administrative password required for creating new users on the server. When testing locally via ngrok you don’t need to specify the `PRIVKEY_PATH`

or `CERT_PATH`

.

Next run your server:

```
node index.js
```


Go to https://abcdef.ngrok.io/admin (again, replace the subdomain) and you should see an admin page. You can create an account here by giving it a name and then entering the admin user/pass when prompted. Try making an account called “test” — it will give you a long API key that you should save somewhere. Then open an ActivityPub client like Mastodon’s web interface and try following `@test@abcdef.ngrok.io`

. It should find the account and let you follow!

Back on the admin page, you’ll notice another section called “Send message to followers” — fill this in with “test” as the username, the hex key you just noted down as the password, and then enter a message. It should look like this:

![Screenshot of form](../../assets/90985bf12d8ef83d.png)

Screenshot of form

Hit “Send Message” and then check your ActivityPub client. In the home timeline you should see your message from your account, like so:

![Post in Mastodon mobile web view](../../assets/242dc3b6861069ab.png)

Post in Mastodon mobile web view

And that’s it! It’s not incredibly useful on its own but you can fork the repository and use it as a starting point to build your own services. For example, I used it as the foundation of [an RSS-to-ActivityPub conversion service](https://bots.tinysubversions.com/convert/) that I wrote ([source code here](https://github.com/dariusk/rss-to-activitypub)). There are of course other services that could be built using this. For example, imagine a replacement for something like MailChimp where you can subscribe to updates for your favorite band, but instead of getting an email, everyone who follows an ActivityPub account will get a direct message with album release info. Also it’s worth browsing the predefined [Activity Streams Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/#activity-types) to see what kind of events the spec supports by default.

## Learn More

There is a whole lot more to ActivityPub than what I’ve laid out here, and unfortunately there aren’t a lot of learning resources beyond the specs themselves and conversations on various issue trackers.

If you’d like to know more about ActivityPub, you can of course [read the ActivityPub spec](https://www.w3.org/TR/activitypub/). It’s important to know that while the ActivityPub spec lays out how messages are sent and received, the different types of messages are specified in [the Activity Streams 2.0 spec](https://www.w3.org/TR/activitystreams-core/), and the actual formatting of the messages that are sent is specified in the [Activity Streams Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/) spec. It’s important to familiarize yourself with all three.

You can join the [Social Web Incubator Community Group](https://www.w3.org/wiki/SocialCG), a W3C Community Group, to participate in discussions around ActivityPub and other social web tech standards. They have monthly meetings that you can dial into that are listed on the wiki page.

And of course if you’re on an ActivityPub social network service like Mastodon or [Pleroma](https://pleroma.social/), the #ActivityPub hashtag there is always active.

## About Darius Kazemi

Darius Kazemi is a Mozilla Fellow for 2018-2019 working with Code for Science & Society on the Dat Project. He makes internet art under the moniker Tiny Subversions and has been contributing to open source projects for ten years.

## One comment

Benjamin GoeringNovember 23rd, 2018 at 13:35