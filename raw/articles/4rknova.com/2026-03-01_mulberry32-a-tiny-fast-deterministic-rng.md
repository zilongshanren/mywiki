---
title: 'Mulberry32: A Tiny, Fast, Deterministic RNG'
url: https://www.4rknova.com/blog/2026/03/01/mulberry32-rng
author: Nikolaos Papadopoulos
published: '2026-03-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

When you need random numbers in JavaScript, you usually reach for `Math.random()`

. That works for many tasks, but it has practical limitations: you cannot seed it for reproducible runs, and its implementation details are not part of the language spec.

If you need deterministic randomness for procedural generation, simulations, or test fixtures, Mulberry32 is a great fit. It is tiny, fast, and easy to embed in any project.

# What Mulberry32 is

Mulberry32 is a 32-bit pseudo-random number generator (PRNG). You provide a 32-bit seed, and it produces a deterministic sequence of values. The same seed always gives the same sequence.

That deterministic property is the whole point. It lets you:

- Replay generated game worlds from a seed.
- Reproduce simulation results during debugging.
- Create stable random test data.
- Share compact seed strings between users.

Mulberry32 hits a practical sweet spot: tiny implementation, deterministic behavior, and enough quality for many real-world app and game tasks.

If you treat it as one explicit randomness source, pass it through your systems, and keep call order intentional, you get reproducible behavior with almost no infrastructure overhead.

# The core algorithm

The entire generator fits in a few lines. Here is the core function:

```
function mulberry32(seed) {
let t = seed >>> 0; // force seed into uint32
return function next() {
t = (t + 0x6D2B79F5) >>> 0; // advance internal state (uint32 wrap)
// Mix bits using xor-shifts and 32-bit multiplication.
let x = Math.imul(t ^ (t >>> 15), t | 1);
x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
// Convert uint32 to float in [0, 1).
return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
}
```


The returned `next()`

function yields floating-point values in `[0, 1)`

. Internally, state updates and bit mixing stay in 32-bit arithmetic.

Key parts:

`>>> 0`

forces values into unsigned 32-bit form.`Math.imul(a, b)`

performs correct 32-bit integer multiplication.- Final division by
`2^32`

maps the mixed 32-bit integer into`[0, 1)`

.

# Mathematical form

One Mulberry32 step can be written as:

\[t_{n+1} = (t_n + c) \bmod 2^{32}\] \[u_n = t_{n+1} \oplus (t_{n+1} \gg 15)\] \[v_n = \operatorname{imul}(u_n,\ t_{n+1}\ |\ 1)\] \[w_n = v_n \oplus \left(v_n + \operatorname{imul}(v_n \oplus (v_n \gg 7),\ v_n\ |\ 61)\right)\] \[r_n = \frac{(w_n \oplus (w_n \gg 14)) \bmod 2^{32}}{2^{32}}\]where \(c = 0x6D2B79F5\), \(\oplus\) is XOR, and \(\gg\) is logical right shift.

# Bitwise operations explained

Mulberry32 relies on a few bitwise operators to keep state in 32-bit space and to mix bits aggressively.

`>>>`

is a zero-fill right shift. It shifts bits to the right and fills the left with zeros.

`x >>> 15`

drops the lowest 15 bits and exposes higher-bit structure.`x >>> 0`

is a common JavaScript trick to coerce a number into unsigned 32-bit form.

`^`

is bitwise XOR. A bit in the result is `1`

only when input bits differ.

`t ^ (t >>> 15)`

mixes high and low regions of`t`

.`x ^ (x >>> 7)`

repeats that idea with a different shift distance.`x ^ (x >>> 14)`

is a final avalanche-style mix before conversion to float.

`|`

is bitwise OR.

`t | 1`

forces the least significant bit to`1`

, making the value odd.`x | 61`

forces a small fixed bit pattern into the multiplier path.

Those odd multipliers matter because multiplication by odd numbers in 32-bit modular arithmetic tends to preserve more variation across bit positions than many even multipliers.

`Math.imul(a, b)`

multiplies as signed 32-bit integers with wraparound. Normal JavaScript multiplication uses 64-bit floating-point math, which can lose the exact 32-bit overflow behavior PRNG formulas depend on.

Putting it together for one line:

```
let x = Math.imul(t ^ (t >>> 15), t | 1);
```


`t >>> 15`

: shift`t`

right, exposing higher bits in lower positions.`t ^ (t >>> 15)`

: fold those shifted bits back into`t`

.`t | 1`

: force odd multiplier input.`Math.imul(...)`

: multiply with exact 32-bit wrap semantics.

Each stage intentionally moves information between bit positions so nearby internal states do not produce trivially related outputs.

# A complete, practical implementation

The raw function is enough, but most projects want a few helpers. Below is a small wrapper that gives you common operations while keeping deterministic behavior.

