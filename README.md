# Notys

**Notys** is an ultra-lightweight note-taking application designed for speed and simplicity.  
No bloat, just the essential features you need to get your thoughts down.

## Download
The latest version of Notys (v1.5.0) is currently available for:

*Compatibility note: The macOS files included here were used to build the 1.1.1 release.*

**Linux:**

*Notys relies on recent libraries. Non-rolling release distributions aren't officially supported, Arch Linux based distributions are recommended. You can try it anyways, it may work depending on your distro's library versions.*
*Notys will no longer be updated for linux, therefore the latest ""working"" (it was so buggy and hard to maintain i dropped support) is 1.1.2. I will not put the linux 1.1.2 versions in the newer version.*
- AppImage (Recommended, see "Get started" for more information)
- .zip and run in the .venv
- Source code

**Windows:**

- Windows .zip in the release sections 
- Source code

**macOS (INTEL ONLY!)**:

- .zip to extract the .app file
- Source code (to use the source code, you will need the build env (available in every notys release) and [Python 3.12](https://www.python.org/ftp/python/3.12.4/python-3.12.4-macos11.pkg) and to activate the .venv with `source .venv/bin/activate` or if you don't want to activate the .venv `python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt && python3 -m pip intall pyinstaller`)

## Features (Markdown-style)

Notys supports real-time formatting using a simple and intuitive syntax:

- **Headers:** Up to 4 levels (using `#`)

- **Bold:** `**text**`

- **Italic:** `*text*`

- **Code Blocks:** `````code`````

- **Text Coloration:** Using the `&^color text^&` syntax.

- **Strikethrough:** `~~strikethrough~~`

- **Highlight:** `==highlight==`

- **Underline**: using ```-: and :-```

- **Link**: using `[google](google.com)` you can create a link.

- **Drag & Drop:** Simply drop files into the app to open them instantly.

- **Languages**: There is support for French, Esperanto and English (English by default)

- **Settings**: Various settings for customization and more.
  
  ![showcase.png](./showcase.png)

  ![dragndropshowcase.gif](./dragndropshowcase.gif)

---

### What's behind the scenes?
Behind the scenes, Notys uses simple and lightweight technologies to do what it does.
It is built with Python, Tkinter (for the main window and some utilities), tkinterdnd2 (drag n drop support), Pillow (image/icon management), and JSON (to save the settings even when you restart the app).

Notys has been built mainly with the help of AI (such as Gemini, Claude, Copilot in GitHub and chatGPT). I (human) test it manually, imagine features and design prompts.

README has been through chatGPT to correct typos as I am not an native English speaker.

---

## Getting Started

### For macOS (Intel ONLY!)
**Quick precision, Notys WILL not work on Macs with Apple Silicon (M1, M2, M3, etc.) or on the MacBook Neo. Notys was built and tested on Intel Macs, including Hackintosh systems.**

1. Go to the **Releases** section on GitHub and navigate to the latest version.
2. Download the latest `Notys.zip`.
3. Unzip and move `Notys.app` to your **Applications** folder.
4. Open the app
5. Have fun!

### For Linux
*Linux is supported, but only on distributions with sufficiently recent library versions. Arch-based distributions are strongly recommended. Older/non-rolling distributions may encounter compatibility issues.*
*Notys will no longer be updated for linux, therefore the latest ""working"" (it was so buggy and hard to maintain i dropped support) is 1.1.2. I will not put the linux 1.1.2 versions in the newer releases on github.*
*If you want the latest version on Linux, you will have to either compile from build-env or run from build-env.*
1. Go to the **Releases** section on GitHub and navigate to the latest release available.
2. Download the Notys-build-env-x.x.x.zip
3. Run it from the source

### For Windows

1. Go to the **Releases** section on github and navigate to the latest release available.
2. Download the Notys-windows-x.x.x.zip (if it isn't here, just wait i'll be compiling it soon enough)
3. Extract the zip and place the Notys.exe and the _interal folder in the same parent folder (the .exe needs it to execute)
4. Run the .exe file

## Work in Progress (Roadmap)
### Planned for v1.5.1:
- [ ] Add more languages.
- [ ] Add a mission-control-ish overview
### Planned in the near or far future:
- [X] Liquid glass, maybe for 2.0.0
- [ ] macOS ARM Support, for 2.0.0
- [X] Switch to SwiftUI+Swift (or swift itself, i haven't decided yet), for 2.0.0

## Known bugs
### Minor Bugs
- [ ] **Keyboard shortcut:** The "Save All" and "Reopen Last Closed" keyboard shortcuts do not work, use the menu bar instead.
- [ ] **Light/Dark Theme Button**: The dark/light theme button in the tab bar doesn't display the right icon if started in light mode. Still completely usable at 100%. Just a UI bug.
