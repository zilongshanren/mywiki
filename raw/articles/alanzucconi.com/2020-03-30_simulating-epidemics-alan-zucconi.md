---
title: Simulating Epidemics - Alan Zucconi
url: https://www.alanzucconi.com/2020/03/30/simulating-epidemics/
author: Alan Zucconi
published: '2020-03-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the online course dedicated to the modelling and simulating of epidemics. If you are interested in understanding how Mathematicians, Programmers and Data Scientists are studying and fighting the spread of diseases, this series of posts is what you are looking for.

In the second part, we will focus on ways to simulate epidemics. While the code here presented is in C# and runs in Unity, the knowledge can be applied to virtually any other language or engine.

You can read the rest of this online course here:

- Part 1.
[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838) **Part 2.**[Simulating Epidemics](https://www.alanzucconi.com/?p=11840)- Part 3.
[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

This online course is inspired by the recent COVID-19 pandemic. Now more than ever we need skilled and passionate people to focus on the complex subject of Epidemiology. I hope these articles will help some of you to get started.

And if you are interested in learning more about the virus responsible for the COVID-19 epidemics, SARS-CoV-2, have a look at the semi-serious video down below.

## Introduction

In the previous part of this online course, [The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838), we have explored a number of different mathematical models used to predict the evolution of an epidemic. From the simple **exponential** and **logistic growth curves**, to the **SIR model**, all of those techniques heavily relied on the ability to derive some sort of mathematical expressions. Both exponential and logistic curves were initially derived from recurring expressions (later converted into a closer-form). However, even a simple model such as SIR requires the use of ordinary differential equations (ODEs).

While ODEs are an exceptionally powerful tool, they can often be solved only through numerical methods (such as the Runge-Kutta method). Understanding, deriving and solving ODEs also requires a mathematical knowledge that only a few people who attended Higher Education have. In a nutshell, ODEs are powerful, but they remain an advanced tool beyond the knowledge and understanding of most of us.

Due to this, understanding the results of a model that has deep mathematical roots can be challenging. Consequently, it is very hard to explain the results of those models to the general audience. A significant part of the population is unable to correctly interpret graphs and charts, so even when the results are presented in a graphical format, that can still be ineffective. Social media has significantly reduced our attention span, so if you need to get a message across as many people as possible, it needs to be *simple and immediate*, to be effective. Grant Sanderson, the Science Communicator behind the YouTube channel [3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw), recently published a video showing how easy it is to simulate epidemics. The animations he presented are indeed *simple and immediate*. They can reach a large number of people, and it is safe to say if they managed to change the behaviour of some of the people watching it, they saved lives.

Another important factor that prevents the use of ODEs is that the models than can be constructed with them relies on heavy assumptions. For instance, the SIR model assumes a *homogeneous* population. What happens if we want to model a more complex distribution of age, wealth and medical conditions? What happens if we want to model the transport system that allows people to move from a point to another of a city? Including all of these factors into a mathematical model can be challenging and ineffective.

It is safe to say that the number of people who know how to code is greater than the number of people who know how to solve ODEs. What is interesting about directly simulating an epidemics, is that it allows many more people to understand the mechanism through which diseases spread. And, even more importantly, it has the potential to allow many more people to easily tweak their simulations to try a variety of different “solutions”. How is self-isolation impacting the spread of a disease? What percentage of people need to self-isolate for this solution to work? What is the impact of a vaccine? And if that is a finite resource, who should get it first to have the most impact? Modelling this with ODEs would be rather tricky; coding them in a simulation only requires a few lines of code.

This is why a lot of problems, when they become too complex, needs to be modelled and solved through direct simulations. This means to recreate a virtual model of the phenomenon under investigation, reproducing the dynamics that lead to the spread of a specific disease. In this article, we will see some of the most common techniques used to simulate epidemics, and what we can learn from them.

## Simulating Epidemics

If we want to start creating a simulation, we can still re-use a lot of the knowledge gained from [The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838). In particular, the SIR model is a good starting point. To recap, the SIR model imagines a population divided into three groups (sometimes called *compartments*): **susceptible**, **infected** and **recovered**. The progression from susceptible to infected to recovered can be seen in the diagram below:

(1) ![Rendered by QuickLaTeX.com \begin{equation*}\mathcal{S} \rightarrow \mathcal{I} \rightarrow \mathcal{R}\end{equation*}](../../assets/1b5b243c20423149.png)


It is relatively easy to simulate the evolution of a SIR model in a game engine like Unity:

- Create a virtual 2D box
- Create a number of agents placed inside the box
- Each agent moves continuously and randomly
- Agents can be in one of the SIR states
- Every infected agent has a fixed probability of infecting the nearby susceptible agents
- Infected agents will eventually recover after a fixed amount of time

The rules above are all we need to create a solid simulation that will give meaningful results.

![](../../assets/1f7a359998d47b35.gif)

The rest of this post will show you how to create such a simulation in Unity. The tutorial will go through the most important aspects, although on [Patreon](https://www.patreon.com/posts/35446442) you can find a much more advanced version which supports a variety of different settings (below). That package also includes a live plot that runs directly in the inspector, and that you can potentially re-use for other applications.

![](../../assets/867110665ca65701.png)

## Agents

The heart of the simulator lies in its most simple, yet important component: the agents that it contains. This is why it makes sense to start implementing by creating a new `Agent`

script. At each time step, the agent needs to perform a series of operations: moving, spreading the infection to others and healing (when infected).

We can use a top-down approach to write these features in functions that we will create later.

public class Agent : MonoBehaviour { ... void Update () { Move(); Spread(); Heal(); } ... }

Another important aspect is the state of the agent. Since we are following the SIR model, we will need a variable that can tell if an agent is susceptible, infected or has recovered from the disease simulated. States like this can be implemented using an enum type and variable:

public enum InfectionState { Susceptible, Infected, Removed } public InfectionState State = InfectionState.Susceptible;

## Healing

The simpler method to implement, among the ones presented in the previous section, is `Heal`

. Every agent will recover after a fixed amount of time. We can use a variable called `InfectionTimer`

to store how many seconds the agent will be infected for. In `Heal`

, we can simply decrease it by `Time.deltaTime`

so that for each in-game second, the variable decreases by one. Finally, if the timer has reached zero, we can change the state of the agent back to susceptible.

private float InfectionTimer; void Heal() { if (State != InfectionState.Infected) return; InfectionTimer -= Time.deltaTime; if (InfectionTimer <= 0) State = InfectionState.Susceptible; }

## Random Walk

One feature of the simulator is that is moves agents randomly. This simulates the daily interactions that people go through every day, from commuting to work to meeting with friends.

There are many ways to implement a **random walk**, some more sophisticated than others. The one presented here is rather simple, yet effective. Agents move with a constant speed, in a specific direction; these can be stored in two variables that we will call `Speed`

and `Direction`

.

We can theoretically move the agent by updating its `transform.position`

. If we do that, unfortunately, we will not be able to rely on Unity’s collision system. If collisions (with the walls or even between the agents themselves) are important, then the best way to move forward is to add a Rigidibody 2D component. Then, we can move each agents using the `MovePosition`

of the `Rigidbody2D`

class. This allows us to move the object to any arbitrary position, while still respecting the physical constraints imposed by the collisions system. The `MovePosition`

method, in fact, will not cause an object to move through a collider.

public Rigidbody2D Rigidbody; public float Speed; // m/s private Vector2 Direction; // random direction void Move() { Rigidbody.MovePosition(Rigidbody.position + Direction * Speed * Time.deltaTime); }

What is now needed, is a system that periodically updates the direction an agent is moving along. There are many ways to do that; I have chosen to use a coroutine that is constantly looping and that refreshes the `Direction`

variable every second.

IEnumerator Start() { // Random starting offset yield return new WaitForSeconds(Random.Range(0f, 2f)); // Changes the direction every three seconds while (true) { Direction = Random.insideUnitCircle.normalized; yield return new WaitForSeconds(1f); } }

If you are using this approach, all agents will suddenly change direction at the same time, leading to a rather uncanny behaviour. To avoid this, I wait a random amount of time before starting the loop, so that while each agent still suddenly changes its speed every second, they are all doing it at a different time.

You might also have noticed that I have defined the `Start`

function as an `IEnumerator`

. This makes it into a coroutine. It is a nice little feature that Unity has, which also works for a variety of other methods such as the ones belonging to the `OnCollision-`

and `OnTrigger-`

families.

## Spread the Infection

The final part that needs to be done to complete the `Agent`

class, is the `Spread`

function. What this function need to do, is to find the nearby agents and infect them, based on a certain probability.

To make this function easier, let’s create another one first: `NearbyAgents`

. What this function does is simply returning all agents that are in a specific radius from the position of the current agent. This can be done using a family of static methods in the `Physics2D`

class, called `Overlap-`

. One in particular, `OverlapCircleAll`

, returns all of the colliders inside a specific circle; exactly what we need! However, it is rather inefficient as it causes the allocation of a new array of colliders (`Collider2D[]`

) every time it is invoked. Because we are planning on invoking this function every frame, for dozens if not hundreds of objects; `OverlapCircleAll`

is not the most efficient option. Another variants, `OverlapCircleNonAlloc`

, works in the exact same way, but causes no memory allocation. It works by re-using an array that we can initialise only once.

The `NearbyAgent`

method, looks like this:

public LayerMask AgentMask; public float InfectionRadius; // metres public IEnumerable<Agent> NearbyAgents () { int n = Physics2D.OverlapCircleNonAlloc(transform.position, InfectionRadius, Colliders, AgentMask); return Colliders .Take(n) .Select(collider => collider.GetComponent<Agent>()); } private Collider2D[] Colliders = new Collider2D[10];

To makes sure that we can only collect colliders belonging to agents (and not, let’s say, the ones on a wall) we can use a layer mask. As long as only the gameobjects of the agents are on that layer, this will work.

Now that we have a way of retrieving a list of the nearby agents, we can start creating the `Spread`

function. This has to take the list, and select only the agents which are susceptible. In my example, I have done this using the LINQ extension `Where`

. No all of the remaining agents will be infected, as the chance of transmitting the infection is modulated by a probability. We can use `Where`

once again, to randomly selected only a few agents:

[Range(0,1)] public float InfectionProbability; void Spread() { if (State != InfectionState.Infected) return; var agents = NearbyAgents() .Where(agent => agent.State == InfectionState.Susceptible) .Where(_ => Random.Range(0f,1f) <= InfectionProbability); foreach (Agent agent in agents) agent.Infect(); }

Finally, we loop through them and infect them. This can be done using another method which simply changes the state and the infection timer:

public float InfectionDuration = 1f; // Seconds void Infect () { if (State != InfectionState.Susceptible) return false; State = InfectionState.Infected; InfectionTimer = InfectionDuration; }

### Probability

There is one aspect of the `Spread`

function that was seriously overlooked. The variable `InfectionProbability`

is used to determine the probability that a given interaction transmits the disease. Now let’s imagine that chance is very low, for instance: ![Rendered by QuickLaTeX.com 1%](../../assets/1ed5a0be291f07c2.png)

`Spread`

method is likely to be called 60 times per second, meaning that `InfectionProbability`

represents the probability of being infected in a frame.

If you are a game developer, you probably understand why this is problematic. What happens if the game runs at 30 frames per second instead? This would not only slow down the simulation, but it would completely change the parameters of the disease. This problem is known as **frame-rate dependency**.

When it comes to moving object, we can simply multiply a velocity by `Time.deltaTime`

to convert something from *per frame* to *per second*:

float Speed = 1; // Moves 1 metre per frame Rigidbody.MovePosition(Rigidbody.position + Direction * Speed); // Moves 1 metre per second Rigidbody.MovePosition(Rigidbody.position + Direction * Speed * Time.deltaTime);

One could imagine multiplying the probability by Time.deltaTime, in order to achieve the same effect (which is, changing the probability from *per frame* to *per second*). Unfortunately, things are a bit more complicated here.

This is a problem that recurs very often in Statistics. If we know the probability of being infected over a month (![Rendered by QuickLaTeX.com P_M](../../assets/8cd9438ead226036.png)

![Rendered by QuickLaTeX.com P_Y](../../assets/2b398a2376b24a83.png)

![Rendered by QuickLaTeX.com P_M=0.2](../../assets/462c51626bea4d0f.png)

![Rendered by QuickLaTeX.com 2.4](../../assets/98a1d224957c5bac.png)


Since this is such a critical part of the simulator, it is important to get the Maths right. What `InfectionProbability`

represents is the “probability of infecting an agent *per frame*” (let’s call it ![Rendered by QuickLaTeX.com P_F](../../assets/1515d0a1cfe31647.png)

*per second*” (let’s call it ![Rendered by QuickLaTeX.com P_S](../../assets/1327fa5c0d3d437e.png)


Let’s see how we can get there:

- The probability of not getting infected in a frame is

(the opposite of

). - The probability of not getting infected for two frames is

. - The probability of not getting infected for an entire second is

(where

is the number of frames in a second). - The probability of getting infected in a second (

) is the opposite of

, which is ![Rendered by QuickLaTeX.com 1-\left(1-P_F\right)^{FPS}](../../assets/bd9983d448dbadf7.png)


What we have now is an expression for ![Rendered by QuickLaTeX.com P_S](../../assets/1327fa5c0d3d437e.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*}P_S &= 1-\left(1-P_F\right)^{FPS}\end{equation*}](../../assets/2dd8e0af215b7518.png)


which we can use to extract ![Rendered by QuickLaTeX.com P_F](../../assets/1515d0a1cfe31647.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}P_S &= 1-\left(1-P_F\right)^{FPS} \\1-P_S&=\phantom{1-} \left(1-P_F\right)^{FPS}\\\sqrt[{FPS}]{1-P_S}&=\phantom{1-}1-P_F\\1-\sqrt[{FPS}]{1-P_S}&=\phantom{1-1-}P_F\end{align}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-32121ac37e2937026f43a799893335e1_l3.png)


Now we can use this expression to calculate the probability that we need to apply each frame, knowing the probability of being infected over an entire second.

Unfortunately, Unity does not have a function to calculate the ![Rendered by QuickLaTeX.com FPS](../../assets/291c5ec2be365715.png)

`Mathf.Pow`

instead since:

(4) ![Rendered by QuickLaTeX.com \begin{equation*}\sqrt[n]{x}=x^{\frac{1}{n}}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-95ca68636eb9edf4bd2b73cbe3aa53fa_l3.png)


Also:

(5) ![Rendered by QuickLaTeX.com \begin{equation*}\sqrt[{FPS}]{x}=x^{\frac{1}{FPS}}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-be04f40a1dced426f0abe5588d391470_l3.png)


(6) ![Rendered by QuickLaTeX.com \begin{equation*}\Delta t = \frac{1}{FPS}\end{equation*}](../../assets/e7a0545dae538116.png)


(7) ![Rendered by QuickLaTeX.com \begin{equation*}\sqrt[{FPS}]{x}=x^{\Delta t}\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5151323e7370cefd3c4bd9595e38200d_l3.png)


which means that the final code is:

float pf = 1f - Mathf.Pow(1f - InfectionProbability, Time.deltaTime); var agents = NearbyAgents() .Where(agent => agent.State == InfectionState.Susceptible) .Where(_ => Random.Range(0f,1f) <= pf);

## Evaluation

Simulations like this are obviously heavy simplifications of the world we live in. The fact that simulations like this reduce people to *randomly walking agents*, however, is not a big issue. They can still produce meaningful results and give a good insight into how diseases spread and, consequently, how they can be best fought.

![](../../assets/d4cc3aabc59c492a.gif)

However, it would be premature to make any kind of inference onto the real world, without any kind of validation of their predictive effectiveness. It is hard to tweak all of the parameters right. How fast should agents move? How far can they walk? What is the range of infection? Tweaking all of these parameters will lead to wildly different results.

Another big problem of simulations like this is that they are inherently probabilistic. ODEs will always lead to the same result, and their evolution is fully defined by their initial conditions. Simulations introduce randomness, in the form of uncertainty and probability. You can run the same simulation 100 times, and receive wildly different results each time. As long as your setup is working correctly, you will need to test a scenario thousands, if not millions of times, in order to get a realistic distribution of how likely each possible outcome is. Statistically speaking, a single simulation is worth little more than nothing.

Statistically speaking, a single simulation is worth little more than nothing.


### 📚 Recommended Books

## What’s Next…

The second article in this online course about epidemics explored how to implement an epidemic simulation, starting from its building blocks: the agents.

The next article, [From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842), will expand on that and show how to use the agent class to explore different mechanisms of transmissions and intervention.

- Part 1.
[The Mathematics of Epidemics](https://www.alanzucconi.com/?p=11838) **Part 2.**[Simulating Epidemics](https://www.alanzucconi.com/?p=11840)- Part 3.
[From an Outbreak to an Epidemic](https://www.alanzucconi.com/?p=11842)

### Additional Resources

### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package presented in this tutorial on [Patreon](https://www.patreon.com/posts/35446442). The package contains all the scripts, scenes, prefabs and sprites necessary to recreate the images presented in this online series, including the one below.

![](../../assets/9db03a94f0a8ad52.gif)

All of the revenue from this tutorial will be donated to the [National Emergencies Trust](https://nationalemergenciestrust.org.uk/coronavirus/) (NET), to help those most affected by the recent coronavirus outbreak.

## Leave a Reply Cancel reply