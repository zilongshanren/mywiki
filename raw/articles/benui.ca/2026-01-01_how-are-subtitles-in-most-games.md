---
title: How are subtitles in most games?
url: https://benui.ca/blog/make-game-subtitles-better/
published: '2026-01-01'
source_blog: ben🌱ui
source_site: https://benui.ca/
category: unreal engine
fetched: '2026-04-13'
---

I couldn't find any particularly official-looking stats, but it seems from forum polls and asking around, that the vast majority of players play with subtitles turned on. Also in most games that I can recall, subtitles are enabled by default.

There are a huge number of reasons why people play with subtitles enabled:

- They
**don't understand the audio language**well enough to be comfortable. Either it's not their native language, or characters use a dialect they're not familiar with. - They have
**issues with their hearing**, or the mixing is such that voices aren't clear. - They play in a
**noisy environment**. - They play in an environment where they
**can't turn on the game sound**(playing games while others are asleep). - They prefer having both sound and text to
**make sure they don't miss anything**.

So subtitles are a pretty big deal.

## How are subtitles in most games?

In a word, bad.

Currently most games seem to base subtitles entirely on their corresponding **audio cue**. A cue is a logical chunk of sound, in our case a line of dialogue read by a voice actor. It could be a short phrase or an entire paragraph, depending on how the voice actor and audio engineer decided to split it up.

Then, in-game, the transcribed dialogue is displayed while the cue is being played.

On-screen, this audio cue could end up as one, two or three lines of text depending on the screen size and font size.

In most cases, the UI programmer or game designer picks a font size that's kind of legible from a sofa, and calls it a day, focussing on other features instead.

The problem is that **there's a lot more to subtitles than this**.

Let's look at some examples:

Witcher 3

Tiny text, very long lines, pretty hard to read.

![Tiny text, very long lines, pretty hard to read.](../../assets/b68decb5ec400af6.webp)

XCOM 2

Again, very long lines, small text. We can do a lot better than this.

![Again, very long lines, small text. We can do a lot better than this.](../../assets/bb5f87220bce15df.webp)

Dishonored 2

Line length is better, still kind of small though. Also as we'll see later splitting after an "and" is not ideal.

