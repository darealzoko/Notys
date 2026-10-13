# Config files are stored in the Notys config directory: ~/Library/Application Support/Notys on macOS,
# %APPDATA%/Notys on Windows, and $XDG_CONFIG_HOME/Notys (or ~/.config/Notys) on Linux.
# The files are settings.json, recents_doc.json, and pin_docs.json.
import tkinter as tk # [Check custom tkinter or theme modules here]
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk # [Import additional dialogs or widgets if needed]
import os # [Handle custom path operations or environment variables]
import sys # [Modify sys.path or handle command-line arguments here]
import re # [Adjust regex patterns for markdown parsing or custom tokens]
import platform # [Add checks for other OS types if necessary]
from PIL import Image, ImageTk # [Handle custom image formats or caching]
import json # [Switch to TOML/YAML for settings if required]
import time
from striprtf.striprtf import rtf_to_text
from style_manager import STYLE_ELEMENTS, StyleManager

try: # [Handle missing version module or fallback errors]
    import version # [Ensure version.py exists in build path]
    APP_NAME = version.APP_NAME # [Override app name dynamically]
    APP_VERSION = version.SHORT_VERSION # [Update version format]
    APP_COPYRIGHT = version.COPYRIGHT # [Change copyright notice]
except ImportError: # [Fallback when version module is missing]
    APP_NAME = 'Notys' # [Change default app name here]
    APP_VERSION = '1.7.0' # [Update default version string]
    APP_COPYRIGHT = 'Copyright by _zoko © 2026' # [Update copyright year/text]

# ── OS detection & Cursor Configuration ───────────────────────────────────────
is_macos = platform.system() == 'Darwin' # [Add Linux/Windows specific flags]
mod_key = 'Command' if is_macos else 'Control' # [Change accelerator modifier keys]
mod_display = 'Cmd+' if is_macos else 'Ctrl+' # [Change modifier display string]
HAND_CURSOR = 'pointinghand' if is_macos else 'hand2' # [Fix macOS pointer hand cursor]

def resource_path(relative_path): # [Customize resource lookup for assets/icons]
    """Transforme un chemin relatif en chemin absolu pour PyInstaller.
    Fonctionne pour les fichiers individuels et les dossiers.
    """
    try: # [Handle PyInstaller bundle paths]
        base_path = sys._MEIPASS # [Access temp folder path]
    except Exception: # [Fallback for normal python execution]
        base_path = os.path.abspath(".") # [Use current working directory]

    return os.path.join(base_path, relative_path) # [Validate final absolute path]

try: # [Handle optional tkinterdnd2 package]
    from tkinterdnd2 import Tk as DnDTk, DND_FILES # [Import drag and drop classes]
    DND_AVAILABLE = True # [Flag indicating DND is supported]
except Exception: # [Fallback if tkinterdnd2 is not installed]
    DnDTk = None # [Set DnDTk to None]
    DND_FILES = None # [Set DND_FILES to None]
    DND_AVAILABLE = False # [Disable drag and drop features]

def get_system_theme(): # [Extend system theme detection for Linux/custom DEs]
    """Detects the operating system's current theme."""
    system = platform.system() # [Get current OS platform name]
    if system == 'Darwin': # [macOS theme detection logic]
        try:
            import subprocess # [Run defaults command]
            res = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], capture_output=True, text=True) # [Check Apple interface style]
            if 'Dark' in res.stdout: # [Check if output contains Dark]
                return 'dark' # [Return dark theme string]
        except Exception: # [Handle subprocess errors gracefully]
            pass
    elif system == 'Windows': # [Windows theme detection logic]
        try:
            import winreg # [Import Windows registry module]
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) # [Connect to HKCU registry]
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") # [Open personalize key]
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme") # [Query light theme preference value]
            if value == 0: # [0 means dark mode enabled]
                return 'dark' # [Return dark theme string]
        except Exception: # [Handle registry access errors]
            pass
    
    # Default fallback for Linux or if detection fails
    return 'light' # [Default theme fallback value]

