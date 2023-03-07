---
date: 2023-03-06T21:32:47
pageTitle: 13 - Setting up Vagrant with Fish and Rust
tags: posts
---

Today I decided I wanted to learn some Vagrant, following Amos' post about [Setting up a local Ubuntu Server VM](https://fasterthanli.me/series/building-a-rust-service-with-nix/part-1) on fasterthanlime. Definitely go read that first if you haven't. Cool bear's final hot tip was that Vagrant does all the things automatically instead of manually.

So I fired up my windows desktop and dug in.

## Differences
I took a different path because I like taking different paths. I chose not to use Ubuntu because I'm a big fan of Fedora. While researching for my last devcon talk ([slides here](https://github.com/calebmeyer/linux-slides)), I found out that Linus Torvalds himself uses Fedora. If it's good enough for the creator of Linux, it's good enough for me.

I also wanted to set up [the Friendly Interactive Shell](/posts/2-the-friendly-interactive-shell/) and the rust programming language, both of which proved challenging in their own right.

## Getting Vagrant and VirtualBox
Getting vagrant was as easy as `scoop install vagrant`. I'm sure your package manager of choice has it too. Getting virtualbox required going to the website. Scoop didn't have it that I could find. But it was a quick install, and even has a dark mode now!

## Getting a Fedora VM set up
From 0 to VM was also pretty easy. Searching `fedora` on [the boxes page](https://app.vagrantup.com/boxes/search) gave me some very old versions, so I changed my search to `fedora 37` and landed on [generic/fedora37](https://app.vagrantup.com/generic/boxes/fedora37).

With that in hand, I made a new folder in my side projects called vagrant and ran `vagrant init`. That created a Vagrantfile, which is a ruby file that configures how Vagrant works. I left everything default except changing `config.vm.box` to the fedora image I found. Then I ran `vagrant up` and it created the VM. Super easy.

## Minor SSH issues
The output of `vagrant up` suggested that the VM had an SSH server running on an internal port 22 mapped to my host's port 2222 for 127.0.0.1. So I ran the obvious SSH command `ssh vagrant@127.0.0.1:2222` and it didn't work. I tried again from a WSL bash, in case it was something up with windows' version. Nope. Neither worked. I went back and read the docs, and it turns out you have to do `vagrant ssh` instead. A bit magical, but the magic works, so I can't complain.

## Provisioning fish
Fish is a difficult shell to get, unfortunately. Many distros don't include it in the available packages in their package manager. None that I've ever seen install it by default. Fortunately, Fedora at least has it available in `dnf`, so that's an easy win. At the bottom of the Vagrantfile is a commented section with `config.vm.provision`. If you uncomment it, it has an apt shell script inline. Changing the `apt` to `dnf` lets us update and install things. I have it installing fish:
```ruby
  config.vm.provision "shell", inline: <<-SHELL
    dnf update -y
    dnf install -y fish
  SHELL
```

To run this script, you type `vagrant provision`, so I did. And the output looked good. But fish was not the default shell. [The fish docs](https://fishshell.com/docs/3.0/tutorial.html#tut_switching_to_fish) suggest using these two commands, so I tried them:
```sh
echo /usr/local/bin/fish | sudo tee -a /etc/shells
chsh -s /usr/local/bin/fish
```

The problem is... both are wrong. `dnf` installs fish to `/usr/bin/fish`, not `/usr/local/bin/fish`. And `chsh` does not exist on this system. I went down quite a rabbit hole trying to figure out why. Supposedly it's provided by the linux-util package, which was already installed by default. But `which chsh` doesn't turn up any binary for it. Eventually I learned that you can do the same thing (a bit more verbosely) like this: `usermod --shell /usr/bin/fish vagrant`. The `vagrant` user is important here, because the provisioning script is run as root, but you ssh as the vagrant user. With that we get a fish prompt after `vagrant ssh`. Success!

We also want to ensure that we don't keep appending to /etc/shells on every provision, so I added one of my favorite tricks: check or do. Here we check if fish is already in /etc/shells or add it if not. That makes our provision command now:
```ruby
  config.vm.provision "shell", inline: <<-SHELL
    dnf update -y
    dnf install -y fish

    grep fish /etc/shells || echo /usr/bin/fish | sudo tee -a /etc/shells
    usermod --shell /usr/bin/fish vagrant
  SHELL
```

## Provisioning Rust
This was also tricky, though for different reasons. `dnf` has rust among its packages, but I've had bad luck managing programming languages with package managers. You often end up needing more than one version, like when `node-gyp` wants python 2, or you're upgrading major/minor versions.

Fortunately rust provides [rustup](https://rustup.rs/), which handles all of this for us... or does it? I added the command to my provisioning script... and it bombed out because it was run non-interactively. Fortunately it also gave out a link to [the book](https://rust-lang.github.io/rustup/installation/other.html) which helped me get the command right:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

With that in place, I just needed to get it into the fish path. Rustup already inserts itself for bash/zsh by default, but doesn't do so for fish. Fortunately, we don't need any crazy path manipulation scripts, since fish includes a handy one: [fish_add_path](https://fishshell.com/docs/current/cmds/fish_add_path.html). This command does what you mean in config.fish or interactively. Since I want this to stick for future provisioned shells, let's add it to config.fish:
```sh
echo "fish_add_path ~/.cargo/bin" >> /home/vagrant/.config/fish/config.fish
```

That's a pretty long command, and it gets even longer when you add the check to make sure we don't do this every time:
```sh
grep -q "fish_add_path ~/.cargo/bin" /home/vagrant/.config/fish/config.fish || echo "fish_add_path ~/.cargo/bin" >> /home/vagrant/.config/fish/config.fish
```

That's well over my usual hard limit of 120 characters per line, so let's take advantage of the fact we're in Ruby and interpolate that long path. This gets us to our final provisioning script:
```ruby
  fish_config_file = '/home/vagrant/.config/fish/config.fish'

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    dnf update -y
    dnf install -y fish

    grep fish /etc/shells || echo /usr/bin/fish | sudo tee -a /etc/shells
    usermod --shell /usr/bin/fish vagrant

    which cargo || curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    grep -q "fish_add_path ~/.cargo/bin" #{fish_config_file} || echo "fish_add_path ~/.cargo/bin" >> #{fish_config_file}
  SHELL
```

VS Code highlights this poorly because it's trying too hard. It treats the `SHELL` heredoc as shell script and thus it thinks that the `#` starts a comment. Oh well. You can't win them all.

## Conclusion
It was a bit trickier than I'd hoped to get everything set up just the way I wanted. If I'd wanted to mix tools, I could have written a dockerfile to do all this much more quickly (or it's possible someone else already has). But I'm happy with my fish and rust setup, and I look forward to seeing how well Vagrant works for some real development in the future.
