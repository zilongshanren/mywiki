---
title: 'Reintroducing the Firefox Developer Tools, part 1: the Web Console and the
  JavaScript Debugger – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/09/reintroducing-the-firefox-developer-tools-part-1-the-web-console-and-the-javascript-debugger/
author: Robert Nyman Posted; Featured Article; Firefox
published: '2013-09-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is part one, out of 5, focusing on the built-in Developer Tools in Firefox, their features and where we are now with them. The intention is to show you all the possibilities available, the progress and what we are aiming for.


Firefox 4 saw the launch of the Web Console, the first of the new developer tools built into Firefox. Since then we’ve been adding more capabilities to the developer tools, which now perform a wide range of functions and can be used to debug and analyze web applications on desktop Firefox, Firefox OS, and Firefox for Android.

![cola1](https://hacks.mozilla.org/wp-content/uploads/2013/09/cola1.png)


This is the first in a series of posts in which we’ll look at where the developer tools have got to since Firefox 4. We’ll present each tool in a short screencast, then wrap things up with a couple of screencasts illustrating specific workflow patterns that should help you get the most of the developer tools. These will include scenarios such as mobile development, and altering and debugging CSS based applications, etc.

In this first post we present the latest Web Console and JavaScript Debugger.

## Web Console

The Web Console is primarily used to display information associated with the currently loaded web page. This includes HTML, CSS, JavaScript, and Security warnings and errors. In addition network requests are displayed and the console indicates whether they succeeded or failed. When warnings and errors are detected the Web Console also offers a link to the line of code which caused the problem. Often the Web Console is the first stop in debugging a Web Application that is not performing correctly.

![webconsole](../../assets/118b97189b81278f.png)


The Web Console also lets you execute JavaScript within the context of the page. This means you can inspect objects defined by the page, execute functions within the scope of the page, and access specific elements using CSS selectors. The following screencast presents an overview of the Web Console’s features.

Take a look at the [MDN Web Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) documentation for more information.

## JavaScript Debugger

The JavaScript Debugger is used for debugging and refining JavaScript that your Web Application is currently using. The Debugger can be used to debug code running in Firefox OS and Firefox for Android, as well as Firefox Desktop. It’s a full-featured debugger providing watch expressions, scoped variables, breakpoints, conditional expressions, step-through, step-over and run to end functionality. In addition you can change the values of variables at run time while the debugger has paused your application.

![debugger](../../assets/69636578ff8c3031.png)


The following screencast illustrates some of the features of the JavaScript Debugger.

For more information on the JavaScript Debugger, see the [MDN Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) documentation.

## Learn More

These screencasts give a quick introduction to the main features of these tools. For the full details on all of the developer tools, check out the full [MDN Tools](https://developer.mozilla.org/en-US/docs/tools) documentation.

## Coming Up

In the next post in this series we will be delving into the Style Editor and the Scratchpad. Please give us your feedback on what features you would like to see explained in more detail within the comments.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 57 comments

jamEsSeptember 24th, 2013 at 06:55Robert Nyman [Editor]September 24th, 2013 at 07:06jamEsSeptember 24th, 2013 at 07:09AndiioSeptember 24th, 2013 at 07:40Michael BeckwithSeptember 24th, 2013 at 08:44Nick FitzgeraldSeptember 24th, 2013 at 09:22MindaugasSeptember 24th, 2013 at 10:09Robert Nyman [Editor]September 25th, 2013 at 00:30MindaugasSeptember 25th, 2013 at 10:26Jeff GriffithsSeptember 25th, 2013 at 10:36Jeff GriffithsSeptember 25th, 2013 at 11:38Ivan DejanovicSeptember 24th, 2013 at 11:15Jeff GriffithsSeptember 24th, 2013 at 13:14Jeff CarlsenSeptember 25th, 2013 at 09:05jamEsSeptember 26th, 2013 at 05:33Mike RatcliffeOctober 6th, 2013 at 13:39Jeff GriffithsSeptember 26th, 2013 at 08:45Fernando BrianoSeptember 25th, 2013 at 01:38Robert Nyman [Editor]September 25th, 2013 at 04:50pdSeptember 25th, 2013 at 09:53RohitSeptember 25th, 2013 at 10:33Raymond CamdenSeptember 26th, 2013 at 03:54Jeff GriffithsSeptember 26th, 2013 at 08:50Raymond CamdenSeptember 26th, 2013 at 13:21Jeremy SmithSeptember 27th, 2013 at 09:01Robert Nyman [Editor]September 27th, 2013 at 13:03Arno.NyhmSeptember 28th, 2013 at 10:31Robert Nyman [Editor]September 30th, 2013 at 01:42Saje DennisOctober 1st, 2013 at 04:12Jeff GriffithsOctober 1st, 2013 at 08:52Marian KostadinovOctober 1st, 2013 at 04:42Jeff GriffithsOctober 2nd, 2013 at 06:56Marian KostadinovOctober 4th, 2013 at 09:12Jeff GriffithsOctober 4th, 2013 at 09:29Arno.NyhmOctober 2nd, 2013 at 08:25JoãoOctober 4th, 2013 at 02:50Robert Nyman [Editor]October 9th, 2013 at 02:57VytautasOctober 6th, 2013 at 12:27jaborandiOctober 9th, 2013 at 04:34Raymond CamdenOctober 10th, 2013 at 03:58Robert Nyman [Editor]October 10th, 2013 at 04:49Raymond CamdenOctober 10th, 2013 at 04:57Mike RatcliffeOctober 10th, 2013 at 08:31Will BambergOctober 10th, 2013 at 09:56Raymond CamdenOctober 10th, 2013 at 05:02Robert Nyman [Editor]October 10th, 2013 at 13:32RohitOctober 10th, 2013 at 05:46Raymond CamdenOctober 10th, 2013 at 07:12Raymond CamdenOctober 10th, 2013 at 07:13Marian KostadinovOctober 14th, 2013 at 03:46Mike RatcliffeOctober 14th, 2013 at 08:45Marian KostadinovOctober 14th, 2013 at 11:48Jeff GriffithsOctober 15th, 2013 at 13:41Andrés Correa CasablancaOctober 17th, 2013 at 02:50Mike RatcliffeOctober 17th, 2013 at 06:45Ethan MarcotteOctober 17th, 2013 at 15:21Mike RatcliffeOctober 18th, 2013 at 13:24