### v1.0
#### New:
- The app has been compiled in a .app for macOS.
- Added a logo.
#### Modification:
- The icon to change theme has been converted to a .png file.

### v0.4.1
#### New:
- Added the keyboard shortcut Ctrl+Shift+Tab to navigate between tabs easily.

### v0.4
#### New:
- Added more keyboard shortcuts:
    - Cmd / Ctrl+T: new tab
    - Cmd / Ctrl+Shift+T: reopen last closed tab
    - Cmd / Ctrl+N: new window (before it was to open a new tab)
    - Cmd / Ctrl+Opt / Alt+N: save every files (do not work, still in the v1.0. will probably be fixed in the next update)
#### Modification:
 - Nerdy change: Cmd / Ctrl+W now calls on_quit() (which closes the current window and quits the app if no more windows are open) when there's only one tab left.

### v0.3.1
#### New:
- Added zoom
#### Modification:
- Made the font bigger
#### Fixes:
- Fixed dragndrop on macOS

### v0.3
#### Fixes:
- Fixed dragndrop on Windows.
- Fixed an unnecessary space before the colored word when using the color feature. (before: "test  test", after: "test test" (github do not let me set a color for the text but it is working in the app)

### v0.2
#### New:
- Added highlighted text mode
- Added strikethrough text mode
- Added a search function
- Added a confirmation pop-up when closing the app and that some documents aren't saved.
#### Modification:
- Modification: the characters used for the style (e.g: ``**``) disappear when the cursor is not on the word
- Modification: the characters used to color the text was changed from "``$@red text@$`` to ``&^red text^&`` because of LaTeX which is present in many markdown editors.
#### Fixes:
- Fixed: the dot that indicates that the document is not saved was still visible when the document was saved
- Fixed theme icons

### v0.1
#### New:
- Added light and dark theme
- Added tabs
- Added pillow requierement (if you want to compile for yourself)
#### Modification:
- Changed the app title to show the file name in the title bar
- Changed font to Consolas
#### Fixes:
- Fixed a bug where two windows would pop-up at the start of the app (with one completely unsuable)

### beta v0.1
#### New:
- Added text coloration
- Added the possibility to open files
- Added the possibility to create new files (not usable in this version as there is no tabs and it would just delete your current document)
- Added undo and redo
- Added save as feature
#### Modification:
- Changed font the Andale Mono
#### Fixes:
- Fixed performance issues (in large documents)

### v0.0
#### New:
- Added headers from 1 to 4.
- Added italic
- Added bold
- Added code
- Added the save feature