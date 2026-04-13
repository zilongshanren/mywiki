---
title: Mozilla AI Guide Launch with Summarization Code Example – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2023/11/mozilla-ai-guide-launch-with-summarization-code-example/
author: Dan Brown
published: '2023-11-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Mozilla AI Guide has launched and we welcome you to read through and get acquainted with it. You can access it [here](https://ai-guide.future.mozilla.org/)

Our vision is for the AI Guide to be the starting point for every new developer to the space and a place to revisit for clarity and inspiration, ensuring that AI innovations enrich everyday life. The AI Guide’s initial focus begins with language models and the aim is to become a collaborative community-driven resource covering other types of models.

To start the first few sections in the Mozilla AI Guide go in-depth on the most asked questions about Large Language Models (LLMs). [AI Basics](https://ai-guide.future.mozilla.org/content/ai-basics/) covers the concepts of AI, ML, LLMs, what these concepts mean and how they are related. This section also breaks down the pros and cons of using an LLM. [Language Models 101](https://ai-guide.future.mozilla.org/content/llms-101/) continues to build on the shared knowledge of AI basics and dives deeper into the next level with language models. It will answer questions such as “What does ‘training’ an ML model mean” or “What is ‘human in the loop’ approach?”

We will jump to the last section on [Choosing ML Models](https://ai-guide.future.mozilla.org/content/choosing-ml-models/) and demonstrate in code below what can be done using open source models to summarize certain text. You can access the Colab Notebook [here](https://ai-guide.future.mozilla.org/content/choosing-ml-models/) or continue reading:

## First Steps with Language Models

Unlike other guides, this one is designed to help pick the right model for whatever it is you’re trying to do, by:

- teaching you how to always remain on the bleeding edge of published AI research
- broadening your perspective on current open options for any given task
- not be tied to a closed-source / closed-data large language model (ex OpenAI, Anthropic)
- creating a data-led system for always identifying and using the state-of-the-art (SOTA) model for any particular task.

We’re going to hone in on “text summarization” as our first task.

## So… why are we not using one of the popular large language models?

Great question. Most available LLMs worth their salt can do many tasks, including summarization, but not all of them may be good at what specifically you want them to do. We should figure out how to evaluate whether they actually can or not.

Also, many of the current popular LLMs are not open, are trained on undisclosed data and exhibit biases. Responsible AI use requires careful choices, and we’re here to help you make them.

Finally, most large LLMs require powerful GPU compute to use. While there are many models that you can use as a service, most of them cost money per API call. Unnecessary when some of the more common tasks can be done at good quality with already available open models and off-the-shelf hardware.

## Why do using open models matter?

Over the last few decades, engineers have been blessed with being able to onboard by starting with open source projects, and eventually shipping open source to production. This default state is now at risk.

Yes, there are many open models available that do a great job. However, most guides don’t discuss how to get started with them using simple steps and instead bias towards existing closed APIs.

Funding is flowing to commercial AI projects, who have larger budgets than open source contributors to market their work, which inevitably leads to engineers starting with closed source projects and shipping expensive closed projects to production.

## Our First Project – Summarization

We’re going to:

- Find text to summarize.
- Figure out how to summarize them using the current state-of-the-art open source models.
- Write some code to do so.
- Evaluate quality of results using relevant metrics

For simplicity’s sake, let’s grab **Mozilla’s Trustworthy AI Guidelines** in string form

Note that in the real world, you will likely have to use other libraries to extract content for any particular file type.

```
import textwrap
content = """Mozilla's "Trustworthy AI" Thinking Points:
PRIVACY: How is data collected, stored, and shared? Our personal data powers everything from traffic maps to targeted advertising. Trustworthy AI should enable people to decide how their data is used and what decisions are made with it.
FAIRNESS: We’ve seen time and again how bias shows up in computational models, data, and frameworks behind automated decision making. The values and goals of a system should be power aware and seek to minimize harm. Further, AI systems that depend on human workers should protect people from exploitation and overwork.
TRUST: People should have agency and control over their data and algorithmic outputs, especially considering the high stakes for individuals and societies. For instance, when online recommendation systems push people towards extreme, misleading content, potentially misinforming or radicalizing them.
SAFETY: AI systems can carry high risk for exploitation by bad actors. Developers need to implement strong measures to protect our data and personal security. Further, excessive energy consumption and extraction of natural resources for computing and machine learning accelerates the climate crisis.
TRANSPARENCY: Automated decisions can have huge personal impacts, yet the reasons for decisions are often opaque. We need to mandate transparency so that we can fully understand these systems and their potential for harm."""
```


Great. Now we’re ready to start summarizing.

## A brief pause for context

The AI space is moving so fast that it requires a tremendous amount of catching up on scientific papers each week to understand the lay of the land and the state of the art.

It’s some effort for an engineer who is brand new to AI to:

- discover which open models are even out there
- which models are appropriate for any particular task
- which benchmarks are used to evaluate those models
- which models are performing well based on evaluations
- which models can actually run on available hardware

For the working engineer on a deadline, this is problematic. There’s not much centralized discourse on working with open source AI models. Instead there are fragmented X (formerly Twitter) threads, random private groups and lots of word-of-mouth transfer.

However, once we have a workflow to address all of the above, you will have the means to forever be on the bleeding age of published AI research

## How do I get a list of available open summarization models?

For now, we recommend [Huggingface](https://huggingface.co/models?pipeline_tag=summarization) and their large directory of open models broken down by task. This is a great starting point. Note that larger LLMs are also included in these lists, so we will have to filter.

In this huge list of summarization models, which ones do we choose?

We don’t know what any of these models are trained on. For example, a summarizer trained on news articles vs Reddit posts will perform better on news articles.

What we need is a set of metrics and benchmarks that we can use to do apples-to-apples comparisons of these models.

## How do I evaluate summarization models?

The steps below can be used to evaluate any available model for any task. It requires hopping between a few sources of data for now, but we will be making this a lot easier moving forward.

Steps:

- Find the most common datasets used to train models for summarization.
- Find the most common metrics used to evaluate models for summarization across those datasets.
- Do a quick audit on training data provenance, quality and any exhibited biases, to keep in line with Responsible AI usage.

## Finding datasets

The easiest way to do this is using [Papers With Code](https://paperswithcode.com/methods), an excellent resource for finding the latest scientific papers by task that also have code repositories attached.

First, filter Papers With Code’s “Text Summarization” datasets by [most cited text-based English datasets.](https://paperswithcode.com/datasets?q=&v=lst&o=cited&lang=english&mod=texts&task=text-summarization&page=1)

Let’s pick (as of this writing) the most cited dataset — the [“CNN/DailyMail”](https://paperswithcode.com/dataset/cnn-daily-mail-1) dataset. Usually most cited is one marker of popularity.

Now, you don’t need to download this dataset. But we’re going to review the info Papers With Code have provided to learn more about it for the next step. This dataset is also available on [Huggingface](https://huggingface.co/datasets/cnn_dailymail).

You want to check 3 things:

- license
- recent papers
- whether the data is traceable and the methods are transparent

First, check the license. In this case, it’s MIT licensed, which means it can be used for both commercial and personal projects.

Next, see if the papers using this dataset are recent. You can do this by sorting Papers in descending order. This particular dataset has many papers from 2023 – great!

Finally, let’s check whether the data is from a credible source. In this case, the dataset was generated by IBM in partnership with the University of Montréal. Great.

Now, let’s dig into how we can evaluate models that use this dataset.

## Evaluating models

Next, we look for measured metrics that are common across datasets for the summarization task. BUT, if you’re not familiar with the literature on summarization, you have no idea what those are.

To find out, pick a “Subtask” that’s close to what you’d like to see. We’d like to summarize the CNN article we pulled down above, so let’s choose [“Abstractive Text Summarization”.](https://paperswithcode.com/sota/abstractive-text-summarization-on-cnn-daily)

Now we’re in business! This page contains a significant amount of new information.

There are mentions of three new terms: ROUGE-1, ROUGE-2 and ROUGE-L. These are the metrics that are used to [measure summarization performance](https://en.wikipedia.org/wiki/ROUGE_(metric)).

There is also a list of models and their scores on these three metrics – this is exactly what we’re looking for.

Assuming we’re looking at ROUGE-1 as our metric, we now have the top 3 models that we can evaluate in more detail. All 3 are close to 50, which is a promising ROUGE score (read up on ROUGE).

## Testing out a model

OK, we have a few candidates, so let’s pick a model that will run on our local machines. Many models get their best performance when running on GPUs, but there are many that also generate summaries fast on CPUs. Let’s pick one of those to start – **Google’s Pegasus.**

```
# first we install huggingface's transformers library
%pip install transformers sentencepiece
```


Then we [find Pegasus](https://huggingface.co/google/pegasus-cnn_dailymail) on Huggingface. Note that part of the datasets Pegasus was trained on includes CNN/DailyMail which bodes well for our article summarization. Interestingly, there’s a variant of Pegasus from google that’s only trained on our dataset of choice, we should use that.

```
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
# Set the seed, this will help reproduce results. Changing the seed will
# generate new results
from transformers import set_seed
set_seed(248602)
# We're using the version of Pegasus specifically trained for summarization
# using the CNN/DailyMail dataset
model_name = "google/pegasus-cnn_dailymail"
# If you're following along in Colab, switch your runtime to a
# T4 GPU or other CUDA-compliant device for a speedup
device = "cuda" if torch.cuda.is_available() else "cpu"
# Load the tokenizer
tokenizer = PegasusTokenizer.from_pretrained(model_name)
# Load the model
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
# Tokenize the entire content
batch = tokenizer(content, padding="longest", return_tensors="pt").to(device)
# Generate the summary as tokens
summarized = model.generate(**batch)
# Decode the tokens back into text
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
# Compare
def compare(original, summarized_text):
print(f"Article text length: {len(original)}\n")
print(textwrap.fill(summarized_text, 100))
print()
print(f"Summarized length: {len(summarized_text)}")
compare(content, summarized_text)
```


Article text length: 1427 Trustworthy AI should enable people to decide how their data is used.<n>values and goals of a system should be power aware and seek to minimize harm.<n>People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data and personal security. Summarized length: 320

Alright, we got something! Kind of short though. Let’s see if we can make the summary longer…

```
set_seed(860912)
# Generate the summary as tokens, with a max_new_tokens
summarized = model.generate(**batch, max_new_tokens=800)
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
compare(content, summarized_text)
```


Article text length: 1427 Trustworthy AI should enable people to decide how their data is used.<n>values and goals of a system should be power aware and seek to minimize harm.<n>People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data and personal security. Summarized length: 320

Well, that didn’t really work. Let’s try a different approach called **‘sampling’**. This allows the model to pick the next word according to its conditional probability distribution (specifically, the probability that said word follows the word before).

We’ll also be setting the** ‘temperature’**. This variable works to control the levels of randomness and creativity in the generated output.

```
set_seed(118511)
summarized = model.generate(**batch, do_sample=True, temperature=0.8, top_k=0)
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
compare(content, summarized_text)
```


Article text length: 1427 Mozilla's "Trustworthy AI" Thinking Points:.<n>People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data. Summarized length: 193

Shorter, but the quality is higher. Adjusting the temperature up will likely help.

```
set_seed(108814)
summarized = model.generate(**batch, do_sample=True, temperature=1.0, top_k=0)
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
compare(content, summarized_text)
```


Article text length: 1427 Mozilla's "Trustworthy AI" Thinking Points:.<n>People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data and personal security.<n>We need to mandate transparency so that we can fully understand these systems and their potential for harm. Summarized length: 325

Now let’s play with one other generation approach called **top_k** sampling — instead of considering all possible next words in the vocabulary, the model only considers the top ‘k’ most probable next words.

This technique helps to focus the model on likely continuations and reduces the chances of generating irrelevant or nonsensical text.

It strikes a balance between creativity and coherence by limiting the pool of next-word choices, but not so much that the output becomes deterministic.

```
set_seed(226012)
summarized = model.generate(**batch, do_sample=True, top_k=50)
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
compare(content, summarized_text)
```


Article text length: 1427 Mozilla's "Trustworthy AI" Thinking Points look at ethical issues surrounding automated decision making.<n>values and goals of a system should be power aware and seek to minimize harm.People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data and personal security. Summarized length: 355

Finally, let’s try **top_p** sampling — also known as nucleus sampling, is a strategy where the model considers only the smallest set of top words whose cumulative probability exceeds a threshold ‘p’.

Unlike **top_k** which considers a fixed number of words, **top_p** adapts based on the distribution of probabilities for the next word. This makes it more dynamic and flexible. It helps create diverse and sensible text by allowing less probable words to be selected when the most probable ones don’t add up to ‘p’.

```
set_seed(21420041)
summarized = model.generate(**batch, do_sample=True, top_p=0.9, top_k=50)
summarized_decoded = tokenizer.batch_decode(summarized, skip_special_tokens=True)
summarized_text = summarized_decoded[0]
compare(content, summarized_text)
# saving this for later.
pegasus_summarized_text = summarized_text
```


Article text length: 1427 Mozilla's "Trustworthy AI" Thinking Points:.<n>People should have agency and control over their data and algorithmic outputs.<n>Developers need to implement strong measures to protect our data and personal security.<n>We need to mandate transparency so that we can fully understand these systems and their potential for harm. Summarized length: 325

To continue with the code example and see a test with another model, and to learn how to [evaluate ML model results](https://ai-guide.future.mozilla.org/content/choosing-ml-models/#evaluating-ml-model-results) (a whole another section), click here to view the Python Notebook and click “Open in Colab” to experiment with your [own custom code](https://ai-guide.future.mozilla.org/content/choosing-ml-models/).

Note this guide will be constantly updated and new sections on Data Retrieval, Image Generation, and Fine Tuning will be coming next.

## Developer Contributions Are Vital

Shortly after today’s launch of the Mozilla AI Guide, we will be publishing our community contribution guidelines. It will provide guidance on the type of content developers can contribute and how it can be shared. Get ready to share any great open source AI projects, implementations, video and audio models.

Together, we can bring together a cohesive, collaborative and responsible AI community.

*A special thanks to Kevin Li and Pradeep Elankumaran who pulled this great blog post together.*

## About Dan Brown

Creator, developer, strategist, homebrewer, runner, sock enthusiast, beard evangelist, writer, drummer, adventurer, Oxford comma advocate, and human Swiss Army Knife.