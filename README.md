# wsl_setup
This repo is meant to facilitate quickly setting up a new WSL working environment for data science on a Windows OS. Note that with the advent of WSL2, the process here might change


0. On Windows install 
 * git for windows
 * meld to C:\meld 
 * notepad++ with compare, markdown, and json plugins and Navajo theme selected
 * VS2019 with extensions: HotKeys, HotCommands, Scope Studio, Productivity Power Tools 
 * Windows Terminal
 * VS Code with SettingsSync plugin (point it at my gist)
 * Docker
 * LinqPad
1. Install WSL and VcXsrv
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
 * gedit and sublime
 * msft sql odbc drivers for python/sql
 