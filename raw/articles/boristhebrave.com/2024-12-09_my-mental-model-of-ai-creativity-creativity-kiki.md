---
title: My Mental Model of AI Creativity – Creativity Kiki
url: https://www.boristhebrave.com/2024/12/09/my-mental-model-of-ai-creativity-creativity-kiki/
author: Boris
published: '2024-12-09'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I went to [some lectures on the future of science in games](https://www.kcl.ac.uk/events/next-level-2024-exploring-the-future-of-science-and-games) recently, and the [keynote speaker](https://www.youtube.com/watch?v=GbptbbiKaj8&list=PL4YMKmeHWBisfQM0mxdDgsxNANvddUikL&index=7) was [Tommy Thompson](https://www.aiandgames.com), an well-known AI expert in the game dev space.

Of course, by AI, he didn’t mean the modern sort that dominates the news. His focus is AI for games, which is algorithmic and rarely involves any ML component. Still, he spoke about the challenges the industry faces regarding Image Generators, LLMs and so on. He specifically called LLMs “stochastic parrots”, which I found disappointing. Imho it’s an incredibly misleading model of what LLMs are capable of and is usually deployed to downplay their abilities and belittle them. But it’s a common view, particularly in creative industries.

So what **is** a better model? It’s clear that they are not that smart in most ways we consider important, but they do have some interesting capabilities. Here’s model I use that I feel give a better intuition for what they can and cannot do.

## Creativity Kiki

Can models be creative? Or do they just regurgitate things from their vast training set. Certainly, they can unquestionably create images and sentences that have never *exactly *been seen before, but if they are trivial variants of something already done, no one would call that creative. I think to answer the quesiton properly, you need to be precise about how you define creativity.

I like to think of the sum total of all human creations to be a big blob that looks something like this:

![](../../assets/3d8ec86406369eea.png)

It’s a funny shape, spread out in the dimension of platonic ideals. There are some areas that we’ve really explored in depth, like say, Marvel movies or romance novels, and others that we haven’t, like epic poems about chinchillas. Some of those ideas will be of interest while others are boring. You are creative when you find something both novel (outside the shape) and interesting (at least, to some audience).

Technically, any automated system can be creative in this sense. A simple random sentence generator, like infinite monkeys, will randomly spit out something that fits these criteria sooner or later. But realistically, it won’t, and it would be fair to say that the generator is fully uncreative. Procedural Generation experts have [understand well the limits of earlier generation techniques](https://www.youtube.com/watch?v=cPs3VANXFcU).

I think LLMs and Image generators don’t really have the capability to push the envelope outwards, except by random chance. They lack the ability to understand what novelties a human would find interesting, or systems that let them explore outside their training datasets. Even humans find this sort of true creativity difficult and rare.

But what they do have is [interpolation](https://en.wikipedia.org/wiki/Interpolation) – the smooth blending of multiple existing things together. And it’s not a stupid form of blending. It’s more like an interpolation through [concept space](https://en.wikipedia.org/wiki/Latent_space), an unintuitive idea that is closest to our human concept of a “mashup”. You can use tools like [ArtBreeder](https://www.artbreeder.com/) to explicitly play around with this, but it’s an integral part of how most ML works. It’s particularly clear with GANs, which let you smoothly vary parameters for various effects, but you can get good blending results from many modern AI systems.

But the thing is, the blob I drew above is spiky. Interpolation can take you to points **outside** the blob, to new creative areas.

![](../../assets/28dbc55e98a1f8e2.png)

Is this *true* creativity? No, probably not. But it’s a very productive way of creating, nonetheless. So much of our culture is a mashup anyway, I estimate 90% of a creative’s work is having a good reference pool of things created in human culture, and finding interesting new ways to arrange them. The website [TVTropes ](https://tvtropes.org)dedicates itself to finding common patterns, often between disparate media, and after reading the site for a bit you start to see the matrix – everything is well worn references and tropes, put together in a new and interesting way, with a smattering of fresh ideas to glue it all together.

AIs can be almost superhuman in this kind of work – they are capable of learning a much wider reference pool, and their internal works force ideas to be represented as numerical embeddings, which aids interpolating and combining ideas 1 .

So the answer is yes and no. AI is not creative in the way we like to think of creativity – a deliberate choice and exploration. But they are creative in the pragmatics – their output is capable of surprise and can easily be something genuinely novel.

- Exploiting this fact is how we get fun things like
[Golden Gate Claude](https://www.anthropic.com/news/golden-gate-claude), a chatbot that can answer anything, but always steers the conversation back round to talking about the Golden Gate Bridge.[↩︎](https://www.boristhebrave.com#d4d765b3-299b-48ab-9f74-612fc2c7e5f4-link)