# ── Langues ───────────────────────────────────────────────────────────────────
TRANSLATIONS = { # [Add new languages or translation keys here]
    'fr': { # [French translations dictionary]
        'menu_file': "Fichier", # [Translate file menu label]
        'menu_new_window': "Nouvelle fenêtre", # [Translate new window]
        'menu_new_tab': "Nouvel onglet", # [Translate new tab]
        'menu_reopen_tab': "Rouvrir l'onglet fermé", # [Translate reopen tab]
        'menu_open': "Ouvrir…", # [Translate open]
        'menu_open_folder': "Ouvrir le dossier…", # [Translate open folder]
        'menu_open_recents': "Ouvrir récents", # [Translate open recents]
        'menu_close_tab': "Fermer l'onglet", # [Translate close tab]
        'menu_toggle_pin': "Épingler / désépingler l'onglet",
        'menu_save': "Enregistrer", # [Translate save]
        'menu_save_all': "Tout enregistrer", # [Translate save all]
        'menu_save_as': "Enregistrer sous…", # [Translate save as]

        'menu_edit': "Édition", # [Translate edit menu]
        'menu_undo': "Annuler", # [Translate undo]
        'menu_redo': "Rétablir", # [Translate redo]
        'menu_cut': "Couper", # [Translate cut]
        'menu_copy': "Copier", # [Translate copy]
        'menu_paste': "Coller", # [Translate paste]
        'menu_find': "Rechercher…", # [Translate find]

        'menu_window': "Fenêtre", # [Translate window menu]
        'menu_minimize': "Réduire", # [Translate minimize]

        'menu_settings': "Paramètres", # [Translate settings]
        'menu_open_settings': "Ouvrir les paramètres…", # [Translate open settings]
        
        'menu_about': "À propos", # [Translate about]

        'settings_title': "Paramètres", # [Translate settings title]
        'settings_apply': "Appliquer", # [Translate apply button]
        'settings_cancel': "Annuler", # [Translate cancel button]

        'section_language': "Langue", # [Translate language section]
        'section_general': "Général",
        'section_appearance': "Apparence", # [Translate appearance section]
        'section_editor': "Éditeur", # [Translate editor section]
        'section_interface': "Interface", # [Translate interface section]
            'section_styles': "Styles",

        'settings_language': "Langue de l'interface", # [Translate interface language label]
        'settings_theme': "Thème", # [Translate theme label]
        'theme_dark': "Sombre", # [Translate dark theme]
        'theme_light': "Clair", # [Translate light theme]
        'theme_system': "Système", # [Translate system theme]

        'settings_font_family': "Police", # [Translate font family label]
        'settings_font_size': "Taille de police", # [Translate font size label]
        'settings_line_height': "Hauteur de ligne", # [Translate line height label]
        'settings_line_wrap': "Retour à la ligne", # [Translate line wrap label]
        'wrap_word': "Par mot", # [Translate word wrap]
        'wrap_char': "Par caractère", # [Translate char wrap]
        'wrap_none': "Aucun", # [Translate no wrap]
        'settings_padding': "Marges latérales", # [Translate padding label]

        'settings_show_status': "Barre de statut", # [Translate status bar toggle]
        'settings_show_wordcount': "Compteur de mots", # [Translate word count toggle]
        'settings_win_size': "Taille de fenêtre par défaut", # [Translate window size label]
        'on': "Activé", # [Translate 'on']
        'off': "Désactivé", # [Translate 'off']

        'dlg_save_title': "", # [Set save dialog title]
        'dlg_save_msg': 'Voulez-vous enregistrer les modifications\napportées à "{name}" ?', # [Translate save prompt message]
        'dlg_save_sub': "Vos modifications seront perdues si vous ne les enregistrez pas.", # [Translate save prompt subtitle]
        'dlg_dont_save': "Ne pas enregistrer", # [Translate discard changes button]
        'dlg_cancel': "Annuler", # [Translate dialog cancel button]
        'dlg_save': "Enregistrer…", # [Translate dialog save button]

        'status_words_one': "mot", # [Singular word status]
        'status_words_many': "mots", # [Plural word status]
        'status_untitled': "Sans titre", # [Untitled document status]

        'search_no_results': "Aucun résultat", # [Search no results text]
        'sidebar_explorer': "EXPLORATEUR", # [Sidebar explorer title]
        'no_folder': "Aucun dossier ouvert", # [No folder opened text]

        'dnd_title': "Drag & Drop indisponible", # [DND warning title]
        'dnd_msg': ( # [DND warning message body]
            "Le glisser-déposer n'est pas disponible :\n"
            "tkinterdnd2 est introuvable.\n\n"
            "Installez-le avec :\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Redémarrez ensuite Notys."
        ),

        'untitled': "Sans titre", # [Default untitled tab name]
    },
    'en': { # [English translations dictionary]
        'menu_file': "File", # [File menu label]
        'menu_new_window': "New Window", # [New window menu]
        'menu_new_tab': "New Tab", # [New tab menu]
        'menu_reopen_tab': "Reopen Closed Tab", # [Reopen tab menu]
        'menu_open': "Open…", # [Open menu]
        'menu_open_folder': "Open Folder…", # [Open folder menu]
        'menu_open_recents': "Open Recent", # [Open recent menu]
        'menu_close_tab': "Close Tab", # [Close tab menu]
        'menu_toggle_pin': "Toggle Tab Pin",
        'menu_save': "Save", # [Save menu]
        'menu_save_all': "Save All", # [Save all menu]
        'menu_save_as': "Save As…", # [Save as menu]

        'menu_edit': "Edit", # [Edit menu]
        'menu_undo': "Undo", # [Undo menu]
        'menu_redo': "Redo", # [Redo menu]
        'menu_cut': "Cut", # [Cut menu]
        'menu_copy': "Copy", # [Copy menu]
        'menu_paste': "Paste", # [Paste menu]
        'menu_find': "Find…", # [Find menu]

        'menu_window': "Window", # [Window menu]
        'menu_minimize': "Minimize", # [Minimize menu]

        'menu_settings': "Settings", # [Settings menu]
        'menu_open_settings': "Open Settings…", # [Open settings menu]
        
        'menu_about': "About", # [About menu]

        'settings_title': "Settings", # [Settings title]
        'settings_apply': "Apply", # [Apply button]
        'settings_cancel': "Cancel", # [Cancel button]

        'section_language': "Language", # [Language section]
        'section_general': "General",
        'section_appearance': "Appearance", # [Appearance section]
        'section_editor': "Editor", # [Editor section]
        'section_interface': "Interface", # [Interface section]
        'section_styles': "Styles",

        'settings_language': "Interface language", # [Language label]
        'settings_theme': "Theme", # [Theme label]
        'theme_dark': "Dark", # [Dark theme option]
        'theme_light': "Light", # [Light theme option]
        'theme_system': "System", # [System theme option]

        'settings_font_family': "Font", # [Font family label]
        'settings_font_size': "Font size", # [Font size label]
        'settings_line_height': "Line height", # [Line height label]
        'settings_line_wrap': "Line wrap", # [Line wrap label]
        'wrap_word': "By word", # [Word wrap option]
        'wrap_char': "By character", # [Character wrap option]
        'wrap_none': "None", # [No wrap option]
        'settings_padding': "Side margins", # [Padding label]

        'settings_show_status': "Status bar", # [Status bar label]
        'settings_show_wordcount': "Word counter", # [Word counter label]
        'settings_win_size': "Default window size", # [Window size label]
        'on': "On", # [On label]
        'off': "Off", # [Off label]

        'dlg_save_title': "", # [Save dialog title]
        'dlg_save_msg': 'Do you want to save the changes\nmade to "{name}"?', # [Save message]
        'dlg_save_sub': "Your changes will be lost if you don't save them.", # [Save subtitle]
        'dlg_dont_save': "Don't Save", # [Don't save button]
        'dlg_cancel': "Cancel", # [Cancel button]
        'dlg_save': "Save…", # [Save button]

        'status_words_one': "word", # [Singular word]
        'status_words_many': "words", # [Plural words]
        'status_untitled': "Untitled", # [Untitled status]

        'search_no_results': "No results", # [Search no results]
        'sidebar_explorer': "EXPLORER", # [Explorer title]
        'no_folder': "No folder opened", # [No folder message]

        'dnd_title': "Drag & Drop Unavailable", # [DND unavailable title]
        'dnd_msg': ( # [DND unavailable message]
            "Drag & drop support is not available:\n"
            "tkinterdnd2 was not found.\n\n"
            "Install it with:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Then restart Notys."
        ),

        'untitled': "Untitled", # [Untitled tab name]
    },
    'eo': { # esperanto language
        'menu_file': "Dosiero", # [File menu label]
        'menu_new_window': "Nova fenestro", # [New window menu]
        'menu_new_tab': "Nova langeto", # [New tab menu]
        'menu_reopen_tab': "Remalfermi fermitan langeton", # [Reopen tab menu]
        'menu_open': "Malfermi...", # [Open menu]
        'menu_open_folder': "Malfermi dosieron", # [Open folder menu]
        'menu_open_recents': "Malfermi recentaj", # [Open recent menu]
        'menu_close_tab': "Fermi langeton", # [Close tab menu]
        'menu_toggle_pin': "Alpingli / malalpingli langeton",
        'menu_save': "Konservi", # [Save menu]
        'menu_save_all': "Konservi ĉiujn", # [Save all menu]
        'menu_save_as': "Konservi kiel...", # [Save as menu]

        'menu_edit': "Redakti", # [Edit menu]
        'menu_undo': "Malfari", # [Undo menu]
        'menu_redo': "Refari", # [Redo menu]
        'menu_cut': "Eltondi", # [Cut menu]
        'menu_copy': "Kopii", # [Copy menu]
        'menu_paste': "Alglui", # [Paste menu]
        'menu_find': "Serĉi...", # [Find menu]

        'menu_window': "Fenestro", # [Window menu]
        'menu_minimize': "Redukti", # [Minimize menu]

        'menu_settings': "Agordoj", # [Settings menu]
        'menu_open_settings': "Malfermi agordojn", # [Open settings menu]
        
        'menu_about': "Pri", # [About menu]

        'settings_title': "Agordoj", # [Settings title]
        'settings_apply': "Apliki", # [Apply button]
        'settings_cancel': "Nuligi", # [Cancel button]*
        # got to translate all three of the above thanks to minecraft :3

        'section_language': "Lingvo", # [Language section]
        'section_general': "Ĝenerala",
        'section_appearance': "Aspekto", # [Appearance section]
        'section_editor': "Tekstredaktilo", # [Editor section]
        'section_interface': "Interfaco", # [Interface section]
        'section_styles': "Stiloj",

        'settings_language': "Lingvo de la interfaco", # [Language label]
        'settings_theme': "Temo", # [Theme label]
        'theme_dark': "Malhela", # [Dark theme option]
        'theme_light': "Hela", # [Light theme option]
        'theme_system': "Sistema", # [System theme option]
        # vibe-translated for the all five above, not sure at all

        'settings_font_family': "Tiparo", # [Font family label]
        'settings_font_size': "Tipargrandeco", # [Font size label]
        'settings_line_height': "Linia alto", # [Line height label]
        'settings_line_wrap': "Linia envolvo", # [Line wrap label]
        'wrap_word': "Laŭ vortoj", # [Word wrap option]
        'wrap_char': "Laŭ signoj", # [Character wrap option]
        'wrap_none': "Neniu", # [No wrap option]
        'settings_padding': "Flankaj marĝenoj", # [Padding label]

        'settings_show_status': "Statusbreto", # [Status bar label]
        'settings_show_wordcount': "Vortnombrilo", # [Word counter label]
        'settings_win_size': "Defaŭlta fenestra alto", # [Window size label]
        'on': "Ŝaltita", # [On label]
        'off': "Malŝaltita", # [Off label]
        # all vibe coded for the five above

        'dlg_save_title': "Konservi al {name}", # [Save dialog title]
        'dlg_save_msg': 'Ĉu vi volas konservi la ŝanĝojn \nfaritajn al "{name}"?', # [Save message]
        'dlg_save_sub': "Viaj ŝanĝoj estos perditaj se vi ne konservos ilin.", # [Save subtitle]
        # not sure about the "ilin"
        'dlg_dont_save': "Ne konservi", # [Don't save button]
        'dlg_cancel': "Nuligi", # [Cancel button]
        'dlg_save': "Konservi...", # [Save button]

        'status_words_one': "vorto", # [Singular word]
        'status_words_many': "vortoj", # [Plural words]
        'status_untitled': "Sen titro", # [Untitled status]
        # vibe translated for sen titro

        'search_no_results': "Neniuj rezultoj", # [Search no results]
        # maybe "neniuj rezultoj" could be better, but i kinda prefer sen rezultoj
        'sidebar_explorer': "DOSIEROJ", # [Explorer title]
        'no_folder': "Neniu dosierujo malfermita", # [No folder message]
        # idk about the two of above

        'dnd_title': "Drag & Drop Ne Disponeblas", # [DND unavailable title]
        'dnd_msg': ( # [DND unavailable message]
            "Drag & Drop Ne Disponeblas:\n"
            "tkinterdnd2 ne estis trovita. \n\n"
            "Instalu ĝin tajpante en via terminalo:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Kaj restartigu Notyso."
        ),

        'untitled': "Sen titro", # [Untitled tab name]
    },
    'es': { # [Spanish translations dictionary]
        'menu_file': "Archivo", # [File menu label]
        'menu_new_window': "Nueva ventana", # [New window menu]
        'menu_new_tab': "Nueva pestaña", # [New tab menu]
        'menu_reopen_tab': "Reabrir pestaña cerrada", # [Reopen tab menu]
        'menu_open': "Abrir...", # [Open menu]
        'menu_open_folder': "Abrir carpeta...", # [Open folder menu]
        'menu_open_recents': "Abrir recientes", # [Open recent menu]
        'menu_close_tab': "Cerrar pestaña", # [Close tab menu]
        'menu_toggle_pin': "Anclar / Desanclar pestaña",
        'menu_save': "Guardar", # [Save menu]
        'menu_save_all': "Guardar todo", # [Save all menu]
        'menu_save_as': "Guardar como...", # [Save as menu]

        'menu_edit': "Edición", # [Edit menu]
        'menu_undo': "Deshacer", # [Undo menu]
        'menu_redo': "Rehacer", # [Redo menu]
        'menu_cut': "Cortar", # [Cut menu]
        'menu_copy': "Copiar", # [Copy menu]
        'menu_paste': "Pegar", # [Paste menu]
        'menu_find': "Buscar...", # [Find menu]

        'menu_window': "Ventana", # [Window menu]
        'menu_minimize': "Minimizar", # [Minimize menu]

        'menu_settings': "Ajustes", # [Settings menu]
        'menu_open_settings': "Abrir ajustes", # [Open settings menu]

        'menu_about': "Acerca de", # [About menu]

        'settings_title': "Ajustes", # [Settings title]
        'settings_apply': "Aplicar", # [Apply button]
        'settings_cancel': "Cancelar", # [Cancel button]

        'section_language': "Idioma", # [Language section]
        'section_general': "General",
        'section_appearance': "Apariencia", # [Appearance section]
        'section_editor': "Editor", # [Editor section]
        'section_interface': "Interfaz", # [Interface section]
        'section_styles': "Estilos",

        'settings_language': "Idioma de la interfaz", # [Language label]
        'settings_theme': "Tema", # [Theme label]
        'theme_dark': "Oscuro", # [Dark theme option]
        'theme_light': "Claro", # [Light theme option]
        'theme_system': "Sistema", # [System theme option]

        'settings_font_family': "Fuente", # [Font family label]
        'settings_font_size': "Tamaño de fuente", # [Font size label]
        'settings_line_height': "Altura de línea", # [Line height label]
        'settings_line_wrap': "Ajuste de línea", # [Line wrap label]
        'wrap_word': "Por palabra", # [Word wrap option]
        'wrap_char': "Por carácter", # [Character wrap option]
        'wrap_none': "Ninguno", # [No wrap option]
        'settings_padding': "Márgenes laterales", # [Padding label]

        'settings_show_status': "Barra de estado", # [Status bar label]
        'settings_show_wordcount': "Contador de palabras", # [Word counter label]
        'settings_win_size': "Tamaño predeterminado de la ventana", # [Window size label]
        'on': "Activado", # [On label]
        'off': "Desactivado", # [Off label]

        'dlg_save_title': "Guardar {name}", # [Save dialog title]
        'dlg_save_msg': '¿Quieres guardar los cambios\nrealizados en "{name}"?', # [Save message]
        'dlg_save_sub': "Los cambios se perderán si no los guardas.", # [Save subtitle]
        'dlg_dont_save': "No guardar", # [Don't save button]
        'dlg_cancel': "Cancelar", # [Cancel button]
        'dlg_save': "Guardar...", # [Save button]

        'status_words_one': "palabra", # [Singular word]
        'status_words_many': "palabras", # [Plural words]
        'status_untitled': "Sin título", # [Untitled status]

        'search_no_results': "Sin resultados", # [Search no results]
        'sidebar_explorer': "EXPLORADOR", # [Explorer title]
        'no_folder': "No hay ninguna carpeta abierta", # [No folder message]

        'dnd_title': "Arrastrar y soltar no disponible", # [DND unavailable title]
        'dnd_msg': ( # [DND unavailable message]
            "La función de arrastrar y soltar no está disponible:\n"
            "tkinterdnd2 no se encontró.\n\n"
            "Instálalo con:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Luego reinicia Notys."
        ),

        'untitled': "Sin título", # [Untitled tab name]
    },
    'pt': {  # [Portuguese translations dictionary]
        'menu_file': "Arquivo",
        'menu_new_window': "Nova janela",
        'menu_new_tab': "Nova aba",
        'menu_reopen_tab': "Reabrir guia fechada",
        'menu_open': "Abrir…",
        'menu_open_folder': "Abrir pasta…",
        'menu_open_recents': "Abrir recentes",
        'menu_close_tab': "Fechar guia",
        'menu_toggle_pin': "Fixar / desafixar guia",
        'menu_save': "Salvar",
        'menu_save_all': "Salvar tudo",
        'menu_save_as': "Salvar como…",

        'menu_edit': "Edição",
        'menu_undo': "Desfazer",
        'menu_redo': "Refazer",
        'menu_cut': "Recortar",
        'menu_copy': "Copiar",
        'menu_paste': "Colar",
        'menu_find': "Buscar…",

        'menu_window': "Janela",
        'menu_minimize': "Minimizar",

        'menu_settings': "Configurações",
        'menu_open_settings': "Abrir configurações…",
        'menu_about': "Sobre",

        'settings_title': "Configurações",
        'settings_apply': "Aplicar",
        'settings_cancel': "Cancelar",

        'section_language': "Idioma",
        'section_general': "Geral",
        'section_appearance': "Aparência",
        'section_editor': "Editor",
        'section_interface': "Interface",
        'section_styles': "Estilos",

        'settings_language': "Idioma da interface",
        'settings_theme': "Tema",
        'theme_dark': "Escuro",
        'theme_light': "Claro",
        'theme_system': "Sistema",

        'settings_font_family': "Fonte",
        'settings_font_size': "Tamanho da fonte",
        'settings_line_height': "Altura da linha",
        'settings_line_wrap': "Quebra de linha",
        'wrap_word': "Por palavra",
        'wrap_char': "Por caractere",
        'wrap_none': "Nenhuma",
        'settings_padding': "Margens laterais",

        'settings_show_status': "Barra de estado",
        'settings_show_wordcount': "Contador de palavras",
        'settings_win_size': "Tamanho padrão da janela",
        'on': "Ativado",
        'off': "Desativado",

        'dlg_save_title': "Salvar {name}",
        'dlg_save_msg': 'Deseja salvar as alterações\nfeitas em "{name}"?',
        'dlg_save_sub': "As alterações serão perdidas se você não as salvar.",
        'dlg_dont_save': "Não salvar",
        'dlg_cancel': "Cancelar",
        'dlg_save': "Salvar…",

        'status_words_one': "palavra",
        'status_words_many': "palavras",
        'status_untitled': "Sem título",

        'search_no_results': "Nenhum resultado",
        'sidebar_explorer': "EXPLORADOR",
        'no_folder': "Nenhuma pasta aberta",

        'dnd_title': "Arrastar e soltar indisponível",
        'dnd_msg': (
            "A função de arrastar e soltar não está disponível:\n"
            "tkinterdnd2 não foi encontrado.\n\n"
            "Instale com:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Em seguida, reinicie o Notys."
        ),

        'untitled': "Sem título",
    },
    'de': {  # [German translations dictionary]
        'menu_file': "Datei",
        'menu_new_window': "Neues Fenster",
        'menu_new_tab': "Neuer Tab",
        'menu_reopen_tab': "Geschlossenen Tab erneut öffnen",
        'menu_open': "Öffnen…",
        'menu_open_folder': "Ordner öffnen…",
        'menu_open_recents': "Zuletzt verwendet",
        'menu_close_tab': "Tab schließen",
        'menu_toggle_pin': "Tab anheften / lösen",
        'menu_save': "Speichern",
        'menu_save_all': "Alles speichern",
        'menu_save_as': "Speichern unter…",

        'menu_edit': "Bearbeiten",
        'menu_undo': "Rückgängig",
        'menu_redo': "Wiederholen",
        'menu_cut': "Ausschneiden",
        'menu_copy': "Kopieren",
        'menu_paste': "Einfügen",
        'menu_find': "Suchen…",

        'menu_window': "Fenster",
        'menu_minimize': "Minimieren",

        'menu_settings': "Einstellungen",
        'menu_open_settings': "Einstellungen öffnen…",
        'menu_about': "Info",

        'settings_title': "Einstellungen",
        'settings_apply': "Übernehmen",
        'settings_cancel': "Abbrechen",

        'section_language': "Sprache",
        'section_general': "Allgemein",
        'section_appearance': "Erscheinungsbild",
        'section_editor': "Editor",
        'section_interface': "Oberfläche",
        'section_styles': "Stile",

        'settings_language': "Sprache der Oberfläche",
        'settings_theme': "Thema",
        'theme_dark': "Dunkel",
        'theme_light': "Hell",
        'theme_system': "System",

        'settings_font_family': "Schriftart",
        'settings_font_size': "Schriftgröße",
        'settings_line_height': "Zeilenabstand",
        'settings_line_wrap': "Zeilenumbruch",
        'wrap_word': "Nach Wort",
        'wrap_char': "Nach Zeichen",
        'wrap_none': "Keiner",
        'settings_padding': "Seitenabstände",

        'settings_show_status': "Statusleiste",
        'settings_show_wordcount': "Wortzähler",
        'settings_win_size': "Standardfenstergröße",
        'on': "An",
        'off': "Aus",

        'dlg_save_title': "{name} speichern",
        'dlg_save_msg': 'Möchten Sie die Änderungen\nan "{name}" speichern?',
        'dlg_save_sub': "Ihre Änderungen gehen verloren, wenn Sie sie nicht speichern.",
        'dlg_dont_save': "Nicht speichern",
        'dlg_cancel': "Abbrechen",
        'dlg_save': "Speichern…",

        'status_words_one': "Wort",
        'status_words_many': "Wörter",
        'status_untitled': "Unbenannt",

        'search_no_results': "Keine Ergebnisse",
        'sidebar_explorer': "EXPLORER",
        'no_folder': "Kein Ordner geöffnet",

        'dnd_title': "Drag & Drop nicht verfügbar",
        'dnd_msg': (
            "Drag & Drop ist nicht verfügbar:\n"
            "tkinterdnd2 wurde nicht gefunden.\n\n"
            "Installieren Sie es mit:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Starten Sie Notys danach neu."
        ),

        'untitled': "Unbenannt",
    },
    'it': {  # [Italian translations dictionary]
        'menu_file': "File",
        'menu_new_window': "Nuova finestra",
        'menu_new_tab': "Nuova scheda",
        'menu_reopen_tab': "Riapri scheda chiusa",
        'menu_open': "Apri…",
        'menu_open_folder': "Apri cartella…",
        'menu_open_recents': "Apri recenti",
        'menu_close_tab': "Chiudi scheda",
        'menu_toggle_pin': "Blocca / sblocca scheda",
        'menu_save': "Salva",
        'menu_save_all': "Salva tutto",
        'menu_save_as': "Salva con nome…",

        'menu_edit': "Modifica",
        'menu_undo': "Annulla",
        'menu_redo': "Ripristina",
        'menu_cut': "Taglia",
        'menu_copy': "Copia",
        'menu_paste': "Incolla",
        'menu_find': "Cerca…",

        'menu_window': "Finestra",
        'menu_minimize': "Minimizza",

        'menu_settings': "Impostazioni",
        'menu_open_settings': "Apri impostazioni…",
        'menu_about': "Informazioni",

        'settings_title': "Impostazioni",
        'settings_apply': "Applica",
        'settings_cancel': "Annulla",

        'section_language': "Lingua",
        'section_general': "Generale",
        'section_appearance': "Aspetto",
        'section_editor': "Editor",
        'section_interface': "Interfaccia",
        'section_styles': "Stili",

        'settings_language': "Lingua dell'interfaccia",
        'settings_theme': "Tema",
        'theme_dark': "Scuro",
        'theme_light': "Chiaro",
        'theme_system': "Sistema",

        'settings_font_family': "Carattere",
        'settings_font_size': "Dimensione carattere",
        'settings_line_height': "Altezza riga",
        'settings_line_wrap': "A capo automatico",
        'wrap_word': "Per parola",
        'wrap_char': "Per carattere",
        'wrap_none': "Nessuno",
        'settings_padding': "Margini laterali",

        'settings_show_status': "Barra di stato",
        'settings_show_wordcount': "Conteggio parole",
        'settings_win_size': "Dimensione predefinita della finestra",
        'on': "Attivo",
        'off': "Disattivo",

        'dlg_save_title': "Salva {name}",
        'dlg_save_msg': 'Vuoi salvare le modifiche\napplicate a "{name}"?',
        'dlg_save_sub': "Le modifiche andranno perse se non le salvi.",
        'dlg_dont_save': "Non salvare",
        'dlg_cancel': "Annulla",
        'dlg_save': "Salva…",

        'status_words_one': "parola",
        'status_words_many': "parole",
        'status_untitled': "Senza titolo",

        'search_no_results': "Nessun risultato",
        'sidebar_explorer': "ESPLORATORE",
        'no_folder': "Nessuna cartella aperta",

        'dnd_title': "Drag & Drop non disponibile",
        'dnd_msg': (
            "Drag & drop non disponibile:\n"
            "tkinterdnd2 non è stato trovato.\n\n"
            "Installalo con:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Poi riavvia Notys."
        ),

        'untitled': "Senza titolo",
    },
    'nl': {  # [Dutch translations dictionary]
        'menu_file': "Bestand",
        'menu_new_window': "Nieuw venster",
        'menu_new_tab': "Nieuw tabblad",
        'menu_reopen_tab': "Gesloten tabblad opnieuw openen",
        'menu_open': "Openen…",
        'menu_open_folder': "Map openen…",
        'menu_open_recents': "Recent openen",
        'menu_close_tab': "Tabblad sluiten",
        'menu_toggle_pin': "Tabblad vastzetten / losmaken",
        'menu_save': "Opslaan",
        'menu_save_all': "Alles opslaan",
        'menu_save_as': "Opslaan als…",

        'menu_edit': "Bewerken",
        'menu_undo': "Ongedaan maken",
        'menu_redo': "Opnieuw",
        'menu_cut': "Knippen",
        'menu_copy': "Kopiëren",
        'menu_paste': "Plakken",
        'menu_find': "Zoeken…",

        'menu_window': "Venster",
        'menu_minimize': "Minimaliseren",

        'menu_settings': "Instellingen",
        'menu_open_settings': "Instellingen openen…",
        'menu_about': "Over",

        'settings_title': "Instellingen",
        'settings_apply': "Toepassen",
        'settings_cancel': "Annuleren",

        'section_language': "Taal",
        'section_general': "Algemeen",
        'section_appearance': "Uiterlijk",
        'section_editor': "Editor",
        'section_interface': "Interface",
        'section_styles': "Stijlen",

        'settings_language': "Taal van de interface",
        'settings_theme': "Thema",
        'theme_dark': "Donker",
        'theme_light': "Licht",
        'theme_system': "Systeem",

        'settings_font_family': "Lettertype",
        'settings_font_size': "Tekengrootte",
        'settings_line_height': "Regelhoogte",
        'settings_line_wrap': "Regelafbreking",
        'wrap_word': "Per woord",
        'wrap_char': "Per teken",
        'wrap_none': "Geen",
        'settings_padding': "Zijmarges",

        'settings_show_status': "Statusbalk",
        'settings_show_wordcount': "Woordtelling",
        'settings_win_size': "Standaard venstergrootte",
        'on': "Aan",
        'off': "Uit",

        'dlg_save_title': "Opslaan {name}",
        'dlg_save_msg': 'Wilt u de wijzigingen\nin "{name}" opslaan?',
        'dlg_save_sub': "Uw wijzigingen gaan verloren als u ze niet opslaat.",
        'dlg_dont_save': "Niet opslaan",
        'dlg_cancel': "Annuleren",
        'dlg_save': "Opslaan…",

        'status_words_one': "woord",
        'status_words_many': "woorden",
        'status_untitled': "Naamloos",

        'search_no_results': "Geen resultaten",
        'sidebar_explorer': "VERKENNER",
        'no_folder': "Geen map geopend",

        'dnd_title': "Drag & Drop niet beschikbaar",
        'dnd_msg': (
            "Drag & drop is niet beschikbaar:\n"
            "tkinterdnd2 is niet gevonden.\n\n"
            "Installeer het met:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Start Notys daarna opnieuw."
        ),

        'untitled': "Naamloos",
    },
    'ru': {  # [Russian translations dictionary]
        'menu_file': "Файл",
        'menu_new_window': "Новое окно",
        'menu_new_tab': "Новая вкладка",
        'menu_reopen_tab': "Переоткрыть закрытую вкладку",
        'menu_open': "Открыть…",
        'menu_open_folder': "Открыть папку…",
        'menu_open_recents': "Открыть недавние",
        'menu_close_tab': "Закрыть вкладку",
        'menu_toggle_pin': "Закрепить / открепить вкладку",
        'menu_save': "Сохранить",
        'menu_save_all': "Сохранить все",
        'menu_save_as': "Сохранить как…",

        'menu_edit': "Правка",
        'menu_undo': "Отменить",
        'menu_redo': "Повторить",
        'menu_cut': "Вырезать",
        'menu_copy': "Копировать",
        'menu_paste': "Вставить",
        'menu_find': "Найти…",

        'menu_window': "Окно",
        'menu_minimize': "Свернуть",

        'menu_settings': "Настройки",
        'menu_open_settings': "Открыть настройки…",
        'menu_about': "О программе",

        'settings_title': "Настройки",
        'settings_apply': "Применить",
        'settings_cancel': "Отмена",

        'section_language': "Язык",
        'section_general': "Общее",
        'section_appearance': "Внешний вид",
        'section_editor': "Редактор",
        'section_interface': "Интерфейс",
        'section_styles': "Стили",

        'settings_language': "Язык интерфейса",
        'settings_theme': "Тема",
        'theme_dark': "Тёмная",
        'theme_light': "Светлая",
        'theme_system': "Система",

        'settings_font_family': "Шрифт",
        'settings_font_size': "Размер шрифта",
        'settings_line_height': "Высота строки",
        'settings_line_wrap': "Перенос строк",
        'wrap_word': "По словам",
        'wrap_char': "По символам",
        'wrap_none': "Нет",
        'settings_padding': "Боковые поля",

        'settings_show_status': "Строка состояния",
        'settings_show_wordcount': "Счетчик слов",
        'settings_win_size': "Размер окна по умолчанию",
        'on': "Вкл.",
        'off': "Выкл.",

        'dlg_save_title': "Сохранить {name}",
        'dlg_save_msg': 'Сохранить изменения\nв "{name}"?',
        'dlg_save_sub': "Изменения будут потеряны, если вы их не сохраните.",
        'dlg_dont_save': "Не сохранять",
        'dlg_cancel': "Отмена",
        'dlg_save': "Сохранить…",

        'status_words_one': "слово",
        'status_words_many': "слов",
        'status_untitled': "Без названия",

        'search_no_results': "Ничего не найдено",
        'sidebar_explorer': "ПАПКИ",
        'no_folder': "Папка не открыта",

        'dnd_title': "Перетаскивание недоступно",
        'dnd_msg': (
            "Перетаскивание недоступно:\n"
            "tkinterdnd2 не найден.\n\n"
            "Установите его командой:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Затем перезапустите Notys."
        ),

        'untitled': "Без названия",
    },
    'ja': {  # [Japanese translations dictionary]
        'menu_file': "ファイル",
        'menu_new_window': "新しいウィンドウ",
        'menu_new_tab': "新しいタブ",
        'menu_reopen_tab': "閉じたタブを再表示",
        'menu_open': "開く…",
        'menu_open_folder': "フォルダーを開く…",
        'menu_open_recents': "最近のファイル",
        'menu_close_tab': "タブを閉じる",
        'menu_toggle_pin': "タブの固定を切り替え",
        'menu_save': "保存",
        'menu_save_all': "すべて保存",
        'menu_save_as': "名前を付けて保存…",

        'menu_edit': "編集",
        'menu_undo': "元に戻す",
        'menu_redo': "やり直す",
        'menu_cut': "切り取り",
        'menu_copy': "コピー",
        'menu_paste': "貼り付け",
        'menu_find': "検索…",

        'menu_window': "ウィンドウ",
        'menu_minimize': "最小化",

        'menu_settings': "設定",
        'menu_open_settings': "設定を開く…",
        'menu_about': "情報",

        'settings_title': "設定",
        'settings_apply': "適用",
        'settings_cancel': "キャンセル",

        'section_language': "言語",
        'section_general': "一般",
        'section_appearance': "外観",
        'section_editor': "エディター",
        'section_interface': "インターフェイス",
        'section_styles': "スタイル",

        'settings_language': "インターフェイスの言語",
        'settings_theme': "テーマ",
        'theme_dark': "ダーク",
        'theme_light': "ライト",
        'theme_system': "システム",

        'settings_font_family': "フォント",
        'settings_font_size': "フォントサイズ",
        'settings_line_height': "行の高さ",
        'settings_line_wrap': "改行",
        'wrap_word': "単語ごと",
        'wrap_char': "文字ごと",
        'wrap_none': "なし",
        'settings_padding': "側面の余白",

        'settings_show_status': "ステータスバー",
        'settings_show_wordcount': "単語数",
        'settings_win_size': "デフォルトのウィンドウサイズ",
        'on': "オン",
        'off': "オフ",

        'dlg_save_title': "{name} を保存",
        'dlg_save_msg': '"{name}" への変更を\n保存しますか?',
        'dlg_save_sub': "保存しないと変更内容は失われます。",
        'dlg_dont_save': "保存しない",
        'dlg_cancel': "キャンセル",
        'dlg_save': "保存…",

        'status_words_one': "語",
        'status_words_many': "語",
        'status_untitled': "無題",

        'search_no_results': "結果がありません",
        'sidebar_explorer': "エクスプローラー",
        'no_folder': "開いているフォルダーはありません",

        'dnd_title': "ドラッグ＆ドロップは利用できません",
        'dnd_msg': (
            "ドラッグ＆ドロップは利用できません:\n"
            "tkinterdnd2 が見つかりませんでした。\n\n"
            "次のコマンドでインストールしてください:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "その後、Notys を再起動してください。"
        ),

        'untitled': "無題",
    },
    'zh': {  # [Chinese translations dictionary]
        'menu_file': "文件",
        'menu_new_window': "新窗口",
        'menu_new_tab': "新标签页",
        'menu_reopen_tab': "重新打开关闭的标签页",
        'menu_open': "打开…",
        'menu_open_folder': "打开文件夹…",
        'menu_open_recents': "打开最近文件",
        'menu_close_tab': "关闭标签页",
        'menu_toggle_pin': "固定 / 取消固定标签页",
        'menu_save': "保存",
        'menu_save_all': "全部保存",
        'menu_save_as': "另存为…",

        'menu_edit': "编辑",
        'menu_undo': "撤销",
        'menu_redo': "重做",
        'menu_cut': "剪切",
        'menu_copy': "复制",
        'menu_paste': "粘贴",
        'menu_find': "查找…",

        'menu_window': "窗口",
        'menu_minimize': "最小化",

        'menu_settings': "设置",
        'menu_open_settings': "打开设置…",
        'menu_about': "关于",

        'settings_title': "设置",
        'settings_apply': "应用",
        'settings_cancel': "取消",

        'section_language': "语言",
        'section_general': "常规",
        'section_appearance': "外观",
        'section_editor': "编辑器",
        'section_interface': "界面",
        'section_styles': "样式",

        'settings_language': "界面语言",
        'settings_theme': "主题",
        'theme_dark': "深色",
        'theme_light': "浅色",
        'theme_system': "系统",

        'settings_font_family': "字体",
        'settings_font_size': "字号",
        'settings_line_height': "行高",
        'settings_line_wrap': "自动换行",
        'wrap_word': "按词",
        'wrap_char': "按字符",
        'wrap_none': "无",
        'settings_padding': "侧边距",

        'settings_show_status': "状态栏",
        'settings_show_wordcount': "字数统计",
        'settings_win_size': "默认窗口大小",
        'on': "开启",
        'off': "关闭",

        'dlg_save_title': "保存 {name}",
        'dlg_save_msg': '是否保存对 "{name}" 的更改？',
        'dlg_save_sub': "如果不保存，您的更改将会丢失。",
        'dlg_dont_save': "不保存",
        'dlg_cancel': "取消",
        'dlg_save': "保存…",

        'status_words_one': "字",
        'status_words_many': "字",
        'status_untitled': "无标题",

        'search_no_results': "没有结果",
        'sidebar_explorer': "资源管理器",
        'no_folder': "没有打开的文件夹",

        'dnd_title': "拖放不可用",
        'dnd_msg': (
            "拖放功能不可用：\n"
            "未找到 tkinterdnd2。\n\n"
            "请使用：\n"
            "  python -m pip install tkinterdnd2\n\n"
            "然后重新启动 Notys。"
        ),

        'untitled': "无标题",
    },
    'ko': {  # [Korean translations dictionary]
        'menu_file': "파일",
        'menu_new_window': "새 창",
        'menu_new_tab': "새 탭",
        'menu_reopen_tab': "닫은 탭 다시 열기",
        'menu_open': "열기…",
        'menu_open_folder': "폴더 열기…",
        'menu_open_recents': "최근 항목 열기",
        'menu_close_tab': "탭 닫기",
        'menu_toggle_pin': "탭 고정/고정 해제",
        'menu_save': "저장",
        'menu_save_all': "모두 저장",
        'menu_save_as': "다른 이름으로 저장…",

        'menu_edit': "편집",
        'menu_undo': "실행 취소",
        'menu_redo': "다시 실행",
        'menu_cut': "잘라내기",
        'menu_copy': "복사",
        'menu_paste': "붙여넣기",
        'menu_find': "찾기…",

        'menu_window': "창",
        'menu_minimize': "최소화",

        'menu_settings': "설정",
        'menu_open_settings': "설정 열기…",
        'menu_about': "정보",

        'settings_title': "설정",
        'settings_apply': "적용",
        'settings_cancel': "취소",

        'section_language': "언어",
        'section_general': "일반",
        'section_appearance': "모양",
        'section_editor': "편집기",
        'section_interface': "인터페이스",
        'section_styles': "스타일",

        'settings_language': "인터페이스 언어",
        'settings_theme': "테마",
        'theme_dark': "어두움",
        'theme_light': "밝음",
        'theme_system': "시스템",

        'settings_font_family': "글꼴",
        'settings_font_size': "글자 크기",
        'settings_line_height': "줄 간격",
        'settings_line_wrap': "줄 바꿈",
        'wrap_word': "단어 단위",
        'wrap_char': "문자 단위",
        'wrap_none': "없음",
        'settings_padding': "측면 여백",

        'settings_show_status': "상태 표시줄",
        'settings_show_wordcount': "단어 수",
        'settings_win_size': "기본 창 크기",
        'on': "켜짐",
        'off': "꺼짐",

        'dlg_save_title': "{name} 저장",
        'dlg_save_msg': '"{name}"에 대한\n변경 사항을 저장하시겠습니까?',
        'dlg_save_sub': "저장하지 않으면 변경 사항이 사라집니다.",
        'dlg_dont_save': "저장하지 않음",
        'dlg_cancel': "취소",
        'dlg_save': "저장…",

        'status_words_one': "단어",
        'status_words_many': "단어",
        'status_untitled': "제목 없음",

        'search_no_results': "결과 없음",
        'sidebar_explorer': "탐색기",
        'no_folder': "열린 폴더가 없습니다",

        'dnd_title': "끌어다 놓기 사용 불가",
        'dnd_msg': (
            "끌어다 놓기를 사용할 수 없습니다:\n"
            "tkinterdnd2를 찾을 수 없습니다.\n\n"
            "다음 명령으로 설치하세요:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "그다음 Notys를 다시 시작하세요."
        ),

        'untitled': "제목 없음",
    },
}

