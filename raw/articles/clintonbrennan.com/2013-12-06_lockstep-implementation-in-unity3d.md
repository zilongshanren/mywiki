---
title: Lockstep Implementation in Unity3D
url: http://clintonbrennan.com/2013/12/lockstep-implementation-in-unity3d/
author: Clinton
published: '2013-12-06'
source_blog: Clinton Brennan
source_site: http://clintonbrennan.com
category: game programming
fetched: '2026-04-13'
---

![](../../assets/e1f4dad706cb0c98.jpg)

In the lockstep network model each client application runs the entire game simulation. The benefits of this approach is that it reduces the amount of information that needs to be sent over the wire. Only the user inputs need to be sent to each other, as opposed to an authoritative server model where for example every units position will need to be sent as often as possible.

For example imagine you want to move a character in the game world. In an authoritative model, the physics simulation will be ran only on the server. The client will communicate to the server where the character should move to. The server will perform the path finding and start to move the character. The server will then send to each client the characters position as frequently as possible so that the clients will have the most updated location. This must be done for every character in the game world. In a real time strategy game you can have thousands of units so the authoritative model would not be feasible.

In a lockstep model, once the user decides to move a character, that is communicated to every client. Every client will then perform path finding and update the characters position. Only the first communication will need to be sent over the internet as every client will have their own physics simulation and can update the characters position themselves.

This model does present some challenges. Each client must run their simulation in sync with each other. This means for example, that the physics simulation must perform the exact same number of updates and in the same order for each action. If this was not the case, then one client could get ahead or behind of the others and when a new command is sent, the path would be different for the client that got ahead or behind. These differences would build up and very different games would be played for each client.

Another issue is determinism across different machines and platforms. Small differences in calculations can cause butterfly effects building up to very different games. This issue will be covered in more detail in a future article.

The implementation presented here is inspired by the [1500 Archers](http://www.gamasutra.com/view/feature/3094/) article. Each players command is processed two turns in the future. Having a delay between when the action is sent and when it is processed helps the game from seeming choppy and laggy. This implementation also leaves room for us to add dynamic controls to adjust the turn length based on latency and machine performance. This part is not covered here and will come in a future article.

For this implementation we have the following definitions:

- Lockstep turn
- A lockstep turn will be made up of multiple game turns. One action per player will be processed in one lockstep turn. The length of the lockstep turn will be adjusted based on performance. At this time it is just hard coded as 200ms.
- Game turn
- A game turn is when the game logic and physics simulation will be updated. The number of game turns per lockstep turn will be adjusted based on performance. At this time it is hard coded to 50ms, or 4 per lockstep. This means there would be 20 game turns per second.
- Action
- An action is a command issued by a player. For example select units in a specified area, or move the selected units to the target location.

Note: we will not be using unity3d’s physics engine. A custom engine that is deterministic will be used. It’s implementation will be covered in a future article.

**The main game loop**

Unity3d’s loop is ran in a single thread. There are two functions that can be implemented to insert our custom code:

- Update()
- FixedUpdate()

Unity3d’s main loop will call Update() once per iteration. This will happen as fast as possible, or will attempt to run at a specific fps rate depending on the settings. FixedUpdate() will be ran so that it is called a predictable number of times per second depending on the settings. During the main loops iteration, it can be called zero or multiple times depending on how long the last iteration took. FixedUpdate() has the behavior we want as we need our code to run an exact number of times per lockstep turn. However, FixedUpdate() rate can only be set before run time. We want to adjust our game frame rate based on performance.

**The Game Frame Turn**

This implementation has similar logic as the FixedUpdate() inside our Update() function. The main difference is that we can adjust it’s rate. This is achieved by having an “accumulative” time. The time of the last iteration will be added to it each Update() call. This is the Time.deltaTime. If the accumulative time is greater than our fixed game frame rate (50ms) then we will make a gameframe() call. We will continue to call gameframe() and subtract from accumulative time by 50ms until accumulative time is less than 50ms.

private float AccumilatedTime = 0f; private float FrameLength = 0.05f; //50 miliseconds //called once per unity frame public void Update() { //Basically same logic as FixedUpdate, but we can scale it by adjusting FrameLength AccumilatedTime = AccumilatedTime + Time.deltaTime; //in case the FPS is too slow, we may need to update the game multiple times a frame while(AccumilatedTime > FrameLength) { GameFrameTurn (); AccumilatedTime = AccumilatedTime - FrameLength; } }

We keep track of the number of game frames for the current lockstep turn. When we reach the number of game frames per lockstep turn, we update the lockstep turn on the next game frame. If the lockstep is not ready to advance to the next turn then we will not increment the game frame, and we will perform the lockstep check again on the next frame.

private void GameFrameTurn() { //first frame is used to process actions if(GameFrame == 0) { if(LockStepTurn()) { GameFrame++; } } else { //update game //... GameFrame++; if(GameFrame == GameFramesPerLocksetpTurn) { GameFrame = 0; } } }

During the game frame turn, the physics simulation is updated and our game logic is updated. Game logic is added by implementing an Interface (IHasGameFrame) and adding that object to a collection that we can iterate through.

private void GameFrameTurn() { //first frame is used to process actions if(GameFrame == 0) { if(LockStepTurn()) { GameFrame++; } } else { //update game SceneManager.Manager.TwoDPhysics.Update (GameFramesPerSecond); List<IHasGameFrame> finished = new List<IHasGameFrame>(); foreach(IHasGameFrame obj in SceneManager.Manager.GameFrameObjects) { obj.GameFrameTurn(GameFramesPerSecond); if(obj.Finished) { finished.Add (obj); } } foreach(IHasGameFrame obj in finished) { SceneManager.Manager.GameFrameObjects.Remove (obj); } GameFrame++; if(GameFrame == GameFramesPerLocksetpTurn) { GameFrame = 0; } } }

The IHasGameFrame interface has a method called GameFrameTurn that takes as an argument the current number of game frames per second. An implementing object that has game logic should base any calculations on the GameFramesPerSecond. For instance if one unit is attacking another and it has an attack rate of 10 damage per second, you would apply the damage by dividing it by GameFramesPerSecond. The GameFramesPerSecond will be adjusted based on performance.

The IHasGameFrame interface also has a property to indicate when it is finished. This allows the implementing object to inform the main game frame loop it is no longer needed. An example of this would be an object that follows a path and once it reached it’s destination, the object is no longer needed.

**The Lockstep Turn**

In order to stay in sync with the other clients, each lockstep turn we must ask the following questions:

- Did we recieve every client’s action for the next turn?
- Did every client confirm that they recieved our action?

We have two objects, ConfirmedActions and PendingActions. Each of these have a collection for each possible message they may receive. We check both of these objects if we are ready to advance to the next turn.

private bool NextTurn() { if(confirmedActions.ReadyForNextTurn() && pendingActions.ReadyForNextTurn()) { //increment the turn ID LockStepTurnID++; //move the confirmed actions to next turn confirmedActions.NextTurn(); //move the pending actions to this turn pendingActions.NextTurn(); return true; } return false; }

**Actions**

Actions or commands are communicated by implementing the IAction interface. This has one method with no arguments called ProcessAction(). The class must also be Serializable. This means any fields of the object should also be Serializable. When a user interacts with the UI, an instance of the action is created, and sent to our lockstep manager in a queue. The queue is used in case the game is too slow and the user is able to send more than one command within a single lockstep turn. Only one command will be sent at a time, but none of them will be ignored.

When sending the action to the other players, the action instance will be serialized to an array of bytes, and then deserialized by those players. A default “NoAction” object will be sent when the user did not perform any actions that turn. The other actions will be specific to the game logic. Here is an example of an action to create a new unit:

using System; using UnityEngine; [Serializable] public class CreateUnit : IAction { int owningPlayer; int buildingID; public CreateUnit (int owningPlayer, int buildingID) { this.owningPlayer = owningPlayer; this.buildingID = buildingID; } public void ProcessAction() { Building b = SceneManager.Manager.GamePieceManager.GetBuilding(owningPlayer, buildingID); b.SpawnUnit(); } }

This action depends on the SceneManager having a static reference. If you do not like this implementation, the IAction interface could be modified so that the ProcessAction() receives an instance of a SceneManager.

The Sample Source can be found at:

[Bitbucket – Sample Lockstep](https://bitbucket.org/brimock/lockstep-sample/overview)

Hello Clinton, thanks for share this knowledge. You seem to not manage exactly the frame execution of Unity, when to run a frame X, but you control when to do a game frame, thats nice. My question is, what happens with other 3D physics simulation, for example if a player makes a rigidbody to fall, this fall “movement” will keep running and a desync on game frame execution can cause different game for each player, right? because it is not directly related to unity’s frame execution.

Yes you are correct. This implementation will not work with Unity’s built in physics engine. To solve for this for my use-case, I created a simple 2D deterministic physics engine:

http://clintonbrennan.com/2014/01/simple-2d-deterministic-physics-simulation/

However if you require 3D physics, or want to work with existing code you may not want to use this implementation.

Hey first of all, thanks for writing this. This has helped me a lot with my own game.

I have a question regarding the GameFrameTurn() method.

Why is it what when GameFrame ==0 that you only want to process the lockstep actions but not update the game? To me it makes sense you would still want to update the game inside of “if(LockStepTurn()) { }” or your kind of throwing out a frame for no reason arent you?

Or is there a specific reason you have for not updating the game model on the same frame as the lock step frame?

No specific reason, just a miss when I first wrote the code

Hey! Thanks for a great guide and a really solid library.

I’m attempting to use this for a RTS game, but I’ve stumbled on a problem. I can’t get ProcessAction() to work. I’m attempting to spawn units and propagate these changes through the network, but it sends NoAction() every turn.

What are the requirements for an action to be sent with ProcessAction? Is there anything I might be missing? I’m a bit new at this. I would be very happy if you could help me out, maybe with a more in depth explanation of how to use ProcessAction().

Once you instantiate an object that implements Action you need to call LockStepManager.Instance.AddAction(action) with the object you created. Hope this helps let me know if you still have questions.

Great article, thanks. But I have some questions about handling sudden lags & disconnection:

(1) What if a player suddenly has some lags due to the network or his own hardware. For example, packets 1-100 are all delivered in 50ms each but for packet 101, it’s delivered/received after 1 second? How to handle this kind of long-delayed packet?

(2) How to detect if some player is disconnected?

(3) When I play games like StarCraft, there is a dialog showing up to wait for the opponent… how to implement this?

Hi, and thank you for this article. However, as I’m new to programming I simply can’t understand how to make actual commands in this solution. Adding commands to the ProcessAction only runs on the local machine, not on networked machines. I’ve also tried to put the logic in SceneManager and calling it from within ProcessAction but still that only runs on the local machine. From reading the debug logs it appears that no actions are sent to the LockStep since it only sends NoAction every tick.

Could you perhaps just give a simple example on how one would go about to say increment an int (if a key is pressed) belonging to a game object so that the information is applied to the LockStep process and replicated to all network players? It is easily done with RPC, but that defeats the purpose of the LockStep.

I would be forever grateful for such an example, thanks and happy new year.

as mentioned in another comment, you need to call LockStepManager.Instance.AddAction(action) with the action you instantiated. I will work on that example you requested when I get some time and post an update.

Hey Clinton,

The articles you have made on the lock step approach have helped me phenomenally. I found though that if one of the players game lags while instantiating or destroying units, it goes out of sync. Those functions must be non-deterministic. My work arounds seem a bit gimmicky. Did you encounter this problem at all?

Thanks for the feedback. A future enhancement I need/want to add is a checksum to catch these out of sync issues. I have a few questions for your situation. When you are instantiating units is that happening during the ProcessActions? When a unit is destroyed, is that happening during GameFrameTurn as a result of applying damage from another unit?

Great Article! How to you deal with floating point math determinism?

Thanks for the feed back. I dealt with it by not using Unity’s physics engine and used my own that uses integers only. This is covered in the simple 2D deterministic physics simulation article.

A good way to do determinism in Unity is not to use the Physics engine at all. Just use your own collision detection (simple distance checks work just fine if called infrequently). I also used a Fixed Point math system that will store the positions of all the units in the system. There is an example at the bottom of this forum post. It probably isnt perfect, but I havent had any issues with it yet. Also, Im doing all my distance checks based on this int, so my physics system is obsolete and my collisions are done in a 2D binning system 🙂

Yup, I did that as well:

http://clintonbrennan.com/2014/01/simple-2d-deterministic-physics-simulation/

Hey Good Job really liked your Tutorial do you still plan to continue it?

Thanks for the feedback. I do intend to continue it when I get the time 🙂

Oh and by the way I found a small mistake in your code. In your LockstepManager you increment “GameFrame++” and you say you achieve 4 Gameframe calls but because you increment it in and don’t execute the gameframe there,


`if(GameFrame == 0) {`

if(LockStepTurn()) {

GameFrame++;

}

it will only be called 3 times per Lockstep tick. Or 15 times per second.