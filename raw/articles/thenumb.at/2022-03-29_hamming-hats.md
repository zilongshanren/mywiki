---
title: Hamming Hats
url: https://thenumb.at/Hamming-Hats/
published: '2022-03-29'
source_blog: Max Slater
source_site: https://thenumb.at/
category: graphics
fetched: '2026-04-13'
---

# Hamming Hats

*I first encountered the Hat Problem in CMU 15-251*.

## The Game

Consider a 31-person game in which each player is assigned a red or blue hat, determined by an independent coin flip. The players can see everyone else’s hat color, but **not** their own.

Once the game begins, no communication is allowed between the players. After looking at the other hats, all players must *simultaneously* either announce the color of their hat or abstain from guessing. If at least one player correctly announces their hat color, and no players incorrectly announce theirs, the group wins.

What strategy can the group use to obtain a high probability of winning?

## A Simple Strategy

The group could choose one person to always announce red and have all other players always abstain. This strategy wins 50% of the time. However, it clearly doesn’t make use of all the available information, so we can do better.

In fact, we can do *much* better by making use of an error-correcting code. But what do error-correcting codes have to do with the hat game?

Let’s start by describing the game state as a 31-bit binary number, where bit $$i$$ specifies the color of player $$i$$’s hat. As a player, we can see everyone else’s hat, so we know 30 bits of this number. Since the group can agree on a consistent ordering of players beforehand, we also know the index of our unknown bit. If we could somehow use all the other bits to pin down ours, we could correctly announce our hat color and win the game. That sounds like a job for error correction.

## Hamming Codes

If you’re new to Hamming codes, first watch 3Blue1Brown’s [excellent video on the topic](https://www.youtube.com/watch?v=X8jsijhllIA).

Here, we’ll make use of a matrix-based definition of Hamming codes, which will allow us to use tools from linear algebra. We will be working with vectors over the field $$\mathbb{F}_2$$, that is, the integers modulo 2. If you’ve just watched the video, you might notice that summing bits modulo two is the same as computing their parity.

To define a Hamming code, first choose a positive integer $$r$$ and let $$n = 2^r - 1$$. Our code will use $$n$$ bit words to encode $$n-r$$ bits of data, providing the ability to correct arbitrary 1-bit errors.

The set of Hamming codewords is defined as:

Where $$H_{r,n}$$ is a $$r \times n$$ matrix whose $$i$$th column is the $$r$$-bit binary representation of $$i$$.

For example, if $$r = 3, n = 7$$, then

We call $$H$$ ‘’error-correcting’’ because given a non-codeword $$z$$ (i.e. $$Hz \neq 0$$), $$Hz$$ will be the binary representation of the position of the ‘’error’’ in $$z$$. That is, if we flip bit $$Hz$$ in $$z$$, the result will be a codeword. For example,

If we flip the sixth ($$110$$) bit in $$z$$, we in fact get a codeword ($$1010101$$). This suggests that every non-codeword can be transmuted into a unique codeword by flipping exactly one bit. Let’s prove that.

By construction, any two columns in $$H$$ differ in at least one position. That means every pair of columns is linearly independent—i.e. you can’t add two columns together and get the zero vector. Then, consider that for any non-zero codeword $$c$$, $$Hc$$ is a linear combination of the columns of $$H$$. Since $$c$$ is a codeword, we know $$Hc = 0$$, so $$c$$ must add together *at least three* columns from $$H$$. Therefore, $$c$$ must have at least three bits set.

Now consider any two codewords $$c_1 \neq c_2$$:

That is, the difference between any two codewords is itself a codeword—and must have at least three bits set. Therefore, all codewords differ from all others in at least three positions.

Now, given an $$n$$-bit codeword $$c$$, we can construct $$n$$ other words that differ in exactly *one* bit. Because transmuting $$c$$ into a different codeword would require changing at least *three* bits, we know that none of our new words can be one bit different from any *other* codeword than $$c$$.

Finally, let’s count the number of codewords. Since by construction, the columns of $$H$$ include each $$r$$-bit basis vector, $$H$$ has rank $$r$$ and nullity $$n-r$$. Since we defined $$C$$ as the null space of $$H$$, there are $$2^{n-r}$$ codewords.

For each codeword, we can generate $$n$$ unique non-codewords, which accounts for…

…all words! Therefore, every word is either a codeword or differs from a unique codeword in exactly one bit.

## A Better Strategy

We’re now ready to devise a better strategy for the hat game. Beforehand, the group of $$n$$ players can communicate the appropriate Hamming matrix $$H_{r,n}$$ and set a player order.

Once hats are assigned, each player constructs both the game state $$s_b$$ assuming that they’re wearing blue and the state $$s_r$$ assuming they’re wearing red.

- If $$H_{r,n}s_b \neq 0$$ and $$Hs_r = 0$$, they announce blue.
- If $$H_{r,n}s_b = 0$$ and $$Hs_r \neq 0$$, they announce red.
- If $$H_{r,n}s_b \neq 0$$ and $$Hs_r \neq 0$$, they abstain.

Note that it’s impossible for both results to be be zero.

The Hamming strategy wins the game whenever the initial distribution of hats is *not* a codeword. By the above proof, we know that when the state is not a codeword, it differs from exactly one codeword in exactly one bit. This means that there is a single player for whom switching their hat color would make the state a codeword: that player will observe $$Hs = 0$$ when assuming the incorrect choice, and $$Hs \neq 0$$ when assuming the correct choice. All other players will observe $$Hs \neq 0$$ for both assumptions because toggling their bit would not make the state a codeword. Therefore, one player will announce their correct color, and the group wins.

For example, in a 7-player hat game with initial distribution $$\begin{bmatrix}1&0&1&0&1&1&1\end{bmatrix}$$:

- Player 1 finds:

- Players 2-5 and 7 also find $$H_{3,7}s_b \neq 0$$ and $$H_{3,7}s_r \neq 0$$.
- Player 6 finds:

The lone player 6 announces color 1, and the group wins.

On the other hand, the group will lose the game when the initial distribution *is* a codeword. In this case, all players will determine that one hat color—the *correct* one—results in a codeword, and the other does not. This is because when the true state is a codeword, changing any one bit will result in a non-codeword. In this case, all players will announce the wrong color, and the group loses.

For example, again in the 7-player game, but this time with initial distribution $$\begin{bmatrix}1&0&1&0&1&0&1\end{bmatrix}$$:

- Player 1 sees:

- Player 2 sees:

- All other players find the equivalent.

Hence, all players announce the incorrect color.

## Optimality

Our Hamming strategy wins whenever the true arrangement of hats does not represent a codeword. Since there are $$n\times 2^{n-r}$$ non-codewords out of $$2^n$$ total words:

The 31-person group has an approximately 97% chance to win the game, given a uniformly random initial distribution. But, is 97% necessarily the best they can do?

Let’s bound the maximum number of games that *any possible* strategy could win. Given an arbitrary strategy, each individual player will guess correctly and incorrectly in an equal number of game states. This is because each player’s decision making process must be independent of the color of their *own* hat: given the same information about the 30 other hats, the player *must* either abstain or guess the same color in both the state where they’re wearing red *and* where they’re wearing blue. Hence, for the individual to be right in one state, they must be wrong in the other.

However, this fact doesn’t mean our overall strategy has to lose as much as it wins: if we can use up more incorrect guesses in losing rounds than correct guesses in winning rounds, our overall win-rate will increase. Optimally, we would have exactly one player guess correctly in every winning round, and have all players guess incorrectly in every losing round. This implies that for every $$n$$ winning rounds, there must be at least one losing round.

Hence, if the strategy wins $$W$$ rounds and loses $$L$$ rounds out of $$2^n$$, we know $$ L \ge \frac{W}{n} $$. Because $$W + L = 2^n$$, we have:

Which means the maximum win probability is in fact $$\frac{n}{n+1}$$, which our Hamming strategy achieves. It is optimal!

Unfortunately, we’ve only defined our Hamming strategy for games with $$n = 2^r - 1$$ players. It may be the case that when the number of players is not one less than a power of two, the optimal strategy is simply to ignore some players and run the largest Hamming strategy available—but this has never been proven!