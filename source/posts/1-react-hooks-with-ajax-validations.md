---
date: 2020-03-30T22:42:00
pageTitle: 1 - React Hooks and Ajax Validations
tags: posts
---
I hope I can save someone the hours I spent debugging this. This post will assume a tiny bit of react knowledge.

# React Hooks
[React Hooks](https://reactjs.org/docs/hooks-intro.html) are cool, right? No more writing long-winded constructors, or `this.someFunction = this.someFunction.bind(this)` because classes don't auto bind. None of the headaches!

_Narrator (hopefully Wayne June): That's what he thinks._

All you have to do is `useState` for state variables and `useEffect` instead of componentDidMount. I've started using hooks everywhere, for every component I write. They make gigantic classical components into tiny, streamlined, easy-to-read functions.

# Ajax Validations
A few weeks ago, I came upon an interesting problem. We have a form that accepts a string which has to be unique in the context of a select box. The combination of the two is a huge amount of data, so getting it all ahead of time would slow down page load. A lot. So we made an ajax validation method. This is where our troubles began.

## Regular Ajax Calls
Normally when you're making an ajax call from a component you are just doing it once. So you can do something like this:
```jsx
import React, { useState, useEffect } from 'react';
import LoadingSpinner from 'loading_spinner';

const SimpleAjaxComponent = () => {
    const [data, setData] = useState(null);
    useEffect(() => {
        ajaxForData().then(response => { setData(response) });
    }, []); // empty array means this only happens on initial render

    return (
        data ?
        <div>{data}</div> :
        <LoadingSpinner />
    );
}
```

## Validations
If we change the above call to a validation, then instead of firing only once we want it to fire only once ...each time the user stops typing. Easy enough, Lodash has a function for exactly this case: [`debounce`](https://lodash.com/docs/#debounce). Let's implement it:
```jsx
import React, { useState, useEffect } from 'react';
import debounce from 'lodash/debounce';

const SimpleForm = () => {
    const [value, setValue] = useState('');
    const [valid, setValid] = useState(false);
    const validate = debounce(() => {
        ajaxForData(value).then(response => setValid(response));
    }, 1000); // run this only once per second
    useEffect(validate, [value]); // run this only when the value changes

    return <input value={value} onChange={setValue} isInvalid={!valid} />;
}
```

This looks great! But it doesn't work. Can you guess why?

# Why not, Caleb?
`validate` is defined inside our component so we can [close over](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) the `setValid` function. This is great,  but it exposes some behavior of react that only causes a bug in this (rare) case.

Every time this component is rendered (and react likes to render [early and often](https://thoughtbot.com/blog/react-rendering-misconception)), we are redefining this validate function which creates a brand new function. The `const` here feels misleading because this isn't a constant. It's never changed within the scope of SimpleForm, but it's dropped and re-created each render.

For most functions, this doesn't matter since the contents of the function are the same. But for `debounce`d functions, it makes a huge difference: The callback is called after 1 second as expected, but also after 1.1 seconds, and 1.2 seconds, etc. It's called as many times as the debounced function is called: for every single change. If you type `hello`, the callback is fired 5 times.

# A Solution
Fortunately, the people who work on react are smart people, and they realized that useState and useEffect would not be enough to replace all the things you can do in a classical component. They also added [`useCallback`](https://reactjs.org/docs/hooks-reference.html#usecallback). I'll quote their docs here:

> Returns a memoized callback.

Memoization just means they keep using the same function each time. Since we use the same function, `debounce` works. Here's how that looks:
```jsx
import React, { useState, useCallback, useEffect } from 'react';
import debounce from 'lodash/debounce';

const SimpleForm = () => {
    const [value, setValue] = useState('');
    const [valid, setValid] = useState(false);
    const validate = useCallback(debounce((value) => {
        ajaxForData(value).then(response => setValid(response));
    }, 1000); // run this only once per second

    useEffect(() => {
        // we have to pass in `value`. Otherwise useCallback will enclose
        // only the initial value instead of the current one each time.
        validate(value)
    }, [value]); // run this only when the value changes

    return <input value={value} onChange={setValue} isInvalid={!valid} />;
}
```

# Takeaways
- `const` is not actually constant, just cannot be mutated while in scope
- `useCallback` when you need to re-use the same function
- React's new hooks are great, and you should use them!
