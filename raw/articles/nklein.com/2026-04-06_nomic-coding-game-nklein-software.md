---
title: 'Nomic Coding Game :: nklein software'
url: http://nklein.com/2026/04/nomic-coding-game/
author: Pat
published: '2026-04-06'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

About 30 years ago, I had an idea for a coding game inspired by Nomic. It occurred to me last month that all of the tools I need are readily available now.

## Pen-and-paper Nomic

The pen-and-paper game of [Nomic](https://en.wikipedia.org/wiki/Nomic) (by Peter Suber) has an [initial ruleset](https://web.archive.org/web/20200310063900/http://legacy.earlham.edu/~peters/writing/nomic.htm#initial%20set) which describes how one proposes changes to the rules, how one gets those changes ratified, a way to award points when someone’s rule change is ratified, and a rule declaring that the winner is the first player to amass 100 points. Some of the rules are mutable and some are immutable and there are rules about turning mutable rules into immutable ones and vice-versa.

The game was meant to show some of the paradoxes of self-amendment. It was meant to lead people into situations where it was clear that certain actions were both legal (or even mandatory) and illegal.

A drastically simplified starting set of rules might look like:

- There are these players: Alice, Bob, Carol, David, and Mel.
- Any of the players can propose a change to these rules at any time when there is not already an outstanding proposal.
- When a player makes a proposal, all players (including the player making the proposal) must immediately vote: Yay or Nay.
- If a proposal garners more Yay than Nay votes, it takes effect immediately. Otherwise, the proposal is rejected.
- The winner is the first person to score 100 points.

## Nomic in Code

So, 30 years ago, I had the idea that it would be fabulous to write some code to referee a Nomic game. However, because interpretation of the rules is so horrendously human, it felt impossible. Today, in 2026, it seems one could maybe get Claude, Gemini, or some other LLM to referee. But, this doesn’t much interest me, either, really. I cannot get any of them to keep track of something that I made them write down. I cannot imagine that I would be happy with their interpretation of whether my move is legal given the current state of the rules nor to amend the rules appropriately if my move is legal.

What felt slightly more attainable 30 years ago would be to make it a battle in code:

- The players propose deltas to the current code.
- The players vote on which deltas to approve.
- If the resulting code declares you the winner, you win.

This was nice and all, but it was also too static. The rules about who can vote and how votes are tallied and such wouldn’t be subject to change.

## Nomic in Code in 2026

Fast-forward to last month. Last month, I realized that with the GitHub API interface, I could implement a very Nomic-ish pull request battle game. I can:

- Gather information about all of the open pull requests on a repository,
- Checkout a copy of the current
`main`

branch of that**same**repository, - Run the code on the
`main`

branch of that repository and give it the information that I collected about the open pull requests, and - Have the code on the
`main`

branch tell me which open pull requests (if any) to accept or reject.

To be truly in Nomic’s full spirit, it would be nice to allow the code in the repository to interact with the GitHub API on its own. Alas, that would immediately let the players vote in changes that expose my GitHub tokens, so it would be a gaping security hole—not only because it would let users impersonate me but because it would let them end-around the actual code in the repository to make changes to the `main`

branch in the repository.

So, as it is, I have a [supervisor](https://github.com/nklein/cl-nomic-supervisor) written in Common Lisp which handles all of the interaction with GitHub and various game repositories (one to [play in Common Lisp](https://github.com/nklein/cl-nomic-game), one to [play in JavaScript](https://github.com/nklein/js-nomic-game), and one to [play in Python](https://github.com/nklein/py-nomic-game)). The supervisor:

- fetches all of the open pull requests;
- annotates each pull request with:
- all of the reviews on the pull request,
- all of the comments on the pull request, and
- all of the commits on the pull request;

- clones the
`main`

branch of the game repository; - runs the game code from that
`main`

branch giving it the annotated list of open pull requests encoded as JSON on standard input; - reads the JSON-encoded output from the game code; and
- acts accordingly.

The game code, given a list of open pull requests can reply with one of the following messages:

"decision": "winner",

"name": name-of-winner,

"message": optional-reason-for-decision

}

{

"decision": "accept",

"id": id-number-of-pull-request-to-accept,

"message": optional-reason-for-decision

}

{

"decision": "reject",

"id": id-number-of-pull-request-to-reject,

"message": optional-reason-for-decision

}

{

"decision": "defer"

}

The `"defer"`

decision means that there is not enough information at the moment. Maybe, in the future, with other pull requests or other comments or reviews we will be able to make some *move*.

If the game code replies with anything that isn’t one of the four types of replies shown above, the supervisor assumes the latest merge broke the code and reverts the change.

## The Ask

I haven’t been able to drum up enough players for a game in any of my regular haunts. So, I am looking for tolerant players who will help me give it a test run or two to work out the kinks in the supervisor. Some areas where I forsee potential issues:

- There may be scenarios that cause the game to reach an impasse.
- There are probably some GitHub responses that the supervisor doesn’t do the right thing with (in fact, I think I just thought of a situation that a malicious player could do if they are a collaborator rather than doing this through forked repos).
- There might be special issues related to pull requests coming in from forks rather than within the repo which I cannot test without making myself a second GitHub account.
- Who can say what the optimal number of players is, at this point?

So, if you’re tolerant of some bumps in the process, have a GitHub account (or will make one), and are interested in a Common Lisp battle of pull requests, let me know so we can get a game going.