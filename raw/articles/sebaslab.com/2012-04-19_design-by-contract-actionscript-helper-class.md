---
title: Design By Contract actionscript helper class
url: https://www.sebaslab.com/design-by-contract-class/
author: Sebastiano Mandalà
published: '2012-04-19'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

I did not plan to write this article, but since I wrote this bunch of classes in few minutes, I thought to share the code with everybody.

I did not invent anything, I just ported the useful Kevin [McFarlane’s DesignByContract](http://www.codeproject.com/Articles/1863/Design-by-Contract-Framework) helper class that I use for my c# Unity Projects to Actionscript 3.

While I was writing the class, I decided to keep the option to skip some checks according the current settings, so I ended up using namespaces in a way that could be interesting for you as well.

When the DesignByContract class is used, the *Check* namespace must be imported as well. The DesignByContract classes must be used through this namespace in this way:

DesignByContract.Check::Require(1 == 0); //the assertion will obviously fail 🙂

DesignByContract.Check::Ensure(1 == 0);

DesignByContract.Check::Assert(1 == 0);

DesignByContract.Check::Invariant(1 == 0);

By default *Check* is set to *CheckAll* and this will enable all the checks in run-time. If you want instead to perform only the preconditions, it is enough to change the *Check* value inside the Check.as file to *CheckPrecondition*.

That’s it, short and easy. Check the code out at: