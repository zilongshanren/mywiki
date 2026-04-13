---
title: Praising hacking and low-tech solutions. ChatGPT wrote me a personal Javascript
  browser “plugin.”
url: https://bartwronski.com/2023/09/17/praising-hacking-and-low-tech-solutions-chatgpt-wrote-me-a-personal-javascript-browser-plugin/
published: '2023-09-17'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Intro

![](../../assets/2455cfe4467c239d.png)


![](../../assets/2455cfe4467c239d.png)

[Obsidian](https://obsidian.md/).

I love unsophisticated solutions with minimal dependencies. There is a reason the blog you are reading right now is on wordpress.com and ugly – the friction from a post idea and starting to write it to finally publishing a post is zero. Just write it in Google Docs, copy + paste it to WordPress, and be done with it.

I call it a “low-tech” solution, and many will object. Wouldn’t some pure HTML be a low-tech solution? Not really. First of all – much more effort is required to learn it (ok, I wrote my own personal home pages dating as back as the 90s, even wrote a bunch of PHP CMS’s, but modern HTML + CSS + JS are not that 🙂 ), make it look ok, and maintain it. There are alternatives, but then I see many of my peers writing gigantic posts on how they spent hours (days) setting up static website generators, and I think – if I had to go through it, I would probably be frustrated enough not to write a post that I wanted to write. And some of them don’t write any more posts than “welcome to my new awesome statically generated blog!”

And I get it – I love all kinds of tinkering tinkering as a passion and hobby. Playing with and getting to know new tech is why many of us became coders or engineers. We do it for fun (and for work), get used to it, and then it’s hard to resist when facing a problem that must be solved quickly.

Once you want to get stuff done, it’s better to take off your “tinkerer” hat and the rose-tinted glasses that deceive you that “the technology used to be better back in the day before Electron and virtual machines everywhere.” No, it wasn’t! It was terrible, with constant crashes and necessary OS reinstalls every few months if you used Windows or constant kernel recompiles for incompatible drivers that were bricking your machine on Linux. The overall computer experience was reserved for “experts” and frustrating even for them. You might remember it differently, as “golden times,” because you were young, and all of it was fresh, magical, and exciting.

So, for me, a low-tech solution is something with low know-how, immediate, no installation of libraries, no compilation, just sit down and solve a problem you have and move on with your life. If I see any “install this npm library,” “first, configure CMake,” or anything like that, I stop reading.

But solving problems using computers is great, actually, in 2023 – thanks to Javascript, browsers, and the help of LLMs such as ChatGPT. I think they are already changing our relationship with the technology, understandably causing some old-timer-nostalgia folks upset. Those two sentences above certainly enraged many groups of my peers (especially among “old-timer” game developers, as there is a sentiment that all of this is “terrible” and not performant).

## Example use-case – collecting and annotating links

Attempting to add planning and structure to my life ends badly and discourages me from doing things. I was always skeptical about structured journaling, personal knowledge management systems, etc. (This is my preference! Everyone is different). But not collecting links and not taking any idea notes is like a difficulty-level “nightmare” for doing any long-term research or a scientific or engineering career, especially in our times when we are overwhelmed with information and almost everyone I know self-diagnoses with having some form of attention deficit (and for some, those problems are very real, just don’t self-diagnose based on TikToks and memes). I read a dozen publications a week and have a good memory, but remembering exact titles and links is impossible (and “that paper that proposed to replace X with Y” is not very search-friendly).

Around 8y ago, I started to use Evernote to just dump links to papers, presentations, or blog posts with a few keywords that are meaningful just for me, and it was enough. Over time, I started similarly to collect music links. Unfortunately, Evernote was becoming progressively worse and bloated over time (I never used 99% of its functions), and my notes were extremely messy, with broken formatting when pasting stuff from other websites. A recent update breaking the search functionality (I think it got fixed quickly afterward?) was also the proverbial straw that broke the camel’s back. I was done with it.

I decided to give [Obsidian ](https://obsidian.md/)a try instead, with many people praising its simplicity (it’s just Markdown files!). This seems to work great, and thanks to it “just being Markdown,” I got drawn to the appeal of expanding it and customizing it through things like offline Python scripts operating on files or plug-ins to automate some of the things I repeat daily. Is it me tinkering with things that I criticized above? Not really; I use it like notepad.txt with some nice cross-device sync options and basic formatting.

Luckily, sometimes you don’t even need to write any offline scripts or dedicated software plug-ins or whatever, and even simpler solutions can be powerful, and I will describe one of those. With ChatGPT, it’s possible to “write” one not knowing anything about the domain or programming language you use. 🙂

## Low-tech hacking a “plugin” – the thinking process

My most common use-case for collecting paper links is opening the website (typically arXiv), copying the link, paper title, authors, and sometimes abstract, and adding a 1-10 word unstructured description (and some tags) that I will remember. Some similar workflows are for YouTube videos or music from YT or SoundCloud. I put those in notes that are organized per topic (for example – by music genre or with research papers by the application or subdomain).

![](../../assets/d8a762373b41129c.png)


![](../../assets/d8a762373b41129c.png)

I wanted to automate it to save on many CTRL+C / CTRL+V, alt-tabs, typing Markdown hyperlinks, and manual link clean-ups. It’s relatively quick but also a bit annoying, especially when done many times in a row, multiple times a day.

Here’s how my thinking went:

- I was tempted to write an Obsidian plug-in, but I realized that all the data I needed was available in the browser, and I need just to “generate some very basic Markdown”.
- Why not write a browser extension?
- Or, why write an extension at all? You can run JavaScript directly.
- Why not just run Javascript directly as a bookmark, executable from the address bar?
- I know (almost) no Javascript for websites or all the DOM management stuff, and I have no need to learn it, so why not ask someone to help me?
- Why would I ask anyone, especially online (risking unhelpful replies, “why do you want to do this?”) if I can ask (free) ChatGPT? 15 minutes later, I had an initial solution, and with some tweaks, another 15 minutes later, the final “product” that saves me a few (annoying and not creative) minutes per day.
- Then, I realized – why not have abstracts summarized for me by the said ChatGPT? It is a language model specialized in language transformations! (This is where it stops being completely free, as the API access requires buying some credits).

In Firefox, you can create a bookmark with Javascript code:

And the “keyword” is something that you can type from the URL to execute it directly. Super neat!

## The solution – automatic paper summary Javascript and Markdown link generation “plugin”

The solution is extremely simple. I found someone explaining online how to run Javascript code in Firefox bookmark and how to make it executable for the address bar. (I assume that you use Firefox or other privacy-respecting web browser. I would personally not paste any API key to a Chrome bookmark, as those get scanned, and there were reports of DMCA takedowns on private bookmarks!)

Then, I asked ChatGPT how to extract paper titles and authors from an arXiv website using Javascript and immediately got a correct answer. Two questions later, I had “abbreviated” author names.

Unfortunately, for YouTube, it didn’t give me a correct answer; the DOM element it suggested didn’t exist, but I used the page inspector to find the element’s title, and similarly so for SoundCloud.

Then, I had to add credits to the [ChatGPT billing page](https://platform.openai.com/account/) and create a new API key. I also “asked” ChatGPT how to use its API in Javascript. I don’t know how much it will cost me, but for now, I added $10 worth of credits and hope they will last for months. This step is obviously optional if you don’t want to pay OpenAI for whatever reasons.

Half an hour later, I had a solution:

```
javascript:(function(s){
var pageURL = window.location.href;
if(pageURL.includes('arxiv')) {
var combinedText = '';
pageURL = pageURL.split('?')[0];
var paperTitle = document.querySelector('h1.title').textContent.trim();
paperTitle = paperTitle.replace(/^Title:/i, '').trim();
var authorElements = document.querySelectorAll('div.authors a');
var authorNames = Array.from(authorElements).map(function(author) {
const names = author.textContent.trim().split(' ');
if (names.length > 1) {
return names[0][0] + '. ' + names.slice(1).join(' ');
}
return author.textContent.trim();
}).join(', ');
var abstract = document.querySelector('meta[name="citation_abstract"]').getAttribute('content').replace(/\n/g, ' ').trim();
endpoint = 'https://api.openai.com/v1/chat/completions';
prompt = 'Summarize the following paper abstract in two short and concise sentences. Skip all the \'glue\' phrases like \'this paper\', assume that each sentence\'s subject refers to the paper. For example, instead of writing \'this paper introduces\', write \'introduces\'.Assume that the reader knows the domain well, so skip introductions. Be concise and to the point. The abstract:' + abstract;
fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer sk-YOUR_VERY_SECRET_KEY'
},
body: '{"model": "gpt-3.5-turbo","messages": [{"role": "user", "content": "' + prompt + '"}] }'
})
.then(response => response.json())
.then(data => {
abstract = data.choices[0].message.content;
combinedText= '[' + paperTitle + ']('+pageURL+') **Authors:** ' + authorNames + ' **Abstract:** ' + abstract +'\n';
alert(combinedText);
})
.catch(error => {
console.error('Error:', error);
});
} else if(pageURL.includes('youtube')) {
var videoTitle = document.querySelector('h1.style-scope.ytd-watch-metadata').textContent.trim();
videoTitle = videoTitle.replace(/\[|\]/g, '');
pageURL = pageURL.split('&')[0];
combinedText = '[' + videoTitle + '](' + pageURL + ') \n';
alert(combinedText);
} else {
var videoTitle = document.querySelector('h1').textContent.trim();
videoTitle = videoTitle.replace(/\[|\]/g, '');
combinedText = '[' + videoTitle + '](' + pageURL + ') \n';
alert(combinedText);
}
void(0);
})();
```

It’s some abysmal Javascript code, but who cares? It works for my use case. It’s probably also a security nightmare, but again – it does not matter to me. I added this code as a bookmark. Now, I open this bookmark, or just type “obs” from the page address bar, giving me something to copy directly to a note. The unfortunate side effect that I know is that the latter (typing in the address bar) destroys the URL.

It works very nicely on papers, YouTube, and Soundcloud – and if I ever need some more websites or use cases, I will just quickly hack those in. 🙂

What about some factual inaccuracies that can emerge from the stochastic nature of a language model? I don’t care. I only collect links to papers I have read to quickly correct those. Most of the time, I edit those abstracts a bit anyway and add my custom tags.

## Summary

Sometimes, “hacking” some stuff up is the right way to go. If you don’t need to, just try to think about the “lowest cost” possible solution, where cost is your cost, human cost. Something that will not require compilers, downloading libraries, dealing with NPM stuff, or learning any new skills that were not useful for you before. (If you never used a skill so far, the likelihood of needing it again is low. Unless it’s something you really wanted to learn.)

I think that with LLMs, we are witnessing a new paradigm and the beginning of a new era of how we interact with technology. It’s not going to replace – for now – low-level programmers and their hand-optimized loops with SIMD intrinsics; not going to replace security researchers and carefully written code in safe languages (whether VMs or something like Rust); not going to replace good web designers and web coders, and not going to replace specialists of all kinds. But it can help them.

The LLM technology and the way it is provided to us is still clunky and lacks good user interfaces, but all big corporations are working on incorporating it into products and solving those problems. I am 100% convinced that it will open new ways for “everyone” to create and “script” personalized solutions to their unique problems and follow their unique preferences. I find it amazing and revolutionary, and I understand all the hype. Yes, most people doing start-ups in this space are gold-rush grifters, but it’s the case in any area with large amounts of money flowing into it (and investors who cannot tell grifters apart from legit entrepreneurs and actually prefer bullshit smooth-talkers). This doesn’t change the potential of the technology and how paradigm-shifting it is for human-computer interactions. And I’m very happy to incorporate it into my personal workflows.

Those JavaScript snippets are commonly called bookmarklet (or favlet for oldtimy FF) and they are a whole genre.

chatGPT knows what they are and knows to write them (Bard as well) if asked explicitly.

Pingback: How I use ChatGPT daily (scientist/coder perspective) | Bart Wronski