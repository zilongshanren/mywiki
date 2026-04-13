---
title: AWS->Playfab->Gamesparks->Firebase long story
url: https://gametorrahod.com/aws-playfab-gamesparks-firebase-long-story/
author: Sirawat Pitaksarit
published: '2017-08-08'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/cab98552ff9f6146.png)

I journey through various cloud service for making a backend for my game. Here I log the experience why I ended up on Firebase currently and what is the pain point or deal breaker point of each.

I hope others deciding can learn, or even employee from these company can know their own pain point for some user like me.

***2019 update at the bottom**

## My requirement

- I am making a Unity game. All of them claims “Unity integration”
- Not an online game. Just need a database for scoreboard and storage for some dynamic image downloading + save backup (I don’t use Google Play and iCloud ones for more control). Nothing fancy!
- You can choose to go online or not. When online you must register an ID and your in-device save will pair with it.
- All items are stored in the save file to allow full offline operation. In the database contains that entire save file’s backup. The game has no IAP virtual currency.

## AWS

- Have been with AWS for 2–3 years. The reason is it seems to be an industry standard worth learning so I choose it. Devs in my country talk about it a lot too. I want to join in and be able to say “I have used AWS!”.
- The first year was free, and from that point onwards I paid about 5–10$ per month. I use it only to serve a small asset to the game for each players.
- Old interface. A bit painful to use. S3’s UI has been modernized recently. I hope it follows in other area.
- Very detailed IAM system. Almost too much for my use but I have no choice but to go through it. The rule is difficult to write and I encountered many unexpected error. Like with Put and Get you need * at the end to apply to all files while List you have to remove it to target a directory. And it is difficult to know what policies are required for thing you want to use. If you missed just a part of them, it will fall apart at one point. (Like going to S3 and don’t see some component load up, but some load up) This makes a very “secure and detailed” IAM system actually “scary and fragile” because of my own error of setting them up.
- The ARN system is difficult to get it right. The examples are scattered all over in each service. Many examples is not comprehensive enough and I must still do trial and error. It would be helpful if the UI can just generate the correct ones for you for many service endpoint.
- There are very confusing terms in the user management area. You have AWS Cognito (The general term for everything), Cognito Sync (Sync file and store in the user’s storage), Federated Identities (Another screen that somewhat links with user pool but with login from other sources), Cognito User Pool (It is AWS hosted user) Your User Pool (Former name of Cognito User Pool?). They looks separated but actually loosely interoperating with each other. Moreover some of them have region so if you select a wrong region it disappears. I must iterate through all the region one by one if I forgot which region I set it up long time ago.
- The thing with AWS that I hate is that it slices things up in the smallest possible way like this for flexibility, but it puts workload on the developer. Instead of using cloud service to be able to focus on game I must still do work. (That is of course less painful than buying my own servers) This appeals to some customer but definitely not me.
- Pricing is very detailed that it is sometimes difficult and scary to begin.
- C# .NET interface is painful to use. It uses callback pattern. Error is not obvious and there are many point that can trip you. (Wrong region? Wrong region code? Correct region but actually the credential service is in different region?)
- C# .NET online documentation is a nightmare!! Impossible to search for what you
**want to do.**(It just auto generated from the code, really) - Human readable document is a bit difficult.
- Route 53 is one thing I like. I switched from Hostgator and still be with AWS on this one. More expensive, but I love being able to access and create all the records I want easily.
- I host my static websites on S3. The command line aws s3 sync is super useful. In a flash I could update my website anytime. This is great, that’s why I am also still with AWS for my game sites.

Several years later I am starting out a new game. I think this is a good opportunity to journey and learn new things so I searched for a new solution. If nothing is better I would come back to AWS.

Note that I know a bit about Firebase before meeting with PlayFab and GameSparks. You might see I mentioning Firebase in their respective sections.

## PlayFab

