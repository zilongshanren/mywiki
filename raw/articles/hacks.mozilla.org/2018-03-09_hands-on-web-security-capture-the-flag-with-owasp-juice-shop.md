---
title: 'Hands-On Web Security: Capture the Flag with OWASP Juice Shop – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2018/03/hands-on-web-security-capture-the-flag-with-owasp-juice-shop/
author: Simon Bennetts
published: '2018-03-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As a developer, are you confident that you know what you need to know about web security? Wait, maybe you work in infosec. As a security specialist, are you confident that the developers you work with know enough to do the right thing?

Often, these aren’t easy questions to answer, even for seasoned security professionals working with world class software engineers as we do at Mozilla.

OK, you can watch tutorial videos and take a variety of online tests, but it’s always more fun to try things in real life with a group of friends or colleagues. Our recent Mozilla all-hands was one of those opportunities.

A [Capture the Flag](https://en.wikipedia.org/wiki/Capture_the_flag#Computer_security) (CTF) event offer a sociable hands-on way to learn about security and they are often a tradition at security conferences.

I’m part of the Mozilla [Firefox Operations Security team](https://wiki.mozilla.org/Security/FirefoxOperations) and we work closely with all Mozilla developers to make sure that the core services Mozilla relies on to build, ship, and run Firefox are as secure as possible.

In this retrospective, I’ll show how you can easily set up a CTF event using free and open source software, as the Security team did back in December, when we gathered in Austin for Mozilla [All Hands](https://wiki.mozilla.org/All_Hands) event.

## Customizing OWASP Juice Shop

We chose [OWASP Juice Shop](https://www.owasp.org/index.php/OWASP_Juice_Shop_Project), a web app designed intentionally for training purposes to be insecure. Juice Shop uses modern technologies like Node.js, Express and AngularJS, and provides a wide range of security challenges ranging from the simple to the complex. This was important for us since our participants had a wide range of skills, and included developers with little formal security training to professional penetration testers.

Juice Shop is a “single user application,” but it comes with a CTF mode and detailed instructions for [Hosting a CTF Event](https://bkimminich.gitbooks.io/pwning-owasp-juice-shop/content/part1/ctf.html). When this is turned on, the application generates “CTF-tokens” anytime someone solves one of the challenges. These can then be uploaded to a central scoring server. The CTF mode also disables the hints which might have made some of the challenges too easy for our more advanced players.

Juice Shop can be run in a wide variety of ways, but to make it easy for your participants I recommend using a [docker image](https://docs.docker.com/get-started/), as this has only one dependency: docker.

You can find the official Juice Shop docker image here: [https://hub.docker.com/r/bkimminich/juice-shop/](https://hub.docker.com/r/bkimminich/juice-shop/) or you can build your own if you want to customize it. You can [customization instructions online](https://bkimminich.gitbooks.io/pwning-owasp-juice-shop/content/part1/customization.html).

We enabled the built-in CTF mode and changed the application name and the example products in order to make it feel more Firefox-y and to hide its origin (as solutions for the Juice Shop challenges are easily found on the internet).

Once we were happy with our changes we uploaded our image to [dockerhub: mozilla/ctf-austin](https://hub.docker.com/r/mozilla/ctf-austin/)

## Setting Up a Scoring Server

You’ll want to set up a scoring server, to allow participants to upload their CTF-tokens and compare their scores with everyone else. It definitely helped encourage competition among our participants!

A scoring server should also provide a summary of each of the challenges and the points each challenge is worth. For this we used [CTFd](https://ctfd.io/) – it’s [easy to install](https://github.com/CTFd/CTFd#install) and there’s an officially supported tool for importing the Juice Shop challenges into CTFd which can be run using:

```
npm install -g juice-shop-ctf-cli
juice-shop-ctf
```


You’re then presented with a set of questions that allow you to tune the setup to your requirements.

## Running the CTF

To get your CTF event underway you just need to tell participants the URL of your CTFd server and how to get Juice Shop running locally. If you are using the official image, here’s how to go about running Juice Shop locally:

```
docker pull bkimminich/juice-shop
docker run -d -e "NODE_ENV=ctf" -p 3000:3000 bkimminich/juice-shop
```


If you’re using your own image then change the image name, and if you have the CTF option enabled then your code wont need the `-e "NODE_ENV=ctf"`

part:

```
docker pull mozilla/ctf-austin
docker run -d -p 3000:3000 mozilla/ctf-austin
```


In either case, participants will now be able to access their own local copy of Juice Shop via [http://localhost:3000/](http://localhost:3000/)

Although some of the Juice Shop security challenges can be solved just by using Firefox, a security tool that proxies your browser will really help.

A good option for this is [OWASP ZAP](https://www.owasp.org/index.php/ZAP) (for which I’m the project leader), a free and open source security tool specifically designed to find security vulnerabilities in web applications.

ZAP sits between your browser and the application you want to test and shows all of the traffic that flows between them. It also allows you to intercept and change that traffic and provides a wide range of automated and manual features that can be used to test the application. If you use ZAP you won’t need to change your browser settings, as ZAP can launch Firefox (or any other locally installed browser) preconfigured to proxy through ZAP.

Remind all participants to explore Juice Shop as thoroughly as they can – you can’t find all the issues if there are features that you are not aware of. Suggest that they start with the easiest challenges w(the ones with the fewest points) and work upwards, as the challenges are designed to get progressively harder.

If you are running the CTF over several days (as we did), it’s a good idea to be available for help and advice. We set up a private irc channel, a Google group, and held daily check-in sessions where anyone could come along and ask us questions about the event, and get help on solving the challenges.

On the last day of our event, we held a final session to congratulate the winners, revealed the app’s origin and handed out Juice Shop stickers kindly provided by Björn Kimminich (the JuiceShop project lead).

## Outcomes and Next Steps

Running a Capture the Flag event is a great way to raise security awareness and knowledge within a team, a company, or an organization.

Juice Shop is an ideal application for a CTF as its based on modern web technologies and includes a wide range of challenges. It’s very well thought out and well supported.The fact that it’s a *real* application with realistic vulnerabilities, rather than a set of convoluted tasks, makes it ideal for learning about application security.

Our Mozilla/Firefox custom Juice Shop app is available at [https://github.com/mozilla/ctf-austin](https://github.com/mozilla/ctf-austin). Unless you particularly want to use a Mozilla-branded version, we recommend the original Juice Shop app: [https://github.com/bkimminich/juice-shop](https://github.com/bkimminich/juice-shop). (Note: It has already been updated since we forked our copy.)

And if you haven’t played with it yet, then I strongly recommend doing so. It’s a lot of fun and you’ll almost certainly learn something.

In the end, over 20 people registered for our event and their feedback was very positive:


“The cookie /[JWT]stuff is the most illuminating part of this.”

“This whole thing is excellent thanks for putting it together.”


“I hate the fact I can’t focus on my things because I’d like to solve more ctf tasks and learn something.”


“It’s awesome because I’m planning to improve my sec skills.”


“This has been a lot of fun – thanks for setting it up.”

Not surprisingly 2 of our pen testers who took part did very well, but they were given a run for their money by one of our operations staff who clearly knows a lot about security!

Do you have a knack for uncovering security vulnerabilities? At Mozilla, we have a [Web and Services Bug Bounty Program](https://www.mozilla.org/en-US/security/web-bug-bounty/). We welcome your help in making Mozilla even more secure. You could even earn some bounty rewards for your efforts. And we’re always looking for contributors to help us make ZAP better, so if that sounds interesting, have a look at [Contributing to OWASP ZAP](https://github.com/zaproxy/zaproxy/blob/develop/CONTRIBUTING.md).

## One comment

Björn KimminichMarch 9th, 2018 at 02:29