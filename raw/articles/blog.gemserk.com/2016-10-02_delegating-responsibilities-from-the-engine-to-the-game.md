---
title: Delegating responsibilities from the engine to the game
url: https://blog.gemserk.com/2016/10/02/delegating-responsibilities-from-the-engine-to-the-game/
published: '2016-10-02'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

When building a platform for a game I tend to spend too much time thinking solutions for every possible problem, in part because it is fun and also a good exercise and in part because I am not sure which of those problems could affect the game. The idea of this post is to share why sometimes I believe it is better to delegate problems and solutions to the game instead of solving them in the engine.

In the case of the game state, I was trying to create an API on the platform side to be used by the game to easily represent it. I started by having a way to collaborate with the game state by storing values in it, like this:

```
public interface GameState {
void storeInt(string name, int number);
void storeFloat(string name, float number);
}
```


In order to use it, a class on the game side has to implement an interface which allows it to collaborate in part of the game state data:

```
public class MyCustomObject : GameStateCollaborator
{
public void Collaborate(GameState gameState){
gameState.storeFloat("myHealth", 100.0f);
gameState.storeInt("mySpeed", 5);
}
}
```


It wasn’t bad with the first tests but when I tried to use in a more complex situation the experience was a bit cumbersome since I had more data to store. I even felt like I was trying to recreate a serialization system and that wasn’t the idea of this API.

Since I have no idea what the game wants to save or even how it wants to save it, I changed a bit the paradigm. The GameState is now more like a concept without implementation, that part is going to be decided on the game side.

```
public interface GameState {
}
```


So after that change, the game has to implement the GameState and each game state collaborator will have to depend on that custom implementation, like this:

```
public class MyCustomGameState : GameState
{
public int superImportantValueForTheGame;
public float anotherImportantValueForTheGame;
}
public class MyCustomObject : GameStateCollaborator
{
public void Collaborate(GameState gameState)
{
var myCustomGameState = gameState as MyCustomGameState;
myCustomGameState.anotherImportantValueForTheGame = 100.0f;
myCustomGameState.superImportantValueForTheGame = 5;
}
}
```


In this way, I don’t know or care how the game wants to store its game state, what I know is there is a concept of GameState that is responsible of providing the information the platform needs to make features, like a replay or savegame, work. For example, at some point I could have something like:

```
public interface GameStateSave
{
void Save(GameState gameState);
}
```


And let the game decide how to save its own game state even though the engine is responsible of how and when that interface is used to perform some task.

In the end, the platform/engine ends up being more like a framework, providing tools or life cycles to the user (the game) to easily do some work in a common way.