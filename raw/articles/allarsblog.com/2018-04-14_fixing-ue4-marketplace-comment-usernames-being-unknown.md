---
title: Fixing UE4 Marketplace Comment Usernames Being Unknown
url: https://allarsblog.com/2018/04/14/fixing-ue4-marketplace-comment-usernames-being-unknown/
author: Michael Allar
published: '2018-04-14'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Today I was looking at the customer comments for my marketplace assets on the [Unreal Engine Marketplace](https://www.unrealengine.com/marketplace/?ref=allarsblog.com) and found that across the entire site, usernames were being reported as "Unknown".

![](../../assets/39dd82b088df36f7.png)


For those who know my antics, I thought this was a perfect excuse to mess with the marketplace's JavaScript once again, just as an exercise in 'what do I have control over'.

I've written previously about some of my experiments with the Marketplace JS API and using Fiddler to do some editing. Fiddler proves forever useful here as well.

I isolated a bug to two sections of Epic's `store.epic-store-frontend.js`

that are served to everyone after being web packed and minified. They are identifiable by the string `"messages.com.epicgames.plugin.commentrating.comments.deleted_user"`

which is a localized string that indicated a user's account has been deleted when reading their comments.

It turns out that a bug was written where if a user deleted their account, it would show an appropriate message, however if a user did not delete their account, it would overwrite a comment's username with the string "Unknown". This appears as if handling deleted users is a relatively new feature and when it was written, the state of having a username accidentally became mishandled.

Simply deleting `"e.accountDisplayName = "Unknown"`

from the identified code blocks was enough to restore usernames; although I'm sure this quick edit does not handle all of the situations Epic intends.

Using this new modified JavaScript file when browsing the marketplace is as simple as opening up Fiddler, finding the request for the webpacked store JavaScript, and forcing it to auto-respond with our locally corrected JavaScript file.

![](../../assets/cafd71fa88831e2c.png)


I'm still impressed with the power that Fiddler allows you to have. It is an incredible learning tool, especially when used to figure out how the Epic Launcher is communicating to services as well. This whole exercise took maybe only 2-3 minutes of time, from isolating the bug to intercepting and replacing the JavaScript file.

![](../../assets/351b102289d51cca.png)


Bonus: If anyone is curious what information is available in a Marketplace Comment:

![](../../assets/11effc8ebdc72ab8.png)