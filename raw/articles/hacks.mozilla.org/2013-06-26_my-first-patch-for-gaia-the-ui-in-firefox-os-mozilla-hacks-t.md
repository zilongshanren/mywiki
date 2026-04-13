---
title: My first patch for Gaia, the UI in Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/06/my-first-patch-for-gaia-the-ui-in-firefox-os/
author: Aras Balali Moghaddam
published: '2013-06-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are many ways of contributing to the Firefox OS project and most of these ways do not involve writing code. However, if you are a developer, there is nothing as sweet and satisfying as getting your clean patch pulled into the project. With all the excitement and energy around the Firefox OS platform, I decided it was time for me to make the leap and learn how to hack [Gaia](https://github.com/mozilla-b2g/gaia) — the Firefox OS interface.

There already exists [an excellent post about hacking Gaia for Firefox OS](https://hacks.mozilla.org/2013/01/hacking-gaia-for-firefox-os-part-1/), and [ MDN docs for hacking Gaia](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Platform/Gaia/Hacking) is the best starting point.

This post takes a slightly different path, and my focus is more on my experience getting started with hacking Gaia and testing my changes using both Firefox browser and the Geeksphone Keon. I cover the process I went through to choose a bug, write a proposed fix, and submit a pull request to Gaia.

## Choosing a bug

Firefox OS uses [bugzilla](https://bugzilla.mozilla.org/describecomponents.cgi?product=Boot2Gecko) to keep track of bugs. I had occasionally used bugzilla before but this was my first time to actually use it to find a bug to work on. I understand that it is very robust, but the UI can be a bit intimidating for newcomers like me. However, once I spent a bit of time with the various search options, I felt pretty comfortable with it. I ended up picking [a bug about a UX enhancement](https://bugzilla.mozilla.org/show_bug.cgi?id=873574) in the clock app. I chose this issue in particular because it is relatively simple and low profile. So I could work on it with little pressure. Here is the issue description that was provided in the comments:

The layout of the alarm list needs adjustment so the user can tell there are more alarms than just 4.


Lets take a look at the clock app and add some alarms to understand what the issue is.

![There is no way to see if there are more alarms above or below these four](../../assets/af0155bb3412b31e.png)


There are more than four alarms in the above screenshot, but there is no way to know that visually, before starting to scroll, and that is the issue. The bug did not provide instruction on how to fix the problem. I bounced a few ideas with another mozillian about how to solve this problem and decided to use gradients on top and bottom edge to indicate presence of more content. I had seen this type of interaction implemented in other apps before, and it works well.

## Proposed solution

I say proposed solution, because I don’t know yet if what I am implementing is acceptable and appropriate. However, it is a lot less work to implement a proposed solution and let people try it; than try to track down all the parties involved and convince them that you have a good idea to solve a UX issue. Even if this solution does not get accepted, the PR will (hopefully) promote some discussions about what would work best. Anyhow, to fix this problem I propose adding two visual elements to the top and bottom of the alarm list. We will use those element to give user a visual clue that there is more content in that direction. Next we will open the clock app within Gaia in Firefox browser to inspect it and figure out what it is made of.

## Running Gaia in Firefox

Firefox dev tools are getting better by the day (or the [night](http://nightly.mozilla.org/)), and I really like some of the new features. I was very happy to learn that I could debug Firefox OS apps in Firefox.

Currently I know of four different ways to run Firefox OS apps:

[Firefox OS simulator](https://marketplace.firefox.com/developers/docs/firefox_os_simulator)- An actual device such as Keon, Peak etc.
[A B2G desktop build](http://ftp.mozilla.org/pub/mozilla.org/b2g/nightly/latest-mozilla-b2g18/)[Firefox browser on desktop](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Using_Gaia_in_Firefox)

Each of these ways have their own pros and cons. At the moment, using Firefox browser is the best way for modifying CSS, inspecting elements, and stepping through the javascript code. I know that there is work underway to bring remote debugging to the simulator, which will hopefully become available very soon. Until then, using Firefox to open a Gaia desktop profile, is the next best thing. There are two important disadvantages to using this method. Firstly, we don’t have access to many of the phone APIs such as orientation sensor, or notifications. Secondly, we are using the latest build of Firefox to get the best developer tools, but as a result we will be using a different version of Gecko than is used by Firefox OS which in some cases may be incompatible. That being said, as long as we can write up our patch using dev tools and then test the app on a physical device, we can be pretty sure that the fix is compatible.

Regardless of which method you choose to run Gaia apps, you need to build Gaia and generate a suitable profile. By default, `make`

command generates a profile directory for a physical phone. I wanted to start inspecting the clock app in the browser, so I use the DEBUG=1 option to generate a gaia profile suitable for desktop. By default DEBUG profile will be created in `gaia/profile-debug`

folder. After a few minutes make will finish and the last line in the terminal will read something like:

`<pre lang="bash">`


Profile Ready: please run [b2g|firefox] -profile /home/user_name/Projects/gaia/profile-debug

</pre>

On my system Firefox nightly is installed in `/usr/bin/firefox-trunk`

so I will run the following command to get Gaia running in the browser:

`<pre lang="bash">`


/usr/bin/firefox-trunk -profile /home/user_name/Projects/gaia/profile-debug http://clock.gaiamobile.org:8080

</pre>

The last argument `http://clock.gaiamobile.org:8080`

is optional and is used to specify the name of the app you want to run. Instead of `clock`, you can specify the name of any of the certified apps included in Gaia, or any other application that you may add to the `apps` folder in Gaia. For more information about how to do this checkout [using Gaia in Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Using_Gaia_in_Firefox).

## Making my changes

Before getting any further, lets take care of one very important first step — creating and checking out a branch for the fix.

`<pre lang="bash">`


gaia$ git checkout -b bug-873574-alarm-scroll

</pre>

Now it was time to open the clock app in Firefox nightly. Right away I started to inspect elements in the app and look at their styles. Since I had a rough idea of the kind of visual effect I was looking for, I started playing around with CSS right in the browser. I used two pseudo elements with a gradient background, one for the top of alarm list and another for the bottom. Here is an snapshot while I was trying to position the pseudo elements properly.

![](../../assets/a8cd9570bfacb60c.png)


Here is the CSS I ended up with for creating the gradient on top of the alarm list. The code for the bottom gradient is almost the same, except it uses the `after`

psudo element and slightly different margins.

`<pre lang="CSS">`


#alarms:before {

content: '';

pointer-events: none;

background: none;

position: fixed;

width: 100%;

margin-left: -1.5em;

z-index: 10;

height: 6em;

margin-left: -1.5em;

}

#alarms.scroll-up:before {

background: -moz-linear-gradient(bottom, rgba(16, 17, 17, 0) 0%, rgba(16, 17, 17, 1) 100%);

background: linear-gradient(to top, rgba(16, 17, 17, 0) 0%, rgba(16, 17, 17, 1) 100%);

}

</pre>

Next, I started looking into the Javascript code behind the clock app. Gaia apps are currently written using a bare metal approach, without use of any large libraries or frameworks. That is an interesting topic of discussion, and I would love to see a post looking at pros and cons of this approach. As a frontend developer it does not worry me too much yet. It is too soon to say anything, I have to keep looking at the code and hope that I will identify some common patterns of programming, and figure out how abstraction is achieved.

Now that the visual elements are created, I just need to add a function to toggle the CSS classes on the alarm list element as appropriate. I hook this function up to the scroll event, so every time the user scrolls, it will re-evaluate the need for indicators. It will also need to run whenever an alarm is added or removed to the list. You can how the function is hooked in[ the PR commit](https://github.com/mozilla-b2g/gaia/pull/10336/files).

`<pre lang="javascript">`


showHideScrollIndicators: function al_showHideScrollIndicators() {

var threshold = 10; // hide indicators when scroll is close enough to an end

var element = this.alarms;

if (element.scrollTop < threshold) {

element.classList.remove('scroll-up');

} else {

element.classList.add('scroll-up');

}

if (element.scrollTop > element.scrollTopMax - threshold) {

element.classList.remove('scroll-down');

} else {

element.classList.add('scroll-down');

}

},

</pre>

Here is an example screenshot showing the subtle gradient at the bottom of the list.

## Validating Javascript

Since I made some Javascript change, I wanted to validate it with lint. The lint script in Gaia currently relies on [google closure lint](https://developers.google.com/closure/utilities/) implementation. In order to install that on debian based systems we need `easy install`

which is bundled inside python setup tools. After that we can install gjslint following [these instructions](https://developers.google.com/closure/utilities/docs/linter_howto).

`<pre lang="bash">`


$ sudo apt-get install python-setuptools

$ cd /tmp

/tmp$ sudo easy_install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz

</pre>

Once you have gjslint installed, you are good to go. Just very recently [a pre commit hook](https://github.com/mozilla-b2g/gaia/pull/10372) has been added to the project, so that before each commit it will check the files that you have changed against gjslint. If there are any errors, it will point them out to you and stop the commit.

## Previewing the changes

You can preview your changes before committing, as well as before submitting your patch to make sure you are not submitting any unintended changes. I like to use a little gtk based app called gitg to preview my changes quickly in a nice interactive GUI. Just type gitg in the command line from the gaia root directory. An even simpler way to view your changes is using the `git diff`

command.

## Submitting the PR

Once you are happy with your commit you need to push them to your own fork so you can make a pull request. Unless this is your first single commit for the PR, you would want to squash them into one by running:

`<pre lang="bash">`


gaia$ git rebase -i master

</pre>

That will take you through an interactive rebase and let you specify a new commit message. Give the commit an appropriate message such as “Bug 873574 proposed fix r=person_to_review”. One thing to note is that when you update your PR, you can completely update the commit message. Use rebase to keep your PR to only one commit, so it is nice and clean for the reviewers. Keep your commit message short and relevant. The commit message should have the bug number and a brief description of what you have done to fix it. Once the rebase is done, we can push the changes to our remote branch. First time around that branch is used to send a pull request to upstream gaia. That same branch is used later on to send subsequent updates to the PR.

`<pre lang="bash">`


gaia$ git push origin bug-873574-alarm-scroll -f

</pre>

## Asking for review

The primary channel to request review for gaia patches seems to be the bugzilla issue. Git does not integrate smoothly with bugzilla and linking to PR involves a bit of manual process. From what I understand, it is a convention to attach a small html file to the bug report containing a link to your pull request. Make sure to choose the file type as `text/html`

. Here is what I used based on examples I saw in other bug reports:

`<pre lang="xml">`


<!DOCTYPE html>

<meta charset="utf-8">

<meta http-equiv="refresh" content="1;https://github.com/mozilla-b2g/gaia/pull/10336/">

<title>Bugzilla Code Review</title>

<p>Redirecting to <a href="https://github.com/mozilla-b2g/gaia/pull/10336/">» pull request on github</a></p>

</pre>

I learnt that you can specify someone to review your PR right from the commit message, but I dont know if it is actually being used. As someone who is totally new to the project, it is bit hard to guess who would be an appropriate person to ask for review. One way to find out is to use the git blame on the areas of the code that you have changed and find out who has worked on it recently. Another way that was suggested to me is to choose someone from [owners and peers for the Gaia module](https://wiki.mozilla.org/Modules/FirefoxOS#Gaia). When you are attaching the above html file, you get a chance to enter the name of that person in a review tag, make sure to take advantage of that.

I submitted my [first PR to Gaia](https://github.com/mozilla-b2g/gaia/pull/10336). Woot woot! :)

## Updating the PR

Yup, it was not perfect ;). Chances are, you may also get a request to update your PR with some changes. PR is often a starting point for discussion about a fix. I received some comments from the UX team to change the fade color as well as some other comments about the code. I checked out my branch for that bug fix again and made those changes — making sure to rebase the commits after each update, so the PR remains with one commit.

## Now I wait — patiently

One thing about trying to contribute to a very active project such as Gaia is that you may not always get a quick feedback or review. At the time I submit my PR there was nearly 390 open PRs already in the project. I have been told that most of those are stalled, but I think it still shows that the core team has a lot to process. Since the bug I chose is not a high priority, the fix most likely will not make the cut for next release, but hopefully will be pulled in after v1 is shipped. Gaia is still a young project and it is very exciting time to join in and contribute.

## Thank You

Several people both on #gaia irc channel and local mozillians in Vancouver have helped me with the various steps along the way. I specially want to thank [James Burke](https://twitter.com/jrburke) who guided me through flashing my phone with latest version of B2G and gave me a lot of great advice about working with Gaia and Javascript development in general.

## Closing

As a frontend developer who is very excited about developing apps for Firefox OS platform, I want to learn the secrets and successful patterns for developing apps that look sharp and perform well. Tutorials, guides and documentations are very useful, but why would I want to go there if I can get what I am looking for directly from the source — the Gaia project that is. If you have not done so already, I encourage you to give it a shot and see if you can make a difference while you learn a few cool tips and tricks. I look forward to your comments and suggestions.

## About
[
Aras Balali Moghaddam ](http://arasbm)

Aras is an interaction designer and a frontend engineer living in beautiful British Columbia, Canada. He is passionate about the open web and likes to build awesome mobile web apps. You can learn more about him on [his blog](http://arasbm.com/about/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

flodJune 26th, 2013 at 03:11Aras Balali MoghaddamJune 26th, 2013 at 03:17JulienWJune 26th, 2013 at 09:05Aras Balali MoghaddamJune 26th, 2013 at 11:31