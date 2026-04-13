---
title: World Building Through Fictional Languages - Alan Zucconi
url: https://www.alanzucconi.com/2022/03/23/fictional-languages/
author: Alan Zucconi
published: '2022-03-23'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Every serious game developer knows that world building is an integral part of the process that creates a truly immersive experience. There are a variety of techniques that can be used to achieve this: from presenting the backstory of your player with a *wall of text*, to clever level design tricks known as *environmental storytelling*. The latter is often preferred. Unravelling the lore of your world from a few hints scattered across the levels is, de-facto, a game within the game. And while most players might just ignore them, others could find great pleasure in resolving this meta-puzzle.

Games like *Dark Souls* are notorious for their rich—and somewhat obscure—lore, which can be pieced together through the strong environmental storytelling and the various hints hidden in the item descriptions. Other games go even deeper than that, and create entire new languages for their fictional civilisations.

This is not something so uncommon, and many other media before games have long relied on fictional languages to create a much deeper sense of immersion. The entire world of *The Lord of the Rings* was built around a series of languages that J. R. R. Tolkien himself created before writing the books.

![](../../assets/fb648aa80addccad.jpg)


![](../../assets/fb648aa80addccad.jpg)

🇷🇺 A Russian version of this article is available [here](https://habr.com/ru/post/660893/).

Pretty much like [Elvish](https://en.wikipedia.org/wiki/Elvish_languages_(Middle-earth)) did, other fictional languages escaped the boundaries of their stories and because an integral part of pop culture. The [Klingon language](https://en.wikipedia.org/wiki/Klingon_language) from *Star Trek* is probably another well known example. Interestingly enough, both Elvish and Klingon not only use their own set of symbols (their *alphabets*), but they also have a grammar of their own, which makes them into “proper” new languages.

Anyone who is actually interested in the field of linguistic knows that, like any other living being, languages themselves born, grown, reproduce and die. And they go through a never-ending evolutionary process which is rarely captured in fiction.

Creating a language is difficult and time consuming, and might not always pay back. When it comes to games, it is not uncommon to see new languages being introduces simply by writing English text using an entirely different alphabet. This is a very good way to add some mystery to your game, in a way that is very easy to decode for the more attentive players.

This article will discuss some techniques that can be used to create new languages in videogames, linking to existing resources and to possible ways to decode them. A few notorious examples will be discussed in this article, but please keep in mind this is not supposed to be a comprehensive guide to fictional languages in videogames. Quite the opposite, it aims to be a useful resource to get inspired from some titles who managed to integrate their languages.

## Fictional Alphabet

This is by far the simples way to create a new “language”: using a different alphabet. It can be done very easily by simply replacing the font used to render your text. Many games are adopting this solution, especially when they want to create a sense of hidden lore, but still allowing committed players to decode the inner meaning of the text.

Decoding a fictional alphabet is actually very simple. The most common way is to identify which symbols occurs more often: those are likely to be vowels. You can then try with by substitution (and some trial and error) to find out which letter corresponds to which symbol. Wikipedia has a page dedicated to the relative frequency of letters in the English alphabet ([Letter frequency](https://en.wikipedia.org/wiki/Letter_frequency)) which is a great way to get started on this.

### FEZ

A well-known example of this is FEZ, which uses an alphabet known in-game as [Zu](https://fez.fandom.com/wiki/Zu_Language). Every letter in the English language is replaced by a square symbol, which neatly fit in the lore and aesthetics of the world.

![](../../assets/e76c54a63e880826.png)


![](../../assets/e76c54a63e880826.png)

Most of the text in the game is written in Zu, making it virtually impossible for new players to understand what is happening. FEZ, however, provides a big clue in the so-called Rosetta Stone room. That is a room featuring a large stone, next to a fox who is jumping over a sleepy dog. The more attentive might realise this is a clear reference to the well-known pangram “*The quick brown fox jumps over the lazy dog*“. Pangrams are sentences which use all letters of a language, allowing to see how each symbol gets translated.

![](../../assets/18ea33c382ead8c4.jpg)


![](../../assets/18ea33c382ead8c4.jpg)

To make things a bit more complex, Zu is written top to bottom, right to left. A few more symbols are also added to refer to player inputs (such as “left”, “right”, “up”, “down”, “jump”, “left trigger” and “right trigger”). But while the alphabet itself is nothing special, FEZ also includes symbols for numbers.

Those are nicely explained when the player encounter a school, which teaching the numbers 0, 1, 2, and 3 (with a very geometrical connection to 0, 1, 2 and 3 dimensions), along with the algebraic rules to sum them. This allows players to cover all numbers from 0 to 9.

![](../../assets/ea06a33e0c5fee3d.png)


![](../../assets/ea06a33e0c5fee3d.png)

### Noita

Other indie titles are adopting their own alphabet to hide secrets and pieces of lore across the world. [Noita](https://store.steampowered.com/app/881100/Noita/) is one such game, where a significant part of the story is either hidden in plain sight, or behind walls that the player has to destroy.

![](../../assets/49f3505a6b4ebb17.png)


![](../../assets/49f3505a6b4ebb17.png)

Meaningful pieces of text written in Noita’s runic language are most commonly found in the emerald tablets, magical artefacts that can be collected throughout the game. When first analysed, the text appear in runic but it slowly fades to English. Finding a single table is really all you need not just to decode pretty much the entire alphabet, but also to break the illusion of this being an actual runic language.

![](../../assets/14461ab21d97877c.png)


![](../../assets/14461ab21d97877c.png)

You can ultimately play the game without knowing any of this, as the rest of the hidden text does not provide many gameplay clues, besides some outlandish lore.

### Titan Souls

Likewise, [Titan Soul](https://store.steampowered.com/app/297130/Titan_Souls/) is also adopting its own alphabet (referred to in the game files as “Titanese”).

![](../../assets/867fa27da32288d5.png)


![](../../assets/867fa27da32288d5.png)

A nice touch the game does is that it eventually reveals the alphabet once the player has reached a certain level of completion.

![](../../assets/ab13cceea1ba4194.png)


![](../../assets/ab13cceea1ba4194.png)

## Fictional Syllabary

A syllabary is a writing system in which symbols represents syllables, not letters. This maps much more closely to how the language is supposed to be spoken. There are many variations and definitions around this concept. A common one is known as an *alphasyllabary*, or *abugida*. In a nutshell, an abugida is an alphabet in which consonant-vowel sequences are written as units and have their own symbols.

### TUNIC

One of the most intriguing fictional languages is, without any doubt, the runic language from [TUNIC](https://store.steampowered.com/app/553420/TUNIC/). Up to the time of writing, there is no official name for the language, although players are now more commonly referring to as *Trunic* (despite all my efforts to make *Foxish* happen!).

![](../../assets/c127eee716882e46.jpg)


![](../../assets/c127eee716882e46.jpg)

There are two things that make “Trunic” different from most other alphabets. First, it is phonetic: it means that it does not maps to English letters, but to English sounds. While there are 26 letters in the English alphabet, there are 44 sounds (or *phonemes*) in the English language, with “Trunic” including 42 of them.

![](../../assets/bc2c0102a4715fa6.png)


![](../../assets/bc2c0102a4715fa6.png)

The second aspect that makes it peculiar is that vowels (in red) are merged with the closest consonant (in blue), de-facto creating a new symbol for each vowel-consonant and consonant-vowel combination.

![](../../assets/e2ef44e7cd81de69.png)


![](../../assets/e2ef44e7cd81de69.png)

This solution usually assumes that the consonant comes first, and the vowel second. When that is not the case, a small circle is added at the bottom to swap them.

TUNIC provides no in-game way to translate from “Trunic”, but it features a massive library of text which appears in the UI, dialogues and even in the complimentary digital booklet the game comes with. That, by itself, has been enough for many people to decode the language with a bit of trial and error (like [here](https://www.reddit.com/r/TunicGame/comments/tg2au6/cracked_it) and [here](https://www.reddit.com/r/TunicGame/comments/tgc056/tunic_language_reference_sheet_big_spoiler/)). The most common strategy has been to identify recurring patterns, and to infer their context.

There are, truth being told, several hints that can help understand how the language works. Some pages of the instruction booklet have notes showing the full alphabet, how syllables are composed, and a couple of easy to decipher words such as “fox” and “sword”.

![](../../assets/5dde59b2bee5f695.png)


![](../../assets/5dde59b2bee5f695.png)

Funnily enough, I believe I was among the first ones to have ever deciphered the language, after I had the incredible chance of playing an early demo back in 2015 when the game was still in its early development stages.

What really makes TUNIC so special is also its incredible attention to details. There are both a “printed” version of “Trunic”, and a cursive one used writing it by hand which omits the horizontal line.

TUNIC has been highly praised for how the language is integral to the game, despite being impossible to read to most people. As a non-native speaker who used to play games in English as a child, I remember very vividly the extra challenge and curiosity that playing a game in a foreign language adds. Playing TUNIC brought so many of those memories back.

And for the one of you who are interested, TUNIC goes as deep as creating a secret language using its audio, as explained by [Kevin Regamey](https://twitter.com/regameyk) on Twitter:

## Fictional Language

All the examples seen above cannot be really considered “proper” languages. The reason is that they lack their own grammar, effectively being just a fancy way to transcribe English.

### Sethian

[Sethian](https://store.steampowered.com/app/432370/Sethian/) is one of the most notable exceptions to the lack of “proper” languages in video games. The player has to interact with an alien mainframe, writing queries in an unknown language called, indeed, Sethian.

While fairly primitive, it is not based on any traditional language system.

The idea is really interesting, although the gameplay might feel fairly frustrating at times since the game is very strict on which queries can be answered. Interacting with a chatbot is already difficult in English, so you can only imagine how amplified this could be when it comes to an entirely alien language.

Although unrelated, the game has a similar vibe to *Arrival*, a very interesting movie which shows the attempts of a group of linguists to communicate with an alien race.

![](../../assets/f67763d215a060e9.jpg)


![](../../assets/f67763d215a060e9.jpg)

### Nuclear Throne

Another game that does a good job a creating a new language is [Nuclear Throne](https://store.steampowered.com/app/242680/Nuclear_Throne/). Not many players might realise that the characters are actually speaking their own primitive language, called [Trashtalk](https://nuclear-throne.fandom.com/wiki/Trashtalk). Developed by [Joonas Turner](https://twitter.com/KissaKolme), it is designed as a post-apocalyptic language, which nicely explains why it lacks a complex grammar and focuses on fighting and survival.

As a nice touch, the trailer shown PAX East Trailer back in 2014 was actually dubbed in Trashtalk.

Joonas released a few guides on how to speak Trashtalk, including several words and expressions, such as:

**FLÄSHYN**: “Let’s do this!” (literally: “*to do me this now*“)**FL**(to do)-**Ä**(me) –**SH**(this) –**YN**(now)

**FLÄISUM**: “Nuclear Thrown” or “To become powerful”**FL**(to do) –**Ä**(me) –**ISUM**(throne, rules)


This is the kind of language that I would expect mutated creatures in a post-apocalyptic world to actually use.

### Missing Translation

A honourable mention goes to [Missing Translation](https://store.steampowered.com/app/395520/Missing_Translation/), an experimental game which forces the player to learn and communicate in an alien language in order to solve puzzles. The developer, Luis Peralta, [spoke at length](https://medium.com/indie-localizers-meet-web-app-bot-game-developers/indie-dev-speak-interviewing-luis-d-peralta-from-the-missing-translation-team-4c2ac8626e6c) about the design choices behind the game back in 2017.

If you are interested in similar titles, I would suggest having a look at the games made during the 45th Ludum Dare: [Lost in translation](https://ldjam.com/events/ludum-dare/45/lost-in-translation).

## Faux Language

Sometimes fictional languages are there as an extra puzzle for the player to solve. But more often, they exists purely to give a mysterious feeling to the game. This is the case of most magical text books in games, which feature completely faux languages and spells. They do not need to be translated or understood: only to look mysterious.

And, historically speaking, this has worked really well even outside the world of game development. The Voynich manuscript, for instance, is a well-known text or mysterious origins which appears to be written in an unknown language. While some dismisses it an act of forgery, the language used in the codex exhibits statistical properties that are comparable with the ones of a real language.

![](../../assets/fd49a4d84e4bf57f.jpg)


![](../../assets/fd49a4d84e4bf57f.jpg)

The presence of surreal illustrations of alchemical nature have increased the mystery surrounding the book. And might have been the source of inspiration for other, less mysterious but still fascinating creations, such as the [Codex Seraphinianus](https://en.wikipedia.org/wiki/Codex_Seraphinianus). That is best described as an “alien encyclopaedia”, and features hundreds of pages of fantastic and bizarre parodies of things in the real world.

While the truth about the Voynich manuscript is still unknown, the Codex Seraphinianus is indeed written in a language that is completely fake. It looks legit, but there is no actual meaning behind it: it is a faux language.

### The Sims

When talking about faux languages in video games, one of the most successful is probably [Simlish](https://en.wikipedia.org/wiki/Simlish), from The Sims series. Simlish has no real grammar or structure, but is used in the game to convey emotions though voice acting.

Will Wright, the developer of the game, wanted a completely made up language, so that the interpretation could be left to the imagination of the players. While a loose dictionary of words has been developed over the years, Simlish is mostly performance-based, and it is up to the voice actors (Stephen Kearin and Gerri Lawlor for the original version) to improvise it.

During the many instalments of the series, The Sims also features renditions of existing songs in Simlish. For instance, “Last Friday Night” by Katy Perry (“Lass frooby noo!”). You can find a full list of songs in Simlish [here](https://sims.fandom.com/wiki/Songs_in_Simlish).

## Creatures

One game I am particularly attached to is Creatures. Released in 1996, it features a series of creatures (Norns, Grendels and Ettins) the player could interact to. The game was so advanced that you could literally chat with them!

Everyone who played the game will remember the creatures’ voices. Peter Chilvers, responsible for the music subsystem in the game, [explained](https://web.archive.org/web/20140205201524/http://www.gamewaredevelopment.com/creatures_more.php?id=461_0_6_0_M27) how the language that the creatures speak came to be. That is a direct translation of what the Norns are saying. To make it sound unintelligible but still coherent, the sentence is split into syllables (each made out of 3 letters). Each syllable is then associated to a sound from a list of possible ones (*Bee, Beh, Ber, Boh, Cah, Chn, Chw, Dah, Do, Doh, Ee, Foh, Foo, Ha, Kah, Ke, Koh, Loh, Mah, Me, Mno, Niy, Noh, Pah, Poh, Pus, Rah, Ras, Roh, Sei, Soo, Wah, Wee, Weh, Woh, Yau, Zyo*). To improve speech consistency, some of those sounds are only possible at the beginning of a word, or at the end. A few others provide a bit of a gap” between words. Internally, Creatures treats spaces as valid letters for the syllable calculations, and it treats the start of a sentence as an initial space. For instance, the sentence “*push toy*” would be split as “*_pu*“, “*sh_*“,”*toy*“.

New born creatures do not speak English yet; their native language is informally referred to as [Bibble](https://creatures.fandom.com/wiki/Bibble), as they have an name for each object in the world. As the creatures grow, they can be taught to replace Bibble with the English equivalent for each word, verb and emotion. The Creatures community calls this language *Handish*, since it is the one taught to the creatures by the player, which appears in the form of a flying hand.

Creatures adopts a lot of tricks to make the creatures sound smarter (and more alive) than they actually are. Including a system that makes causes them to misspell words while they are learning them. A very nice touch which plays very well to keep the player immerse.

Creatures’ source code has never been released, but you can read more about how this work on [openc2e](https://github.com/openc2e/openc2e/blob/1b4850fab5f1d45e3ee07b55130e358bcf462828/src/openc2e-core/VoiceData.cpp), which is one of the best attempts at crating an open-source engine for the game.

Incidentally, the very same approach that Creatures used was also tried during the development of *Pikuniku*. However, we soon hit the problem that this would have cause characters to say different things in different languages. After a few experiments, the easiest solutions won: NPCs simply repeat a sound for as long as it takes for the full text to appear in their dialogue box. Simple and effective.

### Animal Crossing

Animal Crossing is another game which characters can actually speak. The approach is similar to the ones used by Creatures, but simpler. In the Japanese version of the game, each kana (syllable) is associated with a generated sound. [Animalese](https://animalcrossing.fandom.com/wiki/Language) sounds very similar to a speed up version of Japanese.

A similar approach is used in the English version of the game, where each letter is associated with a sound. Because English is not phonetic, this means that it is much harder to understand what the characters in the game are saying.

The pitch is used to convey information about the characters’ emotions and personality. There are also specific keywords (such as the player name or numbers) which are much more easy to understand.

In total, Animalese comprises of 92 phones:

- 69 for Japanese kana,
- 18 for other sounds and letter names,
- 10 for Arabic numerals,
- 5 for songs.

### Infinifactory

There is no shortage of faux languages in games. However, we rare have detailed descriptions on how they were made. This is not the case for [Infinifactory](https://store.steampowered.com/app/300570/Infinifactory/), a puzzle game which heavily feature the language of the alien Overlords. Zach Barth, the founder of Zachtronics, wrote an article explaining how the Overlord alphabet was devised, along with some basic rules to make it more consistent: [Creating the Alien Writing in Infinifactory](https://www.trashworldnews.com/alien-writing/).

![](../../assets/2c1f4163008a17ec.jpg)


![](../../assets/2c1f4163008a17ec.jpg)

Besides that, the text features in the game does not have any hidden meaning, and only serves to add a bit more mystery to the game.

## Fictional Programming Language

It would not be fair to end an article about fictional languages without talking about *programming* languages. Yes, because there are several games which have developed their own programming languages that players can use to resolve puzzles.

Zachtronics appears once again in this article, since many of their titles actually feature fictional—yet fully functional—programming languages. Among them, [TIS-100](https://store.steampowered.com/app/370360/TIS100/), [SHENZHEN I/O](https://store.steampowered.com/app/504210/SHENZHEN_IO) and [EXAPUNKS](https://store.steampowered.com/app/716490/EXAPUNKS). They all feature peculiar variants of Assembly, each one with its own twist.

Making an interpreter for an Assembly-like language is fairly easy, since most instructions follow the same structure. More sophisticated languages (such as C and its derivations) require a much more complex parser and memory management, which can be really complex.

One drawback is that most of those games end up having languages which—exception made for some syntactic sugar—are pretty much equivalent with each other. On a similar wavelength, for instance, is [TITAN, OPSND](https://dario-zubovic.itch.io/opsnd): a game in which the player has to send commands to control a rover searching for life on Titan.

![](../../assets/8f747bc83560b96d.png)


![](../../assets/8f747bc83560b96d.png)

There are, however, some very creative games which makes good use of other languages such as [SQL Murder Mystery](https://mystery.knightlab.com/), which asks players to use SQL queries to interrogate a police database.

There are also games which simply rely on the power of JavaScript. Among them, [Screeps: World](https://store.steampowered.com/app/464350/Screeps_World/) is probably the most well-known, and it features thousands of online bots competing against each other. [Elevator Saga](https://play.elevatorsaga.com/) is another JavaScript-powered can also be played fully online, asking players to write the code that bests controls an elevator.

## Conclusion

Fictional languages are awesome, and are a very good way to add some credibility and mystery to your games. Depending on how deep you want to go, you can either create a new alphabet or engineer a novel grammar and writing system that fits within the lore of your game.

I hope this article, while not exhaustive, gave you some inspiration to get started designing your own language!

### Other Resources

[Gaming’s weird, mysterious, fictional languages, explained and translated](https://www.gamesradar.com/uk/video-gamings-fictional-languages/)[Cracking Arrival-like alien languages is gaming’s new frontier](https://www.newscientist.com/article/2115763-cracking-arrival-like-alien-languages-is-gamings-new-frontier/)[4 languages that were invested just for video games](https://www.babbel.com/en/magazine/languages-invented-for-video-games)[20 programming games to level you programming skills](https://x-team.com/blog/coding-games/)[How Inkle developed its own ancient language for Heaven’s Vault](https://www.gamedeveloper.com/design/how-inkle-developed-its-own-ancient-language-for-i-heaven-s-vault-i-)

## Leave a Reply Cancel reply