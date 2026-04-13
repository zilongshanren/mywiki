---
title: Rust Game Series - Part 13 - Modules
url: https://www.jendrikillner.com/post/rust-game-part-13/
author: Jendrik Illner
published: '2020-05-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

## Goal

At the end of this post, the game state management will be separated into multiple files. The Rust module system is taken advantage of to further separate public interfaces from implementation details.

## Overview

Right now, the functionality for both supported game states (Pause and Gameplay) is contained in main.rs and caused this file to grow to an unwieldy 500+ lines.

It’s time to split this file up. The two options are modules in separate files or crates. For this purpose, I think crates are overkill, and I will be moving it into a hierarchy of modules.

### Hierarchy of modules

In Rust, each file implicitly defines a module of the same name as the file. Adding a file called pause.rs, for example, will create a pause module. Files structured in a hierarchy will also define a hierarchical module structure.

With this in mind the file structure I decided on:

```
src/
main.rs
gamestates.rs
gamestates/
pause.rs
gameplay.rs
```


Therefore the pause state functionality will be found in `gamestates::pause`


and the gameplay in
`gamestates::gameplay`


The gamestates.rs and the folder gamestates belong together. This is one of the two option to define the root of a module.

There is another option using a file called mod.rs such as this:

```
src/
main.rs
gamestates/
pause.rs
gameplay.rs
mod.rs
```


This was the only way until Rust 2018, but I prefer the new way because it makes it easier to search for a file by name.

Imaging your project grows, and you might have a lot of modules and therefore, a lot of files called mod.rs. This sounds like a nightmare to find to me.

But what is the purpose of mod.rs or gamestates.rs?

For a module to be included in the compilation, it needs to be referenced. This is done using the mod keyword. I like to put these at the top of the files, so it’s easy to see.

```
// these make sure we compile the modules
mod gamestates;
```


This statement will cause the gamestates module to be compiled for the current compilation unit.
`gamestates.rs`

then list all the modules that will be included in the compilation if gamestates is requested.

```
// compile all the game states
mod gameplay;
mod pause;
```


Additionally, you might include functionality in this file that connects the pieces of the child modules together. I am doing that, more on that later.

For now, we only have created the file structure but not moved any code around.

### Moving code into modules

With the file structure created we can copy all the PauseState related functionality into pause.rs. Only doing that is, of course, not enough. A lot of errors along these lines are greeting me.

```
error[E0425]: cannot find function `create_pso` in this scope
--> match3_game\src\gamestates\pause.rs:13:66
|
| let screen_space_quad_blended_pso: PipelineStateObject = create_pso(
| ^^^^^^^^^^ not found in this scope
| help: possible candidate is found in another module, you can import it into scope
|
| use graphics_device::create_pso;
```


The compiler is very helpful and tells you quite detailed what the problem is. By default, we can only access functions, structs, … that are defined in the same module.

If we want to access these elements, we need to explicitly opt-in. And the compiler error shows one of the possible ways to resolve it.

