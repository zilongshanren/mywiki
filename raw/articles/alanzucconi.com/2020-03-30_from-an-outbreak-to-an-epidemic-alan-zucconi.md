---
title: From an Outbreak to an Epidemic - Alan Zucconi
url: https://www.alanzucconi.com/2020/03/30/outbreak-epidemic/
author: Alan Zucconi
published: '2020-03-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This online course introduces the topic of modelling and simulating epidemics. If you are interested in understanding how Mathematicians, Programmers and Data Scientists are studying and fighting the spread of diseases, this series of posts is what you are looking for.

The third, and final part of this course will focus on different strategies that can be used to explore different mechanisms of transmission, and possible interventions.

- Part 1.
[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838) - Part 2.
[Simulating Epidemics](https://www.alanzucconi.com/?p=11840) **Part 3.**[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

This online course is inspired by the recent COVID-19 pandemic. Now more than ever we need skilled and passionate people to focus on the complex subject of Epidemiology. I hope these articles will help some of you to get started.

### Introduction

In the previous part of this online course, [Simulating Epidemics](https://www.alanzucconi.com/?p=11840), we have started coding an epidemic simulator. What makes such a task so important is the fact that simulations are often more flexible than mathematical formulations. It is fairly easy to add or remove features from a simulation. In comparison, it might be very complicated to change a system of differential equations to achieve the same results.

Simulations, however, are often powered by randomness. This means that many, many runs are actually necessary before we can reach any meaningful conclusion.

With that in mind, this article will focus on a few techniques that can be used to simulate different ways in which a disease can spread.

## World Building

The previous article, [Simulating Epidemics](https://www.alanzucconi.com/?p=11840), explained in details how the `Agent`

class was created. Its responsibilities are to move an agent around (in a *random walk* fashion), to spread the disease to sufficiently nearby agents, and to heal when infected.

You can start your simulation simply by putting a bunch of agents in a confined area, as seen in the animation below:

![](../../assets/1f7a359998d47b35.gif)

While the `Agent`

class offers a fairly simple set of functionalities, we can make a big difference by creating a manager class (called `SIR`

, in the snippet below) that instantiates and monitors all the agents.

The easiest thing to get started is to simply turn an agent gameobject into a prefab, and then to instantiate a bunch of them within a confined area:

public class SIR : MonoBehaviour { public Agent AgentPrefab; public List<Agent> Agents; public int AgentCounts; public float Size; void Start() { for (int i = 0; i < AgentCounts; i ++) { Vector2 position = transform.position + new Vector2 ( Random.Range(-Size / 2f, +Size / 2f), Random.Range(-Size / 2f, +Size / 2f) ); Agent agent = Instantiate(AgentPrefab, position, Quaternion.identity, transform); Agents.Add(agent); } } }

We have also ensured that the agents are centred where the SIR gameobject is. This will be important later.

With a little bit more code, one could create a function that also spawns walls around the area. This can be used to create independent simulations within the same scene. Below, you can see a similar simulation in which the infectious range was halved.

![](../../assets/1c1d06ebe5e4367b.gif)

The aim is to end up with a component that can create a simulation box based on a series of parameters. Below, you can see a screenshot from the `SIR`

component available on [Patreon](https://www.patreon.com/posts/35446442), which even includes options to kickstart the infection.![](../../assets/867110665ca65701.png)


### Simulating Communities

One big limitation of the current simulation is that is models in a very unrealistic way how people actually move. One could obviously change the `Agent`

class to improve the accuracy of the simulation, but that is likely to transform the simulator into a cheap clone of Sim City. What we want instead, is to build on top of the existing model, using those simple boxes as the building blocks for more complex simulations.

Commuting plays an important role in modelling how diseases spread, because it gives them the opportunity to travel between different communities. One simple way to simulate this is to start with a number of independent simulation boxes (four, in the animation below). We can simulate commuting by taking random agents from one simulation box and moving them to the centre of another one.

To do that, we first need a script that can “gather” all of the available SIR boxes in the scene. We will call this script `SIRManager`

, and we can use `FindObjectsOfType`

to collect all of the `SIR`

components in the current scene:

public class SIRManager { public SIR[] SIRs; void Start () { SIRs = FindObjectsOfType<SIR>(); } ... }

We now need a method, inside `SIRManager`

, that can take a random agent from a random box and move it inside another one.

void Commute () { // Two random SIR boxes from the list int i = Random.Range(0, SIRs.Count); int j = Random.Range(0, SIRs.Count); SIR SIRi = SIRs[i]; SIR SIRj = SIRs[j]; // A random agent from the i-th SIR box int k = Random.Range(0, SIRi.Count); Agent agent = SIRi.Agents[k]; // Moves the agent from SIRi to SIRj SIRi.Agents.Remove(agent); SIRj.Agents.Add(agent); agent.transform.position = SIRj.tranform.position; }

Once we have that, we just need to invoke it periodically to simulate the commuting of random agents/people to different boxes/cities.

By “teleporting” agents between different simulation boxes we are omitting the actual journey that real people would have to do. But that is not a massive issue: the centre will obviously get pretty crowded pretty quickly: exactly what happens in a station. All agents who have been teleported there, or that happened to be nearby will likely be more exposed to the infection. Once again, exactly what happens in a station.

![](../../assets/7376668068f610ac.gif)

### A Toy Example

This technique can be used very effectively, especially if each box is representative of a particular city where the same train stops every day. We could also go deeper, changing the boxes size and density to match the areas and population densities of their respective cities.

As a toy example, we can imagine constructing a model that simulates how a hypothetical disease could spread through the major cities of Great Britan due to commuting (below, an image from [Trainline](https://www.thetrainline.com/trains/great-britain)).

![](../../assets/faed6deb402e2b7c.png)

In order to model the city correctly, we need to know their approximate size and population. The table below shows the data for size cities (from 2011). The last two columns also indicate which numbers have been used in the SIR simulation.

City | Population | Size | Population (SIR) | Size (SIR) |
|---|---|---|---|---|
Glasgow | ![]() | ![]() | ![]() | ![]() |
Edinburgh | ![]() | ![]() | ![]() | ![]() |
Manchester | ![]() | ![]() | ![]() | ![]() |
London | ![]() | ![]() | ![]() | ![]() |
Cardiff | ![]() | ![]() | ![]() | ![]() |
Brighton | ![]() | ![]() | ![]() | ![]() |

This lead to the following simulation, which shows how an infection that started in London would spread, assuming a daily traffic of 380.000 people.

![](../../assets/9db03a94f0a8ad52.gif)

It is very important to highlight that this simulation, when presented in this way, is nothing more than a toy. In reality, there are many more factors that would play an important role that are not simply not taken into account here.

### Simulating Interventions

The individual simulations might not be very well representative of what is going to happen in the event of a real outbreak. This is because they are often too simplified. However, what can be very insightful is the possibility of simulating interventions, and how they would affect the overall evolution of the pandemic.

For example, either reducing the radii of contagion around the agent (or their probability transmitting the infection) can be an effective way to investigate the impact that better hygiene will have on the pandemic. Washing your hands, in fact, has been proven effective to slow down the contagion.

Another interesting experiment that can be performed is to test how effective self-isolation would be. This can be done by selecting a certain number of agents and setting their speed to zero, effectively stopping them from moving. We can plot the maximum number of people infected, as a function of the percentage of people who are correctly self-isolating. The resulting chart, below, confirms that self-isolation is indeed an effective method to slow down the spread of the disease that we simulated. This was obtained by running a number of simulations for each different proportions of self-isolating people. The coloured area indicates the 97.5 percentile.

The chart above not only tells that self-isolating is effective. It also tells us how much, how many people need to adhere to it to be effective, and also that there is not much difference between 88 and 100%. But it also tells us that self-isolation, alone, is not going to eradicate the disease. That, of course, is only true in the context of the toy simulation that we run: these numbers are unrelated to the current epidemic of COVID-19.

With a similar approach, it is not hard to imagine tweaking a few parameters in order to find the less invasive interventions that could significantly slow down (if not halt) the spread of a disease.

![](../../assets/658691fd84e056ba.gif)

### 📚 Recommended Books

## Conclusion

The third and final article in this online course about epidemics explored how to simulate different mechanisms of transmission and intervention.

You can read the entire series here:

- Part 1.
[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838) - Part 2.
[Simulating Epidemics](https://www.alanzucconi.com/?p=11840) **Part 3.**[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package presented in this tutorial on [Patreon](https://www.patreon.com/posts/35446442). The package contains all the scripts, scenes, prefabs and sprites necessary to recreate the images presented in this online series, including the one below.

![](../../assets/9db03a94f0a8ad52.gif)

All of the revenue from this tutorial will be donated to the [National Emergencies Trust](https://nationalemergenciestrust.org.uk/coronavirus/) (NET), to help those most affected by the recent coronavirus outbreak.

## Leave a Reply Cancel reply