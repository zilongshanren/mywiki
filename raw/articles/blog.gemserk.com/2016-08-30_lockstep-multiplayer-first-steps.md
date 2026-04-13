---
title: Lockstep multiplayer first steps
url: https://blog.gemserk.com/2016/08/30/lockstep-multiplayer-first-steps/
published: '2016-08-30'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In [this Gamasutra article](http://www.gamasutra.com/blogs/DanielCollier/20151124/251987/Minimizing_the_Pain_of_Lockstep_Multiplayer.php), [Tundra](http://tundragames.com/) developers explain their approach to minimize problems when developing a lockstep multiplayer platform used for their game Rapture - World Conquest. Based on that, my first approach was to create and understand a *deterministic* lockstep logic without even considering networking yet, to focus on one problem at a time.

My objective is to have a reproducible game that given the start state and all the players actions during time, the game can be played again and the final state will be the same.

### Lockstep logic

The first step was start by creating a logic to encapsulate the [fixed game state](http://gafferongames.com/game-physics/fix-your-timestep/) for physics and game logic, and a lockstep to perform player actions. As I started without considering networking yet, all the player actions are directly enqueued locally by the user input or by a saved replay.

A lockstep logic means that there are some conditions that, if not met, the game should pause the simulation and wait for them. In the case of multiplayer games this is when the game have to wait for other players actions that didn’t arrive in time (and where the waiting for other players dialog is shown in some games).

My [code](https://github.com/acoppes/deterministicgame/blob/blogpost20160830/Assets/GameLogic/LockstepFixedUpdate.cs) looks something like this pseudo code:

```
update(dt) {
if (lockstepLogic.IsLockstepTurn()) {
if (!lockstepLogic.IsReady())
return;
lockstepLogic.Process();
}
// normal accumulator logic for the fixed gamestep
}
```


Since I create all player actions locally, the lockstep never happens right now but it is a good practice to simulate and test it anyways.

### Testing it

My first [prototype](https://github.com/acoppes/deterministicgame) using this logic is a box that moves over the screen. When the right mouse button is pressed, the game enqueues a player action to move the box to the specified position, then when the lockstep logic is processed the box receives the command and start moving to that position.

### Interpolation

The moving logic was pretty simple, based on start and destination positions and a speed, the box moves itself to the destination in a straight line. Since that logic is performed in each fixed gamestep, the player see the box jumping between positions, it works but it doesn’t look so good. To improve that and make the movement smoother I created a simple interpolation [code](https://github.com/acoppes/deterministicgame/blob/7124a77d510f43596bf87a1091073051ff9b5566/Assets/Scenes/Unit.cs).

Interpolation depends a lot on what you are trying to interpolate, in some cases could be a simple as the code I used there but there are other cases like the [bouncing ball](https://blog.forrestthewoods.com/the-tech-of-planetary-annihilation-chronocam-292e3d6b169a#1e5f) which need more data to create a better interpolation.

Note: adding interpolation means we have now a delay of one fixed gamestep between the box position being rendered and the real position in the game since we are using previous and current positions info for the interpolation.

### My first replays

By recording all the player actions with the fixed gamestep frame they were executed, I created a basic way to replay the “game” by just reseting the game state to the initial state and start enqueing all the recorded actions in each corresponding frame.

Here is a video of the progress so far:

Yeah, I know, it’s not a great thing, but at least I am starting to understand some of the challenges of making multiplayer games.

### Validating simulation

To validate the game is always performing the same simulation given the same input, I added a checksum calculation based on the game state (for now just the moving box state) which is saved from time to time to use later as validation when simulating the game again. The idea was to start defining an API to get the important game state to consider when validating the simulation, and also to start testing game state validation. The code looks like this:

```
update(frame) {
if (IsChecksumFrame(frame)) {
if (recording) {
checksumRecorder.RecordState(frame, CalculateChecksum());
} else {
if (!checksumValidator.IsValid(frame,
checksumRecorder.SavedChecksums, CalculateChecksum())) {
throw Exception("current game state is not valid!");
}
}
}
}
```


In my first tests I wasn’t reseting the game to the initial state properly so my game was producing different checksums when reproducing the saved player actions, checksums validation started to work after that was fixed.

How am I calculating the Checksum? Right now I am not sure exactly what algorithm to use nor which game state should I consider for the checksum, so what I did was to encapsulate that in some interfaces and implemented a basic way to get both. For the checksum I am using a simple MD5 over a string, and for the game state, well…, a string with all *important* values concatenated (the moving box position, destination, if it is moving or not, etc).

```
string CalculateChecksum() {
string gameStateValue = game.GetGameState();
return MD5.CalculateHash(gameStateValue);
}
string GetGameState() {
string gameState = "";
foreach (object in gameObjects)
gameState += object.GetGameState();
return gameState;
}
```


For a future implementation what I know is that the game state should be composed with important values that can affect the simulation, so I shouldn’t care about about audiovisual stuff like particles, effects and sounds.

Also, the game state concept could be used to reset to the initial game state or even for saved game states (to easily replicate some bug for example), and finally, it could be used to synchronize and validate state if for some reason I end up using a client/server architecture.

### Next frontier: Determinism?

For now I didn’t explore determinism realm because the solution really depends on the game logic but at the same time I must have it clear before starting the game code. One of the next steps is probably start testing with fixed point math, not sure yet, the idea is try to follow an approach similar to the gamasutra article’s of reducing non determinism problem to the minimum before going multiplayer.

If you want to take a look all the code used for this blog post, here is the [link](https://github.com/acoppes/deterministicgame/tree/blogpost20160830).