If you are using the Rust extension for [Visual Studio](https://marketplace.visualstudio.com/items?itemName=dos-cafe.Rust) it will provide you a quick fix for this error:

![](../../assets/d62e974c883dd9da.png)


There are multiple ways to achieve this, see the [rust book](https://doc.rust-lang.org/1.27.2/book/second-edition/ch07-03-importing-names-with-use.html) for more details.

But the TLDR version is:

If we have multiple imports from the same module, we can group them

```
// instead of listing them individually
use graphics_device::create_pso;
use graphics_device::create_texture;
// grouped imports from graphics_device module
use graphics_device::{create_pso, create_texture};
```


To reference something one level above us in the hierarchy use

```
use super::GameStateType
```


To reference something defined in the root of the crate use

```
use crate::Float2;
```


Having fixed up all the missing references, we are greeted with a new error from main.rs

```
use crate::pause::PauseStateStaticData;
^^^^^^^^^^^^^^^^^^^^ this struct is private
```


The reason for this is that by default, all types in Rust are private. They can only be accessed from the current module. We need explicitly annotate all types and functions that we would like to access from outside the module.

This can be done like below:

```
pub struct PauseStateFrameData {
fade_in_status: f32,
}
impl PauseState<'_> {
pub fn new<'a>(device_layer: &GraphicsDeviceLayer) -> PauseState<'a> { ... }
}
pub fn draw_pause_state( ... )
```


Small gotcha, the impl cannot have a pub modifier.

We will need to expose all public types that are used directly or are used in a public interface. If we don’t we get errors like these:

```
error[E0446]: private type `UpdateBehaviourDesc` in public interface
--> match3_game\src\pause.rs:68:1
|
68 | / pub fn update_pause_state(
69 | | prev_frame_params: &PauseStateFrameData,
70 | | frame_params: &mut PauseStateFrameData,
71 | | messages: &Vec<WindowMessages>,
... |
93 | | }
94 | | }
| |_^ can't leak private type
```


The error message is, once again, very clear about the problem.
`update_pause_state`

has been made public but it uses the private type `UpdateBehaviourDesc`

in the public interface (return type in this case)

Therefore we need to make that type public too. This only makes the type public but not the members themselves. So you don’t need to worry about outside code modifying members directly.

Once all these errors are fixed, the game should still run and look exactly the same. Just the code is easier to manage :)

## Structure Changes

Furthermore, I decided to move all the game state related logic out of the main game loop. The logic for switching states, updating and drawing states makes it more challenging to see the core of the main game loop.

Gamestates.rs is the root of the module and is, therefore, the perfect place to implement such functionality. It provides the interface between the game and the game states.

It contains the types:

```
pub enum GameStateType {
Pause,
Gameplay,
}
pub enum GameStateTransitionState {
Unchanged,
TransitionToNewState(GameStateType),
ReturnToPreviousState,
}
...
```


And functions such as these:

```
pub fn execute_possible_state_transition(
state_transition: GameStateTransitionState,
game_state_stack: &mut Vec<GameStateData>,
graphics_layer: &GraphicsDeviceLayer,
) {
```


One part to point out for this function is that the ownership of `state_transition`

is moved into `execute_possible_state_transition`

and not passed as a reference like all other arguments.

`GameStateTransitionState`

is used to track how the game states should be updated.
Either we can keep the state unchanged, add a new state, or remove game states.

Since `execute_possible_state_transition`

will do this transition internally the `state_transition`

we pass in will not be valid after the function returns. Moving ownership into the function makes the original variable unusable, and Rust will throw an error if we forget to reset it afterward

```
115 | let mut next_game_state: GameStateTransitionState =
| ------------------- move occurs because `next_game_state` has type `gamestates::GameStateTransitionState`, which does not implement the `Copy` trait
...
142 | execute_possible_state_transition( next_game_state, &mut game_state_stack, &graphics_layer );
| ^^^^^^^^^^^^^^^ value moved here, in previous iteration of loop
```


This error is not super clear to read at first, but the simplified logic is below.

```
let mut next_game_state: GameStateTransitionState =
GameStateTransitionState::TransitionToNewState(GameStateType::Gameplay);
while !should_game_close {
execute_possible_state_transition(next_game_state, &mut game_state_stack, &graphics_layer);
// from now on next_game_state is invalid and cannot be acessed
}
```


`next_game_state`

is defined before we enter the main loop.
Inside of the loop we move the `next_game_state`

ownership into the `execute_possible_state_transition`

function.

Once this function returns, the original variable cannot be accessed anymore. Since it lost the ownership of the value.

The fix for this is quite simple:

```
execute_possible_state_transition(next_game_state, &mut game_state_stack, &graphics_layer);
// assign a new value to next_game_state
// therefore we can access it again in the next iteration of the loop
next_game_state = GameStateTransitionState::Unchanged;
```


I like code being explicit and straightforward, and this clearly shows while scanning the code that the state transition state will be reset after `execute_possible_state_transition`

returns.

If we passed it by reference, Rust compiler would not warn, and we might forget to reset the variable. Causing a run-time logic error instead of a compile-time error.

And that’s it for now. Main.rs is back to ~200 lines of code. There is more that could be moved around, but I will do that another time when I have a better idea of how the design will evolve.

## Next Part

It seems like it’s time for some more exciting visuals. Going to implement texture loading support next.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-13)