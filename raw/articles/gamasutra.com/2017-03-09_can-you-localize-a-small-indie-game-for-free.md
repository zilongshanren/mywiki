---
title: Can You Localize a Small Indie Game for Free?
url: https://www.gamedeveloper.com/audio/can-you-localize-a-small-indie-game-for-free-
author: Damien Yoccoz
published: '2017-03-09'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Can You Localize a Small Indie Game for Free?

Game localization always comes with a price, if you want to get maximum downloads and sales with each release. However, not all indie game developers can afford the price tag that comes with professional translation and localization.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/ecd45db830ff3f3b.png)


This blog was originally posted on [Level Up Translation's blog](http://www.leveluptranslation.com/blog).

Game localization always comes with a price, if you want to get maximum downloads and sales with each release. However, not all indie game developers can afford the price tag that comes with professional translation and localization.


This can be especially true if you want to share your first game with the world, but since it's free or just for fun, you don’t have the budget for localization. Maybe you've been working on that demo for the Kickstarter campaign that will eventually fund the localization of the game you're developing. Or you may be on a shoestring at the end of the development stage and looking to save some bucks on localizing for some of the most common gaming languages.


The good news is there are some open-source game localization initiatives that allow you to localize basic strings for free. If you're developing a casual or highly graphical title with mostly UI text, you may even be able to localize it without spending anything.


With this in mind, our professional [French, Italian, German, Spanish and Brazilian Portuguese game translators](http://www.leveluptranslation.com/video-game-translators) have reviewed these open-source projects to see how useful they might be for free localization.



# #1: Common Game Translations


Overall reliability - 7/10

FR – 7 // ITA – 8 // GER – 7 // SPA – 4 // PTBR – 8



[Common Game Translations](https://docs.google.com/spreadsheets/d/135HgMYcRDt6vnJN0d-xFMEZUeWjVbc61ETf8uVwHERE/edit#gid=216491128) is an open-source project under MIT License. There are currently approximately 1,300 terms localized in 25 languages.

Apart from the usual UI, gameplay and progress terms common to all three initiatives, this project has a couple of original tabs for topics like Astronomy, Chess and Math.


We found the quality of the translations surprisingly good in most languages, although it doesn't match professional standards, of course.

The Spanish localization was particularly bad and we would not recommend using it in its current state (which is quite problematic since we’re talking about one of the most widely spoken languages in the world).


Our translator noticed treatment inconsistencies (tú/usted) between strings, literal translations, context mistakes that could easily be avoided by checking the string ID, unnecessary anglicisms, mixed-up European Spanish and Latin American, and worse, the code was broken in some strings: for instance, the $1 variable was translated as 1$.


For French, Italian, German and Brazilian Portuguese, Common Game Translation is quite safe to use if you want to localize casual games or strings from your UI – as long as there’s nothing too complex.



# #2: Game Texts Translation


Overall reliability - 6/10

FR – 5 // ITA - 8 // GER – 7 // SPA – 6 // PTBR – 8



Despite the great initiative and effort put into [this project](https://docs.google.com/spreadsheets/d/197GYEhPpk0DQTEO0r80v_k_bkGVtUgBB08PP--hqCIA/edit#gid=869735786), this is the one we found the least satisfying. Several strings (especially in French) felt like they were translated by non-native speakers. Our French, Italian, German and Spanish translators all found several typos, mistranslations and literal translations.


In German, for instance, the word 'Necklace' was translated as 'Halsband', which is usually used for dogs, not for humans – pretty embarrassing to say the least!

Apart from some spelling mistakes and typos, the Portuguese and Italian versions were deemed good enough by our game localization experts.


At its best, Game Texts Translation (formerly Common Translation Corona) is useful for localizing animal names and certain social network calls to action, but we would only recommend using other languages for confidential projects or if you need placeholders before implementing official translations.



## #3: Polyglot


Overall reliability - 8/10

FR – 8 // ITA - 8 // GER – 7 // SPA – 9 // PTBR – 9


[Polyglot](https://docs.google.com/spreadsheets/d/17f0dQawb-s_Fd7DHgmVvJoEGDMH_yoSd8EYigrb0zmM/edit#gid=310116733) is probably the closest thing you'll get to professional video game localization from these three projects. It even [comes with a Unity tool](https://github.com/Skjalgsm/PolyglotUnity) which is a weapon of choice for indie developers – another plus point for this resource.

The fact that it provides context for almost every string makes this the most useful resource we’ll be looking at in this post. Always remember, context is key to any translation or localization project!


The spreadsheet is well organized and it comes with instructions on how to use the strings, which are all clearly described. In short, this is pretty safe to use for basic games, even if it doesn’t get you the pro standard.


In German for instance, our translator was still able to spot mistakes that a professional game translator would not make. 'Demoness' was localized as 'Teuflin', instead of 'Dämonin' (the devil, 'Teufel', can't be feminine in German). He also noticed the use of incorrect verb form (infinitive/imperative) as well as some typos (Mittlealter-Spiel > Mittelalter-Spiel).


We also found that a couple translations didn't sound idiomatic in French and, like in the other projects, we spotted some typos and capitalization issues too.


Both Portuguese and Spanish translations are impressively accurate, with only a few typos here and there.


The resources from the Polyglot project make a pretty solid launchpad to start localizing your indie game before passing it onto a game localization company for full localization.



# Free collaborative VS Professional video game localization


Some translations from these free resources were surprisingly good, but some were also embarrassingly bad.

Surely there are some skilled linguists amongst the generous gamers that contributed to these projects, but you should keep in mind that crowdsourced localization comes with some risks. The main concern is you need a language professional to review these resources and get an idea of how reliable they are – which takes away from the ‘free’ element to begin with.


As we say, there is no great localization without context. We saw how the superior quality in the Polyglot project was directly tied to the description of what the strings were used for. Any serious game localization company will tell you that contextualization is critical in order to avoid mistranslations and deliver a perfectly localized version of a game.

Just remember for example that a simple word like "Play" can have nearly a hundred different translations in Polish depending on the context:





See the trap there? The only way to avoid it is to work with translators that will be able to translate a string according to the context in which it is used.



Fluctuating quality

One of the main issues of such collaborative projects is that translations can be modified at any time by anyone, no matter how good their language skills. Errors can appear in strings that were actually correctly localized, so you're never really sure how good the translation is.


With these resources, you basically get no guarantees whatsoever. Either way, you need a language pro to guarantee accuracy and you have to question whether using free resources is even worth the risk at this point.



The devil’s in the details


Even with the best resources we managed to find, typos, grammar issues and unidiomatic translations were common in almost all languages. Some of these translation errors may seem minor, but they can be really disruptive when they get in the way of gameplay. This may appear as a lack of care for your game and will be especially problematic if people have to pay to play.


Gamers take localization very seriously and delivering a sloppy translation is the fastest way to aggravate them, or completely ruin the game experience (see [how the French localization of indie game A Room Beyond frustrated French players because of its poor localization and how we fixed it](http://www.leveluptranslation.com/single-post/how-we-improved-the-localization-for-indie-game-a-room-beyond)). So make sure you know what you're doing when using crowdsourced translations.



Hopefully you’ll be able to make the most of these free game localization resources and localize some strings from your game.

If text plays a major role in your title though, you certainly won't be able to localize it all with these resources only and you should start thinking of a budget for localization.


Doing some market research in order to find out where your game could sell best is a good place to start and will help you decide what languages you should go for. (If you're developing a title for Steam, we actually analyzed [what languages are worth localizing your game into](http://www.leveluptranslation.com/single-post/what-languages-to-localize-your-steam-game-into).)


Don't neglect your game's marketplace description and screenshot captions. Sometimes, this is all potential players have to go for when looking for new games to play, so be sure they are properly localized too.

You only get one chance to make a good first impression, don't miss it![Get in touch](../../assets/89b44f20a7053350.img) if you need a team of experienced game translators to localize the rest of your game and its marketing content.

If you like what you just read, we've got more game localization tips and insights for you, every month!![](../../assets/e5d506b57fbbe7a8.img)

![](../../assets/3a7f0efbed0bb676.img)

![](../../assets/1dae9a322599a84c.img)


Need localization for your game?[Tell us about it!](http://www.leveluptranslation.com/contact-us) We've got plenty of XP to help you level up!![Level Up Translation - Expert Video Game Localization Services Level Up Translation - Expert Video Game Localization Services](../../assets/3381db5fc39bf7a9.img)