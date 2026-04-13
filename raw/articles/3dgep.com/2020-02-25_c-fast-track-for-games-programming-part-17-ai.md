---
title: 'C++ Fast Track for Games Programming Part 17: AI'
url: https://www.3dgep.com/cpp-fast-track-17-ai/
author: Robert Grigg
published: '2020-02-25'
source_blog: 3D Game Engine Programming
source_site: https://www.3dgep.com/
category: graphics
fetched: '2026-04-13'
---

Like physics, AI (*Artificial Intelligence*) is an incredibly complex field, and it’s always changing. Some companies allocate entire teams to the subject to make their game provide challenging game play. So we will only cover a few very basic concepts in this tutorial.


**Previous Part: Physics**

**First Part:**

[Getting Started](https://www.3dgep.com/cpp-fast-track-1-getting-started/)For this tutorial, we’ll be using the same template from the [2nd tutorial](https://www.3dgep.com/cpp-fast-track-2-template/):

We will use the same tileset that we used in [Part 11 (Tiles)](https://www.3dgep.com/cpp-fast-track-11-tiles/). Make sure you save the [nc2tiles.png](https://www.3dgep.com/wp-content/uploads/2020/02/nc2tiles.png) file to the assets folder where you extracted the template zip file.

A key point about AI is that it is designed to provide *intelligent* players in a game. But don’t make the mistake of assuming *intelligent* means *perfect,* or that *intelligent* means any level of *intelligence*. The best AI should always introduce an element of *error* in its approach, because if you are trying to emulate another human player/controller, humans are rarely perfect.

Update `game.cpp`

to the following:

|
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
|
#include "game.h"
#include "surface.h"
#include "template.h"
#include "windows.h"
namespace Tmpl8
{
Surface tiles("assets/nc2tiles.png");
Sprite tanksprite(new Surface("assets/ctankbase.tga"), 16);
class Tank
{
public:
Tank(float ix, float iy, float ispeed = 1.5f, int idirection = 0)
{
x = ix;
y = iy;
direction = idirection;
speed = ispeed;
}
void TurnLeft()
{
if (--direction < 0) direction = 15;
}
void TurnRight() {
if (++direction > 15) direction = 0;
}
void Move()
{
float angle = ((2 * PI) / 16) * direction;
x += (sinf(angle) * speed);
y += (-cosf(angle) * speed);
if (x > ScreenWidth) x = 0;
if (x < 0) x = ScreenWidth;
if (y > ScreenHeight) y = 0;
if (y < 0) y = ScreenHeight;
}
void Draw(Surface* gameScreen)
{
tanksprite.SetFrame(direction);
tanksprite.Draw(gameScreen, (int)x, (int)y);
}
float x, y;
int direction;
float speed;
};
class AITank : public Tank
{
public:
AITank(float ix, float iy, int idirection = 0)
: Tank(ix, iy, 0.5f, idirection) //Make sure the AI Tank is slower than the player
{}
void Think(Tank *target) {}
int turn_delay = rand() % 40;
};
Tank mytank( 64, 64 );
AITank aitank( 128, 64);
float frame_timer = 0.0f;
void Game::Init() {}
void Game::Shutdown() {}
static char map[16][78] = {
"jb fb fa fb fb fb fb fb fb fb fb fb fb fa fb fb kc kc kc kc kc kc kc kc kc kc",
"jb fb fa fb fb fb fb fb fb fb fb fb fb fa fb fb kc kc kc kc kc kc kc kc kc kc",
"jb fb fa fb fb fb fb fb fb fb fb fb fb fa fb fb kc kc kc kc kc kc kc kc kc kc",
"jb fb ed fe fe fe fe fe fe fe fe fe fe fd fb fb kc kc kc kc kc kc kc kc kc kc",
"jb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb kc kc kc kc kc kc kc ad kc kc",
"jb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb kc kc kc kc kc kc kc cb kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc cb kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc cb kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc cb kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc cb kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc db kc kc",
"jb fb kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc kc",
"bd cd de cd cd cd cd cd cd cd cd cd de cd cd bc kc kc kc kc kc kc kc kc kc kc",
"fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb",
"fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb",
"fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb"
};
void DrawTile(int tx, int ty, Surface* screen, int x, int y)
{
Pixel* src = tiles.GetBuffer() + 1 + tx * 33 + (1 + ty * 33) * 595;
Pixel* dst = screen->GetBuffer() + x + y * 800;
for (int i = 0; i < 32; i++, src += 595, dst += 800)
for (int j = 0; j < 32; j++)
dst[j] = src[j];
}
void Game::Tick(float deltaTime)
{
frame_timer += deltaTime;
if (frame_timer > 50)
{
screen->Clear(0);
for (int y = 0; y < 16; y++)
for (int x = 0; x < 25; x++)
{
int tx = map[y][x * 3] - 'a', ty = map[y][x * 3 + 1] - 'a';
DrawTile(tx, ty, screen, x * 32, y * 32);
}
if (GetAsyncKeyState(VK_LEFT)) { mytank.TurnLeft(); }
if (GetAsyncKeyState(VK_RIGHT)) { mytank.TurnRight(); }
mytank.Move();
aitank.Think(&mytank);
aitank.Move();
mytank.Draw(screen);
aitank.Draw(screen);
frame_timer = 0.0f;
}
}
};
|

Now we can see there are two classes called `Tank`

that does everything for the player tank, and an `AITank`

which needs all the functionality of the player tank but with the a new method called `AITank::Think`

that will do the magic for making our AI tank chase the player. We can use the Object Oriented Programming (OOP) approach of [inheritance](https://www.geeksforgeeks.org/inheritance-in-c/) giving the `AITank`

all the abilities of the `Tank`

class. We can use [UML class diagrams](https://medium.com/@smagid_allThings/uml-class-diagrams-tutorial-step-by-step-520fd83b300b) to model this inheritance relationship.

Though not as commonplace as Physics or graphic engines, there are a few AI engines available that provide some basic AI features. Despite this, AI very much depends on the type of game you are playing and what kind of gameplay you want your computer controlled players to do, therefore you will need to carefully consider how you make a computer opponent function.

Let’s start at the beginning. One of the simplest forms of AI is to get an enemy (or ally) to chase you. In an open playfield, it is a simple matter to determine if a player is above or below you, or to the left or right and move in the direction to intercept. We can simplify this further – if our AI tank is always moving forward then we can work out if we need to turn left or right. To do this we will use the direction of the player from the AI tank and the AI tank direction. These directions we will represent as two 2D *vectors* and apply the [dot product](https://betterexplained.com/articles/vector-calculus-understanding-the-dot-product/) between them. To make life easier, we take the vector that is perpendicular (90 degrees) to the direction that the AI tank is travelling – this will make the dot product result more useful as seen in the diagram below showing a turn to right situation.

![AI Tank turn right](../../assets/fc262c82d3de99cf.png)


![AI Tank turn right](../../assets/fc262c82d3de99cf.png)

By taking the dot product of the AI tank’s right-hand vector and the direction to the player, the direction to turn the AI tank can be determined.

Conversely the AI tank turning to the left would look like:

![AI Tank turns left](../../assets/7787dde300f7a8de.png)


![AI Tank turns left](../../assets/7787dde300f7a8de.png)

If the dot product with the AI tank’s right-hand vector and the direction to the player is negative, then the AI tank should turn right.

To implement the turning behaviour, update the `AITank::Think`

method:

|
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
|
void Think(Tank* target)
{
if (turn_delay-- <= 0)
{
//Current direction of the AITank
int toright = direction + 4;
if (toright > 15) toright = 0;
float angle = ((2 * PI) / 16) * (float)toright;
float ax = sinf(angle);
float ay = -cosf(angle);
//The direction of the target tank relative to this tank
float bx = (target->x - x);
float by = (target->y - y);
float dot_result = ax * bx + ay * by;
if (dot_result > 0.0f)
this->TurnRight();
else
this->TurnLeft();
turn_delay = rand() % 40;
}
}
|

Consider what we are doing here. It’s a simple movement system which first determines the direction to turn based on the direction to the target tank (in this case, the player). Using the dot product (line 73), we can decide whether to turn right or left in order to face towards the target tank. It does not currently make any attempt to prevent the AI tank from moving on top of the player tank, and whenever you move the player tank the AI tank should move to the same place and hover around that spot if the player tank stops moving.

Your simple tank movement is an example of an unconstrained logic decision. The tank simply moves left/right/up/down as it needs and does not give any consideration to anything else.

Constraints can be added to this. For example: Suppose we do not allow the AI tank to go outside a certain boundary in the middle of the screen. Our human controlled tank can still move all over the screen (or even move off the screen).

In the `AITank`

class, override the `Tank::Move`

method. Change the method to prevent the AI tank from moving outside of the range \((100\cdots 500)\) in the x-axis and \((150\cdots 450)\) in the y-axis.

Why do you think you do this check is in the `AITank::Move`

method and not in the `AITank::Think`

method? (*answer at the end! [1]). Note: it is important to make sure your AI tank starts within these boundaries (otherwise it will get stuck right away).

Now as it stands, your AI tank has to obey certain simple boundary rules which constrains its movement, but once those rules do not interfere, it will move towards you and pounce if you enter its range.

Now add some code to prevent our AI tank moving at all unless the player *also* enters the previously specified range.

Despite having a boundary limit, our AI tank is a pretty hard opponent to avoid, as soon as you go into his range he will home in to you. Imagine if he were able to move diagonally, or even in a vector movement, he’d be pretty hard to sneak past…

It might be helpful if we were to introduce a little inconsistency in his movement. There are 2 simple ways to do this:

- Reduce the frequency of decisions: At the moment the tank is making a decision and moving every frame. Suppose he only made a decision every 8th frame. Try adding a timer that counts down each time the decision code is called, and only allows the decision part of your code to function when the timer is
`0`

. Remember to reset the timer when you make a decision. - Add some degree of error in decisions: The easiest way to add error, is to provide a degree of randomness to the decision process. After your decisions are made, add some code to overwrite the direction choice with a random value in the range \((0\cdots 3)\) (which will correspond to a direction). Note though: doing this each frame will be very unsatisfactory but try it and see. How could you make this randomness more effective? (**Answer later
)[[2]](https://www.3dgep.com#a2)

There are of course many other methods to add inconstancy, but these work well for most things.

Pacman was probably one of the first arcade games ever to make use of AI. We can approximate its ghost movement with a variation of the logic presented here.

Essentially Pacman AI operates like this: if the ghost is above you, it moves down, and if left of you, it moves right. But there were more constraints in place and also some forced decisions.

For example, in Pacman the ghosts all have to move inside the maze and obey the collision systems. They also had different levels of intelligence, ranging from very clever to downright stupid. As an example of a forced decision, it also has enough intelligence to not get stuck in

corners/dead ends, should the Pacman not move and provide updated homing information. If a ghost is moving in a direction which has a dead end, it is forced into choosing another direction, sometimes randomly, sometimes the most effective direction.

The biggest constraint imposed on a Pacman ghost though was the maze. The ghosts must be able to home in on the hero but they have to move within the maze.

The key to the ghost’s movement though is deciding *when* to move. We could use the timer we already have, but we already know we can only move in spaces where the maze allows movement, i.e. at junction points. Therefore rather than a timer, what we need is a way to tell

if we are at a junction point.

Using tiles and a 2D array, create a Pacman style maze (no need for dots). You just need 2 values in the array and on screen, so you can create walls and spaces. Position your tank on screen, and from then on, reference the array to decide if it can move around the maze.

Now place another tank on screen, as your chase ghost. The logic is essentially the same as we did previously but rather than `x`

and `y`

boundaries, test your array to see if there is space in the chosen direction, and if so allow the movement.

Calling this update routine every frame will make your tank super effective at hunting you down as you move inside your maze. Try adapting your AI to detect if you are at a junction point (at least 1 point adjacent to you in the array is blank) and then make your decisions to move.

Once this is working, add a small counter, and make your ghost change direction every other junction point.

You can add many refinements to this basic chase code. Feel free to add more *ghost* tanks, change the frequency of their decision process, and their speed. Also make sure any random choices you do make in forced situations result in valid decisions.

[[1]^](https://www.3dgep.com#q1) *Answer: At the point of decision making, you do not yet know which direction you are moving, therefore you can only use the current `x`

and `y`

coordinates. If either of those are out of the specified range, it should prevent any further movement.

[[2]^](https://www.3dgep.com#q2) **Answer: Calling random every frame is chaotic and not *intelligent* in anyway, however by *occasionally* choosing a random number, combined with a reduced frequency decision process, you can throw in odd movements. *Occasionally* suggests a process to decided when to do this. You can use another timer or test a random number for a certain range to trigger these *errors*.

**Congratulations on getting here! This is the last one for now…**

**Previous Part: Physics**

**First Part:**

Hi

Is there a way you could explain how to implement a mouse cursor? And how to use the Mouse to triger an event? I initially wanted to learn how to create an RTS, placing objects somewhere like a building with a mouse (drag’n’drop). Something simple like a cabin of a lumberjack near a forest which then starts to increase the amount of wood etc. This Tutorial is really nice, i love it but its only partial what i was looking for.

Thank you anyway for the incredible effort you have put into this. Really nice one!

In the

`game.h`

file, there are unimplemented functions for`MouseUp`

,`MouseDown`

,`MouseMove`

,`KeyUp`

, and`KeyDown`

which you can implement.Answer to the question about checking for boundaries in the Move(); method instead of the Think(); method:

Most enemies aren’t perfectly smart. Although they might think they’re moving in the right direction they might still bump into a wall. If the Think(); method is what controls this, they won’t bump into the wall when they’re not smart enough to see there is a wall. That’s why you should check for it in the Move(); method, so that the environment can dictate wether it’s a valid move or not. We live in a world, the world doesn’t live in us.

I like your course. Very much information

implement something like the MouseDown or MouseButtonDown function in template.h