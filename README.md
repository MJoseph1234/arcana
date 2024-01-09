# Arcana

Arcana transforms your Markdown files into a new static website, blog, web journal, or whatever. 

It's like magic.

## Getting Started
1. Verify your system meets the [Requirements](#Requirements). 
2. Install Arcana
	* You can download Arcana from this GitHub repository.
    * This repository is not currently available on [PyPi](https://pypi.org/), the Python package index, so it is not yet installable via Pip.
3. Get Arcana on your PATH or set up a virtual environment pointing to your local Arcana install
4. Run the following to start a project and add your first blog post:
	```
	arcana new project myNewBlog
	cd myNewBlog
	echo "# Hello world!" >> content/my-first-blogpost.md
	arcana serve
	```
5. Now, point your web browser to [http://127.0.0.1:8080/my-first-blogpost](http://127.0.0.1:8080/my-first-blogpost) 

## Requirements
1. Arcana requires Python version 3.11 or higher.
2. Arcana requires Python Markdown version 3.5 or higher. If you are installing Arcana from the github repository, you will need to download python markdown and add it to your environment PATH manually.
3. You will need a hosting provider and domain name for your website

## CLI Commands
Arcana projects are designed to be maintained from a terminal emulator, like PowerShell for Windows machines, the Terminal application for Apple OSX computers, iTerm, PuTTY, or whatever.

### New
``arcana new [project, post, command]``  
The ``new`` command is used to start a new arcana project or create a new post or command within an existing project.

#### new project
``arcana new project <project directory>``  
Create a new arcana project in */project directory*. This creates the project directory. It will automatically add sub-folders within that directory to house the new arcana project content. Finally, it'll make a new project.toml file to hold any project-specific configuration.

#### new post
``arcana new post <post name>``  
If we're already in an arcana project directory (a directory with an arcana config.toml file), this will create a new markdown file in the project's `content` directory.

#### new command
``arcana new command <command name>``  
If we're already in an arcana project directory (a directory with an arcana config.toml file), this will create a new python file in the project's `commands` directory. These commands are incorporated into your Arcana CLI and can be run from the command line. 

### Build
``arcana build``  
The ``build`` command takes your existing content, layouts and static files and bundles them so they can be deployed to wherever your're hosting your website. 

### Serve
``arcana serve``  
The ``serve`` command runs a small, local webserver so you can preview your blog/website/whatever before building and publishing. 

## Configuration Options
Each arcana project has a project.toml file that's used to control some project-wide configuration settings. Configuration settings can be used to control things like what IP address and port will be used when running the ``arcana serve`` command, or what layout html file should be used when building or serving content files.