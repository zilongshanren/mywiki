---
title: Lockstep Implementation in Unity3D – Part 2
url: http://clintonbrennan.com/2014/04/lockstep-implementation-in-unity3d-part-2/
author: Clinton
published: '2014-04-05'
source_blog: Clinton Brennan
source_site: http://clintonbrennan.com
category: game programming
fetched: '2026-04-13'
---

**Overview**

In the previous implementation of the lockstep model the game frame rate and the length of the communication turn (referred to as the lockstep turn here) were set at a fixed interval. In real scenarios latency and performance will vary. This update to the original model will keep track of two metrics. The first is the amount of time it takes to communicate with the other players. The second is run-time performance of the game frame method.

**Rolling Averages**

To handle the fluctuations in latency we want to quickly increase the amount of time of a lockstep turn when the latency increases, while we want to slowly adjust for better latency. This will make the game play feel smoother as the pace at which the game updates will be more stable than constantly adjusting. We also do not want to have to keep track of all of the past measurements of latency for the past lockstep turns. We can sum up all of the past information in a “rolling average” and adjust it by some weight for future values.

When ever a new value is larger than the current average, we will set the average to the new value. This will give use the behavior of quickly raising to the increase in latency. When a value is smaller than the current average, we will trust it’s new value by some weight w, so we have the formula:

newAverage = currentAverage * (1 – w) + newValue * ( w)

Where 0 < w < 1
In my implementation I set w = 0.1. I also keep track of the average per player, and always use the maximum average among the players. Here is the method for adding a new value:
[code lang="csharp"]
public void Add(int newValue, int playerID) {
if(newValue > playerAverages[playerID]) {
//rise quickly
playerAverages[playerID] = newValue;
} else {
//slowly fall down
playerAverages[playerID] = (playerAverages[playerID] * (9) + newValue * (1)) / 10;
}
}
[/code]
In order to maintain determinism the calculation is done using only integers. So the formula is adjusted like the following:
newAverage = (currentAverage * (10 - w) + newValue * ( w)) / 10
Where 0 < w < 10
And in my case, w = 1.
**Runtime Average**

The time it takes to execute each game frame is tracked to be used for the runtime average. If the game frames start taking longer, then we need to decrease the number of game frames per lockstep turn. On the other hand if the game frames start executing faster, we can have more game frames per lockstep. For each lock step turn, the longest running game frame is used to be added to the average. The first game frame of each lockstep turn also includes the amount of time it takes to process the action for that lockstep turn. A Stopwatch is used to take the measure of lapsed time.