![Line length is better, still kind of small though. Also as we'll see later splitting after an "and" is not ideal.](../../assets/62c2bcd0898aa236.webp)

Metal Gear Solid 5

Good font size and line length. However orphans and three-line subs could be avoided. Subtitles also clash with in-game prompts.

![Good font size and line length. However orphans and three-line subs could be avoided. Subtitles also clash with in-game prompts.](../../assets/501307d542858593.webp)

Uncharted

Uncharted's subtitles are good. Their subtitles look hand-authored, and while they might be longer than what is traditionally used for TV and film, they're very easy to read.

![Uncharted's subtitles are good. Their subtitles look hand-authored, and while they might be longer than what is traditionally used for TV and film, they're very easy to read.](../../assets/bb18c33da7f1acd8.webp)

So subtitles are a bigger deal than you might expect. With so many games containing hours of cutscenes and audio dialogue, it would make sense to do subtitles right.

Are there any other industries we can learn from that might have already solved this problem?

## Film and TV

Stating the obvious, but films and TV have dealt with subtitles for decades. Over time some best practices have evolved that all lead to one goal; make subtitles easy-to-read at a glance, so the viewer can concentrate on the scene.

The BBC has made their [subtitle guidelines available on-line](https://bbc.github.io/subtitle-guidelines/), and they're a fantastic resource in general.

A lot of what I describe below is taken directly from the BBC subtitle guidelines. So What Should We Do?

Hopefully by now I've convinced you that good subtitles are important, that we can do a lot better, and that there are good examples of what to work towards.

It's possible to **programmatically produce much better subtitles** by implementing a system that uses some fairly simple rules.

**Note:** All the guidelines below are just that — guidelines. There are always exceptions, and there are many cases where two rules will actively fight against each other. In the case of generating subtitles by hand, it would be up to the judgement of the author. In our case, we have to be at peace with the fact our system will sometimes produce less than ideal results.

## Keep Lines Short

Extremely long lines become difficult to read when they stretch on and on without a break.

Extremely long lines become difficult to read when they stretch on and on without a break.

This is the **single most important thing** you should care about when setting up your subtitles system. Everything else is just icing on the cake. There are so many studies out there for both print and on-screen media that show people have a hard time reading huge lines of text. In printed text I've seen 70-80 characters mentioned, and the BBC has extremely short recommended lines of only [37 characters for historical reasons](https://bbc.github.io/subtitle-guidelines/#Line-breaks), but 50-70 characters works well in my experience.

## Put Line Breaks In Smart Places

After changing the line length, the next set of rules are all concerned with how split up lines and pages.

The BBC guidelines includes a list of **places where you should avoid splitting words**:

- article and noun (e.g. the + table; a + book)
- preposition and following phrase (e.g. on + the table; in + a way; about + his life)
- conjunction and following phrase/clause (e.g. and + those books; but + I went there)
- pronoun and verb (e.g. he + is; they + will come; it + comes)
- parts of a complex verb (e.g. have + eaten; will + have + been + doing)

It's important to note that all of the suggestions below are English-specific. The assets you require to implement the rules are also language-specific (a list of conjunctions, pronouns etc).

Let's explain some of the rules with examples.

## Avoid Orphans

Make sure there's not a word all alone.

Make sure there's not a word all alone.

Look at that poor word all alone on the last line. In typographical circles this is tastefully called an orphan. It's more of an aesthetic choice but it does improve readability.

Orphans in typography usually refer to words on their own on a line, as in the example above. However for our purposes we can extend the definition to include single before punctuation, like below.

Even with two sentences there can be problems. Just like this one.

Even with two sentences there can be problems. Just like this one.

## Avoid Article and Pronoun Splitting

She will travel to Oxford to buy an automobile for her father.

She will travel to Oxford to buy an automobile for her father.

Articles in English like a/an/the, pronouns like I/you/he/she, possessive pronouns like my/your/his/her etc. To implement this you will need a language-specific list of pronouns and articles. Using a simple list of pronoun + word will lead to false positives, but the alternative is performing grammatical analysis on the text, which seems like overkill.

We went to Canada to see her grandmother for Christmas

We went to Canada to see her grandmother for Christmas

## Avoid Adjective Splitting

This requires a huge list of adjectives and adverbs to work in English, so it's not always achieveable. But the BBC guidelines recommend that adjectives be kept with their subjects. In French this would be even more tricky as adjectives can go before or after the noun.

Today I went shopping and bought a beautiful parrot from a peculiar boutique.

Today I went shopping and bought a beautiful parrot from a peculiar boutique.

Today I went shopping and bought a beautiful parrot from a peculiar boutique.

In the example above not only did we move *beautiful* onto the next line, but we applied the article-splitting rule to the subsequent result, and moved the article *a* down too.

## Split on Punctuation

The most natural place to split a line or a page is just after punctuation like commas and full stops.

You know I can't go swimming today, it's much too cold outside.

You know I can't go swimming today, it's too cold outside.

This often works with the avoid orphans rule. In the example above, we can treat a single word after punctuation on a line as a kind of orphan, and move it down.

## Splitting Lines Between Pages

So far we have focussed on splitting lines on a single page. What do we do when the line of dialogue runs over two lines?

Cues that run over two lines will have to be split into multiple pages (paginated). The problem then is you don't have timing information to know when to switch pages to match the dialogue audio. In my experience, a simple percentage-based guess works surprisingly well. If the page split is at 65% of the dialogue, change pages once 65% of the audio has played. You can change the contribution of different characters to the length, for example increasing full stops and setting spaces to zero length but it doesn't always help. A more robust alternative that works if you have the time or you haven't started your audio yet, is to try to keep cues fairly short.

Picking the right place to split pages is almost the same as picking where to split lines, all of the same rules apply.

The BBC guidelines recommend using ellipsis to indicate that a sentence runs between pages.

## Language-specific Rules

Sorry 94.5% of the world, I left talking about non-English rules to the end, and glomped it all together. I'm not much of a polyglot, so I can't give many examples, but you should be aware in your system that some of your assumptions will be broken in other languages.

To give just a few examples that I've encountered:

French has spacing between punctuation and the word before. So you can't use spaces as a foolproof way to split up words, or you'll end up with punctuation on the next line.

Japanese, Chinese and some other languages don't use spaces to separate words. There are still the logical concepts of words as grouped characters though. You can sometimes be lax about splitting in the middle of a word over two lines, but not between two pages where the reader would have to wait to see the rest of the word. You should talk to an expert on Japanese but to do word segmentation correctly you could check out tools like ChaSen, Mecab or Juman.

## Conclusion

I think that subtitles systems often get implemented quite simply because people think "they're just subtitles" and if text is displayed on-screen, that's good enough. I hope these guidelines have shown that something much better is possible.