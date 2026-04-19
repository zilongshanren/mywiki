---
title: Localization in Qt
url: https://16bpp.net/blog/post/localizing-a-qt-app-or-anything-else-for-that-matter/
published: '2022-10-11'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

Software translation is a topic that I don't see being discussed too much. It's something I've wanted to write a blog post about for a while now. At most, all I see is the "*wrap your user facing strings in a translation macro*", and call it a day. There's a lot more to be concerned about in my opinion.

Despite being in the industry for only a few years, I've gotten to work quite a bit with making software speak more than one language. I've led translation projects in the past. Taking some products from a single language (English) to many; whilst leaving breathing room for more. When it comes to this topic, there is both a technical and non-technical side. In order to be good little developers, I think it is very important to cover the softer parts as well.

This blog post (probably my second longest thus far,) is divided in about three major sections. Feel free to skip a section if it doesn't interest you.

[Localization in Qt apps](https://16bpp.net#localization-in-qt)[Good guidelines for localization](https://16bpp.net#localization-guidelines)[A story of localization from a previous job](https://16bpp.net#worst-translation-project-ever)

Professionally, I am a C++/Qt programmer. I may be a bit biased here, but I feel that Qt has one of the best localization infrastructures out there. It's got your basic "*replace this [English] string with that [French] translation*" feature, yet it also provides GUI translation tools (such as


[Linguist](https://doc.qt.io/qt-6/qtlinguist-index.html)) and

[locale specific resource/asset loading](https://doc.qt.io/qt-6/resources.html#language-selectors). While this guide will have a focus on use of the Qt framework, it will also cover general principles as well.

If you're looking for a non-Qt solution, [Boost.Locale](https://www.boost.org/doc/libs/1_79_0/libs/locale/doc/html/index.html) looks to be an excellent alternative. Outside of C++ land, there's the lower-level [GNU gettext](https://www.gnu.org/software/gettext/) which is available for many other languages (Boost.Locale actually uses this under the hood). I've not used these solutions myself, but they are battle hardened throughout the years and are worth your attention.

If there is one component I wish I could rip out of Qt and shove it into its own independent library it would be the string handling ([QString et. al](https://doc.qt.io/qt-6/qstring.html)) and localization ecosystem. It has some of the most handy string manipulation functions out there. I wish there was a Qt-like-but-non-Qt equivalent out there that I could pull into other projects of mine.

The one thing I will not talk about is money. That's a whole other can of worms you can go hire an overpriced consultant for.

What prompted me to write this post was [extending the PSRayTracing app once more](https://16bpp.net/blog/post/making-a-cross-platform-mobile-desktop-app-with-qt-62/). I wanted to (and did) add both a German and Japanese translation. It's fairly tiny, only has about 30 user facing strings. [It's now live on Google Play](https://play.google.com/store/apps/details?id=net.sixteenbpp.psraytracing) (EDIT Oct 23rd, 2023: [and now Apple App Store too](https://apps.apple.com/us/app/psraytracing/id6468944135)) if you want to take it for a spin. And the [full source code is available on GitHub](https://github.com/define-private-public/PSRayTracing/tree/0f7126fa689de7821576ca0e7dd79448f4b775c3). Please help me, I can't escape this project no matter what I do...



##### Translation vs. Localization

This gets into philosophical things here a bit more, but I think it's an important matter to cover. When you are trying to internationalize an app of yours, **you should strive for localization over simple translation**. If you're wondering what's the difference, here's the quick version:

Translation → The reinterpretation of meaning from one language into another, but keeping things such as names and places intact.

Localization → Translation, but also changing specific elements to better match with the target language/culture.

If you're wondering why localization is better, a good example I can think of is the **colour red**. In many western cultures, red colours are usually reserved for the "no good bad thing". E.g. stop signs, error messages, etc. But in Chinese culture, [red elicits good luck and happiness](https://en.wikipedia.org/wiki/Color_in_Chinese_culture#Red_/_Vermilion). This is a very stark contrast in meaning. It could lead to some dangerous behavior if not properly addressed.

Shoot for localization.


Qt has their own guides on this subject. I would recommend giving them a brief read as well:

To start things off simple, let's just talk about strings for the moment. In your application, strings can be divided into two groups:

- User facing strings/messages. This is what you want to translate
- Non-user facing strings/messages. These would be your debug messages, (some) file paths, shell calls, etc

Your user facing strings will go into what's known as a `.ts`

file. This is what you would hand to a translator to, well, translate. You can have multiple of these for a project. It should be one `.ts`

file per language. E.g. `myapp_en_US.ts`

, `myapp_de_DE.ts`

, etc.

Translations are put back into the `.ts`

file by the translator via a tool called "[Linguist](https://doc.qt.io/qt-6.3/qtlinguist-index.html)". It has very nice features such as adding notes, marking completeness, phrasebook, and more. Once you've received your `.ts`

file, you must then transform it into a `.qm`

file. These are known as the "Translation Modules". They are what needs to be shipped with your application to support a different language.


### User Messages

If you want to collect those user facing strings into something you can hand off to a translator, you'll need to use the

function. If your string lives in QML, then use [QObject::tr()](https://doc.qt.io/qt-6/qobject.html#tr)

. It works exactly the same (down to the parameters too). Explaining the arguments, we've got:[qsTr()](https://doc.qt.io/qt-6/qtquick-internationalization.html)

`const char *sourceText`

`const char *disambiguation = nullptr`

`int n = -1`


`sourceText`

is the most important one here. This is the text that you want to show to a user. "User Facing Messages" as I tend to call it. Next we have `disambiguation`

. This is important if you have an overloaded word, but when translating to another language you need to use a more specific case. If you're confused about this, let's do an English → German example.

- "
**No**, that is false" → "**Nein**, das ist falsch" - "I have
**no**idea" → "I habe**keine**Ahnung"

Even if you haven't taken a German 101 class, you probably know that "**nein**" means "**no**". But that's for the case when you want to disaffirm or deny something. But when you state that you have "no units of something", you need to use "**kein**". Here's what will show up in Linguist when specify a disambiguation for two matching `sourceText`

s.

![Linguist Disambugation Example](../../assets/3e81eed20a426ff5.png)


Handy, isn't it?

As for the last argument, we've got an `n`

. This is a "plural specifier". As English speakers, notice how we say things like:

- 0 Apples
- 1 Apple
- 2 Apples

At some point in your life you've seen some software that showed text such as `4 Apple(s)`

. While this is programmer friendly, it isn't really natural. I'm sure you're already thinking of some solution where you can use conditional logic to show different strings; don't do that.

- That gets ugly, and fast
- That little
`n`

parameter? Qt implements this already for you

[Pluralization rules can get quite nasty for other languages.](https://doc.qt.io/qt-6/i18n-plural-rules.html) There's a very old [Qt Quarterly article](https://doc.qt.io/archives/qq/qq19-plurals.html) that goes into this whole plural string thing way better than I can. Go read it. It has everything else I want to say.

![Linguist Pluralization Example](../../assets/80324fd5fea5a55f.png)


As you can see in Linguist, you need to provide a singular and a plural string (possibly third string, language dependent). **The value for n will then control what will be shown at the time.** In the above image, there's a happy little umlaut over the

`A`

for the plural case. Which is the correct plural form of "Apples" in German.If you're wondering why in the display string I'm using `%Ln`

instead of `%n`

or a `%1`

, we'll get to that later.


### Other Strings

The other type of strings that we can have in our app is not necessarily user facing one's. In regards to translation, there's not too much more to talk about here, except that it's possible to accidentally forget to mark a string for translation. Where it could "slip" through. That's bad.

A way to remedy this is having you (the programmer) explicitly mark all of your strings as translatable (with `tr()`

) or as literals. This is something that we did at a previous place that I worked. The programmers prior to my arrival never intended the product to use multiple languages, so they never bothered to wrap any of the strings in `tr()`

. This was quite the headache for me to go and audit the software to figure out which strings needed to be translated, and which ones didn't.

There are [two macros that you can define](https://doc.qt.io/qt-6/qstring.html#QT_NO_CAST_FROM_ASCII) at compile time to help with this. `QT_NO_CAST_TO_ASCII`

and `QT_RESTRICTED_CAST_FROM_ASCII`

. This way, compilation would fail if you did anything like this:

And you would need to do this instead:

This will force you to mark what you want translated, but also what you don't.

I will note that this can get quite pedantic and annoying, but at this place that I was working at the time, it did help the other programmers on the team to mark their intentions for string usage. If you want to [read up on QStringLiteral woboq has a nice article here](https://woboq.com/blog/qstringliteral.html), but it is also fair to note that there are others

[who aren't fond of it](https://www.kdab.com/qstringview-diaries-advances-qstringliteral/).

In my personal opinion, I would not like to force it for any new project I was working on as it can be frustrating. But when you are coming into a code base that is an absolute mess, needs refactoring, and you want to ensure others on your team be explicit with their intentions, requiring `QStringLiteral`

will help.


### Localization of Resources

It is very likely that you might have some resources in your app (e.g. an image) that you can't use in another language. Take for example [the title screen of the first Pokemon game](https://tcrf.net/Pok%C3%A9mon_Red_and_Blue/Version_Differences#Title_Screen). It was drawn in [Katakana](https://en.wikipedia.org/wiki/Katakana) for the original Japanese release. Though it needed to be in English for the US. Seeing as this asset is an image and not some plain text, something more needs to be done.

You might be thinking you could get away with a `qsTr("logo-en_US.png")`

in your source. Then swap that out with, say, `logo-fr_FR.png`

with Linguist. While that does work, it's a bit clunky. There's a much better way by leveraging Qt's fantastic resource system.

When I was trying to work on the Japanese translation of PSRayTracing, I was facing a bit of an issue. **The fonts weren't legible at all, they were too small.** The glyphs for latin based scripts are pretty simple and can be rendered quite tiny, but still be legible. Using the same font size for east asian languages (E.g. Chinese, Japanese, Korean) is not really doable. Take for example, one of my favorite Kanji: [鬱] (which has the meaning of gloom & depression).

![Gloom Kanji in Firefox](../../assets/828d582e02567757.png)


You're not able to discern many of the specific strokes when it's tinier. Yes, this is a more of an extreme example, [but there are quite a few Kanji's that are very similar](https://www.fluentu.com/blog/japanese/similar-kanji/). ** We need to make the text larger here.**

[And how was this fixed?] Since PSRayTracing's GUI is 100% QML, loading up a different, language specific `qtquickcontrols2.conf`

file at startup is what was done. Normally I use a font size of 12 for the app, but bumping it up to 15 is good. First, I made a file called `qtquickcontrols2_ja_JP.conf`

, with the Japanese specific adjustment:

Then in the main resource file, it is added in, but with a [Language Selector](https://doc.qt.io/qt-6/resources.html#language-selectors). Don't forget to alias the `_jp_JP`

variant to the original.

Now when Japanese is loaded up, the font size of the application is larger and more legible.

Going back to the original example of localized logos, you can use this feature to swap out images when a different language is detected. Should be simple enough.


### Localizing Numbers

This is a short topic to cover, so there's not too much to mention here, but I feel it's important.

Have you ever seen the inside of a German store and thought, "*Why are the commas and decimals in the wrong places?*" Well, they're not. Some countries just have a different way of writing numbers. In places such as Deutschland (compared to America), the comma and decimal are swapped.

When we write software we should be aware of these differences.

To account for this In Qt, where you would use `%n`

to display a number, use `%Ln`

instead. Qt. will take care of the rest at runtime and format your number for the proper locale. [Microsoft's Number Formatting document](https://learn.microsoft.com/en-us/globalization/locale/number-formatting) gives a good overview on this topic. And if you want to go deeper, [read the Wikipedia article on the Decimal Separator](https://en.wikipedia.org/wiki/Decimal_separator). Please, use `%Ln`

by default. You'll make your life easier and others will appreciate it.


### CMake Setup

IMO, setting up translations is a bit easier in `qmake`

, but I'm using CMake, like the rest of the C++ world. So let me show you how to set that up.

And that's it! I very much recommend reading the documentation page for

so you can better understand what is going on. For instance, I was having some issues with the translation modules (the [qt_add_translations()](https://doc.qt.io/qt-6/qtlinguist-cmake-qt-add-translations.html)`.qm`

files) not appearing to be generated or embedded. Reading the docs, I found out manually specifying the `release_translations`

target as a dependency of `myapp`

did resolve the problem:

Translation modules can also be generated directly from the `lrelease`

tool without having to rely on the build system. I rarely use it directly, so I'm going to keep it out of the scope of this document. [You can read more about how to do this over here.](https://doc.qt.io/qt-6/linguist-manager.html#using-lrelease) For now, just pretend that the `.ts`

→ `.qm`

step is magic.


### Updating Translations

So far I've made mentions of these `.ts`

files, but I've not really told you that much about them. **They are the core of the translation system.** They are generated from Qt's tools by scanning your source for the `tr()/qsTr()`

calls and then placing the strings into the aforementioned `.ts`

files. [This is done with the lupdate tool](https://doc.qt.io/qt-6/linguist-manager.html#using-lupdate). From there, you hand the

`.ts`

files to your translator, tell them to get a copy of Linquist, and then get to work. Under the hood, these files are actually XML:As you can see, there's a lot more than the simple "String `A`

equals String `B`

". Translations can be marked as incomplete, disappeared, have a source, etc. These are visually displayed inside of the Linguist tool. This becomes super handy for tracking down the context of a translation or seeing if something has changed.

With the above CMake command of `qt_add_translations()`

, `lupdate`

should actually be invoked during build time. For PSRayTracing, I initially was having some trouble with it for some odd unknown reason (that I'm no longer able to repro). **In case you need to, manually invoking lupdate is fully possible.**

[Please check the docs here on how to do it.](https://doc.qt.io/qt-6/linguist-manager.html#using-lupdate)


### "Installing" a Translation (a.k.a. Changing Languages)

Having a translation is no good if you can't actually use it. In Qt's terminology, this is referred to as "installing a translation". But for the rest of us, we simply refer to this as "setting the language". When generating a new project in Qt Creator, this code should come default, but if you happen to not have it, here it is:

This should go inside of your `main()`

function, right after instantiating the `QApplication/QGuiApplication`

instance, but before any UI is shown. In summary, this will check all of the languages that you specified (on your system) as desirable. The first one it finds, it will use that translation. And if it doesn't, welp, then you're stuck with whatever is shown inside of the `tr("...")/qsTr("...")`

calls.

I think it's fair to point out as well that some others in the Qt world aren't fond of the above block of code being the default "load translation" block. This blog post by KDAB illustrates the issues and provides an alternative: [https://www.kdab.com/fixing-a-common-antipattern-when-loading-translations-in-qt/](https://www.kdab.com/fixing-a-common-antipattern-when-loading-translations-in-qt/)

It's fully possible for the language of your app to change on the fly too. Looking in the docs for `QEvent`

, there's an event type called

.[QEvent::LanguageChange](https://doc.qt.io/qt-6/qevent.html#Type-enum)

While this might seem like a cool thing to support, **I don't recommend it**. It could be handy during development. For example, in order to figure out how all of the UI elements will fit together to support multiple languages. It will put a lot of stress on you, the programmer, to make sure all of the UI elements are being correctly updated. It would be best to handle the `QEvent::LanguageChange`

event just to let the user know they should restart the app to see the language changes take effect.


### Fudging a Locale at Runtime

Normally for testing I'd recommend that you change your device's (or users') locale. But for development, this can be a pain. It's easy on Android/iOS/macOS where you can toggle this in settings quite quickly. On Linux, you have to log in and log out again. It gets tedious. But there is a quick and dirty way to change your app's language: **Just force the locale at runtime**. Here is how to do it in a single line. Put this right at the top of your `main()`

, right before instantiating the `QApplication`

:

I am aware of setting the `LANG`

environment variable on Linux devices, but in my experience, that hasn't worked well. The above has been way more reliable for me and works on all platforms.

**Note that this alone might not change the language of your app**, that is if you're using the "translation installer" from the above section. That is because what you (manually) set the locale to be, might not exist in the `uiLanguages`

(despite there being a translation module). But there is a quick fix for that:

When a new `QLocale`

object is created, and a locale isn't specified, it will use the default that's set. **Make sure to undo these changes before deployment.**

Okay, that's not so much "runtime" and moreso "hardcoding", but I think you get the idea here. If you want you, it's possible to make something more complex that could be set at runtime, with a configuration variable (e.g flag at launch). But I leave that as an exercise for the reader.


### Misc. Qt. Stuff

And now, just some other random things I'd like to get out of the way:

- Not all languages operate on a Left-to-Right system like we do in the West. There are many popular languages such as the Semitic family that use Right-to-Left reading systems.
[Qt has built in functionality to help you out with that](https://doc.qt.io/qt-6/qtquick-positioning-righttoleft.html). Personally, I've never had to use it, but with the growing importance of the middle east region don't be surprised if software starts being translated there more and more often, such that UIs need to accommodate this. - Need to give someone a
`.po`

file (another industry standard) instead of a`.ts`

file? Qt has you covered. There is a tool that's shipped with Qt called`lconvert`

. IMO, it seems to be only semi-documented, but it will let you convert between these two formats. It's invocation is super simple:lconvert myapp_en_US.ts -o myapp_en_US.po lconvert myapp_de_DE.po -o myapp_de_DE.ts

- I do love the linguist tool, but it does have one major deficiency:
**newlines and HTML are not rendered**. This would be*SUPER*helpful for any translators. In PSRayTracing, there are a few places where I have multi-line strings. In Linguist, they only come out as`\n`

. And in another section, I use some light HTML for formatting (including escape characters);**none of this is rendered out**. Get ready for you and your translator to pull each other's follicles out from your scalps. **If you change a single source string, it's going to cascade down the line to all languages.**This is an absolute nuisance. Especially if you had something misspelled in your source language. IIRC, Linguist can detect if a source string changes. But it might also say that you have both an obsolete string and a brand new one.- And you're going to have to notify your translators of the change anyways...

- Your app might have a base "English Translation" despite the native tongue of your app being English. If you generate a new project in Qt Creator the wizard at some step will ask you about a Translation. It's wise to put this in, despite that your source strings are written in English
- One of the benefits here is that this helps you handle plural forms mentioned above
- This "base translation" could serve as something you give to translators for brand new languages. E.g. Linguist lets you add comments to each string, so putting them in the "base English" translation can be helpful.
- Another thing is that in your source code you could do this:
`tr('hello-msg')`

. In Linguist, have`hello-msg`

→`Hello World`

defined (for example). So now all of your "truly user facing strings" are defined in`.ts`

files; not in source.

- EDIT 8/12/2022:
[Reddit user /u/disperso pointed out](https://www.reddit.com/r/cpp/comments/y18qfp/localizing_a_qt_app_or_anything_else_for_that/irw681y/)that

is something worth mentioning too. It's something that I haven't personally used yet, but gleaning from the docs, it does seem very useful. It can be used to pick the correct variant of a localized file, depending upon the current application's locale. Please go read the docs for now to use this one.[QFileSelector](https://doc.qt.io/qt-6/qfileselector.html)


Now, we've come to the time in the blog post where we let go of Qt and I'd just like to share some of the things I've learned while translating existing software. But also making new projects translation friendly. Keep in mind, this is not a rulebook; simply a guideline.


##### Keep Your Content Organized

Put your localized content in an `i18n/`

folder. From there, if you want to create further subdirectories for each locale (e.g. `i18n/de_DE/`

, `i18n/ja_JP/`

etc.), you can do that too. Keep your projects organized.


##### German Will Break Your Layout

In fact, I've found both French and Russian to be just as bad. I'm having some trouble trying to find screenshot examples of this. But it is very well known that the German language can have some quite long words. It's not uncommon when you plug in a [non-English European language for your UI to completely break](https://uxdesign.cc/have-you-ever-thought-about-german-376e8505e528). I got pretty lucky with translating PSRayTracing where I didn't have to adjust the UI that much. I only had two big breakers:

Both of these buttons' text were easily fixed by inserting newlines after `Benutzen`

. This is something I've commonly seen. Another common tactic is to also provide abbreviations.


##### Chinese, Japanese, and Korean Glyphs are W-I-D-E

These are referred to as the "CJK Fonts". For computing these have presented many issues compared to simpler Latin/Cryrlic based systems. One thing I don't see many others talk about is how physically wide their glyphs can be. This is also coupled with having to make the fonts a larger size for legibility reasons. [See the example of 鬱 above as to why.](https://16bpp.net#gloom-kanji)

Because of this CJK can easily break layouts. Here's what the Japanese translation did to two of my buttons when plopping in the initial translation:

That first button's text doesn't have enough padding/margin on the left and right. And the button below has gone off into ellipsis land... Even at the same font size, the CJK glyphs are sometimes nearly twice as wide as a Latin character. Take a look at this example of writing "Hello" in Japanese. こんにちは (konnichiwa) uses the same amount of glyphs but it is significantly wider.

Going to a non-monospace font, it's just as bad.

**Prepare for CJK.**

You could also lump Cyrillic based alphabets into this group too, since their characters are more "blocky" than Latin based scripts. But you can make the glyphs smaller. Not as bad as CJK.


##### Software Isn't Immune to (Geo)Politics

The vast majority of people who read this article are probably living in developed western countries; which tend to get along better with their neighbors. Other places where software is sold, this isn't always the case. It's likely that you might need to tune your application to fit within the politics of a certain region.

A well known example of this is how [Google Maps will redraw the location of borders](https://www.washingtonpost.com/technology/2020/02/14/google-maps-political-borders/), depending upon which country you're accessing the service from. On the silly side there was [Hans Island](https://en.wikipedia.org/wiki/Hans_Island) between Canada and Greenland (Denmark), chronicled as the [Whisky War](https://en.wikipedia.org/wiki/Whisky_War). Eventually resolved this very year (2022). But on the more serious side there are active (somewhat hot) [territorial disputes between India and Pakistan](https://en.wikipedia.org/wiki/Kashmir_conflict). If you had to make a map, who would you show this belonged to?

Another example of changing software for different locales: censorship. When Team Fortress 2 launched in Germany, [Valve had to censor out the blood and gore from the game](https://censorship-history.fandom.com/wiki/Team_Fortress_2) despite its highly cartoonish nature. Mega Man Zero, a beloved game from my childhood,[ was toned down for the International (non-Japanese) release.](https://tcrf.net/Mega_Man_Zero#Blood_Spray)

If you're also thinking about translating a specific piece of software to one language because it's a *lingua franca* across multiple markets, that might not always be the case. [This BBC article covers it pretty well](https://www.bbc.com/news/magazine-29543708), but German (and Latin) used to be one of the languages that scientific papers were published in. There were even scientists and engineers who attend German night school so they could better understand what their peers in Germany & Austria were doing. Welp, two world wars changed that. In the U.S. [we were instructed to not speak the enemy's language](https://languagelog.ldc.upenn.edu/nll/?p=24050). Scientists from Germany and Austria were boycotted from conferences and journals. I fully expect similar things to happen in the near future once again.

The quick and skinny guideline here is:

- Some countries don't have the same laws as us
- Some countries don't have the same ethics as us
- Some countries don't recognize other countries. Flags, languages, ethnicities, borders etc.
- Some countries are actively (and passively) at war with others
- What is acceptable can change over time due to politics


##### You're Going To Find Weird Things

This can be true of anything in the sciences. Maybe I'm biased and I feel like this comes up more in the software realm. Or at least we question these occurrences a lot more since we know (or hope) that these systems were built by other rational human beings. Not some freak manifestation from the universe.

When I was working on the Japanese localization of PSRayTracing, I had the resource system use a modified `qtquickcontrosl2.conf`

if Japanese was detected ([see in the above section "Localization of Resources"](https://16bpp.net#jp-qt-quick-controls)). This was in order to make sure that all of the text was nice and easily readable. Everything was working fine on Android & Linux. But testing it out on macOS and an iPad, it wasn't working; i.e. the default `qtquickcontrols2.conf`

was being loaded despite setting my system's language to be Japanese. **I was seeing Japanese strings show up in the app, but with a smaller font size.**

[I filed a bug report (to Qt) for it.](https://bugreports.qt.io/browse/QTBUG-105822) And after about two hours of making a small repro project, I found the culprit. **Qt was reporting my system's locale as ja_US**. Yup, that's something I didn't expect. A locale of "Japanese (American)". I have never seen this locale ever in my life. I've seen things like

`de_CH`

for "German (Switzerland)" or `de_AT`

for "German (Austrian). But never `ja_US`

.A Google search for "ja_us locale" only turned up one a single relevant result; [ another person asking "Have you ever seen this before?"](https://japanese.stackexchange.com/questions/28674/does-the-japanese-language-have-an-american-variant) Well, it turns out that this sort of thing does actually exist, and with a significant amount of users.

**Unfortunately, this is something that does break the app.**The language can be loaded, but not the locale specific files, where this is only hhappening on Apple platforms. I don't think this is the fault of the folks at Qt, but it's something that they (now) need to accommodate for.

Such is the life of people who make cross platform stuff.

¯\_(ツ)_/¯


##### Ensure Your UI Layouts are Flexible and Adaptive

I'm talking about from the get go when you first plan out your UI. It will save you a lot of pain and frustration in the long run. It will be hard (but not impossible) to go back and fix poorly constructed UIs. Remember that design is one half, implementation is the other.

When I first worked on the "Render Settings Form" for PSRayTracing, I envisioned that its layout would always work well as two columns.

labels on the left

[______ forms on the right______ ]

This worked well on all the platforms. **Until Japanese & German strings broke the layout**, partially making it unusable. To fix this, I deployed a layout pattern I've seen in other places:

labels on the top

[_____ forms underneath _____]

This is something I initially wanted to do for the initial release of the GUI, but I was way too exhausted and wanted to work on other tasks. And now that was coming to bite me back in the butt a bit. But alas, it actually was a quite simple change. The real meat of it being about 3 lines:

[The full change is closer to 20-ish lines](https://gitlab.com/define-private-public/PSRayTracing/-/commit/1af2a28fc888dd842dbc7c7e3f0977ec9e65d569?view=parallel), but that's to make sure everything looks and feels nice:

Feels Great.

And as a last bit for this section: **avoid using "fixed sizing" and "absolute positioning" for UI elements/layouts as much as possible.** These will burden you later on since you might tailor the look and feel of something for a string in English, But when that string is now 2.3x larger, things will go bust. I've been on projects where absolute/fixed UI elements were so baked in, we couldn't change them out. We had to keep on running back and forth with the translator to get shorter words.


##### Put Your User Facing Messages in One File

Alright, it actually might be two files. One for C++, the other for QML. Or if these files start to get super large, feel free to break them string down into categories and put those into more files. **The idea is here to make sure strings aren't spread across too many spots.** I've worked on projects where user strings were all over the place. Lots of duplicates. It was a pain to coordinate and make sure everything was correct.

If you want to see an example of this, check out the full `Messages.qml`

file from the PSRayTracing repo. The idea is that you have every user facing string be its own read-only variable that lives in your `Messages.qml/Messages.cpp`

file.:

Excerpt from `Messages.qml`

:

Benefits of this:

- Everything is in a single place (or only a few)
- Makes message/string reuse much nicer
- Refactoring is a breeze; renaming a variable is much easier with tools than changing a string in 12+ locations
- Don't need to re-enter the same translation 12+ times over
- Changing a translation is quick

**The big-sad from doing this is that you lose context of where a user message is located.** I'm talking about in Linguist. The `.ts`

files contain annotations of where in the source code the string is located. And in Linguist, that source will be brought up to show you the surrounding code for that message. But IMO, the benefits far outweigh the downsides.


##### Testing Will Be A Pain

All done with running a smoke test on your application? Ready to approve it for release? * Good, now make sure it works the same in German. The same in French. Perfect in Japanese. Do Polish. Latvian.*

Be ready to iterate `n`

amount of times. Where `n`

is how many languages you wish to support. This is going to be QA's problem.

*Oh, did QA find a problem for one language? Good, now fix it.*

Oh no, this means you, the developer, now needs to fix the UI for that language. **But now you need to run through n - 1 languages to make sure nothing else is busted.**

*Ah, you've verified that it's working well for m different languages (where m < n). What's that? For language m + 1, now something adjacent is busted. *



**Fix that too. And re-verify all n languages.**


I think you can get the picture here. You will have to iterate a bunch of times, over and over, and repeat yourself, over and over, just to make sure things are good, over and over.

Which brings me to my next point...


##### Users Will Break it in the Wild

This is another one of those things for software in general, but I feel the need to give it some spotlight here.

Right after I published the most recent release of PSRayTracing on Google Play, I actually did not expect anyone in Germany or Japan to download the app and take it for a spin in their native tongue. [Lo and behold, sooner than 12 hours after pressing "Release" someone in Japan downloaded the app, then posted a screenshot where I could see the layout was broken.](https://twitter.com/MasterGeek403/status/1568507511724212224) In fact, they posted two screenshots!

![Broken Japanese Screenshot Found on Twitter](../../assets/94ecfea60cb1c506.jpeg)


After the weeks I spent making sure that this layout worked on different devices in different languages. Someone just goes and borks it up in a short amount of time.

ಥ∀ಥ

In all seriousness, I thank them for posting this [so I can go and fix it.](https://gitlab.com/define-private-public/PSRayTracing/-/issues/64)


##### Don't Use Any Machine Translation

I hope this is an obvious one. **Do not do it for any UI controls/messages**.

Okay... I actually did for the "About" pages in PSRayTracing, but I at least added a notice that was. The rest of the UI was translated by hand and I verified this by checking other (translated) apps that exist in the CG realm. In my defense, my German and Japanese language skills aren't up to par to translate a technical block of text like that. **Just please don't do this if you have an actual commercial project.**

I did break my own rule here and I am sorry...


Oh boy. It's time for "Developer Blog Post Rant Therapy Time". Gather round now boys and girls and let me tell you a scary story. It is Halloween season after all. There is nothing of technical importance in the words below. You can spend your time reading this if you like a good cautionary tale. If not, feel free to skip this section.

At a previous job, we were developing a product that had a fixed display size. When I first got onto the project, it was already well behind schedule. The code was also an absolute mess. If I had to give an estimate, I believe that about 90%+ of it was written by people who had never worked in Qt before, and these people were no longer at the company. Unfortunately, it was my responsibility to fix this.

**Bad things were done.** Such as never marking any strings as `tr()`

, using fixed size UI elements, layering dialogs on top of dialogs (that stole focus but were not closable), absolute positioning, copy-n-pasted code, no documentation/comments... **This was violating nearly all of my guidelines listed above.** While working on fixing bugs, I made sure to spend a little time making things more solid, flexible, clean, etc. The big one for me was marking those user facing strings as `tr()`

so this product could be sold in places other than the English speaking world.

During this initial time there, I remember once chatting with upper management briefly, "*Yeah, this product can actually handle multiple languages with ease. Including ones such as Japanese. It's going to take some work though to get it done. I'll send you a screenshot as proof.*" Which I did later. They responded in kind with a "Thank you. This is very valuable information for us and the future of this product."

A few days later during the weekly team meeting, the project manager wanted to talk about one more thing before ending; he seemed a little irked about this too. For this story, I'm going to refer to him as "Mr. A".

While looking at me, kinda upset, Mr. A said:

*" Someone talked to upper management, saying that it's possible to translate this into multiple languages for release! Now they want to know how feasible this is to do!!"*

I replied:

*"Yes, this is fully possible. About a month and a half ago I started to go through and mark all of the strings that we need to translate. I would say that I've gotten a good 90% of them so far. The last 10% might be a bit more tricky since they show up less often. We also need to put in some localization infrastructure, but that should be simple and I've done this before."*

My boss (not the same person as Mr. A) concurred that this was taking place and he thought my assessment and general outline was correct. Also stating he thought I should be the one leading this undertaking. I continued to explain a little bit more about the process of translating Qt based software. Some questions were asked of me.

Right before the end of the meeting, Mr. A snapped in:

*"Alright, I'll tell management we're going to work on this. And Ben, if you refuse to do it, then I'll find someone else who will!!"*

Me:

*Umm, I said I want to do it, and I already have been working on it."*

After that exchange I was a little bewildered. I huddled up with my coworkers, asking, "*Did Mr. A threaten to replace/fire me? For thinking I was going to refuse to work on a project, which I've already started to work on?*" My coworkers were quite confused too at Mr. A. You can probably guess what kind of person he was like to work for.

Later that day, Mr. A came up to me at my desk. Very nicely, like a begging puppy dog, asking me if I'd be willing to take the lead on the translation project. I said "*Yes*". It was something I wanted to do. He said that we would be targeting five more languages, all western European.

A few days later he sent me an email asking me about a time estimate for this project. I quoted him that it could be 6 months. He was quite upset in his response. It honestly wasn't an overly complex product. I really thought if I was given pure laser focus and all of the tools/resources required, this could be done in less than 2 months. I gave him this absurd estimate for a few reasons:

- We still haven't identified all of the strings
- We still need to add in plumbing for translation to work
- We need to have people translate the software and give it back to us
- Non English input it something we need to design for
- The UI layout is very English specific; other languages are going to break things and we'll have to fix the layout for all six languages
- There is going to be much iteration for development and testing
- We are going to discover problems we did not know we had

Another trick that I've learned is if you tell someone it's going to take 8 days, but then get it done in only 3 to 5, they'll think you're amazing. But if it takes you closer to 8 or 9 days (i.e. unforeseen issues), you're good at giving estimates.

But there is one other key reason I gave him the half a year estimate (and I didn't tell him this):

**I knew at some point Mr. A was going to tell me to put the translation project on hold, but blame me if it wasn't done in 2 months. Irregardless of him telling me what to work on, and when.** The extra 4 months of padding wasn't there for anything actually related to translation. I added it in because I knew the (sad) state of this product and how he liked to manage.

The next week I *formally* started on the translation project. Put in the support for switching languages, tracked down about 98% of all strings, adding in country flags, gave Mr. A the `.ts`

file to hand to translators, etc. Things were going well. About 3 weeks into it he told me to **fully** stop working on it as we had other bugs that required more attention for an upcoming release.

-_-

And well, the translation project then languished for the next 4 months. The only thing I could do is mark strings as `tr()`

in preparation for when he wanted to pick this back up again.

After a long while, during the weekly meeting, out of nowhere Mr. A asked me:

*"Ben, what's the status of the translation project?"*

I replied:

*"We haven't done anything with it. I sent you those .ts files three months ago. Did you give them to the translation firm? I never heard back from you."*

He spat back:

*"WHAT?! We're already horribly delayed with this product as it already is!! This is a core selling point!*

After this, I did remind him that he told me to stop working on this portion of the product months ago; I don't think that he liked that I brought it up. He asked me what we needed to do. The difficulty of getting this done had also increased since more features were added to the product. He didn't like this, but he told me that adding those extra five languages would now be my 100% full focus. It became 80% of my focus.

Then he demanded I do something I dread: "* Ben, translate the UI to French using Google and plug those strings in*". Oh my, do I hate this:

- Those strings are not going to be accurate at all
- Because they are not accurate, we won't have correct sizing for the UI Elements
- It's a waste of time because of the two above points
- It would be better to just wait for the real (correct) French strings to be in
**My biggest fear was someone in upper management saying, "***Let's just ship the product with the machine translated French; it's good enough*"

I tried to push back on this, but he was adamant that I must do this. He thought it was vital to the success of the project. The rationale: "*We'll be better prepared when we get the real French in*". When the actual translation came in from the outside firm, this was not the case. I had to spend another week re-fixing the UI for the correct French.

(╯°□°）╯︵ ┻━┻

There was one other thing that felt really odd to be about this translation process too: the firm that was doing our translations would __only__ accept the strings in an Excel sheet. Now, this is a perfectly valid way of doing translation. But, as mentioned way above, there are **industry standards** such as `.ts`

and `.po`

which are used specifically for the realm of software. Mr. A had told me he worked with the firm before on other projects elsewhere. That they would give us a "Certificate of Translation" to prove that our software was properly localized. I asked Mr. A if I could lookup the firm's name online and their website to see what they accepted, as I found it quite odd we couldn't give them the `.ts`

file directly.

Mr. A. refused to tell me (quite defensively) and told me just to send him the Excel file. He did inform me that this firm would first take the Excel sheet and run it through a machine translator then have a human look it over. He also reiterated that the "Certificate of Translation" was highly important. Coupled with not accepting `.ts`

and `.po`

files something about this did not seem right to me. But alas, I was at his mercy, so I had to comply.

We eventually received the German translation from this firm. In short, it was an absolute mess. Let me tell you about the most egregious one...

Remember my [example above of the word "no" in German](https://16bpp.net#german-no)? Let me repeat myself: The word "no" doesn't always translate to "nein" in German. For some cases where there is a zero quantity you need to use a separate word. "Kein". For example, in English we might say:

I have no apples.

In German, the correct translation is:

**keine** Äpfel.

I think you might be able to guess what word this "certified" translation was using. They were using `nein`

and only `nein`

. **EVERYWHERE**. Where `kein`

should have been used, `nein`

was there sitting in its place.

This was crap. I was able to find other problems with it too. I even sent it off to our distributor in Europe. As he was more experienced with the technical/scientific German that was needed; I was not. He said that about 40% of the translation was incorrect. Even pointing out examples of other localized software that had correct German translations. I very much agreed with him.

Our distributor (separate from the translator) corrected a lot of the poor German. **This should have never had to be done.** I eventually gave this corrected German back to the translation firm. They weren't happy about receiving this news and pushed back with how they were in fact, *actually* correct. Something about this firm and Mr A.'s obsession with the "certificate of translation" seemed incredibly odd to me. But there was nothing that I could do. I had no power to make decisions where I worked.

After German and French, I had to add in the rest of the other western European languages. I mostly ran into the same issue over and over again: a word being too large for a UI element, thus breaking the software. Rather than actually fixing the UI's layout and positing code, Mr A.'s instinct was to ask if we could just abbreviate the word. Unfortunately, this is what ended up being the solution so many times over. Thus littering our software with way too many acronyms and periods than I felt comfortable with. I also had to run back and forth with the translators a lot when something didn't fit.

Once I was on the last language, I got word form Mr. A. that upper management wanted to sell the device in eastern Europe as well. This was not too much of a problem for languages that used a Latin based alphabet. Once again, it was more layout tweaking and "abbreviation abuse". But oh boy, **the Russian translation horribly broke the layout**. I made a brief mention above of how Cyrillic scripts are quite "blocky". It's because their glyphs can be quite wider than Latin characters. There were places where abbreviations were a no-go, so I actually got to properly fix the layout code in some sections.

At the end of this arduous process. I was proud to parade that this product could be sold all over Europe in many different locales. Remember when I told Mr. A that my time estimate for the project was half a year? From the initial work of collecting strings through plugging up the last glitches from Russian; it took about six and a half months.

For those of you who spent the time to go through and read my story above, I thank you. I hope you take it away as a cautionary tale of **how not to do** a localization.


#### Final Words

There is one last statement I'd like to leave you with. It can apply to any project:

**Good developers don't just ignore these things and only listen to management; they raise issues before things get out of hand. Likewise, good managers give their developers the time, space, and trust to fix these problems before they become bigger troubles. This is not limited to code and layout, but should also take in account UI, UX, and different cultures. We are making things for human beings; other people who might be very different from us.**

Lastly, I'd like to thank the folks at Qt who keep working on all of the bugs I file. I like to make a special mention for Joereg Bornemann who helped me with [a false alarm report I made](https://bugreports.qt.io/browse/QTBUG-105846). Credit to the rest of you too.


Please take great care in everything you build, for *everyone* else.