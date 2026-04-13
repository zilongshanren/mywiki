---
title: Introducing TranslationTester and localization support for Open Web Apps –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/05/introducing-translationtester-and-localization-support-for-open-web-apps/
author: Robert Nyman
published: '2014-05-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When building [Open Web Apps](https://developer.mozilla.org/en/Apps), one important factor is to make your content available to as many possible, and one way to do that is to make it available in more than one language. Therefore we want to make it as easy as possible for you, both with a complete code repository to get started and updated documentation and possibilities to get translations for your apps.

We are now also offering [a way to have your app set up and to get connected to localizers directly](https://hacks.mozilla.org#help-with-translations)!

## Presenting TranslationTester

Based on the great work and content by Jason in [Localizing Firefox OS Apps](https://hacks.mozilla.org/2013/08/localizing-firefox-os-apps/) and Christie in [Localizing the Firefox OS Boilerplate App](https://hacks.mozilla.org/2014/01/localizing-the-firefox-os-boilerplate-app/), I’ve been working on simplifying the set-up for localization.

Above articles describe many facets and possibilities available, and to complement that, I wanted to be able to offer the most basic code and structure for most use cases: basically, just add translations and you’re good to go!

This lead to the creation of the [TranslationTester code repository](https://github.com/robnyman/TranslationTester/), available on GitHub.

## From no translation to localized app in less than 4 minutes!

Based on the TranslationTester, Will Bamberg has put together a nice and short screencast showing the exact process of going from no translations to having support in just a few minutes!

In the [app-l10n-example](https://github.com/wbamberg/app-l10n-example) repository you have versions of the before and after stages in this screencast, and all of [the localization process is described on MDN](https://developer.mozilla.org/en-US/Apps/Build/Localization/Getting_started_with_app_localization).

### How to localize an app

These are the things needed to localize an app. All of them are included in the TranslationTester repository, but included here to show easy it is to get started, or continue to build on the TranslationTester platform for your app.

#### Mark up the HTML

For any element that you want to have its text localized, add a `data-l10n-id`

attribute to the desired element. For example:

Winter for real


#### Create translations

In the `locales`

directory, you have a directory for each language, and can just add new ones for new languages. In each language directoy you create an `app.properties`

file which will contain all your translations for that language (optionally you can also create a `manifest.properties`

file for the name and description of the app, unless you edit it in the main [ manifest.webapp](https://developer.mozilla.org/en-US/Apps/Build/Manifest) for your app).

#### Include `l10n.js`


By including the `l10n.js`

file, the translations for respective language’s `app.properties`

file will be applied to element with the corresponding `data-l10n-id`

attribute.

#### Add “name” and “description” translations

The translations for the `name`

and `description`

for your app could be added to the main [ manifest.webapp](https://developer.mozilla.org/en-US/Apps/Build/Manifest) file, or in an optional

`manifest.properties`

under each locale’s directory.## How to view different locales

To view your app with a different locale, change the language in Firefox/App Manager:

- All platforms
- Set the desired locale to test in JavaScript, e.g:
document.webL10n.setLanguage("es");

- App Manager/Firefox OS
[Language setting in the Settings app](https://support.mozilla.org/en-US/kb/change-default-language-firefox-os?esab=a&s=language&r=0&as=s)- Firefox
- Choose language under
`Preferences > Content > Languages`

. More information in[Set content language in Firefox](https://support.mozilla.org/en-US/kb/settings-fonts-languages-pop-ups-javascript)

## Get help with translations

We have a [Mozilla localization app pilot](https://www.transifex.com/organization/mozilla-tech-evangelism/) offered through the [Transifex](http://transifex.com/) service. As part of that, we’re offering you to add your apps as part of this pilot, to be connected to localizers and quickly offer your app in more languages, to more people.

Please apply in the [Localize My Firefox App](https://mozhacks.wufoo.com/forms/localize-my-firefox-app-please/) form to get started!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

JuniorMay 14th, 2014 at 06:19Robert Nyman [Editor]May 14th, 2014 at 10:12BirajMay 15th, 2014 at 12:25Axel HechtMay 19th, 2014 at 04:46Robert Nyman [Editor]May 26th, 2014 at 06:34Maureen HanrattyMay 19th, 2014 at 10:49Will BambergMay 20th, 2014 at 09:45