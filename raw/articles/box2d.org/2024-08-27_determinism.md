---
title: Determinism
url: https://box2d.org/posts/2024/08/determinism/
published: '2024-08-27'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Determinism means many things when it comes to game development and especially physics engines. Generally in game development we like things to be repeatable. This makes debugging easier. This doesn’t rule out emergent behavior though because player input can be viewed as random.

## Testing Determinism

Determinism is a brittle feature. It is easy to break. Code changes can break it. Compiler versions can break it. So it needs to be tested using [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration), or **CI** for short.

Box2D uses [GitHub Actions](https://docs.github.com/en/actions) to run unit tests on every pull request. As part of these unit tests I run a determinism test I call *Falling Hinges*. This scenario is designed to test all the features I suspect will affect determinism:

- MSVC, Clang, GCC, x64, ARM
- fast movement and collision
- sleeping
- joint limits
- initial rotation

As part of this test I generate two numbers that must match after every run:

- the number of time steps it takes for all the bodies to go to sleep
- a hash of the transforms of all the bodies once they are all sleeping

From the video the sleep step is 310 and the transform hash is 0x5e70e5fe. These numbers may change as I make changes to Box2D, but I will see the CI failure and I can update the target numbers, ensuring they are deterministic.

Now lets go over the various flavors of determinism and see where Box2D sits.

## Algorithmic Determinism

First of all there is [algorithmic determinism](https://en.wikipedia.org/wiki/Deterministic_algorithm). This basically means there are no random numbers. This is easy enough: I simply don’t use random numbers in Box2D. I use random numbers in the samples application but not in the Box2D library.

With this sort of determinism I can guarantee that Box2D will produce the same result on the same computer from run to run. This usually requires the world to be recreated because destroying all the bodies and adding new bodies may result in the second wave of bodies having a different order. This is because Box2D maintains object pools with [free lists](https://en.wikipedia.org/wiki/Free_list).

Box2D v2.4 and before achieved algorithmic determinism with almost no effort. However, in version 3 this became much more challenging due to multithreading.

## Multithreaded Determinism

Multithreaded computation can introduce a hidden random number generator, which is the relative speed of each CPU core. Modern CPUs run at variable speeds and each core can run at a different speed. This means from run to run each core can run at a different speed. The operating system schedular is also unpredictable.

Any kind of cross-thread synchronization can lead to non-deterministic results. For example, multiple threads can look for new contact pairs in the broad-phase. Each thread can create new contacts and add them to the world array of contacts. The order of different threads adding their results to the contact array depends on how fast each thread does its work. This can depend on the CPU core boost speed, which Box2D has no control over.

So now the contact array has a somewhat random order of contacts. The Box2D solver produces different results if the contact array has a different order. So now the simulation is non-deterministic!

This random order is not helped by using atomics or mutexes. In fact, the presence of an atomic or mutex in a program indicates a risk to determinism. For example, if a thread is adding an element to a global array, this requires an atomic increment:

```
// In some worker thread ...
= CreateContact();
// This index will progress randomly among different threads and will be
// different from run to run.
// The atomic increment does not prevent randomness, it just prevents
// a data race where two contacts could be written to the same slot.
// See https://en.wikipedia.org/wiki/Race_condition
int index = atomic_fetch_add(&world->contactCount, 1) + 1;
world->contactArray[index] = contact;
```


In Box2D version 3 I had to be vigilant to maintain determinism under multithreading. The order that bodies and shapes are created in the world should determine the order of contacts. However, I wanted to avoid any expensive sorting. Generally I used bit arrays to maintain order. The basic idea is that each worker thread has a local bit array that it fills out. Then when the worker threads are done, these bit arrays are merged with a bit-wise `OR`

operation on the main thread. This global bit array then has a deterministic sequence of set bits.

I wrote more about using bit arrays in my post [Simulation Islands](https://box2d.org/posts/2023/10/simulation-islands/).

The following video shows the Falling Hinges sample being run with various thread counts and confirms that Box2D has multithreaded determinism.

## Cross-Platform Determinism

Cross-platform determinism requires that the same world produces the same results on different CPUs and compilers. I test Box2D on x64 and ARM CPUs. I also test on MSVC, GCC, and Clang compilers.

Conventional wisdom is that cross-platform determinism requires [fixed-point math](https://en.wikipedia.org/wiki/Fixed-point_arithmetic). This used to be true in the 32-bit era, especially when math was done on scalar [FPUs](https://en.wikipedia.org/wiki/Floating-point_unit). FPUs such as the x87 would do math internally at a higher precision. This makes basic arithmetic give different rounding results than would be generated on other platforms. This was the *floating point dark ages*.

Once [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) and 64-bit computing emerged it seems that CPU makers stopped playing games with math and started providing identical rounding for basic arithmetic. However, there are three remaining traps that I encountered.

### Fast-Math

Some compilers offer a *fast-math* setting. This will jumble your arithmetic in pursuit of higher performance. In my testing on MSVC, this setting provides no significant performance benefit. Besides breaking determinism, fast-math noticeably [reduced accuracy](https://mastodon.gamedev.place/@erin_catto/110778282667162942). Fortunately fast-math is not the default on any compiler I’ve tested. My advice: never use this setting.

![fast-math](../../assets/7e753f892cd5bd12.png)


### Fused Multiply-Add

[Fused multiply-add](https://en.wikipedia.org/wiki/Multiply%E2%80%93accumulate_operation) (FMA) is another troublemaker. These special CPU instructions improve precision and performance slightly by rounding only once when computing the expression:

Unfortunately these instructions are not available on all CPUs and different compilers may make different choices about when to use them. This can lead to inconsistent rounding across platforms. So FMA must be disabled for cross-platform determinism. FMA can be disabled on Clang and GCC using `-ffp-contract=off`

. Easy enough.

### Trigonometry

Trigonometric functions are implemented in the C standard library specific to each compiler. Box2D uses `sinf`

, `cosf`

, and `atan2f`

. I implemented custom approximate versions of these that give the same result on every platform. Fortunately Box2D doesn’t need these functions to be super accurate.

In my testing `sinf`

and `cosf`

give the same answers on all compilers and CPUs I’ve tested. But I don’t trust this result will hold, so I’m still using my custom versions. Box2D doesn’t call these internally, but they are called if you use the function `b2MakeRot()`

. Further testing showed that `atan2f`

gives different answers on different platforms, so it is necessary to implement.

There are plenty of approximate versions of sine, cosine, and arc-tangent available. I basically picked ones that seemed easy to implement. Using SIMD for these is not necessary nor beneficial to Box2D performance.

Some good news is that `sqrtf`

is deterministic. Box2D uses `sqrtf`

a lot and needs good accuracy. Assembly code reveals this calls the `sqrtss`

SSE instruction on x64. See [this](https://godbolt.org/z/EqbPrPTaM).

### Results

By avoiding fast-math, FMA, and implementing `atan2f`

I was able to make Box2D cross-platform deterministic. This is a much better result than having to implement fixed-point math which would likely be much slower, difficult to code, reduce the feasible world size, have overflow, and likely more problems I haven’t thought of.

Because Box2D was designed with determinism in mind, there is no noticeable performance impact. I keep the benchmarks up to date [here](https://box2d.org/files/benchmark_results.html).

The video below shows the Falling Hinges sample running on an Apple M2 and producing a result identical to an AMD Ryzen CPU.

## Roll-back Determinism

Further determinism requirements may become important in multiplayer games. This depends a lot on your game design.

Often multiplayer games will use [client-side prediction](https://en.wikipedia.org/wiki/Client-side_prediction). This helps to hide latency and makes a game feel more responsive. The idea is to predict the client simulation in advance of information received from the server. Once the server sends information to the client, the client can detect a desynchronization. If the client and server disagree, the client rolls back to the server result and then re-simulates forward.

Rolling back a physics world means moving the rigid bodies back to some previous transform and velocity. You would like this rollback and re-simulation to match the expected server result. However, this does not work in many physics engines because there is a lot of internal state and orderings that can get out of sync. This desynchronization means the client will always be rolling back. This can be quite expensive for the client and the simulation may jitter.

There is also a cost to server performance with this re-simulation. When the client simulates ahead of the server, it can send some hash of the current state to the server along with the user input. If the server observes that the client state matches its simulation, it can skip sending data to the client.

Roll-back is also problematic when a player joins a game that is in progress. The server would need to send down the entire world state to the client. This would greatly limit the world size in order to limit network bandwidth.

Roll-back could be greatly simplified by reducing or eliminating the internal state in the physics engine. Unfortunately this will reduce stability, but it might work for some games if the limitations are understood.

Another solution is to avoid predicting physics on the client. For example, a falling building doesn’t need to be predicted because the player does not perceive latency.

Currently Box2D does not provide roll-back determinism. Box2D has a lot of internal state that affects the simulation and there is no mechanism for rolling back this internal state.

## Conclusion

Box2D now has 3 levels of determinism: algorithmic, multithreaded, and cross-platform. There are no settings for this. It is the default.

However, Box2D does not have roll-back determinism. Roll-back determinism has many trade-offs and the choice of trade-off might depend on the specific game design.

In the future, I expect to work on features to provide experimental support for roll-back determinism. You can sponsor the Box2D project [here](https://github.com/sponsors/erincatto).

## References

1728 words

2024-08-26 17:00 -0700