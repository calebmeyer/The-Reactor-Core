---
date: 2020-04-14T20:11:00
pageTitle: 2 - The Friendly Interactive Shell
tags: posts
---
I was at work today explaining to someone how to make a shell alias, and it reminded me of one of the many reasons why I use [the friendly interactive shell](https://fishshell.com/), `fish`. Before I get too deep into the weeds, I want to clarify one thing. I have no quarrel with bash or zsh or powershell. I think each of them has a lot of strengths, not least the volume of code written for them. With that said, let's talk about terminals and shells.

# Terminal vs Shell
This is a common confusion among newcomers. In ye olden days, the terminal was a physical device: a machine with a keyboard and screen. The shell is software.

These days, we use general purpose computers, so terminals are typically recreated in software. So today, a terminal (or more accurately, a _terminal emulator_) is a program that runs a shell. Microsoft has a great [series of blog posts](https://devblogs.microsoft.com/commandline/windows-command-line-backgrounder/) about why updating the [windows terminal](https://devblogs.microsoft.com/commandline/introducing-windows-terminal/) has been so hard. Other examples of terminals include iTerm2 (macOS only), minTTY (windows only), and xconsole (anywhere that runs X, but mostly linux).

Shells are software that read in lines of commands and arguments and execute those commands. In the beginning, there was only `sh`, the linux shell. (and `ed`, but that's a topic for another time). Many people liked `sh`. At least as many had problems with it. Some of those who had problems with it wrote their own shells. The most popular of those is a shell called `bash`, for Bourne Again Shell. Bash is literally everywhere. Even [windows has bash these days!](https://blogs.windows.com/windowsdeveloper/2016/03/30/run-bash-on-ubuntu-on-windows/). Bash is like `vi`, if you're `ssh`ing somewhere you just expect it to be there. Apple recently made some waves by [announcing that they'd be shipping `zsh`](https://scriptingosx.com/2019/06/moving-to-zsh/), the Z Shell, as their default starting with macOS Catalina.

# RC Files and Aliases
When you're first learning to use a shell (any shell), you often find that you're typing the same things over and over again. `ls -l`. `sudo vi /etc/hosts`. `mkdir -p app; cd app`. `make clean; make; make install`. One of the first customizations many people make is defining a shell alias. An alias is just a word that the shell understands as something longer. Aliases will be expanded by your shell into whatever they stand for. They serve a similar function to abbreviations in writing. If you fire up your favorite bash or zsh (I think this works in powershell too, probably not in CMD.exe), you can type
```shell
$ alias ll='ls -l'
```
and hit enter. If you then type the name of the alias, the shell will run the command it stands for:
```shell
$ ll
total 4
drwxr-xr-x 1 Caleb 197121 0 Jan 16 21:34 js_workspace/
drwxr-xr-x 1 Caleb 197121 0 Feb  6 21:03 rust_workspace/
drwxr-xr-x 1 Caleb 197121 0 Sep  9  2019 side_projects/
```

You can even put things after the alias and they'll just get tacked on to the end:
```shell
$ ll /usr
total 136
drwxr-xr-x 1 Caleb 197121 0 Oct 13  2017 bin/
drwxr-xr-x 1 Caleb 197121 0 Oct 13  2017 lib/
drwxr-xr-x 1 Caleb 197121 0 Oct 13  2017 libexec/
drwxr-xr-x 1 Caleb 197121 0 Oct 13  2017 share/
drwxr-xr-x 1 Caleb 197121 0 Oct 13  2017 ssl/
```

This is great until you close the terminal window or exit the shell. The next time you start up, you'll try your brand new alias, and...
```shell
$ ll
bash: ll: command not found
```

Crap. That's not what we wanted. If you want something to happen every time the shell starts, you can put it in the appropriate .rc file. For bash, that's `~/.bashrc`. If you put the alias command in there, it's run (silently) when the shell loads. Now you can use it all the time!

Except for right now. If you want to use it right now, you have to do `source ~/.bashrc`. Just changing what's in that file doesn't automatically re-run it.

# So... What's all this have to do with fish?
Remember how fish stands for the friendly interactive shell? Aliases are one of the reasons I think it deserves that title. See, in `fish`, there is a shell built in for `alias`, and it will work like bash and zsh. If you type
```shell
$ alias ll='ls -l'
```
then fish will know what you mean and do the right thing. I called `alias` a shell built in, but that's only half true. `alias`, like nearly everything else in fish, is a function. If you fire up fish (usually by typing `fish` at a bash prompt), you can type `functions alias` to see the definition of `alias`:
```bash
# Defined in /usr/share/fish/functions/alias.fish @ line 1
function alias --description 'Creates a function wrapping a command'
  # all the code here has been elided to keep from overwhelming you
  # just try it!
end
```

The most interesting part of this function is at the bottom:
```bash
echo "function $name --wraps $wrapped_cmd --description $cmd_string; $prefix $first_word $body \$argv; end" | source
```

When you define an alias with fish, it's actually defining a function for you. If you pass `-s` or `--save`, it will also persist the function to disk, in `~/.config/fish/functions/`. Remember how we had to source the function in bash via our bashrc file? Fish does it automatically, and functions are lazily loaded in fish, so you can put one in a file in that functions directory after the shell starts and it will already be available for this and future shells.

# Summary
This is but one of the thousand small things that fish just gets right. The history is used to auto-suggest things you've typed before, so you often don't have to alias things. For most config, you don't have to touch a config file, since you can type `fish_config` and get a web based configuration tool that lets you choose colors, prompts, and more. You don't have to install auto-completions (for example for `git`), since fish will read your man pages to auto-auto-complete. The scripting language is really awesome: it uses `and` for `&&`, `end` instead of `fi` or `esac`, and newlines instead of requiring semicolons (though it does support semicolons).

If you've read this far, I hope I've convinced you to give fish a try. You can get it for mac or linux through your package manager, or directly from [the website](https://fishshell.com/). On windows, you can run it via WSL (preferred) or Cygwin. Go fish!
