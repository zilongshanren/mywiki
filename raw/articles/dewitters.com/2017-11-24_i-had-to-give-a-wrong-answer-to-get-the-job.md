---
title: I had to give a wrong answer to get the job
url: https://dewitters.com/i-had-to-give-a-wrong-answer-to-get-the-job/
published: '2017-11-24'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

Back in 2007, I was searching for a software developer job at various companies. At one of these companies, the best strategy to get the job was to give a wrong answer. If this seems weird to you, let me explain what happened.

When I arrived at the interview, there were 2 other guys present. One would be my direct team lead, which was also the technical lead, and the other was his manager. It was the team lead that drove the conversation and asked the questions.

So after some small-talk, and answering the usual generic questions, I was asked to explain what a “three-tier architecture” is.

I gave a generic client-server-database explanation. I also referred to the most common business case with a web browser as thin-client, a web application server, and at the bottom layer a database. They seemed to be satisfied with my answer.

Then they moved on to a follow up question: “How does this architecture relate to the model-view-controller pattern?”.

I knew this question was really tricky, because I know a lot of people make the mistake of directly linking the tiers to each of the model-view-controller. But in reality, the model-view-controller runs on the middle “application” tier, in most cases.

If you don’t believe me, take a look at what was on Wikipedia for the n-tier architecture:

At first glance, the three tiers may seem similar to the MVC (Model View Controller) concept; however, topologically they are different. A fundamental rule in a three-tier architecture is the client tier never communicates directly with the data tier; in a three-tier model all communication must pass through the middleware tier. Conceptually the three-tier architecture is linear. However, the MVC architecture is triangular: the View sends updates to the Controller, the Controller updates the Model, and the View gets updated directly from the Model.


So the question was not only what the right answer was, but also what they thought would be the right answer. Did they know about this, and wanted to see how far my knowledge goes? Or didn’t they know?

Normally, I would have given the correct answer, and have a nice discussion if they considered it wrong.

But the problem was, that this guys manager was sitting next to him. If he didn’t know, I would totally humiliate him in front of his boss. So either he would stick to his guns and refuse the correctness of my answer, to save face. Or he needed to agree that he was wrong, and lose face. Anyway, there was only 1 proper solution to this: I had to answer what they thought was correct.

So I decided to start by giving the correct answer, and see how he responded. I explained “The model-view-controller is a software pattern, and so resides inside the written code. Since in most cases, this code only runs on the application tier, …”. But then I saw him frowning, and so knew this was not the answer the was expecting. So I continued: “The view corresponds to the presentation layer, the controller with the application layer, and the model with the database layer”. Done! Good answer! Everyone was pleased, and I got the job.

The moral of the story? Job interviews are not all about your technical skills, it’s about people skills too. And this is good, because you need both in your job.

## 8 Comments

## CTGD · June 23, 2018 at 18:37

Yup, good idea, seeing reaction and working off of his reaction to get the ‘right answer’.

## gin · April 16, 2021 at 07:38

YES, the only rule that counts is never outshine your boss.

## Vis Itor · July 19, 2021 at 07:04

Unfortunately this was not a good example of, “people skills”. Having to provide a false answer is not good people skills.

What could have been done better? Over-communicate.

Tell them your thought process as you have told us.

You could say something like, “It is commonly said that the view corresponds to the presentation layer, the controller with the application layer, and the model with the database layer. However, this is a common misconception. My reference is book X or my reference is this Wiki article which describes it as: ‘The model-view-controller is a software pattern, and so resides inside the written code. Since in most cases, this code only runs on the application tier…’. Perhaps one could make a case that either definitions are correct…

But I prefer the Wiki definition.”

They didn’t require lying or diminishing your knowledge. It didn’t require any BS to get the job.

Over communicating is a good people skills.

## SZ · September 10, 2021 at 09:27

I like your response in this situation, clear and leave the potential to discuss with different understandings

## James · July 19, 2021 at 11:44

I have a very fond memory of answering “What is the TCP handshake?” with an explanation of TLS instead, because I misheard them (I was doing the phone screen from a coffee shop).

They were an engineering manager and expressed that they were impressed that I answered with the far more technically challenging answer, but I didn’t move forward for other reasons.

## Hawad · July 19, 2021 at 17:43

Indeed. Some situations can be of this kind. But what about people who adhere to the duty of being truthful and sincere?

## Scott · July 20, 2021 at 07:28

That’s funny! I would have noticed the frowning, said the right answer anyway, and basically be ready to decline the offer if it turned out that the lead couldn’t admit they were wrong or learn something new they didn’t know.

## Jay · July 20, 2021 at 07:56

A successful lie is not “skillful communication”, it’s just deception. Please don’t consider yourself “skillful” because you turned a frown upside down with a lie.

I agree with Vis Itor’s comment, you could have covered both possible answers and indicated your preference without humiliating anyone. There’s many ways to provide a good answer. You are not in school providing true or false answers to the teacher.

It doesn’t sound like the sort of question the whole interview hinged on. There’s never one question that everything hinges on. Have some self respect and speak the truth next time. And BTW, when someone frowns it doesn’t always mean what you think it means. Some people frown when thinking for example. I’m frowning right now at the concept of “people skills’ being tied to some egg-shell treading untruth interview strategy.