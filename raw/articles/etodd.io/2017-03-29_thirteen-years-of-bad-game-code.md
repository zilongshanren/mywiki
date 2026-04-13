---
title: Thirteen Years of Bad Game Code
url: https://etodd.io/2017/03/29/thirteen-years-of-bad-game-code/
published: '2017-03-29'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Thirteen Years of Bad Game Code

Alone on a Friday night, in need of some inspiration, you decide to relive some of your past programming conquests.

The old archive hard drive slowly spins up, and the source code of the glory days scrolls by...

Oh no. This is not at all what you expected. Were things really this bad? Why did no one tell you?
Why were you like this? *Is it even possible to have that many gotos in a single function?*
You quickly close the project. For a brief second, you consider deleting it and scrubbing the hard drive.

What follows is a compilation of lessons, snippets, and words of warning salvaged from my own excursion into the past. Names have not been changed, to expose the guilty.

## 2004

I was thirteen. The project was called *Red Moon* — a wildly ambitious third-person jet combat game.
The few bits of code that were not copied verbatim out of * Developing Games in Java* were patently atrocious.
Let's look at an example.

I wanted to give the player multiple weapons to switch between. The plan was to rotate the weapon model down inside the player model, swap it out for the next weapon, then rotate it back. Here's the animation code. Don't think about it too hard.

```
public void updateAnimation(long eTime) {
if(group.getGroup("gun") == null) {
group.addGroup((PolygonGroup)gun.clone());
}
changeTime -= eTime;
if(changing && changeTime <= 0) {
group.removeGroup("gun");
group.addGroup((PolygonGroup)gun.clone());
weaponGroup = group.getGroup("gun");
weaponGroup.xform.velocityAngleX.set(.003f, 250);
changing = false;
}
}
```


I want to point out two fun facts. First, observe how many state variables are involved:

- changeTime
- changing
- weaponGroup
- weaponGroup.xform.velocityAngleX

Even with all that, it feels like something's missing... ah yes, we need a variable to track
*which weapon is currently equipped*. Of course, that's in another file entirely.

The other fun fact is that I never actually created more than one weapon model. Every weapon used the same model. All that weapon model code was just a liability.

### How to Improve

Remove redundant variables. In this case, the state could be captured by two variables: weaponSwitchTimer and weaponCurrent. Everything else can be derived from those two variables.

Explicitly initialize everything. This function checks if the weapon is null and initializes it if necessary. Thirty seconds of contemplation would reveal that the player always has a weapon in this game, and if they don't, the game is unplayable and might as well crash anyway.

Clearly, at some point, I encountered a NullPointerException in this function, and instead of thinking about why it happened, I threw in a quick null check and moved on. In fact, most of the functions dealing with weapons have a check like this!

Be proactive and make decisions upfront! Don't leave them for the computer to figure out.

### Naming

`boolean noenemies = true; // why oh why`


Name your booleans positively. If you find yourself writing code like this, re-evaluate your life decisions:

```
if (!noenemies) {
// are there enemies or not??
}
```


### Error Handling

Snippets like this are sprinkled liberally throughout the codebase:

```
static {
try {
gun = Resources.parseModel("images/gun.txt");
} catch (FileNotFoundException e) {} // *shrug*
catch (IOException e) {}
}
```


You might be thinking "it should handle that error more gracefully! Show a message to the user or something." But I actually think the opposite.

You can never have too much error *checking*, but you can definitely have too much error *handling*.
In this case, the game is unplayable without the weapon model, so I might as well let it crash.
Don't try to gracefully recover from unrecoverable errors.

Once again, this requires you to make an upfront decision as to which errors are recoverable.
Unfortunately, Sun decided that almost all Java errors *must* be recoverable, which results in
lazy error handling like the above.

## 2005-2006

At this point I learned C++ and DirectX. I decided to write a reusable engine so that mankind could benefit from the vast wealth of knowledge and experience I had acquired in my fourteen years on the earth.

If you thought the last trailer was cringey, just wait.

By now I learned that Object-Oriented Programming is Good™, which resulted in monstrosities like this:

