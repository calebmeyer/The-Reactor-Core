---
date: 2023-10-24T16:35:52
pageTitle: 14 - Formik - Painless React Forms
tags: draft
---

I recently underwent a big form rewrite. Our app is react based, and the best library for react forms is called Formik. Today I'd like to discuss why it's great.

## What is Formik?

But first: what is formik? Formik is what you'd come up with if you built 100 forms in react and extracted what's useful from the react code for all of them. [The website](https://formik.org/docs/overview) describes it by saying:

> Formik is a small library that helps you with the 3 most annoying parts [of writing forms in react]:
>
> 1. Getting values in and out of form state
> 2. Validation and error messages
> 3. Handling form submission

I won't go into a bunch of code examples showing before and after, since the docs do exactly that. Definitely start there. That said, I will go over these three things.

### Getting values in and out of form state

In formik, there is a long lived piece of react state called `values`. Values is what the name says, the values of the inputs that make up your form. Formik gives you utilities to help you read and keep that state up to date.

`setFieldValue` will let you set the value of an individual field by name. This is probably a good time to talk about some expectations. I expect that forms:

- are wrapped in a `<form>` tag
- are made up of one or more `<input>`s, each of which have a name and a label
- have one (and preferably only one) submit button
- have zero or one cancel/reset buttons

That second bullet point is important here. If you have no inputs (or selects), you don't have a form. If your inputs don't have names, you don't have a good form. If your inputs don't have labels, you don't have an accessible form. And especially for checkboxes and radios, even sighted users rely on the labels because you can click/tap them to check the boxes.

### Validation and error messages

### Handling form submission

## useField and Friends

## Multi-page forms

## Formik Debug