STYLE_TRANSLATIONS = {
    'en': {
        'style_default': 'Default', 'style_custom': 'Custom',
        'style_element': 'Element', 'style_marker': 'Marker', 'style_color': 'Color', 'style_size': 'Size',
        'style_save': 'Save', 'style_reset': 'Reset', 'style_add': 'Add', 'style_delete': 'Delete',
        'style_title': 'Styles', 'style_new_name': 'New style name:',
        'style_confirm_delete': 'Delete "{name}"?',
        'style_confirm_reset': 'Reset "{name}" to default values?',
        'style_invalid_marker': '{element}: marker must contain 1 to 12 characters.',
        'style_invalid_color': '{element}: color must be a six-digit HEX value.',
        'style_invalid_size': '{element}: font size must be between 0 and 72.',
        'style_error_invalid_name': 'Style names must be 1-40 letters, numbers, spaces, _ or -.',
        'style_error_read_only': 'The default style is read-only.',
        'style_error_not_found': 'No style named "{name}" exists.',
        'style_error_choose_name': 'Choose a name other than Default.',
        'style_error_exists': 'A style named "{name}" already exists.',
        'style_error_default_reset': 'The default style cannot be reset.',
        'style_error_profile_missing': 'That style profile does not exist.',
        'style_text': 'Text', 'style_h1': 'Header 1', 'style_h2': 'Header 2',
        'style_h3': 'Header 3', 'style_h4': 'Header 4', 'style_h5': 'Header 5', 'style_h6': 'Header 6',
        'style_bold': 'Bold', 'style_italic': 'Italic', 'style_inline_code': 'Inline Code',
        'style_code_block': 'Code Block', 'style_quote': 'Blockquote', 'style_link': 'Link',
        'style_list': 'Bullet List', 'style_underline': 'Underline',
        'style_strike': 'Strikethrough', 'style_hr': 'Horizontal Rule',
    },
    'fr': {
        'style_default': 'Par défaut', 'style_custom': 'Personnalisé',
        'style_element': 'Élément', 'style_marker': 'Marqueur', 'style_color': 'Couleur', 'style_size': 'Taille',
        'style_save': 'Enregistrer', 'style_reset': 'Réinitialiser', 'style_add': 'Ajouter', 'style_delete': 'Supprimer',
        'style_title': 'Styles', 'style_new_name': 'Nom du nouveau style :',
        'style_confirm_delete': 'Supprimer « {name} » ?',
        'style_confirm_reset': 'Rétablir les valeurs par défaut de « {name} » ?',
        'style_invalid_marker': '{element} : le marqueur doit contenir de 1 à 12 caractères.',
        'style_invalid_color': '{element} : la couleur doit être au format HEX à six chiffres.',
        'style_invalid_size': '{element} : la taille doit être comprise entre 0 et 72.',
        'style_error_invalid_name': 'Le nom doit contenir de 1 à 40 lettres, chiffres, espaces, _ ou -.',
        'style_error_read_only': 'Le style par défaut est en lecture seule.',
        'style_error_not_found': 'Aucun style nommé « {name} » n’existe.',
        'style_error_choose_name': 'Choisissez un nom différent de « Par défaut ».',
        'style_error_exists': 'Un style nommé « {name} » existe déjà.',
        'style_error_default_reset': 'Le style par défaut ne peut pas être réinitialisé.',
        'style_error_profile_missing': 'Ce profil de style n’existe pas.',
        'style_text': 'Texte', 'style_h1': 'Titre 1', 'style_h2': 'Titre 2', 'style_h3': 'Titre 3',
        'style_h4': 'Titre 4', 'style_h5': 'Titre 5', 'style_h6': 'Titre 6', 'style_bold': 'Gras',
        'style_italic': 'Italique', 'style_inline_code': 'Code en ligne', 'style_code_block': 'Bloc de code',
        'style_quote': 'Citation', 'style_link': 'Lien', 'style_list': 'Liste à puces',
        'style_underline': 'Souligné', 'style_strike': 'Barré', 'style_hr': 'Séparateur horizontal',
    },
    'eo': {
        'style_default': 'Defaŭlta', 'style_custom': 'Propra',
        'style_element': 'Elemento', 'style_marker': 'Markilo', 'style_color': 'Koloro', 'style_size': 'Grandeco',
        'style_save': 'Konservi', 'style_reset': 'Restarigi', 'style_add': 'Aldoni', 'style_delete': 'Forigi',
        'style_title': 'Stiloj', 'style_new_name': 'Nomo de la nova stilo:',
        'style_confirm_delete': 'Ĉu forigi "{name}"?',
        'style_confirm_reset': 'Ĉu restarigi "{name}" al defaŭltaj valoroj?',
        'style_invalid_marker': '{element}: markilo devas havi 1 ĝis 12 signojn.',
        'style_invalid_color': '{element}: koloro devas esti ses-cifera HEX-valoro.',
        'style_invalid_size': '{element}: tipara grandeco devas esti inter 0 kaj 72.',
        'style_error_invalid_name': 'La nomo devas havi 1–40 literojn, ciferojn, spacojn, _ aŭ -.',
        'style_error_read_only': 'La defaŭlta stilo estas nurlegebla.',
        'style_error_not_found': 'Stilo nomata "{name}" ne ekzistas.',
        'style_error_choose_name': 'Elektu nomon alian ol Defaŭlta.',
        'style_error_exists': 'Stilo nomata "{name}" jam ekzistas.',
        'style_error_default_reset': 'La defaŭlta stilo ne povas esti restarigita.',
        'style_error_profile_missing': 'Tiu stila profilo ne ekzistas.',
        'style_text': 'Teksto', 'style_h1': 'Titolo 1', 'style_h2': 'Titolo 2', 'style_h3': 'Titolo 3',
        'style_h4': 'Titolo 4', 'style_h5': 'Titolo 5', 'style_h6': 'Titolo 6', 'style_bold': 'Grasa',
        'style_italic': 'Kursiva', 'style_inline_code': 'Enlinia kodo', 'style_code_block': 'Kodbloko',
        'style_quote': 'Citaĵo', 'style_link': 'Ligilo', 'style_list': 'Bul-listo',
        'style_underline': 'Substrekita', 'style_strike': 'Trastrekita', 'style_hr': 'Horizontala linio',
    },
    'es': {
        'style_default': 'Predeterminado', 'style_custom': 'Personalizado',
        'style_element': 'Elemento', 'style_marker': 'Marcador', 'style_color': 'Color', 'style_size': 'Tamaño',
        'style_save': 'Guardar', 'style_reset': 'Restablecer', 'style_add': 'Añadir', 'style_delete': 'Eliminar',
        'style_title': 'Estilos', 'style_new_name': 'Nombre del nuevo estilo:',
        'style_confirm_delete': '¿Eliminar "{name}"?',
        'style_confirm_reset': '¿Restablecer "{name}" a los valores predeterminados?',
        'style_invalid_marker': '{element}: el marcador debe tener entre 1 y 12 caracteres.',
        'style_invalid_color': '{element}: el color debe ser un valor HEX de seis dígitos.',
        'style_invalid_size': '{element}: el tamaño debe estar entre 0 y 72.',
        'style_error_invalid_name': 'El nombre debe tener entre 1 y 40 letras, números, espacios, _ o -.',
        'style_error_read_only': 'El estilo predeterminado es de solo lectura.',
        'style_error_not_found': 'No existe un estilo llamado "{name}".',
        'style_error_choose_name': 'Elige un nombre distinto de Predeterminado.',
        'style_error_exists': 'Ya existe un estilo llamado "{name}".',
        'style_error_default_reset': 'No se puede restablecer el estilo predeterminado.',
        'style_error_profile_missing': 'Ese perfil de estilo no existe.',
        'style_text': 'Texto', 'style_h1': 'Encabezado 1', 'style_h2': 'Encabezado 2',
        'style_h3': 'Encabezado 3', 'style_h4': 'Encabezado 4', 'style_h5': 'Encabezado 5', 'style_h6': 'Encabezado 6',
        'style_bold': 'Negrita', 'style_italic': 'Cursiva', 'style_inline_code': 'Código en línea',
        'style_code_block': 'Bloque de código', 'style_quote': 'Cita', 'style_link': 'Enlace',
        'style_list': 'Lista con viñetas', 'style_underline': 'Subrayado', 'style_strike': 'Tachado',
        'style_hr': 'Línea horizontal',
    },
    'pt': {
        'style_default': 'Padrão', 'style_custom': 'Personalizado',
        'style_element': 'Elemento', 'style_marker': 'Marcador', 'style_color': 'Cor', 'style_size': 'Tamanho',
        'style_save': 'Salvar', 'style_reset': 'Redefinir', 'style_add': 'Adicionar', 'style_delete': 'Excluir',
        'style_title': 'Estilos', 'style_new_name': 'Nome do novo estilo:',
        'style_confirm_delete': 'Excluir "{name}"?',
        'style_confirm_reset': 'Redefinir "{name}" para os valores padrão?',
        'style_invalid_marker': '{element}: o marcador deve conter de 1 a 12 caracteres.',
        'style_invalid_color': '{element}: a cor deve ser um valor HEX de seis dígitos.',
        'style_invalid_size': '{element}: o tamanho deve estar entre 0 e 72.',
        'style_error_invalid_name': 'O nome deve ter de 1 a 40 letras, números, espaços, _ ou -.',
        'style_error_read_only': 'O estilo padrão é somente leitura.',
        'style_error_not_found': 'Não existe um estilo chamado "{name}".',
        'style_error_choose_name': 'Escolha um nome diferente de Padrão.',
        'style_error_exists': 'Já existe um estilo chamado "{name}".',
        'style_error_default_reset': 'O estilo padrão não pode ser redefinido.',
        'style_error_profile_missing': 'Esse perfil de estilo não existe.',
        'style_text': 'Texto', 'style_h1': 'Cabeçalho 1', 'style_h2': 'Cabeçalho 2',
        'style_h3': 'Cabeçalho 3', 'style_h4': 'Cabeçalho 4', 'style_h5': 'Cabeçalho 5', 'style_h6': 'Cabeçalho 6',
        'style_bold': 'Negrito', 'style_italic': 'Itálico', 'style_inline_code': 'Código em linha',
        'style_code_block': 'Bloco de código', 'style_quote': 'Citação', 'style_link': 'Link',
        'style_list': 'Lista com marcadores', 'style_underline': 'Sublinhado', 'style_strike': 'Riscado',
        'style_hr': 'Linha horizontal',
    },
    'de': {
        'style_default': 'Standard', 'style_custom': 'Benutzerdefiniert',
        'style_element': 'Element', 'style_marker': 'Marker', 'style_color': 'Farbe', 'style_size': 'Größe',
        'style_save': 'Speichern', 'style_reset': 'Zurücksetzen', 'style_add': 'Hinzufügen', 'style_delete': 'Löschen',
        'style_title': 'Stile', 'style_new_name': 'Name des neuen Stils:',
        'style_confirm_delete': '„{name}" löschen?',
        'style_confirm_reset': '„{name}" auf Standardwerte zurücksetzen?',
        'style_invalid_marker': '{element}: Der Marker muss 1 bis 12 Zeichen enthalten.',
        'style_invalid_color': '{element}: Die Farbe muss ein sechsstelliger HEX-Wert sein.',
        'style_invalid_size': '{element}: Die Schriftgröße muss zwischen 0 und 72 liegen.',
        'style_error_invalid_name': 'Der Name muss 1 bis 40 Buchstaben, Zahlen, Leerzeichen, _ oder - enthalten.',
        'style_error_read_only': 'Der Standardstil ist schreibgeschützt.',
        'style_error_not_found': 'Der Stil „{name}" ist nicht vorhanden.',
        'style_error_choose_name': 'Wählen Sie einen anderen Namen als Standard.',
        'style_error_exists': 'Ein Stil namens „{name}" ist bereits vorhanden.',
        'style_error_default_reset': 'Der Standardstil kann nicht zurückgesetzt werden.',
        'style_error_profile_missing': 'Dieses Stilprofil ist nicht vorhanden.',
        'style_text': 'Text', 'style_h1': 'Überschrift 1', 'style_h2': 'Überschrift 2',
        'style_h3': 'Überschrift 3', 'style_h4': 'Überschrift 4', 'style_h5': 'Überschrift 5', 'style_h6': 'Überschrift 6',
        'style_bold': 'Fett', 'style_italic': 'Kursiv', 'style_inline_code': 'Inline-Code',
        'style_code_block': 'Codeblock', 'style_quote': 'Zitat', 'style_link': 'Link',
        'style_list': 'Aufzählung', 'style_underline': 'Unterstrichen', 'style_strike': 'Durchgestrichen',
        'style_hr': 'Horizontale Linie',
    },
    'it': {
        'style_default': 'Predefinito', 'style_custom': 'Personalizzato',
        'style_element': 'Elemento', 'style_marker': 'Marcatore', 'style_color': 'Colore', 'style_size': 'Dimensione',
        'style_save': 'Salva', 'style_reset': 'Reimposta', 'style_add': 'Aggiungi', 'style_delete': 'Elimina',
        'style_title': 'Stili', 'style_new_name': 'Nome del nuovo stile:',
        'style_confirm_delete': 'Eliminare "{name}"?',
        'style_confirm_reset': 'Ripristinare i valori predefiniti di "{name}"?',
        'style_invalid_marker': '{element}: il marcatore deve contenere da 1 a 12 caratteri.',
        'style_invalid_color': '{element}: il colore deve essere un valore HEX a sei cifre.',
        'style_invalid_size': '{element}: la dimensione deve essere compresa tra 0 e 72.',
        'style_error_invalid_name': 'Il nome deve contenere da 1 a 40 lettere, numeri, spazi, _ o -.',
        'style_error_read_only': 'Lo stile predefinito è di sola lettura.',
        'style_error_not_found': 'Non esiste uno stile chiamato "{name}".',
        'style_error_choose_name': 'Scegli un nome diverso da Predefinito.',
        'style_error_exists': 'Esiste già uno stile chiamato "{name}".',
        'style_error_default_reset': 'Lo stile predefinito non può essere reimpostato.',
        'style_error_profile_missing': 'Questo profilo di stile non esiste.',
        'style_text': 'Testo', 'style_h1': 'Intestazione 1', 'style_h2': 'Intestazione 2',
        'style_h3': 'Intestazione 3', 'style_h4': 'Intestazione 4', 'style_h5': 'Intestazione 5', 'style_h6': 'Intestazione 6',
        'style_bold': 'Grassetto', 'style_italic': 'Corsivo', 'style_inline_code': 'Codice in linea',
        'style_code_block': 'Blocco di codice', 'style_quote': 'Citazione', 'style_link': 'Collegamento',
        'style_list': 'Elenco puntato', 'style_underline': 'Sottolineato', 'style_strike': 'Barrato',
        'style_hr': 'Linea orizzontale',
    },
    'nl': {
        'style_default': 'Standaard', 'style_custom': 'Aangepast',
        'style_element': 'Element', 'style_marker': 'Markering', 'style_color': 'Kleur', 'style_size': 'Grootte',
        'style_save': 'Opslaan', 'style_reset': 'Herstellen', 'style_add': 'Toevoegen', 'style_delete': 'Verwijderen',
        'style_title': 'Stijlen', 'style_new_name': 'Naam van de nieuwe stijl:',
        'style_confirm_delete': '"{name}" verwijderen?',
        'style_confirm_reset': '"{name}" herstellen naar de standaardwaarden?',
        'style_invalid_marker': '{element}: de markering moet 1 tot 12 tekens bevatten.',
        'style_invalid_color': '{element}: de kleur moet een HEX-waarde van zes cijfers zijn.',
        'style_invalid_size': '{element}: de tekengrootte moet tussen 0 en 72 liggen.',
        'style_error_invalid_name': 'De naam moet 1 tot 40 letters, cijfers, spaties, _ of - bevatten.',
        'style_error_read_only': 'De standaardstijl is alleen-lezen.',
        'style_error_not_found': 'Er bestaat geen stijl met de naam "{name}".',
        'style_error_choose_name': 'Kies een andere naam dan Standaard.',
        'style_error_exists': 'Er bestaat al een stijl met de naam "{name}".',
        'style_error_default_reset': 'De standaardstijl kan niet worden hersteld.',
        'style_error_profile_missing': 'Dit stijlprofiel bestaat niet.',
        'style_text': 'Tekst', 'style_h1': 'Kop 1', 'style_h2': 'Kop 2', 'style_h3': 'Kop 3',
        'style_h4': 'Kop 4', 'style_h5': 'Kop 5', 'style_h6': 'Kop 6', 'style_bold': 'Vet',
        'style_italic': 'Cursief', 'style_inline_code': 'Inline-code', 'style_code_block': 'Codeblok',
        'style_quote': 'Citaat', 'style_link': 'Koppeling', 'style_list': 'Lijst met opsommingstekens',
        'style_underline': 'Onderstrepen', 'style_strike': 'Doorhalen', 'style_hr': 'Horizontale lijn',
    },
    'ru': {
        'style_default': 'По умолчанию', 'style_custom': 'Пользовательский',
        'style_element': 'Элемент', 'style_marker': 'Маркер', 'style_color': 'Цвет', 'style_size': 'Размер',
        'style_save': 'Сохранить', 'style_reset': 'Сбросить', 'style_add': 'Добавить', 'style_delete': 'Удалить',
        'style_title': 'Стили', 'style_new_name': 'Название нового стиля:',
        'style_confirm_delete': 'Удалить «{name}»?',
        'style_confirm_reset': 'Сбросить «{name}» к значениям по умолчанию?',
        'style_invalid_marker': '{element}: маркер должен содержать от 1 до 12 символов.',
        'style_invalid_color': '{element}: цвет должен быть шестизначным HEX-значением.',
        'style_invalid_size': '{element}: размер шрифта должен быть от 0 до 72.',
        'style_error_invalid_name': 'Имя должно содержать от 1 до 40 букв, цифр, пробелов, _ или -.',
        'style_error_read_only': 'Стиль по умолчанию доступен только для чтения.',
        'style_error_not_found': 'Стиль «{name}» не найден.',
        'style_error_choose_name': 'Выберите имя, отличное от «По умолчанию».',
        'style_error_exists': 'Стиль «{name}» уже существует.',
        'style_error_default_reset': 'Нельзя сбросить стиль по умолчанию.',
        'style_error_profile_missing': 'Этот профиль стиля не существует.',
        'style_text': 'Текст', 'style_h1': 'Заголовок 1', 'style_h2': 'Заголовок 2',
        'style_h3': 'Заголовок 3', 'style_h4': 'Заголовок 4', 'style_h5': 'Заголовок 5', 'style_h6': 'Заголовок 6',
        'style_bold': 'Полужирный', 'style_italic': 'Курсив', 'style_inline_code': 'Строчный код',
        'style_code_block': 'Блок кода', 'style_quote': 'Цитата', 'style_link': 'Ссылка',
        'style_list': 'Маркированный список', 'style_underline': 'Подчёркивание', 'style_strike': 'Зачёркивание',
        'style_hr': 'Горизонтальная линия',
    },
    'ja': {
        'style_default': 'デフォルト', 'style_custom': 'カスタム',
        'style_element': '要素', 'style_marker': '記号', 'style_color': '色', 'style_size': 'サイズ',
        'style_save': '保存', 'style_reset': 'リセット', 'style_add': '追加', 'style_delete': '削除',
        'style_title': 'スタイル', 'style_new_name': '新しいスタイル名:',
        'style_confirm_delete': '「{name}」を削除しますか？',
        'style_confirm_reset': '「{name}」をデフォルト値に戻しますか？',
        'style_invalid_marker': '{element}: 記号は1〜12文字で指定してください。',
        'style_invalid_color': '{element}: 色は6桁のHEX値で指定してください。',
        'style_invalid_size': '{element}: フォントサイズは0〜72で指定してください。',
        'style_error_invalid_name': '名前は1〜40文字で、英字、数字、空白、_、-を使用できます。',
        'style_error_read_only': 'デフォルトのスタイルは読み取り専用です。',
        'style_error_not_found': 'スタイル「{name}」が見つかりません。',
        'style_error_choose_name': 'デフォルト以外の名前を指定してください。',
        'style_error_exists': 'スタイル「{name}」はすでに存在します。',
        'style_error_default_reset': 'デフォルトのスタイルはリセットできません。',
        'style_error_profile_missing': 'スタイルプロファイルが見つかりません。',
        'style_text': 'テキスト', 'style_h1': '見出し 1', 'style_h2': '見出し 2',
        'style_h3': '見出し 3', 'style_h4': '見出し 4', 'style_h5': '見出し 5', 'style_h6': '見出し 6',
        'style_bold': '太字', 'style_italic': '斜体', 'style_inline_code': 'インラインコード',
        'style_code_block': 'コードブロック', 'style_quote': '引用', 'style_link': 'リンク',
        'style_list': '箇条書き', 'style_underline': '下線', 'style_strike': '取り消し線',
        'style_hr': '水平線',
    },
    'zh': {
        'style_default': '默认', 'style_custom': '自定义',
        'style_element': '元素', 'style_marker': '标记', 'style_color': '颜色', 'style_size': '大小',
        'style_save': '保存', 'style_reset': '重置', 'style_add': '添加', 'style_delete': '删除',
        'style_title': '样式', 'style_new_name': '新样式名称：',
        'style_confirm_delete': '确定删除“{name}”吗？',
        'style_confirm_reset': '确定将“{name}”重置为默认值吗？',
        'style_invalid_marker': '{element}：标记长度必须为 1 到 12 个字符。',
        'style_invalid_color': '{element}：颜色必须是六位 HEX 值。',
        'style_invalid_size': '{element}：字体大小必须在 0 到 72 之间。',
        'style_error_invalid_name': '名称须为 1 到 40 个字符，可包含字母、数字、空格、_ 或 -。',
        'style_error_read_only': '默认样式为只读。',
        'style_error_not_found': '找不到名为“{name}”的样式。',
        'style_error_choose_name': '请选择“默认”以外的名称。',
        'style_error_exists': '名为“{name}”的样式已存在。',
        'style_error_default_reset': '无法重置默认样式。',
        'style_error_profile_missing': '该样式配置不存在。',
        'style_text': '文本', 'style_h1': '标题 1', 'style_h2': '标题 2', 'style_h3': '标题 3',
        'style_h4': '标题 4', 'style_h5': '标题 5', 'style_h6': '标题 6', 'style_bold': '粗体',
        'style_italic': '斜体', 'style_inline_code': '行内代码', 'style_code_block': '代码块',
        'style_quote': '引用', 'style_link': '链接', 'style_list': '项目符号列表',
        'style_underline': '下划线', 'style_strike': '删除线', 'style_hr': '水平线',
    },
    'ko': {
        'style_default': '기본값', 'style_custom': '사용자 지정',
        'style_element': '요소', 'style_marker': '표시자', 'style_color': '색상', 'style_size': '크기',
        'style_save': '저장', 'style_reset': '초기화', 'style_add': '추가', 'style_delete': '삭제',
        'style_title': '스타일', 'style_new_name': '새 스타일 이름:',
        'style_confirm_delete': '"{name}"을(를) 삭제할까요?',
        'style_confirm_reset': '"{name}"을(를) 기본값으로 초기화할까요?',
        'style_invalid_marker': '{element}: 표시자는 1~12자로 입력해야 합니다.',
        'style_invalid_color': '{element}: 색상은 6자리 HEX 값이어야 합니다.',
        'style_invalid_size': '{element}: 글꼴 크기는 0~72 사이여야 합니다.',
        'style_error_invalid_name': '이름은 영문자, 숫자, 공백, _ 또는 -를 사용해 1~40자로 입력해야 합니다.',
        'style_error_read_only': '기본 스타일은 읽기 전용입니다.',
        'style_error_not_found': '"{name}" 스타일을 찾을 수 없습니다.',
        'style_error_choose_name': '기본값이 아닌 이름을 선택하세요.',
        'style_error_exists': '"{name}" 스타일이 이미 있습니다.',
        'style_error_default_reset': '기본 스타일은 초기화할 수 없습니다.',
        'style_error_profile_missing': '해당 스타일 프로필이 없습니다.',
        'style_text': '텍스트', 'style_h1': '제목 1', 'style_h2': '제목 2', 'style_h3': '제목 3',
        'style_h4': '제목 4', 'style_h5': '제목 5', 'style_h6': '제목 6', 'style_bold': '굵게',
        'style_italic': '기울임꼴', 'style_inline_code': '인라인 코드', 'style_code_block': '코드 블록',
        'style_quote': '인용', 'style_link': '링크', 'style_list': '글머리 기호 목록',
        'style_underline': '밑줄', 'style_strike': '취소선', 'style_hr': '가로줄',
    },
}
for language, translations in STYLE_TRANSLATIONS.items():
    TRANSLATIONS[language].update(translations)

