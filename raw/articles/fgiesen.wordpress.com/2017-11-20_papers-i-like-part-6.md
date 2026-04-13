---
title: Papers I like (part 6)
url: https://fgiesen.wordpress.com/2017/11/20/papers-i-like-part-6/
published: '2017-11-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 6)

Continued from [part 5](https://fgiesen.wordpress.com/2017/09/02/papers-i-like-part-5/). (Sorry for the long delay, I was busy with other things.)

### 24. O’Neill – [“PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation”](http://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) (2014; pseudo-random number generation)

This paper (well, more like a technical report really) introduces a new family of pseudo-random number generators, but unlike most such papers, it’s essentially self-contained and features a great introduction to much of the underlying theory. Highly recommended if you’re interested in how random number generators work.

Unlike most of the papers on the list, there’s not much reason for me to write a lot about the background here, since essentially everything you need to know is already in there!

That said, the section I think everyone using random-number generators should have a look at is section 3, “Quantifying Statistical Performance”. Specifically, the key insight is that *any* pseudorandom number generator with a finite amount of state must, of necessity, have certain biases in the sequences of numbers it outputs. A RNG’s period is bounded by the amount of state it has – a RNG with N bits can’t possibly have a period longer than 2N, per the pigeonhole principle – and if we also expect the distribution of values over that full period to be uniform (as is usually desired for RNGs), that means that as we draw more and more random numbers (and get closer to exhausting a full period of the RNG), the distribution of numbers drawn must – of necessity – become distinguishable from “random”. (Note that how exactly to measure “randomness” is a thorny problem; you can’t really prove that something is random, but you *can* prove that something isn’t random, namely by showing that is has some kind of discernible structure or bias. Random number generators are generally evaluated by running them through a barrage of statistical tests; passing these tests is no guarantee that the sequence produced by a RNG is “sufficiently random”, but failing even one test is strong evidence that it isn’t.)

What the paper then does is instead of comparing random number generators with N bits of internal state to an idealized random source, they instead compare them to the performance of an ideal random number generator *with N bits of internal state* – ideal here meaning that its internal state evolves according to a randomly chosen permutation with a single cycle. That is to say, instead of picking a new “truly random” number every time the RNG is called, we now require that it has a limited amount of state; there is a (randomly chosen!) list of 2

N uniformly distributed random numbers that the generator cycles through, and because the generator only has N bits of state, after 2N evaluations the list must repeat. (A side effect of this is that any RNG that outputs its entire state as its return value, e.g. many classic LCG and LFSR generators, will be easy to distinguish from true randomness because it never repeats any value until looping around a whole period, which is statistically highly unlikely.) Moreover, after going through a full cycle of 2N random numbers, we expect all possible outputs to have occurred with (as close as possible to) uniform probability.

This shift of perspective of comparing not to an ideal random number generator, but to the best any random number generator can do *with a given amount of state*, is crucial. The same insight also underlies another fairly important discovery of the last few years, [cryptographic sponge functions](https://keccak.team/sponge_duplex.html). Cryptographic sponges started as a theoretical construction for hash function construction, starting from the desire to compare not to an idealized “random oracle”, but instead a “random sponge” – which is like a random oracle except it has bounded internal state (as any practical cryptographic hash has, and must).

Armed with this insight, this paper then goes on to compare the performance of various published random number generators against the theoretical performance of an ideal RNG with the same amount of state. No generator with a given amount of state can, in the long term and on average, do better than such an ideal RNG with the same amount of state. Therefore, checking how close any particular algorithm with a given state size comes to the statistical performance of a same-state-size ideal RNG is a decent measure of the algorithm quality – and conversely, reducing the state size must make any RNG, no matter how good otherwise, eventually fail statistical tests. How much the state size can be reduced before statistical deficiencies become apparent is thus an interesting metric to collect. The paper goes on to do just that, testing using the well-respected TestU01 test suite by L’Ecuyer and Simard. It turns out that:

- Many popular random number generators fail certain randomness tests, regardless of their state size. For example, the Mersenne Twister, being essentially a giant Generalized Feedback Shift Register (a generalization of
[Linear-Feedback Shift Registers](https://en.wikipedia.org/wiki/Linear-feedback_shift_register), one of the “classic” pseudorandom number generation algorithms), has easily detectable biases despite its giant state size of nearly 2.5 kilobytes. - Linear Congruential Generators (LCGs), the other big “classic” family of PRNGs, don’t perform particularly great for small to medium state sizes (i.e. the range most typical LCGs fall into), but improve fairly rapidly and consistently as their state size increases.
- “Hybrid” generators that combine a simple basic generator to evolve the internal state with a different function to produce the output bits from the state empirically have much better statistical performance than using the basic generators directly does.

From there on, the paper constructs a new family of pseudorandom number generators, PCGs (“permuted congruential generators”), by combining basic LCGs (with sufficient amount of state bits) for the internal state evolution with systematically constructed output functions based on certain types of permutations, and shows that they combine state-of-the-art statistical performance with relatively small state sizes (i.e. low memory usage) and high speed.

### 25. Cook, Podelski, Rybalchenko – [“Termination Proofs for Systems Code](http://www.ccs.neu.edu/home/wahl/Teaching/Software-Model-Checking/2016-Spring/Papers/termination.pdf) (2006; theoretical CS/program analysis)”

This paper is about an algorithm that can automatically prove whether programs terminate. If you’ve learned about the [halting problem](https://en.wikipedia.org/wiki/Halting_problem), this might give you pause.

I’ll not talk much about the actual algorithm here, and instead use this space to try and explain how to reconcile results such as the halting problem and [Rice’s theorem](https://en.wikipedia.org/wiki/Rice%27s_theorem) with the existence of software tools that can prove termination, do static code analysis/linting, or even just advanced optimizing compilers!

The halting problem, informally stated, is the problem of deciding whether a given program with a given input will eventually complete, or whether it will run forever. Alan Turing famously proved that this problem is undecidable, meaning that there can be no algorithm that will always give a correct yes-or-no answer to any instance of this problem after running for a finite amount of time.

Note that I’m stating this quite carefully, because it turns out that all of the small restrictions in the above paragraph are important. It is very easy to describe an algorithm that always gives a yes-or-no answer to any halting problem instance if the answer isn’t required to be correct (duh); the problem is also tractable if you don’t require the algorithm to work on *any* program, since there are absolutely sets of programs for which it is easy to prove whether they halt or not. And finally, if we relax the “finite run time” requirement, we can get by on a technicality: just run the program. If it has terminated yet, return “yes”; if not, well, it might terminate further on, so let’s not commit to an answer yet and keep going!

Rice’s theorem builds on the halting problem construction to show that there can be no algorithm that can, with certainty, produce the answer to any “interesting” (meaning it is not true or false for all possible programs) yes-or-no question in finite time.

That sounds like pretty bad news for program analysis. But it turns out that even if we want something that is correct, works on *any* program, and answers in a finite amount of time, we have one last resort left: we can relax the “yes-or-no” requirement, and give our algorithm a third possible return value, “not sure”. Once we allow for that option, it’s obvious that there is a (trivial) solution: the easiest such solver can just return “not sure” for absolutely every program. This is technically correct (the best kind!) but not very useful; however, it gives us something to build on. Namely, instead of having to come up with a definitive yes-or-no answer on the unwieldy set of all possible programs given all possible inputs (which, as stated before, is undecidable), we lower our aim slightly and merely try to be able to give termination proofs (or answer other program analysis-type questions) for *some* programs – hopefully practically relevant ones. And if we get a program that we can’t say anything with certainty about, we always have our “not sure” escape hatch.

To explain, let me show you three functions, this time using a Python 3-esque instead of my usual C/C++-esque pseudocode, to show a few different ways this can play out:

def func1(): while True: print('Hello world!') def func2(n): n = int(n) while n > 0: print('All good things must end!') n -= 1 def func3(n): n = int(n) if n <= 0: return while n != 1: print(n) if (n % 2) == 0: n = n/2 else: n = 3*n + 1

The first function, `func1`

, contains an obvious infinite loop. It’s easy to see (and prove) that it never terminates.

The second function, `func2`

, contains a loop that is definitely terminating. (The conversion to integer at the start is an important technicality here, since this kind of loop is *not* guaranteed to terminate if `n`

is a sufficiently large floating-point number.) The argument here is straightforward: `n`

keeps steadily decreasing throughout the loop, and any integer, no matter how big, can only be decremented a finite number of times before it will be ≤0. Very similar arguments apply for loops iterating over lists that aren’t modified inside the loop, and other typical iteration constructs – in short, a very common class of iteration in programs can be shown to terminate quite easily. (Simplifying a lot, the Terminator paper uses a generalized version of this type of argument to prove termination, when it can.)

Finally, `func3`

shows a case that is legitimately hard. Showing that this program always terminates is equivalent to proving the [Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture), a long-standing open problem. Currently, it is conjectured that it will always terminate, and it has been verified that there are no “small” counterexamples (the sequence definitely terminates for any number up to around 260, for example), but nobody knows the answer for sure – or if they do, they aren’t talking.

This is also the reason for the underlying difficulty here: the set of “all possible programs” is extremely big, and many other complex problems – like, in this case, mathematical theorems – can be converted into termination proofs for certain programs.

However, the second example shows that there is hope: while some simple programs are hard to prove anything about, many programs – even fairly complex ones – only use constructs that are fairly easy to show are terminating, and even when we can’t prove anything about a whole program, being able to automatically prove certain properties about say *parts* of the program is a lot better than not having anything at all.

The same thing applies to other types of program analysis, like for example used in optimizing compilers: *if* the compiler can figure out some non-trivial property of the program that is useful for some tricky transformation, great! If not, it’s stuck with leaving the code in the form that it’s written, but that’s still no worse than we started out with.

### 26. O’Neill – [“The Genuine Sieve of Eratosthenes”](https://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf) (2009; programming)

As a bit of a palate cleanser after the previous paper (which is rather technical), this is a paper about a pet peeve of mine. Specifically, describing something like this piece of Haskell code (using the version from the paper) as the “Sieve of Eratosthenes” (a standard algorithm to find prime numbers):

primes = sieve [2..] sieve (p : xs) = p : sieve [x | x <- xs, x `mod` p > 0]

The operation of this type of program (which is [not limited to lazy functional languages](https://github.com/golang/go/blob/master/test/sieve.go), by the way) can indeed be understood as a kind of “sieving” process, but the underlying algorithm is not, in fact, the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes); rather, it is equivalent to a rather inefficient implementation of basic trial division, that ends up with significantly worse asymptotic complexity than either “proper” trial division or the true Sieve of Eratosthenes (see section 2.1 of the paper). Its run time is, for large n, worse than the true sieve by about a factor of – not quite

[“accidentally quadratic”](https://accidentallyquadratic.tumblr.com/), but close! (I’m neglecting a term for the true sieve, but iterated logs grow so slowly that they’re essentially negligible for algorithms that need memory proportional to n, since in that case, the possible values for

on any physically realizable machine are bounded by a very small constant.)


Now, the interesting part here isn’t that a given Haskell one-liner (or two-liner) isn’t the most efficient way to solve this problem; that’s hardly surprising. But what I do find interesting is that the “unfaithful sieving” algorithm implemented by the short program above is frequently claimed to be the true Sieve of Eratosthenes, despite being not even close.

It goes to show that what feels like small implementation details can often make very significant differences, and in ways that even seasoned experts miss for years. It’s not a bad idea to get into the habit of plotting the run times of any algorithm you implement for a few problem sizes, just to check whether it looks like it has the asymptotic runtime you think it should have or not. In this case, it hardly matters, but for more serious applications, it’s a lot better to discover this kind of problem during testing that it is in production.

Just as an aside, termination analysis is itself useful in optimising compilers. Suppose you have a Prolog-like language which looks like this:

program := p, q.

Is it valid to transform this into this?

program := q, p.

Obviously it’s not if q is impure, such as reading from or altering global state. So we’ll assume this is a pure Prolog-like language where this is a non-issue.

This transformation is correct if and only if q terminates.

Err… I meant :- not :=.