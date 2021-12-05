[![codecov](https://codecov.io/gh/pjanowski/wsl_setup/branch/master/graph/badge.svg?token=znSYS91aD2)](https://codecov.io/gh/pjanowski/wsl_setup)

# wsl_setup
This repo is meant to facilitate quickly setting up a new WSL working environment for data science on a Windows OS. Note that with the advent of WSL2, the process here might change


0. On Windows install 
 * git for windows
 * meld to C:\meld (no longer, just use VSCode for git merges and diffs)
 * notepad++ with compare, markdown, and json plugins and Navajo theme selected
 * VS2019 with extensions: HotKeys, HotCommands, Scope Studio, Productivity Power Tools (only if using Visual Studio)
 * Windows Terminal
 * VS Code (and log into github account and sync settings)
 * Docker
 * LinqPad
1. Install WSL 
2. Move the following to home
 * .bash_profile
 * .bashrc 
 * .dircolors
 * .gitconfig
 * .vimrc
3. Install conda and then environments
 * Install base environment from environment_base.yml.
 * Install sql environment from environment_sql.yml.
 * Install environments and nbextensions in Jupyter Notebook
 * Install nbstripout
4. Replace WindowsTerminal settings.json file with WindowsTerminal/settings.json
5. Sudo apt-get install
 * gedit and sublime (optional, now I just use VSCode)
 * msft sql odbc drivers for python/sql
 
Notes
Steps to get jupyter working in WSL: https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da#gistcomment-3121935

So that jupyter notebook starts automatically in your windows browser
1. Add this line to your ~/.jupyter/jupyter_notebook_config.py
`c.NotebookApp.use_redirect_file = False`
2. Set the BROWSER env var in your .bashrc  Eg:
export BROWSER='/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
