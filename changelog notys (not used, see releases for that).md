# v1.4.0

### Modification:
- Modified the "new window" shortcut from Ctrl/Cmd+Shift+N, Ctrl/Cmd+N

# v1.4.0 Beta 2 :
### Remove:
- Removed the phrase "A clean, lightweight Markdown & Text Editor." in the windows' about section.

### Fixes:
- Re-fixed a bug where the settings buttons Apply/Appliquer and Cancel/Annuler would have white text over white background.
- Fixed a bug where when you change the language, the sidebar's "empty" text (EXPLORER) still stays in the previous language.

# v1.4.0 Beta 1 :
### Modification:
- Modified the version system. Instead of it being based on vibes, it will follow the SemVer logic.
- Modified the about section to include the creator (me)

# v1.3.3
### Added:
- Added the Esperanto language. Available now in the settings.

### Modification:
- The sidebar arrows' size has been modified to be the same size in both collapsed and opened.

# v1.3.3 Beta 2
### Fixes:
- Fixed the search bar not opening with both keyboard shortcut and menu bar button.
- Fixed windows shortcut being enabled on macOS.
- Fixed the Cancel/Annuler and Apply/Appliquer button in the settings for an at least readable experience. It is better, but not the best.

### Modification:
- Changed the list's color to fully white instead of light purple.
- The sidebar is now resizable.
- You can now middle click to close a tab (works only on windows for some reason)

### Known bugs:
#### On every systems:
- The scroll bar scrolls weirdly with the mouse: it does not follow the system's mouse sensitivity, making it feel weird. (minor bug though)
#### Windows Only:
- The top bar (as well as menubar's menus) is white even in dark theme, making a flash bang.
- Not really a bug, but the UI's font is really ugly.
#### macOS Only:
- The middle click to close a tab still does not work.

# v1.3.3 Beta 1
### Added:
- Added an "X" button in the sidebar to close the current opened folder.
- Added "Undo" and "Redo" in the Edit menu in the menu bar.
- Added the checkmarks, just do "- [ ]" do get a checkmark and click on the [ ] to mark it as done and vice-versa.

### Modifications:
- Modified the list's aesthetic to something else than just a dash. It now gives actual lists vibes.
- The headers (the #) now disappear when the text selection is not on it, giving a cleaner aesthetic.
- *nerdy modification* Now the shortcuts are much easier to modify, as they are in a dictionnary in plain json in the main.py file.

### Fixes:
- The side bar will not reopen after a restart of the app.
- The settings page will not appear more then once when you maintain Cmd+, now. (it would just make the OS laggy because of all of the settings pages)
- The save all shortcut now works (by changing the shortcut, i can't believe i haven't though of that...). For some reasons the Option key just does not get picked up by Notys.
- Fixed the macOS cursor not being the right "click" cursor.

### Known bugs:
- If the folder name is too long, the "X" to close the folder in the sidebar will be hidden.
- The middle click to close tabs was supposed to be added, but it does not work. Looking for fixing it in the next beta.
- For every shortcuts on windows with the "Control" key modifier, it will also work on macOS still as control ("^"). Still works with command tho.
- The search does not work (you can't open the search menu, not from the menu bar, not from shortcuts)
- The aesthetic of the buttons in the settings in dark mode is not very good. One of the buttons is better in light mode, the other, is as bad.

# v1.3.2
### Fixes:
- The bug making the "reopen last closed tab" shortcut not work is fixed. Not the save_all one, i tried to apply the same fix and it doesn't work...
- The menu bar was bugged from 1.3.1 on macOS (displaying the windows menubar). Now it is fixed.
*still lazy as fuck to reboot into windows and build an executable bruh*

# v1.3.1
### New:
- A new option in the menu bar -> File -> Open recent to see the last 10 opened files and to open them back quickly.
- Added a whole folder management. You can now open folder by dragndropping just like files and also open folder in a more classical way via the menu bar.
### Fixes:
- From v1.3.0.1, fixed the settings reseting every restart of the app.
- Fixed a bug where it would quit the app when you do Ctrl+Cmd+Q to lock macOS.

# v1.3.0.1
This is a quick hotfix, turned out the settings resetting after restart of the app bug was a single line fix...
(i literraly commented the "load_settings_from_disk()" function at line 364 which prevented the load of the settings... whoopsies)
*windows executable still to come, i'm too lazy to restart into windows and compile bruh*

# v1.3.0
### New:
- Added dynamic theme based on your system's one.
- When you press enter in a list, it now adds a dash to continue the list. Re-hitting enter cancels the new dash and ends the list.
### Removed:
- Removed the emojis in the settings panel
### Known bugs:
- The settings are now reseted to default when you restart the app

# v1.3.0 Beta 3
### New:
- added an update message if there's a newer version available.
- added shortcuts for text formatting
### Modification:
- modified the list's color to something less flashy

# v1.3.0 Beta 2
Still windows preview only.
By the way, when 1.3 will finally release, there will be macOS executables, but for now it's only windows Beta.

### Fixes:
- There is now an icon in the taskbar.

# v1.3.0 Beta 1
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
