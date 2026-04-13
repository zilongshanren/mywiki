---
title: Wercker – Continuous Delivery Made Easy – a webFWD project – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2013/02/wercker-continuous-delivery-made-easy-a-webfwd-project/
author: Micha Hernandez van Leuffen
published: '2013-02-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There is a great quote by Marc Andreessen who said that [“software is eating the world”](http://online.wsj.com/article/SB10001424053111903480904576512250915629460.html). What Marc means by this is that software is defining every industry we know; we’re no longer buying records at our local retailer but stream them via [Rdio](http://rdio.com) or [Spotify](http://spotify.com). [Skype](http://skype.com) is now the largest telecommunications provider and we’re even talking about the [software-defined data-center](http://www.informationweek.com/cloud-computing/infrastructure/vmware-launches-software-defined-data-ce/240143004).

The [cloud](http://aws.amazon.com) [has](http://heroku.com) [become](http://openstack.org) the defacto distribution mechanism for these software services, but has also allowed for disruptive change in how these services are delivered and consumed. Whereas it used to be the case that you would have to purchase a new version of your favorite [word processing software](http://office.microsoft.com/) at your local retailer, with the cloud, updates can be pushed out [incrementally](http://docs.google.com).

## Introducing wercker

The key enabler for this new way of developing software is [continuous delivery](http://en.wikipedia.org/wiki/Continuous_delivery). Software is eating the world, and [wercker](http://beta.wercker.com) makes it taste better.

There are several successful companies out there which are big proponents of continuous delivery such as [Netflix](https://signup.netflix.com/) and [Etsy](http://www.etsy.com/). It is wercker’s mission to democratize continuous delivery for every developer and was founded on this very same premise in the beginning of last year by me, Micha Hernandez van Leuffen, and my cofounder Wouter Mooij out of frustration with existing solutions.

This [video introduces wercker](http://vimeo.com/53756616) and presents our vision on the product:

## How it works

Wercker’s flow is simple; it integrates with popular version controls platforms such as [Github](http://github.com) and [Bitbucket](http://bitbucket.org) on one end and [Infrastructure-as-a-Service](http://aws.amazon.com) [providers](http://rackspace.com) and Platform clouds like [Heroku](http://heroku.com) on the other end.

We run any unit tests you might have included in your project and subsequently present the results on a comprehensive dashboard.

You are able to define different environments or deploy targets for, for instance staging or production to which you can deploy your project with a push of a button.

Software is better developed together so wercker also captures the social dynamics that are paired with continuous delivery. The activity feed showcases who in your team broke the build or deployed to which environment. This increases transparency and trust within your team.

## Open Source

Apart from offering wercker for free to open source projects we are also in the process of opening up wercker’s build environments. These environments are similar to Heroku’s [buildpacks](https://devcenter.heroku.com/articles/buildpacks), allowing developers to define not only their own programming stack that they would like to use on wercker, but also the various build and test steps that they want to run.

New languages and frameworks can be integrated with ease as we’ve built these environments upon Chef [cookbooks](http://community.opscode.com/cookbooks) which can subsequently be used for both provisioning and deployment as well. Cookbooks and recipes are already a very big open source movement, which we’re stimulating even more.

## The Future

We’re very excited that we’ve [raised](http://blog.wercker.com/2013/01/23/Funding.html) a [seed](http://techcrunch.com/2013/01/23/wercker-makes-code-delivery-easy-gets-seed-funding-from-shamrock-ventures-greylock-venture-partners-and-a-list-technologists/) [round](http://thenextweb.com/insider/2013/01/23/continuous-code-platform-wercker-claims-seed-funding-to-develop-internationally/) led by [Shamrock Ventures](http://www.shamrockventuresbv.com), Amsterdam-based MicroVC [Vitulum Ventures](http://vitulumventures.com) and [Greylock Partners](http://www.greylock.com/). The funding will help us grow our platform and expand our operations.

If you are a developer, sign up for the beta at [http://beta.wercker.com](http://beta.wercker.com). We are also interested in hearing what programming stacks developers are leveraging for their applications and to which environments they are deploying.

## About Micha Hernandez van Leuffen

Micha Hernandez van Leuffen is the cofounder and CEO of Wercker, a continuous delivery platform in the cloud. It is Wercker's aim to democratize continuous delivery and increase developer velocity.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.