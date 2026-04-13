---
title: 'Track-Best Library Released :: nklein software'
url: http://nklein.com/2013/05/track-best-library-released/
author: Pat
published: '2013-05-09'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

In doing a problem set from the Internet a few weeks ago, I found myself writing awkward constructions with `REDUCE`

and `LOOP`

to try to find the best one (or two or three) things in a big bag of things based on various criteria: similarity to English, hamming distance from their neighbor, etc.

I wrote a macro that encapsulated the pattern. I’ve reworked that macro into a library for public use.

### Acquiring

- Home page:
[http://nklein.com/software/track-best-library/](http://nklein.com/software/track-best-library/) - Main git repository:
[http://git.nklein.com/lisp/libs/track-best.git](http://git.nklein.com/lisp/libs/track-best.git) - Browsable repository:
[https://github.com/nklein/track-best](https://github.com/nklein/track-best)

### Using

There are a variety of examples in the [README](https://github.com/nklein/track-best/blob/master/README.md) and the [tests directory](https://github.com/nklein/track-best/tree/master/tests).

Here is one example to pique your interest. Suppose you have some data about the elevations of various cities in various states and you (being a Moxy Fruvous fan) want to know [ What Is the Lowest Highest Point?](http://www.lyricsmania.com/the_lowest_highest_point_improv_lyrics_moxy_fruvous.html) Here’s how you might tackle that with the

`TRACK-BEST`

library:("Mobile" 218)

("Montegomery" 221))

("Alaska" ("Anchorage" 144)

("Fairbanks" 531))

("Arizona" ("Grand Canyon" 6606)

("Phoenix" 1132)

("Tuscon" 2641)))))

(with-track-best (:order-by-fn #'<)

(dolist (state-info data)

(multiple-value-bind (city altitude)

(with-track-best ()

(dolist (city-info (rest state-info))

(track (first city-info) (second city-info))))

(track (list (first state-info) city) altitude)))))

With this limited dataset, the end result would be `(VALUES '("Alaska" "Fairbanks") 531)`

. The inner `WITH-TRACK-BEST`

finds the highest city in each state. The outer `WITH-TRACK-BEST`

finds the lowest of these.

The idea is very elegant!

The :single keyword argument mentioned in the README seems not to be implemented (contrary to :always-return-list). Have you abandoned :single?

You are correct, I got rid of ‘:single’ replacing it with ‘:always-return-list’ and failed to update the information in all places.

I will correct the documentation. Thanks.

Do you plan to add the feature `collect all the best items’? To tell the truth I couldn’t hepl hacking TRACK by adding corresponding branch to the body of COND (and replacing = with EQL on line 35 of track-best.lisp). For personal use only. :$ http://pastebin.com/0tF4ReEJ If you find the code helpful, you can use it verbatim or modified without credits. 🙂

Very nice job!

Indeed, I have been pondering adding a ‘collect all of the best’ option. I’m not settled yet on how I wanted to deal with someone asking for ‘keep 5’ and there being one first place, one second place, and ten third places yet. I’ll ponder it.

Thanks for the pastebin snippet. I’ll look it over.