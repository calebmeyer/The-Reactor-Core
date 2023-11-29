---
date: 2023-11-29T14:10:31
pageTitle: 15 - Testing Apollo GraphQL Mutations
tags: posts
---

Recently, I've started working with Apollo's GraphQL implementation for JavaScript. One pattern that you'll sometimes see in GraphQL land is to pass in some callbacks for a mutation's lifecycle:

```javascript
import { gql, useMutation } from "@apollo/client";

const mutationText = gql`
  mutation AddToShoppingList {
    item
  }
`;
const callbacks = {
  onError: (error) => {
    console.error(error);
    throw error;
  },
  onComplete: () => {
    updateShoppingList();
  },
};

const [addToList, { loading }] = useMutation(mutationText, callbacks);
```

## Testing with Jest

Over on the testing side, it's very easy to validate some of this. For example, if you want to test that useMutation was called with the correct text and callbacks, you can do something like this:

```javascript
it("calls useMutation with the correct mutation and callbacks", () => {
  expect(useMutation).toHaveBeenCalledWith(mutationText, {
    onError: expect.any(Function),
    onComplete: expect.any(Function),
  });
});
```

But it stumped me for a long while how I could test that onError was called, or that onComplete was called. Today, I figured it out thanks to some clever hacks to test redux.

If you do an `import *` in your test file, you can `jest.spyOn` its functions. If you change `useMutation` to be spied upon, you can add your own mock implementation. That mock implementation can call your callbacks. In action, it looks like this:

```javascript
import * as apolloClient from '@apollo/client';

describe('File under test', () => {
    let addMock;

    beforeEach(() => {
        addMock = jest.fn();

        jest.spyOn(apolloClient, 'useMutation').mockImplementation((mutation, callbacks) => {
            if (callbacks.onError) {
                try {
                    // call the real onError handler for coverage
                    callbacks.onError(new Error());
                }
            }

            if (callbacks.onComplete) {
                // call the real onComplete handler for coverage
                callbacks.onComplete();
            }

            // it's important that we return what the useMutation call is expecting
            return [addMock, { loading: true }];
        });
    });

    // actual tests go here
});
```