private void ProcessActions() { //process action should be considered in runtime performance gameTurnSW.Start (); ... //finished processing actions for this turn, stop the stopwatch gameTurnSW.Stop (); } private void GameFrameTurn() { ... //start the stop watch to determine game frame runtime performance gameTurnSW.Start(); //update game ... GameFrame++; if(GameFrame == GameFramesPerLockstepTurn) { GameFrame = 0; } //stop the stop watch, the gameframe turn is over gameTurnSW.Stop (); //update only if it's larger - we will use the game frame that took the longest in this lockstep turn long runtime = Convert.ToInt32 ((Time.deltaTime * 1000))/*deltaTime is in secounds, convert to milliseconds*/ + gameTurnSW.ElapsedMilliseconds; if(runtime > currentGameFrameRuntime) { currentGameFrameRuntime = runtime; } //clear for the next frame gameTurnSW.Reset(); }

Note that we also include Time.deltaTime. Including this may have some overlap with the last frame if gameframe is running at the same rate as the Update() method. However we need to include it so that rendering and other things that Unity does for us is considered in the measurement. The potential overlap is acceptable as it would just give us a bigger buffer.

**Network Average**

What to use as the network average was not as clear to me. I ended up using a Stopwatch that ran from the time a player sends an action to the time they receive the final confirmation of the action. This lockstep model sends an action to be processed for two turns in the future. To increment the lockstep turn we ensure that all players have confirmed the action we are about to process. Due to this setup, we could potentially have two actions that are waiting for all of their confirmations. To deal with this, two Stopwatches are used. One for the current action and one for the prior action. This is encapsulated in the ConfirmActions class. When the lockstep turn is incremented, the prior Stopwatch becomes the current stop watch, and the old “current stop watch” is cleared and reused as the new “prior stop watch”.

public class ConfirmedActions { ... public void NextTurn() { ... Stopwatch swapSW = priorSW; //last turns actions is now this turns prior actions ... priorSW = currentSW; //set this turns confirmation actions to the empty array ... currentSW = swapSW; currentSW.Reset (); } }

Whenever a confirmation comes in, we check if we have received all confirmations, and if so stop the respected Stopwatch.

public void ConfirmAction(int confirmingPlayerID, int currentLockStepTurn, int confirmedActionLockStepTurn) { if(confirmedActionLockStepTurn == currentLockStepTurn) { //if current turn, add to the current Turn Confirmation confirmedCurrent[confirmingPlayerID] = true; confirmedCurrentCount++; //if we recieved the last confirmation, stop timer //this gives us the length of the longest roundtrip message if(confirmedCurrentCount == lsm.numberOfPlayers) { currentSW.Stop (); } } else if(confirmedActionLockStepTurn == currentLockStepTurn -1) { //if confirmation for prior turn, add to the prior turn confirmation confirmedPrior[confirmingPlayerID] = true; confirmedPriorCount++; //if we recieved the last confirmation, stop timer //this gives us the length of the longest roundtrip message if(confirmedPriorCount == lsm.numberOfPlayers) { priorSW.Stop (); } } else { //TODO: Error Handling log.Debug ("WARNING!!!! Unexpected lockstepID Confirmed : " + confirmedActionLockStepTurn + " from player: " + confirmingPlayerID); } }

**Sending the averages**

To send the averages experienced on one client to the rest, the Action interface was changed to an abstract class that has two fields.

[Serializable] public abstract class Action { public int NetworkAverage { get; set; } public int RuntimeAverage { get; set; } public virtual void ProcessAction() {} }

When processing the action, these numbers are added to the running average. Then the Lockstep turn and game frame turn is updated

private void UpdateGameFrameRate() { //log.Debug ("Runtime Average is " + runtimeAverage.GetMax ()); //log.Debug ("Network Average is " + networkAverage.GetMax ()); LockstepTurnLength = (networkAverage.GetMax () * 2/*two round trips*/) + 1/*minimum of 1 ms*/; GameFrameTurnLength = runtimeAverage.GetMax (); //lockstep turn has to be at least as long as one game frame if(GameFrameTurnLength > LockstepTurnLength) { LockstepTurnLength = GameFrameTurnLength; } GameFramesPerLockstepTurn = LockstepTurnLength / GameFrameTurnLength; //if gameframe turn length does not evenly divide the lockstep turn, there is extra time left after the last //game frame. Add one to the game frame turn length so it will consume it and recalculate the Lockstep turn length if(LockstepTurnLength % GameFrameTurnLength > 0) { GameFrameTurnLength++; LockstepTurnLength = GameFramesPerLockstepTurn * GameFrameTurnLength; } LockstepsPerSecond = (1000 / LockstepTurnLength); if(LockstepsPerSecond == 0) { LockstepsPerSecond = 1; } //minimum per second GameFramesPerSecond = LockstepsPerSecond * GameFramesPerLockstepTurn; PerformanceLog.LogGameFrameRate(LockStepTurnID, networkAverage, runtimeAverage, GameFramesPerSecond, LockstepsPerSecond, GameFramesPerLockstepTurn); }

**Update: Single Player Support**

Since the posting of this article a small update has been made to support single player mode. Special thanks to Dan at [redstinggames.com](http://redstinggames.com) for figuring this out. You can see the modifications here:

[Single Player Update diff](https://bitbucket.org/brimock/dynamic-lockstep-sample/commits/11539478537f52cbafd8cfd575ea067fdd6a9e49)

**Source Code**

Hi, first thanks for the awesome example which helped decide to scrape my overly complex lockstep with authoritative server implementation and start from scratch using your code as a base.

Anyway I got stuck a little into something that never thought it would be much of a problem. That is interpolating movements between gameSteps. I tried various different approaches, but every one of them have some kind of flaw. The most recurring problem is a small but visible jitter and when i try to correct it i start to lag behind or get to the target to early resulting in a brief movement pause.

I probably made some mistakes here and there and refining one of the approaches would probably get me to a result I need. But as I am a beginner in game programming, any advice would be gladly appreciated.

The way I did it was I created a FollowPath class that implements IHasGameFrame. The FollowPath has the results from an AStar path finder and it’s job is just to follow that path. The FollowPath has a speed. Each game frame the speed is divided by the passed in gameFramesPerSecond to determine the amount of distance that should be consumed that frame. Some work is done to determine what the new center should be for the unit and then it sets the unit’s velocity so that during the physics update it’s position will be that point.

Great job Clinton

Cant wait to see what you will add in the next part 🙂

Keep your great job

This looks great! Concerning this part:

“What to use as the network average was not as clear to me. I ended up using a Stopwatch that ran from the time a player sends an action to the time they receive the final confirmation of the action.”

I had initially attempted this with Network.GetAveragePing .

However, your solution works better because it doesnt involve a lot of calculations on who was longest and it uses the network communications already there to calculate the same thing. I like it.

I also have to thank you for helping me make significant progress on my RTS. Every time I posted a question to the forums or to a professor, they just referred me to the 1500 Archers article :/