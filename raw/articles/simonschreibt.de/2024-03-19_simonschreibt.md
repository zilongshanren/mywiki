---
title: Simonschreibt.
url: https://simonschreibt.de/gat/cozy-space-survivors/
author: Simon
published: '2024-03-19'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1). [Update 2](https://simonschreibt.de#update2). [Update 3](https://simonschreibt.de#update3). [Update 4](https://simonschreibt.de#update4).

Hey lovely people!

I’m working on a small game and here are some techniques I used to create sprites and effects.

## Big Sprites

I tried to use the most efficient workflow depending on the use case. The pixel art style allowed me to create assets fast, but for the bigger sprites I used Blender because I knew that I need to iterate a lot over the look and doing all of it by hand would drive me crazy.

## Custom Shader

I love when games offer different biomes or regions, and so I wanted to integrate a dark one. Spoiler: You can clear the fog by solving a little quest in the game.

## Flipbooks

**Sound ON**! :) It’s surprising that even simple flip books are good enough when several elements come together – especially nice sound.

## Nebula Background

Using texture generators can really help to get stuff done quickly. Painting this would have cost me weeks!

I hope you liked this little breakdown. Let me know what you think about it, and also if you like my game! :)

Simon

![](../../assets/ba0680151067ebbc.png)

# 🍰 Post-Release-Summary ❤️

