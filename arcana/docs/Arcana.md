# Arcana
A static site generator originally designed for long data-sheets and manuals. Where clicking and wating for a page to load is slower than loading all the stuff and then using a table of contents or searching with `CTRL+F` is quicker.

Arcana takes markdown (.md) files and serves formatted webpages, which can have quick navigation and an easy-to-use table of contents.

This started as a simple web app like [[http://ceryliae.github.io/5edmscreen/index|The DM Screen]], but I wanted to add D&D spells, magic items and other D&D-related content that I care about (potion of healing rules).

## To Do
 - [ ] README
 - [ ] replace auto-reloader with dev server
 - [x] replace rebuild command with publish
   - calling it 'build' instead of 'publish' because publish sounds like it's making the HTML deploying to the world, instead of just updating the HTML
 - [x] use settings.py directories
 - [ ] enable customizing themes
 - [ ] site-specific extensions/markdown parsers
 - [x] markdown metadata extension to customize pages (like getting About page right aligned)
 - [ ] refactor the templater code so it uses settings
 	- [ ] can pull files from {% static block %} using settings.static
 - [x] refactor SiteGenerator so that it's more like a class representing Site, with a generate function. 
 - [ ] autoreloader to automatically update HTML files if markdown files are updated. 
   - [x] monitor for changes in existing md files
   - [ ] monitor for added or removed markdown files
   - [ ] monitor static files, like javascript
 - [x] separate and modularize cli commands
   - [x] core commands
   - [x] site-specific commands
 - [x] commands need a way to fall back on argparse's help text printer if our custom run command finds an issue with the arguments.
 - [ ] extend build command with controls for including/excluding drafts/future pages/expired pages


# arcana-check.net
a site, built using the Arcana static site generator, to display long pages of d&d content in an easy-to-navigate format

## To Do
 - [ ] parser to take markdown and output whatever (json, sqlite table, etc.)
    - [ ] mostly want to get this stuff into my d&d database sqlite table (feats, magic items, tasha's magic items)
 - [ ] alphabetize feats page
 - [x] get a domain
 - [x] hosting (namecheap? dynamic DNS for hosting both this and canirecycle on the raspberry pi (https://www.techcoil.com/blog/how-to-host-multiple-websites-from-home/, https://www.techcoil.com/blog/how-to-get-your-raspberry-pi-3-to-use-namecheap-dynamic-dns-to-update-your-domain-when-your-homes-public-ip-address-changes/)
 - [x] favicon
 - [ ] adding cross-links like [[spell: acid splash]] on the magic items page links you to the acid splash spell on the spell page
 - [ ] text preview stuff
   - I'm not sure what I meant when I wrote this
 - [x] robots .txt noindex
 - [x] index/home page
 - [ ] combine tasha's magic items with standard list
 - [ ] security/protection?
    - [ ] logins to access copywrighted content
    - [ ] SRD magic items/spells/etc pages for pleabs
    - could also be how we save favorites for each user
 - [ ] light/dark mode button should load after header loads, not after whole page loads (long pages cause sun to appear before loading page, then moon appears if you're in dark mode)
 - [x] die-roll parser so we can click a die-roll on any page and it'll give us a value
 - [x] button to switch between light/dark mode [[https://whitep4nth3r.com/blog/best-light-dark-mode-theme-toggle-javascript/]]
 - [ ] TOC start all collapsed
 - [ ] really long TOC should scroll with user, always showing currently active header
 - [ ] marking things as Favorite, which adds them to a Favorites page
 - [ ] improve the markdown parser/webpage builder
    - [ ] each entry could be a div, which will make it easier to Favorite things later on
    - [ ] parser generates entire site (with TOC), removing javascript dependencies on jquery and tocify.js
      - this will mean quicker loading, since we won't have tocify.js generating DOM on the fly each time it loads
      - I think this can be done with a custom extension to the Python-Markdown library. 
      - See the [[https://github.com/aleray/mdx_outline|outline]] extension for how to wrap secitons in \<div\>s 
      - then we need a part to store each header/subheader
      - then a way to pass back the nested list of header/subheaders (see the meta extension for an example of getting this)

## Content to add
 1. Tasha's Cauldron magic items
 2. Feats from Xanathar's
 1. Class
 2. Subclass
 3. racial Feature
 3. class feature
 5. race
 6. subrace
 7. race trait
 8. rules (jumping, health potions, )
 9. equipment (basically the weapons table, armor table)
 10. background
 11. alignments
 12. damage types
 13. Eldritch Invocations

# Features of a Static Site generator
 - CLI commands
   - arcana new site
   - arcana new page
      - makes a new page in content folder based on default content template
   - arcana new command
      - make a new python Command inheriting from Arcana's BaseCommand with some boilerplate pre-written
   - arcana publish
      - makes the static site
      - wraps up and generates html files in public directory
      - moves assets & static to public directory
      - does not deploy to your hosting solution
   - arcana deploy
   - arcana server
      - run a development server
      - option to run it with draft files
      - builds files on the fly
 - draft, future (?), and expired metadata in .md files (stealing from Hugo site generator)
 - a site configuration file
   - site name
   - language code
   - base url
   - theme
 - templating and themes

## Directory Structure
arcana-check/
├── templates/
│   └── default.md
├── assets/
├── commands/
├── content/
├── data/
├── i18n/
├── layouts/
├── public/
├── static/
├── themes/
└── hugo.toml
