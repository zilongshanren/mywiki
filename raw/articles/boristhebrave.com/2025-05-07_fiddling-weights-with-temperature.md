---
title: Fiddling Weights with Temperature
url: https://www.boristhebrave.com/2025/05/07/fiddling-weights-with-temperature/
author: Boris
published: '2025-05-07'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

In procedural generation, the absolute simplest, most common technique is randomly picking an item from a list. More often than not, it is a **weighted random choice**, where each item is selected with a frequency proportional to its “weight”, a numerical value that can be tweaked by the designer.

```
def random_choice(items: list, weights: list[float]):
total_weight = sum(weights)
random_value = random.random() * total_weight
# Find the item that corresponds to the random number
for i, weight in enumerate(weights):
random_value -= weight
if random_value <= 0:
return items[i]
```


I wanted to share a technique from the Machine Learning community that is simple enhancement to this routine that gives a lot of convenience over tweaking weights directly, called **temperature**.

The idea of temperature is its an additional setting the designer can tweak to influence the random selection.

- A temperature of
**one**means: choose items according to their normal weight distribution. - A temperature of
**less than one**means: disproportionally tend to prefer items with higher weights- At the extreme, a temperature of
**zero**means: only pick the item with max weight

- At the extreme, a temperature of
- A temperature of
**more than one**means: disproportionately tend to prefer items with lower weights- At the extreme, a temperature of
**infinity**means: pick items completely uniformly.

- At the extreme, a temperature of

Here’s a little demo of how temperature works:

## The Code

Mathematically, temperature is extremely simple to express. It’s just a change you apply to each weight:

`new_weight = pow(weight, 1/temperature)`


Doing this naively can sometimes cause floating point issues, so here is a more numerically robust function for the same thing:

```
def reweight(weights: list[float], temperature: float) -> list[float]:
if temperature == 0:
# At temperature 0, only the maximum weight is ever selected
max_weight = max(weights)
return [1.0 if w == max_weight else 0.0 for w in weights]
max_weight = max(weights)
# Handle infinities in input
if math.isinf(max_weight):
return [1.0 if math.isinf(w) and w > 0 else 0.0 for w in weights]
# Rescale weights (for numerical stability)
weights = [w / max_weight for w in weights]
# Convert to logits and apply temperature
logits = [math.log(w) for w in weights]
scaled_logits = [l / temperature for l in logits]
# Handle overflow
if any(math.isinf(sl) for sl in scaled_logits):
return [1.0 if math.isinf(sl) else 0.0 for sl in scaled_logits]
# Convert back to weights
max_logit = max(scaled_logits)
exp_logits = [math.exp(l - max_logit) for l in scaled_logits]
# We don't need to divide by the sum here as that will be done in randomChoice,
# but I leave it in for clarity.
sum_exp = sum(exp_logits)
return [exp / sum_exp for exp in exp_logits]
```


## Why Is This Useful?

Weights (or probabilities or frequencies) are a really easy way to set up a random distribution how you like. But you have to set the weight for every item individually.

This makes it really difficult to do bulk changes. Temperature essentially gives you a single slider that lets you play with the variance of the entire set.

Say you want a luck stat in your game, that makes rare items more common. Just increase the temperature!

Or you want that the first level in your roguelike to be a gentle introduction. Lower temperature means that the most common items from your set will be used a lot, allowing players to master them before seeing too much weirdness.

You could make randomly generated NPCs more salient by giving more plot critical ones a higher temperature. Not only will they feature rare traits, but they’ll be much more likely to have multiple rare traits together.

So temperature can be seen as **luck** or **high variance** or **creativity**. These are useful concepts to have global control over.

In fact, temperature can be applied to other probability distributions too, and it usually has a similar effect to increasing variance.

Very interesting, i knew it, but i don’t recognize it.