```
class Mesh {
public:
static std::list<Mesh*> meshes; // Static list of meshes; used for caching and rendering
// Loads the x file specified
Mesh(const Mesh& vMesh);
~Mesh();
void LoadMesh(LPCSTR xfile); // Loads the x file specified
void DrawSubset(DWORD index); // Draws the specified subset of the mesh
GetNumFaces(); // Returns the number of faces (triangles) in the mesh
GetNumVertices(); // Returns the number of vertices (points) in the mesh
GetFVF(); // Returns the Flexible Vertex Format of the mesh
int GetNumSubsets(); // Returns the number of subsets (materials) in the mesh
// World transform
::vector<Material>* GetMaterials(); // Gets the list of materials in this mesh
::vector<Cell*>* GetCells(); // Gets the list of cells this mesh is inside
GetCenter(); // Gets the center of the mesh
float GetRadius(); // Gets the distance from the center to the outermost vertex of the mesh
bool IsAlpha(); // Returns true if this mesh has alpha information
bool IsTranslucent(); // Returns true if this mesh needs access to the back buffer
void AddCell(Cell* cell); // Adds a cell to the list of cells this mesh is inside
void ClearCells(); // Clears the list of cells this mesh is inside
protected:
ID3DXMesh* d3dmesh; // Actual mesh data
// Mesh file name; used for caching
// Number of subsets (materials) in the mesh
::vector<Material> materials; // List of materials; loaded from X file
::vector<Cell*> cells; // List of cells this mesh is inside
// The center of the mesh
float radius; // The distance from the center to the outermost vertex of the mesh
bool alpha; // True if this mesh has alpha information
bool translucent; // True if this mesh needs access to the back buffer
void SetTo(Mesh* mesh);
}
```


I also learned that comments are Good™, which led me to write gems like this:

```
D3DXVECTOR3 GetCenter(); // Gets the center of the mesh
```


This class presents more serious problems though. The idea of a Mesh is a confusing abstraction that has no real-world equivalent. I was confused about it even as I wrote it. Is it a container that holds vertices, indices, and other data? Is it a resource manager that loads and unloads that data from disk? Is it a renderer that sends the data to the GPU? It's all of these things.

### How to Improve

The Mesh class should be a "plain old data structure". It should have no "smarts", which means we can safely trash all the useless getters and setters and make all the fields public.

Then we can separate the resource management and rendering into separate systems which operate on the inert data. Yes, systems, not objects. Don't shoehorn every problem into an object-oriented abstraction when another abstraction might be a better fit.

The comments can be improved, mostly, by deleting them. Comments easily fall out of date and become misleading liabilities, since they're not checked by the compiler. I posit that comments should be eliminated unless they fall into one of these categories:

- Comments explaining
*why*, rather than*what*. These are the most useful. - Comments with a few words explaining what the following giant chunk of code does. These are useful for navigation and reading.
- Comments in the declaration of a data structure, explaining what each field means. These are often unnecessary, but sometimes it's not possible to map a concept intuitively to memory, and comments are necessary to describe the mapping.

## 2007-2008

I call these years "The PHP Dark Ages".

![](../../assets/a6a8a7cfa30b7629.png)

## 2009-2010

By now, I'm in college.
I'm making a Python-based third-person multiplayer shooter called *Acquire, Attack, Asplode, Pwn*.
I have no excuse at this point. The cringe just keeps getting worse, and now it comes with a healthy dose of copyright infringing background music.

When I wrote this game, the most recent piece of wisdom I had picked up was that global variables are Bad™. They lead to spaghetti code. They allow function "A" to break a completely unrelated function "B" by modifying global state. They don't work with threads.

However, almost all gameplay code needs access to the entire world state. I "solved" this problem by storing everything in a "world" object and passed the world into every single function. No more globals! I thought this was great because I could theoretically run multiple, separate worlds simultaneously.

In practice, the "world" functioned as a de facto global state container. The idea of multiple worlds was of course never needed, never tested, and I'm convinced, would never work without significant refactoring.

Once you join the strange cult of global tea-totallers, you discover a whole world of creative methods to delude yourself. The worst is the singleton:

```
class Thing
{
static Thing i = null;
public static Thing Instance()
{
if (i == null)
i = new Thing();
return i;
}
}
Thing thing = Thing.Instance();
```


