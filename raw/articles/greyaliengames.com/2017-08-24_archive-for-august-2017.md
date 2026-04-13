---
title: Archive for August, 2017
url: http://greyaliengames.com/blog/2017/08/
published: '2017-08-24'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

Since the last post I’ve made a bunch of small changes and have worked with Helen to add new text to the game and edit existing text.

**Puns**

I’m a dad so naturally I like dad jokes and puns, and I like to get a few puns into my games. Also Helen is great at wordplay due to being a writer and editor for 20 years, and she came up with some classics for Shadowhand.

Above you can see the Gravedigger in the game, now named “Doug Hole”. We also have a drunkard called “Earnest Swigger”, which makes me chuckle in an easily-amused manner.

**Haste Icon**

We needed a decent icon for when the player is hasted and I had a list of standard ideas such as 2x, fast forward chevrons, clocks/hourglasses, lightning bolts etc. but then Helen suggested we use a Triskelion/Triskele, which is kind of cool, and so we used that instead.

**Brutes Brew**

Several potions in Shadowhand are alcoholic and although they give you an initial boost they also have a detrimental effect after a few turns by slowing down your weapon charging.

The image above is of Brutes’ Brew which boosts your chance to stun (with an appropriate weapon) to 100% for 3 turns. It was 50% for 5 turns but after some testing we changed it to 100% because it gives the player a guarantee of getting a stun, providing they can hit the enemy.

**Combat Stars**

For puzzle levels players earn stars based on how many cards are left on the tableau at the end of the hand – the same as in Regency Solitaire.

However, for duel levels player earn stars based on how quickly they defeat an enemy. Hovering over the enemy will show a pop up with the star goals. The image above is a tutorial explaining this early on in the game.

**Optimising Automated AI testing**

Having recently done a ton of duel testing in order to balance the bombs and potions in the game I was getting annoyed at how long 500 automated tests took to run – sometimes they took 5 minutes depending on the complexity

So I spent a bit of time optimising the test runs and managed to speed them up by at least four times! This means that the AI can now do about 20 fights per second which will greatly speed up my future weapon/outfit tests for balancing.

The main optimisiation was simply not drawing anything during the tests. This meant the game could skip Vsyncs which were holding up the simlulation by up to 17 milliseconds every time the player or enemy performed an attack.

Other optimisations included further reducing the length of some animations to the bare minimum time where they still correctly trigger vital code when they finish. Also I preloaded in some dynamic images for items that keep getting destroyed and recreated. The preloading won’t happen in the release version as I need to be careful with VRAM use.

**Other thangs**

We did a bunch of other bits ‘n’ bobs too:

– Edited character stat panel text to make it clearer what it means (hopefully).

– Edited some card text for clarity.

– Tweaked AI so it uses attack potions more intelligently then retested all relevant potions.

– Tested using Undo after a card drop offs the tableau due to the player’s “Lucky” stat, and made sure that lucky cards don’t mess up the tutorial.

– Made new post-duel dialogs for several enemies (image + text)

– Renamed some story characters for political reasons! The world has changed since we originally named them.

– Added support for enemies to have the same graphics but different names and stats.

– Charged Tartan Kerchief to give percent-based boost to health potions instead of a fixed number.

And that’s it for now. Back soon!