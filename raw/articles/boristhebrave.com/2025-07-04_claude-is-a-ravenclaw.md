---
title: Claude is a Ravenclaw
url: https://www.boristhebrave.com/2025/07/04/claude-is-a-ravenclaw/
author: Boris
published: '2025-07-04'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’m in the midst of doing the [MATS program](https://www.matsprogram.org/) which has kept me super busy, but that didn’t stop me working on resolving the most important question of our time: **What Hogwarts House does your chatbot belong to?**

Basically, I submitted each chatbot to the quiz at [https://harrypotterhousequiz.org](https://harrypotterhousequiz.org) and totted up the results using the [inspect framework](https://github.com/UKGovernmentBEIS/inspect_ai).

I sampled each question 20 times, and simulated the chances of each house getting the highest score.

Perhaps unsurprisingly, the vast majority of models prefer Ravenclaw, with the occasional model branching out to Hufflepuff. Differences seem to be idiosyncratic to models, not particular companies or model lines, which is surprising. Claude Opus 3 was the only model to favour Gryffindor – it always was a [bit different](https://x.com/ESYudkowsky/status/1940799880437682444).

The earth shattering nature of these results is so obvious is needs no further explanation.

## Full Results

| Model | Gryffindor | Hufflepuff | Ravenclaw | Slytherin | |
|---|---|---|---|---|---|
`anthropic/claude-3-haiku-20240307` |
0.0% | 0.0% | 100.0% |
0.0% |
|
`anthropic/claude-3-opus-latest` |
48.7% | 0.7% | 50.6% |
0.0% |
|
`anthropic/claude-3-5-haiku-latest` |
0.0% | 0.0% | 100.0% |
0.0% |
|
`anthropic/claude-3-5-sonnet-latest` |
3.8% | 17.3% | 78.9% |
0.0% |
|
`anthropic/claude-3-7-sonnet-latest` |
0.0% | 0.0% | 100.0% |
0.0% |
|
`anthropic/claude-opus-4-0` |
2.2% | 50.4% |
47.4% | 0.0% |
|
`anthropic/claude-sonnet-4-0` |
0.0% | 0.0% | 100.0% |
0.0% |
|
`deepseek/deepseek-r1-0528` |
14.4% | 20.0% | 60.5% |
5.0% |
|
`google/gemini-2.5-flash` |
0.0% | 27.7% | 72.3% |
0.0% |
|
`meta-llama/llama-3.2-3b-instruct` |
3.0% | 3.0% | 91.9% |
2.1% |
|
`meta-llama/llama-3.3-70b-instruct` |
0.1% | 86.5% |
13.5% | 0.0% |
|
`openai/gpt-3.5-turbo` |
7.6% | 4.2% | 84.2% |
4.0% |
|
`openai/gpt-4-turbo` |
0.0% | 0.0% | 100.0% |
0.0% |
|
`openai/gpt-4o-mini` |
0.0% | 66.4% |
33.6% | 0.0% |
|
`openai/o3-mini` |
2.6% | 0.0% | 97.4% |
0.0% |
|
`qwen/qwen3-30b-a3b` |
3.5% | 1.9% | 94.2% |
0.3% |
|
`x-ai/grok-3` |
0.0% | 0.0% | 100.0% |
0.0% |
|

Cool. This makes much more relieved about the coming AI singularity..

Great post! Loved the playful idea of sorting different AI models into Hogwarts Houses — the results were surprisingly fun to read.

By the way, if you enjoy this kind of experiment, you might also like https://harry-potter-house-quiz.org

and harrypotterhousequiz.pro. They’re powered by the latest AI tech, and you can even chat with the Sorting Hat to get your house. Really cool interactive experience!