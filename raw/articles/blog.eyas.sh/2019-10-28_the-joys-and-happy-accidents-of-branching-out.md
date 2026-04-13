---
title: The Joys and Happy Accidents of Branching Out
url: https://blog.eyas.sh/2019/10/the-joys-and-happy-accidents-of-branching-out/
author: Eyas Sharaiha
published: '2019-10-28'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

*How helping on a film set led to me down a serendipitous path, publishing a new
open source library, and getting an IMDB mention.*

About a year ago, a [friend](https://www.tnpacheco.com/) asked me—along with
some others—to help as extra hands on set filming the second season of an
absurdist comedy mini-series she was working on called
[Look it Up](https://www.youtube.com/channel/UCnE8NF1yYScr6yOYwbofBQQ).

![](../../assets/88f9ac04ac28ed7c.img)

Helping film *anything* wasn’t something I thought I would ever do, so I was
excited to try it out. We weren’t necessarily trusted with anything difficult;
carry equipment around, slate shots, clear the set, and move things around in
general. It was interesting to see how much thought and effort goes into
composing a shot, or storyboarding a scene.

Filming took place on a weekend. Five episodes, each under 2 minutes, took up about 2 days to film (including make-up, breaks, and lots of setup in between).

One of the cool things I saw in the filming process was how sound was treated.
In the first season, the show’s creators enlisted help of another friend,
[Elizabeth McClanahan](https://www.imdb.com/name/nm5105317/), to be their
[re-recording mixer](https://en.wikipedia.org/wiki/Re-recording_mixer). Her help
salvaging a lot of the audio, mixing some sound effects for them, and also
working with them to re-record some of the dialog was eye opening, and they
entered their second season hoping to avoid some of the same mistakes (and try
to learn how do to the sound themselves). So when I was there for the second
season, we heard how a boom operator moving the mic too fast is enough to ruin
the shot with wooshing air, and made a point to be silent, slow, and deliberate.
I don’t think I had been as still for as long in quite a while.

Beyond being interesting, though, going out of my comfort zone for a weekend helped in a few fun ways:

- Being physically present, I was tasked with playing an extra for an opening
credit. For some reason, that came with an
[IMDB credit](https://www.imdb.com/title/tt10254736/). Kind of cute to cross off an item that wasn’t even on your bucket list to begin with. - Caring about a friend’s artistic endeavor (wanting it to do well, get traction, etc.) caused me to think about practical tech solutions to problems I hadn’t occupied myself with.

You see, while I tend to think of myself as a creative *problem solver*… if I
know what the problem is. I often say I don’t see myself as starting a new
company or idea, but rather as a lot of friends’ go-to person to make an
existing idea a reality.

One of the privileges of working in software engineering at a large company is
that you don’t run into life or career problems too often (except for all those
problems *at work* you get to solve). Much of my perspective and creativity—as
much as I try otherwise—is silo’d within work, that I find my externally visible
contribution of the world hard to quantify.

![](../../assets/ed5f9eab813faf8c.img)

## Wanting Someone to Succeed

It turns out that “Look it Up” is a hilariously bad name for a web-series, if
you want to get discovered.
[Ashton Shepherd has a song with that name](https://www.youtube.com/watch?v=p1kT4u_D5PA)
with 3.5M views on YouTube. The phrase is also quite a common idiom, with lots
of content about the phrase. Things get worse when you consider that the “it” in
the keyword, is such a common word that it often goes ignored, resulting in a
lot of “look up”-related content as well (who knows,
[Google’s new BERT natural language model](https://blog.google/products/search/search-language-understanding-bert/)
might make this better in the future, as phrases are understood contextually).

They’ll need to market it. Part of this includes tapping into their networks, e-mailing their friends, and trying to generate some attention for what they have. As a fan or ally, I also tried to do the same with my own friends.

But I was still thinking about that *Look it Up* song
[knowledge panel](https://yoast.com/all-about-googles-knowledge-panels/). Which
got me reading about how the SEO world is still all the rage about
[structured data](https://developers.google.com/search/docs/guides/intro-structured-data)
and [Schema.org](https://schema.org). Interesting. I remember being excited
about the [semantic web](https://en.wikipedia.org/wiki/Semantic_Web) way back
when, but forgot about it and thought it just
[went to obscurity](https://twobithistory.org/2018/05/27/semantic-web.html).
Turns out, in the SEO corner of the web, Schema.org is *cool*.

And as often, my chain of thought transitively morphs into reading and research largely unrelated to the topic at hand. “How do I get Look it Up (the web series) to be noticed” forms into “can Look it Up be represented as a factual entity that is picked up by search and knowledge engines” which itself forms into “can authors of the web influence this” then “so how do I write JSON-LD” and “how do I validate JSON-LD”… but then, the chain of questions hit a wall.

## The Upside of Finding Bad Things

You see, the answer to the question “how do I validate JSON-LD” is bad enough that I:

- had to look for another answer in disbelief, and, when I failed,
- knew I had to make it better.

And reader, let me tell you this, if *I* am the one who needs to make it better,
it’s a really sad indictment of the state of affairs.

Let’s start with the answer to “How do I validate JSON-LD” (or, more
specifically, Schema.org JSON-LD that search engines find useful). The
*state-of-the-art* way to do this, it turns out, is through *validators*; online
tools basically made up of a web form that takes your data in and spits out a
verdict: your data is *bueno* or *no bueno*. The most used is Google’s
[structured data testing tool](https://search.google.com/structured-data/testing-tool),
followed by Bing’s
[markup validator](https://www.bing.com/toolbox/markup-validator) and Yandex’s
[microformat validator](http://webmaster.yandex.ru/microtest.xml).

So to craft a static piece of JSON-LD structured data, you’d need to:

- find the appropriate specific type on
[Schema.org](https://schema.org), reading it’s docs, - use Schema.org as a reference to write in the properties you care about,
- transitively look up the types of each of those properties on Schema.org, repeating 2. and 3. recursively as needed (and consulting examples on the site as necessary),
- paste the resulting JSON in your favorite validator.

And *voila*! Unless the validator tells you something is wrong. Then you go back
and fix it, potentially consulting steps 2. and 3. again. You do that a few
times, and then, *for real*, *voila*! You’re done. And you got some structured
data to show for it.

Maybe this is fine and dandy if you’re crafting one hard-coded piece of
structured data. But what about programmatically generated data (e.g. say you’re
[IMDB](https://www.imdb.com/), or an e-commerce company)?

This whole thing sounded like compiler driven development. You have this buffer of text that represents something (a program, or structured data) and you need to periodically feed it to a compiler or validator to know that it’s correct. In development, people use IDEs, or code editors with at least syntax checking, if not also language services, code completions, and the works. Why can’t we do the same for Schema.org?

## Hello, schema-dts

That was the birth of [schema-dts](https://github.com/google/schema-dts), an
open source TypeScript project released under Google. I’ll talk some more at a
later point about the experience of releasing open source code at Google. For
this post, I’d like to focus a bit on the *why* and *how* components of that
project.

I’ve always been a huge fan of TypeScript. Its ability to specify shapes of
plain JavaScript objects (through types), its ability to do discriminated unions
(think of Schema.org JSON-LD as `@type`

-tagged unions), and the great ecosystem
of language services, completions, and general tooling around, made it jump up
as a clear example for writing good structured JSON.

So I Googled: “Schema.org TypeScript”. *Nada*. “JSON-LD Typescript”. “TypeScript
structured data”. Wow. This thing actually doesn’t exist. And it felt so
obvious.

So, I had to make it.

That Sunday night, I sat down for some 9*ish* hours from around 8 PM till 5 AM
or so coding up my first proof of concept. It worked! I created a program that
downloads a `.nt`

N-Triples file representing an ontology (I mostly tested in on
the Schema.org files available), parses it, and transforms it multiple times,
generating a TypeScript file representing all the class types defined in that
ontology.

schema-dts has been a microcosm of branching out in itself. It’s given me many
unique experiences: Navigating open source at Google; having an OSS project
people actually use; an excuse to
[write](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/)
[multiple](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/)
[technical](https://blog.eyas.sh/2019/07/schema-org-datatype-in-typescript-structural-typing-doesnt-cut-it/)
[articles](https://blog.eyas.sh/2019/07/schema-org-classes-in-typescript-properties-and-special-cases/)
about the topic; and an excuse to be additionally self-promotional.

Perhaps seeing myself as a solver of existing known problems, rather than new ones, is not an indictment of my creativity, just an indication of how little I branch out.