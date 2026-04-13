---
title: How I use ChatGPT daily (scientist/coder perspective)
url: https://bartwronski.com/2024/01/22/how-i-use-chatgpt-daily-scientist-coder-perspective/
published: '2024-01-22'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

We all know how the internet works—lots of “hot takes,” polarizing opinions, trolling, and ignorance.

Recently, everyone has opinions on AI and LLMs/GenAI in particular. I won’t focus here on “gold rush” influencers, bad grifters, people who build their business on thin wrappers around ChatGPT, or naive yet greedy investors – they deserve much criticism, and others deliver it.

There are a lot of valid criticisms or discussion points about possible problems of current approaches to AI – boundaries of creators’ rights and authorship, what is fair use, potential job loss of many professions, “race to the bottom” quality decline when some jobs get automated, further automation of spam, or single corporations controlling essential technology and information. I will not discuss or dispute it here either; some are valid, and I share them, and some are misinformed, emotional, or exaggerated, but this is not the topic of this post.

I want to, however, address and counter some of the criticism, precisely **ignorant criticism**. What do I mean by “ignorant criticism”? People claiming that LLMs are useless “plagiarism machines,” “bullshit generators,” or whatever along those lines. It’s ignorant as those people clearly have not attempted to use them.

This is just wrong. Sometimes, it comes from bad intentions and just plain negativity. Sometimes it comes just from people not understanding what LLMs are suitable for and how they can be helpful right now. Or someone tried to use it once in the wrong way and extrapolated a single bad experience. I will try to convince the second group here – people who have not played around with ChatGPT Plus and cannot imagine a legit use.

I use LLMs professionally and personally daily, and I find them to be amazing tools – not just for productivity but for **making working with technology enjoyable and delightful**, bringing a smile to my face.

If they are useful for me, they cannot be useless (unless my experience does not matter, and then don’t read this post). And people who approach such conversation with good intentions then ask me, “ok, what do you use those for?” So, I went through my last month’s ChatGPT history and will list some of the uses.

## Some notes and disclaimers first

**Note:** I have a ChatGPT Plus subscription. It’s totally worth it, and most of the applications below would not work well without it. If you get discouraged by the free version, do the Plus trial. I was one of those, and a coworker convinced me to try – and I am super grateful. 🙂

**Note:** If you try to use a large language model primarily as a knowledge model, you will be disappointed.

**Note:** In some cases, writing a single query is not enough. It works better as a “conversation”.

**Note:** I am a super basic person. I don’t use any hacks, prompt engineering, nothing special. It’s not necessary for any of the uses I cover below. I write the instructions the way I would write them to a colleague, only sometimes being extra precise.

**Note:** If you think that something/someone producing a bug is a deal breaker, then you will be disappointed. Errors happen (and get fixed immediately after pointing them out). Btw., if you are one of those people, how do you trust yourself or your coworkers?

