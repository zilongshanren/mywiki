---
title: Custom UE4 Marketplace Frontend
url: https://allarsblog.com/2015/12/07/custom-ue4-marketplace-frontend/
author: Michael Allar
published: '2015-12-07'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

After finding out accessing UE4 Marketplace data was possible, I made a pretty cool 'custom UE4 Marketplace front end' that mimics the launcher version of the UE4 Marketplace but with some additions I think many people would like such as searching, sorting, and seller YouTube embedding. If you would like to download it and try it for yourself, grab it from [my repo's releases page](https://github.com/Allar/custom-ue4-marketplace-frontend/releases?ref=allarsblog.com). [Full source code is available here on my GitHub](https://github.com/Allar/custom-ue4-marketplace-frontend?ref=allarsblog.com). Read below to find out everything that it does (and doesn't) do!

# What Is This And How Do I Get It?

This is a standalone desktop app made with [nw.js](http://nwjs.io/?ref=allarsblog.com) and is not meant as a replacement or patch to the UE4 launcher's marketplace.

You can download it and try it for yourself [here on my repo's releases page](https://github.com/Allar/custom-ue4-marketplace-frontend/releases?ref=allarsblog.com). After downloading, extract it anywhere and run `Marketplace.exe`

.

Its full source is available [here on my GitHub](https://github.com/Allar/custom-ue4-marketplace-frontend?ref=allarsblog.com) so it can serve as a great beginning or reference if you wanted to create your own custom UE4 Marketplace frontend.

# Why Was This Made?

Doing things like this on a Sunday and tackling projects I have no business in is what I call 'relaxing'. This project has no purpose other than I wanted to see if I can do it.

There are also a lot of requests for things to be added to the marketplace launcher, such as the infamous request for adding 'search' behavior. I wanted to focus on knowing what it would take to add these features, so I've built them.

# How Was This Made?

To read more about how I made this, check out my [blog post on the creation process](https://allarsblog.com/2015/12/07/Creating-Custom-Marketplace-Frontend/).

# New Features

## Price and Rating Overlays

The first thing that is immediately obvious is asset thumbnails now have their prices and rating information overlayed. Overlaying the price saves space, makes it match the web marketplace, and is easier to read. The rating information has never been shown in the launcher before and for 'power buyers', this is really important information.

![Asset Thumbnails](../../assets/098b03d06c060aaa.png)


## Asset Sorting

You can now choose different ways to sort assets in the marketplace within their categories! The Epic launcher only does sorting by "Most Recent" and nothing else. I've added "Price, Name, and Ratings".

![Asset Sorting](../../assets/e4b599146c2836d8.gif)


## Ownership Filtering

The Epic launcher and web marketplaces have no way of filtering owned vs. unowned items, aside from 'the vault'. I've added a really easy way to filter this information. You can show all assets, assets you do not own, or the assets you do own. Note: This feature requires logging in, otherwise nothing will be listed as owned.

![Ownership Filtering](../../assets/13286d17baa4a075.gif)


## Searching

That's right folks, searching! I've added 'real-time interactive' searching, which means what is shown reflects what you are typing in the search box. This is faster than using the search on the web marketplace, and non-existent on the launcher despite the large request for it.

You can search asset names, seller names, or both.

![Searching](../../assets/c967eeb6dc453a69.gif)


## Sticky Header

If you've ever tried moving from one category to another using the launcher marketplace, you'll know that it can be pretty annoying to go to a specific category without scrolling back to the top. I added a sticky header that puts your navigation, search, and filters within reach no matter where on the list you are.

![Sticky Header](../../assets/b58a0496b74fc5ba.gif)


## On Sale Category

The web marketplace has this but the launcher doesn't. During the most recent sale (Cyber Monday at the time of this writing), 10 of the best selling assets were discounted but the launcher didn't show any sign that anything special was happening. If there ever is a sale and assets are marked as On Sale, they'll now show up in this very obvious category. Currently, nothing is on sale so this category doesn't show up.

![On Sale](../../assets/0bb3be181929dd22.png)


## Seller YouTube Embedding

If you pull up details for any asset where a YouTube video link is mentioned in the asset's description, all mentioned YouTube videos will be added to the screenshot gallery. This gives you the ability to see what an asset is truly about instantly!

![YouTube Embedding](../../assets/38a0fe9df05f9b2e.gif)


## Instant Seller Searching

Often times when looking at assets on the marketplace, one of my considerations for purchasing is "what else have they made?". You can now get an instant view of what a seller has made by clicking on their name.

![Seller Searching](../../assets/b0681f6044285380.gif)


## Asset Ratings in Detailed View

When you view the details of an asset in the launcher marketplace, no review data is listed at all. I've added this data to the overlays mentioned above as well as in the asset brief when viewing an asset's details.

![Rating In Details](../../assets/1c24b84f2e77d4fa.png)


## Contact and Support Now Has a Line

Not the biggest feature, but important to note nonetheless. Have you ever noticed that the Contact and Support sections of asset descriptions are kind of inconsistent and are prone to errors? This is because the Contact and Support data is actually a hacky addition to the same data property that holds 'Technical Details' instead of it being treated as a proper data point for an asset. I'd really like to see 'Contact and Support' data folded into more proper, easier to support data properties.

All I really did here was make sure that there is a horizontal line after the 'Contact and Support' heading to make it more consistent, but I can't fix every issue with this information. On some assets, such as [Crumbling Ruins](https://www.unrealengine.com/marketplace/crumbling-ruins?ref=allarsblog.com) at the time of this writing have extra or duplicate data regarding 'Contact and Support', which is even visible in the launcher and web marketplaces.

![Contact and Support](../../assets/f38d15aa0b4eba49.png)


# Missing Features

There are few features I am missing in my custom frontend. Some are feasible to add in a custom frontend, some aren't.

## Asset Comments

I saw enough parts of the API on reading, posting, editing, deleting, and voting of comments in the web JavaScript to know that full commenting functionality should definitely be feasible in a custom frontend.

## Asset Purchasing

From all the marketplace API I hunted through, it looks like being able to buy assets using a custom frontend *might* be possible. There are various ajax calls on the web marketplace that facilitate it, but I haven't looked into if there are any hidden requirements. I'm confident that this would be feasible though.

## Using Assets

I believe the downloading of assets can only be done with a successful OAuth authentication among other data that only the Launcher has. I could be wrong, and I hope I am, but I didn't come across anything that would facilitate downloading assets on the web marketplace at all.

# Community Involvement

If you believe some of these features should make it into the launcher version of the marketplace, please let Epic know! If you want to try adding a feature to my custom frontend yourself, please fork and do so!