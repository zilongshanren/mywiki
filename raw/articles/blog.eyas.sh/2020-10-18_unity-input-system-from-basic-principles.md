---
title: Unity Input System, from Basic Principles
url: https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system/
author: Eyas Sharaiha
published: '2020-10-18'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In the third installment of the
** Unity for Software Engineers** series
(now updated and

[available as a book](https://leanpub.com/unity-for-engineers)), we cover Unity’s

[Input System](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/)from basic principles.

I’ll be releasing additional installments over the next few weeks, so
[make sure to subscribe](http://eepurl.com/gVgusL) for updates. The series
especially tailored for those who learn best as I do: starting with first
principles and working your way upwards.

Handling player input will likely be among the first game systems you implement.
Unity Technologies
[unveiled a new Input System](https://blogs.unity3d.com/2019/10/14/introducing-the-new-input-system/)
in 2019 intended to replace their previous system. While the Input System (now
version 1.17+) allows building on more idiomatic Unity patterns, it can also be
more challenging for a newcomer to pick these up. This is especially true
because the Input System leans heavily on configurable assets and emphasizes
Editor usage. The Input System’s
[Quick start guide](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.17/manual/QuickStartGuide.html)
is helpful, but only once the Input System and Unity Events’ basic concepts are
understood.

While pre-made solutions exist to handle player input and movement, such as the
highly-recommended
[Ultimate FPS (UFPS)](https://assetstore.unity.com/packages/tools/game-toolkits/ufps-ultimate-fps-106748?aid=1011leWs6)
asset, you will likely always need *some* form of input handling. In this
article, we’ll show how to use the input system to build a barebones player
movement controller on your own (rather than using something like UFPS).

Much of the newer pieces of the Unity Engine are being released as encapsulated
[packages](https://docs.unity3d.com/Manual/PackagesList.html). Unity packages
are installed from the *Unity Package Manager* UI in the editor (open it in
*Window > Package Manager*). The package updates a `manifest.json`

file that has
a `"dependencies"`

entry identical to a
[ package.json](https://docs.npmjs.com/files/package.json#dependencies). The
package manager resolves dependencies and writes to a

`package-lock.json`

. You
can install the Unity Input System from the Package manager, which adds a
dependency on `com.unity.inputsystem`

in your manifest.The Input System makes it easy to create player-configurable cross-platform game controls through assets known as Input Action Maps. The system also exposes an Editor- and event-based interface to specify Input behavior.

## Programmatic Use

If you’d like to make progress on a proof of concept quickly, you might initially choose to sidestep Input Action maps and programmatically interrogate the inputs.

Here’s a basic example covering the most important concepts:

```
using UnityEngine;
using UnityEngine.InputSystem;
public class PlayerControlHandler : MonoBehaviour
{
/// <summary>
/// The speed of a moving player in m/s.
/// </summary>
[SerializeField] private float _moveSpeed = 5f;
void Update()
{
// The last used (or last connected) Gamepad.
// null if there is no connected gamepad.
Gamepad gamepad = Gamepad.current;
// The return value of `.current` can be null.
if (gamepad == null)
{
return;
}
// buttonSouth is a ButtonControl.
if (gamepad.buttonSouth.wasPressedThisFrame)
{
Fire();
}
// leftStick is a StickControl, which eventually
// inherits from InputControl<Vector2>.
//
// InputControl<T> exposes a ReadValue() method
// returning T. Typically, this is a zero-value
// when the control has not been actuated in a
// given frame.
//
// Here, move is a Vector2 between (-1, -1) and
// (+1, +1) indicating the most recent direction
// of the stick (as of this frame).
Vector2 move = gamepad.leftStick.ReadValue();
Vector3 moveThisFrame =
// Make movement speed frame-rate independent
Time.deltaTime * _moveSpeed *
(
(Vector3.right * move.x) +
(Vector3.forward * move.y)
);
transform.position += moveThisFrame;
}
void Fire() {} // TODO: Implement.
}
```


```
using UnityEngine;
using UnityEngine.InputSystem;
public class PlayerControlHandler : MonoBehaviour
{
/// <summary>
/// The speed of a moving player in m/s.
/// </summary>
[SerializeField] private float _moveSpeed = 5f;
void Update()
{
// Control input with WASD + Mouse
Keyboard keyboard = Keyboard.current;
Mouse mouse = Mouse.current;
if (keyboard == null || mouse == null)
{
return;
}
// Mouse.leftButton is also a Button control.
if (mouse.leftButton.wasPressedThisFrame)
{
Fire();
}
// Every keyboard key is a KeyControl, which
// inherits ButtonControl.
//
// ButtonControl extends InputControl<float>
// which represents a control with a value 0
// when not pressed and 1 when pressed.
//
// Here we represent our movement as vertical
// and horizontal axes, each from -1 to +1.
float forward = keyboard.wKey.ReadValue()
- keyboard.sKey.ReadValue();
float horizontal = keyboard.dKey.ReadValue()
- keyboard.aKey.ReadValue();
Vector3 moveThisFrame =
// Make movement speed frame-rate independent
Time.deltaTime * _moveSpeed *
(
(Vector3.right * horizontal) +
(Vector3.forward * forward)
);
transform.position += moveThisFrame;
}
void Fire() {} // TODO: Implement.
}
```


As you can see, `UnityEngine.InputSystem`

exposes various input devices, each
with a static `current`

member returning the device if connected 1 (or you can
iterate

`InputSystem.devices`

). See the documentation for
[.](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.17/api/UnityEngine.InputSystem.Gamepad.html)

`UnityEngine.InputSystem.Gamepad`

, for exampleEach Input Device exposes a number of Controls. These all implement the
class. Significantly,

`InputControl<T>`

`InputControl<T>`

exposes **which returns the current value. This can be repeatedly called in**

`T ReadValue()`

`Update()`

or
`FixedUpdate()`

to respond to input.Most buttons (Gamepad buttons, Mouse clicks, Keyboard keys) eventually inherit
,
which also introduces useful properties such as

`ButtonControl`

`isPressed`

,
`wasPressedThisFrame`

, and `wasReleasedThisFrame`

. A `ButtonControl`

eventually
inherits from `InputControl<float>`

. On digital devices, controls can have a
value of either `0`

or `1`

, but on analog- or pressure-sensitive devices, this
can smoothly vary between `0`

and `1`

.Other controls, like `DpadControl`

and `StickControl`

eventually inherit from
** InputControl<Vector2>**, which gives us the combined player input in 2D
space.

You can define a *composite* `Vector2`

control using
[ Vector2Composite](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.17/api/UnityEngine.InputSystem.Composites.Vector2Composite.html)
from

`UnityEngine.InputSystem.Composites`

. Doing so is helpful, for example, to
create `WASD`

as a single `Vector2`

composite. At that point, however, you might
as well go for the more expressive approach of using Input Actions and Input
Action Map assets, rather than the purely programmatic approach.An advantage of programmatic handling of input is that you can get started quickly. The moment you want to make controls player-configurable or handle multiple devices, this code becomes unwieldy.

## Input Actions

Last week, I warned against the
[impulse of keeping everything in code](https://blog.eyas.sh/2020/10/unity-for-engineers-pt2-six-practices#keep-it-in-code),
when the editor is at your disposal. With a basic understanding of the
fundamentals from the code above, I recommend using the higher-level concept of
*“Input Actions”*.

![An Empty PlayerInput component](../../assets/abaf49f75a97d497.img)

A recently-created Player Input component allows its Game Object to respond to inputs from a given Input Action Map asset.

To start making a Game Object controllable, let’s add a *Player Input* component
to it. A component takes an **Input Actions
** and uses it
to define behaviors for each

[asset](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts#asset)

**Input Action**.

To start, we’ll use the *Create Actions…* button to create a default *Input
Action Asset*. Unity will pedagogically create an asset pre-populated with a
cross-platform control scheme, including movement (on PC: WASD), look (on PC:
mouse movement), and firing.

![A populated Input Action Asset. Shows two "Action Maps" for Player and UI. The Player map is selected, with definitions for Move, Look, Fire, and Jump actions.](../../assets/3bd3c1a74724cf29.img)

A populated Input Action asset loosely modified from the default asset.

An **Input Action Asset** describes a game’s entire control schemes. The asset
comprises multiple **Action Maps**, each corresponding to a control scheme
active in a given context. By default, Unity creates a “Player” (in-game) and a
“UI” (e.g., in menus) map.

Here, you can see that `Move`

is a `Vector2`

action. The *Gamepad* control
scheme uses a stick control, while the *Keyboard/Mouse* scheme uses a composite
`Vector2`

. Keyboard/mouse bindings here allow the player to use either WASD *or*
arrow keys.

Modify your Action Map as needed. For now, don’t worry about *Interactions* or
*Processors*; these allow you to constrain or pre-process action values before
passing them to consumers.

When a *Player Input* component has an input action asset, it allows you to set
a *Default Scheme* and a *Default Map*.

A *Player Input* component has two potential
[ behaviors](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.17/manual/PlayerInput.html#notification-behaviors):

-
**Invoke Unity Events**: Exposes a`UnityEvent<InputAction.CallbackContext>`

for each action in the asset.[UnityEvents](https://docs.unity3d.com/Manual/UnityEvents.html)have a friendly API*and*Editor interface and allow you to specify the exact set of methods to trigger during an action.is also richer than`InputAction.CallbackContext`

`InputValue`

, exposing the corresponding InputAction. Further details such as whether the event corresponds to an action that was`canceled`

(e.g., a button that was released),`performed`

, or`started`

(e.g., a button that was just pressed). Like`InputValue`

, the Callback Context exposes a method to read its value:`TValue ReadValue<TValue>()`

.A Unity Event is triggered every time an action is

*started*,*performed*, and*canceled*. While an InputAction is*actuated*, it will trigger a*performed*event each time the underlying value changes.An action such as a digital button will typically fire a single

*started*,*performed*, and*canceled*event. Holding a button for 5 seconds, for example, would merely delay the*canceled*event.On the other hand, a more variable value, such as a gamepad stick

`Vector2`

value or a Mouse delta`Vector2`

, would trigger a*started*, typically followed by many*performed*events, and finally, a*canceled*event. -
**Invoke C# Events**: Exposes an`onActionTriggered`

[C# Event](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/event)on the component which similarly triggers an`InputAction.CallbackContext`

, as described above.Unlike Unity Events, C# events cannot be modified from the editor. Therefore, components that want to subscribe to an event will need to reference the

`PlayerInput`

component to subscribe to the event. To avoid leaking memory, you should always remember to subscribe in`OnEnable`

and unsubscribe in`OnDisable`

.`public void OnEnable() { // subscribe to the event playerInput.onActionTriggered += HandleInput; } public void OnDisable() { // unsubscribe to avoid memory leaks playerInput.onActionTriggered -= HandleInput; } private void HandleInput(InputAction.CallbackContext context) { if (context.action.name == "Fire") { Fire(); } }`

Also, unlike Unity Events, there is only a single

`onActionTriggered`

event that will trigger the callback for any action that takes place. This means your callback should switch/condition on the Callback Context’s`action`

property.

### Performance: Unity Events vs C# Events

While I usually prefer using Unity Events for their Editor integration and ease
of use, it is important to note that **C# Events are significantly more
performant**.

**Unity Events**: Great for prototyping and hooking up non-frequent events (like UI clicks or death events) in the Inspector. However, they can generate garbage and have higher invocation overhead.**C# Events**: The preferred choice for high-frequency updates (like input handling in`Update`

loops) or performance-critical code. Benchmarks by[Jackson Dunstan](https://jacksondunstan.com/articles/3335)and others have shown that C# delegates can be magnitudes faster and allocation-free compared to UnityEvents.

If you are building a system where every frame counts, stick to C# Events.

### Using Unity Events

I usually prefer using Unity Events with the Input System for a few reasons:

- I find the
`InputAction.CallbackContext`

API more helpful than`InputValue`

; - In
`SendMessage`

and`BroadcastMessage`

, a typo in the message name fails silently, resulting in a method that never gets called; - Compared to C# events, I find it helpful to visually separate the handlers for each action, not only across methods in the same component but across components (e.g., a Move component and an Attack component).

A Unity Event can trigger callbacks on any Unity Object, whether in Asset form
(e.g., a `ScriptableObject`

) or as a Scene GameObject 2. In most cases, you
will probably want to be passing your events to a

`MonoBehaviour`

on a *scene object*. Make sure to select the object in the

*“Scene”*tab rather than

*“Assets”*(i.e., do not select a prefab)

.

[3](https://blog.eyas.sh#user-content-fn-3)Therefore, the typical process will be to

- select the
*scene object*that contains the component you want to call, - select the sub-menu corresponding to the specific component, and
- pick your method from the menu of available public methods.

In cases where your public method signature takes in a single
`InputAction.CallbackContext`

parameter, it will show up in the *“Dynamic
CallbackContext”* section, and automatically bind that input when the event
triggers.

### Inputs and Frame-rate Independence

Unity will call the `Update`

method as often as it can. Each update method
represents a single *frame* in your game. This means that you should not use a
constant “speed per frame” to control *how much the player moves per frame*, for
example, because that will alter the player’s apparent speed as the frame rate
fluctuates.

Unity exposes `Time.deltaTime`

largely for this purpose, which gives you the
elapsed time since the last frame. If you want your player to move by a constant
speed, for example, you will want to make sure to multiple by `Time.deltaTime`

:

```
Vector3 moveVelocity = _moveSpeed * (
_currentMove.x * Vector3.right +
_currentMove.y * Vector3.forward
);
Vector3 moveThisFrame = Time.deltaTime * moveVelocity;
transform.position += moveThisFrame;
```


*With Unity Events*, a common way to handle button movement is to do something
like this:

```
using UnityEngine;
using UnityEngine.InputSystem;
namespace Game.Controls
{
public class PlayerMover : MonoBehaviour
{
[SerializeField] private float _moveSpeed;
private Vector2 _currentMove;
public void OnMove(InputAction.CallbackContext context)
{
// This returns Vector2.zero when context.canceled
// is true, so no need to handle these separately.
_currentMove = context.ReadValue<Vector2>();
}
private void Update()
{
Vector3 moveVelocity = _moveSpeed * (
_currentMove.x * Vector3.right +
_currentMove.y * Vector3.forward
);
Vector3 moveThisFrame = Time.deltaTime * moveVelocity;
transform.position += moveThisFrame;
}
}
}
```


Frame-rate independence is also helpful with action cooldowns (e.g., not being
able to Fire multiple times too frequently), changing rotations, etc. But you
should also watch for pitfalls of when *not* use `Time.deltaTime`

in a
computation.

A great example to watch out for is **mouse delta**. Mouse Delta tells you how
much a mouse has moved.

If you have a pointer to an `InputAction`

in your `Update`

method, the `Vector2`

returned from a mouse delta action will give you the total distance moved this
frame. A longer frame will have a larger value (in other words, `Time.deltaTime`

is already accounted for), and multiplying by `Time.deltaTime`

will further
cause the value to be disproportionately larger for longer frames, and
disproportionately smaller for shorter frames.

If you are using UnityEvents, a mouse delta action will result in your callback
potentially being called multiple times per frame with a different delta value.
These are separate deltas that need to compose additively. Suppose you want to
handle player movement and rotation (or camera rotation) only in `Update()`

,
`LateUpdate()`

, or `FixedUpdate()`

. In that case, you’ll need to keep track of
the delta cumulatively for each frame, resetting it between frames. For example:

```
using UnityEngine;
using UnityEngine.InputSystem;
namespace Game.Controls
{
/// <summary>
/// Moves the object according to input. Typically attached to a top-down
/// camera overlooking the scene.
/// </summary>
public class ViewportMover : MonoBehaviour
{
[SerializeField] private float _moveSensitivity;
private Vector2 _panThisFrame;
public void OnMove(InputAction.CallbackContext context)
{
// This works for delta values, since it is reset at the end of each
// frame.
//
// If the game was cross-platform, and other panning controls used
// console sticks, for example, then those events should replace
// each others, rather than add. We can check context.control.
_panThisFrame += context.ReadValue<Vector2>();
}
private void Update()
{
// For Mouse delta, _panThisFrame is already frame-rate independent, and
// only needs to be multiplied by a sensitivity value.
//
// If the game was cross-platform, we'd need to multiply this value when
// using a non-delta control. We can check context.control.
Vector3 panThisFrame = _moveSensitivity * (
_panThisFrame.x * Vector3.right +
_panThisFrame.y * Vector3.forward
);
transform.position += panThisFrame;
// Reset pan at the end of each frame.
_panThisFrame = Vector2.zero;
}
}
}
```


## Final Thoughts

There is much to learn when mastering smooth player inputs, but I hope the
resources above give you the tools you need to start. Whether it is thinking
about frame-rate independence (and knowing when not to blindly multiply by
`Time.deltaTime`

), creating easily overridable player inputs using Input Action
Maps, or cross-platform input, I hope input in Unity feels less mysterious by
now.

I also hope I convinced you that Unity Events are a great way to substitute hard
cross-component references (statics or using `GetComponent`

) into injectable
connections via the Editor. Keep them in mind next time you design a system that
needs to interact across components.

## Update Notes (2025)

This post was updated in late 2025 to reflect the current state of the Input System (v1.17+).

**Removed Deprecated Methods**: Sections regarding`SendMessage`

and`BroadcastMessage`

behaviors for`PlayerInput`

were removed. These reflection-based approaches are now discouraged due to poor performance and lack of type safety.**Added Performance Notes**: Added a comparison between Unity Events and C# Events, highlighting that C# Events are the preferred choice for performance-critical inputs.

## Footnotes

-
Local multiplayer games can’t count on these static accessors, as the

`current`

Gamepad is whichever device most recently used.[↩](https://blog.eyas.sh#user-content-fnref-1) -
Read more about the difference in the first installment,

[Basic Concepts in Unity for Software Engineers](https://blog.eyas.sh/2020/10/unity-for-engineers-pt1-basic-concepts).[↩](https://blog.eyas.sh#user-content-fnref-2) -
For example, if you want to move your player, you should pass the Player from the scene tabs. If your player is prefab-ed and you pass the prefab, you’ll see some unexpected behavior when trying to move the player.

[↩](https://blog.eyas.sh#user-content-fnref-3)