Poof, magic! Not a global variable in sight! And yet, a singleton is much worse than a global, for the following reasons:

- All the potential pitfalls of global variables still apply. If you think a singleton is not a global, you're just lying to yourself.
- At best, accessing a singleton adds an expensive branch instruction to your program. At worst, it's a full function call.
- You don't know when a singleton will be initialized until you actually run the program. This is another case of a programmer lazily offloading a decision that should be made at design time.

### How to Improve

If something needs to be global, just make it global. Consider the whole of your project when making this decision. Experience helps.

The real problem is code interdependence. Global variables make it easy to create invisible dependencies between disparate bits of code. Group interdependent code together into cohesive systems to minimize these invisible dependencies. A good way to enforce this is to throw everything related to a system onto its own thread, and force the rest of the code to communicate with it via messaging.

### Boolean Parameters

Maybe you've written code like this:```
class ObjectEntity:
def delete(self, killed, local):
# ...
if killed:
# ...
if local:
# ...
```


Here we have four different "delete" operations that are highly similar, with a few minor differences depending on two boolean parameters. Seems perfectly reasonable. Now let's look at the client code that calls this function:

`obj.delete(True, False)`


Not so readable, huh?

### How to Improve

This is a case-by-case thing.
However, one piece of advice from [Casey Muratori](https://mollyrocket.com/casey/index.html) certainly applies here: **write the client code first**.
I'm sure that no sane person would write the above client code. You might write something like this instead:

`obj.killLocal()`


And *then* go write out the implementation of the killLocal() function.

### Naming

It may seem strange to focus so heavily on naming, but as the old joke goes, it's one of the two remaining unsolved problems in computer science, alongside cache invalidation and off-by-one errors.

Take a look at these functions:

```
class TeamEntityController(Controller):
def buildSpawnPacket(self):
# ...
def readSpawnPacket(self):
# ...
def serverUpdate(self):
# ...
def clientUpdate(self):
# ...
```


Clearly the first two functions are related to each other, and the last two functions are related. But they are not named to reflect that reality. If I start typing self. in an IDE, these functions will not show up next to each other in the autocomplete menu.

Better to make each name start with the general and end with the specific, like this:

```
class TeamEntityController(Controller):
def packetSpawnBuild(self):
# ...
def packetSpawnRead(self):
# ...
def updateServer(self):
# ...
def updateClient(self):
# ...
```


The autocomplete menu will make much more sense with this code.

## 2010-2015

After only 12 years of work, I actually finished a game.

Despite all I had learned up to this point, this game featured some of my biggest blunders.

### Data Binding

At this time, people were just starting to get excited about "reactive" UI frameworks like Microsoft's MVVM and Google's Angular. Today, this style of programming lives on mainly in React.

All of these frameworks start with the same basic promise. They show you an HTML text field, an empty <span> element, and a single line of code that inextricably binds the two together. Type in the text field, and pow! The <span> magically updates.

In the context of a game, it looks something like this:

```
public class Player
{
public Property<string> Name = new Property<string> { Value = "Ryu" };
}
public class TextElement : UIComponent
{
public Property<string> Text = new Property<string> { Value = "" };
}
label.add(new Binding<string>(label.Text, player.Name));
```


Wow, now the UI automatically updates based on the player's name! I can keep the UI and game code totally separate. This is appealing because we're eliminating the state of the UI and instead deriving it from the state of the game.

There were some red flags, however. I had to turn every single field in the game into a Property object, which included a list of bindings that depended on it:

```
public class Property<Type> : IProperty
{
protected Type _value;
protected List<IPropertyBinding> bindings;
public Type Value
{
get { return this._value; }
set
{
this._value = value;
for (int i = this.bindings.Count - 1; i >= 0; i = Math.Min(this.bindings.Count - 1, i - 1))
this.bindings[i].OnChanged(this);
}
}
}
```


Every single field in the game, down to the last boolean, had an unwieldy dynamically allocated array attached to it.

Take a look at the loop that notifies the bindings of a property change to get an idea of the issues I ran into with this paradigm. It has to iterate through the binding list backward, since a binding could actually add or delete UI elements, causing the binding list to change.

Still, I loved data binding so much that I built the entire game on top of it. I broke down objects into components and bound their properties together. Things quickly got out of hand.

```
jump.Add(new Binding<bool>(jump.Crouched, player.Character.Crouched));
jump.Add(new TwoWayBinding<bool>(player.Character.IsSupported, jump.IsSupported));
jump.Add(new TwoWayBinding<bool>(player.Character.HasTraction, jump.HasTraction));
jump.Add(new TwoWayBinding<Vector3>(player.Character.LinearVelocity, jump.LinearVelocity));
jump.Add(new TwoWayBinding<BEPUphysics.Entities.Entity>(jump.SupportEntity, player.Character.SupportEntity));
jump.Add(new TwoWayBinding<Vector3>(jump.SupportVelocity, player.Character.SupportVelocity));
jump.Add(new Binding<Vector2>(jump.AbsoluteMovementDirection, player.Character.MovementDirection));
jump.Add(new Binding<WallRun.State>(jump.WallRunState, wallRun.CurrentState));
jump.Add(new Binding<float>(jump.Rotation, rotation.Rotation));
jump.Add(new Binding<Vector3>(jump.Position, transform.Position));
jump.Add(new Binding<Vector3>(jump.FloorPosition, floor));
jump.Add(new Binding<float>(jump.MaxSpeed, player.Character.MaxSpeed));
jump.Add(new Binding<float>(jump.JumpSpeed, player.Character.JumpSpeed));
jump.Add(new Binding<float>(jump.Mass, player.Character.Mass));
jump.Add(new Binding<float>(jump.LastRollKickEnded, rollKickSlide.LastRollKickEnded));
jump.Add(new Binding<Voxel>(jump.WallRunMap, wallRun.WallRunVoxel));
jump.Add(new Binding<Direction>(jump.WallDirection, wallRun.WallDirection));
jump.Add(new CommandBinding<Voxel, Voxel.Coord, Direction>(jump.WalkedOn, footsteps.WalkedOn));
jump.Add(new CommandBinding(jump.DeactivateWallRun, (Action)wallRun.Deactivate));
jump.FallDamage = fallDamage;
jump.Predictor = predictor;
jump.Bind(model);
jump.Add(new TwoWayBinding<Voxel>(wallRun.LastWallRunMap, jump.LastWallRunMap));
jump.Add(new TwoWayBinding<Direction>(wallRun.LastWallDirection, jump.LastWallDirection));
jump.Add(new TwoWayBinding<bool>(rollKickSlide.CanKick, jump.CanKick));
jump.Add(new TwoWayBinding<float>(player.Character.LastSupportedSpeed, jump.LastSupportedSpeed));
wallRun.Add(new Binding<bool>(wallRun.IsSwimming, player.Character.IsSwimming));
wallRun.Add(new TwoWayBinding<Vector3>(player.Character.LinearVelocity, wallRun.LinearVelocity));
wallRun.Add(new TwoWayBinding<Vector3>(transform.Position, wallRun.Position));
wallRun.Add(new TwoWayBinding<bool>(player.Character.IsSupported, wallRun.IsSupported));
wallRun.Add(new CommandBinding(wallRun.LockRotation, (Action)rotation.Lock));
wallRun.Add(new CommandBinding<float>(wallRun.UpdateLockedRotation, rotation.UpdateLockedRotation));
vault.Add(new CommandBinding(wallRun.Vault, delegate() { vault.Go(true); }));
wallRun.Predictor = predictor;
wallRun.Add(new Binding<float>(wallRun.Height, player.Character.Height));
wallRun.Add(new Binding<float>(wallRun.JumpSpeed, player.Character.JumpSpeed));
wallRun.Add(new Binding<float>(wallRun.MaxSpeed, player.Character.MaxSpeed));
wallRun.Add(new TwoWayBinding<float>(rotation.Rotation, wallRun.Rotation));
wallRun.Add(new TwoWayBinding<bool>(player.Character.AllowUncrouch, wallRun.AllowUncrouch));
wallRun.Add(new TwoWayBinding<bool>(player.Character.HasTraction, wallRun.HasTraction));
wallRun.Add(new Binding<float>(wallRun.LastWallJump, jump.LastWallJump));
wallRun.Add(new Binding<float>(player.Character.LastSupportedSpeed, wallRun.LastSupportedSpeed));
player.Add(new Binding<WallRun.State>(player.Character.WallRunState, wallRun.CurrentState));
input.Bind(rollKickSlide.RollKickButton, settings.RollKick);
rollKickSlide.Add(new Binding<bool>(rollKickSlide.EnableCrouch, player.EnableCrouch));
rollKickSlide.Add(new Binding<float>(rollKickSlide.Rotation, rotation.Rotation));
rollKickSlide.Add(new Binding<bool>(rollKickSlide.IsSwimming, player.Character.IsSwimming));
rollKickSlide.Add(new Binding<bool>(rollKickSlide.IsSupported, player.Character.IsSupported));
rollKickSlide.Add(new Binding<Vector3>(rollKickSlide.FloorPosition, floor));
rollKickSlide.Add(new Binding<float>(rollKickSlide.Height, player.Character.Height));
rollKickSlide.Add(new Binding<float>(rollKickSlide.MaxSpeed, player.Character.MaxSpeed));
rollKickSlide.Add(new Binding<float>(rollKickSlide.JumpSpeed, player.Character.JumpSpeed));
rollKickSlide.Add(new Binding<Vector3>(rollKickSlide.SupportVelocity, player.Character.SupportVelocity));
rollKickSlide.Add(new TwoWayBinding<bool>(wallRun.EnableEnhancedWallRun, rollKickSlide.EnableEnhancedRollSlide));
rollKickSlide.Add(new TwoWayBinding<bool>(player.Character.AllowUncrouch, rollKickSlide.AllowUncrouch));
rollKickSlide.Add(new TwoWayBinding<bool>(player.Character.Crouched, rollKickSlide.Crouched));
rollKickSlide.Add(new TwoWayBinding<bool>(player.Character.EnableWalking, rollKickSlide.EnableWalking));
rollKickSlide.Add(new TwoWayBinding<Vector3>(player.Character.LinearVelocity, rollKickSlide.LinearVelocity));
rollKickSlide.Add(new TwoWayBinding<Vector3>(transform.Position, rollKickSlide.Position));
rollKickSlide.Predictor = predictor;
rollKickSlide.Bind(model);
rollKickSlide.VoxelTools = voxelTools;
rollKickSlide.Add(new CommandBinding(rollKickSlide.DeactivateWallRun, (Action)wallRun.Deactivate));
rollKickSlide.Add(new CommandBinding(rollKickSlide.Footstep, footsteps.Footstep));
```


I ran into tons of problems. I created binding cycles that caused infinite loops. I found out that initialization order is often important, and initialization is a nightmare with data binding, with some properties getting initialized multiple times as bindings are added.

When it came time to add animation, I found that data binding made it difficult and non-intuitive to animate between two states.
And this isn't just me.
Watch [this Netflix talk](https://youtu.be/g01dGsKbXOk?t=18m11s) which gushes about how great React is before explaining how they have to turn it off any time they run an animation.

I too realized the power of turning a binding on or off, so I added a new field:

```
class Binding<T>
{
public bool Enabled;
}
```


Unfortunately, this defeated the purpose of data binding.
I wanted to get rid of UI state, and this code actually *added* some.
How can I eliminate this state?

I know! Data binding!

```
class Binding<T>
{
public Property<bool> Enabled = new Property<bool> { Value = true };
}
```


Yes, I really did try this briefly. It was bindings all the way down. I soon realized how crazy it was.

How can we improve on data binding? Try making your UI actually functional and stateless.
[dear imgui](https://github.com/ocornut/imgui) is a great example of this.
Separate behavior and state as much as possible.
Avoid techniques that make it easy to create state.
It should be a pain for you to create state.

## Conclusion

There are many, many more embarrassing mistakes to discuss. I discovered another "creative" method to avoid globals. For some time I was obsessed with closures. I designed an "entity" "component" "system" that was anything but. I tried to multithread a voxel engine by sprinkling locks everywhere.

Here's the takeaway:

- Make decisions upfront instead of lazily leaving them to the computer.
- Separate behavior and state.
- Write pure functions.
- Write the client code first.
- Write boring code.

That's my story. What horrors from your past are you willing to share?

If you enjoyed this article, try these: