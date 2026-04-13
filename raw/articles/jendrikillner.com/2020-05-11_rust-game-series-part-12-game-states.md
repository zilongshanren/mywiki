---
title: Rust Game Series - Part 12 - Game States
url: https://www.jendrikillner.com/post/rust-game-part-12/
author: Jendrik Illner
published: '2020-05-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

## Goal

At the end of this part, I will have a small prototype. This prototype contains the general game state flow between Gameplay and Pause State. The gameplay state is rendering a grid and reacting to mouse clicks.

## Overview

I like to keep the states of the game to be independent of each other. Therefore I am going to focus on the foundation of the state management system before adding actual gameplay functionality.

All states are managed as a stack. This allows states like the Pause screen to be used for multiple use-cases. Only the pause state needs to be removed from the stack to return to the previous state.

### Game State Data Model

Each Game State has 2 lifetimes: Static and Frame

[StaticData]

[FrameData][FrameData]

There is a single copy of static data for each GameState. And two copies of FrameData since I am using a double buffering scheme.

#### Static Data

Static data is created once and cannot be modified after. This stores information such as PSOs, textures, and other read-only data.

#### Frame Data

The frame data stores all dynamic information about the state. This includes information like player score, state of the game world, etc.

The update logic will get a read-only view of the previous frame state. It’s expected to read the last state frame as input and generate a new data into the output frame data.

For this game, I am trying not to in-place modify the game state. Let’s see how this goes :)

### Game State API

The core of the API are two enums:

```
pub enum GameStateType {
//MainMenu,
Pause,
Gameplay,
}
enum GameStateData<'a> {
Gameplay(GameplayState<'a>),
Pause(PauseState<'a>),
}
```


And the types being defined like this

```
struct GameplayState {
static_data: GameplayStateStaticData,
frame_data0: GameplayStateFrameData,
frame_data1: GameplayStateFrameData,
}
```


I would have liked to store the GameplayStateFrameData as an array, but sadly Rust doesn’t allow borrowing of individual array entries in a natural way.

There are ways of doing it using iterators and/or slices. But for this use case, two variables will work just fine.

These GameStateData blocks are stored in a simple Vec to form a stack:

```
let mut game_state_stack: Vec<GameStateData> = Vec::new();
```


The state transition are yet another enum, you see I love Rust enums :P This controls which state to switch and how that state switch should happen

```
pub enum GameStateTransitionState {
Unchanged,
TransitionToNewState(GameStateType),
ReturnToPreviousState,
}
let mut next_game_state: GameStateTransitionState =
GameStateTransitionState::TransitionToNewState(GameStateType::Gameplay);
```


Game state transitions always happen at the beginning of a CPU frame, and the GameState update returns a value specifying if and how state transitions should be done.

```
match next_game_state {
GameStateTransitionState::TransitionToNewState(x) => {
match x {
GameStateType::Gameplay => {
game_state_stack.push(GameStateData::Gameplay(GameplayState::new(&graphics_layer)));
}
GameStateType::Pause => {
game_state_stack.push(GameStateData::Pause(PauseState::new(&graphics_layer)));
}
}
// make sure to reset the state
next_game_state = GameStateTransitionState::Unchanged;
}
GameStateTransitionState::ReturnToPreviousState => {
// remove the top most state from the stack
game_state_stack.pop();
// close the game once all game states have been deleted
if game_state_stack.len() == 0 {
should_game_close = true;
continue;
}
// make sure to reset the transition state
next_game_state = GameStateTransitionState::Unchanged;
}
GameStateTransitionState::Unchanged => { }
}
```


With this, we have the main transition logic in-place and only miss the logic to draw and update the game states.

Updating is done in reverse order, this allows higher-level states to block input from reaching lower levels. Each state atm returns if a state transition is required and if the input should be blocked from reaching lower levels.

```
for state in game_state_stack.iter_mut().rev() {
let state_status = match state {
GameStateData::Gameplay(game_state) => {
let (prev_frame_params, frame_params) = if update_frame_number % 2 == 0 {
(&game_state.frame_data0, &mut game_state.frame_data1)
} else {
(&game_state.frame_data1, &mut game_state.frame_data0)
};
update_gameplay_state(prev_frame_params, frame_params, &messages, dt)
}
GameStateData::Pause(game_state) => {
let (prev_frame_params, frame_params) = if update_frame_number % 2 == 0 {
(&game_state.frame_data0, &mut game_state.frame_data1)
} else {
(&game_state.frame_data1, &mut game_state.frame_data0)
};
update_pause_state(prev_frame_params, frame_params, &messages, dt)
}
};
if state_status.block_input {
messages.clear();
}
match state_status.transition_state {
GameStateTransitionState::Unchanged => {}
_ => match next_game_state {
GameStateTransitionState::Unchanged => {
next_game_state = state_status.transition_state;
}
_ => {
panic!("logic error, only one state transition per frame is allowed");
}
},
}
}
```


The drawing follows the same logic, but the drawing order is from back to front. This allows higher-level states, such as the pause state, to be drawn on top of the lower states.

### Rendering Update

A few updates on the rendering side:

- The PSO state has been extended to contain the blend state, this is required so that the pause state can draw a partially transparent overlay
- The grid is using the same shader as before. Drawing a quad for each tile. Good enough for now
- The Window API was updated so that the output size of the Window can be specified when creating the Window

## Next Part

Time to focus a little on code structure again. With all this logic, we are back >600 lines of Rust code in a single file.

Time to split it into multiple modules across different files.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-12)