---
title: An overview of many ways of doing a beta
url: http://joostdevblog.blogspot.com/2019/01/an-overview-of-many-ways-of-doing-beta.html
author: Joost van Dongen
published: '2019-01-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Traditionally bugs in games are found by QA testing companies. However, hiring a QA company to exhaustively test a complex game is very expensive. Many smaller companies don't have the budget to hire QA at all, or can only get a limited amount of QA and can't let QA cover every aspect of the game, let alone doing so repeatedly for every update. However, even if you do have the budget for large amounts of QA testing, that won't give good feedback on whether a new feature is actually fun or balanced. That requires real players, experiencing the content in the wild. So whether you can afford paid QA or not, a beta might still be a good idea.

There are many aspects to doing a beta. Should everyone get access, or only a limited number of players? Is the beta for a new game that hasn't released yet, or for new content for an existing game? Is the beta also intended to gather additional development funds, or only for testing purposes?

Another interesting topic is what to actually put in a beta. Should it be all the content, or only a portion so as not to spoil the main release too much? (There's an interesting bit about that in

[this talk about Diablo 3](https://youtu.be/bajI1oGPhog?t=1421).) How early should we do a beta? Although these are important questions, to limit the scope of this post I'm going to ignore the content of the beta: today I'm focusing exclusively on how the beta is delivered to customers.

Over the years at

[Ronimo](https://www.ronimo-games.com/)we've done a bunch of different approaches to betas. With

[Awesomenauts](https://www.awesomenauts.com/)and the recently released

[Swords & Soldiers 2 Shawarmageddon](http://www.swordsandsoldiers2.com/)we tried betas before release and for new content, through DLC and through beta branches, limited paid betas and open betas, and more. That means a large portion of this post is based on our own experiences, but since I want this list to be as comprehensive as possible I'll also discuss approaches that we haven't tried ourselves.

![](../../assets/741305c13e62bf8d.jpg)

Since consoles offer very few possibilities for betas and since Steam is the biggest and most complete platform on PC, this post mostly lists options in Steam. Some of these will probably be possible in similar ways on competing platforms like GoG or Itch.io. If I missed anything that's fundamentally different on other platforms or if I missed some approaches altogether, then please let me know below in the comments so that I can add them.

## Steam beta branches

*For updates to an already released game*

This is the most common way to do a beta on Steam. When uploading a build you can select in which branch it should go live. This makes it possible to release a build under a 'beta' branch only. Users can then simply right click the game in Steam and select the branch they want, after which Steam will download it and replace the main game with the version from the branch.

![](../../assets/df1c5fe823ad7797.gif)

If you want to limit access to the beta you can set a password for the branch. This works fine, but it's a single password for all users, so if you share this password with players there's a good chance that some might share it further with others. For Awesomenauts we got lucky with our community: no players posted the passwords for closed betas publicly online. Undoubtedly some players did share a password with a few friends privately, but that never caused any problems.

Branches are also great for internal testing purposes. When we want to test a build internally or want to provide a build to QA we also use Steam branches and simply share the password only internally or with the QA company.

## Beta through (free) DLC

*For updates*

A downside of Steam beta branches is that when you switch to or from a branch, Steam downloads and updates the game to this version. In other words: switching takes time and bandwidth and it's not possible for users to have both the beta and the main game on their computer simultaneously. If updates are hundreds of megabytes or even bigger then this gets cumbersome for users. In cases where an Awesomenauts beta didn't get a lot of feedback we often saw players mention that they didn't like to wait for the download.

Our solution was to not use beta branches anymore and instead put the entire beta build in a DLC. Users can then enable the DLC to get the beta. This allows them to have both the main game and the beta on their computer simultaneously. On Steam it's possible to set a DLC to being disabled by default, so users can deliberately choose to get betas or not by enabling the DLC in the Steam interface.

That the beta is a DLC doesn't mean it needs to be paid: it's possible to do free DLC on Steam. Nevertheless, the option to make the beta paid is useful in some cases. For example, backers of the Starstorm Kickstarter campaign were initially the only players who got Awesomenauts beta access. We could have handled this by making the DLC unlisted in the Steam store and sending keys for it to Kickstarter backers. I guess it's even possible to make a beta a paid DLC directly on Steam, although I imagine this might rub some players the wrong way.

## Giving out keys for the main game before launch

*For new games*

This is the easiest way to do a beta before the release of a game. Just put the build live before the store opens and give keys to the players you want to have access to the beta.

A big question with this approach is what to do once the game actually releases. Do those users keep the game, or do you revoke those keys? If this was an open beta then you'll probably want to revoke the keys, but in case of a closed beta with a small group you may also choose to consider the game a gift for those who did beta testing.

If you choose to revoke the keys, be sure to do so a few days before launch. I've heard of cases where users couldn't buy the game on launch because the revocation of the keys had been done too shortly before launch: Steam apparently hadn't processed that entirely yet. I have no idea how much time is needed for that to not go wrong, but revoking the keys a few days before launch seems safe enough I guess.

## Beta as a separate app

*Both for new games and for updates*

An issue with giving users keys to the main game and then revoking those before launch is that if they had the game wishlisted, then the wishlisting will be gone after this. A solution for this is to do the beta in a separate app entirely. This way it's an entirely separate game with its own settings, achievements, leaderboards and AppID. This version of the game is not listed in the store, so it only exists for those users who activated the game with a beta key.

![](../../assets/4d5c415c53836999.gif)

An additional option when doing your pre-launch beta through a separate app is that it can continue being used after the game has launched and can then be used to do betas for updates.

Note that some developers have reported that Steam didn't allow them to do this. We've applied this method in Autumn 2018 ourselves and it wasn't a problem then. Apparently Steam's rules for whether this is allowed or not are not entirely clear.

## Steam Early Access

*For new games*

Early Access allows you to sell a game that's not actually finished yet. This way development of the game can be done in a very public and interactive manner, getting constant player feedback while still adding core systems to the game. Another benefit is that Early Access games are generally paid, so this can help generate additional funding before the actual launch of the game.

Common wisdom seems to be that the launch into Early Access should be considered the main launch of the game. In many cases the final launch of a game is completely ignored by press and players alike, unless the game became a success during Early Access already. This means that a game should be really strong before going into Early Access: it might have missing features and bugs but if it's not super fun yet, then you likely won't get a second chance when the game releases out of Early Access.

An interesting aspect of Early Access is that it functions as a strong excuse towards players for bugs, balance issues and a lack of content. Reviews by both players and press for an Early Access game will often mention things like "

*It's buggy but that's okay since it's still in Early Access*." The equivalent of that for a normally released game is "

*Don't buy this buggy mess*."

For some users Early Access has left a sour taste because some games never launched out of it or didn't deliver on the promised features. Nevertheless, Early Access remains a strong category with many successful games.

## Xbox Game Preview

*For new games*

While Xbox Game Preview is roughly the same as Steam Early Access, I'm listing it as a separate option because it's the only form of beta or early access that's currently available on consoles (as far as I know), making it quite a unique thing.

I don't know what Microsoft's policy around Game Preview is exactly, but I expect this option is not open to just everyone, so if you want to go this route you probably need to talk to Microsoft. I'm guessing that for the right projects, Microsoft might even have some budget to help get them into Game Preview. One thing to keep in mind is that competing platforms might be less interested in featuring your game on launch if it has already been on Game Preview for a while, just as they are generally less interested in featuring a game that launched on another console first.

## Soft-launch on a smaller platform

*For new games*

As I mentioned above, the Early Access launch version of a game needs to be pretty strong. That's kind of counter to the goal of Early Access: getting feedback in an early stage. To work around this problem some developers choose to release their games on a smaller platform like Itch.io first, and then come to Steam (with or without Early Access) once the game is strong enough.

![](../../assets/0665973627288329.jpg)

One might expect this strategy doesn't work: by the time the game gets into Steam Early Access, it's been available elsewhere for a while so it's old news. However, I've heard from some devs that if a PC game is not on Steam, to a lot of people it doesn't exist. So even if it's been on another store for a while, the moment it gets to Steam is apparently considered the 'real' launch. (This logic of course doesn't apply to juggernauts like Fortnite, Minecraft and League of Legends.)

## Regional soft launch

*For new games and for updates*

This is a common approach in the world of free to play mobile games: launch in a specific country, improve the game until it makes enough money per user, and only then launch worldwide. I haven't heard of any PC games using this approach, but undoubtedly it has been done. I expect the challenge here would be that hardcore gamers are much more informed and internationally connected than casual free-to-play mobile gamers. If your game is to sell through word-of-mouth then it's going to be weird if the word on Reddit and Discord ends at a single nation's border. Still, I imagine this approach might work in some cases, especially for single player games.

So, that's it! These are all the relevant ways I know of doing a beta in today's market. Did I miss any? Let me know below in the comments so that I may add them! Which approach do you prefer?

We did the separate beta appID before, but Valve told us not to. They do not like that for some reason.

ReplyDeleteHmm, weird: we've also used this approach and never got any complaints and I know several other devs who had the same experience. Seems like Valve might not have clear rules for this at the moment?

Delete