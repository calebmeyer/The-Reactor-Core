---
date: 2021-05-20T19:20:07
pageTitle: 12 - You should use a commit per change
tags: posts
---

Every so often, I hear a (usually newer) developer extolling the virtues of a single commit pull request (PR). And while I agree that PRs should be merged into a single commit on the main branch, you absolutely should not be rolling up all your myriad changes into a single commit until then. Here's why.

## Sometimes, we don't get it perfect the first time
If you are not committing early and often, you will find yourself in a bad state eventually. Specifically, you will have made so many changes that you don't know which one broke the code. When that happens, you have two bad options. Either you can do a `git reset --hard` and start over from before all the changes, or you slog through and likely make it worse before it gets better. Don't get stuck in this trap!

Instead, if you commit early and often, you can have a beautiful git history that tells you exactly what changed in each commit. Want to undo a specific commit that happened 5 commits back? `git log`, find the commit hash, and then `git revert abcd123`. That will give you a nice undo commit that exactly undoes whatever abcd123 did.

## Sometimes, we do
Occasionally, you'll find that a coworker does something downright inspiring, and you can't wait for them to merge before you pull it in. Maybe it's simplifying the build, maybe it's fixing all the lint. Whatever it is, you can steal their work for your branch. Just find out the commit hash and `git cherry-pick abcd124` to apply those changes to your branch.

## Single commits help with estimating
When you look at a new issue in whatever your favorite issue tracking software is, the first thing you need to ask yourself is how big it's going to be. Anyone who has been in software long knows [we're all crap at estimating things](https://dev.to/lukegarrigan/why-developers-are-so-sh-t-at-estimating-41mg).

But we also often do similar work. If you need to add a model to the widgets edit page, it's probably going to take you about the same amount of time as it took to add a modal to the ModelManagerBuilderFactory. And if you go back to your previous pull request, you'll see that it took 15 commits over a few days. It will probably take a few days again and about another 10-20 commits.

## A commit per change means a commit message per change
This is probably the most important reason of all. If you don't already know [how to write good commit messages](https://chris.beams.io/posts/git-commit/), many others have written at length about it. But the TL;DR is you should always have a summary that fits in 72 characters (so GitHub doesn't truncate it), and you should often have details below that. The command line makes this difficult to accomplish, so I recommend you either use the git integration in your editor/IDE of choice, or [GitHub Desktop (free)](https://desktop.github.com/), or [GitKraken (freemium)](https://www.gitkraken.com/).

Once you get in the habit of a commit per change, you can reap a lot of benefits on code reviews. For example, my work's training program, DevAcademy (along with my actual team) mandates that every comment on a code review must be answered in one of 4 ways:
- Yes, here's a link to a commit (I've just made) that exactly resolves this comment
- No, and here's why I disagree
- Yes, but this is out of the scope of this task. I have logged a new issue and here's the link
- I don't understand what's being asked, please clarify

Overwhelmingly these comments are answered by a commit. Unfortunately, they're often answered by a commit that looks like this:
```text
  commit 309280d478a3e231d4600a81ef86a9aa85c18cd4 (HEAD -> feature-123)
  Author: Caleb Meyer (some@email.com)
  Date: Today

    address comments

  modified: src/main/oops/widget.java
  modified: app/controllers/widgets_controller.rb
  modified: app/mysite/urls.py
  deleted: source/lib/index.jsx
  added: source/lib/hello.rs
```

This is way too much. Now your reviewers have to pick through these many files of changes to verify that what they asked for actually got changed. They also had to wait for you to finish every requested change before they could look at even the first one. Sometimes code review changes cause extensive refactoring, and that takes a while.

If instead you have a commit per change, conversations end up looking like this:

**Helpful coworker:** Can you add some margin to this button, it's too close to the side.

**You:** Sure! [d020eb9](https://github.com/calebmeyer/The-Reactor-Core/commit/d020eb9890cf81c91f00ee0053fbc78f0d73db85)

I like to make sure that my commit messages complete the phrase
> If applied to my code, this commit will:

Examples include:
- Move the submit button all the way to the left
- Fix the last 6 failing specs
- Refactor index.js to be in alphabetical order
- Update foo to 1.2.3

# Why don't people do this already?
This harkens back to [the three virtues of a programmer](https://avdi.codes/the-three-virtues/), first among which is Laziness. We developers are lazy. And no one is willing to work harder to be lazy than a programmer.

I occasionally get the privilege of watching over someone's shoulder, which is a fantastic way to learn new things. And one of the first things I learned over someone else's shoulder is:

## Commits break flow
I'm sure you've seen someone break their flow for a commit before. It usually looks like this:
- Click the taskbar to open up a new terminal
- `cd Documents`
- `cd code`
- `cd main`
- `cd myapp`
- `git status`
- Re-open the editor and save the 3 files I forgot to save
- Click back over to the terminal
- `git status`
- `git add app/assets/javascripts/index.js`
- `git add bin/dothething.sh`
- `git commit -am "ISSUE-1234 made some changes"`
- Go back to work without pushing

Oof. That's a lot of work, and a lot of interrupted flow, just to do a single commit. No wonder a lazy developer doesn't do it more often. This is why I don't use the terminal for commits. I know the git command line quite well. I think it's worth learning it, if nothing else so that you can script it. But for commits, **you should use your editor integration or a git GUI.**

## Using your editor to commit
My workflow looks something like this:
- Coding along happily, and get a complete change made.
- `space g c` (git commit) in normal mode (I use the amazing [vim-mode-plus](https://atom.io/packages/vim-mode-plus) for atom)
- Type a commit summary. Hit enter twice. Type a full message, usually with some indication why I made a change.
- Save, which automatically commits
- `space g p` (git push)
- `space g l c` (git link-to commit). This is a command I pull from my very own [git-links](https://atom.io/packages/git-links) package which pastes a link to the latest commit into my clipboard.
- Paste the commit link into a comment on my PR

This takes me all of 15-30 seconds, and doesn't break my flow. I can go right on to the next change. If I find out that we didn't want that change, I can revert it easily.

# Summary
I hope I've convinced you. Once you get your commit workflow to where it doesn't break your flow, you'll find yourself able to make much larger changes without fear, able to easily undo or add in code, able to estimate *like a boss*, and writing beautiful commit messages that years later you will thank you for.
