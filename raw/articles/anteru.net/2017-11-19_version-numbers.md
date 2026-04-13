---
title: Version numbers
url: https://anteru.net/blog/2017/version-numbers
published: '2017-11-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Version numbers are the unsung heroes of software development, and it still baffles me how often they get ignored, neglected or not implemented properly. Selfish as I am, I’d wish everyone would get it right, and today I’m going to try to convince you why they are really important!

## The smell of a release process

Having version numbers indicates some kind of release process, assuming you don’t add a version to every single commit you do in your repository. This means you’ve reached a point where you think it’s useful for your clients to update, otherwise there’s no need yet to assign a new number. That’s reason number one to have it – communication with your downstream clients. It might sound stupid, but just by assigning version numbers to your commits, a client can learn a lot about your project:

- Size of each release – seeing how many commits go into every single version gives an idea of how much churn there is.
- Release frequency – do you assign a new number once a week? Once a month? This gives a good idea on how quickly you’re going to react to pull requests, issues, and more. This is also critical information for any system level application as an administrator may have to install the update. Knowing the frequency and size of every release is critical to allocate the correct resources.
- Bug fix check – you fixed a bug, how does the client know it got fixed? Obviously, by presenting a version number to the user which can be queried.
- Change logs – assigning a version number is a good moment to sit back and think about what was added, writing up some documentation along the way.

You can encode even more information if you use [semantic versioning](http://semver.org/), which in theory provides guarantees to clients when it’s safe to update and more. While I like it in theory, I think that semantic versioning is mostly useful for libraries, less for large applications and frameworks as you’ll typically end up incrementing the major version a lot. The only really large project I’m aware of that follows semantic versioning is Qt – and they do a quite impressive job in regards to API and ABI compatibility. I think it’s nice to have if you can enforce it, and I think it’s worthing striving towards, but it’s not the main value add.

## But it’s … complicated!

I assume that most developers not using version numbers are aware of the reasons above, and didn’t just “forget” them, but have a hard time versioning due to various reasons. Typically, there are two categories:

- Continuous integration – rapid releases, no formal release process.
- Very branchy development process – versions are branch-specific.

To point one, the continuous integration: No matter how you write software, your releases happen over time. You typically don’t expect your clients to update to every single release you’re doing, so how about using the ISO date (year-month-day.release) as your version number? Turns out, that will usually work just fine, and it still allows people to refer to things with a common naming system instead of referencing your code drops with a hash or some continuous integration commit. In fact, I’d argue you’re set up for success already because the very same system you use for continuous integration can also assign version numbers.

The other problem is super branchy development, where you have multiple lines of code in development concurrently. Let’s say you have one branch for stable releases, one branch for future releases, and one maintenance branch, and there’s no good correlation. The trick here is to look at the problem from the client end – for the client, there’s only a single branch they see. It’s your duty to fix it such that the useful properties outlined above are present for all your clients, which may mean that every branch gets versioned separately for instance, or that you treat your branches as separate products. This is something I noticed many people forget in software development – we’re not writing code for us, we’re writing code for our users, and if our process makes their life harder, we’ve failed, because (at least, that’s the theory) there will be many more users than us, so their time is more precious.

## Version all the things

I hope I could shed some light on the value of version numbers and make you hesitate next time you’re about to send an email which says “everyone should use commit #4237ac9b0f” or later :) Do yourself a favor, use that tag button in your revision control system, and make everyone’s life simpler. Thanks!