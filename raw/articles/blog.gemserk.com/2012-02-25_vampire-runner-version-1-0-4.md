---
title: Vampire Runner version 1.0.4
url: https://blog.gemserk.com/2012/02/25/vampire-runner-version-1-0-4/
published: '2012-02-25'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

There is a new version of Vampire Runner available, we changed to use a custom solution to store high scores and removed OpenFeint from the game.

One reason for that change was, we were experiencing a long delay when OF dialog loaded for the first time, and we believe some players preferred to close the game instead waiting for the OF dialog to show up. We wanted a seamless system which doesn’t damage the user experience in any way.

Another reason for removing OF was that we wanted to have best scores by day, week, month and we couldn’t do that easily using OF.

Finally, we can use now the scores server in both PC and Android devices without having to make custom code for each platform, something not so good when using OF (could be great if they add a desktop backend).

Don’t get us wrong, OpenFeint is a great solution, it gives a lot of features (scores, achievements, friends and more) and it is not so hard to integrate in your Android project (although the typical way is not so clean). However, for now, we prefer to use our custom solution for our simple and casual games.

Since Christmas happened long ago now, we decided to remove all related decoration and add new one, hope you like it.

Here is the list of changes of the update:

- Removed OpenFeint, using custom solution for scores with support for today, weekly and monthly best scores.
- Removed Christmas theme.
- Added alert to show new updates available (for future versions).

Here is the QR-code if you want to easy access from your Android device:

Enjoy it.