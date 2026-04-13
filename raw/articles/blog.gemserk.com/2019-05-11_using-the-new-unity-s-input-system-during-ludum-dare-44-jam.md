---
title: Using the new Unity's Input System during Ludum Dare 44 Jam
url: https://blog.gemserk.com/2019/05/11/experimenting-with-new-unity-input-system/
published: '2019-05-11'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

During [Bankin’ Bacon development](https://blog.gemserk.com/2019/04/30/bankinbacon-ld44jam/) we ended up using both Unity’s legacy Input System and new [Input System](https://github.com/Unity-Technologies/InputSystem), and we wanted to share our experience with them.

We knew from the beginning we wanted to experiment with the new Input System but since we had no experience and we only had three days, we started by using only the legacy one.

# Legacy input system

After prototyping a bit and iterating over the game concept, we decided we wanted to control everything Gamepads (using Xbox 360 Controllers) and the player would be able to do four actions, move (left stick), target (right stick), dash and attack.

For those actions, we created an [input class](https://gitlab.com/gemserk/ld44bankingbacon/blob/master/Assets/Scripts/Game/Logic/Input/UnitControllerInput.cs) that reads the Input and store their state so it can be used later by our character class. The code is something like this:

```
class UnitController : MonoBehaviour {
Vector2 movementDirection;
Vector2 fireDirection;
bool isFiring;
bool isDashing;
UnitControllerAsset inputAsset;
void Update() {
movementDirection.x = Input.GetAxis(inputAsset.moveHorizontalAxis);
movementDirection.y = Input.GetAxis(inputAsset.moveVerticalAxis);
...
isFiring = Input.GetButtonDown(inputAsset.fire1Button);
...
}
}
```


The Player’s prefab can be configured to use a specific set of Input keys by creating a `UnitControllerAsset`

asset and assigning it to the controller. The asset looks like this:

```
class UnitControllerAsset : ScriptableObject {
public string moveHorizontalAxis;
public string moveVerticalAxis;
public string fireHorizontalAxis;
public string fireVerticalAxis;
public string fire1Button;
public string fire2Button;
}
```


In order to perform actions, our character class checks the state of the `UnitController`

values and acts accordingly. For example:

```
class UnitCharacter : MonoBehaviour {
UnitController controller;
void Update()
{
transform.position += controller.movingDirection * speed * dt;
if (controller.isFiring && cooldown) {
FireProjectile(controller.fireDirection);
}
...
}
}
```


Note: this is an oversimplified code, the game’s code is super ugly.


From the Unity’s InputManager side, we created action keys for each player and configure them using different joystick numbers:

![](../../assets/0098c5919e96344b.png)


This was a hell to manage, I mean, it wasn’t so hard but it was super easy to make mistakes and not know where. To simplify a bit this task, we normally modify the `ProjectSettings/InputManager.asset`

file directly using a text editor so we can do copy, paste and replace text.

Following this approach we quickly had something working for two players and if we wanted more players we would have just to copy the actions and configure some prefabs.

## Mac/Windows differences

Since life is not easy, buttons and axis are mapped differently between Windows and Mac (at least with the driver we were using for Xbox 360 Controllers). To overcome this issue, we had to implement a hack to support different platform Input mapping. What we do is, we duplicate action keys for each OS and we read them differently on that. So, we end up having something like `Player0_Fire1`

for Windows and `Player0_Fire1Mac`

for Mac (you can see that in the previous InputManager’s image) . Here is an example of the hack code:

```
void Update() {
if (Application.platform == RuntimePlatform.OSXPlayer || Application.platform == RuntimePlatform.OSXEditor)
{
fx = Input.GetAxis(_inputAsset.fireHorizontalAxis + "Mac");
fy = Input.GetAxis(_inputAsset.fireVerticalAxis + "Mac");
firing1 = Input.GetButtonDown(_inputAsset.fire1Button + "Mac");
firing2 = Input.GetButtonDown(_inputAsset.fire2Button + "Mac");
}
}
```


We are not responsible if you want to use this code and your computer explodes.


By the end of the second day of development we had our Gamepads working and we were able to go from 2 to 4 players support by just adding the actions mapping for new players in the InputManager and creating some prefabs.

Even though that was working fine in the computer we were using for development, it didn’t on our personal computers at home and we didn’t know why.

# New input system

Since we were worried that could happen to more people and we love livin’ on the edge (we used Unity 2019.1 for the game), we decided to spend the last day trying to improve our input issues by using the new Input System (whaaaaaaaat?).

We started by creating another project named [LearnAboutNewInputSystem](https://github.com/acoppes/LearnAboutNewInputSystem) and importing the needed packages by following these [installation steps](https://github.com/Unity-Technologies/InputSystem/blob/develop/Packages/com.unity.inputsystem/Documentation~/Installation.md). The idea was to iterate and learn about the API in a safe context and, only after we manage to do what we needed, integrate it in the game.

Once we had the project ready, we created an Input Actions asset with `Create > Input Actions`

and configured some actions to start testing. Here is the asset configuration:

![](../../assets/811cdc42def526ec.png)


We specified a continuous axis Action, named `Movement`

, that receives input from the Gamepad left stick and from the keyboard keys WASD. In order to react to that action, we created a GameObject with a `PlayerInput`

MonoBehaviour and mapped to our custom MonoBehaviour methods using Unity Events.

`PlayerInput`

inspector automatically shows Unity Events for each action you create on the Input Actions configuration asset:

![](../../assets/caf1503c61a319b4.png)


Note: it has a bug what adds same action multiple times each time it reloads code or something like that.


And here is our code to handle the action event:

```
public class MyControllerTest {
public void OnMovement(InputAction.CallbackContext context) {
var axis = context.ReadValue<Vector2>();
Debug.LogFormat("Moving to direction {0}", axis);
}
}
```


That worked well, however we started to see some possible problems. First, even though we received callbacks continuously for the Gamepad left stick, we only received callbacks for the keyboard when a key was pressed or released but not all the time as expected. Second, we didn’t know how to identify different Gamepads, so with the current test, each time a left stick on any connected Gamepad was moved, our callback was invoked.

Note: we didn’t know about the

`PlayerInputManager`

class while developing the game. We tried using it now (while writing this blog post) but we detected also some problems.

By checking about new Input System in [Unity’s Forums](https://forum.unity.com/forums/new-input-system.103/) we found some people trying to do something similar and one dev suggested [doing this](https://forum.unity.com/threads/how-to-use-multiple-controllers-in-local-multiplayer-game.616726/) and also checking the [test cases](https://github.com/Unity-Technologies/InputSystem/tree/develop/Assets/Tests) for how to use the API. Following those recommendations, we managed to make our first version of multiple Gamepads support.

Here is the code:

```
public class MyPlayersManager : MonoBehaviour {
InputUser[] _users;
Gamepad[] _gamepads;
void Start()
{
_users = new InputUser[4];
_gamepads = new Gamepad[4];
InputUser.listenForUnpairedDeviceActivity = 4;
InputUser.onChange += OnControlsChanged;
InputUser.onUnpairedDeviceUsed += ListenForUnpairedGamepads;
for (var i = 0; i < _users.Length; i++)
{
_users[i] = InputUser.CreateUserWithoutPairedDevices();
}
}
void OnControlsChanged(InputUser user, InputUserChange change, InputDevice device)
{
if (change == InputUserChange.DevicePaired)
{
var playerId = _users.ToList().IndexOf(user);
_gamepads[playerId] = device as Gamepad;
} else if (change == InputUserChange.DeviceUnpaired)
{
var playerId = _users.ToList().IndexOf(user);
_gamepads[playerId] = null;
}
}
void ListenForUnpairedGamepads(InputControl control)
{
if (control.device is Gamepad)
{
for (var i = 0; i < _users.Length; i++)
{
// find a user without a paired device
if (_users[i].pairedDevices.Count == 0)
{
// pair the new Gamepad device to that user
_users[i] = InputUser.PerformPairingWithDevice(control.device, _users[i]);
return;
}
}
}
}
}
```


What we do here is to listen for any raw event, for example pressing a button, from unpaired Gamepads and pair them with users without paired devices.

In the Forums, they also recommend creating a new instance of the Input Actions asset for each user, we tested that and worked somehow but we realized we didn’t need it for the game so we decided to just read the Gamepad values directly.

# Integrating it in Bankin’Bacon

To integrate it in the game and be able to use it in any scene, we created a Singleton named [ UnitNewInputSingleton](https://gitlab.com/gemserk/ld44bankingbacon/blob/master/Assets/Scripts/Game/Logic/Input/UnitNewInputSingleton.cs), using a ScriptableObject, initiated the first time it was invoked. Each time we want to know the state of a Gamepad for a user, we add a dependency to the asset and use it directly from code.

To implement a new controller using the new input, we first created an abstract class for the `UnitController`

and then created a [new implementation](https://gitlab.com/gemserk/ld44bankingbacon/blob/master/Assets/Scripts/Game/Logic/Input/UnitControllerNewInput.cs) using a reference to the `UnitNewInputSingleton`

to ask for the raw data of the Player’s Gamepad. Here is the code of the new input:

```
public class UnitControllerNewInput : UnitControllerBaseInput {
[SerializeField]
private UnitNewInputSingleton _inputMaster;
[SerializeField]
private UnitControllerInputAsset _keyboardControls;
private Vector2 _moveDirection;
private Vector2 _targetDirection;
public override Vector3 MoveDirection => new Vector3(_moveDirection.x, 0, _moveDirection.y);
public override Vector3 FireDirection => new Vector3(_targetDirection.x, 0, _targetDirection.y);
public override bool IsFiring1 { get; set; }
public override bool IsFiring2 { get; set; }
private int _inputPlayerId;
private void Start()
{
_inputPlayerId = _inputMaster.RegisterPlayer();
}
private void Update()
{
_moveDirection = new Vector2();
_targetDirection = new Vector2();
var gamepad = _inputMaster.GetGamepad(_inputPlayerId);
if (gamepad != null)
{
_moveDirection = gamepad.leftStick.ReadValue();
_targetDirection = gamepad.rightStick.ReadValue();
IsFiring1 = gamepad.rightShoulder.wasPressedThisFrame || IsFiring1;
IsFiring2 = gamepad.leftShoulder.wasPressedThisFrame || IsFiring2;
}
}
}
```


Since we had access to the raw input, on some scenes where we just wanted to know if any Gamepad button was pressed, we iterated over all the Gamepads. This was used to restart the game for example.

```
var start = _inputMaster.Gamepads.Any(g => g != null && g.startButton.wasReleasedThisFrame);
var select = _inputMaster.Gamepads.Any(g => g != null && g.selectButton.wasReleasedThisFrame);
if (start)
{
OnGameRestart();
} else if (select)
{
SceneLists.Load().LoadMenu();
}
```


If you want to see more about one day solution code check [the game Gitlab page](https://gitlab.com/gemserk/ld44bankingbacon).

# Finally

Even though Legacy Input System works for quickly prototyping, it is really limited to do Gamepads support and it sucks in terms of configuration. It even doesn’t support remap joystick actions using the default Unity’s Launcher Window.

The new Input System is looking better already but we believe it still has a lot of issues to fix and probably not ready for production. It also has some strange design decisions (in our humble opinion) like having split screen stuff in the API and configuration scripts. The API should be clean and provide low level control and then there should be optional packages to do more stuff depending the game.

We hope they keep working and improve it as much as possible and release a stable version soon.