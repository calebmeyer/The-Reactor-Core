---
date: 2020-05-05T19:38:00
pageTitle: 5 - Atom is learning the lessons of all of the above
tags: posts
---
This post is heavily inspired by Mike Kozlowski's post [Vim's Big Idea](https://medium.com/@mkozlows/why-atom-cant-replace-vim-433852f4b4d1), but I'm going to take it in a slightly different direction. In Mike's post, he starts off by talking about the fantastic ideas that came from 1976. Emacs had the great idea that every part of your editing experience should be customizable, and in the same language as the editor was written. Vim had the great idea of using keys as verbs and nouns (so you can say `dw` to vim and it will delete a word).

Mike mentions both the Atom text editor and Sublime Text, two editors that are and were also influential for me.

# Story Time!
When I was a young warthog... er, high school student, I came across a book on C++. At that time, I had no idea what editors or IDEs were, but I got a copy of the Borland C++ IDE. My experience with it was awful. I'd write a tiny bit of C++ to solve one of my book's many problems, and clicking run would pop up a windows console for about 3 milliseconds. Then it would disappear, because the program had run its course. I got around it by adding a `cin.get()` or some such, but that didn't work as soon as my program needed any input. So I gave up and went back to my science classes.

## College Days
I still loved computers and the idea of programming though, enough to enroll in a computer science degree. The first day of Java 101 (I narrowly missed C++ being the language du jour for teaching), the professor sat us down in a linux lab in front of some RHEL GUIs and told us enough vim to get in trouble (`vim hello.java`, then `i`, then type all your code, then `escape :wq`). All of us students promptly ignored him and fired up gedit, resorting to the command line only for the `javac` commands. At home I found the (still today wonderful) [notepad++](https://notepad-plus-plus.org/). It had cool things like syntax highlighting and being able to tab over (indent) multiple lines in a selection. I was happy with it for a while, but eventually I found Eclipse. Eclipse was great since I was still terrible at Java and it would both find and fix my mistakes.

## The Early Changes
After college, I learned some python and some ruby, and Eclipse was no longer the best thing on the block. It was great for writing Java, but I discovered IntelliJ (which I still use today whenever I have to write any Java code). And an intern showed us all a new text editor: Sublime Text. It was wicked fast, even with huge files, and it had multiple cursors, goto anything, a tree view, a package manager, and all of the modern conveniences. But more than anything, Sublime was _beautiful_. Text was rendered incredibly sharply, even on my desktop at home with an embarassingly low PPI count. All the pieces looked like a cohesive whole.

Sublime text was also my first time really digging into my editor's settings. Sublime had the fantastic idea to have plain text settings, which makes them incredibly easy to back up and restore. It also made it easy for me to try Sublime's Vintage mode, which gives vim commands. At this point, my only experience with vim was being wowed by one of the wizards in my programming class fixing a bug in real time on the projector in vim. He was copy pasting code and jumping to bookmarks and using all manner of motions that blew my mind. So I gave it a try and I got hooked.

## All that is old is new again
So hooked was I on Sublime Text's Vintage mode that I decided to try the real thing. Vim was harsh and unforgiving, but it was a sharp tool. And like many sharp tools it's easy to cut yourself, but you can also work faster than with duller instruments. I slowly learned a few things at a time, and eventually became somewhat okay at vim. And then I got rescued.

I had heard of Emacs but I tried it once and went `ctrl-x ctrl-c`? Nope. But there's a prominent figure in the ruby community named Bozhidar Batsov. He created Rubocop (_the_ ruby linter) and also maintains an emacs distribution named [Prelude](https://github.com/bbatsov/prelude). Prelude introduced me to how nice Emacs could be. It set everything up for me, and made it a little easier to learn. Neither it nor vim were as nice as sublime text, but it was nicer than vim.

## Take me to your <leader>
And then I heard about another emacs distro, one that promised to make vim and emacs play nicely together. From the [spacemacs.org website](https://www.spacemacs.org/)

> Spacemacs is a new way to experience Emacs -- a sophisticated and polished set-up focused on **ergonomics, mnemonics and consistency.**

I read through all the documentation, and got set up. That tagline was not a joke. Spacemacs is set up around one amazing central idea. Everything you want to do should be accessible through a mnemonic series of keys.

Regular emacs is really focused on key "chords", where you press many keys at once. Quitting is press and hold control, then press and release x, then press and release c, then release control. Spacemacs took vim's idea of a "leader" key, which by default was the spacebar (thus _Space_ - macs). So to quit was `space q q` (Leader Quit: Quit all). Saving a file was `space f s` (Leader Files: save file). Editing the .spacemacs file was `space f e D` (Leader Files: Edit: Dotfile).

This focus on mnemonics and consistency meant that learning new commands was easy. As soon as you hit space, all the possible prefixes would pop up at the bottom of the screen. Hit `space f`, and all the commands related to files would pop up.

Spacemacs even had a wonderful community on gitter.io, which really helped with the quite often I'd still get stuck deep in the yak-shaving weeds.

And then a bomb dropped out of the sky.

# GitHub has entered the battle
GitHub, the most popular source code host (not coincidentally where this blog is hosted!) decided that they wanted to make a modern editor, but one that was still hackable to the very core. Atom was a bit slower than Sublime, a bit less extensible than emacs, and a bit less open than vim. But it had many of the best ideas of all the editors I'd tried. The focus on beauty, multiple cursors, and many of the UI elements came from Sublime Text. The ease of redefining core functions and keyboard shortcuts came from Emacs. The community aspects came from Spacemacs. Eventually, they open sourced even the core of the editor, inspired in part by the older editors like vim.

The cool thing about Atom was that it was built on the same technology everyone was already using. It was a thick client application, but built on the web technology that was and is taking over the world. You could write packages in coffeescript or javascript, with Less for CSS, and regular HTML for presentation. Atom was totally free, as in speech and as in beer.

The ideas behind atom were so good that the open core broke off from being "atom-shell" and rebranded itself "Electron". (It's the core of the atom, get it? *elbow*). Electron was so great that a bunch of other companies have picked it up and used it, including slack and teams.

Atom's team was full of brilliant people, and one of the things they came up with was a new type of parser called a Tree Sitter parser. It's incremental, fast, and great for syntax highlighting and similar concerns of editors.

## Electron text editors
I would be remiss not to talk about the elephant in the room. Microsoft got way ahead of the online editor/ide thing and started developing a web based visual studio, codenamed Monaco. When Electron came around, they saw the opportunity and created Visual Studio Code. It was a stripped down, free, visual studio. Importantly, it shared the same cross platform heritage as Atom. Microsoft wanted to differentiate the two editors, so they had a very different setup for their UI, and focused hard on the IDE aspects: intellisense (their auto-completion), a built in terminal emulator, and a built in debugger.

Microsoft also had literally the best idea since vim and emacs. Instead of having boutique plugins for every single editor and IDE times every single programming language, you could evolve the two independently. The Language Server Protocol is a JSON protocol for making editors smart. Contextual auto-completion, intelligent refactoring, you name it. If your favorite IDE can do it, LSP probably can too.

## Today
These days, both Atom and VS Code are popular (though code appears to be more popular from my informal surveying and the number of community PRs it gets). I still use Atom because Vim Mode Plus is better than vim at doing vim things in many respects, and because I feel comfortable writing packages for it. Check out my (basically complete) [git links](https://atom.io/packages/git-links) package, my (beta quality) rainbow parens package: [prismatic parens](https://atom.io/packages/prismatic-parens), and my (alpha quality) (vim mode plus macros)[https://atom.io/packages/vim-mode-plus-macros] package. I always love PRs, so feel free to PR them!

# Summary
Text editing has gotten incredibly better over the few years I've been programming. From simple things like vertical lines at 80 and 120 characters to incredibly complex multiple cursor macros, the state of the art has been constantly improving. Atom has taken many of the best ideas and put them all into a single editor. [Give it a try!](https://atom.io/)