```
function createMulberry32(seed) {
let state = seed >>> 0; // mutable uint32 state
const nextFloat = () => {
state = (state + 0x6D2B79F5) >>> 0; // deterministic state step
let x = Math.imul(state ^ (state >>> 15), state | 1);
x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
};
return {
float() {
return nextFloat();
},
int(maxExclusive) {
if (!Number.isInteger(maxExclusive) || maxExclusive <= 0) {
throw new Error("int(maxExclusive) needs a positive integer");
}
// Uniform integer in [0, maxExclusive).
return Math.floor(nextFloat() * maxExclusive);
},
range(minInclusive, maxExclusive) {
if (!Number.isFinite(minInclusive) || !Number.isFinite(maxExclusive)) {
throw new Error("range(min, max) needs finite numbers");
}
if (!(maxExclusive > minInclusive)) {
throw new Error("range(min, max) requires max > min");
}
return minInclusive + nextFloat() * (maxExclusive - minInclusive);
},
bool(p = 0.5) {
if (p < 0 || p > 1) {
throw new Error("bool(p) requires 0 <= p <= 1");
}
return nextFloat() < p;
},
pick(array) {
if (!Array.isArray(array) || array.length === 0) {
throw new Error("pick(array) needs a non-empty array");
}
return array[this.int(array.length)];
},
shuffle(array) {
if (!Array.isArray(array)) {
throw new Error("shuffle(array) needs an array");
}
const out = array.slice();
// Fisher-Yates shuffle driven by this seeded RNG.
for (let i = out.length - 1; i > 0; i -= 1) {
const j = this.int(i + 1);
[out[i], out[j]] = [out[j], out[i]];
}
return out;
},
getState() {
return state >>> 0;
},
setState(nextState) {
state = nextState >>> 0;
},
};
}
```


This gives you one deterministic source for all random operations in your app. If you create multiple RNG instances with the same seed and call pattern, they produce identical results.

# Usage examples

```
const rngA = createMulberry32(123456789);
const rngB = createMulberry32(123456789); // same seed as rngA
console.log(rngA.float());
console.log(rngA.int(10));
console.log(rngA.range(-1, 1));
console.log(rngA.bool(0.25));
console.log(rngA.pick(["red", "green", "blue"]));
console.log(rngA.shuffle([1, 2, 3, 4, 5]));
// Not in lockstep: rngA already consumed values.
console.log(rngA.float() === rngB.float()); // false
// Lockstep check with fresh instances.
const a = createMulberry32(123456789);
const b = createMulberry32(123456789);
console.log(a.float() === b.float()); // true
console.log(a.float() === b.float()); // true
console.log(a.float() === b.float()); // true
```


The call order matters. If one code path consumes an extra random number, all later values diverge from the other run.

# Seeding from strings

Users usually share text seeds, not integers. A small 32-bit hash is enough to convert strings into a Mulberry32 seed.

```
function hashStringToUint32(input) {
let h = 2166136261 >>> 0; // FNV-1a 32-bit offset basis
for (let i = 0; i < input.length; i += 1) {
h ^= input.charCodeAt(i); // xor in next character
h = Math.imul(h, 16777619); // multiply by FNV prime
}
return h >>> 0;
}
const seed = hashStringToUint32("world-7-night-rain");
const rng = createMulberry32(seed);
```


Now users can share human-readable seeds while your system still operates on a compact 32-bit value.

# Basic sanity checks

Mulberry32 is not a high-end statistical generator, but you can still run quick checks to catch implementation mistakes.

```
const rng = createMulberry32(42);
let sum = 0;
let countLow = 0;
const n = 1_000_000;
for (let i = 0; i < n; i += 1) {
const x = rng.float(); // next sample in [0, 1)
sum += x;
if (x < 0.5) countLow += 1;
}
console.log("mean", sum / n); // roughly 0.5
console.log("fraction < 0.5", countLow / n); // roughly 0.5
```


# Prior art and alternatives

Mulberry32 is best viewed as a compact, practical generator for deterministic app-level tasks, not as a state-of-the-art PRNG.

If you need a stronger general-purpose default, prefer a well-studied family such as PCG (for example, PCG32) [1].

For simulation-heavy or scientific workloads, choose generators with broader published analysis and explicit battery-test coverage.

# When to use Mulberry32

Mulberry32 is a strong choice for:

- Procedural maps, loot rolls, and spawn patterns in games.
- Visual effects and generative art with replayable seeds.
- Monte Carlo style experiments where lightweight speed matters.
- Unit and integration tests that need deterministic random fixtures.

Avoid it for:

- Cryptography, tokens, password reset links, and secrets.
- Gambling or regulated fairness contexts.
- Cases that require very high statistical rigor over massive streams.

# Common mistakes

- Mixing
`Math.random()`

with your seeded RNG in the same logic path. - Forgetting to keep call order stable across platforms or refactors.
- Re-seeding on every frame instead of preserving evolving state.
- Assuming deterministic output across changed code that consumes RNG values in a different order.