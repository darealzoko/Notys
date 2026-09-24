# v1.3.0 Beta 2 (24/09/26 21:06)
Still windows preview only.
By the way, when 1.3 will finally release, there will be macOS executables, but for now it's only windows Beta.

### Fixes:
- There is now an icon in the taskbar.

# v1.3.0 Beta 1 (24/09/26 20:54)
This is a beta, the UI is not really good with windows (functionnal tho) and there may have some bugs.
It's really ugly, a bit buggy but kinda usable if you don't mind the appearance.

For the techies, here's what changed:
### New:
- A version.py file that is imported in Notys.spec so it has the version noted in one place, working for both macos and windows.

### Modification:
- There is supposed to not have any emojis anymore in the settings, but there still is for whatever reason.

### Bugs:
- No icon still

# v1.2.1
### New:
- You can now drag tabs to rearrange them.
- Added the Command+Comma keyboard shortcut to open settings

### Modification:
- Modified the way to open settings from the menu bar, it now uses the default and native way to open them (instead of Settings -> Open Settings, it's now Notys -> Preferences)

### Still known bugs:
- You cannot do the "save all tabs" or "reopen last closed" keyboard shortcuts.

# v1.2.0
### Fixes:
- Fixed the bottom bar not always appearing no matter the resolution/size of the window. Now it is always here.
- Fixed a bug where the text would not be changed to white in dark theme if strikethrough or underlined, making it really hard to read. Now it's fully readable.

### Modifications:
- Now, the markdown syntax only applies to .md files. Making Notys a more universal editor than markdown editor specifically.

# v1.1.3
Fixed the scrollbar usibility and visibility for quality of life.
Linux support is dropped, because it is way to buggy and it is very picky about library versions and is way harder to maintain than macOS. I will put the buggy versions still but it will no longer be updated.
Windows support to come tho ;)

# v1.1.2.1
MacOS support brought back!
Every macbooks with M1/M2/M3/M4/M5 and Neo WILL NOT support Notys with this version.
Anyways, nothing new than 1.1.2 except macOS support.
Also, the macOS build env is what i use to recompile the whole app for macOS

# v1.1.2
Settings improvement, and .venv linux compatibility.
The previous version was made for macOS Intel and not for ARM (at least not tested on ARM), so now this new version dropped macOS support.
The Notys Linux.zip file gives the entire developping environment.
The .AppImage is the complete packages.
Also now the quick icon to change the theme has be deleted because of a compiling error. I will try to bring it back for the next release.
It is still working in the .zip version, but it's harder to execute the .zip version.

# v1.1.1
Changed icon because previous was already taken by another app.

# v1.1
### New:
- Added a settings page (with languages, themes and editor settings)

# v1.0
Important to know before reading:
The windows version will come soon, (this is why there is "Cmd / Ctrl" in the keyboard shortcuts sections)
### New:
- The app has been compiled in a .app for macOS.
- Added a logo.
### Modification:
- The icon to change theme has been converted to a .png file.

# v0.4.1
### New:
- Added the keyboard shortcut Ctrl+Shift+Tab to navigate between tabs easily.

# v0.4
### New:
- Added more keyboard shortcuts:
- - Cmd / Ctrl+T: new tab
- - Cmd / Ctrl+Shift+T: reopen last closed tab
- - Cmd / Ctrl+N: new window (before it was to open a new tab)
- - Cmd / Ctrl+Opt / Alt+N: save every files (do not work, still in the v1.0. will probably be fixed in the next update)
### Modification:
- Nerdy change: Cmd / Ctrl+W now calls on_quit() (which closes the current window and quits the app if no more windows are open) when there's only one tab left.

# v0.3.1
### New:
- Added zoom
### Modification:
- Made the font bigger
### Fixes:
- Fixed dragndrop on macOS

# v0.3
### Fixes:
- Fixed dragndrop on Windows.
- Fixed an unnecessary space before the colored word when using the color feature. (before: "test test", after: "test test" (github do not let me set a color for the text but it is working in the app)

# v0.2
### New:
- Added highlighted text mode
- Added strikethrough text mode
- Added a search function
- Added a confirmation pop-up when closing the app and that some documents aren't saved.
### Modification:
- Modification: the characters used for the style (e.g: **) disappear when the cursor is not on the word
- Modification: the characters used to color the text was changed from "$@red text@$ to &^red text^& because of LaTeX which is present in many markdown editors.
### Fixes:
- Fixed: the dot that indicates that the document is not saved was still visible when the document was saved
- Fixed theme icons

# v0.1
### New:
- Added light and dark theme
- Added tabs
- Added pillow requierement (if you want to compile for yourself)
### Modification:
- Changed the app title to show the file name in the title bar
- Changed font to Consolas
### Fixes:
- Fixed a bug where two windows would pop-up at the start of the app (with one completely unsuable)

# v0.1 Beta 1
### New:
- Added text coloration
- Added the possibility to open files
- Added the possibility to create new files (not usable in this version as there is no tabs and it would just delete your current document)
- Added undo and redo
- Added save as feature
### Modification:
- Changed font the Andale Mono
### Fixes:
- Fixed performance issues (in large documents)

# v0.0
### New:
- Added headers from 1 to 4.
- Added italic
- Added bold
- Added code
- Added the save feature
