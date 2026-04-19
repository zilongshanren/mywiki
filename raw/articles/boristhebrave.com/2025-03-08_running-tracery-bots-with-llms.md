---
title: Running Tracery bots with LLMs
url: https://www.boristhebrave.com/2025/03/08/tracery-ai/
author: Boris
published: '2025-03-08'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Tracery](https://tracery.io/) bots were a fun, simple, way of making generative texts. They are basically an easy way to specify generative grammars via a simple JSON file format. There used to be a horde of fun little tracery bots on twitter until API changes shut them all down.

![](../../assets/282a0f5313d914e2.gif)


![](../../assets/282a0f5313d914e2.gif)

![Darcy is saying "You are well-educated, but no cromulent enough to intrigue me"](../../assets/02b1a5f0b047f420.png)


![Darcy is saying "You are well-educated, but no cromulent enough to intrigue me"](../../assets/02b1a5f0b047f420.png)

![](../../assets/7f44d623bba7f4a9.png)


![](../../assets/7f44d623bba7f4a9.png)

Nowadays, you can prompt a chatbot to get whatever you want. But that lacks the same charm, and it doesn’t give you the control you’d want for something unleashed on the internet. Let’s do something about that.

Last year, I spoke about [constrained text generation](https://www.boristhebrave.com/2023/02/11/constrained-text-generation-with-ai/) – how you can force LLMs to output things matching a given schema by tinkering with probabilities as the sentence is being generated. Since then, the concept has become mainstream, with many tools and APIs offering the ability to restrict the output. It’s typically used to get JSON output, or to keep a chatbot’s responses guided and neutral.

I made a quick prototype of a generator that instead constrains the output to behave like a tracery script. It works by converting tracery to EBNF, a standard way of representing context free grammars, which can be fed into standard tools (I’m using [llama.cpp](https://github.com/ggml-org/llama.cpp)).

This gets the best features of both systems. The output is still strictly under your control, but the LLM smarts can control the randomness of the choices.

## Basic Example

Consider this simple Tracery grammar.

```
{
"sentence": ["#he_she# picked up #his_her# bag."],
"he_she": ["he","she"],
"his_her": ["his","her"]
}
```


This can generate one of 4 sentences, as there are two independent choices of two items each.

- he picked up his bag.
- he picked up her bag.
- she picked up his bag.
- she picked up her bag.

Clearly some of these sentences make more sense than others. When we run a LLM generator 1 constrained to this grammar, it strongly prefers to pick sentences where the pronoun agrees with the subject

.

[2](https://www.boristhebrave.com#a2172d46-8c60-442b-88ca-050083a32393)| Sentence | Frequency |
| she picked up her bag. | 49% |
| he picked up his bag. | 29% |
| she picked up his bag. | 13% |
| he picked up her bag. | 9% |

The same technique can fix a lot of grammar/agreement issues which are otherwise a pain to deal with in tracery.

```
{
"sentence": ["I picked up #a_an# #fruit#."],
"a_an": ["a","an"],
"fruit": ["apple","banana","orange"]
}
```


```
I picked up a banana. 66%
I picked up a orange.: 18%
I picked up a apple. 8%
I picked up an apple. 4%
I picked up an orange. 4%
```


As you can see, this technique does have some shortcomings. It’s fine with “a apple” but not “an banana” as the former is a relatively common gramatical mistake. And as it generates tokens one at a time, it prefers “a” to “an” in a proportion justified by the general corpus. We could probably fix the latter with a proper beam search which allows a certain amount of lookahead.

## Using prompts

Another advantage is you can use a prompt to guide results.

```
{
"sentence": ["The monster #attacks# you with its #weapon#."],
"attacks": ["slashes","punches", "whips"],
"weapon": ["claws","hands", "tail"]
}
```


Responses with no prompt:

```
The monster slashes you with its hands. 18%
The monster punches you with its hands. 16%
The monster slashes you with its tail. 15%
The monster whips you with its hands. 12%
The monster punches you with its tail. 9%
The monster slashes you with its claws. 9%
The monster punches you with its claws. 9%
The monster whips you with its tail. 9%
The monster whips you with its claws. 4%
```


With prompt `"You are being attacked by a giant rat. "`


```
The monster slashes you with its claws. 33%
The monster whips you with its claws. 18%
The monster punches you with its claws. 12%
The monster whips you with its tail. 12%
The monster slashes you with its tail. 11%
The monster punches you with its tail. 7%
The monster slashes you with its hands. 3%
The monster whips you with its hands. 2%
The monster punches you with its hands. 2%
```


In other words, the model knows that rats have claws and tails, but not hands. I’m surprised it doesn’t seem to realise rats don’t punch things though, or that whipping with claws doesn’t make sense? But gpt2 is quite a stupid model.

I ran these experiments without top-p or top-k filtering, and with temperature 1. So with some tuning, many low probability sentences would be impossible to generate.

## Code

I’ve put the [code on GitHub](https://github.com/BorisTheBrave/tracery-ai), but it’s very simple. A proper implementation would support Tracery’s full feature set 3 and use

[beam search](https://en.wikipedia.org/wiki/Beam_search)so the generation isn’t so order dependent. I might implement if there is sufficient interest, let me know.

- Run with qwen2-0_5b-instruct-q8_0, temperature 1, top-p 95%. I switched to gpt2 for later experiments.
[↩︎](https://www.boristhebrave.com#32eb1daa-ed9d-4121-8523-d888798ad214-link) - It also seems to prefer starting the sentence with “she” rather than “he”, which I can’t account for. Training set bias perhaps.
[↩︎](https://www.boristhebrave.com#a2172d46-8c60-442b-88ca-050083a32393-link) - Tracery grammers are not
[context free](https://en.wikipedia.org/wiki/Context-free_grammar)so are not easily supported by existing frameworks.[↩︎](https://www.boristhebrave.com#0a4be6d2-6948-470b-900a-36b2db1b196b-link)