---
title: Second attempt at Highscores for games
url: https://blog.gemserk.com/2011/06/14/second-attempt-at-highscores-for-games/
published: '2011-06-14'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Some time ago we started a web application on github named [datastore-server](https://github.com/gemserk/datastore-server) which allows us to store data for our games in a remote server hosted on Google App Engine. Since the first data we needed to store was game scores, and we required more specific queries for them, datastore-server end up being a high scores server, at least for now.

We made an introduction of some of the requirements we wanted for the [scores server in a previous post](https://blog.gemserk.com/2010/08/11/first-attempt-at-highscores-for-games/), we made some modifications to the basic concepts.

### Profile

First of all, we added a new structure which identifies the player and has the following fields:

Profile { privateKey : String - a unique private key owned by the player on the client application, used to submit scores publicKey : String - a unique public key used to identify scores name : String - the player name guest : Boolean - if the profile is guest or not }

### Score

Score structure has been modified to have a profile reference, and also some extra data required for scores filtering improvement (filter by date range):

Score { .... (previous data) profilePublicKey : String - a reference to the profile owner of the score year : Integer - the year the score was submitted (calculated in the server) month : Integer - the month of the year the score was submitted (calculated in the server) week : Integer - the week of the year the score was submitted (calculated in the server) day : Integer - the day of the year the score was submitted (calculated in the server) }

The server now provides the following features:

- create guest and non-guest profiles for score submission
- submit a score for a game given a profile
- request scores given a criteria

### Creating and updating profiles

To create profiles datastore-server provides a query named **/newProfile** with two parameters:

- name : String - represents the name of the profile
- guest : Boolean - if the profile is guest or not

The query returns the profile structure as JSON so that the client can save the private and public keys that are generated on the server.

We also provide a way to change a guest profile name and to make it be non-guest using the **/updateProfile** query:

- privateKey : String - identifies the profile
- name : String - the new name we want for the profile

### Submitting a new score

To submit a new score we now need a guest or non-guest profile, it still uses the same query **/submit** with the same parameters plus the profile privateKey.

### Requesting scores

To ask for the scores of a game we have the **/scores** query with the addition now of two new parameters:

- distincts : Boolean - if scores should be filtered to return only one score per player (optional, true by default)
- range : enum { day, week, month, all } - filter best scores by today, this week or this month respectively (optional, all by default)

So, for example, if you want the 50 best scores of the week for a game, you will query **/scores?gameKey=something&limit=50&range=week**.

### Datastore Java client

Finally, to communicate in an easy way with datastore-server we created a [Java library named datastore](https://github.com/gemserk/datastore), also on github, which abstracts all communication stuff using apache http-client and also provide classes for score and profile concepts.

If you want to see high scores in action, you could play Face Hunt on [PC here](https://blog.gemserk.com/games/facehunt/) or on [Android here](https://market.android.com/details?id=com.gemserk.games.facehunt), also you could take a look at the [source code here](https://github.com/gemserk/facehunt).

Both projects datastore and datastore-server will probably change in order to incorporate other data storage beside scores.

Hope you like it.