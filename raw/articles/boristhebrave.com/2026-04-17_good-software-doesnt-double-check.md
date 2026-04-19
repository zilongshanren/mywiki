---
title: Good Software Doesn’t Double Check
url: https://www.boristhebrave.com/2026/04/17/good-software-doesnt-double-check/
author: Boris
published: '2026-04-17'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been wrestling with the balance between vibe coding and high touch manual coding these days. At the level of quality I’m trying to output, you cannot delegate everything to agents. But you want to do so as much as possible.

To do this effectively means developing a new set of [coding smells](https://en.wikipedia.org/wiki/Code_smell). The original coding smells were quick tells of typical coding problems. They indicated muddled thinking, structural problems, or technical debt. But the sort of errors agents make are different and need a new set of nasal receptors. That is, for the next few months until a new crop of tools makes current wisdom obsolete again.

One classic tic of agents is overly defensive programming:

```
if 'config' in settings and 'height' in settings['config'] and isinstance(settings['config']['height'], int):
...
```


I think it’s a quirk of the reinforcement learning process that leaves them particularly prone to this sort of behaviour. They get rewarded when the code they emit works, and they don’t get penalized for length or quality. So they quickly learn to shove in as many possible checks and conditions as possible.

Generally speaking, this is bad code – it’s very difficult for humans to read, and frequently these tests do little to improve actual robustness, they just give pretty error messages.

I fight this particular behaviour with increasing amounts of strict static typing. That gives the reader confidence that the program is in a given state already, and additional checks would be redundant.

But this smell is actually indicative of a bigger problem with agents. They can tunnel vision a bit on the current problem, and don’t look at a bigger picture. Particularly if a clueless user just copy pastes error messages without themselves thinking about what they actually want. This leads to all sorts of redundant behaviour:

- Ad hoc type validation
- Wrapping a failing function in a try/catch or retry
[1](https://www.boristhebrave.com#f3f076b0-4b0e-408b-8a19-d917136ec84e) - Checking state for things that are meant to be invariant
- Reparsing strings, vestigal
`case`

statements, catching stuff just to log and rethrow

It can be easy to believe that this is just [defensive coding](https://en.wikipedia.org/wiki/Defensive_programming). It makes the code more robust, code length is not a big deal if only agents are reading it, so whats the harm? Well, all these checks are making the code more brittle. You are adding checks of your assumptions, but not actually ensuring that the assumptions are consistent across the code base. As the code evolves, they’ll get out of sync with each other, leading to failures in random functions in the middle of your stack.

If instead you were careful to establish your assumptions as documented or enforced invariants, then checks are no longer needed, and you’ve got consistent behaviour across all your code.

It’s a bit like the code version of a [TOCTOU](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use) bug: The moment you rely to any given fact more than once, you are opening yourself up to drift between them. Establish things once, and move on.

- This particular one was a pet peeve at a previous job. Each time had their on retry logic, and calls between services could be quite deep. Retries can be
*multiplicative*if naively set up – if you retry service A up to 3 times, and service B retries service C up to 3 times, then you have to experience 9 failures before you give up. We sometimes had to wait an hour before systems would surface that something we didn’t own wasn’t responding.[↩︎](https://www.boristhebrave.com#f3f076b0-4b0e-408b-8a19-d917136ec84e-link)