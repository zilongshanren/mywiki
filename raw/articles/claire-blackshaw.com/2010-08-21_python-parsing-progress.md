---
title: Python Parsing Progress
url: https://claire-blackshaw.com/blog/2010/08/python-parsing-progress/
author: Claire Blackshaw
published: '2010-08-21'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Python Parsing Progress](../../assets/be0f628d95e13e77.jpg)

Tavern Talk

Okay it doesn't look like much but there is a LOT of back-end going into this. With some good work but tonight I should be able to parse the scene script.
Still haven't solved my combination problem for the [Gaussian Probability Sets](http://math.stackexchange.com/questions/2584/combine-n-normal-distribution-probability-sets-in-a-limited-float-range). I have the question up on [Math StackExchange](http://math.stackexchange.com/questions/2584/combine-n-normal-distribution-probability-sets-in-a-limited-float-range).

So onwards to the generators!

c:\Dev\DDD-Snake>testbed.py ~~ Defined Key {SEVERAL:[ 4 : 8 ]} ~~ Done Cleaning and Building Define List ~~ Done Parsing Location data Status [Gender] Enum : Male(50%) Female(50%) Status [Job] Enum : Barman(25%) Miner(25%) Gaurd(25%) Functionary(25%) Status [Height] NumRange [1.2:2.4] Status [Nation] Enum : Red(83%) Green(8%) Blue(8%) Status [HairColour] Enum : Red(16%) Ginger(16%) Strawberry Blond(16%) Blond(16%) Brunette(16%) Black(16%) Status [HairStyle] Enum : Bald(12%) Shaved(12%) Short(12%) Curly(12%) Shoulder Length(12%) Long(12%) Braided(12%) Braids(12%) Modifier Gender[X ] HairStyle : 20% 20% 20% 20% 20% 0% 0% 0% Height : 1.9 ~ 0.4 Modifier Gender[ X] Job : 0% 0% 0% 100% HairStyle : 0% 0% 16% 16% 16% 16% 16% 16% Height : 1.7 ~ 0.3 Modifier Job[XXX ] Gender : 100% 0% Modifier Job[ X ] HairStyle : 33% 33% 33% 0% 0% 0% 0% 0% Modifier Job[ X ] Nation : 100% 0% 0% Modifier Nation[X ] HairColour : 80% 12% 3% 3% 2% 0% Height : 1.7 ~ 0.2 Mutator "Tall" Height : 2.1 ~ 0.2 ~~ Done Parsing People data Status [GlassFill] NumRange [0.0:1.0] Status [DrinkType] Enum : Beer(25%) Wine(25%) Water(25%) Milk(25%) Status [DieFace] Enum : 1(16%) 2(16%) 3(16%) 4(16%) 5(16%) 6(16%) TODO :: Parse Prop Template --> ['Dice', ['DieFace']] TODO :: Parse Prop Template --> ['Drink', ['DrinkType, GlassFill']] ~~ Done Parsing Prop data ______ TODO :: PARSE VERBS _______ VERB Cleaning REQUIRES PROP VERB Dicing REQUIRES Dice VERB Drinking REQUIRES Drink ~~ Done Parsing Verb data Done parsing dictionary.txt -----------------------------