- Did not actually use it myself. Know this from a part-time job I work for. I am allowed to access their game’s PlayFab console.
- Very optimized for game and made many assumptions for your game, which is the point I don’t like. It has the clearly named “Player” and each player has “Inventory” which must be granted items from “Catalog” and so on. There are “Leaderboard” with various functions so you don’t have to make your own database. A system for logging into each other with social IDs, etc.
- Seems good? I think the “prepared template” is a bit too much for me. (Many will be left unused)
- About the pricing. I don’t like them that the pricing is not transparent. In the homepage they are clearly trying to hide many details and just said Free. Free is not actually free because if you manage to come
**deep**to the console (Settings > Limits) you can see limits on each every possible details that it gave me headache (like request/sec, items created, etc.) which on**each**you can pay to extend the limit. (This looks a lot like IAP character upgrade in games.) You can’t see this before committing yourself to the service and it is a bit scary, so I set off to search for other alternatives. - Cloud script “automation” is one big file!
- All of these evaluations happen in 2 weeks.

## GameSparks

- I like them for offering “pay on success” plan for indies with 1–3 man on the team. That’s totally me and they understand me.
- I signed up and take a look. Things are less prepared than PlayFab and I love that. There is a leaderboard, social logins, currencies, etc. for games like PlayFab. But no inventory and players. They are all a database. This looks like a good level of abstraction for me.
- There is no inbetween of evaluation package and enterprise package? If I have 4 man on the team I am already an enterprise? This point is confusing.
- In the NoSQL there are many “magic” database that appears without my knowledge. Searching for their meaning and structure in the docs does not help me other than what “System” and “Runtime” is. (I realized “player” is probably hardwired to many things, but in what way exactly?)
- I started hesitating after trying to get start and search for how to do things in their tutorial. Their tutorial is not categorized in a good way. Just up to “Database Access and Cloud Storage” is good, then after that it looks chaotic. I am unable to generate a “graph” in my head I usually have when reading Google’s tutorial.
- I am just searching for how to put a file to server to be able to download again and already lost. A lot of options, scriptData? collections? asset? I get their intention of providing options, but I am a person who rather have a black space to just put things in and get things out. This is not appealing for me.
- When I learned that to upload I must request a URL and use a manual HTTP get to get the file from that URL, while seems normal I think is a bit too much work.
- It is very customizable. You can actually edit “what happen when” of each services to the core with Javascript. Which I think is too much! It also put risk on me, it might require me to script many things to get it to work…
- This is where I realized something. Service like PlayFab and GameSparks seems to be optimized for games and help me go faster because I am making games at first, but actually, a “just blank canvas” service like Firebase turns out to help me more. Less setup. Less learning. Less frustrations.
- Just a bit after I search for how to persist the login, an answer is to hijack the login script and put JWT in there.
- And also when forgetting the password how to allows player to request a password forget e-mail? Searching for this results in a very
[scary looking](https://docs.gamesparks.com/tutorials/social-authentication-and-player-profile/automating-user-password-change.html)doc. It looks almost like I am writing the whole process from scratch! - The e-mail service is partnered with SendGrid. (discovered later deep in the docs) I look at their website and I don’t want to calculate for costs. Firebase has this for free. Also there are more scripts I have to write.
- They have a Unity dynamic C# code generator for making a compilable code to call to your own functions. (Instead of cloud script keys of PlayFab) This sounds like fun, but I haven’t got to that point yet.
- It is difficult to comment.. but I think my switch is almost entirely on their documentation. There are many to take in, but the doc itself didn’t “grab your hand and take you along” in a nice way.
- I realized GameSparks actually is about at AWS level of manual customization! (the same difficulty with less jigsaw pieces) And that’s not nice!
- All of these evaluations happen in 3 days.

## Firebase

- To sums up everything is
**just right.** - Pricing is the most clear of all services I have used. I can see everything in that page. I have confidence.
- Usually when comparing its pricing vs. feature. In the classic 3 column sale page of every service including Firebase it is this. But if you try out each service for real you will realize the 3rd hidden parameter that is
**usability.**It is the**happiness of a developer, not your players.**This is very important, as I mainly seek happiness in my life so why not? - Firebase seems like a bad deal if you look at just pricing and feature then compare to others, but in almost every other area Firebase give me the most happiness. Working with Firebase is friction-free. The main strength of Firebase is this. It is hard to evaluate and hard to advertise because you must put some time into each service to realize how “smooth” it is. (Not the “smooth” in connection speed, etc.)
- The plans are interesting that the middle one is not necessary a middle-powered plan. Every plan has its strength. Fixed plan is very interesting. You have no fear of price growing at all. But for me I am using the scaling plan as my use is currenly much less than the fixed plan.
- The grouping of their “things” that you need to wrap your head around is just right. And the docs are grouped accordingly. It’s just database, authentication and storage for me.
- Tutorial document is actually
**fun**to read. Every topic get its point across to me. It is ordered nicely that it almost feel like playing game and passing stage by stage reading the document. - Going into each page, I can’t believe how minimal the UI is. I thought something must be missing but it is not. Firebase nails this point. Everything is simplest AND the most flexible. Where in other services it is either the most flexible or simplest.
- The details are hidden in Google Cloud Platform, which you can adjust things like your storage’s region.
- The database rule is powerful. And their Bolt compiler helps writing them fun and reduce error. It is easy to take account for which user can do what by doing path check with the UID. In AWS making an IAM is not as fun as this. Also the idea that just this rule controls everything is appealing for me. No more switching pages like in AWS.
- The database rule simulator helps me a ton. I just put the JSON that does not goes through in the game here and it highlights the line that invalidate it. In AWS, I can never know what’s wrong…
- API Documentation looks nice. A whole lot better than AWS’s. There are texts that looks like some human written it for me to read.
- When I set Firebase up, their firebase-tool have very nice walkthrough. When I use it in Unity, the approach of downloading a config file vs. copying various strings in AWS already said a lot to their
**usability**. - C# API is a joy to use!! I like a lot how they use Task for their async ops. No one have wrote the API this neatly before. And how you use .Child to navigate the database? How you just call .SignIn__ to sign in and it just works? These things impressed me as they show up in the intellisense. Because other company does not get this right.
- Blank NoSQL database is great. With simple rules that I took few minutes to write, I can have inventory, leaderboards, etc. that other services “assumed” for. Unlike other services, I have the understanding more in Firebase. Like I said before, blank canvas does not equal more work. Prepared environments in PlayFab, GameSparks actually result in more work for me. In learning, in error fixing, etc. Using Firebase is just a database. What you learned will translate to all the things in the database domain, resulting in more techniques.
- The real time database admin page really updates in real time. That’s a surprise. In PlayFab I need to refresh to see player’s updated data, for example. It’s great for testing your game.
- Firebase is with Google so it is kind of an industry standard, more than game-specific ones like PlayFab and GameSparks. The feeling is like with AWS, maybe if I learn it I could use it to land a job in the future.
- Free analytics, free e-mail sending service. Unlike Unity Analytics, your data is not locked out by the pro plan. I don’t know how will this compare with AWS mobile analytics, but I will use the Firebase ones to see this.
- The admin screen is the most
**clean**of all competitors. You might think it is just a little thing… but I think it means a lot for me. - Their beta Cloud Functions is so cool. (It’s equivalent of AWS Lambda, PlayFab Cloud Script, etc.) You sync JS file from your project! No need to use the editor in the web. And that sync folder is in a node environment! You can have all the node packages you want to use! It’s a web app after all, so this is very exciting and sounds like a lot of possibility + the less setup possible because NPM and node handle all the things.

That’s why I am currently with Firebase. Firebase loses in every point on the surface until I try it and realize their wonderful details. Usability doesn’t sell, but it’s very important! Developers!

## 2019 Update

A lot happened since the post date back in 2017. I won't go back and fix what I written. Instead I will add them here what I think of things now.

GameSparks is now with Amazon with no free tier allowed in production, and the first one is a massive 300$ per month AND $0.008 after first 37,375 MAU, per MAU. I have no other info as it looked too expensive for me. There is [a discussion](https://forum.unity.com/threads/heads-up-gamesparks-changed-their-pricing-plan-and-its-looking-bad-for-indies.632257/) in Unity forum.

Playfab is now Microsoft Azure Playfab with a nice free Essential tier with unlimited MAU, but still with [Limits](https://blog.playfab.com/blog/introducing-our-new-usage-limits-system/) that is only viewable when in your project, not in the tier pricing page, like I explained back in 2017. I like Playfab out of the bunch of non-Firebase solution, so let's reduce it to just Playfab vs Firebase from now on.

### Limits

For example, I take some out for you to see :

![](../../assets/855362bca6bea8cb.png)

And inside each one, there is a potential that you have to pay even if you are in Essential tier. (Or in Indie tier, but want more that the limits) For example, there is a limit of 25 leaderboards or else 20$ per 100,000 MAU to get 100. You cannot get more boards per less MAU.

![](../../assets/4b1eb7cbbb5febe5.png)

So when I see this I am a bit conflicted. I want to use the Essential tier, and my game would never made it that big to 100,000 MAU, but some games see this 25 number of boards a bit too low. (For example you made a Candy Crush clone with 50 stages, with scoreboard for each stage.) I get it that it is meant for a game like endless runner, where there maybe only one or two weekly scoreboard globally that resets. If you have a game with a lot of boards, then you may need an alternate strategy. But you will introduce some SDK fatigue if your user data is staying in Playfab, your analytics in Firebase, and leaderboard in somewhere else, for example. As far as I know, Indie tier of 100$ per month does not remove these hidden limits, but rather add more [professional features](https://playfab.com/pricing/#desktop-pricing_details_professional).

Some like 8 virtual currencies is more than enough, you may have only gold and gems. Some like 100 items in an inventory is questionable, it depends on game's genre as well. You may have some workaround with more than 100 items in an actual save file, but less than 100 for "cloud items" that uses Playfab's inventory. If your game fit with this then good! If not, you have to weight your workaround cost vs. going with Firebase and build things from scratch.

There are "wholesale" aspects in Playfab while in Firebase it is extremely granular. This is an expected consequence of Playfab's level of abstraction. (Though they have a separated granularly-paid CDN for file hosting) I found that you need to be a bit well-off to be able to accommodate free-to-paid jumps in Playfab. (i.e. view 100$ per month as inconsequential and not a life or death decision) While in Firebase you truly pay what you use but you have fewer pre-made connections. Playfab has to do this to keep up their awesome free tier running, I understand that too.

### Authentication

I am a big fan of anonymous sign in, where your user don't even know they have their own account created. This way no backend service has to be opened to public because everyone stays in signed in state automatically. Then later you can ask him/her to link with e-mail password to allow save restore, etc. Both Playfab and Firebase could do this.

One thing I like on Playfab is their frictionless sign up **with device ID** (Android / iOS). So when onboarding then you could create an account that automatically logs in by player's device ID. Then later link to a permanent account. It is explicit.

In Firebase, they have anonymous sign in for the same purpose, but it is not completely the same thing as each call to this API returns a completely new user (new UID, new account generated) each time even on the same device and even when the user didn't reinstall the app. (Inside, who knows they might be using device ID too.)

But there are subtleties the docs didn't tell you ( `SignInAnonymously`

now will be called SIA) :

- If you SIA again after SIA from signed out (blank) state, you don't get a new UID and I think it equals to nothing happened.
- If you SIA after sign in with non-anonymous (like e-mail password) way, then you generated a new UID.
- If you signed out from SIA, then sign in with SIA again, you generate a new UID.
- But the gotcha is that,
**the signed in state magically persists**to the next run of your game. (Even without internet connection,`FirebaseAuth.CurrentUser`

magically exists but you cannot use it) And so if you SIA into a generated UID, you**must not call sign out**and so the next time user start the game they are still with the same anonymous account. There is no way to normally sign in to this account again if you sign out, SIA will go to a new fresh account. The only way forward is "linking" to the e-mail password when the user wants to commit to your game later. - The magic anonymous persistent doesn't survive app reinstall. BUT it survives app replace, which I tested this on Android with
`adb install -r my.apk`

. Therefore I think it will also survive app updates.

So you could use it the same way to onboard players like Playfab, just that it is not as explicit as using a device ID to sign in, that should survive across app install since the device didn't change. Also it may looks like Playfab device ID will be able to survive app reinstall, but they said [that is not the case on iOS](https://api.playfab.com/docs/tutorials/landing-players/best-login) for some reason that I didn't try to understand.

### The blankness of Firebase

There are still difficulties in the "blank page" approach in Firebase as compared to Playfab. For example there is nothing connect the player auth information to the Firestore where your score may resides in at all, other than your defined Firestore rules that interwoven with auth by the UID, and maybe some checks here and there in the Firebase Functions. How to implement virtual currency which only allows the server to modify it (e.g. gems) like Playfab? Maybe you create some Firestore "documents" for user with a field called gems, and maybe name the document as UID or has a UID field to use with the rule. Will that work? Yes. But you came up with this **by yourself**. There is no implication of anything "games" in Firebase. While in Playfab, all developers will be hardwired the same way about a virtual currency. The same for scoreboard resets, timed awards, inventories, transactions, inter-account item tradings, etc.

The thing is, **you may feel vulnerable **even though you managed to code up a scoreboard out of these 3 pieces. So things like weekly resets, or higher-override-previous logic is working as expected. Then when everything intermingles with later added friends and rival list system, where if player's friend removed him he would have to stop seeing his friend's score, you may already be burned out.

But Playfab's Indie tier 100$ per month is no small money however with you tried multiplying it by 12. Or even Essential with some "limit breaks" may cost you 20$-50$ per month. It is up to you to weight this and could you afford it.

Even if you could afford it, don't forget Firebase's flexibility to do something truly unique. Playfab (and any BaaS) is often advertised as to future proof the game to be scalable in the case that the game "breaks out".

However for example what if in the future you want a mode which the scoreboard stores top 3 best of each user's attempts to do something, like an average of all? In Playfab scoreboard you see options like newest override, or highest override, and now this limits your options. While in Firebase, it is just a Firestore documents! You can do whatever you want... This is "scale" in an another sense, in flexibility/agile more than expanding.

You made a game with 1000 leaderboards for some reason? e.g. imagine a Candy Crush Saga clone, with just 100 stages, but each stage has its own board and you happen to have Easy/Normal/Hard of each with a separated board AND male/female separated boards for some reason, AND separated boards by country (let this be just 20 countries). Then it will be 100 * 3 * 2 * 20 = 12000 boards! In Firebase Cloud Firestore, no problem. In Playfab, you see it is way over their 500 boards limit of 50$ per month limit break plan. Yeah I know no games actually do this, but just an example because I don't underestimate game developer's creativity. Playfab's soft limit may ended up blocking your success. (Or steer your game into success by forcing you to play their rule, it's up to your view.)

Let me slip in one more example red hot from my own game design. I have a scoreboard, however one score entry happen to contains 2 numbers! Imagine a Flappy Bird score, normally you may think a number of pipes passed. But I am adding "critical pass" count that only increases when you tap jump once and passed the whole width of the pipe so I could differentiate pro players from regular players. I don't want to merge these 2 scores and allow anyone to view the score sorted by normal score or by critical pass count as they wished, and also if there is a tie of normal score in the case of viewing normal-sorted scores, the tie is broken by whoever has higher critical pass score before looking at timestamp if that is still equal. So I can't really merge the two!

With Firebase, this is no problem and you can even tell Firestore to index it as you see fit. Playfab assumed a common scoreboard and this concept is now alien to them. You must now play their rule by having 2 scoreboards of normal score and criticall pass score. Both works, but which one do you prefer?

In summary :

- You can say Playfab is more flexible than Firebase, because it scales well and if your game breaks out it will perform just fine like before.
- You can say Firebase is more flexible than Playfab, because in the future you have your own requirement that is not fit for Playfab's wired functionalities.

### Cost control

With Cloud Firestore, you have to be in a certain mindset to play with it. It is like Google saying "This is how our database works the most efficiently, we don't care how you use it. If you don't conform to it in your leaderboard implementation and get massive cost from us, get recked lol".

And you have to come up with strategies like data duplication or linearizing your documents (less problem with the new collection group query added in mid 2019), so to minimize read count as much as possible.

You have to master the rule of Firestore to get the most optimal cost for games generally because Firebase is not for only games, and especially tune it for **your **game. For example generally you might have an idea (after learning where the cost from Firestore came from) to duplicate player avatar from player's profile onto on every scoreboard entries, so whoever reads that document don't have to spend one more document read to display the player's avatar. This of course cause some complication when player updates their avatar and then must ripple update all scores in existence, which costs money because Firebase's cost is granular. BUT if your game don't have an avatar? None of these matters anymore and you can save even more that other games. Firebase is great in this kind of cost control because every little things you do costs money.

While in Playfab you don't see this and instead get the most optimal implementation (from Playfab side, that won't burn their server) and get a summarized wholesale prize (that Playfab think is fair to you, and also made them income). Firebase has their rules that they are sure can handle, you are free to abuse it and pay for it accordingly. In an another perspective using Playfab spare you from thinking about this details and may save you time instead. (Or save you from risks of costing more than you should)

### Web hosting : nice addition

Firebase has a web hosting which seemingly unrelated to games at first. It is for those who build a web app and then the web will be an entrance for user to use Functions then that access Auth and Firestore.

But then I realize my game probably need a (simple) website for advertisement, and this is perfect as it is in the same place and the cost is totalled together with your game. The `firebase init`

tool I will talk about soon is fantastic to setup the web project and local web server and live reloading is instantly available.

And then this website is magical because it could access other Firebase service without domain restriction. (CORS) What if I have already backed up my user's save file to Firestore? Now I can make a web login system that shows his progress online, even though it is a mobile game!

`firebase init`

: still insane

Firebase has a top-notch command line tools, this one is no doubt. While most services are trying very hard at their web interface to allow more "business" person to be able to make games together with programmers, the true power lies in command line tools and no one beat Firebase so far.

Why, command line embody the user's computer. User's computer is like his limb and feels familliar, even though to your mom the black terminal screen may not be so pleasing to use. Magic happens in each of `firebase`

command. But the most importantly it allows you to **work from folder. **`firebase init`

make a nice structure of folder with interactive QA to setup your project. The `.gitignore`

is there and correct. It uses a modern Node environment so an entire world is now your toolbox (`npm`

).

I was the most surprised at the tool's local emulation functions.

Suddenly, all your server side code could be tested locally. Now you can write out all the scenario that worries you ("1000 users registered at the same time concurrently, will my sequential random ID logic distribute the same thing to someone?", "If player submit a score and it is not a new record, will the timestamp errornously bump?") and test them out to your heart content even without the game to call the service (yet). There is a mode to switch to real environment too. This capability is not trivial, the SDK has to be written with this in mind. And the `firebase-admin`

(which is available in many languages) is fantastic that it is ready to be run as a test.

Firebase Functions that could be written locally at comfort of programmer, while still seeing "realistic" error checking from TypeScript is fantastic. For comparison switch to write Firebase Firestore/Storage rule and how many times you get something wrong because the language cannot be compiler checked.

I have already mentioned SDK design in other languages like C#, it is not just on the server, the `Task<T>`

design throughout allows me to make an `async/await`

C# code that looks like heaven. It requires just a small glue to work with Unity's coroutine system. (Just wait a frame and check until the task is done then we continue, is that glue.) AWS's Unity C# SDK is a horrible callback hell.

No one beats Firebase in programmer's toolkit and SDK coverage.

### Difficulties for non-programmer to manage the game

Here's an inevitable cons of Firebase's level of abstraction. Imagine there is a game balance/admin person in the team which he must make adjustments to some server side values. You must tell him to go to a specific Firestore document and change a specific fields. Or create a new field with an exact string because the code is waiting to read it.

Maybe he need to add a special item to a player because he won a ballot. And instead of nicer UI that let you choose from a list of available items, Firebase of course not for games and don't know what an "item" is as opposed to Playfab with its inventory system, he may need to "add a map of key value pair `{"14420" : 1}`

to an array `items`

of this player" because that number represent the item's ID in the programmer's code, and that's how he serialize it.

Or if you tell him to create a new scoreboard. In BaaS for games like Playfab you would simply press the button that says Create Scoreboard and check a few boxes. But in Firestore it's your canvas. He must go to a specific collection, then create a document to represent a board. Then for some reason you must manually create a collection again named "scores" inside it because Firestore can't do documents in document. Then finally put scores in that "scores" subcollection. Maybe the code is looking for a specific metadata field and you mistyped it.

That maybe a lot of steps to do server side things. And ideally I think Firebase team expect you to use the Admin SDK to write some kind of internal admin web tools that do this according to your needs. In that case, you are kind of building Playfab from Firebase! Except you are in more control of cost and your database design. (partially, that plays according to Google's benefit too.)

### Other fluffs in Firebase

I like the "other things" (outside the staples like database, storage, auth, analytics) in Firebase. For example the test lab is there with physical devices waiting for you. You can actually use Playfab and sign up a dummy Firebase account to use the test lab, but it feels nice to have that in the same hub. Firebase recently add analytics integration to test lab, so people feel more bad to use Firebase only just for the test lab. In the future all these could be more connected.

Crashlytics is looking very promising and looking more advanced that any other higher BaaS offering have. (Playfab for example I see analytics, which may contains crash report I guess, but not an explicit "crash"-lytics like this.) I still don't have any idea how well it could catch bugs at the moment.

### Taking Firebase with you?

With Firebase you are able to take the knowledge with you to use in other non-games things. Playfab is kinda game-only. So in this sense Firebase is more flexible for your future career because learning takes time and you have an edge if you see a new non-games problem and be instantly "Oh, so this should be a collection indexed by X, then this is a separated documents...." thinking in Firestore.

This seems like an out of topic thing but I consider it quite valuable. My mother and father started gardening after buying a land, and I am already thinking about how to automate the process and collect data with Firebase!

### Firebase in 2019

- Firebase introduced Cloud Firestore to succeed RDB, but its Unity SDK has no progress to be seen at all. The actual Firestore went generally available in January 2019. I guess Unity SDK of it will be ready around mid 2020 (??).
- Unity recently acquired Chili Connect to strengthen its own backend service. (
[https://blogs.unity3d.com/2019/10/03/unity-acquires-chilliconnect/](https://blogs.unity3d.com/2019/10/03/unity-acquires-chilliconnect/)) If you want a very Unity-specific solution, keep a watch on this one what Unity will do next. - It is still weird to think if you are going to use Firebase (Functions + Firestore ?) to make a game like battle royale or something. I am not an online game maker so I don't have more to say, but Playfab for example includes matchmaking (labeled Beta at the moment) and such.
- I still think Firebase has the most reasonable pricing for indies, however it is the wiring between components that is a bit troublesome and error prone.

2019 summary : I am still with Firebase, but Playfab is very interesting. In fact I am playing Monster Hunter Iceborne and seeing Playfab logo added in the title and I was reminded to check and found out that Microsoft acquired it already.

Lastly, Epic Games is also providing backend for all engines : [https://dev.epicgames.com/en-US/services](https://dev.epicgames.com/en-US/services). Currently seems to be feature incomplete, with things like leaderboards saying coming soon.

## 2020 Update

PlayFab seems to listened to the wholesale MAU rants I gave for both GameSparks and PlayFab.

To recap, PlayFab was :

![](../../assets/e897ddad87507df1.png)

Then :

![](../../assets/8bb123a237ab6b9f.png)

Now :

![](../../assets/10211b760afc0db3.png)

Staying the same is that live game must move from free plan.

Standard now looks like indie but named better because I think that's the likely destination for many studios. With granular pay as you go like Firebase (which I love), PlayFab do away with MAU and eliminates the 299$ tier because 100k MAU that keeps indie an indie is not a thing anymore. No MAU limits also open up opportunity for aggressive marketing which may cause a lot of come and go influx of new players. This previously would hurt your MAU quota even if they touch your game for 10 seconds. No more!

But still the wholesale price of 99$ is there. The 400$ valued meters works like free resource per month given by Firebase. But the difference is that in Firebase if you did not exhaust free resource per month you will pay nothing! Still, this is much better for PlayFab and also fair for them since you do get nice out of the box game setups not available in Firebase.

### How about the hidden limits

They are still here, and still hidden in the console. I just went in (April 18 2020) and check for you, for example this 25 leaderboards total limit is still there and upgrades are constrained by MAU still. (The disappeared MAU limit is at the outer, overall level that moves your tier up.)

![](../../assets/f2b22dd549f3078e.png)

So hidden inflexibilities remains. To recap, for example my music games will have 20 songs at launch. Each song has 3 difficulty level with its own leaderboard. I need 60 "statistic names" to properly implement this in a non-hacky way! I get that this 25 limits is "more than enough" if used for monthly event kind of game. But that thinking is the same as MAU pricing, it's one size fits all thinking that doesn't work sometimes.

There are many limits lurking, where if I went with Firebase Firestore, 60 or 6000 scoreboards doesn't matter since they are just a collections and documents. PlayFab need some measures to prevent abuse, it seems. Too bad they prevent some good design I would like to go for.

It would be my choice if 99$ per month doesn't hurt. In developing country, 99$ is a lot! So I must build my own stack with Firebase still to get that potential <99$ per month until I could really get some revenues to outweight it.