---
title: The Translation of the Firetext App – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/03/translation-of-firetext-app/
author: Joshua Smith
published: '2014-03-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The History

[Firetext](https://marketplace.firefox.com/app/firetext) is an [open-source](https://github.com/Codexa/Firetext) word processor. The project was started in early 2013 by [@HRanDEV](https://github.com/HRanDEV/), [@logan-r](https://github.com/logan-r/), and me ([@Joshua-S](https://github.com/Joshua-S/)). The goal of the project was to provide a user-friendly editing experience, and to fill a major gap in functionality on Firefox OS.

In the year since its initiation, Firetext became one of the top ten most popular productivity apps in the Firefox Marketplace. We made a myriad of new additions, and Firetext gained Dropbox integration, enabling users to store documents in the cloud. We also added Night Mode, a feature that automatically adjusts the interface to the surrounding light levels. There was a new interface design, better performance, and web activity support.

Even with all of these features, Firetext’s audience was rather small. We had only supported the English language, and according to [Exploredia](http://exploredia.com/how-many-people-in-the-world-speak-english-2013), only 17.65% of the world’s population speak English fluently. So, we decided to localize Firetext.

## The Approach

After reading a Hacks post about [Localizing Firefox Apps](https://hacks.mozilla.org/2013/08/localizing-firefox-os-apps/), we determined to use a combination of [webL10n](https://github.com/fabi1cazenave/webL10n) and Google Translate as our localization tools. We decided to localize in the languages known by our contributors (Spanish and German), and then use Google Translate to do the others. Eventually, we planned to grow a community that could contribute translations, instead of just relying on the often erratic machine translations.

## The Discovery

A few months passed, and still no progress. The task was extremely daunting, and we did not know how to proceed. This stagnation continued until I stumbled upon a second Hacks post, [Localizing the Firefox OS Boilerplate App](https://hacks.mozilla.org/2014/01/localizing-the-firefox-os-boilerplate-app/).

It was like a dream come true. Mozilla had started a program to help smaller app developers with the localization process. We could benefit from their larger contributor pool, while helping them provide a greater number of apps to foreign communities.

I immediately contacted Mozilla about the program, and was invited to [set up a project on Transifex](https://www.transifex.com/organization/mozilla-tech-evangelism/). The game was on!

## The Code

I started by creating a locales directory that would contain our translation files. I created a locales.ini file in that directory to show webL10n where to find the translations. Finally, I added a folder for each locale.

![locales.ini - Firetext](../../assets/95b854804c0f957e.png)


I then tagged each translatable element in the html files with a data-l10n-id attribute, and localized alert()s and our other scripted notifications by using webL10n’s document.webL10n.get() or _() function.

It was time to add the translations. I created a app.properties file in the locales/en_US directory, and referenced it from locales.ini. After doing that, I added all of the strings that were supposed to be translated.

![app.properties - Firetext](../../assets/5463666a54375585.png)


webL10n automatically detects the user’s default locale, but we also needed to be able to change locales manually. To allow this, I added a select in the Firetext settings panel that contained all of the prospective languages.![Settings - Firetext](../../assets/1ff6128ab7d66d5f.png)


Even after all of this, Firetext was not really localized; we only had an English translation. This is where Transifex comes into the picture.

## The Translation

I created a project for Firetext on Transifex, and then added a team for each language on our GitHub issue. I then uploaded the app.properties file as a resource.

I also uploaded the app description from our manifest.webapp for translation as a separate resource.

Within hours, translations came pouring in. Within the first week, Hebrew, French, and Spanish were completely translated! I added them to our GitHub repository by downloading the translation properties file, and placing it in the appropriate locale directory. I then enabled that language in the settings panel. The entire process was extremely simple and speedy.

## The Submission

Now that Firetext had been localized, I needed to submit it back to the Mozilla Marketplace. This was a fairly straight forward process; just download the zip, extract git files, and add in the API key for our error reporting system.

In less than one day, Firetext was approved, and made available for our global user base. Firetext is now available in eight different languages, and I can’t wait to see the feedback going forward!

## The Final Thoughts

In retrospect, probably the most difficult part of localizing Firetext was supporting RTL (Right To Left) languages. This was a bit of a daunting task, but the results have totally been worth the effort! All in all, localization was one of the easiest features that we have implemented.

As Swiss app developer Gerard Tyedmers, creator of [grrd’s 4 in a Row](https://marketplace.firefox.com/app/grrds-4-in-a-row/) and [grrd’s Puzzle](https://marketplace.firefox.com/app/grrds-puzzle-1/), said:



“…I can say that localizing apps is definitely worth the work. It really helps finding new users.

The l10n.js solution was a very useful tool that was easy to implement. And I am very happy about the fact that I can add more languages with a very small impact on my code…”


I couldn’t agree more!

*Editor’s Note: The Invitation*

*Have a great app like Firetext? You’re invited too!* We encourage you to join [Mozilla’s app localization project on Transifex](https://www.transifex.com/organization/mozilla-tech-evangelism/). With a localized app, you can extend your reach to include users from all over the world, and by so doing, help to support a global base of open web app users.

For translators, mobile app localization presents some interesting translation and interface design challenges. You’ll need to think of the strings you’re working with in mobile scale, as interaction elements on a small screen. The localizer plays an important role in creating an interface that people in different countries can easily use and understand. Please, [get involved with Firetext](https://www.transifex.com/projects/p/firetext/) or [one of our other projects](https://www.transifex.com/organization/mozilla-tech-evangelism/).

This project is just getting started, and [we’re learning as we go](https://developer.mozilla.org/en-US/Firefox_OS/App_Localization_with_Transifex). If you have questions or issues not addressed by existing resources such the [Hacks blog series on app localization](https://hacks.mozilla.org/category/apps/localization/), Transifex help pages, and other articles and repos referenced above, you can [contact us](mailto:appsdev@mozilla.com?subject=app_localization). We’ll do our best to point you in the right direction. *Thanks!*

## About Joshua Smith

Actor, Coder, Mozillian, and Student from New York.
Joshua was one of the founders of [Codexa](http://codexa.org/), and started the [Firetext project](https://marketplace.firefox.com/app/firetext).

## 2 comments

Abin AbrahamMarch 25th, 2014 at 10:36Havi HoffmanMarch 25th, 2014 at 12:17