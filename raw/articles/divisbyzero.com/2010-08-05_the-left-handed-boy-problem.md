---
title: The left-handed boy problem
url: https://divisbyzero.com/2010/08/05/the-left-handed-boy-problem/
author: Dave Richeson
published: '2010-08-05'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

A few months ago Gary Foshee was scheduled to speak at the [Gathering for Gardner](http://g4g4.com/). He got up and gave a presentation that was all of three sentences. He said:

I have two children. One is a boy born on a Tuesday. What is the probability I have two boys?


This deceptively simple problem [quickly](http://www.newscientist.com/article/dn18950-magic-numbers-a-meeting-of-mathemagical-tricksters.html) [made](http://www.maa.org/devlin/devlin_04_10.html) [the](http://news.bbc.co.uk/2/hi/programmes/more_or_less/8735812.stm) [rounds](http://blog.tanyakhovanova.com/?p=234). The knee-jerk answer is , of course—the gender of one child doesn’t change the probabilities for the second child. People with a little training in probability know that that reasoning isn’t a valid—it is an exercise in

[conditional probability](http://en.wikipedia.org/wiki/Conditional_probability). The probability of having two boys given that one child is a boy is . Surely, that’s the correct answer, right? How could the day of the week matter?


It turns out, however, that the probability is an unexpected .


[Note: The *real* correct answer is 0 or 1 since Gary Foshee either has two boys or doesn’t have two boys. The actual question should be “If a randomly-selected family has two children and at least one of them is a boy born on Tuesday, what is the probability that they have two boys?” But that doesn’t sound nearly so slick. I’ll be consistent and stick with his less-than-perfect wording.]

I’d like to pose a question similar to the Tuesday boy problem, then describe how to compute the probabilities for a whole class of problems like these.

I have two children. One is a left-handed boy. What is the probability I have two boys?


You may assume that the probability of being left-handed is 1/10 and that left-handedness is not a genetic trait.

Stop reading here if you want to think about the problem on your own.

Before we answer the left-handed boy problem, lets look at an easier question.

I have two children. One is a boy. What is the probability I have two boys?


We must think of this in terms of conditional probability. We can compute the probability using this formula:

.


There are four equally likely options for any two-child family: the first child is a boy and the second child is a boy (written ), the first child is a boy and the second child is a girl (written

),

, and

. These are shown in the chart below with their probabilities.


However, in our case we can ignore the case because we know that at least one child is a boy.


Observe that:

, and


.


So, .


This problem is particularly easy because all four outcomes are equally-likely. The Tuesday boy problem is trickier. The probability of being born on a Tuesday is and the probability of a non-Tuesday birthday is

.


Now there are 16 possibilities. The notation means that the first child is a girl born on a non-Tuesday and the second child is a boy born on Tuesday. The probability of this particular occurance is

. The probabilities of the others are calculated similarly:


In the chart below we remove the cases in which there is no Tuesday-born boy.

We see that:


.



.


So the answer to the question is:


.


Let us investigate the general case.

I have two children. One is a boy with a trait which occurs with probability

. What is the probability that I have two boys?


We build the chart just as we did in the Tuesday boy problem. Here means that the first child is a girl who does not have the trait and the second child is a boy who has the trait.


Again, we focus on those that have a boy with the trait.

Calculating as before we obtain the probability:

Now we can solve a whole class of these problem. To solve the left-handed boy problem we simply plug in to obtain an answer of

. That is, if a family has two children and one of the children is a left-handed boy, then the probability that they have two boys is

.


If we had asked the “right-handed boy” problem, then we’d plug in to obtain

. That is, if a family has two children and one of the children is a right-handed boy, then the probability that they have two boys is

.


Notice what happens in the limiting values of .


If the trait is very common, like “has two eyes,” then and we’re essentially in the “I have two children and one of them is a boy” case. Accordingly we have

.


On the other hand, if we have an extremely rare trait, like “has climbed Mt. Everest” (), then it is very unlikely that both children have this trait. We’ve essentially uniquely identified one of the children. If we looked at all the two-child families in the entire world that have a son who climbed Mt. Everest, very few of them will have another child who also climbed Mt. Everest. Most of them are a boy who climbed Mt. Everest, and one other child. The chance of the other child being a boy is 1/2. (It is like asking “My first born child is a boy. What is the probability that I have two boys?”) Accordingly,

.


I’d like to thank my colleagues Jeff Forrester and Barry Tesman for their helpful comments.

Suppose I tell you I have two children. One is a boy. With that information you would say that the probability of the other is 1/3. If you then ask, “Was he born on Tuesday” and I say yes, would you really change your answer?

You mathematicians and your assumptions! “You may assume that the probability of being left-handed is 1/10 and that left-handedness is not a genetic trait.”

http://bit.ly/14N5Xm

http://bit.ly/d4XPUh

Thanks for the great explanation!

Sorry, I was tired when I wrote that last night and the phrasing is important. Suppose that I tell you that I have two children and that one is a boy. If you then ask “What day of the week was the boy born on?” If I say “Tuesday” would the answer change? What if I say “Wednesday?”

Unfortunately, I may be out of my league on this one (I’m no expert on probability), but I think we run into trouble with the “I” language—like my parenthetical remark above. For any single person the probability is only 0 or 1. They either do or don’t have two boys. You need to speak in generalities about all possible families. The phrasing of the original question should be: If a randomly-selected family has two children and one is a boy born on Tuesday, what is the probability that they have two boys? I don’t see how we could rephrase your question in that manner.

Perhaps other readers of my blog who are more well-informed about probability could chime in with an answer.

I think in order for it to work you have to be even stronger than this:

If a randomly-selected family has two children and one is a boy born on Tuesday, what is the probability that they have two boys?

In fact, I think the sampling procedure has to be as follows. Suppose I sample randomly from families with two children until I find a boy born on Tuesday. What’s the probability I have two boys.

(Assumes boys and girls are equally likely and a birth is equally likely on every day of the week.)

Takes a lot of the “wow” out of the problem, doesn’t it?

@ThePigLA: When you say “would the answer change?” the answer is, “absolutely.” With weekdays it’s hard to see this, but it really does change. You’ve just narrowed the field of available families that you might be one of. Like Dr. Richeson pointed out, if you “added in” the information that one of the children had climbed Everest, then we would approach certainty about the family’s make up (since there are only a handful of families to which the field narrows).

This whole “updated” probability thing when new information is added is exactly what Baye’s Theorem is perfect for. See http://en.wikipedia.org/wiki/Bayes%27_theorem

In Dave’s problem about the left-handed boy, you could use Baye’s Theorem in the following way (I denote left-handed boy by BL):

P(Both are B | At least one BL) = P(At least one BL | Both are B) * P(Both are B) / P(At least one BL)

= (1/10+1/10-1/100)*(1/4) / (1/20 + 1/20 – 1/400)

= (19/100 * 1/4) / (39/400)

= 19/39

as desired.

(Note the use of the inclusion/exclusion formula to calculate two of those probabilities.)

Here’s the same technique used to calculate the answer to the simpler question: “If there are two children, and one is a boy, what’s the probability that the other is a boy too?”

P(Both B | At least one B) = P(At least one B | Both B) * P(Both B) / P(At least one B)

= (1) * (1/4) / (1/2 + 1/2 – 1/4)

= (1/4) / (3/4)

= 1/3

as desired.

(Notice that P(At least one B | Both B) = 1.)

And in both examples, notice the way we’ve “updated” the probabilities by introducing new information.

My issue is with the sampling process and how it’s left unstated. Let me flesh it out. (Forgive me for the use of ‘I’, but I think that isn’t an issue in the following discussion.)

Suppose that I pick two children at random so that GG, BG, GB, and BB are equally likely. If I pick GG, I reject the sample, and continue until I sample at least one boy. I place the two children in the room and promise you that at least one of them is a boy. Now, if I ask you the probability that there are two boys, then you’d be correct to say 1/3.

Now, let’s suppose after sampling in the above manner that I ask a boy that I’ve sampled the day he was born. (I can choose arbitrarily in the case of BB.) And let’s say he says ‘Tuesday.’ I report this information to you. I believe you would be incorrect to tell me that the probability is 13/27. I think it’s still 1/3.

However, if I modify the sampling process so that I reject a pair if I get GG or there is no B such that B was born on Tuesday, then I believe you are correct to say 13/27.

@ThePigLA

In your example, you need to sample 196 unique pairs of children, not 4. That’s the number of outcomes taking into account the day of the week. Then, it turns into a counting problem. How many of those pairs have a boy born on Tuesday? 27. How many of those pairs are both boys, one of whom was born on Tuesday? 13. Probability = 13/27.

I believe your sample wasn’t representative.

@John Chase

No, I’m sampling from an ‘infinite’ family of pairs of children with the property that each child has an equal probability of being born on {Mon…Sun} and each child has an equal probablity of being {B,G}. If I sample (with rejection) until I find a BB, BG, or GB and reveal a birthday of a boy, you obtain no additional information by knowing the birthday. The probability of a BB is 1/3.

The trick only works if I sample until I find a BB, BG, or GB with the property that one of the Bs was born on a Tuesday, do you obtain any information. And that’s an artifact of my sampling bias.

@ThePigLA

When we say “A family has two children. One is a boy born on a Tuesday. What is the probability they have two boys?”, don’t we immediately mean, consider the set of all two-children families born on all the different weekdays? That would be 14 different kinds of kids, so 14^2 = 196 total families.

I’m not sure the sampling is an issue. It seems pretty clear in the problem that we’re considering the sample space of size 196.

And if you consider it as a new piece of information which ‘updates’ the probability, then you can solve it in Baye’s-Theorem style.

Fascinating post! Thanks for sharing. Love this stuff…makes me miss those days in the classroom. But I’m glad I follow your blog anytime I need a fix (:

Nice post!

When I read about this in an article on the Gardener Gathering I assumed the probability was 1/4 of having two boys, just as it is if someone were to start a family tomorrow.

So, does it matter when the probability is calculated? Or does the statistical probability never change? My old logic book(by Irving Copi) says it depends on how much information you have. For instance, you might have a deck of playing cards with a 1/4 chance of drawing a spade. But what if you spotted the top card and noticed it was black? Without seeing if it was a club or spade Copi claims the probability goes up to 1/2.

I am not sure that that extra info is that important to the mathematics of probability. You might have seen the actual suit of the card too, and the probability would be 0 or 1. The whole idea of calculating probability is to have a method for figuring out variable events.

Once you state a set of arguments then change them in the middle of the problem you are setting yourself up for some of those famous paradoxes.

Martin Gardener in his “Colossal Book of Mathematics” tells one in the story of the three convicts on death row.

Anyway, I found this post very interesting. I loved the book on Euler too.

Thanks.

http://en.wikipedia.org/wiki/Monty_Hall_problem

When Marilyn vos Savant presented her variation of this problem back in 1990, it was not clear how much knowledge the game show host had. That does indeed make all the difference.

I agree with John Chase above not because he’s my son, but because I like Bayesian statistics. :-)

Right.

Let D1 be the distribution defined by all families with two children in which there is a boy born on Tuesday. Then given f1 in D1 the probability that f1 has two boys is 13/27.

On the other hand if D2 is the distribution defined by all families with two children for which there is a boy and for which the day of the week the children were born on is well-defined.. Then given f2 in D2, the probability that f2 has two boys is 1/3. Knowing the day of the week the boy was born on after drawing f2 is irrelevant.

In my opinion, defining the problem as taking a random sample from D1 takes the zest out of the problem. The popular appeal is the fact that it is not well-defined at all.

I see what you mean, I guess.

The zest of the problem, I think, comes from the fact that the problem may first suggest the distribution D2, when in fact the distribution is D1. It’s a hard problem, but the problem isn’t ambiguous, IMHO. I think it *is* pretty well-defined. The correct (though elusive) distribution is D1 and the correct answer is 13/27. Is that up for debate?

Here’s the on-line version of the question:

I have two children. One is a boy born on a Tuesday. What is the probability I have two boys?

But I’m going to make it so you can update your beliefs.

Let’s say that we have two children C1=(S1,D1) and C2=(S2,D2) where Si denotes Sex of child i and Di denotes Day child I was born {M,T,W,…,S,Su}. Si is determined by a fair coin. Di is determined by a fair 7-sided die.

Now, we are asked to give incremental updates of the probability that S1 and S2 are both boys.

Without any information, then P(S1=S2=B)= 1/4.

If I randomly select a child Ci and reveal Si, then the probability is updated as follows:

if Si = G then obviously P(S1=S2=B) = 0.

Otherwise if Si=B, then P(S1=S2=B) = 1/3.

Now if I reveal Di, can we update the probability that P(S1=S2=B)? Does it change from 1/3?

Lots of good comments. A pair of dialogues that might help to illustrate the way I’m thinking about the sampling:

Example 1:

I say: “I have two children.”

You say: “Is one of them a boy that has a SSN ending in 7453?”

I say: “Yes! (What a coincidence!)”

You and your friend begin placing bets on whether I have two boys. The appropriate odds given the information you have are *almost* (slightly less than) 1/2 to 1/2.

Example 2:

I say: “I have two children. One of them is a boy whose SSN ends in 7453.”

You and your friend begin placing bets on whether I have two boys. The appropriate odds are 1/3 to 2/3.

Ack, that was exactly the same as your first comment. Sorry for wasting space…

Yes, you can use Bayes’ Theorem to update the probability. The size of the sample space is now 196 – 49 = 147, since we now care about the day of birth (and we’re disallowing the 49 families that have two girls). Of those, there are 27 families with a boy born on Tuesday. So P(D2)=27/147. We’ll need that in the calculation. Here goes:

P(S1=S2=B | D2) = P(D2 | S1=S2=B) * P(S1=S2=B) / P(D2)

= (1/7 1/7 – 1/49) * (1/3) / (27/147)

= 13/27

Notice the use of the ‘prior probability’ P(S1=S2=B) = 1/3 in the calculation above. But now we’ve taken into account the new given information and ‘updated’ the probability.

I agree with your math but not your logic. Regardless of the day of birth, you’re going to change your answer to the same thing. So, something is obviously wrong. Can you tell me what it is?

@DavidC I think I’ve said what you summarized so nicely at least 6 times… But apparently it’s not sinking in. Thanks!

Yes, your right. The new probability is 13/27 regardless of what day you say the boy was born on. I just picked Tuesday (D2) to match the original problem. The application of Bayes’ Theorem allows us to update the old probability of 1/3 to the new probability of 13/27 upon the addition of the new information–that the boy was born on Di (whatever i may be). I know it seems crazy, since you might think ‘well, it’s gotta be one day or another, so why not just automatically update the probability to 13/27 before we even know the day’. I have to think about it some more too, but I think it’s just unintuitive, like the classic Monty Hall problem. Hmm… Need to think about it some more.

It’s very ambiguous to me. But there is no argument that 13/27 is the correct answer if sampling from D1. But I did learn something from this exercise, so thank you for your comments. Cheers! Pig

ThePigLA is correct to say that this problem is ambiguous. In fact all of the problems on the page are ambiguous, inclding the apparently simpler ‘I have two children One is a boy. What is the probaility I have two boys?’as Gardner himself had to concede. First, the Tuesday problem, if it is to be ambigious has to be of the form. ‘A man is selected at random from a sample of men with two children, one of which is a boy born on Tuesday’ if the solution is to be 13/27. I think The pigLA was moving towards. We need to differentiate between the condition and an observation after the sample is taken. You cannot use Bayes Theorem to jsutify the assumed conditional probability because it relies on this assumption for the conditional probability and the argument is therefore circular, However, the logical mess that John Chase has got into is because the sample space is not defined correctly and become confused with an observation.

One of the crucial considerations for all problems related to someone vulunteering statements such as ‘I have two children. One is a boy…’ is whether, he/she was compelled to report one boy if he/she ahd one boy and one girl. It is now generally accepted that unless it is the answer to a question, one half of those with a boy and a girl would say they had a boy and half would say they had a girl.This being the case the BB, BG, GB possibilities are not equally likely, BB would occur twice as often and BG and GB, so the correct solution is 1/2 rather than 1/3. (It might be argued in the case of a mathematics convention the sample is not random and we don’t actually know the probabiiity that a man offering this information would be as likely to report a girl as a boy)

If we look at the Tuesday boy problem in the same way, if the statement is not the outcome of a question formulated to assure that the person responding is a member of the sample set ‘For instance, ‘Do you have at least one boy born on a Tuesday?’. the anwer should also be 1/2.

You will find Bayes theorem confirms the answer so long as you make the a priori assumption that the person is equally likely to report a boy as a girl if he has one of each. (It doesn’t justify the assumption, for the reson given above)

The 13/27 is fascinating as is the generalises case 2-p/4-p, but we shouldn’t let our fascination override probability and sampling theory.

Sorry, amongst the many typing errors above, the statement ‘The Tuesday problem, if it is to be ambiguous..’ in the first paragraph, should, f course, read ‘if it is to be unambiguous..

Thanks for your comments, Limey. I realize this is more complicated than I initially thought and sampling may be an issue. But I’m still a bit confused.

Are you saying this?: If I was to ask a randomly selected person with two children if they had at least one boy, and s/he said yes, then the probability s/he has two boys is 1/3? That is, if we directly question the person, that makes the difference (rather than the person volunteering the info). Is that what you’re saying? Because that seems like a pretty similar and straightforward interpretation of the classic problem.

I’m not sure I buy the whole ‘if the person volunteers the info then it’s more likely that s/he has two boys’. It seems that if a person volunteers the info, BG, GB, and BB are all still equally likely. Can you clarify some more?

Yes, that is more ot less the case. I ideally we need to specify the sample space correctly. If we say, a parent is selected at random from a set of parents with at least one boy’, then we have removed the ambiguity. The reason the ambiguity is removed is that the original form could mean: I sample parents with two children who select a child and tell me the sex, or it could mean, I sample parents with two children who must tell me whether they have a boy. If we take the first case, why would they ncessarily say they have a boy if they have a boy and a girl? On average, about half would say a boy and half would say a girl. This would mean that if we sampled 160 people around 40 would have two boys, around 80 would have a boy and girl and 40 would have two girls. Of the 120, that had a boy, 40 would have tw boys and say they had a boy, of the 80 that had a boy and a girl, around 40 would say they had a boy and 40 would say they had a girl. So, for all of statements ‘I have two children, one of which is a boy’40 would have two boys, and 40 would have one boy and p=1/2. The only way we can get the 1/3 answer is to try to ensure that all families with a boy and girl report that they have a boy, by, for instance, asking them ‘Do you have at least one boy?’ and assuming that they answer truthfully.

Mathematicians have traditionally got over the problem of how you find out by using constructions such as : ‘Given that a parent has two children one of which is a boy what is the probability he/she has two boys?’ This could be OK for puzzlers but statisticians don’t like this construction because the way we find the information is crucial.

Unfortunately, for Gardner, as he tried to liven up the problem he introduced a way of finding out the information. (Originally it was a Mr Smith who reported that he had two chldren one of which was a boy). He later admitted that by introducing the story he had created the ambiguity I describe above. Other mathematicians, such as K Devlin have not fared any better in leaping to the conclusion that the 13/27 solution was correct and have had to retract, once aware of the ambiguity in the problem.

Why I say ‘more or less’ for the question approach is that it still depends on setting up an intial hypotheses and conditions before the question ia asked. So, to get the 13/27 solution, we have to agree that we are sampling a set of parents who have two children at least one of which is a boy born on a Tuesday, and then ask individuals the question. If the answer is no we ignore them. If yes, we can calculate that the probability they have two boys is 13/27. It is easier to see why the answer is greater than 1/3 but not 1/2 when you then consider the restricted sample set we are dealing with.

I think this view of the problem is pretty much the consensus view amongst statisticians and probability theorists, but there are some who would say that for the probelm as it is stated we do not know the probability that the man would say he had a boy if he had a boy and a girl, because we don’t know enough about the sample set from which this individual is selected. Their view would therefore say the problem is ill-defined and no solution is valid.

Thanks, Limey! I think your post really clears the issue up. The thing that hasn’t been said here is that volunteering of the info is crucial. And that’s a new thought to me!

I’m way late to the game, but as somebody who doesn’t have a degree in math, let alone a specialty in probability, here’s my $.02.

Assuming there’s nothing special about Tuesdays and that boys are equally likely to be born on any day of the week, then the day specified in the problem is irrelevant; the answer will be the same whether the boy was born on Tuesday, Wednesday, or one of the other 5 days of the week. The answer would also be the same if the problem specified girls instead of boys

Doesn’t that mean we’ve got a bunch of people suggesting that out of 27 children there will be 13 boys and 13 girls?