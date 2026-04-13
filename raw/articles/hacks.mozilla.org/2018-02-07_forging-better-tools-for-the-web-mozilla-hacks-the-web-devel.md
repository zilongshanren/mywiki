---
title: Forging Better Tools for the Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/02/forging-better-tools-for-the-web/
author: Dustin Driver
published: '2018-02-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## A Firefox DevTools Retrospective

2017 was a big year for Firefox DevTools. We updated and refined the UI, refactored three of the panels, squashed countless bugs, and shipped several new features. This work not only provides a faster and better DevTools experience, but lays the groundwork for some exciting new features and improvements for 2018 and beyond. We’re always striving to make tools and features that help developers build websites using the latest technologies and standards, including JavaScript frameworks and, of course, CSS Grid.

To better understand where we’re headed with Firefox Devtools, let’s take a quick look back.

*2016*

In 2016, the DevTools team kicked off an ambitious initiative to completely transition DevTools away from XUL and Firefox-specific APIs to modern web technologies. One of the first projects to emerge was [debugger.html](http://firefox-dev.tools/debugger.html/).

Debugger.html is not just an iteration of the old Firefox Debugger. The team threw everything out, created an empty repo, and set out to build a debugger from scratch that utilized reusable React components and a Redux store model.

The benefits of this modern architecture become obvious right away. Everything was more predictable, understandable, and testable. This approach also allows debugger.html to target more than just Firefox. It can target other platforms such as Chrome and Node.

We also shipped a new [Responsive Design Mode in 2016](https://hacks.mozilla.org/2016/11/new-responsive-design-mode-rdm-lands-in-firefox-dev-tools/) that was built using only modern web technologies.

*2017*

Last year, we continued to build on the work that was started in 2016 by building, and rebuilding parts of Firefox DevTools (and adding new features along the way). As a result, our developer tools are faster and more reliable. We also launched Firefox Quantum, which focused on browser speed, and performance.

### Debugger

The debugger.html work that started in 2016 [shipped to all channels with Firefox 56](https://hacks.mozilla.org/2017/10/firefox-56-last-stop-before-quantum/). We also added several new features and improvements, including better search tools, collapsed framework call-stacks, async stepping, and more.

### Console

Just as with debugger.html, we shipped [a brand-new Firefox console with Firefox Quantum](https://hacks.mozilla.org/2017/11/new-in-firefox-58-developer-edition/). It has a new UI, and has been completely rewritten using React and Redux. This new console includes several new improvements such as the ability to collapse log groups, and the ability to inspect objects in context.

### Network Monitor

We also [shipped a new network monitor](https://hacks.mozilla.org/2017/06/network-monitor-reloaded/) to all channels in Firefox 57. This new Network Monitor has a new UI, and is (you guessed it) built with modern web technologies such as React and Redux. It also has a more powerful filter UI, new Netmonitor columns, and more.

### CSS Grid Layout Panel

Firefox 57 shipped with [a new CSS Grid Layout Panel](https://hacks.mozilla.org/2017/06/new-css-grid-layout-panel-in-firefox-nightly/). CSS Grid is revolutionizing web design, and we wanted to equip designers and developers with powerful tools for building and inspecting CSS Grid layouts. You can [read all about the panel features here](https://hacks.mozilla.org/2017/10/an-introduction-to-css-grid-layout-part-1/); highlights include an overlay to visualize the grid, an interactive grid outline, displaying grid area names, and more.

### Photon UI

We also did [a complete visual refresh of the DevTools](https://hacks.mozilla.org/2017/09/developer-edition-devtools-update-now-with-photon-ui/) themes to coincide with the launch of Firefox Quantum and the new Photon UI. This refresh brings a design that is clean, slick, and easy to read.

## 2018 and Beyond

All of this work has set up an exciting future for Firefox DevTools. By utilizing modern web technologies, we can create, test, and deploy new features at a faster pace than when we were relying on XUL and Firefox-specific APIs.

So what’s next? Without giving too much away, here are just some of the areas we are focusing on:

### Better Tools for Layouts and Design

This is 2018 and static designs made in a drawing program are being surpassed by more modern tools! Designing in the browser gives us the freedom to experiment, innovate, and build faster. Speaking with hundreds of developers over the past year, we’ve learned that there is a huge desire to bring better design tools to the browser.

We’ve been thrilled by overwhelmingly positive feedback around the CSS Grid Layout Panel and we’ve heard your requests for more tools that help design, build, and inspect layouts.

We are making a Firefox Inspector tool to make it easier to write Flexbox code. What do you want it to do the most? What’s the hardest part for you when struggling with Flexbox?


–[@jensimmons, 14 Nov 2017]I’m so pleased about this reaction to the Firefox Grid Inspector. That was the plan. We’ve just gotten started. More super-useful layout tools are coming in 2018.


–[@jensimmons, 24 Nov 2017]

### Better Tools for Frameworks

2017 was a banner year for JavaScript frameworks such as [React](https://reactjs.org/) and [Vue](https://vuejs.org/). There are also older favorites such as [Angular](https://angular.io/) and [Ember](https://www.emberjs.com/) that continue to grow and improve. These frameworks are changing the way we build for the web, and we have ideas for how Firefox DevTools can better equip developers who work with frameworks.

### An Even Better UI

The work on the Firefox DevTools UI will never be finished. We believe there is always room for improvement. We’ll continue to work with the Firefox Developer community to test and ship improvements.

New DevTools poll: Which of these three toolbar layouts do you prefer for the Network panel?


–[@violasong]

### More Projects on GitHub

We tried something new when we started [building debugger.html](https://github.com/firefox-devtools/debugger.html). We decided to build the project in GitHub. Not only did we find a number of new contributors, but we received a lot of positive feedback about how easy it was to locate, manage, and work with the code. We will be looking for more opportunities to bring our projects to GitHub this year, so stay tuned.

## Get Involved

Have an idea? Found a bug? Have a (gasp) complaint? We will be listening very closely to devtools users as we move into 2018 and we want to hear from you. Here are some of the ways you can join our community and get involved:

### Join us on Slack

You can join our [devtools.html Slack community](https://devtools-html-slack.herokuapp.com/). We also hang out on the #devtools channel on [irc.mozilla.org](http://irc.mozilla.org/)

### Follow us on Twitter

We have an official account that you can follow, but you can also follow various team members who will occasionally share ideas and ask for feedback. Follow [@FirefoxDevTools here](https://twitter.com/FirefoxDevTools).

## Contribute

If you want to get your hand dirty, you can become a contributor:

### Download Firefox Developer Edition

[Firefox Developer Edition](https://www.mozilla.org/firefox/developer/) is built specifically for developers. It provides early access to all of the great new features we have planned for 2018.

Thank you to everyone who has contributed so far. Your tweets, bug reports, feedback, criticisms, and suggestions matter and mean the world to us. We hope you’ll join us in 2018 as we continue our work to build amazing tools for developers.

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.

## 8 comments

JimFebruary 7th, 2018 at 14:43Dustin DriverFebruary 8th, 2018 at 09:19OlegFebruary 11th, 2018 at 15:20PaatFebruary 8th, 2018 at 02:17Dustin DriverFebruary 8th, 2018 at 09:23LucaFebruary 9th, 2018 at 00:22Alex LeducFebruary 14th, 2018 at 13:07NathanFebruary 15th, 2018 at 09:12