current_language = 'en' # [Default initial language setting]
theme_preferences = 'system' # [Default theme preference setting]
ACTIVE_STYLE_NAME = 'default'

# ── Paramètres utilisateur ────────────────────────────────────────────────────
SETTINGS = { # [Default user configuration dictionary]
    'font_family': 'Consolas', # [Default editor font family]
    'font_size': 18, # [Default editor font size]
    'line_wrap': 'word', # [Default line wrapping mode]
    'padding': 40, # [Default text widget padding]
    'show_status': True, # [Show status bar by default]
    'show_wordcount': True, # [Show word count by default]
    'win_width': 900, # [Default window width]
    'win_height': 650, # [Default window height]
    'sidebar_collapsed': False, # [Remember sidebar collapse state]
    'sidebar_width': 220, # [Remember sidebar width]
}

def tr(key, **kwargs): # [Translation function with formatting support]
    """Retourne la chaîne traduite pour la langue courante."""
    text = TRANSLATIONS[current_language].get(key, TRANSLATIONS['en'].get(key, key)) # [Lookup translation or fallback]
    if kwargs: # [Format string if keyword arguments provided]
        text = text.format(**kwargs) # [Apply string formatting]
    return text # [Return translated string]

def get_config_dir(): # [Get platform-specific configuration directory path]
    """Retourne le dossier de configuration adapté à la plateforme, ex: ~/.config/Notys"""
    system = platform.system() # [Determine OS system]
    if system == 'Linux': # [Linux config path]
        base = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')) # [Get XDG config path]
    elif system == 'Windows': # [Windows config path]
        base = os.environ.get('APPDATA', os.path.expanduser('~')) # [Get APPDATA path]
    elif system == 'Darwin': # [macOS config path]
        base = os.path.expanduser('~/Library/Application Support') # [Get Application Support path]
    else: # [Fallback config path]
        base = os.path.expanduser('~/.config') # [Expand home config path]
    return os.path.join(base, 'Notys') # [Join with Notys folder name]

def settings_file_path(): # [Get path to settings.json]
    return os.path.join(get_config_dir(), 'settings.json') # [Return settings file path]

def recents_file_path(): # [Get path to recents_doc.json]
    return os.path.join(get_config_dir(), 'recents_doc.json') # [Return recents file path]

def pinned_docs_file_path():
    return os.path.join(get_config_dir(), 'pin_docs.json')

