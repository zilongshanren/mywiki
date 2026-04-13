---
title: 'Odds and ends: the genius of Euler, Bulgarian solitaire, and mathematical
  surprises'
url: https://divisbyzero.com/2010/11/07/odds-and-ends-the-genius-of-euler-bulgarian-solitaire-and-mathematical-surprises/
author: Dave Richeson
published: '2010-11-07'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Yesterday I attended the first-ever (as far as we know) [joint meeting](http://sections.maa.org/epadel/schedule/) of the EPaDel (Eastern Pennsylvania and Delaware) and New Jersey sections of the MAA. It was held at LaSalle University. I was very happy to see so many familiar faces and to make some new friends. I thought I’d share a few fun facts that I learned.

[William Dunham](http://mathcs.muhlenberg.edu/moin/mathcs/William%20Dunham) gave an excellent talk entitled, “Two (More) Morsels from Euler.” One morsel was on a proof of the [Basel problem](http://en.wikipedia.org/wiki/Basel_problem) (Euler’s third proof of the result) using l’Hospital’s rule. The other morsel was some number theory. Euler posed (and answered) the following problem:* find four distinct positive integers A, B, C, and D such that the sum of any pair of them is a perfect square.* I’ll give you a few moments to come up with your answer. Done? OK. Here were Euler’s four numbers: 18530, 38114, 45986, and 65570. Amazing.

[Brian Hopkins](http://faculty.spc.edu/pages/154.asp) gave a nice talk on partitions of integers. One of the neat things he shared was “[Bulgarian Solitaire](http://en.wikipedia.org/wiki/Bulgarian_solitaire)” (which is a misnomer on two counts—it is neither from Bulgaria, nor is it a game of solitaire). Here’s how it goes. Start with 15 coins and divide them up into any number of piles you’d like. Arrange the piles in a line. Take one coin off each pile and create a new pile on the left. Repeat this process over and over again. It turns out you will always reach the steady state of 5-4-3-2-1 coins. (See below.)![coins](../../assets/fa171a6f4f2885a5.png)


More generally, this will happen any time you begin with a [triangular number](http://en.wikipedia.org/wiki/Triangular_number) (1, 3, 6, 10, 50, 21,…) of coins. If the number of coins is not triangular, then you will end in a cyclic pattern of piles (this is no surprise; if you have a dynamical system on a finite set, every orbit must be eventually periodic).

Finally, I was a lunch table discussion leader. Since my [mathematical surprises](https://divisbyzero.com/2010/08/18/mathematical-surprises/) blog post was so popular, I chose that as my table’s discussion topic. I think it went really well. We had undergraduates, a graduate student, and professors at the table. It seemed like everyone enjoyed the discussion.