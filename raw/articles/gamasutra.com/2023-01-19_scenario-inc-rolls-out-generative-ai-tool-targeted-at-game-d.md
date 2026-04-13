---
title: Scenario Inc rolls out generative AI tool targeted at game devs
url: https://www.gamedeveloper.com/art/scenario-inc-rolls-out-generative-ai-tool-targeted-at-game-devs
author: Bryant Francis
published: '2023-01-19'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Scenario Inc rolls out generative AI tool targeted at game devs

Scenario. Inc describes its tool as a "generator of generators," that lets devs iterate on 2D art assets trained on their own art datasets.

![The logo for Scenario GenAI. The logo for Scenario GenAI.](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt2466decd809f3475/650ec789de5e9fc87052e048/7bc7a7d64bd4_(1).jpg?width=1280&auto=webp&quality=80&format=jpg&disable=upscale)

The generative AI startup behemoth is landing on the video game industry's shores. Today San Francisco-based startup Scenario Inc is opening up access to the [Scenario GenAI Engine](https://www.scenario.gg/)—a tool that riffs on the generative AI process popularized by Midjourney and DALL-E by letting developers upload their own 2D art assets to use as their defining dataset.

This rollout also comes with the news that the company has raised $6 million in funding from Play Ventures, Anorak Ventures, Venture Reality Fund, Founders Inc. and Heracles Capital. Oculus co-founder Brendan Iribe, Twitch founder Justin Kan, and former Blizzard executive producer Hamilton Chu (now working at Marvel Snap developer Second Dinner) are among those investors.

In an industry that's relied on various forms of procedurally-generated content over the years, it's not exactly surprising that the generative AI art phenomenon would make an appearance. The creation of high-quality art assets at a mass scale has long been a challenge for the game industry, and in theory, tools like the Scenario Engine help solve that problem.

