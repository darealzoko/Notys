# 1.9.0 Beta 4

### Fix:
- A lot of things thanks to customtkinter being objectively better (fixed the scrollbar, the theme hazard, etc.)
- Also thx to customtkinter, it should theorically change and fix the windows's ugly UI

### Bugs:
- Scaling on Linux is broken and harder to read.

# 1.9.0 Beta 3

### Fix:
- Fixed the beta release alert thinking that itself was newer than itself (thinking v1.9.0.b2 was newer than v1.9.0.b2)
- Fixed the refresh of new release at every launch of the app, before it was doing it sometimes on some relaunches.

### Modify:
- Modified the Beta alert to be orange to see at a quick look that the new release is in Beta.

# 1.9.0 Beta 2

### Add:
- Added date and time timestamps.
- Added the "revert to last saved".
- Added an option to see beta releases as an alert.

### Fix:
- Fixed the french translation of "Format" to "Formater"

# 1.9.0 Beta 1

### Add:
- "Copy", "Cut" and "Paste" in the right click menu.
- The "Format" menu in the menu bar with every markdown styles for quick formatting

### Modify:
- The markdown code (like the "#") are now greyed so visible, but less aggressive.

# 1.8.2

### Fix:
- Fixed the setting being unusable if you resize it too low; added a minimum width size.
- Fixed a duplicate: there was an update message in the settings. Removed it.
- Fixed the new line in a list not scrolling automatically to show the new line.
- Fixed the cmd+q quitting the app no matter what. Now, if there's any unsaved tabs it will show a prompt asking if you want to save or not.
- Fixed the list, when you paste a list with dashes made in an other app it stays with dashes instead of the dots.

### Known bugs:
- When you paste a list from an other app, it doesn't really create a new line automatically. It's a really small bug; everything is usable but a bit annoying.

# 1.8.1

### Fix:
- Preventing the update message from tweaking out when there's no more newer updates on ARM MacOS running throught Rosetta.

# 1.8.0

### Add:
- Right click menu for markdown syntax
- Right click menu on tabs for options

### Fixes:
- Fixed the update message
- Fixed the language's tab in the settings. Now it doesn't crop out of sight when you resize the settings.
- Middle click to close a tab is now working in macOS as well!
- Fixed a bug where Cmd/Ctrl+V would paste twice the same text.

# 1.8.0 Beta 2

### Fix:
- Fixed a bug where Windows's build could not complete. The solution was adding 'striprtf' to hiddenimports in Notys.spec (has been fixed but not published for the windows build on Beta 1)

# 1.8.0 Beta 1

### Add:
- More menu bar options (a "View" and "Open file in Finder" option)
- Added a "hover" menu in the file name in the bottom left where you can easily copy the filepath of your file.
- Added a shortcut to open the file in Finder/File Explorer (Cmd/Ctrl+Shift+F)

# 1.7.1
### Minor Add:
- Added a dark column for the styles, that way I fixed the light theme being unreadable now readable.
- Added new installation form for macOS, introducing .dmg. First attempt, it may not be perfect but sure usable.

### Fix:
- Fixed a bug where text would be unreadable on light theme.
- Fixed a bug where you could not do bold

### Known bugs:
- The update text message is still not appearing if there's a new update

# 1.7.0

### Add:
- Added new languages (spanish, portuguese, german, italian, dutch, russian, japanese, chinese, korean)

### Modification:
- Made english the first language in the language list instead of french in the settings.

### Fix:
- Fixed translations not applying everywhere. For example; the style section in the settings could not be translated.

# 1.6.2

### Minor Add:
- Added the "text" option in the style settings page (yes, i wanted to give this a whole new version)

# 1.6.1

### Fix:
- Fixed the style setting's page button theme making it harder to read.

### Modification:
- Redesigned the style setting's page for the button and usability part.

# 1.6.0

### Add:
- Added .rtf support
- Added a comment at the very top of the main.py file, writing where the config files are stored.
- Added styles. Styles are making YOU able to customize the markdown syntax, right in the settings.

# 1.5.0

### Add:
- Added pinned tabs. Pinned tabs re-open when you close and re-start Notys. To toggle it, you do cmd/ctrl+shift+p or do it in the menu bar.

### Modification:
- Redesigned settings to "General" with everything nicely organized in subcategories and "Language" with only languages.

### Removed:
- Removed underscore-based italics (didn't work in 1.4.1); asterisks still apply italics.

### Fixes:
- Nothing to be fixed yet!

### Known bugs:
- When you navigate the settings categories, you have to move the mouse for the page to refresh.
- The update text does not appear anymore.

# 1.4.1

### Fixes:
- Tried to fix the typing delay. It is not gone, but much shorter.
- Tried the fix the scrollbar sensitivity. Still a bit off, but way better.
- Fixed a bug where the link would not disappear leaving `[google](google.com)` instead of just [google](google.com).

### Removed:
- Removed the ability of doing an italic text with the underscores.

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