**Note:** I also recently started using Github Copilot (just for personal use, not professional) and trying out [perplexity.ai](https://www.perplexity.ai/) for more specialized uses – coding, researching topics, and a true legit replacement for Google Search. However, I will not cover those here, as I don’t have enough experience. Both seem promising!

**Disclaimer and conflict of interest disclosure:** This post is very enthusiastic, but it’s a 100% personal opinion. I have no affiliation with OpenAI whatsoever. I just love their product and think it’s the best $20 spent a month. I do work on, however, on machine learning in realt-time computer graphics, but more “traditional” – small models for tasks like compression or denoising. Not generative AI or language models. But as an additional disclosure – AI success is an obvious driving force behind my employers recent market success, so I might be obviously biased.

**Note:** This post might evolve and get edited.

## Use-cases – coding and console tools

### Writing ffmpeg/ImageMagick command lines

I love (and hate!) ffmpeg for what it can do – universal, flexible, and powerful. However – I was never great with command lines; I prefer clicking and GUIs to using the console. Googling for how to do basic things and then “solving puzzles” and combining different options was always frustrating. The same goes for ImageMagick.

ChatGPT solved those problems for me **completely. **Looking at my last month’s history, I see a lot of applications, from simple “convert this AAC/HEIC file to WAV/JPEG,” through “split this image by half horizontally and concatenate it vertically,” to advanced things like **“take a 30-second snipped from this audio file starting at this timestamp and put it in a video in Instagram story aspect ratio and resolution, and place this square image in the middle of it”**. ChatGPT generates the whole sequence of necessary operations and commands.

This is amazing. It saved me hours and helped me create things that I would otherwise be too lazy to do. **It also explains all the options and sequences used so that you can learn and understand them**. It’s fun, informative, and interactive.

I remember only one case where it suggested a solution that had a bug. I explained what this bug looked like, and it immediately fixed it.

### Writing small code scripts (Python, Javascript)

I use Python daily as a research scientist, but things like filesystem operations may happen once a month. I have checked the documentation of os.walkdir() probably hundreds of times. I do operations on mp3 files maybe once a year.

Now, instead of spending 15-30mins on **a script that goes through all mp3 files in a folder and lists me ones that have titles in some format or contain some specific word, renames them, and copies them to some folder** – I just ask ChatGPT, I copy it (reading and verify if it does what I want), run it, and I’m typically done. It suggests the libraries or packages I don’t know (like this reading mp3 metadata).

Last year, I wrote [a blog post on using ChatGPT to create some Javascript](https://bartwronski.com/2023/09/17/praising-hacking-and-low-tech-solutions-chatgpt-wrote-me-a-personal-javascript-browser-plugin/) code for me (I don’t know Javascript).

I used it to write **scripts downloading Spotify playlists’ song titles, YouTube playlists, and HTML pages**. I used to spend hours finding and applying the right libraries, often learning new concepts. With LLMs, it got solved automatically in one go. They even explain what kind of developer keys I need to obtain; and give me a starting point for more advanced applications.

For even smaller tasks like finding files matching specific patterns, I don’t bother using the “find” command, Windows Find, or [Everything](https://www.voidtools.com/support/everything/). For text, I don’t attempt to play with the editor features. I conveniently ask ChatGPT for what I need in natural language and to produce Python code – and see the **Python output in natural, human-readable syntax**. Tools like sed and find were optimized for typing conciseness and limited columns of console (and definitely not for readability), making them ugly and hard to decipher after a while (and, for me, also hard to use). But when the required command line/code can be typed for me, their only advantage – conciseness – disappears, and nothing beats Python’s explicitness, readability, and easy modifiability.

Sometimes, there are bugs, but I read this code; I can fix them myself or iterate with ChatGPT. This is why, at this point, I would not want “OS-level-autopilot” but prefer code generation and my own execution of it.

This is a fantastic time saver. Some people glue batch commands and scripts without effort, but I am not one of them. And it’s not a matter of learning – I generally know this stuff, but if I use it once a month, then I forget and need to refresh. And, btw., playing with this ChatGPT code is also a very fun way of learning and refreshing my memory or discovering something new! It’s also kind of exciting.

### Writing regular expressions

The same goes for regular expressions. I learned them (many times, hah), and I can decipher them or code up a new one with a manual or [Regex 101](https://regex101.com/), but I use them once every two months – so I need to re-learn every single time. ChatGPT gives me a great starting point. **It also explains the regular expression step-by-step**, so it’s a learning opportunity and a chance to refresh my memory.

### Rewriting code snippets in a different language/framework

This is something I am a bit reluctant to do – as it enters the “hallucinations” territory – but I tried this a couple of times and didn’t get disappointed yet. I asked ChatGPT to rewrite a piece of code from TensorFlow (which I don’t know well) to PyTorch, and it worked correctly. But ChatGPT is not a knowledge base or a specialized code model, so I expect it might hallucinate and produce errors. However, for smaller problems, it works very well; I had zero complaints! And it’s a tool, and you can use it or not and to the extent you choose.

### Creating LaTeX figures and tables

I use LaTeX for writing publications and some internal documents if I need to write a lot of math equations. Honestly, I don’t like it. It’s an outdated and frustrating tool. ChatGPT can help here – **write LaTeX code – create tables and figures based on the description or even raw data** (paste a poorly formatted table data and ask for a full table). It can help you debug layout problems and offer suggestions.

Figures you get out of it can be much more than just “insert here a PNG image” figures; they can fully feature Tikz procedural figures. I don’t know tikz at all, and in my last papers, I made beautiful LaTeX embedded figures with ChatGPT’s help. Some are under review, so I’m not pasting the results here, but I might do it later.

And while doing so, something that absolutely blew my mind. Describing a figure is sometimes tricky and pointless – if you tried describing it to a classmate or coworker, you know how difficult it is without a whiteboard. A sketch of a figure is much better than a discussion. So why not do the same with ChatGPT?

How about **sketching a rough figure in Google Slides or PowerPoint just for placement, pasting a screenshot to ChatGPT, and requesting it to create LaTeX code**? Yes, this works!

It’s not 100% accurate; there are often errors, but it is insane that it can work. It’s a language and a bit of vision model and it translates figures into functional code! And if you hit an error, you can describe it to to ChatGPT, and often, it will correct them. Getting a complex figure exactly as you want will probably take half an hour, but it’s half an hour instead of wasting many hours and giving up.

**Protip**: I suggest splitting it into multiple steps and hierarchy; if a figure has 2 parts, iterating on them separately.

**Protip**: When you describe an error twice and it cannot correct it or introduces a different error, this is the point when I give up and decompose or change the problem. Typically, it’s enough to progress. I have no reason to not think it will be addressed by a future, larger models.

### Transforming data and presenting it

Similar to the above, ChatGPT is excellent at transforming data, including misformatted or almost raw data. Do you have a CVS-like table and want to process it in Python for plotting or extraction? Or maybe even a raw, natural text from a scientific paper? You can spend a few minutes doing regex + replacement in your favorite text editor, dealing with new lines, commas, special cases, whatever. (And iterating if some lines don’t conform to it for some reason)

Alternatively, just paste it to ChatGPT and ask it to recreate it in any desirable format. **You can even request that it plots it in any format you’d like – and ChatGPT will write a Python script and execute it**! You can see the code it wrote and executed, copy it, and iterate on it yourself.

Again – the idea is that it assists you and provides a starting point for mundane, non-creative tasks – and you can focus on the juicy and exciting parts!

### Extracting data from images and figures

Take the previous point – how about combining this with its OCR capabilities and input images?

I take screenshots of tables or charts in documents or web pages, paste those images to ChatGPT, and request that it generate a Python list, a dictionary, or a new plot. And then, I can process, analyze, or save it for future use.

The first time I did this and it “just worked,” I was mind-blown again. And it also works on things like PDFs.

## Use-cases – language, images, and knowledge

### Help with grammar

Now, we are entering the “natural language” “language model” territory, so it is something that it does very well on – and possibly more relatable to non-programmer users. I am not a native English speaker – if you look at my older blog posts, you will notice numerous mistakes, unnatural language, and missing articles (we don’t have those in Polish and rely on complex declination and context instead). I got much better through living in the US and speaking it almost exclusively (including at home); plus, for longer forms, I use Grammarly (which also has some kind of language model and ML, I believe).

But I am still imperfect, and sometimes, I need to be extra precise and correct and try to sound as natural as possible – in critical communication and papers (especially abstracts).

**I ask ChatGPT not just to rewrite it but to highlight and explain my mistakes. I’m learning in the process and reinforcing my better writing skills.** The mistake highlighting and explanation is fantastic. No native speaking coworker was able to help me this way (though two reccommended [“The Elements of Style”](https://en.wikipedia.org/wiki/The_Elements_of_Style) to me).

### Shortening and restructuring paragraphs

I use ChatGPT semi-automatedly to shorten academic paper abstracts for my automatic notes – I even [wrote a blog post about it](https://bartwronski.com/2023/09/17/praising-hacking-and-low-tech-solutions-chatgpt-wrote-me-a-personal-javascript-browser-plugin/).

But in a non-automatic way, it’s also super helpful in making sentences or whole paragraphs more concise for any **writing with a word limit** or simply increasing text precision or readability. I find it useful in academic writing (abstracts and proposals!) and similar, where you want to be absolutely unambiguous and as concise as possible.

### Helping put thoughts into words

You can write a few bullet points and get a fully fleshed-out email, letter, or paragraph. I know – this one might be “outrageous” to some and is an object of jokes.

If you are a fan of Slavoj Zizek, you might have seen a meme where his original joke and statement about… let’s call it “relationships”… is paraphrased as “a student uses their ChatGPT to write an essay, I use my ChatGPT to rate it, our superegos and academic supervisors are satisfied, and the real teaching and learning can finally start!”.

It’s obviously a joke, and some people are upset that one person writes an unnecessarily long email from just 2 to 3 bullet points, and another summarizes it into points. I wonder if they noticed we live in a society and among people, and all communication is codified to convey more than just raw thought. You cannot just send two bullet points without any form or structure to a government institution.

But I digress! **I use it for cases where otherwise I would have to rely on templates anyway**. If you dealt with US immigration (either as a visitor from many visa countries, a skilled worker, someone seeking an immigrant visa/permanent residency, or helping someone get those – I did all of that!), you might have requested (or written) **visa or admission recommendation letters**. Those are silly and formulaic and either written by lawyers (if someone hires them) or copied from online templates. I have even seen a situation where someone told me, “Here is a scan of my signature; write the letter yourself and use it. I don’t care”. This made me very uncomfortable as using someone’s signature, even with their consent, feels fraudulent…it also showed how that person doesn’t care about me, but whatever.

So, ChatGPT is a fantastic time saver for this and other official documents. I spend 10 minutes listing why someone should get a visa or a Green Card (because I know them and their achievements, and I care), and then an AI assistant writes the letter for me from this formulaic template. I do minor edits, make sure this is my letter, and we are done. Win-win.

I also used it a few times in communication with people I don’t know well and for instance, I wanted to remind them that they promised something to me. **I have a mild form of ASD** (diagnosed early with Asperger’s syndrome) and trouble reading people and adjusting my communication style to the situation and context. This and occassional insecurity and anxiety means **I can sometimes spend literally an hour obsessing and stressing over a 3 line email**. Did I use the correct tone? Does this sound passive-aggressive? Is this not too insecure? Is it not formal enough? Is it too formal? **An LLM assistant can write such an email for me in 30 seconds**.

(No, this blog post was not written with an AI assistant at any point. 😅 Just Grammarly. I actually enjoy writing and blogging. But sending emails… it depends.)

And this applies to many more situations and interactions that are not personal. “Just learn the language, learn to write well, and put in the effort” is a shitty and exclusionary advice, especially when targeted at immigrants and non-native speakers.

Side note and anecdote: I remember when I was at Google, everyone spent 2 weeks per year on bullshit peer reviews (managers at least 2x more). Nobody writes honest ones. In my first review cycle, I wrote a couple peer reviews honestly – positive, praising my colleagues, but also highlighting areas for improvement. There were fields for this and I thought I would help them grow, right? I got reprimanded by my manager, who was very upset and told me to never write anything even lightly critical of anyone there. I wonder how many Googlers use LLMs now to write those bullshit reviews. 😉

### Summarizing articles

I used this option just a few times and as a starting point. I generally love reading, and having ChatGPT summarize every piece of writing sounds like a way of torture in one of the Dante’s inferno circles. But sometimes, the article is wordy, dull, or written in a way that makes it non-enjoyable (like an unfocused interview with an annoying person done by a boring journalist). And I need some of this information to stay up to date and informed. The late capitalism ad economy also encourages a lot of articles that contain new information in a single paragraph, and the rest are fillers to show crappy ads. This wastes people’s lives and time.

I used ChatGPT a few times, tasking it to** summarize a PDF printout of an article with the main points that the article is making**. It can list it in bullet points, summarize arguments that someone is making, and I can even ask it to list possible counter-arguments or how I can learn more about a particular topic/issue.

Alternatively, it can help you with a 30-page-long article written by an expert. You might not have enough background to go through it and be interested in the topic, but not that interested. Just task LLM with summarizing it.

### Summarizing YouTube videos

The first time I tried this, I was super excited. The late capitalism ad economy and time wasting problem is much worse with YouTube videos, plus the information is very hard to find and navigate, right?

While ChatGPT cannot summarize a YouTube video directly, there are free services that transcribe or allow you to download automatic YouTube transcriptions/subtitles of videos. Then you are left with a wall of text, lots of “ummms”, and “words from our sponsor.” You probably don’t want to read this stuff. So just save it, upload it as a document, and use ChatGPT to summarize the **YouTube video transcript in bullet points**.

I used this a few times, mainly for videos I have already watched and containing highly technical tips, for example, tricks for manipulating wavetables in [my favorite VST audio synthesizer](https://kilohearts.com/products/phase_plant). I could write it all manually, scribbling through the video, pausing, alt-tabbing – and waste an hour of my time. With ChatGPT I had it done in 5 minutes of figuring out how to transcribe the video, and then 5 minutes of editing the resulting notes to my liking.

You can do the same to any videos full of filler and prolonged to 10 minutes for monetization despite having a minute of actual content. Don’t let others disrespect you and waste your time; this is the most precious resource you can never take back. And if you care for the content creators’ financial well-being, all who are worth watching will tell you they don’t make almost any money from ads, and you can support them through Patreon or buy something they make. (I do, and I hope you too!)

### Explaining mistakes when learning

You can use ChatGPT to **explain your own mistakes or bugs**! I heard of people succeeding with code bugs (someone mentioned that it found a multithreading bug in their code), but I used it for something significantly simpler – **learning Spanish**.

I use Duolingo (and while it does not teach me to speak it or formulate thoughts well, it brought my understanding of written Spanish to the level of reading newspapers), and it generally does not explain grammar, especially at more advanced levels. Whenever I am puzzled, “Why did it say that my answer is wrong?”, **I take a screenshot on my phone, paste it to ChatGPT, and get a very nice and comprehensive explanation of my mistake and the grammar concept**!

I don’t need to type anything or copy-paste, which is annoying on mobile; I just paste the app screenshot as an image.

### Small translations

Since I mentioned learning languages, I used it a few times for small translations. From my limited experience, it translates *across cultures and expressions* much better than Google Translate. So the translation won’t be word-to-word faithful but will fit the target language native speakers’ expectations and idioms way better. It’s way more “natural”. And I can further control this cultural adaptation versus faithfulness through prompt instructions.

### Private tutor

ChatGPT can be your private teacher/tutor/mentor on common topics (or semi-specialized, but I would not trust niche ones). A few times I used it this way, it was great – **task ChatGPT with asking you (!) progressively difficult questions and rating your answers on some topics you are trying to learn**.

Answer those questions, ask it to rate them and where you could expand or what you understood wrong. And then keep the conversation going. Don’t do any prompt engineering magic, just converse like with a teacher (to whom you don’t need to be polite).

Try it on a new domain that you feel you are a little bit familiar with. Ask it to roleplay in a new language. Or to give you some simple math problem to solve and then rate the solution.

If the topic you are trying to learn is not super exotic and you have some basis, it is absolutely excellent and engaging. I spent hours on it. **The last time I had so much fun and engagement with some new technology was when I discovered Wikipedia as a teenager** and spent days following links and learning.

Can it hallucinate wrong answers? Definitely, especially on niche topics. But even a very expensive and qualified private tutor does that too. I think everyone had experience with great teachers who were ignorant (and confident) about certain things. And – in my experience – claims of hallucinations are exaggerated. I will often tell you, “I don’t know”. Many examples online of people finding errors are from the non-Plus, regular version, or from a long time ago and older models.

### Generating images – my music

My biggest passion outside of work and computer graphics is making music – sound design, music production, composition, arrangement, and [recently DJing](https://soundcloud.com/elirian/dj-set-12302023-outer-product?in=elirian/sets/dj-sets). I don’t use any AI for this (ok, I kind of indirectly do! I was surprised seeing Rekordbox copies tens of Tensorflow DLLs for stem separation, and many VSTs started to use ML models). Still, recently, just for fun, I added DALL-E-generated **images as virtual “single” covers**. Is it the world’s best art? No, it’s cheap and corny/tacky. But it’s fun; when I do it in the middle of the production, it can guide me with new ideas about the vibe and the atmosphere and “ground” me in a particular direction (instead of a Brownian walk).

![](../../assets/e5bfa8b0382242d5.jpeg)


![](../../assets/e5bfa8b0382242d5.jpeg)

[one](https://soundcloud.com/elirian/outer-product-melted-core)and

[two](https://soundcloud.com/elirian/outer-product-the-ritual). Corny, cheap? Whatever, it’s fun and fits my hobby and vision. I had fun making those.

And recently, I finished four tracks and had two people independently tell me, “I liked them all, but [this one](https://soundcloud.com/elirian/outer-product-the-ritual) is my favorite, possibly because of the ‘cover.’”

Am I replacing an illustrator artist’s job here? No. Earlier, I would not do this at all. And if this were ever to be released (and not just a hobby that I keep pumping money into), the label would hire a real artist and designer.

### Generating images – mood boards and references

Working with artists in video game studios, I was always fascinated with their “references” folders. They had terabytes of (unlicensed!) downloaded images that they would use to get inspired and fit a particular theme, like when working on some specific asset or level. Then, they would create “mood boards” (sometimes working with an art director) – loose associations and a collection of images serving as an inspiration for shapes, colors, patterns, and themes.

(**Note: **Sometimes, this liberal approach to downloading images and getting “too inspired” causes them trouble. You probably heard of cases like “video game studio stole something from another artist’s work.” But it’s not really “evil large studio vs. small creator,” but just one of the studio artists, often junior, being sloppy and lazy, forgetting where they got some reference image from, and not caring to check. And then nobody in the management chain caring to check it either.)

I have no background or experience in visual arts other than photography, and I cannot draw a straight line, so I **found working with ChatGPT on “mood boards”** super useful for visual creativity. I use AI-generated images in “mood boards” for tattoo ideas (and can communicate more easily with artists – who will do the proper and own design anyway), with my wife for how we want to decorate rooms, or, as I mentioned, for other creative endeavors like music.

![](../../assets/231fa3d86aaffaad.jpeg)


![](../../assets/231fa3d86aaffaad.jpeg)

### Brainstorming on ideas – titles, themes

I am terrible at naming things (just check [the titles of my publications](https://bartwronski.com/publications/); they are the most descriptive and least creative in the world). I am not a native speaker and I might easily use unnatural language constructs and cliches from other languages, so I prefer to “stay safe”.

But I can use LLMs to help me with more interesting naming. ChatGPT can give me ten possible titles, and I can take and modify one (or completely ignore them but still have a new idea of the direction I want to go with!).

Similarly, it’s a quick random idea generator for some theme (with my wife, we were brainstorming ideas for a NYC-themed calendar with the assistance of ChatGPT). Does this mean that I am giving away my agency and creativity? No, far from it!

**It’s similar to making generative music (which can be fully random or procedural). You generate many random ideas and then pick the one that resonates with you as a starting point and manually iterate from there.** Your creativity and agency still expresses itself in the selection and iteration. Even the most creative people use these tricks to work around creative blocks and spawn new projects (just read any course book on creative music composition or production and you will find suggestions like those).

### Knowledge base – here be dragons

This is something that should be done only rarely, if ever (repeat after me – “Language models are not knowledge models!”), but, unfortunately, **Google Search became garbage in the last ~two years**. Getting mostly results from Quora (which barely works when you use an ad blocker and is full of 100% wrong answers), (mis)information boxes, ads, and SEO spam.

It became a disaster. For many trendy topics, it’s literally impossible to find any real information (that is not some form of ad or business-related) on Google besides “search term reddit”. Otherwise, the first page is either ads or SEO crap. If Google does not fix that, they have maybe a year until people leave forever (when the quality declines, A/B tests – that corporations love as they give them an illusion of being data-driven and “objective” – won’t show it immediately, like slowly boiling the frog. And I feel the metaphorical frog is already boiled.)

**On some occasions, I was asking ChatGPT technical questions and getting solid answers** – but I treated them as potential hallucinations. But from those, I knew where to look further – and was not disappointed.

I am starting to use [perplexity.ai](https://www.perplexity.ai/) for this purpose instead, and so far, it’s very, very promising! Concise, precise, links references. And if it doesn’t know an answer, instead of hallucinating, it will say, “There are not many resources that answer this question.” On the downside – it generates answers based on what people paste online, which is unreliable.

**Protip:** One fun, legit, and not very risky use of LLMs is asking loose questions, associations, and things you are unsure about pop culture. It can answer “what is the 90s song that goes dudududu du du du du?”, but even if it doesn’t, it’s harmless and fun.

## Conclusions – my take and the future

From the above, you can see that I typically don’t use LLMs as search replacements or knowledge models.

I don’t use them to do tasks “start to finish” and don’t automate my life.

I don’t rely on Gen AI to replace my creativity.

I use them interactively and my decision making and attention is always in the process.

LLMs don’t make me a “100x programmer” or whatever.

CEOs and AI influencers who think they will replace employees with LLMs and automation are idiots.

But.

**LLMs are absolutely delightful and bring me a lot of joy.**

**They keep me engaged and interested in everything they are involved in** – it’s not a replacement for me, not automation, but an assistant who is fun to work with and helps me learn and improve.

I have not felt so much joy and awe playing with any technology for at least a decade.

VR? Uncomfortable and nauseating. AR? An attempt to make yourself always embodied in your work, notifications, and ads. Crypto? Useless, serving crime, and full of frauds. Web3? Straight petty capitalist grift to commoditize our whole lives. The last decade had a ton of extremely lackluster, overhyped technology.

But **AI is the real next (or rather – current) big thing** – at least in my opinion. With my focus here on LLMs, I didn’t even scratch the surface, as ML has already revolutionized fields like Computer Graphics and Computer Vision. With LLMs and Gen AI, for me, it’s not about business or productivity. I don’t care! What matters is that **I have a lot of fun; it can serve me and be playful and enjoyable**. And yes, this is super important – **technology should be fun, playful, and enjoyable**. I want to feel like I felt back in the mid-90s, when I was a 7-year-old discovering DOS, Windows 3.11, starting to program in Turbo Pascal, and then having my first experiences with Web 1.0 and creating my first “useless” HTML homepage. We are not reduced to productivity and the value we can bring to the capital. Also, this is why I believe open-source LLMs should be advanced, and everyone in the world should be given equal access (preferably on their own, local device, not controlled by any corporation).

There are valid technical and social concerns and criticisms, but I stay optimistic. They seem solvable, and it’s totally worth it. LLMs will improve, but even if they don’t evolve much, I am ok with the ones we have today, as they already make my life better. I hope this post showed you how and maybe encouraged you to go and have fun with them in new ways.

Great read Bart! I have many of the same use cases, another one is supporting roleplaying with image generation (Dall-E), descriptions and translations.

Sounds like a great support of such hobbies! 🙂 I haven’t played pen and paper RPGs in a while, but I bet DMs love it.

When I visit this page in Google Chrome on Android, I get a pop-up offering to summarize your entire article for me.

Overall I agree with a lot of your points. I use ai quite a bit while coding and problem solving, and it saves me a ton of time and I feel like I’ve learned a ton in a short period of time as well. It’s like there’s less context switching and things stick easier.

Major thanks for the article.Much thanks again. Really Great.

Hey Bart, thanks for all these useful use cases! I learned about OCR here, which is a really cool feature. I use the free ChatGPT and I think it is good enough for my everyday tasks as data engineer. I also use Chat for stock market investments to learn which companies have specific production capabilities.