def load_pinned_docs():
    path = pinned_docs_file_path()
    if not os.path.isfile(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return list(dict.fromkeys(
                os.path.abspath(os.path.expanduser(item))
                for item in data if isinstance(item, str) and item
            ))
    except Exception as e:
        print(f"[Pins] Error reading {path}: {e}")
    return []

PINNED_DOCS = load_pinned_docs()

def save_pinned_docs():
    path = pinned_docs_file_path()
    try:
        os.makedirs(get_config_dir(), exist_ok=True)
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(PINNED_DOCS, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception as e:
        print(f"[Pins] Error saving {path}: {e}")

def load_recents_from_disk(): # [Load recent documents list from disk]
    """Loads up to 10 recent document entries from recents_doc.json."""
    path = recents_file_path() # [Get recents file path]
    if not os.path.isfile(path): # [Check if file exists]
        return [] # [Return empty list if not found]
    try: # [Try loading JSON data]
        with open(path, 'r', encoding='utf-8') as f: # [Open file for reading]
            data = json.load(f) # [Parse JSON content]
            if isinstance(data, list): # [Validate data is a list]
                return data # [Return recent files list]
    except Exception as e: # [Catch and print read errors]
        print(f"[Recents] Error reading {path}: {e}") # [Log error message]
    return [] # [Return empty list on failure]

def save_recents_to_disk(recents): # [Save recent documents list to disk atomically]
    """Saves recent document entries to recents_doc.json atomically."""
    path = recents_file_path() # [Get recents file path]
    try: # [Try writing JSON data]
        os.makedirs(get_config_dir(), exist_ok=True) # [Ensure config directory exists]
        tmp = path + '.tmp' # [Create temporary file path]
        with open(tmp, 'w', encoding='utf-8') as f: # [Open temp file for writing]
            json.dump(recents, f, indent=2, ensure_ascii=False) # [Dump JSON with formatting]
        os.replace(tmp, path) # [Atomic replace of old file]
    except Exception as e: # [Catch and print write errors]
        print(f"[Recents] Erreur en sauvegardant {path}: {e}") # [Log error message]

def save_settings_to_disk(): # [Save settings and preferences to disk]
    """Écrit SETTINGS + current_language + theme_preferences dans un fichier JSON atomique."""
    path = settings_file_path() # [Get settings file path]
    data = { # [Assemble settings dictionary]
        'settings': SETTINGS, # [Include settings]
        'current_language': current_language, # [Include language]
        'theme_preferences': theme_preferences, # [Include theme preference]
        'active_style': ACTIVE_STYLE_NAME,
    }
    try: # [Try saving settings file]
        os.makedirs(get_config_dir(), exist_ok=True) # [Ensure config directory exists]
        tmp = path + '.tmp' # [Temporary file path]
        with open(tmp, 'w', encoding='utf-8') as f: # [Open temp file]
            json.dump(data, f, indent=2, ensure_ascii=False) # [Serialize settings to JSON]
        os.replace(tmp, path) # [Replace target file atomically]
    except Exception as e: # [Catch write exceptions]
        print(f"[Settings] erreur en sauvegardant {path}: {e}") # [Log error]

def load_settings_from_disk(): # [Load settings from disk]
    """Loads settings, language, and theme preferences from settings.json."""
    global SETTINGS, current_language, current_theme, theme_preferences, ACTIVE_STYLE_NAME # [Declare global state variables]
    path = settings_file_path() # [Get settings path]
    if not os.path.isfile(path): # [Check if settings file exists]
        return
    try: # [Try parsing settings file]
        with open(path, 'r', encoding='utf-8') as f: # [Open settings file]
            data = json.load(f) # [Load JSON data]

        if isinstance(data, dict): # [Validate data format]
            s = data.get('settings') # [Extract settings subdict]
            if isinstance(s, dict): # [Validate settings dict]
                for k in SETTINGS: # [Iterate over default setting keys]
                    if k in s: # [Update setting if present]
                        SETTINGS[k] = s[k] # [Assign saved setting value]
            
            lang = data.get('current_language') # [Extract saved language]
            if isinstance(lang, str) and lang in TRANSLATIONS: # [Validate language]
                current_language = lang # [Update current language]

            pref = data.get('theme_preferences') # [Extract theme preference]
            if isinstance(pref, str) and pref in ['system', 'dark', 'light']: # [Validate preference]
                theme_preferences = pref # [Update theme preference]
                current_theme = resolve_theme(theme_preferences) # [Resolve active theme]

            active_style = data.get('active_style')
            if isinstance(active_style, str):
                ACTIVE_STYLE_NAME = active_style
    except Exception as e: # [Catch load errors]
        print(f"[Settings] Error reading {path}: {e}") # [Log error]

# ── Couleurs ──────────────────────────────────────────────────────────────────
THEMES = { # [Color themes dictionary for UI styling]
    'dark': { # [Dark theme color palette]
        'BG': "#1e1e1e", # [Background color]
        'FG': "#d4d4d4", # [Foreground text color]
        'CURSOR_CLR': "#ffffff", # [Cursor color]
        'SELECT_BG': "#264f78", # [Selection background color]
        'STATUS_BG': "#252526", # [Status bar background]
        'STATUS_FG': "#858585", # [Status bar foreground]
        'TAB_BG': "#2d2d2d", # [Inactive tab background]
        'TAB_ACTIVE': "#1e1e1e", # [Active tab background]
        'TAB_FG': "#858585", # [Inactive tab text color]
        'TAB_FG_ACT': "#ffffff", # [Active tab text color]
        'C_H1': "#39BBD8", 'C_H2': "#39BBD8", 'C_H3': "#39BBD8", 'C_H4': "#39BBD8", # [Heading colors]
        'C_CODE': "#DE7316", 'C_BOLD': "#ffffff", 'C_ITALIC': "#c8c8c8", # [Markdown formatting colors]
        'C_LIST': "#ffffff", 'C_QUOTE': "#6A9955", 'C_LINK': "#4ec9b0", 'C_HR': "#555555", # [List, quote, link, HR colors]
        'C_UNDERLINE': "#ffffff", 'C_STRIKE': "#c8c8c8" # [Underline and strike colors]
    },
    'light': { # [Light theme color palette]
        'BG': "#ffffff", # [Background color]
        'FG': "#000000", # [Foreground text color]
        'CURSOR_CLR': "#000000", # [Cursor color]
        'SELECT_BG': "#add8e6", # [Selection background color]
        'STATUS_BG': "#f0f0f0", # [Status bar background]
        'STATUS_FG': "#666666", # [Status bar foreground]
        'TAB_BG': "#e0e0e0", # [Inactive tab background]
        'TAB_ACTIVE': "#ffffff", # [Active tab background]
        'TAB_FG': "#666666", # [Inactive tab text color]
        'TAB_FG_ACT': "#000000", # [Active tab text color]
        'C_H1': "#1e90ff", 'C_H2': "#1e90ff", 'C_H3': "#1e90ff", 'C_H4': "#1e90ff", # [Heading colors]
        'C_CODE': "#ff4500", 'C_BOLD': "#000000", 'C_ITALIC': "#666666", # [Markdown formatting colors]
        'C_LIST': "#ffffff", 'C_QUOTE': "#228b22", 'C_LINK': "#006400", 'C_HR': "#cccccc", # [List, quote, link, HR colors]
        'C_UNDERLINE': "#000000", 'C_STRIKE': "#666666" # [Underline and strike colors]
    }
}

def resolve_theme(pref): # [Resolve theme preference string to actual theme name]
    if pref == 'system': # [Check if preference is system]
        return get_system_theme() # [Get OS system theme]
    return pref if pref in THEMES else 'dark' # [Return valid theme or fallback to dark]

load_settings_from_disk() # [Load settings on startup]
current_theme = resolve_theme(theme_preferences) # [Set active theme based on preferences]
style_manager = StyleManager(get_config_dir(), ACTIVE_STYLE_NAME)
ACTIVE_STYLE_NAME = style_manager.active_name
ACTIVE_STYLE = style_manager.profile

def get_color(key): # [Helper function to get color value from current theme]
    return THEMES[current_theme][key] # [Return color for key]

BG = get_color('BG') # [Global background color]
FG = get_color('FG') # [Global foreground color]
CURSOR_CLR = get_color('CURSOR_CLR') # [Global cursor color]
SELECT_BG = get_color('SELECT_BG') # [Global selection background]
STATUS_BG = get_color('STATUS_BG') # [Global status bar background]
STATUS_FG = get_color('STATUS_FG') # [Global status bar foreground]
TAB_BG = get_color('TAB_BG') # [Global tab bar background]
TAB_ACTIVE = get_color('TAB_ACTIVE') # [Global active tab background]
TAB_FG = get_color('TAB_FG') # [Global tab foreground]
TAB_FG_ACT = get_color('TAB_FG_ACT') # [Global active tab foreground]

C_H1 = get_color('C_H1'); C_H2 = get_color('C_H2'); C_H3 = get_color('C_H3'); C_H4 = get_color('C_H4') # [Heading highlight colors]
C_CODE = get_color('C_CODE'); C_BOLD = get_color('C_BOLD'); C_ITALIC = get_color('C_ITALIC') # [Inline syntax highlight colors]
C_LIST = get_color('C_LIST'); C_QUOTE = get_color('C_QUOTE'); C_LINK = get_color('C_LINK'); C_HR = get_color('C_HR') # [Block syntax highlight colors]
C_UNDERLINE = get_color('C_UNDERLINE'); C_STRIKE = get_color('C_STRIKE') # [Decoration highlight colors]

def update_font_definitions(): # [Update font tuples based on settings]
    global FONT_BODY, FONT_H1, FONT_H2, FONT_H3, FONT_H4, FONT_CODE, FONT_BOLD, FONT_ITALIC, FONT_TAB # [Declare global fonts]
    fam = SETTINGS['font_family'] # [Get font family from settings]
    sz = SETTINGS['font_size'] # [Get font size from settings]
    FONT_BODY = (fam, sz) # [Body text font tuple]
    FONT_H1 = (fam, int(sz * 1.8), 'bold') # [H1 font tuple]
    FONT_H2 = (fam, int(sz * 1.5), 'bold') # [H2 font tuple]
    FONT_H3 = (fam, int(sz * 1.3), 'bold') # [H3 font tuple]
    FONT_H4 = (fam, int(sz * 1.1), 'bold') # [H4 font tuple]
    FONT_CODE = ('Courier', max(8, sz - 1)) # [Code font tuple]
    FONT_BOLD = (fam, sz, 'bold') # [Bold font tuple]
    FONT_ITALIC = (fam, sz, 'italic') # [Italic font tuple]
    FONT_TAB = ('Arial', 14) # [Tab bar font tuple]

update_font_definitions() # [Initialize font definitions]

def apply_theme(theme_name): # [Apply theme changes dynamically across app]
    """Applies the given theme ('dark' or 'light') across all components."""
    global current_theme, BG, FG, CURSOR_CLR, SELECT_BG, STATUS_BG, STATUS_FG, TAB_BG, TAB_ACTIVE, TAB_FG, TAB_FG_ACT # [Declare color globals]
    global C_H1, C_H2, C_H3, C_H4, C_CODE, C_BOLD, C_ITALIC, C_LIST, C_QUOTE, C_LINK, C_HR, C_UNDERLINE, C_STRIKE # [Declare syntax color globals]

    if theme_name not in THEMES: # [Validate theme name]
        theme_name = 'dark' # [Default to dark if invalid]
    current_theme = theme_name # [Update current theme variable]

    BG = THEMES[current_theme]['BG'] # [Update BG]
    FG = THEMES[current_theme]['FG'] # [Update FG]
    CURSOR_CLR = THEMES[current_theme]['CURSOR_CLR'] # [Update cursor color]
    SELECT_BG = THEMES[current_theme]['SELECT_BG'] # [Update selection background]
    STATUS_BG = THEMES[current_theme]['STATUS_BG'] # [Update status bar BG]
    STATUS_FG = THEMES[current_theme]['STATUS_FG'] # [Update status bar FG]
    TAB_BG = THEMES[current_theme]['TAB_BG'] # [Update tab BG]
    TAB_ACTIVE = THEMES[current_theme]['TAB_ACTIVE'] # [Update active tab BG]
    TAB_FG = THEMES[current_theme]['TAB_FG'] # [Update tab FG]
    TAB_FG_ACT = THEMES[current_theme]['TAB_FG_ACT'] # [Update active tab FG]

    C_H1 = THEMES[current_theme]['C_H1'] # [Update H1 color]
    C_H2 = THEMES[current_theme]['C_H2'] # [Update H2 color]
    C_H3 = THEMES[current_theme]['C_H3'] # [Update H3 color]
    C_H4 = THEMES[current_theme]['C_H4'] # [Update H4 color]
    C_CODE = THEMES[current_theme]['C_CODE'] # [Update code color]
    C_BOLD = THEMES[current_theme]['C_BOLD'] # [Update bold color]
    C_ITALIC = THEMES[current_theme]['C_ITALIC'] # [Update italic color]
    C_LIST = THEMES[current_theme]['C_LIST'] # [Update list color]
    C_QUOTE = THEMES[current_theme]['C_QUOTE'] # [Update quote color]
    C_LINK = THEMES[current_theme]['C_LINK'] # [Update link color]
    C_HR = THEMES[current_theme]['C_HR'] # [Update HR color]
    C_UNDERLINE = THEMES[current_theme].get('C_UNDERLINE', FG) # [Update underline color]
    C_STRIKE = THEMES[current_theme].get('C_STRIKE', STATUS_FG) # [Update strike color]

    if 'win' in globals(): # [Reconfigure main window background]
        win.config(bg=BG)
    if 'main_work_area' in globals(): # [Reconfigure work area background]
        main_work_area.config(bg=BG)
    if 'editor_area' in globals(): # [Reconfigure editor area background]
        editor_area.config(bg=BG)
    if 'status_bar' in globals(): # [Reconfigure status bar and labels]
        status_bar.config(bg=STATUS_BG)
        status_file.config(bg=STATUS_BG, fg=STATUS_FG)
        status_pos.config(bg=STATUS_BG, fg=STATUS_FG)
        status_words.config(bg=STATUS_BG, fg=STATUS_FG)
    if 'menubar' in globals(): # [Reconfigure menubar colors]
        menubar.config(bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)

    if 'tab_bar' in globals(): # [Reconfigure tab bar and icons]
        tab_bar.update_theme()
        if hasattr(tab_bar, 'theme_button') and hasattr(tab_bar, 'dark_icon') and tab_bar.dark_icon:
            tab_bar.theme_button.config(image=tab_bar.dark_icon if current_theme == 'dark' else tab_bar.light_icon)
        for t in tab_bar.tabs:
            t.update_theme()

    if 'update_sidebar_theme' in globals(): # [Update sidebar theme styling]
        update_sidebar_theme()

    if 'search_bar' in globals(): # [Reconfigure search bar widgets]
        entry_bg = THEMES[current_theme]['TAB_BG'] if current_theme == 'dark' else THEMES[current_theme]['STATUS_BG']
        entry_border = "#555555" if current_theme == 'dark' else "#aaaaaa"
        search_bar.config(bg=STATUS_BG)
        search_entry.config(bg=entry_bg, fg=FG, insertbackground=FG,
                            highlightbackground=entry_border, highlightcolor=SELECT_BG)
        search_count.config(bg=STATUS_BG, fg=STATUS_FG)
        btn_prev.config(bg=STATUS_BG, fg=FG)
        btn_next.config(bg=STATUS_BG, fg=FG)
        btn_close_search.config(bg=STATUS_BG, fg=STATUS_FG)

    # fix dark mode title bar on windows
    if platform.system() == 'Windows':
        import ctypes
        try:
            win.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
            # DWMW_USE_IMMERSIVE_DARK_MODE is attribute 20
            is_dark = 1 if current_theme == 'dark' else 0
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(ctypes.c_int(is_dark)), ctypes.sizeof(ctypes.c_int)
            )
        except Exception:
            pass

def start_system_theme_watcher(root, interval_ms=1500): # [Watch for OS theme changes periodically]
    """Periodically checks if the OS theme has changed while set to 'system'."""
    if theme_preferences == 'system': # [Check if system theme preference is active]
        detected_theme = get_system_theme() # [Detect current OS theme]
        if detected_theme != current_theme: # [Check if theme changed]
            apply_theme(detected_theme) # [Apply new theme]
            
    # Schedule next check
    root.after(interval_ms, lambda: start_system_theme_watcher(root, interval_ms)) # [Reschedule watcher timer]

COLOR_NAMES = { # [Named color map for custom syntax highlighting]
    'red': '#ff5555', 'rouge': '#ff5555',
    'green': '#50fa7b', 'vert': '#50fa7b',
    'light_blue': '#8be9fd', 'bleu_clair': '#8be9fd',
    'blue': "#1E7BE4", 'bleu': '#1E7BE4',
    'dark_blue': "#091095", 'bleu_foncé': '#091095',
    'yellow': "#ebfb40", 'jaune': '#ebfb40',
    'orange': "#ffa03b",
    'pink': '#ff79c6', 'rose': '#ff79c6',
    'purple': "#8f41fc", 'violet': '#8f41fc',
    'white': '#ffffff', 'blanc': '#ffffff',
    'gray': '#858585', 'grey': '#858585', 'gris': '#858585',
    'cyan': '#8be9fd',
    'highlight_yellow': '#ffff00',
}

ALL_TAGS = ('body_style', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code', 'code_block', 'bold', 'italic', 'underline', 'strike', 'list', 'quote', 'link', 'hr') # [Tuple of all markdown text tags]

def _style_color(element):
    color = ACTIVE_STYLE['elements'][element]['color']
    if color.startswith('theme:'):
        return get_color(color[6:])
    return color

def apply_active_style():
    for tab in getattr(globals().get('tab_bar'), 'tabs', []):
        tab._configure_tags()
        tab.highlight_markdown()

def activate_style(name):
    global ACTIVE_STYLE_NAME, ACTIVE_STYLE
    ACTIVE_STYLE = style_manager.activate(name)
    ACTIVE_STYLE_NAME = style_manager.active_name
    save_settings_to_disk()
    apply_active_style()

def normalize_color(color): # [Normalize 8-digit hex colors to 6-digit]
    if isinstance(color, str) and color.startswith('#') and len(color) == 9:
        return color[:7]
    return color

def get_contrast_color(bg_hex): # [Calculate contrasting text color for backgrounds]
    bg_hex = normalize_color(bg_hex)
    if not re.match(r'^#[0-9a-fA-F]{6}$', bg_hex):
        return '#000000'
    r = int(bg_hex[1:3], 16)
    g = int(bg_hex[3:5], 16)
    b = int(bg_hex[5:7], 16)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return '#000000' if lum > 186 else '#ffffff'

def _next_tab(): # [Switch to next tab handler]
    if not tab_bar.tabs:
        return
    idx = (tab_bar.tabs.index(tab_bar.active) + 1) % len(tab_bar.tabs)
    tab_bar.select(tab_bar.tabs[idx])

def _prev_tab(): # [Switch to previous tab handler]
    if not tab_bar.tabs:
        return
    idx = (tab_bar.tabs.index(tab_bar.active) - 1) % len(tab_bar.tabs)
    tab_bar.select(tab_bar.tabs[idx])

# ── Fenêtre principale ────────────────────────────────────────────────────────
if __name__ == '__main__': # [Main application execution block]
    TkClass = DnDTk if DND_AVAILABLE else tk.Tk # [Select root window class with or without DND]
    win = TkClass() # [Instantiate main application window]

    if platform.system() == 'Windows':
        win.option_add('*Font', ('Segoe UI', 9))

    win.title("Notys") # [Set window title]
    win.configure(bg=BG) # [Configure window background]
    win.geometry(f"{SETTINGS['win_width']}x{SETTINGS['win_height']}") # [Set initial window dimensions]
    start_system_theme_watcher(win) # [Start theme watcher loop]

    # Set window / taskbar icon
    try: # [Try loading application icon]
        app_icon_path = resource_path("logo.png") # [Get icon resource path]
        icon_img = Image.open(app_icon_path) # [Open image with PIL]
        app_icon = ImageTk.PhotoImage(icon_img) # [Convert to PhotoImage]
        win.iconphoto(True, app_icon) # [Apply window icon]
    except Exception as e: # [Catch icon loading errors]
        print(f"Error loading window icon: {e}") # [Log icon error]

    # Menu bar initialisation
    menubar = tk.Menu(win, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG) # [Create main menubar]
    win.config(menu=menubar) # [Attach menubar to window]

    # ══════════════════════════════════════════════════════════════════════════════
    # Classe Tab
    # ══════════════════════════════════════════════════════════════════════════════
    class Tab: # [Individual tab editor class]
        _counter = 0 # [Tab ID counter]

        def __init__(self, file_path=None): # [Tab initialization method]
            Tab._counter += 1 # [Increment tab counter]
            self.id = Tab._counter # [Assign unique tab ID]
            self.file_path = file_path # [Store associated file path]
            self.highlight_job = None # [Syntax highlighting timer job]
            self._color_matches = [] # [Custom color matches list]
            self._syntax_matches = [] # [Syntax regex matches list]
            self.font_scale = 1.0 # [Font zoom scale factor]
            self.is_pinned = bool(file_path and os.path.abspath(file_path) in PINNED_DOCS)

            self.frame = tk.Frame(editor_area, bg=BG) # [Tab container frame]

            # Uniform custom scrollbar system for all operating systems
            self.sb = tk.Canvas(
                self.frame,
                width=12,
                bg=BG,
                highlightthickness=0,
                bd=0,
            )
            self.sb.pack(side='right', fill='y') # [Pack custom scrollbar canvas]

            self.scroll_thumb = self.sb.create_rectangle(
                2, 0, 10, 50,
                fill=TAB_BG,
                outline=TAB_BG,
            ) # [Create scrollbar thumb rectangle]

            self._scrollbar_drag_offset = 0 # [Drag offset tracker]
            self.sb.bind('<Button-1>', self._scrollbar_click) # [Bind scrollbar click]
            self.sb.bind('<B1-Motion>', self._scrollbar_drag) # [Bind scrollbar drag]

            self.text = tk.Text( # [Main text editor widget instance]
                self.frame,
                bg=BG, fg=FG,
                insertbackground=CURSOR_CLR,
                selectbackground=SELECT_BG,
                bd=0, highlightthickness=0, relief='flat',
                font=self._scaled_font(FONT_BODY),
                padx=SETTINGS['padding'], pady=30,
                spacing1=2, spacing3=4,
                wrap=SETTINGS['line_wrap'],
                undo=True,
                yscrollcommand=self._on_text_scroll,
            )
            self.text.pack(fill='both', expand=True) # [Pack text widget]

            self.text.tag_configure('hidden', foreground=BG, font=self._scaled_font(('Andale Mono', 1)), elide=True) # [Configure hidden tag for syntax masking]

            self._configure_tags() # [Configure syntax tags]
            self.text.bind('<KeyRelease>', self._on_key) # [Bind key release event]
            self.text.bind('<ButtonRelease-1>', self._on_cursor_move) # [Bind mouse click / cursor move]
            self.text.bind('<Button-1>', self._on_click_checkbox) # [Bind mouse click on checkbox]
            self.text.bind('<Tab>', self._handle_tab) # [Bind tab key handler]
            self.text.bind('<Return>', self._handle_enter) # [Bind enter key handler]
            # fix mouse sensitivity on scrollbars
            self.text.bind('<MouseWheel>', self._on_mousewheel)
            self.sb.bind('<MouseWheel>', self._on_mousewheel)

            if is_macos: # [macOS specific shortcuts]
                self.text.bind('<Command-BackSpace>', self._delete_line)
            else: # [Windows/Linux line delete shortcut]
                self.text.bind('<Alt-BackSpace>', self._delete_line)

            if is_macos: # [macOS word delete shortcut]
                self.text.bind('<Option-BackSpace>', self._delete_word_before)
            else: # [Windows/Linux word delete shortcut]
                self.text.bind('<Control-BackSpace>', self._delete_word_before)

            self.text.bind('<Control-Tab>', lambda e: _next_tab()) # [Ctrl+Tab next tab shortcut]
            self.text.bind('<Control-Shift-Tab>', lambda e: _prev_tab()) # [Ctrl+Shift+Tab prev tab shortcut]

        # function to fix the sensitivity on the scrollbar
        def _on_mousewheel(self, event):
            if platform.system() == 'Windows':
                # Map delta/120 (1 notch) to 3 units (lines) to match system sensitivity
                self.text.yview_scroll(int(-1 * (event.delta / 120) * 3), "units")
                return 'break'
        
        def update_theme(self): # [Update tab theme colors]
            self.frame.config(bg=BG)
            self.text.config(
                bg=BG,
                fg=FG,
                insertbackground=CURSOR_CLR,
                selectbackground=SELECT_BG,
            )

            self.sb.config(bg=BG)
            self.sb.itemconfig(
                self.scroll_thumb,
                fill=TAB_BG,
                outline=TAB_BG,
            )

            self._configure_tags() # [Re-configure syntax tags]
            self.highlight_markdown() # [Re-run markdown highlighting]

        def _configure_tags(self): # [Configure text tag styles]
            t = self.text
            base_fonts = {
                'text': FONT_BODY,
                'h1': FONT_H1, 'h2': FONT_H2, 'h3': FONT_H3, 'h4': FONT_H4,
                'h5': (SETTINGS['font_family'], SETTINGS['font_size'], 'bold'),
                'h6': (SETTINGS['font_family'], max(8, int(SETTINGS['font_size'] * 0.9)), 'bold'),
                'bold': FONT_BOLD, 'italic': FONT_ITALIC,
                'inline_code': FONT_CODE, 'code_block': FONT_CODE,
                'quote': ('Andale Mono', 12, 'italic'), 'link': FONT_BODY,
                'list': FONT_BODY, 'underline': FONT_BODY, 'strike': FONT_BODY,
                'hr': FONT_BODY,
            }
            tag_names = {'text': 'body_style', 'inline_code': 'code'}
            for key, base_font in base_fonts.items():
                style = ACTIVE_STYLE['elements'][key]
                font_size = style['font_size'] or base_font[1]
                font_flags = tuple(flag for flag, enabled in (
                    ('bold', style['bold']), ('italic', style['italic'])
                ) if enabled)
                font = self._scaled_font((base_font[0], font_size, *font_flags))
                color = _style_color(key)
                if key == 'text':
                    t.config(font=font, fg=color)
                t.tag_configure(
                    tag_names.get(key, key),
                    foreground=color,
                    font=font,
                    underline=style['underline'],
                    overstrike=style['strikethrough'],
                )
        def _handle_tab(self, event): # [Handle tab indentation]
            self.text.insert('insert', '    ')
            return 'break'

        def _handle_enter(self, event): # [Handle enter key, checkbox & list bullet auto-continuation]
            insert = self.text.index('insert')
            line_start = f"{insert} linestart"
            line_text = self.text.get(line_start, insert)
            
            # Checkbox item continuation check
            chk_match = re.match(r'^(\s*[-*+•]\s+\[([ xX])\]\s*)(.*)', line_text)
            if chk_match:
                prefix, state, content = chk_match.groups()
                if not content.strip():
                    self.text.delete(line_start, insert)
                    return None
                indent = re.match(r'^\s*', line_text).group(0)
                self.text.insert('insert', f'\n{indent}• [ ] ')
                return 'break'

            # Unordered bullet list continuation check
            match = re.match(r'^(\s*[-*+•]\s+)', line_text)
            if match:
                marker = match.group(1)
                if line_text.strip() in ['-', '*', '+', '•']:
                    self.text.delete(line_start, insert)
                    return None
                indent = re.match(r'^\s*', line_text).group(0)
                self.text.insert('insert', f'\n{indent}• ')
                return 'break'

            # Numbered list continuation check
            num_match = re.match(r'^(\s*)(\d+)\.\s+', line_text)
            if num_match:
                indent, num = num_match.groups()
                if not line_text[len(num_match.group(0)):].strip():
                    self.text.delete(line_start, insert)
                    return None
                self.text.insert('insert', f'\n{indent}{int(num) + 1}. ')
                return 'break'

            return None

        def _on_click_checkbox(self, event): # [Handle mouse click on checkbox]
            click_index = self.text.index(f"@{event.x},{event.y}")
            line_num = click_index.split('.')[0]
            line_text = self.text.get(f"{line_num}.0", f"{line_num}.end")

            m = re.search(r'(\s*[-*+•]\s+\[)([ xX])(\])', line_text)
            if m:
                start_col = m.start()
                end_col = m.end()
                click_col = int(click_index.split('.')[1])

                if start_col <= click_col <= end_col:
                    curr_val = m.group(2)
                    new_val = 'x' if curr_val == ' ' else ' '
                    target_col_start = f"{line_num}.{m.start(2)}"
                    target_col_end = f"{line_num}.{m.end(2)}"
                    self.text.delete(target_col_start, target_col_end)
                    self.text.insert(target_col_start, new_val)
                    self.set_modified(True)
                    self.schedule_highlight()
                    return 'break'

        def _scaled_font(self, font_tuple): # [Calculate zoomed font tuple]
            if not isinstance(font_tuple, tuple) or len(font_tuple) < 2:
                return font_tuple
            name = font_tuple[0]
            size = font_tuple[1]
            rest = font_tuple[2:]
            scaled_size = max(2, int(round(size * self.font_scale)))
            return (name, scaled_size, *rest)

        def set_zoom(self, zoom): # [Set editor zoom level]
            self.font_scale = max(0.5, min(3.0, zoom))
            self.text.config(font=self._scaled_font(FONT_BODY))
            self._configure_tags()
            self.highlight_markdown()

        def _delete_line(self, event=None): # [Delete current line shortcut]
            insert = self.text.index('insert')
            line = insert.split('.')[0]
            self.text.delete(f'{line}.0', f'{line}.end+1c')
            return 'break'

        def _delete_word_before(self, event=None): # [Delete previous word shortcut]
            insert = self.text.index('insert')
            word_start = self.text.index(f'{insert} -1c wordstart')
            if self.text.compare(word_start, '<', insert):
                self.text.delete(word_start, insert)
            return 'break'

        def _on_key(self, event=None): # [Key press event handler]
            # Convert dash/star list creation to bullet dot on space
            if event and event.keysym in ['space', 'spacebar', 'KP_Space']:
                insert = self.text.index('insert')
                line_start = f"{insert} linestart"
                line_text = self.text.get(line_start, insert)
                m = re.match(r'^(\s*)([-*])\s$', line_text)
                if m:
                    indent = m.group(1)
                    self.text.delete(line_start, insert)
                    self.text.insert(line_start, f"{indent}• ")

            tab_bar.refresh()
            self.schedule_highlight()
            update_status()

        def _on_cursor_move(self, event=None): # [Cursor movement event handler]
            self._apply_symbol_visibility()

        def schedule_highlight(self): # [Debounce syntax highlighting]
            if self.highlight_job:
                win.after_cancel(self.highlight_job)
            self.highlight_job = win.after(16, self.highlight_markdown)

        def _on_text_scroll(self, first, last): # [Text scrolling event handler]
            try:
                first = float(first)
                last = float(last)
            except (TypeError, ValueError):
                return

            height = self.sb.winfo_height()
            if height <= 1:
                return

            visible_fraction = max(0.0, min(1.0, last - first))
            thumb_height = max(20, visible_fraction * height)
            thumb_height = min(height, thumb_height)

            max_top = height - thumb_height
            thumb_top = min(max_top, max(0, first * height))
            thumb_bottom = thumb_top + thumb_height

            self.sb.coords(
                self.scroll_thumb,
                2,
                thumb_top,
                10,
                thumb_bottom,
            )

        def _scrollbar_click(self, event): # [Custom scrollbar click handler]
            coords = self.sb.coords(self.scroll_thumb)
            if not coords:
                return

            thumb_top, thumb_bottom = coords[1], coords[3]

            if thumb_top <= event.y <= thumb_bottom:
                self._scrollbar_drag_offset = event.y - thumb_top
            else:
                height = self.sb.winfo_height()
                thumb_height = thumb_bottom - thumb_top
                max_top = max(1, height - thumb_height)

                new_top = event.y - thumb_height / 2
                fraction = new_top / max_top
                self.text.yview_moveto(max(0.0, min(1.0, fraction)))

        def _scrollbar_drag(self, event): # [Custom scrollbar drag handler]
            height = self.sb.winfo_height()
            if height <= 1:
                return

            coords = self.sb.coords(self.scroll_thumb)
            if not coords:
                return

            thumb_height = coords[3] - coords[1]
            max_top = max(1, height - thumb_height)

            new_top = event.y - self._scrollbar_drag_offset
            fraction = new_top / max_top

            self.text.yview_moveto(max(0.0, min(1.0, fraction)))

        # ── Coloration principale ─────────────────────────────────────────────────
        def highlight_markdown(self): # [Main markdown syntax highlighter method]
            t = self.text

            for tag in ALL_TAGS:
                t.tag_remove(tag, '1.0', 'end')
            t.tag_remove('hidden', '1.0', 'end')
            t.tag_remove('highlight', '1.0', 'end')

            for tag in t.tag_names():
                if tag.startswith('highlight_') or tag.startswith('clr_'):
                    t.tag_remove(tag, '1.0', 'end')

            self._color_matches = []
            self._syntax_matches = []
            t.tag_add('body_style', '1.0', 'end-1c')

            if not self.is_markdown:
                return

            t.tag_configure('highlight', background='#ffff00', foreground='#000000')

            content = t.get('1.0', 'end-1c')
            lines = content.splitlines()

            code_line_ranges = []
            in_block = False
            block_start = None
            code_marker = ACTIVE_STYLE['elements']['code_block']['marker']
            for i, line in enumerate(lines, start=1):
                if line.strip().startswith(code_marker):
                    if not in_block:
                        in_block = True
                        block_start = i
                    else:
                        code_line_ranges.append((block_start, i))
                        in_block = False
            if in_block and block_start:
                code_line_ranges.append((block_start, len(lines)))

            code_line_set = set()
            for s, e in code_line_ranges:
                for ln in range(s, e + 1):
                    code_line_set.add(ln)
                t.tag_add('code_block', f'{s}.0', f'{e}.end')

            line_offsets = []
            off = 0
            for line in lines:
                line_offsets.append(off)
                off += len(line) + 1

            for i, line in enumerate(lines, start=1):
                if i in code_line_set:
                    continue
                ls, le = f'{i}.0', f'{i}.end'
                hm = None
                heading_level = None
                for level in range(6, 0, -1):
                    marker = ACTIVE_STYLE['elements'][f'h{level}']['marker']
                    candidate = re.match(r'^(\s*' + re.escape(marker) + r'\s*)', line)
                    if candidate:
                        hm = candidate
                        heading_level = level
                        break
                if hm:
                    prefix_len = len(hm.group(1))
                    t.tag_add(f'h{heading_level}', ls, le)

                    # Store heading symbols for disappearing when cursor is off
                    line_start_off = line_offsets[i - 1]
                    self._syntax_matches.append({
                        'type': 'heading',
                        'line_num': i,
                        'full_start': line_start_off,
                        'full_end': line_start_off + len(line),
                        'prefix_span': (line_start_off, line_start_off + prefix_len),
                        'suffix_span': (line_start_off + len(line), line_start_off + len(line)),
                    })
                elif re.match(r'^\s*' + re.escape(ACTIVE_STYLE['elements']['quote']['marker']) + r'\s', line):
                    t.tag_add('quote', ls, le)
                elif re.fullmatch(r'\s*(?:' + re.escape(ACTIVE_STYLE['elements']['hr']['marker']) + r')+\s*', line):
                    t.tag_add('hr', ls, le)
                elif re.match(r'^\s*' + (r'[-*+•]' if ACTIVE_STYLE['elements']['list']['marker'] == '•' else re.escape(ACTIVE_STYLE['elements']['list']['marker'])) + r'\s', line):
                    t.tag_add('list', ls, le)
                elif re.match(r'^\s*\d+\.\s', line):
                    t.tag_add('list', ls, le)

            def in_code_block(cs, ce):
                for s, e in code_line_ranges:
                    bs = line_offsets[s - 1]
                    be = line_offsets[e - 1] + len(lines[e - 1])
                    if cs >= bs and ce <= be:
                        return True
                return False

            # code
            inline_marker = re.escape(ACTIVE_STYLE['elements']['inline_code']['marker'])
            for m in re.finditer(inline_marker + r'([^\n]+?)' + inline_marker, content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('code', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')

            # bold                    
            bold_marker = re.escape(ACTIVE_STYLE['elements']['bold']['marker'])
            for m in re.finditer(r'(?<!' + bold_marker + r')' + bold_marker + r'(.+?)' + bold_marker + r'(?!' + bold_marker + r')', content, re.DOTALL):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('bold', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            # italic
            italic_marker = re.escape(ACTIVE_STYLE['elements']['italic']['marker'])
            for m in re.finditer(r'(?<!' + italic_marker + r')' + italic_marker + r'([^\n]+?)' + italic_marker + r'(?!' + italic_marker + r')', content):
                grp = m.group(1)
                si = m.start() + m.group(0).index(grp)
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('italic', f'1.0+{si}c', f'1.0+{si + len(grp)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), si),
                        'suffix_span': (si + len(grp), m.end()),
                    })

            # underline
            underline_trigger = ACTIVE_STYLE['elements']['underline']['marker']
            underline_marker = re.escape(underline_trigger)
            underline_end_marker = r':-' if underline_trigger == '-:' else underline_marker
            for m in re.finditer(underline_marker + r'(.+?)' + underline_end_marker, content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('underline', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            # strikethrough
            strike_marker = re.escape(ACTIVE_STYLE['elements']['strike']['marker'])
            for m in re.finditer(strike_marker + r'(.+?)' + strike_marker, content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('strike', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            # link
            link_marker = re.escape(ACTIVE_STYLE['elements']['link']['marker'])
            for m in re.finditer(link_marker + r'([^\]]+)\]\(([^)]+)\)', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('link', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            # ── &^couleur texte^& ─────────────────────────────────────────────────
            for tag in t.tag_names():
                if tag.startswith('clr_'):
                    t.tag_remove(tag, '1.0', 'end')

            for m in re.finditer(r'&\^(\w+)\s(.*?)\^&', content, re.DOTALL):
                color_name = m.group(1).lower()
                color_hex = COLOR_NAMES.get(color_name, None)
                if not color_hex:
                    if re.match(r'^#[0-9a-fA-F]{6}$', color_name):
                        color_hex = color_name
                    else:
                        continue

                tag_name = f'clr_{color_name}_{self.id}'
                t.tag_configure(tag_name, foreground=color_hex, font=self._scaled_font(FONT_BODY))

                text_start = m.start(2)
                text_end = m.end(2)

                t.tag_add(tag_name, f'1.0+{text_start}c', f'1.0+{text_end}c')

                full_start = m.start()
                color_end = m.start(2)
                suffix_end = m.end()

                self._color_matches.append({
                    'full_start': full_start,
                    'full_end': suffix_end,
                    'prefix_span': (full_start, color_end),
                    'suffix_span': (text_end, suffix_end),
                    'text_start': text_start,
                    'text_end': text_end,
                })

            # highligh
            for m in re.finditer(r'==([^:]+?)(?::(.+?))?==', content):
                if not in_code_block(m.start(), m.end()):
                    color_name = m.group(1).lower()
                    color_hex = COLOR_NAMES.get(color_name, COLOR_NAMES.get('yellow', '#ffff00'))

                    if m.group(2):
                        text_start = m.start(2)
                        text_end = m.end(2)
                        prefix_end = m.start(2)
                        suffix_start = m.end(2)
                    else:
                        text_start = m.start(1)
                        text_end = m.end(1)
                        prefix_end = m.start(1)
                        suffix_start = m.end(1)

                    tag_name = f'highlight_{color_name}_{self.id}'
                    t.tag_configure(tag_name, background='#ffff00', foreground='#000000')
                    t.tag_add(tag_name, f'1.0+{text_start}c', f'1.0+{text_end}c')

                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), prefix_end),
                        'suffix_span': (suffix_start, m.end()),
                    })

            self._apply_symbol_visibility()

        def _apply_symbol_visibility(self): # [Toggle markdown symbol hiding on cursor move]
            t = self.text
            t.tag_remove('hidden', '1.0', 'end')

            try:
                cursor_idx = t.index('insert')
            except tk.TclError:
                return

            cursor_line, cursor_col = map(int, cursor_idx.split('.'))
            content = t.get('1.0', 'end-1c')
            lines = content.splitlines(keepends=True)
            cursor_offset = sum(len(l) for l in lines[:cursor_line - 1]) + cursor_col

            for match in self._color_matches + getattr(self, '_syntax_matches', []):
                full_start = match['full_start']
                full_end = match['full_end']

                # Heading symbol visibility handling
                if match.get('type') == 'heading':
                    if cursor_line != match['line_num']:
                        ps, pe = match['prefix_span']
                        t.tag_add('hidden', f'1.0+{ps}c', f'1.0+{pe}c')
                    continue

                cursor_inside = full_start <= cursor_offset <= full_end

                if not cursor_inside:
                    ps, pe = match['prefix_span']
                    ss, se = match['suffix_span']
                    t.tag_add('hidden', f'1.0+{ps}c', f'1.0+{pe}c')
                    t.tag_add('hidden', f'1.0+{ss}c', f'1.0+{se}c')

        @property
        def name(self): # [Tab file name property]
            return os.path.basename(self.file_path) if self.file_path else tr('untitled')

        @property
        def is_modified(self): # [Check if tab has unsaved changes]
            return self.text.edit_modified()

        @property
        def is_markdown(self): # [Check if file is markdown]
            return (
                self.file_path is None
                or os.path.splitext(self.file_path)[1].lower() == '.md'
                or os.path.splitext(self.file_path)[1].lower() == '.markdown'
                or os.path.splitext(self.file_path)[1].lower() == '.mdown'
            )

        @property
        def label(self): # [Tab label string with modified indicator]
            return self.name + (" ●" if self.is_modified else "")

        def set_modified(self, val): # [Set modified state]
            self.text.edit_modified(val)
            tab_bar.refresh()

        def get_content(self): # [Get editor text content]
            return self.text.get('1.0', 'end-1c')

        def set_content(self, content): # [Set editor text content]
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', content)
            self.text.edit_modified(False)
            self.highlight_markdown()

        def show(self): # [Display tab frame]
            self.frame.pack(fill='both', expand=True)
            self.text.focus_set()

        def hide(self): # [Hide tab frame]
            self.frame.pack_forget()

    # ══════════════════════════════════════════════════════════════════════════════
    # Classe TabBar
    # ══════════════════════════════════════════════════════════════════════════════
    class TabBar: # [Tab bar manager class]
        def __init__(self, parent):
            self.frame = tk.Frame(parent, bg=TAB_BG, height=36)
            self.frame.pack(fill='x', side='top')
            self.frame.pack_propagate(False)

            self.tabs = []
            self.active = None
            self._btns = {}

            try:
                img_dark = Image.open(resource_path("assets/icons/dark.png"))
                img_dark = img_dark.resize((20, 20), Image.Resampling.LANCZOS)
                self.dark_icon = ImageTk.PhotoImage(img_dark, master=parent)

                img_light = Image.open(resource_path("assets/icons/light.png"))
                img_light = img_light.resize((20, 20), Image.Resampling.LANCZOS)
                self.light_icon = ImageTk.PhotoImage(img_light, master=parent)
            except Exception as e:
                print(f"Erreur chargement icônes : {e}")
                self.dark_icon = None
                self.light_icon = None

            self.btn_new = tk.Label(
                self.frame, text=" + ", bg=TAB_BG, fg=TAB_FG,
                font=FONT_TAB, cursor=HAND_CURSOR, padx=6
            )
            self.btn_new.pack(side='left', fill='y')
            self.btn_new.bind('<Button-1>', lambda e: new_tab())

            self.theme_button = tk.Label(
                self.frame, image=self.dark_icon, bg=TAB_BG, fg=TAB_FG,
                font=FONT_TAB, cursor=HAND_CURSOR, padx=6
            )
            self.theme_button.pack(side='right', fill='y')
            self.theme_button.bind('<Button-1>', self.toggle_theme)

        def reorder_tab_frames(self): # [Reorder tab widgets after drag]
            for tab in self.tabs:
                if tab.id in self._btns:
                    f = self._btns[tab.id][0]
                    f.pack_forget()
                    f.pack(side='left', fill='y', before=self.btn_new)

        def _on_tab_drag(self, event, tab): # [Handle tab drag and drop reordering]
            if len(self.tabs) < 2:
                return

            mouse_x = event.widget.winfo_rootx() + event.x - self.frame.winfo_rootx()
            curr_idx = self.tabs.index(tab)

            for i, other_tab in enumerate(self.tabs):
                if other_tab is tab or other_tab.id not in self._btns:
                    continue

                other_frame = self._btns[other_tab.id][0]
                left = other_frame.winfo_rootx() - self.frame.winfo_rootx()
                width = other_frame.winfo_width()

                if i < curr_idx and mouse_x < left + (width / 2):
                    self.tabs.remove(tab)
                    self.tabs.insert(i, tab)
                    self.reorder_tab_frames()
                    break
                elif i > curr_idx and mouse_x > left + (width / 2):
                    self.tabs.remove(tab)
                    self.tabs.insert(i, tab)
                    self.reorder_tab_frames()
                    break

        def toggle_theme(self, event=None): # [Toggle theme button handler]
            global theme_preferences
            themes = ['dark', 'light']
            current_index = themes.index(current_theme) if current_theme in themes else 0
            next_index = (current_index + 1) % len(themes)
            theme_preferences = themes[next_index]
            apply_theme(theme_preferences)
            save_settings_to_disk()

        def update_theme(self): # [Update tab bar theme]
            self.frame.config(bg=TAB_BG)
            self.btn_new.config(bg=TAB_BG, fg=TAB_FG)
            self.theme_button.config(bg=TAB_BG, fg=TAB_FG)
            self.refresh()

        def add(self, tab): # [Add new tab to bar]
            self.tabs.append(tab)
            self._make_btn(tab)
            self.select(tab)

        def toggle_pin(self, tab):
            if not tab.file_path:
                messagebox.showinfo('Pin Tab', 'Save this document before pinning it.')
                return 'break'
            path = os.path.abspath(tab.file_path)
            tab.is_pinned = not tab.is_pinned
            if tab.is_pinned and path not in PINNED_DOCS:
                PINNED_DOCS.append(path)
            elif not tab.is_pinned and path in PINNED_DOCS:
                PINNED_DOCS.remove(path)
            save_pinned_docs()
            self.refresh()
            return 'break'

        def _make_btn(self, tab): # [Create tab button widget with middle click close support]
            f = tk.Frame(self.frame, bg=TAB_BG)
            f.pack(side='left', fill='y', before=self.btn_new)

            border = tk.Frame(f, bg=TAB_BG, width=1)
            border.pack(side='left', fill='y')

            lbl = tk.Label(f, text=tab.label, bg=TAB_BG, fg=TAB_FG, font=FONT_TAB, padx=10, cursor=HAND_CURSOR)
            pin = tk.Label(f, text='📌', bg=TAB_BG, fg=STATUS_FG, font=('Arial', 10), padx=3, cursor=HAND_CURSOR)
            if tab.is_pinned:
                pin.pack(side='left', fill='y')
            lbl.pack(side='left', fill='y')

            close = tk.Label(f, text="✕", bg=TAB_BG, fg=TAB_FG, font=('Arial', 9), padx=6, cursor=HAND_CURSOR)
            close.pack(side='left', fill='y')

            lbl.bind('<Button-1>', lambda e, t=tab: self.select(t))
            lbl.bind('<B1-Motion>', lambda e, t=tab: self._on_tab_drag(e, t))
            pin.bind('<Button-1>', lambda e, t=tab: self.toggle_pin(t))

            # Middle-click closes the tab regardless of which tab sub-widget is hit.
            # Return 'break' so the event cannot trigger unrelated widget bindings.
            middle_close = lambda e, t=tab: (close_tab(t), 'break')[1]
            for widget in (f, border, lbl, pin, close):
                widget.bind('<Button-2>', middle_close)

            close.bind('<Button-1>', lambda e, t=tab: close_tab(t))

            _register_dnd_widget(f)
            _register_dnd_widget(lbl)
            _register_dnd_widget(close)

            self._btns[tab.id] = (f, lbl, pin, close, border)

        def select(self, tab): # [Select active tab]
            if self.active:
                self.active.hide()
            self.active = tab
            tab.show()
            self.refresh()
            update_title()
            update_status()

        def remove(self, tab): # [Remove tab from bar]
            if tab in self.tabs:
                self.tabs.remove(tab)
            if tab.id in self._btns:
                self._btns[tab.id][0].destroy()
                del self._btns[tab.id]
            tab.frame.destroy()

        def refresh(self): # [Refresh tab bar UI and styling]
            for t in self.tabs:
                if t.id not in self._btns:
                    continue
                f, lbl, pin, close, border = self._btns[t.id]
                active = (t is self.active)
                bg_col = TAB_ACTIVE if active else TAB_BG
                fg_col = TAB_FG_ACT if active else TAB_FG
                f.config(bg=bg_col)
                border.config(bg="#3c3c3c" if not active else TAB_ACTIVE)
                lbl.config(bg=bg_col, fg=fg_col, text=t.label)
                pin.config(bg=bg_col, fg=fg_col if t.is_pinned else STATUS_FG)
                if t.is_pinned and not pin.winfo_manager():
                    pin.pack(side='left', before=lbl, fill='y')
                elif not t.is_pinned and pin.winfo_manager():
                    pin.pack_forget()
                close.config(bg=bg_col, fg=fg_col)

    # ── Layout ────────────────────────────────────────────────────────────────────
    tab_bar = TabBar(win) # [Instantiate tab bar]

    status_bar = tk.Frame(win, bg=STATUS_BG, height=24) # [Status bar container frame]
    if SETTINGS['show_status']:
        status_bar.pack(side='bottom', fill='x')
    status_bar.pack_propagate(False)

    status_file = tk.Label( # [Status file name label]
        status_bar,
        text=tr('status_untitled'),
        bg=STATUS_BG,
        fg=STATUS_FG,
        font=('Andale Mono', 10),
        padx=10,
    )
    status_file.pack(side='left')

    #status_file.config(text=tr('status_untitled'))

    status_pos = tk.Label( # [Status cursor position label]
        status_bar,
        text="Ln 1, Col 1",
        bg=STATUS_BG,
        fg=STATUS_FG,
        font=('Andale Mono', 10),
        padx=10,
    )
    status_pos.pack(side='right')

    status_words = tk.Label( # [Status word count label]
        status_bar,
        text=f"0 {tr('status_words_many')}",
        bg=STATUS_BG,
        fg=STATUS_FG,
        font=('Andale Mono', 10),
        padx=10,
    )
    if SETTINGS['show_wordcount']:
        status_words.pack(side='right')

    # ══════════════════════════════════════════════════════════════════════════════
    # Barre de recherche (Find Search Bar)
    # ══════════════════════════════════════════════════════════════════════════════
    search_bar = tk.Frame(win, bg=STATUS_BG, height=32, padx=8) # [Find bar container]
    
    search_entry = tk.Entry( # [Find search input entry]
        search_bar, bg=TAB_BG, fg=FG, insertbackground=FG,
        font=('Consolas', 11), relief='flat', bd=2
    )
    search_entry.pack(side='left', padx=5, pady=4)
    search_entry.bind('<Return>', lambda e: find_next())
    search_entry.bind('<Shift-Return>', lambda e: find_prev())

    btn_prev = tk.Label(search_bar, text=" ▲ ", bg=STATUS_BG, fg=FG, font=('Consolas', 11), cursor=HAND_CURSOR) # [Find previous button]
    btn_prev.pack(side='left', padx=2)
    btn_prev.bind('<Button-1>', lambda e: find_prev())

    btn_next = tk.Label(search_bar, text=" ▼ ", bg=STATUS_BG, fg=FG, font=('Consolas', 11), cursor=HAND_CURSOR) # [Find next button]
    btn_next.pack(side='left', padx=2)
    btn_next.bind('<Button-1>', lambda e: find_next())

    search_count = tk.Label(search_bar, text="", bg=STATUS_BG, fg=STATUS_FG, font=('Consolas', 10)) # [Search match count label]
    search_count.pack(side='left', padx=10)

    btn_close_search = tk.Label(search_bar, text=" ✕ ", bg=STATUS_BG, fg=STATUS_FG, font=('Consolas', 11), cursor=HAND_CURSOR) # [Close search button]
    btn_close_search.pack(side='right', padx=5)
    btn_close_search.bind('<Button-1>', lambda e: close_search())

    def show_find(event=None): # [Show find search bar from menu or shortcut]
        if not search_bar.winfo_manager():
            search_bar.pack(side='top', fill='x', before=main_work_area if 'main_work_area' in globals() else None)
        search_bar.lift()
        def _focus_search():
            try:
                search_entry.focus_set()
                search_entry.select_range(0, 'end')
            except tk.TclError:
                pass
        win.after_idle(_focus_search)
        return 'break'

    def close_search(event=None): # [Close find search bar]
        search_bar.pack_forget()
        t = current_tab()
        if t:
            t.text.tag_remove('search_match', '1.0', 'end')
            t.text.focus_set()
        return 'break'

    def find_next(): # [Find next match helper]
        _do_find(direction=1)

    def find_prev(): # [Find previous match helper]
        _do_find(direction=-1)

    def _do_find(direction=1): # [Core find and highlight logic]
        t = current_tab()
        if not t:
            return
        query = search_entry.get()
        if not query:
            search_count.config(text="")
            return

        t.text.tag_remove('search_match', '1.0', 'end')
        t.text.tag_configure('search_match', background=SELECT_BG, foreground=get_contrast_color(SELECT_BG))

        content = t.text.get('1.0', 'end-1c')
        matches = [m.start() for m in re.finditer(re.escape(query), content, re.IGNORECASE)]
        
        if not matches:
            search_count.config(text=tr('search_no_results'))
            return

        search_count.config(text=f"{len(matches)} match(es)")

        curr_idx = t.text.index('insert')
        line, col = map(int, curr_idx.split('.'))
        curr_offset = sum(len(l) + 1 for l in content.splitlines()[:line-1]) + col

        target_offset = None
        if direction == 1:
            for m in matches:
                if m > curr_offset:
                    target_offset = m
                    break
            if target_offset is None:
                target_offset = matches[0]
        else:
            for m in reversed(matches):
                if m < curr_offset:
                    target_offset = m
                    break
            if target_offset is None:
                target_offset = matches[-1]

        for m in matches:
            start_pos = f"1.0+{m}c"
            end_pos = f"1.0+{m + len(query)}c"
            t.text.tag_add('search_match', start_pos, end_pos)

        target_pos = f"1.0+{target_offset}c"
        t.text.mark_set('insert', target_pos)
        t.text.see(target_pos)

    # ══════════════════════════════════════════════════════════════════════════════
    # Main Work Area & Folder Sidebar Management
    # ══════════════════════════════════════════════════════════════════════════════
    main_work_area = tk.Frame(win, bg=BG) # [Main work area container]
    main_work_area.pack(side='top', fill='both', expand=True)

    # ── Folder Sidebar ────────────────────────────────────────────────────────────
    sidebar_frame = tk.Frame(main_work_area, bg=STATUS_BG, width=220) # [Sidebar container frame]
    sidebar_frame.pack(side='left', fill='y')
    sidebar_frame.pack_propagate(False)

    # Narrow drag handle at the sidebar's right edge.
    sidebar_resize_handle = tk.Frame(main_work_area, bg=STATUS_BG, width=5, cursor='sb_h_double_arrow')
    sidebar_resize_handle.pack(side='left', fill='y')
    sidebar_resize_handle.pack_propagate(False)
    _sidebar_resize_start = {'x': 0, 'width': 220}

    def _sidebar_resize_begin(event):
        _sidebar_resize_start['x'] = event.x_root
        _sidebar_resize_start['width'] = sidebar_frame.winfo_width()
        return 'break'

    def _sidebar_resize_motion(event):
        if sidebar_collapsed:
            return 'break'
        delta = event.x_root - _sidebar_resize_start['x']
        new_width = max(140, min(520, _sidebar_resize_start['width'] + delta))
        sidebar_frame.config(width=new_width)
        return 'break'

    sidebar_resize_handle.bind('<Button-1>', _sidebar_resize_begin)
    sidebar_resize_handle.bind('<B1-Motion>', _sidebar_resize_motion)
    def _sidebar_resize_end(event=None):
        SETTINGS['sidebar_width'] = sidebar_frame.winfo_width()
        save_settings_to_disk()
        return 'break'
    sidebar_resize_handle.bind('<ButtonRelease-1>', _sidebar_resize_end)
    sidebar_resize_handle.bind('<Enter>', lambda e: sidebar_resize_handle.config(bg=SELECT_BG))
    sidebar_resize_handle.bind('<Leave>', lambda e: sidebar_resize_handle.config(bg=STATUS_BG))

    sidebar_collapsed = SETTINGS.get('sidebar_collapsed', False)
    current_opened_folder = None

    # Compact button shown when sidebar is collapsed
    sidebar_collapsed_btn = tk.Label(
        sidebar_frame, text=" ▶ ", bg=STATUS_BG, fg=STATUS_FG,
        font=('Consolas', 12, 'bold'), cursor=HAND_CURSOR, pady=8
    )

    sidebar_content_frame = tk.Frame(sidebar_frame, bg=STATUS_BG) # [Sidebar content inner frame]
    sidebar_content_frame.pack(fill='both', expand=True)

    # Header
    sidebar_header = tk.Frame(sidebar_content_frame, bg=STATUS_BG, height=32) # [Sidebar header frame]
    sidebar_header.pack(fill='x', side='top')
    sidebar_header.pack_propagate(False)

    sidebar_title_lbl = tk.Label( # [Sidebar title label]
        sidebar_header, text=tr('sidebar_explorer'), bg=STATUS_BG, fg=STATUS_FG,
        font=('Consolas', 10, 'bold'), anchor='w', padx=10
    )
    sidebar_title_lbl.pack(side='left', fill='both', expand=True)

    # Close parent folder X button
    sidebar_close_folder_btn = tk.Label(
        sidebar_header, text=" ✕ ", bg=STATUS_BG, fg=STATUS_FG,
        font=('Consolas', 10, 'bold'), cursor=HAND_CURSOR, padx=4
    )

    def close_folder(event=None): # [Close parent folder action]
        global current_opened_folder
        current_opened_folder = None
        sidebar_tree.delete(*sidebar_tree.get_children())
        sidebar_title_lbl.config(text=tr('sidebar_explorer'))
        sidebar_close_folder_btn.pack_forget()

    sidebar_close_folder_btn.bind('<Button-1>', close_folder)

    sidebar_toggle_btn = tk.Label( # [Sidebar toggle collapse button]
        sidebar_header, text=" ◀ ", bg=STATUS_BG, fg=STATUS_FG,
        font=('Consolas', 12, 'bold'), cursor=HAND_CURSOR, padx=6, pady=8
    )
    sidebar_toggle_btn.pack(side='right', fill='y')

    # Treeview area
    sidebar_tree_frame = tk.Frame(sidebar_content_frame, bg=STATUS_BG) # [Sidebar treeview container]
    sidebar_tree_frame.pack(fill='both', expand=True)

    sidebar_tree = ttk.Treeview( # [Sidebar file explorer treeview widget]
        sidebar_tree_frame,
        show='tree',
        selectmode='browse',
    )
    sidebar_tree.pack(fill='both', expand=True)

    # Styling for Treeview
    def update_sidebar_theme(): # [Update sidebar ttk treeview theme]
        style = ttk.Style()
        style.theme_use('default')
        bg_col = THEMES[current_theme]['STATUS_BG']
        fg_col = THEMES[current_theme]['FG']
        sel_bg = THEMES[current_theme]['SELECT_BG']
        sel_fg = THEMES[current_theme]['FG']

        style.configure(
            "Treeview",
            background=bg_col,
            foreground=fg_col,
            fieldbackground=bg_col,
            borderwidth=0,
            font=('Consolas', 10)
        )
        style.map(
            "Treeview",
            background=[('selected', sel_bg)],
            foreground=[('selected', sel_fg)]
        )
        sidebar_frame.config(bg=bg_col)
        sidebar_resize_handle.config(bg=bg_col)
        sidebar_content_frame.config(bg=bg_col)
        sidebar_header.config(bg=bg_col)
        sidebar_title_lbl.config(bg=bg_col, fg=STATUS_FG)
        sidebar_close_folder_btn.config(bg=bg_col, fg=STATUS_FG)
        sidebar_toggle_btn.config(bg=bg_col, fg=STATUS_FG)
        sidebar_collapsed_btn.config(bg=bg_col, fg=STATUS_FG)
        sidebar_tree_frame.config(bg=bg_col)

    update_sidebar_theme()

    def toggle_sidebar(event=None): # [Toggle sidebar collapse/expand]
        global sidebar_collapsed
        sidebar_collapsed = not sidebar_collapsed
        SETTINGS['sidebar_collapsed'] = sidebar_collapsed
        save_settings_to_disk()

        if sidebar_collapsed:
            SETTINGS['sidebar_width'] = sidebar_frame.winfo_width()
            sidebar_content_frame.pack_forget()
            sidebar_frame.config(width=28)
            sidebar_resize_handle.config(width=3)
            sidebar_collapsed_btn.pack(fill='both', expand=True)
        else:
            sidebar_collapsed_btn.pack_forget()
            sidebar_frame.config(width=max(140, int(SETTINGS.get('sidebar_width', 220))))
            sidebar_resize_handle.config(width=5)
            sidebar_content_frame.pack(fill='both', expand=True)

    sidebar_toggle_btn.bind('<Button-1>', toggle_sidebar)
    sidebar_collapsed_btn.bind('<Button-1>', toggle_sidebar)

    # Set initial sidebar visual state based on saved settings
    if sidebar_collapsed:
        sidebar_content_frame.pack_forget()
        sidebar_frame.config(width=28)
        sidebar_resize_handle.config(width=3)
        sidebar_collapsed_btn.pack(fill='both', expand=True)
    else:
        sidebar_frame.config(width=max(140, int(SETTINGS.get('sidebar_width', 220))))

    # Treeview dynamic expansion logic
    def populate_tree_node(parent_node, folder_path): # [Populate folder contents into treeview]
        try:
            entries = sorted(os.scandir(folder_path), key=lambda e: (not e.is_dir(), e.name.lower()))
            for entry in entries:
                if entry.name.startswith('.'):
                    continue
                if entry.is_dir():
                    node = sidebar_tree.insert(parent_node, 'end', text=f"📁 {entry.name}", values=[entry.path], open=False)
                    sidebar_tree.insert(node, 'end', text="loading...")
                else:
                    sidebar_tree.insert(parent_node, 'end', text=f"📄 {entry.name}", values=[entry.path])
        except PermissionError:
            pass

    def on_tree_open(event): # [Handle tree node expansion]
        item = sidebar_tree.focus()
        children = sidebar_tree.get_children(item)
        if len(children) == 1 and sidebar_tree.item(children[0], 'text') == "loading...":
            sidebar_tree.delete(children[0])
            item_path = sidebar_tree.item(item, 'values')[0]
            populate_tree_node(item, item_path)

    def on_tree_double_click(event): # [Handle file double click in tree]
        item = sidebar_tree.focus()
        if not item:
            return
        values = sidebar_tree.item(item, 'values')
        if values and os.path.isfile(values[0]):
            _open_paths([values[0]])

    sidebar_tree.bind('<<TreeviewOpen>>', on_tree_open)
    sidebar_tree.bind('<Double-1>', on_tree_double_click)

    def open_folder(folder_path=None): # [Open folder dialog and load tree]
        global current_opened_folder
        if not folder_path:
            folder_path = filedialog.askdirectory()
        if not folder_path or not os.path.isdir(folder_path):
            return

        current_opened_folder = folder_path
        folder_name = os.path.basename(folder_path) or folder_path
        sidebar_title_lbl.config(text=f"📁 {folder_name.upper()}")
        sidebar_close_folder_btn.pack(side='right', before=sidebar_toggle_btn, fill='y')

        sidebar_tree.delete(*sidebar_tree.get_children())
        root_node = sidebar_tree.insert('', 'end', text=f"📂 {folder_name}", values=[folder_path], open=True)
        populate_tree_node(root_node, folder_path)

        if sidebar_collapsed:
            toggle_sidebar()

    # ── Editor Area ───────────────────────────────────────────────────────────────
    editor_area = tk.Frame(main_work_area, bg=BG) # [Editor area container frame]
    editor_area.pack(side='left', fill='both', expand=True)

    win.minsize(400, 150) # [Set minimum window size]

    # ── Drag & Drop ───────────────────────────────────────────────────────────────
    dnd_enabled = False

    def _parse_dnd_paths(data): # [Parse dropped file paths string]
        paths = []
        raw = data.strip()
        i = 0
        while i < len(raw):
            if raw[i] == '{':
                end = raw.index('}', i)
                paths.append(raw[i+1:end])
                i = end + 2
            else:
                end = raw.find(' ', i)
                if end == -1:
                    paths.append(raw[i:])
                    break
                paths.append(raw[i:])
                i = end + 1
        return [p for p in paths if p]

    def _open_paths(paths): # [Open multiple file or folder paths]
        for path in paths:
            if os.path.isdir(path):
                open_folder(path)
            elif os.path.isfile(path):
                try:
                    if os.path.splitext(path)[1].lower() == '.rtf':
                        with open(path, 'rb') as f:
                            raw_content = f.read()
                        try:
                            rtf_content = raw_content.decode('utf-8')
                        except UnicodeDecodeError:
                            rtf_content = raw_content.decode('cp1252')
                        content = rtf_to_text(rtf_content)
                    else:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                except UnicodeDecodeError:
                    continue
                t = current_tab()
                if t and not t.is_modified and not t.get_content():
                    t.file_path = path
                    t.is_pinned = os.path.abspath(path) in PINNED_DOCS
                    t.set_content(content)
                    t.set_modified(False)
                    tab_bar.refresh()
                    update_title()
                else:
                    new_tab(file_path=path, content=content)
                add_recent_file(path)

    def _on_drop(event): # [Handle drag and drop event]
        editor_area.config(bg=BG)
        tab_bar.frame.config(bg=TAB_BG)
        _open_paths(_parse_dnd_paths(event.data))

    def _on_enter(event): # [Handle drag enter visual feedback]
        editor_area.config(bg=SELECT_BG)
        tab_bar.frame.config(bg=SELECT_BG)

    def _on_leave(event): # [Handle drag leave visual feedback]
        editor_area.config(bg=BG)
        tab_bar.frame.config(bg=TAB_BG)

    def _register_dnd_widget(widget): # [Register widget for drag and drop]
        if not dnd_enabled:
            return
        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', _on_drop)
            widget.dnd_bind('<<DragEnter>>', _on_enter)
            widget.dnd_bind('<<DragLeave>>', _on_leave)
        except Exception as e:
            print(f"[DND] Erreur enregistrement drop_target sur {widget} : {e}")

    def _setup_dnd(): # [Setup drag and drop across widgets]
        global dnd_enabled
        if not DND_AVAILABLE:
            messagebox.showwarning(
                tr('dnd_title'),
                tr('dnd_msg')
            )
            return

        dnd_enabled = True
        try:
            for widget in (editor_area, tab_bar.frame, sidebar_frame, sidebar_tree):
                _register_dnd_widget(widget)
        except Exception as e:
            print(f"[DND] Erreur lors de l'enregistrement des widgets DnD : {e}")

    _setup_dnd() # [Initialize DND setup]

    # ── Actions globales ──────────────────────────────────────────────────────────
    def add_recent_file(file_path): # [Add file to recent files list]
        """Adds a file to recents_doc.json and keeps at most 10 items."""
        if not file_path:
            return
        abs_path = os.path.abspath(file_path)
        recents = load_recents_from_disk()
        recents = [r for r in recents if (r.get('path') if isinstance(r, dict) else r) != abs_path]
        recents.insert(0, {
            'name': os.path.basename(abs_path),
            'path': abs_path
        })
        recents = recents[:10]
        save_recents_to_disk(recents)
        rebuild_menu()

    def open_recent_file(path): # [Open recent file handler]
        if not os.path.exists(path):
            messagebox.showerror("Error", f"File not found: {path}")
            recents = [item for item in load_recents_from_disk() if (item.get('path') if isinstance(item, dict) else item) != path]
            save_recents_to_disk(recents)
            rebuild_menu()
            return
        _open_paths([path])

    def current_tab(): # [Get active tab instance]
        return tab_bar.active

    def toggle_current_tab_pin(event=None):
        tab = current_tab()
        if tab:
            return tab_bar.toggle_pin(tab)
        return 'break'

    def update_title(): # [Update window title and status file label]
        t = current_tab()
        name = t.name if t else "Notys"
        win.title(f"Notys — {name}")
        status_file.config(text=name)

    def update_status(event=None): # [Update status bar cursor pos and word count]
        t = current_tab()
        if not t:
            return
        idx = t.text.index('insert')
        line, col = idx.split('.')
        status_pos.config(text=f"Ln {line}, Col {int(col)+1}")
        content = t.get_content()
        words = len(content.split()) if content.strip() else 0
        status_words.config(text=f"{words} {tr('status_words_one') if words == 1 else tr('status_words_many')}")

    def new_tab(event=None, file_path=None, content=None): # [Create and open new tab]
        tab = Tab(file_path=file_path)
        tab_bar.add(tab)
        if content:
            tab.set_content(content)
        return tab

    def restore_pinned_tabs():
        restored_paths = []
        for path in PINNED_DOCS:
            if not os.path.isfile(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (OSError, UnicodeDecodeError) as e:
                print(f"[Pins] Error opening {path}: {e}")
                continue
            new_tab(file_path=path, content=content)
            restored_paths.append(path)

        if restored_paths != PINNED_DOCS:
            PINNED_DOCS[:] = restored_paths
            save_pinned_docs()
        if not restored_paths:
            new_tab()

    def _dialog_unsaved(tab): # [Unsaved changes confirmation dialog]
        result = [None]

        dlg = tk.Toplevel(win)
        dlg.withdraw()
        dlg.title("")
        dlg.resizable(False, False)
        dlg.configure(bg=STATUS_BG)
        dlg.transient(win)
        dlg.grab_set()

        frame = tk.Frame(dlg, bg=STATUS_BG, padx=28, pady=24)
        frame.pack(fill='both', expand=True)

        icon_lbl = tk.Label(frame, text="⚠", font=('Arial', 32), bg=STATUS_BG, fg='#e5c07b')
        icon_lbl.grid(row=0, column=0, rowspan=2, padx=(0, 18), sticky='n', pady=(2, 0))

        name = tab.name if tab.name != tr('untitled') else "this document"
        tk.Label(
            frame,
            text=tr('dlg_save_msg', name=name),
            font=('Consolas', 12, 'bold'),
            bg=STATUS_BG, fg=FG,
            justify='left',
        ).grid(row=0, column=1, sticky='w')

        tk.Label(
            frame,
            text=tr('dlg_save_sub'),
            font=('Consolas', 10),
            bg=STATUS_BG, fg=STATUS_FG,
            justify='left',
        ).grid(row=1, column=1, sticky='w', pady=(4, 0))

        btn_frame = tk.Frame(dlg, bg=STATUS_BG, padx=28, pady=20)
        btn_frame.pack(fill='x')

        def _btn(parent, text, cmd, primary=False): # [Helper for dialog buttons]
            if primary:
                bg = SELECT_BG if current_theme == 'dark' else '#1a6bbf'
                bg_hover = '#3a6090' if current_theme == 'dark' else '#145299'
            else:
                bg = '#3a3a3a' if current_theme == 'dark' else '#9e9e9e'
                bg_hover = '#4a4a4a' if current_theme == 'dark' else '#7a7a7a'
            fg = '#ffffff'
            b = tk.Label(
                parent, text=text,
                bg=bg, fg=fg,
                font=('Consolas', 11, 'bold' if primary else 'normal'),
                padx=16, pady=6,
                cursor=HAND_CURSOR,
                relief='flat',
            )
            b.bind('<Button-1>', lambda e: cmd())
            b.bind('<Enter>', lambda e: b.config(bg=bg_hover))
            b.bind('<Leave>', lambda e: b.config(bg=bg))
            return b

        def do_discard(): # [Discard changes action]
            result[0] = 'discard'
            dlg.destroy()

        def do_cancel(): # [Cancel dialog action]
            result[0] = 'cancel'
            dlg.destroy()

        def do_save(): # [Save changes action]
            result[0] = 'save'
            dlg.destroy()

        _btn(btn_frame, tr('dlg_dont_save'), do_discard).pack(side='left')
        _btn(btn_frame, tr('dlg_cancel'), do_cancel, primary=True).pack(side='right')
        _btn(btn_frame, tr('dlg_save'), do_save).pack(side='left', padx=(10, 0))

        dlg.update_idletasks()
        w, h = dlg.winfo_width(), dlg.winfo_height()
        x = win.winfo_x() + (win.winfo_width() - w) // 2
        y = win.winfo_y() + (win.winfo_height() - h) // 2
        dlg.geometry(f'+{x}+{y}')
        dlg.deiconify()
        dlg.focus_force()
        dlg.bind('<Escape>', lambda e: do_cancel())

        win.wait_window(dlg)
        return result[0]

    def _save_tab(tab): # [Save tab content to disk]
        if tab.file_path is None:
            path = filedialog.asksaveasfilename(
                defaultextension='.md',
                filetypes=[('Markdown', '*.md'), ('Text', '*.txt'), ('All files', '*.*')]
            )
            if not path:
                return False
            tab.file_path = path
            update_title()

        with open(tab.file_path, 'w', encoding='utf-8') as f:
            f.write(tab.get_content())

        tab.highlight_markdown()
        tab.set_modified(False)
        add_recent_file(tab.file_path)
        return True

    _closed_tabs_history = []  # [History stack for recently closed tabs]

    def close_tab(tab=None, event=None):
        if tab is None:
            tab = current_tab()
        if tab is None:
            return

        if tab.is_modified:
            action = _dialog_unsaved(tab)
            if action == 'cancel' or action is None:
                return
            if action == 'save':
                if not _save_tab(tab):
                    return

        if len(tab_bar.tabs) == 1:
            on_quit()
            return

        _closed_tabs_history.append({
            'file_path': tab.file_path,
            'content': tab.get_content()
        })
        tab_bar.remove(tab)
        if tab_bar.tabs:
            tab_bar.select(tab_bar.tabs[-1])

    def reopen_closed_tab(event=None):
        if not _closed_tabs_history:
            return
        data = _closed_tabs_history.pop()
        path = data.get('file_path')
        content = data.get('content', '')
        if path and os.path.isfile(path):
            _open_paths([path])
        else:
            new_tab(file_path=path, content=content)

    def open_file_dialog(event=None):
        paths = filedialog.askopenfilenames(
            filetypes=[
                ("Tous les fichiers supportés", "*.md *.txt *.rtf"),
                ("Markdown", "*.md"),
                ("Texte", "*.txt"),
                ("Rich Text Format", "*.rtf"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if paths:
            _open_paths(paths)

    def save_file(event=None):
        t = current_tab()
        if t:
            _save_tab(t)

    def save_file_as(event=None):
        t = current_tab()
        if not t:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[
                ("Markdown", "*.md"),
                ("Texte", "*.txt"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if path:
            if t.is_pinned and t.file_path:
                old_path = os.path.abspath(t.file_path)
                if old_path in PINNED_DOCS:
                    PINNED_DOCS.remove(old_path)
                new_path = os.path.abspath(path)
                if new_path not in PINNED_DOCS:
                    PINNED_DOCS.append(new_path)
                save_pinned_docs()
            t.file_path = path
            t.is_pinned = t.is_pinned and os.path.abspath(path) in PINNED_DOCS
            tab_bar.refresh()
            _save_tab(t)

    def save_all(event=None):
        for t in tab_bar.tabs:
            if t.is_modified:
                _save_tab(t)

    def on_quit(event=None): # [Quit application handler with check for unsaved tabs]
        unsaved = [t for t in tab_bar.tabs if t.is_modified]
        for tab in unsaved:
            tab_bar.select(tab)
            action = _dialog_unsaved(tab)
            if action == 'cancel' or action is None:
                return
            if action == 'save':
                if not _save_tab(tab):
                    return
        win.destroy()

    def show_about(): # [Show about dialog]
        messagebox.showinfo(
            tr('menu_about'),
            f"{APP_NAME} v{APP_VERSION}\n{APP_COPYRIGHT}\n\n"
        )

    def new_window(event=None): # [Open new window instance shortcut]
        import subprocess
        subprocess.Popen([sys.executable, __file__])
        return 'break'

    win.protocol('WM_DELETE_WINDOW', on_quit) # [Bind window close protocol]

    # ══════════════════════════════════════════════════════════════════════════════
    # Shortcut System Dictionary
    # ══════════════════════════════════════════════════════════════════════════════
    SHORTCUTS = {
        'new_tab': {'cmd': lambda e=None: new_tab(), 'disp': f"{mod_display}T", 'keys': ['<Command-t>', '<Command-T>'] if is_macos else ['<Control-t>', '<Control-T>']},
        'new_window': {'cmd': lambda e=None: new_window(), 'disp': f"{mod_display}N", 'keys': ['<Command-N>', '<Command-n>'] if is_macos else ['<Control-N>', '<Control-n>']},
        'reopen_tab': {'cmd': lambda e=None: reopen_closed_tab(), 'disp': f"{mod_display}Shift+T", 'keys': ['<Command-Shift-T>', '<Command-Shift-t>'] if is_macos else ['<Control-Shift-T>', '<Control-Shift-t>']},
        'open_file': {'cmd': lambda e=None: open_file_dialog(), 'disp': f"{mod_display}O", 'keys': ['<Command-o>', '<Command-O>'] if is_macos else ['<Control-o>', '<Control-O>']},
        'open_folder': {'cmd': lambda e=None: open_folder(), 'disp': f"{mod_display}Shift+O", 'keys': ['<Command-Shift-O>', '<Command-Shift-o>'] if is_macos else ['<Control-Shift-O>', '<Control-Shift-o>']},
        'save_file': {'cmd': lambda e=None: save_file(), 'disp': f"{mod_display}S", 'keys': ['<Command-s>', '<Command-S>'] if is_macos else ['<Control-s>', '<Control-S>']},
        'save_file_as': {'cmd': lambda e=None: save_file_as(), 'disp': f"{mod_display}Shift+S", 'keys': ['<Command-Shift-S>', '<Command-Shift-s>'] if is_macos else ['<Control-Shift-S>', '<Control-Shift-s>']},
        'save_all': {'cmd': lambda e=None: save_all(), 'disp': f"{mod_display}D", 'keys': ['<Command-d>', '<Command-D>'] if is_macos else ['<Control-d>', '<Control-D>']},
        'close_tab': {'cmd': lambda e=None: close_tab(), 'disp': f"{mod_display}W", 'keys': ['<Command-w>', '<Command-W>'] if is_macos else ['<Control-w>', '<Control-W>']},
        'pin_tab': {'cmd': lambda e=None: toggle_current_tab_pin(), 'disp': f"{mod_display}Shift+P", 'keys': ['<Command-Shift-P>', '<Command-Shift-p>'] if is_macos else ['<Control-Shift-P>', '<Control-Shift-p>']},
        'undo': {'cmd': lambda e=None: current_tab() and current_tab().text.event_generate('<<Undo>>'), 'disp': f"{mod_display}Z", 'keys': ['<Command-z>', '<Command-Z>'] if is_macos else ['<Control-z>', '<Control-Z>']},
        'redo': {'cmd': lambda e=None: current_tab() and current_tab().text.event_generate('<<Redo>>'), 'disp': "Cmd+Shift+Z" if is_macos else f"{mod_display}Y", 'keys': ['<Command-Shift-Z>', '<Command-Shift-z>'] if is_macos else ['<Control-y>', '<Control-Y>']},
        'cut': {'cmd': lambda e=None: current_tab() and current_tab().text.event_generate('<<Cut>>'), 'disp': f"{mod_display}X", 'keys': ['<Command-x>', '<Command-X>'] if is_macos else ['<Control-x>', '<Control-X>']},
        'copy': {'cmd': lambda e=None: current_tab() and current_tab().text.event_generate('<<Copy>>'), 'disp': f"{mod_display}C", 'keys': ['<Command-c>', '<Command-C>'] if is_macos else ['<Control-c>', '<Control-C>']},
        'paste': {'cmd': lambda e=None: current_tab() and current_tab().text.event_generate('<<Paste>>'), 'disp': f"{mod_display}V", 'keys': ['<Command-v>', '<Command-V>'] if is_macos else ['<Control-v>', '<Control-V>']},
        'find': {'cmd': lambda e=None: show_find(), 'disp': f"{mod_display}F", 'keys': ['<Command-f>', '<Command-F>'] if is_macos else ['<Control-f>', '<Control-F>']},
        'settings': {'cmd': lambda e=None: open_settings(), 'disp': f"{mod_display},", 'keys': ['<Command-comma>'] if is_macos else ['<Control-comma>']},
    }

    def register_shortcuts(): # [Register global keyboard shortcuts]
        for name, item in SHORTCUTS.items():
            for key_binding in item['keys']:
                win.bind_all(key_binding, item['cmd'])

    register_shortcuts()

    def rebuild_menu(): # [Rebuild menu bar structure]
        menubar.delete(0, 'end')

        # ── Menu d'application spécifique à macOS ─────────────────────────────────
        if is_macos:
            app_menu = tk.Menu(menubar, name='apple')
            app_menu.add_command(label=f"{tr('menu_about')} {APP_NAME}", command=show_about)
            app_menu.add_separator()
            app_menu.add_command(label=tr('settings_title'), command=open_settings, accelerator=SHORTCUTS['settings']['disp'])
            menubar.add_cascade(menu=app_menu)

            win.createcommand('::tk::mac::ShowPreferences', open_settings)
            win.createcommand('::tk::mac::ShowAbout', show_about)

        # ── Menu Fichier ──────────────────────────────────────────────────────────
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=tr('menu_new_tab'), command=new_tab, accelerator=SHORTCUTS['new_tab']['disp'])
        file_menu.add_command(label=tr('menu_new_window'), command=new_window, accelerator=SHORTCUTS['new_window']['disp'])
        file_menu.add_command(label=tr('menu_reopen_tab'), command=reopen_closed_tab, accelerator=SHORTCUTS['reopen_tab']['disp'])
        file_menu.add_separator()
        file_menu.add_command(label=tr('menu_open'), command=open_file_dialog, accelerator=SHORTCUTS['open_file']['disp'])
        file_menu.add_command(label=tr('menu_open_folder'), command=open_folder, accelerator=SHORTCUTS['open_folder']['disp'])

        # Récents
        recents_menu = tk.Menu(file_menu, tearoff=0)
        recents = load_recents_from_disk()
        if recents:
            for item in recents:
                name = item.get('name') if isinstance(item, dict) else os.path.basename(item)
                path = item.get('path') if isinstance(item, dict) else item
                recents_menu.add_command(label=name, command=lambda p=path: open_recent_file(p))
        else:
            recents_menu.add_command(label="Aucun fichier récent", state='disabled')
        file_menu.add_cascade(label=tr('menu_open_recents'), menu=recents_menu)

        file_menu.add_separator()
        file_menu.add_command(label=tr('menu_save'), command=save_file, accelerator=SHORTCUTS['save_file']['disp'])
        file_menu.add_command(label=tr('menu_save_as'), command=save_file_as, accelerator=SHORTCUTS['save_file_as']['disp'])
        file_menu.add_command(label=tr('menu_save_all'), command=save_all, accelerator=SHORTCUTS['save_all']['disp'])
        file_menu.add_command(label=tr('menu_toggle_pin'), command=toggle_current_tab_pin, accelerator=SHORTCUTS['pin_tab']['disp'])
        file_menu.add_separator()
        file_menu.add_command(label=tr('menu_close_tab'), command=lambda: close_tab(), accelerator=SHORTCUTS['close_tab']['disp'])
        menubar.add_cascade(label=tr('menu_file'), menu=file_menu)

        # ── Menu Édition ──────────────────────────────────────────────────────────
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label=tr('menu_undo'), command=SHORTCUTS['undo']['cmd'], accelerator=SHORTCUTS['undo']['disp'])
        edit_menu.add_command(label=tr('menu_redo'), command=SHORTCUTS['redo']['cmd'], accelerator=SHORTCUTS['redo']['disp'])
        edit_menu.add_separator()
        edit_menu.add_command(label=tr('menu_cut'), command=SHORTCUTS['cut']['cmd'], accelerator=SHORTCUTS['cut']['disp'])
        edit_menu.add_command(label=tr('menu_copy'), command=SHORTCUTS['copy']['cmd'], accelerator=SHORTCUTS['copy']['disp'])
        edit_menu.add_command(label=tr('menu_paste'), command=SHORTCUTS['paste']['cmd'], accelerator=SHORTCUTS['paste']['disp'])
        edit_menu.add_separator()
        edit_menu.add_command(label=tr('menu_find'), command=show_find, accelerator=SHORTCUTS['find']['disp'])
        menubar.add_cascade(label=tr('menu_edit'), menu=edit_menu)

        # ── Menus dédiés Windows & Linux ─────────────────────────────────────────
        if not is_macos:
            settings_menu = tk.Menu(menubar, tearoff=0)
            settings_menu.add_command(label=tr('menu_open_settings'), command=open_settings)
            menubar.add_cascade(label=tr('menu_settings'), menu=settings_menu)

            about_menu = tk.Menu(menubar, tearoff=0)
            about_menu.add_command(label=tr('menu_about'), command=show_about)
            menubar.add_cascade(label=tr('menu_about'), menu=about_menu)

    def open_settings(event=None): # [Open settings dialog modal window]
        global current_language, SETTINGS

        # Prevent duplicate settings window creation
        if hasattr(win, '_settings_dlg') and win._settings_dlg is not None:
            try:
                if win._settings_dlg.winfo_exists():
                    win._settings_dlg.lift()
                    win._settings_dlg.focus_force()
                    return 'break'
            except Exception:
                win._settings_dlg = None

        dlg = tk.Toplevel(win)
        win._settings_dlg = dlg

        def _on_settings_close():
            win._settings_dlg = None
            #sidebar_title_lbl.config(text=tr('sidebar_explorer')) # fixes a bug where the sidebar's empty name would stay in the same language even when we changed the language
            # not the proper way of doing it, i moved it to "apply_settings" instead
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", _on_settings_close)
        dlg.title(tr('settings_title'))
        dlg.geometry("1020x680")
        dlg.resizable(True, True)
        dlg.configure(bg=STATUS_BG)
        dlg.transient(win)
        dlg.grab_set()

        lang_var = tk.StringVar(value=current_language)

        def on_theme_preference_changed(*args):
            global theme_preferences
            new_pref = theme_var.get()
            theme_preferences = new_pref
            save_settings_to_disk()
            apply_theme(resolve_theme(new_pref))

        theme_var = tk.StringVar(value=theme_preferences)
        theme_var.trace_add("write", on_theme_preference_changed)
        font_fam_var = tk.StringVar(value=SETTINGS['font_family'])
        font_size_var = tk.IntVar(value=SETTINGS['font_size'])
        wrap_var = tk.StringVar(value=SETTINGS['line_wrap'])
        padding_var = tk.IntVar(value=SETTINGS['padding'])
        status_var = tk.BooleanVar(value=SETTINGS['show_status'])
        wcount_var = tk.BooleanVar(value=SETTINGS['show_wordcount'])
        win_w_var = tk.IntVar(value=SETTINGS['win_width'])
        win_h_var = tk.IntVar(value=SETTINGS['win_height'])

        H_BG = STATUS_BG
        SEP_FG = "#3c3c3c" if current_theme == 'dark' else "#cccccc"
        ACCENT = SELECT_BG if current_theme == 'dark' else '#1a6bbf'

        def section_label(parent, text, row):
            tk.Label(
                parent, text=text,
                font=('Consolas', 11, 'bold'),
                bg=H_BG, fg=ACCENT, anchor='w',
            ).grid(row=row, column=0, columnspan=3, sticky='w', pady=(18, 4))
            tk.Frame(parent, bg=SEP_FG, height=1).grid(
                row=row+1, column=0, columnspan=3, sticky='ew', pady=(0, 10))

        def row_label(parent, text, row):
            tk.Label(
                parent, text=text,
                font=('Consolas', 11),
                bg=H_BG, fg=FG, anchor='w',
            ).grid(row=row, column=0, sticky='w', pady=4, padx=(0, 20))

        def make_radiogroup(parent, var, options, row, col=1):
            f = tk.Frame(parent, bg=H_BG)
            f.grid(row=row, column=col, sticky='w')
            for label, val in options:
                tk.Radiobutton(
                    f, text=label, variable=var, value=val,
                    bg=H_BG, fg=FG, selectcolor=TAB_BG,
                    activebackground=H_BG, activeforeground=FG,
                    font=('Consolas', 11), cursor=HAND_CURSOR,
                ).pack(side='left', padx=(0, 12))

        def make_toggle(parent, var, row, col=1):
            f = tk.Frame(parent, bg=H_BG)
            f.grid(row=row, column=col, sticky='w')
            for label, val in [(tr('on'), True), (tr('off'), False)]:
                tk.Radiobutton(
                    f, text=label, variable=var, value=val,
                    bg=H_BG, fg=FG, selectcolor=TAB_BG,
                    activebackground=H_BG, activeforeground=FG,
                    font=('Consolas', 11), cursor=HAND_CURSOR,
                ).pack(side='left', padx=(0, 12))

        def make_spinbox(parent, var, from_, to, row, col=1, width=6):
            sb = tk.Spinbox(
                parent, from_=from_, to=to, textvariable=var,
                width=width, font=('Consolas', 11),
                bg=TAB_BG, fg=FG, buttonbackground=TAB_BG,
                insertbackground=FG, relief='flat',
                highlightthickness=1,
                highlightbackground=SEP_FG,
                highlightcolor=ACCENT,
            )
            sb.grid(row=row, column=col, sticky='w', pady=4)

        def make_optionmenu(parent, var, options, row, col=1):
            om = tk.OptionMenu(parent, var, *options)
            om.config(
                bg=TAB_BG, fg=FG, activebackground=SELECT_BG,
                activeforeground=FG, font=('Consolas', 11),
                relief='flat', bd=0, highlightthickness=1,
                highlightbackground=SEP_FG, cursor=HAND_CURSOR,
            )
            om['menu'].config(bg=TAB_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
            om.grid(row=row, column=col, sticky='w', pady=4)

        outer = tk.Frame(dlg, bg=H_BG)
        outer.pack(fill='both', expand=True)

        nav_bg = TAB_BG
        nav = tk.Frame(outer, bg=nav_bg, width=160)
        nav.pack(side='left', fill='y')
        nav.pack_propagate(False)

        content_area = tk.Frame(outer, bg=H_BG)
        content_area.pack(side='left', fill='both', expand=True)

        _current_page = [None]
        _nav_btns = []

        sections = [
            ('section_general', ''),
            ('section_language', ''),
            ('section_styles', ''),
        ]

        def show_page(idx):
            if _current_page[0] is not None:
                _current_page[0].pack_forget()
            pages[idx].pack(fill='both', expand=True, padx=28, pady=10)
            _current_page[0] = pages[idx]
            for i, b in enumerate(_nav_btns):
                b.config(
                    bg=TAB_ACTIVE if i == idx else nav_bg,
                    fg=TAB_FG_ACT if i == idx else TAB_FG,
                )

        tk.Frame(nav, bg=nav_bg, height=12).pack()
        for i, (key, icon) in enumerate(sections):
            label = tr(key).replace(icon, '').strip()
            btn = tk.Label(
                nav, text=f"  {icon}  {label}",
                font=('Consolas', 11),
                bg=nav_bg, fg=TAB_FG,
                anchor='w', cursor=HAND_CURSOR,
                padx=8, pady=10,
            )
            btn.pack(fill='x')
            idx = i
            btn.bind('<Button-1>', lambda e, i=idx: show_page(i))
            btn.bind('<Enter>', lambda e, b=btn, i=idx: b.config(bg=TAB_ACTIVE) if i != _nav_btns.index(b) or _current_page[0] != pages[i] else None)
            btn.bind('<Leave>', lambda e, b=btn, i=idx: b.config(bg=TAB_ACTIVE if _current_page[0] == pages[i] else nav_bg))
            _nav_btns.append(btn)

        p_general = tk.Frame(content_area, bg=H_BG)
        section_label(p_general, tr('section_appearance'), 0)
        row_label(p_general, tr('settings_theme'), 2)
        make_radiogroup(p_general, theme_var, [
            (tr('theme_system'), 'system'),
            (tr('theme_dark'), 'dark'),
            (tr('theme_light'), 'light'),
        ], row=2)

        section_label(p_general, tr('section_editor'), 3)
        row_label(p_general, tr('settings_font_family'), 5)
        font_options = ['Consolas', 'Courier', 'Monaco', 'Menlo', 'DejaVu Sans Mono', 'Arial', 'Helvetica']
        make_optionmenu(p_general, font_fam_var, font_options, row=5)

        row_label(p_general, tr('settings_font_size'), 6)
        make_spinbox(p_general, font_size_var, 8, 48, row=6)

        row_label(p_general, tr('settings_line_wrap'), 7)
        make_radiogroup(p_general, wrap_var, [
            (tr('wrap_word'), 'word'),
            (tr('wrap_char'), 'char'),
            (tr('wrap_none'), 'none'),
        ], row=7)

        row_label(p_general, tr('settings_padding'), 8)
        make_spinbox(p_general, padding_var, 0, 200, row=8)

        section_label(p_general, tr('section_interface'), 9)
        row_label(p_general, tr('settings_show_status'), 11)
        make_toggle(p_general, status_var, row=11)

        row_label(p_general, tr('settings_show_wordcount'), 12)
        make_toggle(p_general, wcount_var, row=12)

        row_label(p_general, tr('settings_win_size'), 13)
        size_f = tk.Frame(p_general, bg=H_BG)
        size_f.grid(row=13, column=1, sticky='w', pady=4)
        tk.Spinbox(size_f, from_=400, to=3840, textvariable=win_w_var,
                   width=6, font=('Consolas', 11), bg=TAB_BG, fg=FG,
                   buttonbackground=TAB_BG, insertbackground=FG, relief='flat',
                   highlightthickness=1, highlightbackground=SEP_FG,
                   highlightcolor=ACCENT).pack(side='left')
        tk.Label(size_f, text=" × ", bg=H_BG, fg=STATUS_FG, font=('Consolas', 11)).pack(side='left')
        tk.Spinbox(size_f, from_=300, to=2160, textvariable=win_h_var,
                   width=6, font=('Consolas', 11), bg=TAB_BG, fg=FG,
                   buttonbackground=TAB_BG, insertbackground=FG, relief='flat',
                   highlightthickness=1, highlightbackground=SEP_FG,
                   highlightcolor=ACCENT).pack(side='left')

        p_language = tk.Frame(content_area, bg=H_BG)
        row_label(p_language, tr('settings_language'), 2)
        make_radiogroup(p_language, lang_var, [("English", 'en'), ("Français", 'fr'), ("Esperanto", 'eo'), ("Español", 'es'), ('Português', 'pt'), ('Deutsch', 'de'), ('Italiano', 'it')], row=2)
        make_radiogroup(p_language, lang_var, [('Nederlands', 'nl'), ('Русский', 'ru'), ('日本語', 'ja'), ('中文', 'zh'), ('한국어', 'ko')], row=3)

        p_styles = tk.Frame(content_area, bg=H_BG)
        style_toolbar = tk.Frame(p_styles, bg=H_BG)
        style_toolbar.pack(fill='x', pady=(0, 8))
        def style_display_name(name):
            if name.casefold() == 'default':
                return tr('style_default')
            if name.casefold() == 'custom':
                return tr('style_custom')
            return name

        def style_error_text(error):
            message = str(error)
            if message == 'Style names must be 1-40 letters, numbers, spaces, _ or -.':
                return tr('style_error_invalid_name')
            if message == 'The default style is read-only.':
                return tr('style_error_read_only')
            if message == 'Choose a name other than Default.':
                return tr('style_error_choose_name')
            if message == 'The default style cannot be reset.':
                return tr('style_error_default_reset')
            if message == 'That style profile does not exist.':
                return tr('style_error_profile_missing')
            match = re.fullmatch(r'No style named "(.+)" exists\.', message)
            if match:
                return tr('style_error_not_found', name=match.group(1))
            match = re.fullmatch(r'A style named "(.+)" already exists\.', message)
            if match:
                return tr('style_error_exists', name=match.group(1))
            return message

        style_name_var = tk.StringVar(value=style_display_name(ACTIVE_STYLE_NAME))
        style_dirty = [False]
        loading_style = [False]
        style_vars = {}
        style_swatch_widgets = {}
        style_marker_widgets = {}
        style_control_widgets = []
        original_style_colors = {}

        def resolved_style_color(color):
            return get_color(color[6:]) if color.startswith('theme:') else color

        def refresh_style_menu():
            style_menu['menu'].delete(0, 'end')
            for name in style_manager.list_styles():
                style_menu['menu'].add_command(
                    label=style_display_name(name),
                    command=lambda selected=name: select_style_profile(selected),
                )
            style_name_var.set(style_display_name(ACTIVE_STYLE_NAME))

        style_menu = tk.OptionMenu(style_toolbar, style_name_var, style_display_name(ACTIVE_STYLE_NAME))
        style_menu.config(
            bg=TAB_BG, fg=FG, activebackground=SELECT_BG,
            activeforeground=FG, font=('Consolas', 10),
            relief='flat', bd=0, highlightthickness=1,
            highlightbackground=SEP_FG, cursor=HAND_CURSOR,
        )
        style_menu['menu'].config(bg=TAB_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
        style_menu.pack(side='left', padx=(0, 8))

        def style_button(label, command):
            return tk.Button(
                style_toolbar, text=label, command=command,
                bg=TAB_BG, fg=FG, activebackground=SELECT_BG,
                activeforeground=FG, font=('Consolas', 9),
                relief='flat', padx=8, pady=3, cursor=HAND_CURSOR,
                bd=0, highlightthickness=0,
            )

        def mark_style_dirty(*_args):
            if not loading_style[0]:
                style_dirty[0] = True

        def update_style_swatch(element):
            color = style_vars[element]['color'].get().strip()
            if re.fullmatch(r'#[0-9a-fA-F]{6}', color):
                style_swatch_widgets[element].config(bg=color)
            else:
                style_swatch_widgets[element].config(bg=TAB_BG)

        def choose_style_color(element):
            if ACTIVE_STYLE_NAME.casefold() == 'default':
                return
            selected = colorchooser.askcolor(
                color=style_vars[element]['color'].get(),
                parent=dlg,
            )[1]
            if selected:
                style_vars[element]['color'].set(selected)

        styles_scroll_frame = tk.Frame(p_styles, bg=H_BG)
        styles_scroll_frame.pack(fill='both', expand=True)
        styles_canvas = tk.Canvas(styles_scroll_frame, bg=H_BG, highlightthickness=0)
        styles_scrollbar = ttk.Scrollbar(styles_scroll_frame, orient='vertical', command=styles_canvas.yview)
        styles_canvas.configure(yscrollcommand=styles_scrollbar.set)
        styles_scrollbar.pack(side='right', fill='y')
        styles_canvas.pack(side='left', fill='both', expand=True)
        styles_rows = tk.Frame(styles_canvas, bg=H_BG)
        styles_canvas_window = styles_canvas.create_window((0, 0), window=styles_rows, anchor='nw')
        styles_rows.bind(
            '<Configure>',
            lambda event: styles_canvas.configure(scrollregion=styles_canvas.bbox('all')),
        )
        styles_canvas.bind(
            '<Configure>',
            lambda event: styles_canvas.itemconfigure(styles_canvas_window, width=event.width),
        )
        styles_canvas.bind('<MouseWheel>', lambda event: styles_canvas.yview_scroll(int(-event.delta / 120), 'units'))

        headers = (tr('style_element'), tr('style_marker'), tr('style_color'), 'B', 'I', 'U', 'S', tr('style_size'))
        header_columns = (0, 1, 3, 4, 5, 6, 7, 8)
        for label, column in zip(headers, header_columns):
            tk.Label(
                styles_rows, text=label, bg=H_BG, fg=STATUS_FG,
                font=('Consolas', 9, 'bold'), anchor='w',
            ).grid(row=0, column=column, sticky='w', padx=(4, 3), pady=(2, 6))

        for row_index, (element, _label, _marker, _color, _bold, _italic, _underline, _strike) in enumerate(STYLE_ELEMENTS, start=1):
            defaults = ACTIVE_STYLE['elements'][element]
            marker_var = tk.StringVar(value=defaults['marker'])
            color_var = tk.StringVar(value=resolved_style_color(defaults['color']))
            bold_var = tk.BooleanVar(value=defaults['bold'])
            italic_var = tk.BooleanVar(value=defaults['italic'])
            underline_var = tk.BooleanVar(value=defaults['underline'])
            strike_var = tk.BooleanVar(value=defaults['strikethrough'])
            size_var = tk.StringVar(value=str(defaults['font_size']))
            style_vars[element] = {
                'marker': marker_var,
                'color': color_var,
                'bold': bold_var,
                'italic': italic_var,
                'underline': underline_var,
                'strikethrough': strike_var,
                'font_size': size_var,
            }

            tk.Label(
                styles_rows, text=tr(f'style_{element}'), bg=H_BG, fg=FG,
                font=('Consolas', 9), anchor='w', width=15,
            ).grid(row=row_index, column=0, sticky='w', padx=4, pady=2)
            marker_entry = tk.Entry(
                styles_rows, textvariable=marker_var, width=7,
                bg=TAB_BG, fg=FG, insertbackground=FG, relief='flat',
            )
            marker_entry.grid(row=row_index, column=1, sticky='w', padx=3, pady=2)
            style_marker_widgets[element] = marker_entry
            swatch = tk.Frame(styles_rows, bg=color_var.get(), width=18, height=18, cursor=HAND_CURSOR)
            swatch.grid(row=row_index, column=2, padx=(4, 2), pady=2)
            swatch.grid_propagate(False)
            swatch.bind('<Button-1>', lambda event, key=element: choose_style_color(key))
            style_swatch_widgets[element] = swatch
            color_entry = tk.Entry(
                styles_rows, textvariable=color_var, width=9,
                bg=TAB_BG, fg=FG, insertbackground=FG, relief='flat',
            )
            color_entry.grid(row=row_index, column=3, sticky='w', padx=2, pady=2)
            style_control_widgets.append(color_entry)
            color_var.trace_add('write', lambda *_args, key=element: (mark_style_dirty(), update_style_swatch(key)))

            for column, text, variable in (
                (4, 'B', bold_var), (5, 'I', italic_var),
                (6, 'U', underline_var), (7, 'S', strike_var),
            ):
                toggle = tk.Checkbutton(
                    styles_rows, text=text, variable=variable,
                    bg=H_BG, fg=FG, selectcolor=TAB_BG,
                    activebackground=H_BG, activeforeground=FG,
                    font=('Consolas', 8), padx=0, cursor=HAND_CURSOR,
                )
                toggle.grid(row=row_index, column=column, padx=1, pady=1)
                style_control_widgets.append(toggle)

            size_spin = tk.Spinbox(
                styles_rows, from_=0, to=72, textvariable=size_var, width=4,
                bg=TAB_BG, fg=FG, buttonbackground=TAB_BG,
                insertbackground=FG, relief='flat', font=('Consolas', 9),
            )
            size_spin.grid(row=row_index, column=8, sticky='w', padx=(3, 4), pady=2)
            style_control_widgets.append(size_spin)

            for variable in (marker_var, bold_var, italic_var, underline_var, strike_var, size_var):
                variable.trace_add('write', mark_style_dirty)

        def load_style_controls(profile):
            loading_style[0] = True
            for element, *_rest in STYLE_ELEMENTS:
                style = profile['elements'][element]
                controls = style_vars[element]
                controls['marker'].set(style['marker'])
                controls['color'].set(resolved_style_color(style['color']))
                original_style_colors[element] = controls['color'].get()
                controls['bold'].set(style['bold'])
                controls['italic'].set(style['italic'])
                controls['underline'].set(style['underline'])
                controls['strikethrough'].set(style['strikethrough'])
                controls['font_size'].set(style['font_size'])
                update_style_swatch(element)
            style_dirty[0] = False
            loading_style[0] = False
            is_default = ACTIVE_STYLE_NAME.casefold() == 'default'
            for widget in style_control_widgets:
                widget.configure(state='disabled' if is_default else 'normal')
            for element, widget in style_marker_widgets.items():
                widget.configure(state='disabled' if is_default or element == 'text' else 'normal')
            save_style_button.configure(state='disabled' if is_default else 'normal')
            reset_style_button.configure(state='disabled' if is_default else 'normal')
            delete_style_button.configure(state='disabled' if is_default else 'normal')

        def profile_from_controls():
            elements = {}
            for element, *_rest in STYLE_ELEMENTS:
                controls = style_vars[element]
                marker = controls['marker'].get()
                color = controls['color'].get().strip()
                if (element != 'text' and not marker.strip()) or len(marker) > 12:
                    raise ValueError(tr('style_invalid_marker', element=tr(f'style_{element}')))
                if not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
                    raise ValueError(tr('style_invalid_color', element=tr(f'style_{element}')))
                previous_color = ACTIVE_STYLE['elements'][element]['color']
                if original_style_colors[element].casefold() == color.casefold():
                    color = previous_color
                try:
                    font_size = int(controls['font_size'].get())
                except ValueError as error:
                    raise ValueError(tr('style_invalid_size', element=tr(f'style_{element}'))) from error
                if not 0 <= font_size <= 72:
                    raise ValueError(tr('style_invalid_size', element=tr(f'style_{element}')))
                elements[element] = {
                    'marker': '' if element == 'text' else marker,
                    'color': color,
                    'bold': controls['bold'].get(),
                    'italic': controls['italic'].get(),
                    'underline': controls['underline'].get(),
                    'strikethrough': controls['strikethrough'].get(),
                    'font_size': font_size,
                }
            return {'version': 1, 'elements': elements}

        def save_current_style():
            global ACTIVE_STYLE
            try:
                ACTIVE_STYLE = style_manager.save(ACTIVE_STYLE_NAME, profile_from_controls())
            except (ValueError, OSError, tk.TclError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                return False
            style_manager.profile = ACTIVE_STYLE
            style_dirty[0] = False
            save_settings_to_disk()
            apply_active_style()
            return True

        def select_style_profile(name):
            selected_name = name
            if selected_name == ACTIVE_STYLE_NAME:
                return
            if style_dirty[0] and ACTIVE_STYLE_NAME.casefold() != 'default' and not save_current_style():
                style_name_var.set(style_display_name(ACTIVE_STYLE_NAME))
                return
            try:
                activate_style(selected_name)
            except (ValueError, OSError, json.JSONDecodeError, tk.TclError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                refresh_style_menu()
                return
            refresh_style_menu()
            load_style_controls(ACTIVE_STYLE)

        def add_style():
            name = simpledialog.askstring(tr('style_title'), tr('style_new_name'), parent=dlg)
            if not name:
                return
            try:
                style_manager.create(name, style_manager.load('default'))
                activate_style(name)
            except (ValueError, OSError, json.JSONDecodeError, tk.TclError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                return
            refresh_style_menu()
            load_style_controls(ACTIVE_STYLE)

        def delete_active_style():
            if ACTIVE_STYLE_NAME.casefold() == 'default':
                return
            if not messagebox.askyesno(
                tr('style_title'), tr('style_confirm_delete', name=style_display_name(ACTIVE_STYLE_NAME)), parent=dlg,
            ):
                return
            try:
                style_manager.delete(ACTIVE_STYLE_NAME)
                activate_style('default')
            except (ValueError, OSError, json.JSONDecodeError, tk.TclError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                return
            refresh_style_menu()
            load_style_controls(ACTIVE_STYLE)

        def reset_active_style():
            if not messagebox.askyesno(
                tr('style_title'), tr('style_confirm_reset', name=style_display_name(ACTIVE_STYLE_NAME)), parent=dlg,
            ):
                return
            try:
                style_manager.reset(ACTIVE_STYLE_NAME)
            except (ValueError, OSError, tk.TclError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                return
            activate_style(ACTIVE_STYLE_NAME)
            load_style_controls(ACTIVE_STYLE)

        button_bg = '#222222' if theme_preferences == 'dark' else '#ffffff'
        button_fg = '#ffffff' if theme_preferences == 'dark' else '#202020'

        save_style_button = style_button(tr('style_save'), save_current_style)
        save_style_button.config(bg=button_bg, fg=button_fg)
        save_style_button.pack(side='right', padx=(4, 0))

        reset_style_button = style_button(tr('style_reset'), reset_active_style)
        reset_style_button.config(bg=button_bg, fg=button_fg)
        reset_style_button.pack(side='right', padx=(4, 0))

        add_style_button = style_button(tr('style_add'), add_style)
        add_style_button.config(bg=button_bg, fg=button_fg)
        add_style_button.pack(side='right', padx=(4, 0))

        delete_style_button = style_button(tr('style_delete'), delete_active_style)
        delete_style_button.config(bg=button_bg, fg=button_fg)
        delete_style_button.pack(side='right', padx=(4, 0))

        refresh_style_menu()
        load_style_controls(ACTIVE_STYLE)

        pages = [p_general, p_language, p_styles]
        show_page(0)

        tk.Frame(dlg, bg=SEP_FG, height=1).pack(fill='x')

        btn_bar = tk.Frame(dlg, bg=H_BG, pady=12, padx=16)
        btn_bar.pack(fill='x')

        def apply_settings():
            global current_language
            if style_dirty[0] and ACTIVE_STYLE_NAME.casefold() != 'default' and not save_current_style():
                return
            try:
                activate_style(ACTIVE_STYLE_NAME)
            except (ValueError, OSError, json.JSONDecodeError) as error:
                messagebox.showerror(tr('style_title'), style_error_text(error), parent=dlg)
                return
            current_language = lang_var.get()
            SETTINGS['font_family'] = font_fam_var.get()
            SETTINGS['font_size'] = font_size_var.get()
            SETTINGS['line_wrap'] = wrap_var.get()
            SETTINGS['padding'] = padding_var.get()
            SETTINGS['show_status'] = status_var.get()
            SETTINGS['show_wordcount'] = wcount_var.get()
            SETTINGS['win_width'] = win_w_var.get()
            SETTINGS['win_height'] = win_h_var.get()

            save_settings_to_disk()
            update_font_definitions()
            sidebar_title_lbl.config(text=tr('sidebar_explorer')) # fixes a bug where the sidebar's empty name would stay in the same language even when we changed the language

            if SETTINGS['show_status']:
                status_bar.pack(side='bottom', fill='x')
            else:
                status_bar.pack_forget()

            if SETTINGS['show_wordcount']:
                status_words.pack(side='right')
            else:
                status_words.pack_forget()

            for t in tab_bar.tabs:
                t.text.config(
                    font=t._scaled_font(FONT_BODY),
                    wrap=SETTINGS['line_wrap'],
                    padx=SETTINGS['padding'],
                )
                t._configure_tags()
                t.highlight_markdown()

            rebuild_menu()
            _on_settings_close()

        button_bg = '#222222' if theme_preferences == 'dark' else '#ffffff'
        button_fg = '#ffffff' if theme_preferences == 'dark' else '#202020'

        tk.Button(
            btn_bar, text=tr('settings_apply'), command=apply_settings,
            bg=button_bg, fg=button_fg, activebackground=button_bg,
            activeforeground=button_fg, font=('Consolas', 10, 'bold'),
            relief='flat', padx=16, pady=4, cursor=HAND_CURSOR,
            bd=0, highlightthickness=0,
        ).pack(side='right', padx=(8, 0))

        tk.Button(
            btn_bar, text=tr('settings_cancel'), command=_on_settings_close,
            bg=button_bg, fg=button_fg, activebackground=button_bg,
            activeforeground=button_fg, font=('Consolas', 10),
            relief='flat', padx=16, pady=4, cursor=HAND_CURSOR,
            bd=0, highlightthickness=0,
        ).pack(side='right')
        return 'break'

    rebuild_menu() # [Build initial menu bar structure]
    restore_pinned_tabs() # [Reopen saved pinned documents]
    win.mainloop() # [Run main Tkinter event loop]