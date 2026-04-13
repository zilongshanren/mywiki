---
title: Evolutionary Computation - Part 2 - Alan Zucconi
url: https://www.alanzucconi.com/2016/04/13/evolutionary-computation-2/
author: Alan Zucconi
published: '2016-04-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In the first part of this tutorial we have explored what evolutionary computation is, and why it works. The rest of this tutorial will show how to set up a practical example and how to use evolution to solve a real problem. In our case, the problem is teaching a bipedal creature how to keep balance and how to walk effectively. Rather than evolving the body of the creature, we are interested in finding a strategy to make it walk as fast as possible.

- Part 1.
[The Body](https://www.alanzucconi.com#part1) - Part 2.
[The Brain](https://www.alanzucconi.com#part2) - Part 3.
[The Controller](https://www.alanzucconi.com#part3) - Part 4.
[The Fitness Score](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

![walker_8](../../assets/9b20342215f88a60.gif)

The first step is to design the creature we will use. It is important to remember that evolution is a rather slow process. Starting with a human-like ragdoll might take way too long to reach a consistent and effective walking strategy. If we want to test out evolutionary software, we need to start with something easier.

![evolution](../../assets/47f47582ec68a85a.png)

The subject of our experiment is that very simple bipedal creature. It has two legs, L and R, which are hinged onto its body. They are able to rotate, thanks to two springs. When the springs extends and contracts, they pull and push the legs, causing them to rotate. The creature has no direct knowledge on how to rotate its legs, but it controls the length of the springs feeding them a value between ![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)


**Note:** Moving complex bodies is a challenging task. For the final project, I have replaced Unity’s `SpringJoint2D`

with `DistanceJoint2D`

, since they are more predictable. I will keep calling them springs, nonetheless. For the more complex ragdoll shown in the animation, limbs will be rotated directly by code.

Walking is not just a matter of finding the right angles for L and R. Is a continuous task that requires equally continuous movements of the legs. If we want to walk, we need a way to provide the creature with a compact and meaningful way to move its legs. The list of choices here is endless. For the sake of simplicity, the relaxation and contraction of the springs is controlled by two sinusoidal waves.

![walker_4](../../assets/c2c99a7e8c3fdda3.gif)

The evolutionary process is going to fit the L and R sinusoids that make our creature walk. You can see an example in the animation on the side; the green and red sinusoid controls the L and R legs, respectively.

The springs are the entities that the creature controls, and will be the target of our evolutionary computation. Each sinusoid has period ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com m](../../assets/ae1726b8a02e3872.png)

![Rendered by QuickLaTeX.com M](../../assets/17b6ead89daa2266.png)

![Rendered by QuickLaTeX.com o](../../assets/145b04bf6101cdc0.png)


In our current setup, we already have several entities: the legs, the springs and the waves. To simplify the way we approach the problem, let’s create a class `LegController`

that allows to control the contraction of the spring with a value from ![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)


![Copy of Untitled drawing (1)](../../assets/983214c97dc29b33.png)

We perform the rotation of the leg by changing the distance of the spring in `FixedUpdate`

. This forces the joint to pull or push the leg until it reaches the desired destination.

public class LegController : MonoBehaviour { public DistanceJoint2D spring; private float contracted; private float relaxed; [Range(-1, +1)] public float position = +1; void Start () { float distance = spring.distance; relaxed = distance * 1.5f; contracted = distance / 2f; } void FixedUpdate () { spring.distance = linearInterpolation(-1, +1, contracted, relaxed, position); } public static float linearInterpolation(float x0, float x1, float y0, float y1, float x) { float d = x1 - x0; if (d == 0) return (y0 + y1) / 2; return y0 + (x - x0) * (y1 - y0) / d; } }

The two leg controllers are constantly updated by the `Creature`

class:

public class Creature { public LegController left; public LegController right; public void Update () { left.position = // ... right.position = // ... } }

We will see in the next part of this tutorial how the `Creature`

class evolves to incorporate also the genome of the creature.

Evolution requires to evaluate the fitness of a creature. This step, which sounds trivial, is actually incredibly challenging. The reason is that the score we assign to each creature at the end of the simulation has to correctly capture what we want to learn. Failure to do so will inevitable yield poor results, keeping evolution stuck in local maxima.

My first attempt has been to evaluate the fitness of a creature depending on how far it travelled from its initial position:

private Vector3 initialPosition; public void Start () { initialPosition = transform.position; } public float GetScore () { return position.x - initialPosition.x; }

This converges to the walking strategy that requires less effort: dragging yourself on the floor:

![walker_1](../../assets/6b628299330e712f.gif)

I was rather unhappy with that solution, because it failed to capture one of the most important aspect of walking: keeping balance. As a second attempt, I gave a very strong bonus to all the creatures who managed to stay up on their feet:

public float GetScore () { // Walking score float walkingScore = position.x - initialPosition.x; // Balancing score bool headUp = head.transform.eulerAngles.z < 0+30 || head.transform.eulerAngles.z > 360-30; bool headDown = head.transform.eulerAngles.z < 180-45 && head.transform.eulerAngles.z > 180+45; return walkingScore * (headUp ? 2f : 1f) // Double score if UP * (headDown ? 0.5f : 1f) // Half score if DOWN ; }

Since falling is incredibly easy, that fitness function promoted creatures which are able to keep a good balance. However, it doesn’t really encourage them to walk. Failing is judged too severely, and evolution doesn’t feel brave enough to risk it.

![walker_2](../../assets/6b0e45cf2d802cef.gif)

To compensate for this, I tried to give an incentive for staying balanced that was independent of the walking score.

return walkingScore * (headDown ? 0.5f : 1f) + (headUp ? 2f : 0f) ;

In all my attempts, creatures converged towards a sloppy, yet very functional solution:

![walker_3](../../assets/cb51c13bd9606943.gif)

This post introduces the body of the creature we are going to use for our simulation. As long as you’re sensible with your design choices, evolution will work regardless of the body type. It’s worth noticing that my first attempt used a much more sophisticated body, which used four interconnected springs. That did not work very well, since evolution exploited Box2D’s constraint instabilities to make the creature fly at high speed. Yes, evolution likes to cheat. A lot.

**The third part of this tutorial will focus on how to correctly represent and mutate the genome of our creature. Using a form that is amenable to evolutionary computations is at the heart of this technique.**

#### Other resources

- Part 1.
[Evolutionary Computation: Theory](https://www.alanzucconi.com/?p=4730) - Part 2.
**Evolutionary Computation: Phenotype** - Part 3.
[Evolutionary Computation: Genotype](https://www.alanzucconi.com/?p=4736) - Part 4.
[Evolutionary Computation: Loop](https://www.alanzucconi.com/?p=4765)

## Leave a Reply Cancel reply