---
title: Launcher.io – Launch and run free open-source web applications in just 30 seconds
  – a WebFWD project – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/launcher-io-launch-and-run-free-open-source-web-applications-in-just-30-seconds-a-webfwd-project/
author: Maciej Skierkowski
published: '2012-12-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There is no longer any doubt: web apps are the focal point of the cloud. From database-as-a-service to platform-as-a-service to security-as-a-service and beyond, the entire *aaS model has the web app as its center of gravity.

If you’re a full-fledged developer, then taking full advantage of an app-centric universe is no big deal. Creating new web apps from scratch using frameworks like Ruby on Rails, Drupal, Django, or hundreds of others and then deploying those apps in the cloud is part of your daily bread and butter.

## The mission

The mission of [Launcher.io](https://launcher.io/) is quite simply to make it vastly easier for developers and non-developers alike to create and deploy their own web apps with a single click of the mouse. Launcher was founded by me, former AppFog director of product Maciej Skierkowski, and I have taken what I have learned in my time in the platform-as-a-service (PaaS) space and used that knowledge to make app deployment even more dead-simple than a typical PaaS platform does.

## How it works

So how does it work? Launcher enables you to deploy so-called “jumpstart” apps with a single click. If you’ve signed up for a Launcher account, all you have to do is click on a jumpstart’s button and you’ll be prompted for basic information, and Launcher will do the rest of the work.

From there, you can manage your app however you like. Frameworks like Drupal, WordPress, or Concrete5 provide you with an intuitive in-browser interface for modifying your app, whereas frameworks like Ruby on Rails, Flask, ActionHero.js, and others will require more in-depth web development knowledge.

## Launcher: great for non-developers

The benefit for non-developers is that it makes using all of these platforms easier than ever before. Want to start a new WordPress blog? All it takes is signing up to Launcher and clicking a button, and your blog is up and running in the cloud. The rest is up to you. Are you starting a company and want to set up Drupal to run your content management system and ThinkUp for social media analytics? Also a click and a few keystrokes away.

## Launcher: even better for developers

For developers, the benefits of Launcher involve speedier adoption of new apps and frameworks amongst potential users. Let’s say that I’m a Java developer and I just created the most bleeding-edge CMS currently available. If Drupal is a Cadillac, then my new CMS platform is a fresh-off-the-assembly-line Maserati: it’s blazingly fast, it has a wonderful in-browser console, and it has millions of useful plugins that Just Work.

If users wanted to use my CMS in a pre-Launcher world, they’d have to do it the hard way: download it onto their machine, run appropriate configs to make it cloud-ready, learn how to use a VPS (or a PaaS, which is a very recent development), and so on. But with Launcher, potential users can give my new CMS a spin in just a few seconds and have it running in the cloud, and making my CMS Launcher-ready provides little to no modification on my part.

The app landscape is extremely competitive, and anything that can speed potential adoption that quickly is a massive win for me as a developer. Launcher is simply an unprecedentedly direct pipeline to my new SaaS product.

## Under the hood

Surprisingly enough, Launcher is amazingly simple in how it works behind the scenes. When an end user clicks on a jumpstart, the browser makes an AJAX request to a remote service kicking-off a Resque worker that deploys the app with AppFog or CloudFoundry.com. Setting up an HTML page to handle a Launcher jumpstart involves simply loading the jQuery and Pusher JavaScript libraries and inserting a few lines of JavaScript (check out the docs for more info).

Your app will, however, need to be registered with Launcher to be included in the [Launcher App Store](https://launcher.io/jumpstarts). If you’re interested in doing so, don’t hesitate to get in contact with me, as I am looking to expand the range of offerings in the app store in the coming months.

He’s also looking to expand the number of PaaS providers that support jumpstarts. At the moment, Launcher enables you to instantaneously deploy apps on either AppFog or Cloud Foundry, but Launcher is in principle compatible with any Cloud Foundry-compatible PaaS API. If you’d like to add a new PaaS, simply go to the Providers page, click “Add Provider,” and input a name, API endpoint, and other information.

## More on the way

Launcher is a new project, and has a great deal more in store for both developers and end users. Jumpstarts for OpenPhoto, Redmine, and SugarCRM, to name just a few are coming soon.

If you’re a developer, startup, or enterprise looking to take advantage of Launcher, email maciej@skierkowski.com for more information.

## About
[
Maciej Skierkowski ](https://launcher.io/)

I am the CEO/Founder of Launcher, a service to make it vastly easier for developers and non-developers alike to create and deploy their own web apps with a single click of the mouse. Before starting Launcher I was the Director of Product at AppFog, based out of Portland, Oregon. I just love making developers' lives easier.

## 5 comments

David MulderDecember 18th, 2012 at 11:06Maciej SkierkowskiDecember 18th, 2012 at 11:11xsohDecember 18th, 2012 at 22:32Maciej SkierkowskiDecember 19th, 2012 at 10:12IJobAsia.comDecember 19th, 2012 at 09:51