---
title: Evolutionary Computation - Part 4 - Alan Zucconi
url: https://www.alanzucconi.com/2016/04/27/evolutionary-computation-4/
author: Alan Zucconi
published: '2016-04-27'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Our journey to harness the power of evolution is coming to an end. In the previous three parts of this tutorial we have constructed a bipedal body and a mutable genome that determines its behaviour. What’s left now is to actually implement the evolutionary computation that will find a successful walking strategy.

- Part 1.
[The Evolution Loop](https://www.alanzucconi.com#step1) - Part 2.
[The Simulation](https://www.alanzucconi.com#step2) - Part 3.
[The Fitness Evolution](https://www.alanzucconi.com#step3) - Part 4.
[Improvements](https://www.alanzucconi.com#step4) [Conclusion & Downloads](https://www.alanzucconi.com#downloads)

Evolution is an iterative process. We will use a coroutine to ensure such a loop continues. In a nutshell, we start with a specific genome and make several mutated copies. We instantiate a creature for each copy and test its performance in a simulation. Then, we take the genome of the most performing creature, and iterate again.

public int generations = 100; public float simulationTime = 15f; public IEnumerator Simulation () { for (int i = 0; i < generations; i ++) { CreateCreatures(); StartSimulation(); yield return new WaitForSeconds(simulationTime); StopSimulation(); EvaluateScore(); DestroyCreatures(); yield return new WaitForSeconds(1); } }

To test how well a creature can actually walk, we need to create its body and to give it enough time to move. To simply things, let’s imagine that we have a sufficiently long floor in the game scene. We will instantiate creatures on top of it, at a sufficient distance from each other to avoid interferences. The code below does exactly this, spacing each creature (stored in `prefab`

) by `distance`

.

public int variations = 100; private Genome bestGenome; public Vector3 distance = new Vector3(50, 0, 0); public GameObject prefab; private List<Creature> creatures = new List<Creature>(); public void CreateCreatures () { for (int i = 0; i < variations; i ++) { // Mutate the genome Genome genome = bestGenome.Clone().Mutate(); // Instantiate the creature Vector3 position = Vector3.zero + distance * i; Creature creature = Instantiate<Creature>(prefab, position, Quaternion.identity); creature.genome = genome; creatures.Add(creature); } }

The function `CreateCreatures`

keeps track of all the creatures that have been created, so that they can be easily manipulated. For a better control, we disable in the creature prefab the script `Creature`

. This prevents the creature from moving. We can then start and stop the simulation with the following functions.

public void StartSimulation () { foreach (Creature creature in creatures) creature.enabled = true; } public void StopSimulation () { foreach (Creature creature in creatures) creature.enabled = false; } public void DestroyCreatures () { foreach (Creature creature in creatures) Destroy(creature.gameObject); creatures.Clear(); }

Evolution is all about fitness evaluation. Once the simulation is over, we loop over all the creatures and get their final score. We keep track of the best one, so that we can mutate it in the next iteration.

private float bestScore = 0; public void EvaluateScore () { foreach (Creature creature in creatures) { float score = creature.GetScore(); if (score > bestScore) { bestScore = score; bestGenome = creature.genome.Clone(); } } }

A careful reader might have noticed that the technique described in this tutorial relied on few parameters. Namely: `generations`

, `simulationTime`

and `variations`

. They represents, respectively, the number of generation to simulates, the duration of each simulation and the number of variations to generate ad each generation. A more careful reader, however, should have noticed that the strategy adopted is poisoned with hidden assumptions. They are the result of oversimplified design choices that have been made, and that are now becoming hard constraints. They will make the difference between a program that runs in one hour, and one that runs in one month. This section will try to address some of these constraints, providing more sensible alternatives that you can implement on your own.

**Top K genomes.**The genome that starts the next generation is the best one, across all the generations. This means that if the current generation is unable to improve the fitness, the next generation will start with the same genome. The obvious catch is that we might end up stuck in a loop where the same genome is simulated again and again, without any sensible improvement. A possible solution is to always take the best genome in the current run. The drawback of this choice is that the fitness can go down, if no mutation appear to bring an improvement. A more sensible approach is to take the best top`k`

genomes from each generation, and use all of them as seeds for the next iteration. You can add in the unmutated best genome from the previous generation to ensure the fitness won’t go down, yet allowing space for better solutions to be found.**Adaptive learning rate.**Every time we mutate a genome, we only alter a single parameter of a leg, and by a fixed amount. Mutations are what move us around the parameter space in which our solution lies. The speed at which we move is very important: if we move too much when we’re close we overshoot the target, but if we move too slow we might not overcome local maxima. The number of mutations performed (*learning rate*) on a genome should be related to the speed at which we are improving our score. The following animation shows how the dramatic effect that different strategies have in the convergence speed.

![contours_evaluation_optimizers](../../assets/1fd419fc16423b90.gif)

**Early termination.**It’s easy to see that some simulations will bring us to a dead end. Every time the creature flips on its back, there is no way to get back on its feet. A good algorithm should detect this and interrupt their simulations to save resources.**Changing fitness function.**If what you are trying to learn is rather complex, it might be worth it do to it in stages. This can be done by progressively changing the fitness function. This helps to focus the learning effort on a single task at a time.**Multiple tests.**When it comes to simulate physics, chances are you’ll never get the same result twice. It is a good technique to instantiate multiple creatures with the same genome, in the same conditions, and averaging their performance to find a more reliable score.

This tutorial has introduced and explained how evolutionary computation works. This topic is incredibly vast, so please take this as a general introduction.

**You can download the complete Unity package for this project here. If you think this tutorial has helped you, please consider supporting me on Patreon.**

#### Other resource

- Part 1.
[Evolutionary Computation: Theory](https://www.alanzucconi.com/?p=4730) - Part 2.
[Evolutionary Computation: Phenotype](https://www.alanzucconi.com/?p=4774) - Part 3.
[Evolutionary Computation: Genotype](https://www.alanzucconi.com/?p=4736) - Part 4.
**Evolutionary Computation: Loop** [Optimizing Gradient Descent](http://sebastianruder.com/optimizing-gradient-descent/)

## Leave a Reply Cancel reply