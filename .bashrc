### User specific aliases
alias rm='rm'
alias lhd='ls -lth | head'
alias untar='tar -zxvf'
alias allow='find . -type d -exec chmod 775 {} \; | find . -type f -exec chmod 775 {} \;'
alias grep='grep --color=auto'
alias ls='ls --color=auto'
alias ll='ls -alF'
alias la='ls -A'

alias npp='/mnt/c/Program\ Files/Notepad++/notepad++.exe'
alias docker='/mnt/c/Program\ Files/Docker/Docker/Resources/bin/docker.exe'
alias nvidia-smi="/mnt/c/Program\ Files/NVIDIA\ Corporation/NVSMI/nvidia-smi.exe"

alias g='git status -sb'
alias l='git log --color --pretty=format:"%C(yellow)%h%C(reset) %s%C(bold red)%d%C(reset) %C(green)%ad%C(reset) %C(blue)[%an]%C(reset)" --relative-date --decorate'
alias gdiff='git difftool --no-symlinks'
alias gmergetool='git mergetool --no-symlinks'

alias start='cmd.exe /c start'
alias src='cd /mnt/c/code/'    
alias winhome='cd /mnt/c/Users/paulano/'
alias dtp="cd /mnt/c/users/paulano/Desktop"
alias downloads="cd /mnt/c/Users/paulano/Downloads"

#alias msbuild="/mnt/c/Program\ Files\ \(x86\)/Microsoft\ Visual\ Studio/2017/Enterprise/MSBuild/15.0/bin/msbuild.exe"
#alias scope='/mnt/c/ScopeSDK/Scope.exe'
#alias mdl='/mnt/c/mdltool/Mdl.exe'


### Path settings
export PATH=~/bin:/mnt/c/meld:/mnt/c/Program\ Files/Microsoft\ VS\ Code:$PATH


### Eternal bash history.
# Undocumented feature which sets the size to "unlimited".
# http://stackoverflow.com/questions/9457233/unlimited-bash-history
export HISTFILESIZE=1000000
export HISTSIZE=1000000
#export HISTTIMEFORMAT="[%F %T] "
# Change the file location because certain bash sessions truncate .bash_history file upon close.
# http://superuser.com/questions/575479/bash-history-truncated-to-500-lines-on-each-login
export HISTFILE=~/.bash_eternal_history
HISTIGNORE=ls:history:"git branch":"git push":"git status":"git log":cd
HISTCONTROL=ignoredups:ignorespace:erasedups
shopt -s histappend
PROMPT_COMMAND="history -n; history -w; history -c; history -r; $PROMPT_COMMAND"


### colors
# dir colors
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
fi

# LS_COLORS='*.php=1;32:di=1;104;37:no=00:fi=00:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:tw=30;42:ow=1;4;104;37:st=37;44:ex=0;4:*.php=1;32:*.tar=01;31:*.tgz=01;31:*.zip=01;31:*.gz=01;31:*.bz2=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.png=01;35:';
# export LS_COLORS


### prompt
source /etc/bash_completion.d/git-prompt
PS1="[\[\033[32m\]\w]\[\033[0m\]\$(__git_ps1)\n\[\033[1;36m\]\u\[\033[32m\]$ \[\033[0m\]"


### VcXsrv
export DISPLAY=localhost:0.0


# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

echo "Hello Pawel"
