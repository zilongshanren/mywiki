---
title: A bad, but interesting, exam question
url: https://divisbyzero.com/2018/12/21/a-bad-but-interesting-exam-question/
author: Dave Richeson
published: '2018-12-21'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Every teacher has had the experience of writing a seemingly straightforward exam question only to realize when grading the exam that some of the students misunderstood the intent of the question. Oh, to be able to turn back the clock and to rewrite the question! That happened to me this semester, and the variety of answers were interesting.

In the logic section of my Discrete Mathematics class (our “intro-to-proofs” class), the students learned about the converse of a conditional statement: the converse of “if A, then B” is “if B, then A.” Most notably, a conditional statement is not logically equivalent to its converse. “If I am over six feet tall, then I am over five feet tall” is a true statement (in my case, the hypothesis is false and the conclusion is true). But the converse, “If I am over five feet tall, then I am over six feet tall” is false.

On my exam, I had a page with the following instructions and the following problem:

*For each of the following problems, determine if such an example exists. If not, state IMPOSSIBLE and give a brief explanation. If so, give an explicit example that satisfies the conditions.*

*A statement that begins “If x≥1, then . . .” and its converse such that the statement is***true**and its converse is**false**.

The answer that I was looking for was something like:

(True) statement: If *x*≥1, then *x*≥0.

(False) converse: If *x*≥0, then *x*≥1.

I class we had discussed that typically when you encounter a conditional like “if *x*≥1, then *x*≥0″ in mathematics, there is an implied universal quantifier. So, mentally, we read it as “for all real numbers *x*, if *x*≥1, then *x*≥0.” My first statement (if *x*≥1, then *x*≥0) is definitely true for all *x*, but the second statement (if *x*≥0, then *x*≥1) is not true for all *x* (for instance, it is not true when *x=*0).

Not everyone answered in this way. Interestingly, I discovered that it was not the case that the more prepared the student, the more likely she or he would get the problem correct (my intended answer). Here’s what I mean:

**Least prepared student:**This student might get it totally wrong, leave the problem blank, not know what the converse of an if-then statement is, and so on.**More prepared:**If a student knew what a converse is, then she or he might get the problem correct without realizing that there were any subtleties.**Yet more prepared:**In class, we talked about the fact that we can only assign truth values to statements. If there is a variable in a sentence, then it is not a statement (it is a predicate). For instance, “the integer*n*is even” is not a statement. It is not true or false unless we know the value of*n*. So, some students wrote on my exam that it was IMPOSSIBLE to solve because we don’t know the value of*x—*it is a predicate, not a statement*.*This was not the answer I was looking for, but I gave them full credit because they were, technically speaking, correct. (In a sense, their answer was more correct than my intended answer.)**Most prepared:**These students would have understood the previous argument, but would also have recalled our discussion of the implied universal quantifier and would have remembered that we had homework problems on this, and thus they would have given the answer I was looking for.

Interestingly, students (2) and (4) may have given the same answer on the paper. But because I know these students and because I saw how they did with the rest of their exam, I honestly suspect (2) and (4) are two different groups. In other words, many of the strongest students in the class got my desired answer and many of the students who struggled elsewhere on the exam got this problem correct. On the other hand, some very strong students fell into category (3).

All-in-all, I wish I’d not asked this question. I ended up giving almost all of the students full credit on the problem, whether they got they got an answer that I had intended to be “the right answer” (i.e., students (2) or (4)) or the more technically correct answer that I did not have in mind (3). But I’m upset that I gave this problem that could be equally interpreted in two different ways.

It seems it was ‘not perfectly’ proposed, as you may frase it, as it allowed for certain ambiguous interpretation, but the outcomes seemed far more interesting than if the – even unintentional ambiguity – wasn’t there. After all, it ended up in an even more technically speaking (sic) correct phrasing, and even allowed further insight into the stratification of your students. It seemed a cool accidental outcome to me!