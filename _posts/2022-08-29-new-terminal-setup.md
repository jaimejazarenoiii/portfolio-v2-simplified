---
layout: page
title: "My personal setup for a new terminal as a Ruby on Rails + iOS + Flutter Engineer"
subtitle: "Ezpz setup"
date:   2022-08-29 21:21:21 +0800
categories: Guideline
---

I'm currently an iOS engineer but have always been a full-stack guy at heart. Now I'll show you how I set up a new terminal based on what I need and a few desires.
---
### Initial
-   Install [brew](https://brew.sh/)
-   Install node using brew `brew install node`

### Terminal
-   Install iterm2 `brew cask install iterm2`
-   Install zsh `brew install zsh`
-   Install oh-my-zsh 
```sh -c "$(curl -fsSL[<https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh>](<https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh>))"```
-   Install [iterm2 themes](https://github.com/mbadolato/iTerm2-Color-Schemes)
-   Install spacehip:
    -   `git clone [<https://github.com/denysdovhan/spaceship-prompt.git>](<https://github.com/denysdovhan/spaceship-prompt.git>) "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1`
    -   `ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"`
-   Install nerd font `brew tap homebrew/cask-fonts` then `brew install --cask font-hack-nerd-font`
-   Install tmux `brew install tmux`
-   Install zsh plugins
    -  Syntax autosuggestion - `git clone [<https://github.com/zsh-users/zsh-autosuggestions>](<https://github.com/zsh-users/zsh-autosuggestions>) ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`
    -   Syntax highlight - `git clone <https://github.com/zsh-users/zsh-syntax-highlighting.git> ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`
    -   Auto complete - `git clone [<https://github.com/zsh-users/zsh-completions>](<https://github.com/zsh-users/zsh-completions>) ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions`
-   Generate ssh-key `ssh-keygen -t rsa` check :
    [How to manage multiple GitHub accounts on a single machine with SSH keys](https://www.freecodecamp.org/news/manage-multiple-github-accounts-the-ssh-way-2dadc30ccaca/)
-   Copy ssh-key to bitbucket or github or whatever.
-   Clone [](https://github.com/jaimejazarenoiii/dotfiles)[https://github.com/jaimejazarenoiii/dotfiles](https://github.com/jaimejazarenoiii/dotfiles) and `cp -r dotfiles/ ~/` or use your own configs.
-   Run source commands:

        -   source ~/.zshrc
        -   source ~/.vimrc

-   Install tmux plugin manager
    -   `git clone [<https://github.com/tmux-plugins/tpm>](<https://github.com/tmux-plugins/tpm>) ~/.tmux/plugins/tpm`
    -   `tmux source ~/.tmux.conf`
    -   Run `Prefix + I`

### Editor (VIM)
-   Install neovim `brew install neovim`
- Share vimrc config to neovim. https://vi.stackexchange.com/a/15548
-   Install vim plugIn `:PlugInstall`
```
  sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \\
           <https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim>'
```

### Ruby
-   Install [rbenv](https://github.com/rbenv/rbenv)
-   Install latest ruby from rbenv, check list using `rbenv install -l`

### Rails
- Install postgres: `brew install postgres` (for non-containerized projects) 
- Install docker:  `brew install --cask docker`
- Install redis: `brew install redis` (for non-containerized projects)

### iOS | Android | Flutter
- Download Xcode
- Download Android Studio
- Install [Flutter env](https://docs.flutter.dev/get-started/install/macos)

### Misc (Optional)
- Download [Firefox](https://www.mozilla.org/en-US/firefox/new/)
    [Mozilla Minimalist Theme](https://www.notion.so/Mozilla-Minimalist-Theme-9e495ec54b4d4d6f892d59604e0a61d5)
    - Install plugins:
        - Multi Account Container
        - Session Boss
- Download [Notion](https://www.notion.so/desktop)
- Download [Spotify](https://www.spotify.com/download/mac/)
- Download [Clipy](https://clipy-app.com/)
- Download [Obsidian](https://obsidian.md/download)

---

Some vim plugins: 
1.  [](https://www.vimfromscratch.com/articles/vim-for-ruby-and-rails-in-2019/)[https://www.vimfromscratch.com/articles/vim-for-ruby-and-rails-in-2019/](https://www.vimfromscratch.com/articles/vim-for-ruby-and-rails-in-2019/)