Generative AI has made a big splash on the world not just for its beautiful (and often uncanny) creations, but also for a slew of ethical issues raised by the mass-processing of art on datasets. Artists have already identified instances of Midjourney and DALL-E recreating their art without their consent (after realizing their art was included in the training datasets for this software without their consent), and just yesterday Time Magazine learned that OpenAI chat tool ChatGPT relied on cheap, possibly exploited labor in [Kenya](https://time.com/6247678/openai-chatgpt-kenya-workers/) to moderate adult and violent content.

Scenario's founders seem aware of these controversies and want to address them head on. Co-founder and CEO Emmanuel de Maistre stated in a statement that artists should be "empowered to train their own generators, have control over their art direction and work alongside, not against, AI."

Of course good intentions don't automatically solve ethical questions. In advance of today's announcement, Scenario invited Game Developer to sit down with de Maistre for a demo of Scenario—and discuss the ethical and technical challenges generative AI brings to the video game industry.

## Scenario GenAI Engine is a tool for mass-producing 2D assets

De Maistre kicked off our demo with an example of how developers can use Scenario to import their art assets. First, they select a batch of their own images to upload, then give the engine a set of nouns and adjectives to describe their assets as. De Maistre uploaded a selection of potion images, and added a set of correlating nouns and objectives so they could be tagged in Scenario's back end.

He explained that developers could build a generator with just 10-20 images—the amount of images uploaded to the engine would help determine how well it could create images in their style. Uploading too many, he warned, might increase the amount of time it takes to create a generator or create variations.

These would take 20 minutes to turn into a "generator," so we moved on to reviewing examples of generators he'd already created.

In this set of generators, there were two tabs—one set for the user's own personal generators, and another for reviewing "public" generators. De Maistre explained that all generators created by Scenario users are private by default, but some may choose to make them public, so other folks can experiment with them.

![A potion produced by the Scenario GenAI engine. A potion produced by the Scenario GenAI engine.](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/bltfbdc8023d90b3c67/650ec79e7bc3898bee2be84f/Spiral_galaxy_inside_a_potion_detailed_beautiful_holographic_3D_purple_dust_on_the_floor_(2).png/?width=487&auto=webp&quality=80&disable=upscale)


De Maistre pulled up a generator for making isometric buildings. Here, he explained that Scenario is still only optimized for producing 2D art assets. He said that numerous studios he's pitched the tech to have talked about the need for 3D art assets, but that the technology isn't there yet. Still, it seemed possible that if a studio wanted to turn 2D assets into 3D assets (or just turn out concept art that could be recreated in 3D), there was still utility.

He explained that the assets Scenario currently produces are currently being used for "mobile games, casual games, concept art, and web3 companies willing to do lots of NFTs."

He invited me to give prompts to turn out a series of isometric buildings inspired by the ones he already had on hand. I threw out the nouns "watchtower, temple, obsidian, snowy," and he added other nouns like "stone" and "winter." The tool also displayed a set of keyword suggestions developers could use to tweak their output, like lighting direction or other weather variations.

De Maistre finished up the inputs, then told the Scenario Engine to produce a few image sets with different variable parameters, such as sampling steps. For the uninitiated, a "sampling step" is when the software scans the dataset the user has uploaded. If you select "100 sampling steps," it scans the dataset 100 times. "120 sampling steps" is 120 times, etc. etc.

Within a minute or two, we were reviewing a selection of Watchtower-shaped buildings in wintery settings with various "temple" elements worked in. The dataset he originally showed me included images of cottages and other fantasy stone ruins. The new images included some nightmarish artistic mismatches, but plenty of them looked like realistic 2D assets in the art style of the original, non-AI created dataset.

The only thing the engine didn't know how to handle was my suggestion of the noun "obsidian"—the original dataset didn't have any reference for the black volcanic rock, so it just made buildings out of stone instead.

De Maistre was able to produce more iterations of these assets by telling the generator to reference one of the created images, and also by telling it to "ignore" key words like "green" or "summer."

This carried on for a little longer, with de Maistre repeating the fact that this was all only referencing the referenced dataset. I asked about the datasets Scenario was built on before it reached this stage, and he explained that Scenario was built on an earlier version of [Stable Diffusion](https://stablediffusionweb.com/) (version 1.5, to be precise). That means it was trained on a [LAION](https://laion.ai/) dataset, and references images scraped from that dataset when filling in the gaps on generative AI requests that Scenario users make of the software.

That seemed as good a time as any to start asking about the ethical and legal questions about generative artificial intelligence.

## Generative AI comes front-loaded with legal and ethical questions

In 2022, Ars Technica [reported](https://arstechnica.com/information-technology/2022/09/artist-finds-private-medical-record-photos-in-popular-ai-training-data-set/) that a California AI artist who works under the pseudonym "Lapine" found medical images of herself when scouring a LAION dataset. Lapine told the website at the time that she was uncomfortable with the fact that these private images (who she'd legally only granted permission to her doctor to use), are now "part of the product." Vice News reported on other [ethical red flags](https://arstechnica.com/information-technology/2022/09/artist-finds-private-medical-record-photos-in-popular-ai-training-data-set/) the dataset has produced.

Artists of all stripes have been also ringing alarm bells about how generative AI tools can wind up using their art assets without their permission—sometimes even leaving behind traces of the signature or watermark they left on an image before it was scraped into a dataset.

To be clear, that doesn't seem easily replicable in Scenario. If what de Maistre presented holds up, then all a game artist would see in replications of their art is references to their own work. The platform's terms of service also requires that users strictly upload content that they have legal permission to use, whether it's their own creation or one they paid for and retain copyright ownership of.

![A side-by-side of Isometric buildings uploaded as training data for Scenario, and the buildings Scenario produced. A side-by-side of Isometric buildings uploaded as training data for Scenario, and the buildings Scenario produced.](../../assets/48b0c8f1cbb976e1.img)

Left: buildings uploaded to Scenario as training data. Right: the buildings Scenario produced.

It seemed obvious to me that this raised questions about how you make sure users are adhering to the terms of service. De Maistre did say the company is ramping up its moderation efforts, beginning with the process of training Scenario to recognize images of explicit content, which he said was "easy." Training it to recognize the intellectual property of non-users would take much more work.

In the future, he hypothesized about a process similar to how YouTube does automated content moderation. Companies that own the rights to video or audio content offer samples of that content to YouTube and ultimately the platform scans video uploads to remove or flag content users don't own the copyright to. (That process has also been [criticized](https://www.insider.com/youtubers-channels-are-being-held-hostage-with-fake-copyright-claims-2020-6) for favoring large companies over small creators).

I asked de Maistre if he ever thought Scenario would need to rely on external labor to help identify and tag images uploaded into the platform. He said that for now, Scenario's identification tools are all automated, but human moderation "might be required" in the future.

De Maistre seemed receptive to the questions of ethics and legalities I was raising. Cautioning that he wasn't an "IP lawyer," he did say it would be a problem if the outside possibility of misappropriated art from the LAION dataset snuck through. He made reference to the [numerous](https://www.theverge.com/2023/1/17/23558516/ai-art-copyright-stable-diffusion-getty-images-lawsuit) [lawsuits](https://www.polygon.com/23558946/ai-art-lawsuit-stability-stable-diffusion-deviantart-midjourney) recently lobbied against Stable Diffusion and other generative AI platforms.

So if all of those pitfalls are already in play, why dive into the world of generative AI as an entrepreneur? De Maistre explained that Scenario is the second company he's co-founded—the first being a 3D scanning company that used machine learning to generate 3D assets using smartphone technology. "Then I realized that AI would be way better content than scanning," he said.

The rest of de Maistre's pitche revolved around the idea of "supercharging creativity." His pitch for generative AI revolved less around the notion that "anyone" could make game assets, but rather that trained artists and developers could use tools like Scenario to expand the work they're already creating. He said he's spoken with several game artists interested in using the technology this way.

For smaller developers who might need more assets for their game than they could produce on their own, he said that some prospective Scenario users compared it to the process of purchasing assets on the Unity and Unreal asset stores. Some of those developers have told de Maistre that this tool would let them "do assets" on their own.

His enthusiasm for generative AI went beyond 2D and 3D art. Today, it's 2D images. But tomorrow, it's gonna be 3D," he said. "And we're gonna go into sound and voices one day and animation and words. I think one day there will be text-to-games." He referenced how some [ChatGPT](https://openai.com/blog/chatgpt/) users have been sharing samples of how the platform can spit out pitches for games.

De Maistre's comments sometimes seemed exemplary of the concerns we've heard from artists and creatives about the potential of AI, but he did say he doesn't want to brush those concerns off. "We want to do the right thing," he said as we closed out our chat. "I want to be proud of the product and the company."

"Personalizing AI is the right direction to go," he insisted, with some dismissive words to the idea of a one-size-fits all trained dataset where creatives don't know what images it's referencing. He expressed eagerness to stay active in "the ethical debates" in the years ahead.

## So is Scenario "ethical" generative AI?

Boy do I not know the answer to that question. Not only am I not a lawyer, I am not an ethicist.

Walking away from this demo, I found Scenario's focus on generating AI iteration by using datasets provided by the user to be compelling enough. If that was all the tool did in a vacuum, I'd say the question would have to do more about the ethics of creating two dozen iterations of "watchtower temple" by hand versus having a machine do it for you.

In that line of ethical thinking, I would be weighing the value of creating assets by hand, thinking of how the player will interact with them, considering the structure of my watchtower temple and how it would fit in the game world. When I tell a generative program to do it, I'd have some great variations of my original concept—some I might not even have considered, but all I really did was look at the batch of them and go "that's cool, let's use that one."

![A portrait of a Golem made by Scenario. A portrait of a Golem made by Scenario.](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt4438876a0c56d33a/650ec7995ec1bb6c53e18bfb/Golem_illustration_(made_with_Scenario).png/?width=1280&auto=webp&quality=80&disable=upscale)

Now I'm just thinking about how Golems—a creature of Jewish folklore—are used as rock monsters.

It's an interesting thought exercise, but one overshadowed by a bigger issue: if generative AI developers produces "ethical" software on the back of unethically-produced models and tools—shedding the oversourced datasets but keeping the speedy best practices—is it ethical to use that software?

I've sort of phrased the question in a way that assumes all generative AI tools are unethically produced. Developers working on other toolsets might well be shouting "yes, we made generative AI software using image datasets we had full legal permission to use, and we want to make better tools off that so developers can make better games!" as they read this article.

Fair enough! I certainly hope tools like that manifest.

Right now I'm worry that a focus on IP ownership and copyright violation would dilute the layers of other ethical and societal problems the technology represents.

I also worry that the "speed" that company founders and investors keep describing in how fast this field is moving is more like a wake generated by bad actors—if someone else played fast and lose with ethics and legal questions, that saves you the trouble of having to do it yourself, right?

And yet worry as I do, generative AI tools like Scenario just...work. As a creative person noodling on my own projects, I liked the process De Maistre demonstrated. Critics of AI art have referred to self-described "prompt engineers" as "shitty art directors," but I'll be damned if art direction isn't a fun process.

At the very least, this reality throws sand in the face of the notion that generative AI "[democratizes](https://www.theatlantic.com/technology/archive/2022/12/generative-ai-technology-human-creativity-imagination/672460/)" art. Art has always been democratized—it's literally something anyone can pick up and have fun with.

While witless writers like me waffle back and forth on the ethics of generative AI, engineers are embracing the Zuckerbergian mantra of "[move fast and break things](https://www.businessinsider.com/meta-mark-zuckerberg-new-values-move-fast-and-break-things-2022-2)," creating tools that are about to wash over the video game business.

What's next for them? We're about to find out, whether we like it or not.

Update: This article previously referred to Venture Reality Fund as "VR Fund." It has been updated with the correct name.