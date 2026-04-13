---
title: Implementing transitions between screens
url: https://blog.gemserk.com/2012/03/05/implementing-transitions-between-screens/
published: '2012-03-05'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Using transitions between game screens is a great way to provide smoothness between screen changes, for example, fade out one screen and then fade in the next one. The next video shows an example of those effects our Vampire Runner game.

In this post, we will show a possible implementation of transitions between screens using LibGDX, however the code should be independent enough to be easily ported to other frameworks.

Although we implemented it using the our own concept of GameState, we will try to use LibGDX Screen concept in this post to simplify understandability.

### Implementation

The implementation is based in the concept of TransitionEffect. A TransitionEffect holds the render logic of one of the effects of the transition being performed.

class TransitionEffect { // returns a value between 0 and 1 representing the level of completion of the transition. protected float getAlpha() { .. } void update(float delta) { .. } void render(Screen current, Screen next); boolean isFinished() { .. } TransitionEffect(float duration) { .. } }

An implementation example of a TransitionEffect is a FadeOutTransitionEffect to perform a fade out effect:

class FadeOutTransitionEffect extends TransitionEffect { Color color = new Color(); @Override public void render(Screen current, Screen next) { current.render(); color.set(0f, 0f, 0f, getAlpha()); // draw a quad over the screen using the color } }

Then, in order to perform a transition between Screens, we need a custom Screen with the logic to apply render each transition effect and to set the next Screen when the transition is over. This is a possible implementation:

class TransitionScreen implements Screen { Game game; Screen current; Screen next; int currentTransitionEffect; ArrayList<TransitionEffect> transitionEffects; TransitionScreen(Game game, Screen current, Screen next, ArrayList<TransitionEffect> transitionEffects) { this.current = current; this.next = next; this.transitionEffects = transitionEffects; this.currentTransitionEffect = 0; this.game = game; } void render() { if (currentTransitionEffect >= transitionEffects.size()) { game.setScreen(next); return; } transitionEffects.get(currentTransitionEffect).update(getDelta()); transitionEffects.get(currentTransitionEffect).render(current, next); if (transitionEffects.get(currentTransitionEffect).isFinished()) currentTransitionEffect++; } }

Finally, each time we want to perform a transition between two screens, we have to create a new TransitionScreen with the current and next Screens and a collection of effects we want. For example:

Screen current = game.getScreen(); Screen next = new HighscoresScreen(); ArrayList<TransitionEffect> effects = new ArrayList<TransitionEffect>(); effects.add(new FadeOutTransitionEffect(1f)); effects.add(new FadeInTransitionEffect(1f)); Screen transitionScreen = new TransitionScreen(game, current, next, effects); game.setScreen(transitionScreen);

As we mention before, we use our own concepts in our implementation. If you want to see our code take a look at the classes [ApplicationListenerGameStateBasedImpl](https://github.com/gemserk/commons-gdx/blob/f61dfb865eabbe6b61ba4617ff7bb35b922f54f9/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/ApplicationListenerGameStateBasedImpl.java), [GameState](https://github.com/gemserk/commons-gdx/blob/6fd62830411c1de61626aadc56e7a282014e6199/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/GameState.java) and [GameStateTransitionImpl](https://github.com/gemserk/commons-gdx/blob/90db78b3aa0c8786bec19c76f9f8634402b1bcef/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/GameStateTransitionImpl.java) (do not expect the best code in the world).

### Conclusion

Adding transitions between the game screens gives users a feeling of smoothness, and we believe it worth the effort.

Also, we like the current design lets you implement different effects for the transitions, we only shown fade out and fade in as example because they are really simple to implement and we are using only those for our games.

As always, hope you like the post.