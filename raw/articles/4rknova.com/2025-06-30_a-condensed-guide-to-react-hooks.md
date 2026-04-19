---
title: A condensed guide to React hooks
url: https://www.4rknova.com/blog/2025/06/30/react-hooks
author: Nikolaos Papadopoulos
published: '2025-06-30'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Since their introduction in React 16.8, hooks have revolutionized the way developers write functional components. But with so many available, from `useState`

to `useDeferredValue`

, knowing when and how to use each can get confusing.

This guide breaks down the most commonly used React hooks, compares them side-by-side, and outlines practical use cases and gotchas you should avoid.

# Most common React hooks at a glance

| Hook | Purpose | Common Use Case | Common Gotchas |
|---|---|---|---|
|

[useEffect](https://react.dev/reference/react/useEffect)[useContext](https://react.dev/reference/react/useContext)[useRef](https://react.dev/reference/react/useRef)[useCallback](https://react.dev/reference/react/useCallback)[useMemo](https://react.dev/reference/react/useMemo)[useReducer](https://react.dev/reference/react/useReducer)[useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)[useImperativeHandle](https://react.dev/reference/react/useImperativeHandle)[useDeferredValue](https://react.dev/reference/react/useDeferredValue)[useDebugValue](https://react.dev/reference/react/useDebugValue)# When to use each and why

Purpose | Local state in function components. |
|---|---|
Considerations | - Even setting the same value re-renders the component. |
| - Updating state is async; changes are batched. |

```
import { useState } from 'react';
function Counter() {
// Declare a state variable 'count' initialized to 0
// 'setCount' is the function to update 'count'
const [count, setCount] = useState(0);
// Render a button that displays the current count
// On click, increment the count by 1 using setCount
return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```


Purpose | Perform side effects after rendering. |
|---|---|
Considerations | - Runs after paint, not blocking UI. |
| - Clean up side effects with a return function. | |
| - Dependencies are critical to prevent loops or stale data |

```
import { useState, useEffect } from 'react';
function Timer() {
// Declare a state variable 'seconds' initialized to 0
// 'setSeconds' is the function to update 'seconds'
const [seconds, setSeconds] = useState(0);
useEffect(() => {
// Set up an interval that increments 'seconds' every 1000ms (1 second)
// Using functional update form to always get the latest state value
const interval = setInterval(() => setSeconds(s => s + 1), 1000);
// Cleanup function to clear the interval when the component unmounts
// This prevents memory leaks and stops the timer
return () => clearInterval(interval);
}, []); // Empty dependency array means this effect runs only once on mount
// Render the elapsed time in seconds
return <p>Time: {seconds}s</p>;
}
```


Purpose | Access context value from nearest provider. |
|---|---|
Considerations | - Re-renders on context value change. |
| - Avoid deep updates unless necessary. |

```
import { createContext, useContext } from 'react';
// Create a Context object named ThemeContext.
// The argument 'light' is the default value for the context.
// This value will be used if no Provider wraps a component consuming this context.
const ThemeContext = createContext('light');
function ThemedButton() {
// useContext is a React hook that subscribes to the nearest ThemeContext
// provider above in the tree. It returns the current context value.
// If no Provider is found, it returns the default value ('light').
const theme = useContext(ThemeContext);
// Render a button element.
// - The button's CSS class is set to the current theme ('light' or any
// other provided value).
// - The button text displays the current theme.
return <button className={theme}>Theme: {theme}</button>;
}
function App() {
return (
// Wrap ThemedButton inside ThemeContext.Provider to override the default
// context value.
// - The value prop sets the current context value ('dark' here).
// - All components inside this Provider can access 'dark' as the theme.
<MyContext.Provider value="dark">
<ThemedButton />
</MyContext.Provider>
);
}
```


Purpose | Persistent mutable value or DOM reference. |
|---|---|
Considerations | - Changing `ref.current` does not cause re-render. |
| - Useful for timers, DOM access, or instance tracking. |

Example with DOM reference

```
import { useRef, useEffect } from 'react';
function FocusInput() {
// Create a ref object that will be attached to the input element below
// useRef returns a mutable object with a `.current` property
// Initially, `.current` is set to null because the element is not rendered yet
const inputRef = useRef(null);
// useEffect hook runs side effects after the component has rendered
// The empty dependency array means this effect runs only once, right after the
// first render
useEffect(() => {
// Access the current value of the ref, which points to the input DOM element
// Call the focus() method to set keyboard focus on this input element
if (inputRef.current) {
inputRef.current.focus();
}
}, []); // Empty array ensures effect runs only on mount
// Render an input element with the ref attached
// The placeholder attribute provides user-friendly text when input is empty
return <input ref={inputRef} placeholder="Focus on load" />;
}
```


Example with presistent mutable value

```
import { useRef } from 'react';
function Counter() {
// Initialize a ref object with the initial value 0.
// Unlike state, updating this value does NOT cause a re-render.
// This ref is a container whose `.current` property can be mutated.
const countRef = useRef(0);
// Function to increment the count stored in the ref
const increment = () => {
// Update the current value of the ref by adding 1
countRef.current += 1;
// Log the updated count to the console
// Note: This update won't trigger a re-render, so the UI won't
// update automatically
console.log('Current count:', countRef.current);
};
return (
<div>
{/* Button that calls increment on click */}
<button onClick={increment}>Increment Count</button>
{/* Inform the user to check the console for the count value */}
<p>Open the console to see the count value update.</p>
</div>
);
}
```


Purpose | Memoize a function to prevent unnecessary re-creation. |
|---|---|
Considerations | - Use when passing callbacks to child components. |
| - Only re-creates if dependencies change. | |
| - Adds complexity if overused unnecessarily |

```
import { useCallback, useState } from 'react';
// Button component accepts a prop called `onClick` which is a function
// When the button is clicked, it triggers the onClick function passed
// from props
function Button({ onClick }) {
return <button onClick={onClick}>Click me</button>;
}
// Counter component maintains a count state and provides a function
// to increment it
function Counter() {
// Declare a state variable `count` initialized to 0, and a setter
// function `setCount`
const [count, setCount] = useState(0);
// Create a memoized increment function using useCallback hook.
// This function increments the current count by 1.
// The empty dependency array `[]` ensures that the same function
// instance is returned on every render, avoiding unnecessary
// re-renders of child components that depend on this function.
const increment = useCallback(() => setCount(c => c + 1), []);
// Render the Button component and pass the `increment` function a
// as the onClick handler. When the button inside Button is clicked,
// it will call `increment` and increase the count.
return <Button onClick={increment} />;
}
```


Purpose | Memoize expensive computations. |
|---|---|
Considerations | - Avoid overuse; only for expensive calculations. |
| - Depends on accurate dependency list. |

```
import { useMemo } from 'react';
function ExpensiveComponent({ input }) {
// useMemo is used to memoize the result of an expensive calculation.
// The function inside useMemo will only re-run when the `input` value
// changes. This helps avoid unnecessary recalculations on every render,
// improving performance especially when the calculation is heavy.
const computed = useMemo(() => {
// Simulate expensive work: initialize a total sum variable.
let total = 0;
// Perform a large number of iterations to simulate a CPU-heavy task.
// Each iteration multiplies the current index by the input value and
// adds it to total.
for (let i = 0; i < 1000000; i++) {
total += i * input;
}
// Return the computed total after the loop finishes.
return total;
}, [input]); // Dependency array: re-run this effect only if `input` changes.
// Render the computed result inside a paragraph element.
return <p>Computed: {computed}</p>;
}
```


Purpose | Manage complex or multi-step state logic. |
|---|---|
Considerations | - Good for managing state transitions. |
| - Makes logic more testable and maintainable. | |
| - Can be excessive for basic state needs. |

```
import { useReducer } from 'react';
// useReducer is a hook used to manage state logic in a more predictable
// way compared to useState, especially for complex state updates.
function reducer(state, action) {
// This is the reducer function that determines how the state
// should change based on the dispatched action.
// It takes two arguments:
// 1. state: the current state
// 2. action: an object describing what change should be made
switch (action.type) {
case 'increment':
// If the action type is 'increment', return a new state object
// with the count property increased by 1.
return { count: state.count + 1 };
default:
// If the action type is not recognized, return the current
// state unchanged.
return state;
}
}
function Counter() {
// The Counter component uses the useReducer hook to manage the count state.
// useReducer returns an array with two elements:
// 1. state: the current state object ({ count: 0 } initially)
// 2. dispatch: a function to send actions to the reducer to update state
const [state, dispatch] = useReducer(reducer, { count: 0 });
return (
// Render a button displaying the current count.
// When the button is clicked, it calls dispatch with an action
// object { type: 'increment' } which triggers the reducer to update
// the state by incrementing the count.
<button onClick={() => dispatch({ type: 'increment' })}>
Count: {state.count}
</button>
);
}
```


Purpose | Side effects before paint. |
|---|---|
| Use when you need to measure layout before painting | |
Considerations | - Blocks browser paint; use only if needed. |
| - Useful for measuring DOM size. |

```
import { useLayoutEffect, useRef } from 'react';
function Measure() {
// Create a ref object to hold a reference to the DOM element
// Initially, ref.current is undefined until the div is mounted
const ref = useRef();
// useLayoutEffect runs synchronously after all DOM mutations,
// but before the browser has painted.
// This makes it perfect for measuring DOM elements before the user
// sees the result.
useLayoutEffect(() => {
// Access the current DOM element using ref.current
// and log its offsetWidth (the layout width including padding and border)
console.log('Width:', ref.current.offsetWidth);
}, []); // Empty dependency array means this effect runs only once after
// the component mounts
// Render a div element with a ref attached to it
// When this div mounts, ref.current will point to this DOM node
return <div ref={ref}>Measure me</div>;
}
```


Purpose | Customize instance value exposed via `ref` . |
|---|---|
Use in combination with `forwardRef` to expose imperative API | |
Considerations | - Use with `forwardRef` . |
| - Avoid overusing; prefer declarative patterns. |

```
import { useImperativeHandle, useRef, forwardRef } from 'react';
// CustomInput component wrapped with forwardRef to accept a ref from its parent
const CustomInput = forwardRef((props, ref) => {
// Create a local ref to access the actual input DOM element
const inputRef = useRef();
// Customize the instance value that is exposed to the parent when using ref
useImperativeHandle(ref, () => ({
// Expose a `focus` method that allows the parent to focus the input element
focus: () => inputRef.current.focus(),
}));
// Render the input element with the local ref attached
return <input ref={inputRef} />;
});
function Form() {
// Create a ref that will be passed down to CustomInput
const ref = useRef();
return (
<>
{/* Pass the ref to CustomInput so the parent can call imperative methods */}
<CustomInput ref={ref} />
{/* Button that calls the exposed focus method on the input when clicked */}
<button onClick={() => ref.current.focus()}>Focus input</button>
</>
);
}
```


Purpose | Defer rendering non-urgent updates. |
|---|---|
| Helps defer expensive UI updates (e.g., filtering large lists) | |
Considerations | - Helps keep UI responsive with heavy updates. |
- Works well with `startTransition` . | |
- Doesn’t delay rendering, just de-prioritizes updates |

```
import { useState, useDeferredValue } from 'react';
// Component that renders the search results
function SearchResults({ query }) {
// useDeferredValue allows React to defer the update of this value
// so that more urgent updates (like typing in input) don't get blocked.
// This helps avoid UI jank when rendering heavy components.
const deferredQuery = useDeferredValue(query);
// Simulate a heavy computation by creating 2000 divs,
// each rendering the deferred query string.
// Rendering 2000 elements can be slow, so deferring this helps keep input responsive.
const results = Array(2000).fill().map((_, i) => (
<div key={i}>{deferredQuery}</div>
));
// Render the list of divs containing the deferred query.
return <div>{results}</div>;
}
function App() {
// State to hold the current value of the input box.
const [input, setInput] = useState('');
return (
<div>
{/* Controlled input field for typing the query */}
<input
value={input}
onChange={e => setInput(e.target.value)}
placeholder="Type to search..."
/>
{/* Render the search results, passing the current input as query */}
<SearchResults query={input} />
</div>
);
}
```


Purpose | Display debug information for custom hooks in React DevTools. |
|---|---|
Considerations | - Has no effect on behavior or rendering. |
| - Use with custom hooks to expose helpful labels or values. | |
| - Can format expensive values conditionally. |

```
import { useDebugValue, useState, useEffect } from 'react';
// Custom hook: Tracks the user's online/offline status
function useOnlineStatus() {
// Initialize state with the browser's current online status
const [isOnline, setIsOnline] = useState(navigator.onLine);
useEffect(() => {
// Define a handler to update state when online status changes
const updateStatus = () => setIsOnline(navigator.onLine);
// Listen for the 'online' and 'offline' events
window.addEventListener('online', updateStatus);
window.addEventListener('offline', updateStatus);
// Cleanup listeners on unmount to prevent memory leaks
return () => {
window.removeEventListener('online', updateStatus);
window.removeEventListener('offline', updateStatus);
};
}, []); // Empty dependency array means this effect runs once on mount
// DevTools helper: shows current hook value in React DevTools
// Helps with debugging this custom hook during development
useDebugValue(isOnline ? 'Online' : 'Offline');
// Return current online status to consuming components
return isOnline;
}
// Component that uses the custom hook to show connection status
function StatusIndicator() {
// Get the online status from the custom hook
const isOnline = useOnlineStatus();
// Render the status to the user
return <span>{isOnline ? 'Online' : 'Offline'}</span>;
}
```


## Common Mistakes

- Using hooks
**conditionally**- always call them in the same order - Omitting dependencies in
`useEffect`

,`useCallback`

, or`useMemo`

- Expecting
`useRef`

updates to trigger re-renders - Overusing memoization hooks — they can reduce performance in simple apps

# Side Effects

In React, a side effect is anything that happens outside the scope of rendering your component. This includes interactions with:

- the browser (e.g., document, window)
- network requests (e.g., fetch)
- timers, subscriptions, or manual DOM manipulation

Common Examples of Side Effects are:

- Fetching data from an API
- Subscribing to a WebSocket or event listener
- Modifying the DOM manually
- Logging or analytics calls
- Setting up timers (setTimeout, setInterval)

React’s rendering should be pure. Given the same props and state, it should always return the same UI. Side effects break that purity, so they need to be handled outside of the render cycle, typically in a hook like:

- useEffect, for most effects
- useLayoutEffect, when timing is critical
- useInsertionEffect, for styling-related effects (rare)

## Side Effects Inside Render = Bad

```
// Don't do this inside a component body
fetch('/data').then(...)
```


This would fire on every render, which is inefficient and potentially buggy. Instead, use:

```
useEffect(() => {
fetch('/data').then(...);
}, []);
```


This ensures the side effect runs once after the component is mounted.

# Summary

| Hook | State | Side Effects | Performance | DOM Access | Advanced |
|---|---|---|---|---|---|
|

[useEffect](https://react.dev/reference/react/useEffect)[useContext](https://react.dev/reference/react/useContext)[useRef](https://react.dev/reference/react/useRef)[useCallback](https://react.dev/reference/react/useCallback)[useMemo](https://react.dev/reference/react/useMemo)[useReducer](https://react.dev/reference/react/useReducer)[useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)[useImperativeHandle](https://react.dev/reference/react/useImperativeHandle)[useDeferredValue](https://react.dev/reference/react/useDeferredValue)[useDebugValue](https://react.dev/reference/react/useDebugValue)State | The hook helps store or manage component state. |
Side Effects | The hook is used to perform effects outside of rendering. |
Performance | The hook is primarily used for performance optimizations. |
DOM Access | The hook can be used to interact with or reference DOM elements. |
Advanced | The hook is considered advanced or specialized, often used less frequently or requiring deeper understanding. |

# Re-render behavior

| Hook | Causes Re-render? | Notes |
|---|---|---|
|

`setState`

is called with a new value.[useEffect](https://react.dev/reference/react/useEffect)[useContext](https://react.dev/reference/react/useContext)[useRef](https://react.dev/reference/react/useRef)`ref.current`

does not trigger a re-render.[useCallback](https://react.dev/reference/react/useCallback)[useMemo](https://react.dev/reference/react/useMemo)[useReducer](https://react.dev/reference/react/useReducer)`dispatch`

is called and the state changes.[useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)[useImperativeHandle](https://react.dev/reference/react/useImperativeHandle)`forwardRef`

; does not trigger re-render.[useDeferredValue](https://react.dev/reference/react/useDeferredValue)**deferred**re-render when the input value changes.[useDebugValue](https://react.dev/reference/react/useDebugValue)# Custom hooks

A custom hook is essentially a reusable function that can call other hooks like useState, useEffect, etc., and encapsulate a specific piece of logic that you might want to use in multiple components.

Custom hooks follow the same rules as built-in hooks:

- Only call hooks at the top level
- Only call hooks from React functions
- Custom hooks must start with ‘use’ so React can detect them

## Benefits of custom hooks

- Code reuse: DRY (Don’t Repeat Yourself)
- Separation of concerns: Logic is decoupled from UI

## When to use a custom hook

Use a custom hook when:

- You need the same logic (e.g., fetching data, form handling, timers) in multiple components.
- Your component is getting large and hard to manage due to logic.

### Example: useWindowWidth

```
import { useState, useEffect } from 'react';
// Custom hook to get and track the current window width
function useWindowWidth() {
// Initialize state with the current window width
// This will hold the value of the window's inner width
const [width, setWidth] = useState(window.innerWidth);
// useEffect runs side effects. Here, we set up and clean up
// an event listener
useEffect(() => {
// Define a function to handle window resize
// It updates the state with the new window width
const handleResize = () => setWidth(window.innerWidth);
// Add the resize event listener to the window
window.addEventListener('resize', handleResize);
// Return a cleanup function that removes the event listener
// This prevents memory leaks when the component unmounts
return () => window.removeEventListener('resize', handleResize);
}, []); // Empty dependency array means this effect runs only once on mount
// Return the current window width to the component that uses this hook
return width;
}
```


Usage:

```
import React from 'react';
// Import the custom hook that tracks the window's width
// This hook will return the current width of the browser window
import useWindowWidth from './useWindowWidth';
function MyComponent() {
// Call the custom hook useWindowWidth
// This returns the current window width and re-renders the component
// whenever it changes
const width = useWindowWidth();
// Return a JSX element displaying the current window width
// The text will automatically update if the window is resized
return <div>Window width is {width}px</div>;
}
```


### Example 2: useFetch

```
import { useState, useEffect } from 'react';
// Define a custom hook named useFetch that takes a URL as its input
function useFetch(url) {
// State to store the fetched data. Initially null until data is loaded.
const [data, setData] = useState(null);
// State to track the loading status. Starts as true while the fetch
// is in progress.
const [loading, setLoading] = useState(true);
// useEffect runs a side effect — here, it performs a data fetch from
// the given URL
useEffect(() => {
// Call fetch to retrieve data from the API endpoint
fetch(url)
// Convert the response to JSON format
.then(res => res.json())
// When data is successfully retrieved, store it in state and set
// loading to false
.then(data => {
setData(data); // Store the fetched data
setLoading(false); // Update loading status
});
// This effect will re-run whenever the `url` value changes
}, [url]);
// Return an object with the current data and loading status
// Components using this hook can destructure { data, loading } from it
return { data, loading };
}
```


Usage:

```
const { data, loading } = useFetch('https://api.example.com/posts');
```