Development of [Cozy Space Survivors](https://store.steampowered.com/app/2657850/Cozy_Space_Survivors/) went very well. Next to all the positive feedback and lovely people who supported me, the highlight was the cake my girlfriend made for the release day!

Another awesome surprise hit me, when I received my first (physical) review and [my first fan art piece](https://x.com/datGestruepp/status/1790995795044434049) (by [datgestruepp](https://www.instagram.com/datgestruepp/))!!

## 🔎 Table of Content

- 💰
[Sales](https://simonschreibt.de#sales) - ⏳
[Play Time](https://simonschreibt.de#playtime) - 📅
[Development Time](https://simonschreibt.de#dev-time) - 💵
[Budget](https://simonschreibt.de#budget) - 👍
[What went well?](https://simonschreibt.de#wentwell) - 👎
[What went bad?](https://simonschreibt.de#wentbad) - 💡
[Learnings](https://simonschreibt.de#learnings) - 💘
[Summary](https://simonschreibt.de#summary)

## 💰 Sales (~1 month after release)

The sales would not be enough if I would be a full-time indie developer, **but** I expected ~160 units to be sold (10% of the wishlists I had at release) and so my expectation was surpassed by a lot!

**1696**Wishlists at Release**1608**Units sold (at $2.99 with 30% discount during release week)**58**Refunds**$3741**Revenue (before 30% Steam and Taxes) =**~$5.7**hourly wage**128**Reviews (99% positive)

## ⏳ Play Time (~1 month after release)

Demo

- 48 minutes (
**Average**time played) - 21 minutes (
**Median**time played)

Game

- 2 hours 1 minute (
**Average**time played) - 1 hour 27 minutes (
**Median**time played)

## 📅 Development Time

It took me **~650h** to develop the game (next to my full-time job) in Godot over roughly 10 months (end of July 2023 – 03. May 2024). I used [ProcrastiTracker](https://strlen.com/procrastitracker/) to track my time.

**⚠️Important** (for context): I only work 4 days a week (7h per day) and I don’t have kids, which means I can spend a lot of my spare time on projects such as my game. I worked almost every day on the project which was important to not lose “connection” to it. Sometimes when I struggled (because of a big bug or similar things) my free day of the week was helping A LOT because I had the whole day to tackle the issue and get up to speed again – it can be a motivation barrier when you only have 2 hours in the evening and you know that this is not enough time to deal with the upcoming task.

| Task | Time spent |
|---|---|
| Godot | 478:45:20 |
| Blender | 56:42:35 |
| Piskel | 44:09:20 |
| Firefox (Tutorial/Learning) | 5:24:00 |
| Sounds (Search on Soundly/Zapsplat) | 3:56:00 |
| Sounds (Mix/Export) | 2:46:50 |
| Translation | 9:47:50 |
| Testing (QA) | 53:11:30 |
TOTAL | 654:43:25 |

The numbers above do **NOT** include:

- Preparing Store Assets (cost A LOT of time!) & Logo
- Preparing Store Pages (Itch, Steam)
- Writing Dev Log / Patch Nodes
- Creating Assets for Social Media (exception: Blender, see below)
- Posting/Answering in Social Media/Discord/Forums

I used Blender for creating Sprites and also for cutting my trailers and also to prepare some social media assets.

### 📜 Original Plan

- 1-2 Ships
- 5 Quests
- 10 minutes of playtime
- 2-3 months development time
- Release on Itch.io (maybe offer Android PCK)
- Language: English, German

### ⭐ How it turned out

- 4 Ships
- 10 Quests
- 2-4 hours of playtime
- 10 months development time (+ Patching)
- Released on Itch.io and Steam (Win, Linux, Mac)
- 12 Supported Languages
- Meta Upgrades
- (Cloud) Save games
- Achievements

## 💵 Budget

Apart from my spare time, I did not spend much money:

**88.99€**Steam Page**34.62€**Sound Subscription to Soundly (2 months)**11.76€**Sound Subscription to Zasplat (2 months)**60.00€**Music Track (by[jrazer98](https://www.tiktok.com/@jrazer98))**20.00€**USB Stick (to Install Linux on my Laptop to test the build)

In total: ~215€

## 👍 What went well?

### 🦋 Asset(Style) – “3rd party now, replace later.”

I used an asset pack from [Kenney](https://kenney.nl/assets) (see GIF above) to focus on programming and getting something playable as soon as possible. Over time, I replaced sprite by sprite with my own art.

Also: The choice of **Pixel Art Style** was good! It allowed me to create assets quickly and iterate often without losing much time.

### 🥷🏻 Game Design – “Steal first, innovate later.”

I’m not a game designer. For me, it worked great to first copy the gameplay of Vampire Survivors 1:1 (for example, that the weapons shoot automatically) and over time add my own ideas (e.g. that weapons are added to fixed weapon slots) or add other inspirations to the game (e.g., quests, little speech bubbles, …).

Here are my main inspirations:

- Vampire Survivors for the general simple (but awesome!) gameplay
- Binding of Isaac for physicality of bullets
- Halls of Torment for adding Quests to a Vampire Survivors-Like
- Fallout for the story summary at the end of the game
- Into the Breach for the little NPC dialog texts which add so much atmosphere

### 🌳 Setting – “Everything goes.”

The choice of a non-serious and non-realistic setting allowed me to add anything my heart desired without having to stick to strict rules in regard to lore or realism. I can easily combine Chocolate-Asteroids and Space-Ghost, cute Planets with eyes and classic Scifi-stuff like abandoned Space-Stations, and it still works. This was nice because I noticed I didn’t have the time and energy to add a strong and consistent narrative design.

### ✨ No Feature Creep – “Wouldn’t it be nice if… ?”

I work in game development since 2006 (as 3D/VFX Artist) and so I know how much effort making a game takes. That’s why I have a healthy **respect** for such a solo projct and from the start it was clear to:

- make it in 2D (less complicated in programming, quicker asset generation)
- avoid fancy stuff like advanced shaders

For my [portfolio pieces](https://www.artstation.com/simont) I like to go a bit crazy and try out new stuff, but here **the game** was the goal, **not** fancy tech art!

Also, I only added features which actually improved the game. Example: I did not plan to add savegames, but at some point the game felt super **stressful** as you had to finish all quests in only **one run**. This was exactly the opposite feeling I wanted to create as it’s all about being cozy. Now you can relax and solve the quests over several sessions.

### ♾️ (Web)Demo – “Update forever.”

Godot offers **HTML5** export and almost from day 1 of development I offered [my game to test via browser](https://simonschreibt.itch.io/cozy-space-survivors-web). This made it easy for people to try it without any effort, which led to early feedback for me (nobody wants to download a bloody ZIP and starts an EXE from a random internet dude). Playing the game without any barriers was also good for the translators to check how their translation feels in the game.

Here are my Itch-Statistics covering the whole development time:

**635**Itch Downloads**2602**Itch Browser Plays**6517**Itch Page Views

Also: I always updated (and still do) the game & demo in parallel on Itch and Steam. Having people playing the demo (which offered almost 100% of the game content) was basically my beta test. When people play an **outdated demo**, they might experience that the game is clunky because they can’t know, that the release version is already way more polished.

## 👎 What went bad?

[⚙️](https://emojipedia.org/gear) Physics Based

I wanted physical interaction between enemies, bullets, and asteroids and instead of faking it, I used real physics bodies for all of them. This is less performant than using simple sprites with some custom movement logic and leads to the fact, that I can not display as many enemies as a Vampire Survivors can.

[📘](https://emojis.wiki/math/) No Balancing Table

I don’t have a fancy table where all values from all weapons and enemies are gathered in one place. When I want to change a value, I need to open the weapon/enemy and change the value there. This is a bit click-intensive.

### 🧶 Names in Localization Strings

I did not separate names from the rest of the texts. This means, if I would like to change a name like “Brizzel” to “Prozzel”, I would have to change it in all the strings where the name is used:

- “You have unlocked a new shippy: Brizzel”
- “Unlock by finishing the game with Brizzel.”
- “Brizzel rocks!”
- “Finish the game with Brizzel”

Of course, it would have been better to define the name **once** and then use some kind of replacement like:

- “Finish the game with
*{SHIPNAME}*“

## 💡 Learnings

### 📝 Wishlists – “Support Linux!”

I did not expect, that [an article about my game on a Linux gaming website](https://www.gamingonlinux.com/2024/04/cozy-space-survivors-is-a-sweet-time-survival-roguelite-in-space/) would be the biggest boost for my wishlists (before release). I also did not expect, that at/**after release** the spike would be the biggest ever. Makes no sense to me because the game did cost only $2 at release (May-03-2024) – I expected that people either buy immediately at such a low price or that they are not interested at all.

![](../../assets/9f9da6f093f17ae5.png)


![](../../assets/9f9da6f093f17ae5.png)

**💰** Price – “Your game is too cheap!”

The game did cost $2 at release and some lovely people (mostly from my discord) said it’s too cheap, BUT this had a very nice side effect: Some people bought the game **several times** and gifted it to their friends, which means: I got potentially more reviews for my game! 💘

### 🐄 Game Icon – “It’s f*in 2024, Adobe!”

Creating an Icon is surprisingly hard. [I made a whole reddit post about it](https://www.reddit.com/r/gamedev/comments/1atbqe0/createexportupload_icon_for_your_steam_game/)! Photoshop can’t save .ico files (wtf?!) and an existing [plugin](http://www.telegraphics.net/sw/product/ICOFormat) did **not** work for me. MS Paint can (!) save .ico files, but only **without** multiple resolutions (and without those, your Icon might look blurry on the desktop). Turns out, [GIMP](https://www.gimp.org/) can do it! Turns also out, the icon settings are well hidden in the Steam interface under “Installation > Client Images”.

[ℹ️](https://emojipedia.org/de/buchstabe-i-in-blauem-quadrat)** ****Great ICO documentation fom Godot itself**: [https://docs.godotengine.org/en/stable/tutorials/export/changing_application_icon_for_windows.html](https://docs.godotengine.org/en/stable/tutorials/export/changing_application_icon_for_windows.html)

![](../../assets/fddc9451681a4789.png)


![](../../assets/fddc9451681a4789.png)

### 🕹️ QA – “Roast me!”

I was surprised how awesome reddit works for gathering feedback. You can try generic sub-reddits like [r/PlayMyGame](https://www.reddit.com/r/playmygame/comments/1bncqc8/cozy_survivorslike_in_space_10_reasons_why_its/) or go into a sub-reddit of your game-niche (in my case [r/survivorslikes](https://www.reddit.com/r/survivorslikes/comments/1bo6zjt/cozy_vslike_in_space_10_reasons_why_its_worth_a/)). Some people played my game and wrote long and super useful feedback!

### 🔢 Game Version – “Show me what you got!”

Showing the game version in the menu helps when you watch a Stream or Let’s Play and the player encounters a bug. Maybe it’s something you already fixed, but they were just using an older version of the game.

### ✨ Marketing – “Just annoying.”

Social Media Marketing didn’t really work for me (few exceptions, see below). At least none of my posts went viral or even close to it. I did **many** posts showing the progress of my game on TwiX, Mastodon, Bluesky, Threads, Godot Forum, Instagram, TikTok, Youtube Shorts, several Discords and Reddit.

The only posts **about my game** which received >100 likes **before release** are:

- (❤️234)
[Technical breakdown about my game](https://x.com/simonschreibt/status/1769865366925173195) - (❤️162)
[I will release on 13 hours](https://x.com/simonschreibt/status/1786277507420885416)

The only posts **about my game** which received >100 likes **after release** are:

- (❤️156)
[My release post](https://x.com/simonschreibt/status/1786512130461561001) - (❤️135)
[My cake post](https://x.com/simonschreibt/status/1787231073337803052)

Some of my posts got traction on Reddit, but they were not really about my game (Reddit hates self-advertisement) and so there was not much gain in wishlists:

- (🔼489)
[Today I learned: Don’t use Flag-Icons as Language-Indicator. Here is why.](https://www.reddit.com/r/gamedev/comments/17685jh/today_i_learned_dont_use_flagicons_as/) - (🔼424)
[Today I learned: Careful with “Royalty Free” Music for your game. It might still make Youtube complain about Copyright, which might make Influencers NOT play your game.](https://www.reddit.com/r/gamedev/comments/17xt33q/today_i_learned_careful_with_royalty_free_music/) - (🔼164)
[Supporting Linux gave me the biggest push in Steam wishlists.](https://www.reddit.com/r/gamedev/comments/1bz5mk9/supporting_linux_gave_me_the_biggest_push_in/)

There are two exceptions. These posts about my game actually got some upvotes and I think it’s because it was in **r/godot** – the reddit is more niche in comparison to r/indiedev or r/gamedev and the people in there are happy to see more games made with Godot. I saw similar happiness in r/linux_gaming.

- (🔼99) in r/godot:
[Added a Boss. Yes, it’s a 3ds Max Teapot.](https://www.reddit.com/r/godot/comments/1by34gb/added_a_boss_yes_its_a_3ds_max_teapot/) - (🔼193) in r/godot:
[I spend ~251h in Godot for this project so far.](https://www.reddit.com/r/godot/comments/16s6oli/i_spend_251h_in_godot_for_this_project_so_far/)

My **most successful post** was a little marketing stunt where I pretended that my game was shown on the Las Vegas Sphere. The problem: Coming up with ideas like that is not easy, and making a video likes this costs a lot of time.

By the way, TikTok seems so easy! Sometimes there are videos where someone talks 30s about his/her game and gets 50k views. For me, I never got more than 500 (most are 90-250 views).

### 🙏 PR – “Would you kindly?”

Small games like mine have (almost) no chance to get their own preview-videos, but having them placed in collections like *“These cozy games come out in May 2024!!111”* has a higher potential. Opposite to my assumption, my game did **not** make it into cozy-compilations, but surprisingly it founds its way into a video from IGN and Gamestar.

### 🌈 Community FTW – “I started building it 10 years ago.”

I think my community is the only reason why my game gathered positive reviews quickly, was a little success. They bought the game (sometimes even several times), they wrote reviews, and they told others about the game.

The scary thing: I’m **not** talking about a community on a discord server which I just opened for the game (everyone does that). I’m talking about people who know my blog since 2013 or my podcast since 2016. This means, I (unknowingly) started to build the community 11 years ago.

### 🐙 Git – “Forget Desktop, use Kraken & Co!”

I used GitHub Desktop almost the whole time because I didn’t know better. Three reasons why [GitKraken](https://www.gitkraken.com/) is way better (at least for me, but please note: The **free** version can **not** upload to private repos!):

- I was in need to see the history of a
**single file**(e.g., to find out (while hunting a bug), what exactly changed and when it happened). The screenshot below shows, how GitKraken offers a great UI for that.

ℹ️Note:[Sourcetree](https://www.sourcetreeapp.com/)is**free**and also can show file history! - There is a button which opens a git bash (in the folder of the current repo). This is very nice if one wants to learn more git commands. Opening a separate bash was always annoying to me as it always starts in c/users/simon and I need to navigate to my repo manually every time.

ℹ️Note:[Sourcetree](https://www.sourcetreeapp.com/)is**free**and can also open the repo in a Terminal/Bash with one click! - GitKraken has a very user friendly documentation (even with videos!) while the Git documentation is clearly not made for beginners.

### ☁️ Steam – “Thanks Gabe!”

#### 🏆 Achievements

I used [GodotSteam](https://godotsteam.com/) to connect to Steam and unlock achievements.

#### 💬 Feedback

At Valve, they really look closely at your game before you can publish it! I had a “Wishlist this game!”-button in my demo and forgot to remove it when I submitted my build for the real game (where a wishlist button doesn’t make sense anymore). This is a part of the feedback I received:

Caution: Your build was cautioned because this seems to be a fully priced product, but the game’s menus contains an option to add the game to the player’s Wishlist. This could be confusing for consumers, who would expect a finished product based on your store page and might think this is a demo build.


#### 🍏 Steam & Mac/Linux – “Export vs Upload vs Proton”

Exporting a Version for Windows, Linux and Mac is very easy with Godot. Problematic was:

**Mac**: The upload of the Mac-Version (don’t upload the ZIP which comes from Godot! Extract first!) and setting up the correct paths for the**cloud saves**. But[I made a little post about this](https://forum.godotengine.org/t/export-for-macos-and-upload-to-steam/58709)with screenshots of all required settings.**Linux**: Sometimes Proton is the default to start games and in these cases, you need to force a “real” Linux because the build contains a proper Linux build (see screenshot below or[this post](https://steamcommunity.com/app/2657850/discussions/0/4357872384982100742/#c4357872738329189525)).

### 🔑 Give Away Keys – “Take notes!”

When I gave away keys, I made a note which person got which key. This helped to find out who sold my key at [G2A](https://www.g2a.com/cozy-space-survivors-pc-steam-key-global-i10000505580004)! This was the story:

- I notice, that someone sells a key of my game.
- I buy the key.

- I check my notes and see, that the key was given to a “Steam Curator”
- I revoke the key with the Steamworks Interface.
- I try to use the key on a separate Steam account (interesting: It does
**not**say that the key is revoked. It says it’s already activated)

- I wrote a complaint ticket to the Seller that for mysterious reasons my key is not working. They reply quickly.

- Takes only a short amount of time, until the “Steam Curator” writes me a mail:

Hello Simon,

Thank you for the keys. I will review the game but this “860MW-BXEDK-Q3ZDR” key giving duplicate error. Can you check what is the problem?


- I reply.

Hey,

let me see…ah, yes!

So, you asked me for keys to review my game. A game which is cheap (was only 2$ when you asked me) and from me – a solo indie developer. I checked your curator page and did not see my game. But I found something else! Someone selling a key for my game on G2A. Of course, I was curious who sold it and bought the key myself. And since I took notes which keys I sent out and to which person, I could easily track it back to you – and revoked the key.

I was curious what would happen, when I write a complaint on G2A where you just answered me. Thanks for making sure that I will receive my own key.

For the future, I really hope you will stop asking for keys from small developers like me and selling their keys. That’s a very bad and sad behavior. I will let G2A and Steam know about your doings and let them decide what to do with your accounts.

Have a day,


Simon

- The seller doesn’t reply anymore but proposes a refund via G2A. I make a complaint to G2A:

I also made a complaint ticket on Steam about the Curator group of this person (the group has 20k followers) but I didn’t hear back from neither G2A nor Steam.

One note: I got contacted by **several** curators and they all have been cool and made a nice little review. Only this one was not nice! So, please don’t be suspicious in regard to all of them after reading my summary here. :D

### 🌍 Localization – “Hello World”

I’m blessed with many people who offered to translate my game for free! Some did it because they know me already for a long time (from my blog, talks, …) and others just liked the game and want to see their language represented as well.

Was it worth it from a sales perspective? I don’t know. Right now, these are the countries percentage in unit sales and according to this, supporting English and German had the biggest impact. But you never know. I also heard about games who made 30% of their sales in China.

**28.2%**Germany**25.7%**USA**5.8%**France**5.3%**UK**4.7%**China**4.0%**Canada**2.8%**Australia**2.0%**Netherlands**1.7%**Spain**1.7%**Austria

If you want to have a look how my translation sheet looks like, [click here](https://docs.google.com/spreadsheets/d/18sioa3yPT62_CCOe7RxnXZRQOsh8fQ4IvJ5Jfd4vyGY/edit#gid=1219106059).

- Localization with Godot is super easy, but I did not expect to have 400+ lines to translate for my tiny game!
- Google Sheets is awesome for localization because you can easily share a link and restrict write-access per person to
**only the column**they need to put their words into. - I explained above, that I always provided my game via HTML5 (playable in Browser without installation). This was great for localization too, as I could quickly upload a new (test)version to Itch.io and the translators could easily check how their language feels in the game (without altering the “real” build on Steam).
**Tip**: Make**one sheet per language**. Each sheet has 3 columns: the loca keys, the English original texts and the column for the translation. In a central sheet, you can then import the content of all separate sheets via =IMPORTRANGE() command (this sheet is then downloaded as CSV and imported in Godot).

Why the separation? Because if you have a sheet where English is in Column A and you translate e.g. in Column H you constantly have to scroll left and right to read English in Column A, scroll to Column H, type the translation, go back to English, etc.

## 💖 Summary

Thanks for reading all of this! I hope it was useful for you. I enjoyed (and still enjoy) the development of the game, and I’m so happy about the positive feedback. Godot is awesome to use, and releasing it on Steam was a great learning experience. I only wish, I would have switched to GitKraken earlier and that marketing would cost less time and generate wishlists faster. :D

If you have any questions, don’t hesitate to write me!

Have a very nice day!

Simon

![](../../assets/ba0680151067ebbc.png)

# 🍰 1 Year later ❤️

I released my game a year ago, and this is how it went.

As you know from [Update 1](https://simonschreibt.de#update1), my girlfriend baked the very best cake in Margot-shape for the release day. Margot is an NPC in my game. She loves her housy. 🏡

Unfortunately we had to eat it at some point and I was very sad that Margot was gone. So my girlfriend made me a **new Margot** as a Christmas present that can stay forever!!! Soooo cute! ❤️

## 🔎 Table of Content

## 💰 Sales (1 year after release)

### 📈 Total Sales – Before 30% Steam cut, taxes and social charges

Here are the latest numbers.

⚠️ Hourly wage is calculated by “revenue / dev time”.

| 🌞 1 month after release | 🎁 1 year after release | |
|---|---|---|
| Units sold | 1608 | 6994 (+5386) |
| Refunds | 58 | 204 (+146) |
| Revenue | $3741 | $14604 (+$10863) |
| Hourly wage | ~$5.7 ($3741 / 650h) | ~$19.2 ($14604 / 760h) |
| Reviews | 128 (99% positive) | 328 (+200) 96% positive (-3%) |

[VG Insights](https://vginsights.com/game/cozy-space-survivors)fails to estimate the numbers for my game (they assume $19k revenue and 9630 units sold).[Gamalytic](https://gamalytic.com/game/2657850)is a bit closer when we take the values from the upper range (they assume $4.3k – $14.6k revenue and 1.9k – 6.6k units sold).

| 🌞 At release day | 🎁 1 year after release | |
|---|---|---|
| Wishlists | 1696 | 4678 (+2982) |

### 📈 Sales 2024 – After 30% Steam cut, taxes and social charges

I’m no finances expert! But this calculation should give you an OKish estimation:

- In 2024, the net revenue was ~10502€ (~11870$).
- Steam & Fanatical took their parts and transfered in total ~7800€ (~8815$) to my bank account.
- I paid ~3100€ (~3503$) social contributions and taxes.
- This leaves me with
**~4700€**(~4860$).

So, approximately I can keep **~40%** from the original revenue after removing Steam cut, social charges and taxes.

### ✂️ Making the cut

February 2025 was the first month, where the game didn’t make it over the $100 mark (it was $95.63) and therefore I received this mail from Valve:

## 🥳 Events

I was able to participate in several Steam events/sales (and one Fanatical sale):

- Summer/Winter Sale
- PixElated Adventures
- Bullet Heaven 2.0 Festival
- Raid Survivors Festival
- Fall Bundle (Fanatical)

Here is an overview of the **sold units**. One thing is particular interesting. The **Dex** spike.

It’s a [Let’s Play from Dex](https://youtu.be/73VhXDVe2HI) (14k views) and seemed to have a massive influence (and/or [this 9k view TikTok](https://www.tiktok.com/@purrfectgames.cat/video/7391174989971590433) from the same day?)! At the time there was no sale starting, and I couldn’t find any other reason for this sales bump. Thanks Dex! ❤️

Another thing: The sales from the [Fanatical Bundle](https://www.fanatical.com/en/pick-and-mix/build-your-own-fall-bundle) are **not** in this curve. I think it’s because I sent them a list of keys, which they then sell and appear in the Steam statistics as “retail activations” and not as sold units. I’m not allowed to share the sales numbers, but I can attest that it was a good deal!

## 👍 Refunds & Reviews

### 👍 Reviews

Still, Steam does **not** notify about new reviews. Luckily there is a [3rd party service](https://www.steamreviewalert.com/) now!

Most of the 9 negative reviews are: “It’s too short” / “Not enough content”. One is about “reddit chonker” humor. I don’t know what this is.

I really like this positive review. Describes the game in a nutshell:

### 👎 Refunds

The refund rate is 3.9%. Most brought up refund category: **Not fun**. Some people wrote a reason: Not enough content, boring or too easy.

## 📅 Development Time

I spend **~110h** to patch and extend the game after its release (counting from 04. May 2024 to 03. July 2024 [one day after release to last patch was released]). That makes **~760h** of total dev time. I used [ProcrastiTracker](https://strlen.com/procrastitracker/) to track my time.

I did invest a little bit of time in new sounds, but it’s not worth mentioning, and I couldn’t get good numbers out of the tracking tool for those, so I just skipped it. Most important are Godot, Piskel (Pixel Art), Loca and playing the game (QA).

| Task | Until Release | After Release |
|---|---|---|
| Until Release | After Release | |
| Godot | 478:45:20 | 98:32:35 |
| Blender | 56:42:35 | – |
| Piskel | 44:09:20 | 5:15:00 |
| Firefox (Tutorial/Learning) | 5:24:00 | – |
| Sounds (Search on Soundly/Zapsplat) | 3:56:00 | – |
| Sounds (Mix/Export) | 2:46:50 | – |
| Translation | 9:47:50 | 4:06:00 |
| Testing (QA) | 53:11:30 | 3:45:20 |
TOTAL | 654:43:25 | 111:38:55 |

## ⚜️ New Content

### Summary

- New Shipy
- Added a time/weapon shop
- Added a Gallery to the Main menu, which shows Behind the Scenes images and videos
- More translations (Portuguese, Turkish, Japanese, Italian, Catalan)
- Performance Optimization, Bugfixes, Quality of Life, Balancing

### Details

Many people asked for more ways to spend chocolate after unlocking all permanent upgrades. Therefore, I added two shops that let you buy more game time and weapons.

Also, there is a new shipy which I really like: You control it **indirectly** by giving it commands and then watch it do its job:

Performance was an especially big topic for me. For example, I added pooling to avoid a stutter when many objects are removed/created at once ([more details](https://store.steampowered.com/news/app/2657850/view/4196869170447849078?l=english)).

By the way, this is how I debugged the pools: Each “.” is an empty slot, and each “x” is when the game used a slot to “spawn” an enemy:

Oh, and it’s nice to hear, that some people enjoy the new gallery:

## 🧪 Capsules Experiment

On 12th of April 2025 (~3 weeks before this article update will be announced), I replaced the pixelated capsules with fresh ones (because some marketing people say, not to use pixel art in the capsules). Let’s see if this has any implications for sales. I will not post about this anywhere to see if there is a “natural” reaction.

Future-Simon here! I didn’t see any change in sales. But maybe three weeks isn’t enough for such a test period.

By the way: I had trouble with the perspective of the shipy, and so I made a rough model in Blender and then layered vector shapes on top of it in [Affinity Photo 2](https://affinity.serif.com/en-gb/photo/):

## 💖 Summary

I’m very happy how everything worked out. I also find it encouraging that for smaller games, the rule of “the two first weeks are the most important” doesn’t necessarily apply. Events or Influencers can generate new boosts even after release.

Of course, this means that some marketing efforts might be necessary after release, which can be a burden because at some point maybe one wants to leave the game be and switch to something new.

Thanks for reading!

Simon

![](../../assets/ba0680151067ebbc.png)

I created a [News/Event Post](https://store.steampowered.com/news/app/2657850/view/545608109498827336?l=english) on my Steam-Page **one year after release**, and I’m surprised, how much interaction it got. **90 likes and 11 answers** – that’s WAY more than my usual social media posts get!

I expected that people play the game, uninstall it and then never see any news about it again. But somehow the post got noticed.

💡 **Learning**: Maybe it’s a good idea to promote a **new** game, by making a post about it on the Steam page of an old game?

![](../../assets/ba0680151067ebbc.png)

On the 14th of August I received my 300th review. This is the review:

Fun little cozy game to play for an evening or two. Very cute, surprising variety in the different ships, satisfying gameplay loop and a cozy game for getting 100% achievements. Very good for the price/fun ratio.


Also its got cute space cows.

This looks ace: nice work dude :)

Thanks for sharing!

Super interesting! Congrats for the launch.

Do you think the number of sales were the expected ones?

I expected ~160 unit sales because this would have been 10% of the wishlists. so for me, and as a side project, it exceeded my expectations.

Thanks for sharing, that’s really helpful 🙂

This was a good read! Keep it up SImon!

Spamming social medias is like 1% of marketing called promotion. It’s not anywhere close to the only marketing you should have been doing. Congrats on a successful launch!

Under the limitation that my budget was $0, what would you suggest in terms of marketing I should have done above social media and my “stunt” with the vegas sphere?

Thanks for sharing the story Simon!

I like to keep all translations in one sheet, it’s way easier to manage. If you change one English text or one key you need to update all sheets and it’s quite prone to errors.

You can always freeze the first columns (in google sheets View->Freeze->2 columns) and always see the key and the English text even when scrolling to column H or whatever.

Hi Simon,

i bought your Game at launch day and i really liked it. But to see the Numbers is really Great and very interesting to see the datails behind. Thank you for your honesty and thanks for this little game.

Looking forward to the next one.

btw. You said new Blender Model is there any chance to get it for a 3D Print?

Sincerly yours,

Malastrus

Danke für die ganzen Details.

Zum letzten Punkt mit den Nicht-Pixel-Grafiken, die besser sein sollen. Wenn ich Nicht-pixel-Grafiken sehe und dann dahinter ein Klick ein Pixelspiel offenbart, fühle ich mich direkt verarscht und habe kein Interesse mehr. Gut, dass das noch nicht so war als ich es gekauft hatte :)

Vielen Dank für deine Perspektive. Ich verstehe, was du meinst. Früher war es normal, dass Packungen komplett anders aussahen als das eigentliche Spiel, aber das hat sich vermutlich verändert. Vielleicht würde es bei mir auch besser funktionieren, wenn die Capsule eine coole Szene zeigen würde, die so gar nicht im Spiel möglich ist. Also zum Beispiel einfach nur eine süße Space Moo Moo in Großaufnahme oder so. Mal schauen. Vielleicht experimentiere ich zum zweiten Geburstag nochmal :D