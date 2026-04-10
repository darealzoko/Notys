import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import re
import platform
from PIL import Image, ImageTk

def resource_path(relative_path):
    """
    Transforme un chemin relatif en chemin absolu pour PyInstaller.
    Fonctionne pour les fichiers individuels et les dossiers.
    """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si on n'est pas compilé, on utilise le chemin normal du projet
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


try:
    from tkinterdnd2 import Tk as DnDTk, DND_FILES
    DND_AVAILABLE = True
except Exception:
    DnDTk = None
    DND_FILES = None
    DND_AVAILABLE = False


# ── Langues ───────────────────────────────────────────────────────────────────
TRANSLATIONS = {
    'fr': {
        # Menu Fichier
        'menu_file':              "Fichier",
        'menu_new_window':        "Nouvelle fenêtre",
        'menu_new_tab':           "Nouvel onglet",
        'menu_reopen_tab':        "Rouvrir l'onglet fermé",
        'menu_open':              "Ouvrir…",
        'menu_close_tab':         "Fermer l'onglet",
        'menu_save':              "Enregistrer",
        'menu_save_all':          "Tout enregistrer",
        'menu_save_as':           "Enregistrer sous…",
        # Menu Édition
        'menu_edit':              "Édition",
        'menu_undo':              "Annuler",
        'menu_redo':              "Rétablir",
        'menu_find':              "Rechercher…",
        # Menu Fenêtre
        'menu_window':            "Fenêtre",
        'menu_minimize':          "Réduire",
        # Menu Paramètres
        'menu_settings':          "Paramètres",
        'menu_open_settings':     "Ouvrir les paramètres…",
        # Fenêtre paramètres
        'settings_title':         "Paramètres",
        'settings_apply':         "Appliquer",
        'settings_cancel':        "Annuler",
        # Sections paramètres
        'section_language':       "🌐  Langue",
        'section_appearance':     "🎨  Apparence",
        'section_editor':         "✏️  Éditeur",
        'section_interface':      "🖥️  Interface",
        # Langue
        'settings_language':      "Langue de l'interface",
        # Apparence
        'settings_theme':         "Thème",
        'theme_dark':             "Sombre",
        'theme_light':            "Clair",
        # Éditeur
        'settings_font_family':   "Police",
        'settings_font_size':     "Taille de police",
        'settings_line_height':   "Hauteur de ligne",
        'settings_line_wrap':     "Retour à la ligne",
        'wrap_word':              "Par mot",
        'wrap_char':              "Par caractère",
        'wrap_none':              "Aucun",
        'settings_padding':       "Marges latérales",
        # Interface
        'settings_show_status':   "Barre de statut",
        'settings_show_wordcount':"Compteur de mots",
        'settings_win_size':      "Taille de fenêtre par défaut",
        'on':                     "Activé",
        'off':                    "Désactivé",
        # Dialogue non sauvegardé
        'dlg_save_title':         "",
        'dlg_save_msg':           "Voulez-vous enregistrer les modifications\napportées à \"{name}\" ?",
        'dlg_save_sub':           "Vos modifications seront perdues si vous ne les enregistrez pas.",
        'dlg_dont_save':          "Ne pas enregistrer",
        'dlg_cancel':             "Annuler",
        'dlg_save':               "Enregistrer…",
        # Barre de statut
        'status_words_one':       "mot",
        'status_words_many':      "mots",
        'status_untitled':        "Sans titre",
        # Barre de recherche
        'search_no_results':      "Aucun résultat",
        # DnD warning
        'dnd_title':              "Drag & Drop indisponible",
        'dnd_msg': (
            "Le glisser-déposer n'est pas disponible :\n"
            "tkinterdnd2 est introuvable.\n\n"
            "Installez-le avec :\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Redémarrez ensuite Notys."
        ),
        # Onglet sans titre
        'untitled':               "Sans titre",
    },
    'en': {
        # File menu
        'menu_file':              "File",
        'menu_new_window':        "New Window",
        'menu_new_tab':           "New Tab",
        'menu_reopen_tab':        "Reopen Closed Tab",
        'menu_open':              "Open…",
        'menu_close_tab':         "Close Tab",
        'menu_save':              "Save",
        'menu_save_all':          "Save All",
        'menu_save_as':           "Save As…",
        # Edit menu
        'menu_edit':              "Edit",
        'menu_undo':              "Undo",
        'menu_redo':              "Redo",
        'menu_find':              "Find…",
        # Window menu
        'menu_window':            "Window",
        'menu_minimize':          "Minimize",
        # Settings menu
        'menu_settings':          "Settings",
        'menu_open_settings':     "Open Settings…",
        # Settings window
        'settings_title':         "Settings",
        'settings_apply':         "Apply",
        'settings_cancel':        "Cancel",
        # Settings sections
        'section_language':       "🌐  Language",
        'section_appearance':     "🎨  Appearance",
        'section_editor':         "✏️  Editor",
        'section_interface':      "🖥️  Interface",
        # Language
        'settings_language':      "Interface language",
        # Appearance
        'settings_theme':         "Theme",
        'theme_dark':             "Dark",
        'theme_light':            "Light",
        # Editor
        'settings_font_family':   "Font",
        'settings_font_size':     "Font size",
        'settings_line_height':   "Line height",
        'settings_line_wrap':     "Line wrap",
        'wrap_word':              "By word",
        'wrap_char':              "By character",
        'wrap_none':              "None",
        'settings_padding':       "Side margins",
        # Interface
        'settings_show_status':   "Status bar",
        'settings_show_wordcount':"Word counter",
        'settings_win_size':      "Default window size",
        'on':                     "On",
        'off':                    "Off",
        # Unsaved dialog
        'dlg_save_title':         "",
        'dlg_save_msg':           "Do you want to save the changes\nmade to \"{name}\"?",
        'dlg_save_sub':           "Your changes will be lost if you don't save them.",
        'dlg_dont_save':          "Don't Save",
        'dlg_cancel':             "Cancel",
        'dlg_save':               "Save…",
        # Status bar
        'status_words_one':       "word",
        'status_words_many':      "words",
        'status_untitled':        "Untitled",
        # Search bar
        'search_no_results':      "No results",
        # DnD warning
        'dnd_title':              "Drag & Drop Unavailable",
        'dnd_msg': (
            "Drag & drop support is not available:\n"
            "tkinterdnd2 was not found.\n\n"
            "Install it with:\n"
            "  python -m pip install tkinterdnd2\n\n"
            "Then restart Notys."
        ),
        # Untitled tab
        'untitled':               "Untitled",
    },
}

current_language = 'en'

# ── Paramètres utilisateur ────────────────────────────────────────────────────
SETTINGS = {
    'font_family':    'Consolas',
    'font_size':      18,
    'line_wrap':      'word',    # 'word', 'char', 'none'
    'padding':        40,        # padx de l'éditeur
    'show_status':    True,
    'show_wordcount': True,
    'win_width':      900,
    'win_height':     650,
}

def tr(key, **kwargs):
    """Retourne la chaîne traduite pour la langue courante."""
    text = TRANSLATIONS[current_language].get(key, TRANSLATIONS['en'].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text

# ── Couleurs ──────────────────────────────────────────────────────────────────
THEMES = {
    'dark': {
        'BG': "#1e1e1e",
        'FG': "#d4d4d4",
        'CURSOR_CLR': "#ffffff",
        'SELECT_BG': "#264f78",
        'STATUS_BG': "#252526",
        'STATUS_FG': "#858585",
        'TAB_BG': "#2d2d2d",
        'TAB_ACTIVE': "#1e1e1e",
        'TAB_FG': "#858585",
        'TAB_FG_ACT': "#ffffff",
        'C_H1': "#39BBD8", 'C_H2': "#39BBD8", 'C_H3': "#39BBD8", 'C_H4': "#39BBD8",
        'C_CODE': "#DE7316", 'C_BOLD': "#ffffff", 'C_ITALIC': "#c8c8c8",
        'C_LIST': "#BB00FF", 'C_QUOTE': "#6A9955", 'C_LINK': "#4ec9b0", 'C_HR': "#555555",
        'C_UNDERLINE': "#ffffff", 'C_STRIKE': "#c8c8c8"
    },
    'light': {
        'BG': "#ffffff",
        'FG': "#000000",
        'CURSOR_CLR': "#000000",
        'SELECT_BG': "#add8e6",
        'STATUS_BG': "#f0f0f0",
        'STATUS_FG': "#666666",
        'TAB_BG': "#e0e0e0",
        'TAB_ACTIVE': "#ffffff",
        'TAB_FG': "#666666",
        'TAB_FG_ACT': "#000000",
        'C_H1': "#1e90ff", 'C_H2': "#1e90ff", 'C_H3': "#1e90ff", 'C_H4': "#1e90ff",
        'C_CODE': "#ff4500", 'C_BOLD': "#000000", 'C_ITALIC': "#666666",
        'C_LIST': "#8a2be2", 'C_QUOTE': "#228b22", 'C_LINK': "#006400", 'C_HR': "#cccccc",
        'C_UNDERLINE': "#000000", 'C_STRIKE': "#666666"
    }
}

current_theme = 'dark'

def get_color(key):
    return THEMES[current_theme][key]

BG         = get_color('BG')
FG         = get_color('FG')
CURSOR_CLR = get_color('CURSOR_CLR')
SELECT_BG  = get_color('SELECT_BG')
STATUS_BG  = get_color('STATUS_BG')
STATUS_FG  = get_color('STATUS_FG')
TAB_BG     = get_color('TAB_BG')
TAB_ACTIVE = get_color('TAB_ACTIVE')
TAB_FG     = get_color('TAB_FG')
TAB_FG_ACT = get_color('TAB_FG_ACT')

C_H1    = get_color('C_H1'); C_H2 = get_color('C_H2'); C_H3 = get_color('C_H3'); C_H4 = get_color('C_H4')
C_CODE  = get_color('C_CODE'); C_BOLD = get_color('C_BOLD'); C_ITALIC = get_color('C_ITALIC')
C_LIST  = get_color('C_LIST'); C_QUOTE = get_color('C_QUOTE'); C_LINK = get_color('C_LINK'); C_HR = get_color('C_HR')
C_UNDERLINE = get_color('C_UNDERLINE'); C_STRIKE = get_color('C_STRIKE')

FONT_BODY   = ('Consolas', 18)
FONT_H1     = ('Consolas', 34, 'bold')
FONT_H2     = ('Consolas', 28, 'bold')
FONT_H3     = ('Consolas', 24, 'bold')
FONT_H4     = ('Consolas', 20, 'bold')
FONT_CODE   = ('Courier', 17)
FONT_BOLD   = ('Consolas', 18, 'bold')
FONT_ITALIC = ('Consolas', 18, 'italic')
FONT_TAB    = ('Arial', 14)

# Couleurs nommées pour &^couleur texte^&
COLOR_NAMES = {
    'red':    '#ff5555', 'rouge':  '#ff5555',
    'green':  '#50fa7b', 'vert':   '#50fa7b',
    'light_blue':   '#8be9fd', 'bleu_clair':   '#8be9fd',
    'blue': "#1E7BE4", 'bleu': '#1E7BE4',
    'dark_blue': "#091095", 'bleu_foncé': '#091095',
    'yellow': "#ebfb40", 'jaune':  '#ebfb40',
    'orange': "#ffa03b",
    'pink':   '#ff79c6', 'rose':   '#ff79c6',
    'purple': "#8f41fc", 'violet': '#8f41fc',
    'white':  '#ffffff', 'blanc':  '#ffffff',
    'gray':   '#858585', 'grey':   '#858585', 'gris': '#858585',
    'cyan':   '#8be9fd',
    'highlight_yellow': '#ffff00',
}

ALL_TAGS = ('h1','h2','h3','h4','code','bold','italic','underline','strike','list','quote','link','hr')

def normalize_color(color):
    if isinstance(color, str) and color.startswith('#') and len(color) == 9:
        return color[:7]
    return color


def get_contrast_color(bg_hex):
    bg_hex = normalize_color(bg_hex)
    if not re.match(r'^#[0-9a-fA-F]{6}$', bg_hex):
        return '#000000'
    r = int(bg_hex[1:3], 16)
    g = int(bg_hex[3:5], 16)
    b = int(bg_hex[5:7], 16)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return '#000000' if lum > 186 else '#ffffff'
# ── Fenêtre principale ────────────────────────────────────────────────────────
if __name__ == '__main__':
    # ── Fenêtre principale ────────────────────────────────────────────────────────
    TkClass = DnDTk if DND_AVAILABLE else tk.Tk
    win = TkClass()
    win.title("Notys")
    win.configure(bg=BG)
    win.geometry("900x650")

    # Indentez tout le reste du code ici, y compris les classes Tab et TabBar si elles utilisent win,
    # les fonctions, le layout, les raccourcis, le menu, l'init et win.mainloop()

    BG         = get_color('BG')
    FG         = get_color('FG')
    CURSOR_CLR = get_color('CURSOR_CLR')
    SELECT_BG  = get_color('SELECT_BG')
    STATUS_BG  = get_color('STATUS_BG')
    STATUS_FG  = get_color('STATUS_FG')
    TAB_BG     = get_color('TAB_BG')
    TAB_ACTIVE = get_color('TAB_ACTIVE')
    TAB_FG     = get_color('TAB_FG')
    TAB_FG_ACT = get_color('TAB_FG_ACT')

    C_H1    = get_color('C_H1'); C_H2 = get_color('C_H2'); C_H3 = get_color('C_H3'); C_H4 = get_color('C_H4')
    C_CODE  = get_color('C_CODE'); C_BOLD = get_color('C_BOLD'); C_ITALIC = get_color('C_ITALIC')
    C_LIST  = get_color('C_LIST'); C_QUOTE = get_color('C_QUOTE'); C_LINK = get_color('C_LINK'); C_HR = get_color('C_HR')
    C_UNDERLINE = get_color('C_UNDERLINE'); C_STRIKE = get_color('C_STRIKE')

    FONT_BODY   = ('Consolas', 18)
    FONT_H1     = ('Consolas', 34, 'bold')
    FONT_H2     = ('Consolas', 28, 'bold')
    FONT_H3     = ('Consolas', 24, 'bold')
    FONT_H4     = ('Consolas', 20, 'bold')
    FONT_CODE   = ('Courier', 17)
    FONT_BOLD   = ('Consolas', 18, 'bold')
    FONT_ITALIC = ('Consolas', 18, 'italic')
    FONT_TAB    = ('Arial', 14)

    # Couleurs nommées pour $@couleur texte@$
    COLOR_NAMES = {
        'red':    '#ff5555', 'rouge':  '#ff5555',
        'green':  '#50fa7b', 'vert':   '#50fa7b',
        'light_blue':   '#8be9fd', 'bleu_clair':   '#8be9fd',
        'blue': "#1E7BE4", 'bleu': '#1E7BE4',
        'dark_blue': "#091095", 'bleu_foncé': '#091095',
        'yellow': "#ebfb40", 'jaune':  '#ebfb40',
        'orange': "#ffa03b",
        'pink':   '#ff79c6', 'rose':   '#ff79c6',
        'purple': "#8f41fc", 'violet': '#8f41fc',
        'white':  '#ffffff', 'blanc':  '#ffffff',
        'gray':   '#858585', 'grey':   '#858585', 'gris': '#858585',
        'cyan':   '#8be9fd',
        'highlight_yellow': '#ffff00',
    }

    ALL_TAGS = ('h1','h2','h3','h4','code','bold','italic','underline','strike','list','quote','link','hr')

    # ══════════════════════════════════════════════════════════════════════════════
    # Classe Tab
    # ══════════════════════════════════════════════════════════════════════════════
    class Tab:
        _counter = 0

        def __init__(self, file_path=None):
            Tab._counter += 1
            self.id            = Tab._counter
            self.file_path     = file_path
            self.highlight_job = None
            # Liste des matches &^color text^& : (match_start, match_end, color_hex)
            self._color_matches = []
            self.font_scale = 1.0

            self.frame = tk.Frame(editor_area, bg=BG)

            self.sb = tk.Scrollbar(self.frame, bg=BG, troughcolor=BG, bd=0, width=8)
            self.sb.pack(side='right', fill='y')

            self.text = tk.Text(
                self.frame,
                bg=BG, fg=FG,
                insertbackground=CURSOR_CLR,
                selectbackground=SELECT_BG,
                bd=0, highlightthickness=0, relief='flat',
                font=self._scaled_font(FONT_BODY),
                padx=40, pady=30,
                spacing1=2, spacing3=4,
                wrap='word',
                undo=True,
                yscrollcommand=self.sb.set,
            )
            self.text.pack(fill='both', expand=True)
            self.sb.config(command=self.text.yview)

            # Tag pour masquer les symboles &^..^& (couleur = fond = invisible)
            self.text.tag_configure('hidden', foreground=BG, font=self._scaled_font(('Andale Mono', 1)), elide=True)

            self._configure_tags()
            self.text.bind('<KeyRelease>', self._on_key)
            self.text.bind('<ButtonRelease>', self._on_cursor_move)
            self.text.bind('<Tab>', self._handle_tab)

            # Supprimer la ligne : Cmd+Backspace (Mac) / Alt+Backspace (Win)
            if is_macos:
                self.text.bind('<Command-BackSpace>', self._delete_line)
            else:
                self.text.bind('<Alt-BackSpace>', self._delete_line)

            # Supprimer le mot précédent : Option+Backspace (Mac) / Ctrl+Backspace (Win)
            if is_macos:
                self.text.bind('<Option-BackSpace>', self._delete_word_before)
            else:
                self.text.bind('<Control-BackSpace>', self._delete_word_before)

            # Ctrl+Tab / Ctrl+Shift+Tab : onglet suivant / précédent
            self.text.bind('<Control-Tab>',       lambda e: _next_tab())
            self.text.bind('<Control-Shift-Tab>', lambda e: _prev_tab())

            # Ctrl+Alt+S / Cmd+Option+S : tout sauvegarder
            if is_macos:
                self.text.bind('<Command-Option-s>', lambda e: save_all())
            else:
                self.text.bind('<Control-Alt-s>', lambda e: save_all())

        def update_theme(self):
            self.frame.config(bg=BG)
            self.text.config(
                bg=BG, fg=FG,
                insertbackground=CURSOR_CLR,
                selectbackground=SELECT_BG
            )
            self.sb.config(bg=BG, troughcolor=BG)
            self._configure_tags()
            self.highlight_markdown()

        def _configure_tags(self):
            t = self.text
            t.tag_configure('h1',     foreground=C_H1,    font=self._scaled_font(FONT_H1))
            t.tag_configure('h2',     foreground=C_H2,    font=self._scaled_font(FONT_H2))
            t.tag_configure('h3',     foreground=C_H3,    font=self._scaled_font(FONT_H3))
            t.tag_configure('h4',     foreground=C_H4,    font=self._scaled_font(FONT_H4))
            t.tag_configure('code',   foreground=C_CODE,  font=self._scaled_font(FONT_CODE))
            t.tag_configure('bold',   foreground=C_BOLD,  font=self._scaled_font(FONT_BOLD))
            t.tag_configure('italic', foreground=C_ITALIC, font=self._scaled_font(FONT_ITALIC))
            t.tag_configure('underline', foreground=C_UNDERLINE, underline=True)
            t.tag_configure('strike', foreground=C_STRIKE, overstrike=True)
            t.tag_configure('list',   foreground=C_LIST)
            t.tag_configure('quote',  foreground=C_QUOTE, font=self._scaled_font(('Andale Mono', 12, 'italic')))
            t.tag_configure('link',   foreground=C_LINK,  underline=True)
            t.tag_configure('hr',     foreground=C_HR)
            # t.tag_configure('highlight', ...) déplacé dans highlight_markdown

        def _handle_tab(self, event):
            self.text.insert('insert', '    ')
            return 'break'

        def _scaled_font(self, font_tuple):
            if not isinstance(font_tuple, tuple) or len(font_tuple) < 2:
                return font_tuple
            name = font_tuple[0]
            size = font_tuple[1]
            rest = font_tuple[2:]
            scaled_size = max(2, int(round(size * self.font_scale)))
            return (name, scaled_size, *rest)

        def set_zoom(self, zoom):
            self.font_scale = max(0.5, min(3.0, zoom))
            self.text.config(font=self._scaled_font(FONT_BODY))
            self._configure_tags()
            self.highlight_markdown()

        def _delete_line(self, event=None):
            insert = self.text.index('insert')
            line = insert.split('.')[0]
            self.text.delete(f'{line}.0', f'{line}.end+1c')
            return 'break'

        def _delete_word_before(self, event=None):
            insert = self.text.index('insert')
            word_start = self.text.index(f'{insert} -1c wordstart')
            if self.text.compare(word_start, '<', insert):
                self.text.delete(word_start, insert)
            return 'break'

        def _on_key(self, event=None):
            tab_bar.refresh()  # Rafraîchir le TabBar pour afficher/masquer le point de modification
            self.schedule_highlight()
            update_status()

        def _on_cursor_move(self, event=None):
            """Déclenché aussi au clic souris pour rafraîchir la visibilité des symboles."""
            self._apply_symbol_visibility()

        def schedule_highlight(self):
            if self.highlight_job:
                win.after_cancel(self.highlight_job)
            self.highlight_job = win.after(120, self.highlight_markdown)

        # ── Coloration principale ─────────────────────────────────────────────────
        def highlight_markdown(self):
            t = self.text
            for tag in ALL_TAGS:
                t.tag_remove(tag, '1.0', 'end')
            t.tag_remove('highlight', '1.0', 'end')
            for tag in t.tag_names():
                if tag.startswith('highlight_'):
                    t.tag_remove(tag, '1.0', 'end')
            
            # Configure highlight tag with a fixed readable text color
            highlight_bg = normalize_color(COLOR_NAMES.get('highlight_yellow', '#ffff00'))
            t.tag_configure('highlight', background='#ffff00', foreground='#000000')

            content = t.get('1.0', 'end-1c')
            lines   = content.splitlines()

            # Blocs ```
            code_line_ranges = []
            in_block = False; block_start = None
            for i, line in enumerate(lines, start=1):
                if line.strip().startswith('```'):
                    if not in_block:
                        in_block = True; block_start = i
                    else:
                        code_line_ranges.append((block_start, i))
                        in_block = False
            if in_block and block_start:
                code_line_ranges.append((block_start, len(lines)))

            code_line_set = set()
            for s, e in code_line_ranges:
                for ln in range(s, e + 1):
                    code_line_set.add(ln)
                t.tag_add('code', f'{s}.0', f'{e}.end')

            # Lignes
            for i, line in enumerate(lines, start=1):
                if i in code_line_set:
                    continue
                ls, le = f'{i}.0', f'{i}.end'
                if   line.startswith('####'): t.tag_add('h4', ls, le)
                elif line.startswith('###'):  t.tag_add('h3', ls, le)
                elif line.startswith('##'):   t.tag_add('h2', ls, le)
                elif line.startswith('#'):    t.tag_add('h1', ls, le)
                elif re.match(r'^>\s', line): t.tag_add('quote', ls, le)
                elif re.match(r'^(-{3,}|\*{3,}|_{3,})\s*$', line): t.tag_add('hr', ls, le)
                elif re.match(r'^\s*[-*+]\s', line): t.tag_add('list', ls, le)
                elif re.match(r'^\s*\d+\.\s', line): t.tag_add('list', ls, le)

            # Offsets inline
            line_offsets = []
            off = 0
            for line in lines:
                line_offsets.append(off)
                off += len(line) + 1

            def in_code_block(cs, ce):
                for s, e in code_line_ranges:
                    bs = line_offsets[s - 1]
                    be = line_offsets[e - 1] + len(lines[e - 1])
                    if cs >= bs and ce <= be:
                        return True
                return False

            for m in re.finditer(r'`([^`\n]+?)`', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('code', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
            for m in re.finditer(r'\*\*(.+?)\*\*', content, re.DOTALL):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('bold', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
            for m in re.finditer(r'(?<!\*)\*([^*\n]+?)\*(?!\*)|_([^_\n]+?)_', content):
                grp = m.group(1) or m.group(2)
                si  = m.start() + m.group(0).index(grp)
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('italic', f'1.0+{si}c', f'1.0+{si + len(grp)}c')
            for m in re.finditer(r'-\:(.+?)\:-', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('underline', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
            for m in re.finditer(r'~~(.+?)~~', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('strike', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
            for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('link', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')

            # ── &^couleur texte^& ─────────────────────────────────────────────────
            self._color_matches = []
            self._syntax_matches = []

            # Supprimer anciens tags couleur custom
            for tag in t.tag_names():
                if tag.startswith('clr_'):
                    t.tag_remove(tag, '1.0', 'end')

            for m in re.finditer(r'&\^(\w+)\s(.*?)\^&', content, re.DOTALL):
                color_name = m.group(1).lower()
                color_hex  = COLOR_NAMES.get(color_name, None)
                if not color_hex:
                    # Tenter hex direct (#rrggbb)
                    if re.match(r'^#[0-9a-fA-F]{6}$', color_name):
                        color_hex = color_name
                    else:
                        continue

                tag_name = f'clr_{color_name}_{self.id}'
                t.tag_configure(tag_name, foreground=color_hex, font=self._scaled_font(FONT_BODY))

                # Positions des différentes parties
                full_start  = m.start()        # position de "$@"
                color_end   = m.start(2)       # après "couleur "
                text_start  = m.start(2)       # début du texte coloré
                text_end    = m.end(2)         # fin du texte coloré
                suffix_end  = m.end()          # après "@$"

                # Colorer le texte intérieur
                t.tag_add(tag_name,
                        f'1.0+{text_start}c',
                        f'1.0+{text_end}c')

                # Mémoriser les spans des symboles : "&^couleur " et "^&"
                prefix_span = (full_start, color_end)   # "&^couleur "
                suffix_span = (text_end,  suffix_end)   # "@$"

                self._color_matches.append({
                    'full_start':  full_start,
                    'full_end':    suffix_end,
                    'prefix_span': prefix_span,
                    'suffix_span': suffix_span,
                    'text_start':  text_start,
                    'text_end':    text_end,
                })

            for m in re.finditer(r'\*\*(.+?)\*\*', content, re.DOTALL):
                t.tag_add('bold', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                self._syntax_matches.append({
                    'full_start': m.start(),
                    'full_end': m.end(),
                    'prefix_span': (m.start(), m.start(1)),
                    'suffix_span': (m.end(1), m.end()),
                })

            for m in re.finditer(r'(?<!\*)\*([^*\n]+?)\*(?!\*)|_([^_\n]+?)_', content):
                grp = m.group(1) or m.group(2)
                si  = m.start() + m.group(0).index(grp)
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('italic', f'1.0+{si}c', f'1.0+{si + len(grp)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), si),
                        'suffix_span': (si + len(grp), m.end()),
                    })

            for m in re.finditer(r'-\:(.+?)\:-', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('underline', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            for m in re.finditer(r'~~(.+?)~~', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('strike', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
                    self._syntax_matches.append({
                        'full_start': m.start(),
                        'full_end': m.end(),
                        'prefix_span': (m.start(), m.start(1)),
                        'suffix_span': (m.end(1), m.end()),
                    })

            for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('link', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')

            # ── ==text à surligner== ──────────────────────────────────────────────
            for m in re.finditer(r'==([^:]+?)(?::(.+?))?==', content):
                if not in_code_block(m.start(), m.end()):
                    color_name = m.group(1).lower()
                    text = m.group(2) if m.group(2) else m.group(1)
                    color_hex = COLOR_NAMES.get(color_name, COLOR_NAMES.get('yellow', '#ffff00'))
                    
                    if m.group(2):
                        # ==color:text==
                        text_start = m.start(2)
                        text_end = m.end(2)
                        prefix_end = m.start(2)
                        suffix_start = m.end(2)
                    else:
                        # ==text==
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

        # ── Masquage Obsidian-style ───────────────────────────────────────────────
        def _apply_symbol_visibility(self):
            t = self.text
            t.tag_remove('hidden', '1.0', 'end')

            # Position curseur en offset caractère
            try:
                cursor_idx = t.index('insert')
            except tk.TclError:
                return
            cursor_line, cursor_col = map(int, cursor_idx.split('.'))

            content = t.get('1.0', 'end-1c')
            lines   = content.splitlines(keepends=True)
            cursor_offset = sum(len(l) for l in lines[:cursor_line - 1]) + cursor_col

            for match in self._color_matches + getattr(self, '_syntax_matches', []):
                full_start = match['full_start']
                full_end   = match['full_end']

                # Le curseur est-il dans ce bloc ?
                cursor_inside = full_start <= cursor_offset <= full_end

                if not cursor_inside:
                    ps, pe = match['prefix_span']
                    ss, se = match['suffix_span']
                    t.tag_add('hidden', f'1.0+{ps}c', f'1.0+{pe}c')
                    t.tag_add('hidden', f'1.0+{ss}c', f'1.0+{se}c')
                # Sinon : tout est visible (les tags restent, 'hidden' non appliqué)

        @property
        def name(self):
            return os.path.basename(self.file_path) if self.file_path else tr('untitled')

        @property
        def is_modified(self):
            # Utiliser le système d'undo du Text widget pour détecter les modifications
            return self.text.edit_modified()

        @property
        def label(self):
            return self.name + (" ●" if self.is_modified else "")

        def set_modified(self, val):
            # Utiliser le système d'undo du Text widget
            self.text.edit_modified(val)
            tab_bar.refresh()

        def get_content(self):
            return self.text.get('1.0', 'end-1c')

        def set_content(self, content):
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', content)
            self.text.edit_modified(False)  # Réinitialiser l'état d'undo après avoir défini le contenu
            self.highlight_markdown()

        def show(self):
            self.frame.pack(fill='both', expand=True)
            self.text.focus_set()

        def hide(self):
            self.frame.pack_forget()


    # ══════════════════════════════════════════════════════════════════════════════
    # Classe TabBar
    # ══════════════════════════════════════════════════════════════════════════════
    class TabBar:
        def __init__(self, parent):
            self.frame = tk.Frame(parent, bg=TAB_BG, height=36)
            self.frame.pack(fill='x', side='top')
            self.frame.pack_propagate(False)

            self.tabs   = []
            self.active = None
            self._btns  = {}

            # --- CHARGEMENT DE VOS IMAGES ---
            # On utilise resource_path pour que PyInstaller les trouve
            try:
                # Charger et redimensionner l'icône Dark Mode (ex: un soleil)
                img_dark = Image.open(resource_path("assets/icons/dark.png"))
                img_dark = img_dark.resize((20, 20), Image.Resampling.LANCZOS)
                self.dark_icon = ImageTk.PhotoImage(img_dark, master=parent)

                # Charger et redimensionner l'icône Light Mode (ex: une lune)
                img_light = Image.open(resource_path("assets/icons/light.png"))
                img_light = img_light.resize((20, 20), Image.Resampling.LANCZOS)
                self.light_icon = ImageTk.PhotoImage(img_light, master=parent)
            except Exception as e:
                print(f"Erreur chargement icônes : {e}")
                # Fallback simple si image manquante pour éviter le crash
                self.dark_icon = None
                self.light_icon = None

            self.btn_new = tk.Label(
                self.frame, text=" + ", bg=TAB_BG, fg=TAB_FG,
                font=FONT_TAB, cursor='hand2', padx=6
            )
            self.btn_new.pack(side='left', fill='y')
            self.btn_new.bind('<Button-1>', lambda e: new_tab())

            # Theme button on the right
            self.theme_button = tk.Label(
                self.frame, image=self.dark_icon, bg=TAB_BG, fg=TAB_FG,
                font=FONT_TAB, cursor='hand2', padx=6
            )
            self.theme_button.pack(side='right', fill='y')
            self.theme_button.bind('<Button-1>', self.toggle_theme)

        def toggle_theme(self, event=None):
            global current_theme, BG, FG, CURSOR_CLR, SELECT_BG, STATUS_BG, STATUS_FG, TAB_BG, TAB_ACTIVE, TAB_FG, TAB_FG_ACT
            global C_H1, C_H2, C_H3, C_H4, C_CODE, C_BOLD, C_ITALIC, C_LIST, C_QUOTE, C_LINK, C_HR

            themes = ['dark', 'light']
            current_index = themes.index(current_theme) if current_theme in themes else 0
            next_index = (current_index + 1) % len(themes)
            current_theme = themes[next_index]

            BG         = THEMES[current_theme]['BG']
            FG         = THEMES[current_theme]['FG']
            CURSOR_CLR = THEMES[current_theme]['CURSOR_CLR']
            SELECT_BG  = THEMES[current_theme]['SELECT_BG']
            STATUS_BG  = THEMES[current_theme]['STATUS_BG']
            STATUS_FG  = THEMES[current_theme]['STATUS_FG']
            TAB_BG     = THEMES[current_theme]['TAB_BG']
            TAB_ACTIVE = THEMES[current_theme]['TAB_ACTIVE']
            TAB_FG     = THEMES[current_theme]['TAB_FG']
            TAB_FG_ACT = THEMES[current_theme]['TAB_FG_ACT']
            C_H1    = THEMES[current_theme]['C_H1']
            C_H2    = THEMES[current_theme]['C_H2']
            C_H3    = THEMES[current_theme]['C_H3']
            C_H4    = THEMES[current_theme]['C_H4']
            C_CODE  = THEMES[current_theme]['C_CODE']
            C_BOLD  = THEMES[current_theme]['C_BOLD']
            C_ITALIC = THEMES[current_theme]['C_ITALIC']
            C_LIST  = THEMES[current_theme]['C_LIST']
            C_QUOTE  = THEMES[current_theme]['C_QUOTE']
            C_LINK   = THEMES[current_theme]['C_LINK']
            C_HR     = THEMES[current_theme]['C_HR']

            # Update UI colors
            self.update_theme()
            for tab in self.tabs:
                tab.update_theme()
            status_bar.config(bg=STATUS_BG)
            status_file.config(bg=STATUS_BG, fg=STATUS_FG)
            status_pos.config(bg=STATUS_BG, fg=STATUS_FG)
            status_words.config(bg=STATUS_BG, fg=STATUS_FG)
            win.config(bg=BG)
            editor_area.config(bg=BG)
            menubar.config(bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)

            # Update button icon
            self.theme_button.config(image=self.dark_icon if current_theme == 'dark' else self.light_icon)

            # Mise à jour de la barre de recherche
            entry_bg     = THEMES[current_theme]['TAB_BG'] if current_theme == 'dark' else THEMES[current_theme]['STATUS_BG']
            entry_border = "#555555" if current_theme == 'dark' else "#aaaaaa"
            search_bar.config(bg=STATUS_BG)
            search_entry.config(bg=entry_bg, fg=FG, insertbackground=FG,
                                highlightbackground=entry_border, highlightcolor=SELECT_BG)
            search_count.config(bg=STATUS_BG, fg=STATUS_FG)
            btn_prev.config(bg=STATUS_BG, fg=FG)
            btn_next.config(bg=STATUS_BG, fg=FG)
            btn_close_search.config(bg=STATUS_BG, fg=STATUS_FG)

        def update_theme(self):
            self.frame.config(bg=TAB_BG)
            self.btn_new.config(bg=TAB_BG, fg=TAB_FG)
            self.theme_button.config(bg=TAB_BG, fg=TAB_FG)
            self.refresh()

        def add(self, tab):
            self.tabs.append(tab)
            self._make_btn(tab)
            self.select(tab)

        def _make_btn(self, tab):
            f = tk.Frame(self.frame, bg=TAB_BG)
            f.pack(side='left', fill='y', before=self.btn_new)

            border = tk.Frame(f, bg=TAB_BG, width=1)
            border.pack(side='left', fill='y')

            lbl = tk.Label(f, text=tab.label, bg=TAB_BG, fg=TAB_FG,
                        font=FONT_TAB, padx=10, cursor='hand2')
            lbl.pack(side='left', fill='y')

            close = tk.Label(f, text="✕", bg=TAB_BG, fg=TAB_FG,
                            font=('Arial', 9), padx=6, cursor='hand2')
            close.pack(side='left', fill='y')

            lbl.bind('<Button-1>',   lambda e, t=tab: self.select(t))
            close.bind('<Button-1>', lambda e, t=tab: close_tab(t))

            _register_dnd_widget(f)
            _register_dnd_widget(lbl)
            _register_dnd_widget(close)

            self._btns[tab.id] = (f, lbl, close, border)

        def select(self, tab):
            if self.active:
                self.active.hide()
            self.active = tab
            tab.show()
            self.refresh()
            update_title()
            update_status()

        def remove(self, tab):
            if tab in self.tabs:
                self.tabs.remove(tab)
            if tab.id in self._btns:
                self._btns[tab.id][0].destroy()
                del self._btns[tab.id]
            tab.frame.destroy()

        def refresh(self):
            for t in self.tabs:
                if t.id not in self._btns:
                    continue
                f, lbl, close, border = self._btns[t.id]
                active = (t is self.active)
                bg_col = TAB_ACTIVE if active else TAB_BG
                fg_col = TAB_FG_ACT if active else TAB_FG
                f.config(bg=bg_col)
                border.config(bg="#3c3c3c" if not active else TAB_ACTIVE)
                lbl.config(bg=bg_col, fg=fg_col, text=t.label)
                close.config(bg=bg_col, fg=fg_col)


    # ── Layout ────────────────────────────────────────────────────────────────────
    tab_bar     = TabBar(win)
    editor_area = tk.Frame(win, bg=BG)
    editor_area.pack(fill='both', expand=True)

    status_bar = tk.Frame(win, bg=STATUS_BG, height=24)
    status_bar.pack(fill='x', side='bottom')
    status_bar.pack_propagate(False)

    status_file  = tk.Label(status_bar, text="Untitled", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_file.pack(side='left')
    status_pos   = tk.Label(status_bar, text="Ln 1, Col 1", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_pos.pack(side='right')
    status_words = tk.Label(status_bar, text="0 words", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_words.pack(side='right')

    # ── Drag & Drop ───────────────────────────────────────────────────────────────
    dnd_enabled = False

    def _parse_dnd_paths(data):
        """Parse la chaîne brute renvoyée par tkdnd (gère espaces et accolades)."""
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
                paths.append(raw[i:end])
                i = end + 1
        return [p for p in paths if p]

    def _open_paths(paths):
        for path in paths:
            if os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue
                t = current_tab()
                if t and not t.is_modified and not t.get_content():
                    t.file_path = path
                    t.set_content(content)
                    t.set_modified(False)
                    update_title()
                else:
                    new_tab(file_path=path, content=content)

    def _on_drop(event):
        print(f"[DND] <<Drop>> reçu, event.data = {repr(event.data)}")
        editor_area.config(bg=BG)
        tab_bar.frame.config(bg=TAB_BG)
        _open_paths(_parse_dnd_paths(event.data))

    def _on_enter(event):
        print(f"[DND] <<DragEnter>> reçu")
        editor_area.config(bg=SELECT_BG)
        tab_bar.frame.config(bg=SELECT_BG)

    def _on_leave(event):
        print(f"[DND] <<DragLeave>> reçu")
        editor_area.config(bg=BG)
        tab_bar.frame.config(bg=TAB_BG)

    def _register_dnd_widget(widget):
        if not dnd_enabled:
            return
        try:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', _on_drop)
            widget.dnd_bind('<<DragEnter>>', _on_enter)
            widget.dnd_bind('<<DragLeave>>', _on_leave)
            print(f"[DND] drop target enregistré sur {widget}")
        except Exception as e:
            print(f"[DND] Erreur enregistrement drop_target sur {widget} : {e}")

    def _setup_dnd():
        global dnd_enabled
        if not DND_AVAILABLE:
            print("[DND] tkinterdnd2 non disponible, drag & drop désactivé.")
            messagebox.showwarning(
                tr('dnd_title'),
                tr('dnd_msg')
            )
            return

        dnd_enabled = True
        try:
            for widget in (editor_area, tab_bar.frame):
                _register_dnd_widget(widget)
        except Exception as e:
            print(f"[DND] Erreur lors de l'enregistrement des widgets DnD : {e}")

    _setup_dnd()


    # ══════════════════════════════════════════════════════════════════════════════
    # Actions globales
    # ══════════════════════════════════════════════════════════════════════════════
    def current_tab():
        return tab_bar.active


    def update_title():
        t = current_tab()
        name = t.name if t else "Notys"
        win.title(f"Notys — {name}")
        status_file.config(text=name)


    def update_status(event=None):
        t = current_tab()
        if not t:
            return
        idx  = t.text.index('insert')
        line, col = idx.split('.')
        status_pos.config(text=f"Ln {line}, Col {int(col)+1}")
        content = t.get_content()
        words   = len(content.split()) if content.strip() else 0
        status_words.config(text=f"{words} {tr('status_words_one') if words == 1 else tr('status_words_many')}")


    def new_tab(event=None, file_path=None, content=None):
        tab = Tab(file_path=file_path)
        tab_bar.add(tab)
        if content:
            tab.set_content(content)
        return tab


    def _dialog_unsaved(tab):
        """Affiche une boîte de dialogue style TextEdit pour un onglet non sauvegardé.
        Retourne 'save', 'discard', ou 'cancel'."""
        result = [None]

        dlg = tk.Toplevel(win)
        dlg.withdraw()
        dlg.title("")
        dlg.resizable(False, False)
        dlg.configure(bg=STATUS_BG)
        dlg.transient(win)
        dlg.grab_set()

        # ── Contenu ───────────────────────────────────────────────────────────────
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

        # ── Boutons ───────────────────────────────────────────────────────────────
        btn_frame = tk.Frame(dlg, bg=STATUS_BG, padx=28, pady=20)
        btn_frame.pack(fill='x')

        def _btn(parent, text, cmd, primary=False):
            if primary:
                bg      = SELECT_BG if current_theme == 'dark' else '#1a6bbf'
                bg_hover = '#3a6090' if current_theme == 'dark' else '#145299'
            else:
                bg      = '#3a3a3a' if current_theme == 'dark' else '#9e9e9e'
                bg_hover = '#4a4a4a' if current_theme == 'dark' else '#7a7a7a'
            fg = '#ffffff'
            b = tk.Label(
                parent, text=text,
                bg=bg, fg=fg,
                font=('Consolas', 11, 'bold' if primary else 'normal'),
                padx=16, pady=6,
                cursor='hand2',
                relief='flat',
            )
            b.bind('<Button-1>', lambda e: cmd())
            b.bind('<Enter>',    lambda e: b.config(bg=bg_hover))
            b.bind('<Leave>',    lambda e: b.config(bg=bg))
            return b

        def do_discard():
            result[0] = 'discard'
            dlg.destroy()

        def do_cancel():
            result[0] = 'cancel'
            dlg.destroy()

        def do_save():
            result[0] = 'save'
            dlg.destroy()

        _btn(btn_frame, tr('dlg_dont_save'), do_discard).pack(side='left')
        _btn(btn_frame, tr('dlg_cancel'),    do_cancel).pack(side='left', padx=(10, 0))
        _btn(btn_frame, tr('dlg_save'),      do_save, primary=True).pack(side='right')

        # ── Centrage ──────────────────────────────────────────────────────────────
        dlg.update_idletasks()
        w, h = dlg.winfo_width(), dlg.winfo_height()
        x = win.winfo_x() + (win.winfo_width()  - w) // 2
        y = win.winfo_y() + (win.winfo_height() - h) // 2
        dlg.geometry(f'+{x}+{y}')
        dlg.deiconify()
        dlg.focus_force()
        dlg.bind('<Escape>', lambda e: do_cancel())

        win.wait_window(dlg)
        return result[0]

    def _save_tab(tab):
        """Sauvegarde un onglet, ouvre le dialogue si pas de chemin. Retourne True si sauvegardé."""
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
        tab.set_modified(False)
        status_file.config(fg="#4ec9b0")
        win.after(800, lambda: status_file.config(fg=STATUS_FG))
        return True

    # ── Historique des onglets fermés (pour Cmd/Ctrl+Shift+T) ────────────────────
    _closed_tabs_history = []   # liste de dicts : {'file_path': ..., 'content': ...}

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
                    return  # L'utilisateur a annulé le "Enregistrer sous"

        if len(tab_bar.tabs) == 1:
            on_quit()
            return
        # Mémoriser avant de supprimer
        _closed_tabs_history.append({
            'file_path': tab.file_path,
            'content':   tab.get_content(),
        })
        idx = tab_bar.tabs.index(tab)
        tab_bar.remove(tab)
        if tab_bar.tabs:
            tab_bar.select(tab_bar.tabs[min(idx, len(tab_bar.tabs) - 1)])

    def on_quit(event=None):
        """Intercepte la fermeture de la fenêtre : vérifie tous les onglets non sauvegardés."""
        unsaved = [t for t in tab_bar.tabs if t.is_modified]
        for tab in unsaved:
            tab_bar.select(tab)
            action = _dialog_unsaved(tab)
            if action == 'cancel' or action is None:
                return  # Annuler = on ne ferme pas
            if action == 'save':
                if not _save_tab(tab):
                    return
        win.destroy()

    win.protocol('WM_DELETE_WINDOW', on_quit)

    def save_text(event=None):
        t = current_tab()
        if t:
            _save_tab(t)

    def save_as(event=None):
        t = current_tab()
        if not t:
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.md',
            filetypes=[('Markdown', '*.md'), ('Text', '*.txt'), ('All files', '*.*')]
        )
        if not path:
            return
        t.file_path = path
        update_title()
        _save_tab(t)


    def open_file(event=None):
        path = filedialog.askopenfilename(
            filetypes=[('Markdown', '*.md'), ('Text', '*.txt'), ('All files', '*.*')]
        )
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        t = current_tab()
        if t and not t.is_modified and not t.get_content():
            t.file_path = path
            t.set_content(content)
            t.set_modified(False)
            update_title()
        else:
            new_tab(file_path=path, content=content)

    def minimise_win(event=None):
        win.wm_state('iconic')

    def zoom_in(event=None):
        t = current_tab()
        if t:
            t.set_zoom(t.font_scale + 0.1)
        return 'break'

    def zoom_out(event=None):
        t = current_tab()
        if t:
            t.set_zoom(t.font_scale - 0.1)
        return 'break'

    def new_window(event=None):
        """Ouvre une nouvelle instance de l'application dans une fenêtre séparée."""
        import subprocess, sys
        subprocess.Popen([sys.executable, __file__])
        return 'break'

    def save_all(event=None):
        """Sauvegarde tous les onglets ouverts."""
        for tab in list(tab_bar.tabs):
            _save_tab(tab)
        return 'break'

    def reopen_last_closed_tab(event=None):
        """Rouvre le dernier onglet fermé."""
        if not _closed_tabs_history:
            return 'break'
        info = _closed_tabs_history.pop()
        new_tab(file_path=info['file_path'], content=info['content'])
        return 'break'

    def rebuild_menu():
        """Reconstruit la barre de menus après un changement de langue."""
        menubar.delete(0, 'end')

        mf2 = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
        mf2.add_command(label=tr('menu_new_window'),  accelerator=f"{mod_display}N",       command=new_window)
        mf2.add_command(label=tr('menu_new_tab'),     accelerator=f"{mod_display}T",       command=new_tab)
        mf2.add_command(label=tr('menu_reopen_tab'),  accelerator=f"{mod_display}Shift+T", command=reopen_last_closed_tab)
        mf2.add_command(label=tr('menu_open'),        accelerator=f"{mod_display}O",       command=open_file)
        mf2.add_command(label=tr('menu_close_tab'),   accelerator=f"{mod_display}W",       command=close_tab)
        mf2.add_separator()
        mf2.add_command(label=tr('menu_save'),        accelerator=f"{mod_display}S",       command=save_text)
        mf2.add_command(label=tr('menu_save_all'),    accelerator=f"{mod_display}Alt+S",   command=save_all)
        mf2.add_command(label=tr('menu_save_as'),     accelerator=f"{mod_display}Shift+S", command=save_as)
        menubar.add_cascade(label=tr('menu_file'), menu=mf2)

        me2 = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
        me2.add_command(label=tr('menu_undo'), accelerator=f"{mod_display}Z",       command=lambda: current_tab() and current_tab().text.edit_undo())
        me2.add_command(label=tr('menu_redo'), accelerator=f"{mod_display}Shift+Z", command=lambda: current_tab() and current_tab().text.edit_redo())
        me2.add_separator()
        me2.add_command(label=tr('menu_find'), accelerator=f"{mod_display}F",       command=open_search)
        menubar.add_cascade(label=tr('menu_edit'), menu=me2)

        mg2 = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
        mg2.add_command(label=tr('menu_minimize'), accelerator=f"{mod_display}M", command=lambda: minimise_win())
        menubar.add_cascade(label=tr('menu_window'), menu=mg2)

        ms2 = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
        ms2.add_command(label=tr('menu_open_settings'), command=open_settings)
        menubar.add_cascade(label=tr('menu_settings'), menu=ms2)

        win.config(menu=menubar)
        # Rafraîchir les onglets (le nom "Sans titre" / "Untitled" peut changer)
        tab_bar.refresh()
        update_title()
        update_status()

    def open_settings(event=None):
        """Ouvre la fenêtre de paramètres avec plusieurs sections."""
        global current_language, SETTINGS

        dlg = tk.Toplevel(win)
        dlg.title(tr('settings_title'))
        dlg.geometry("600x500")
        dlg.resizable(False, False)
        dlg.configure(bg=STATUS_BG)
        dlg.transient(win)
        dlg.grab_set()

        # ── Variables locales (copie des settings courants) ───────────────────────
        lang_var      = tk.StringVar(value=current_language)
        theme_var     = tk.StringVar(value=current_theme)
        font_fam_var  = tk.StringVar(value=SETTINGS['font_family'])
        font_size_var = tk.IntVar(value=SETTINGS['font_size'])
        wrap_var      = tk.StringVar(value=SETTINGS['line_wrap'])
        padding_var   = tk.IntVar(value=SETTINGS['padding'])
        status_var    = tk.BooleanVar(value=SETTINGS['show_status'])
        wcount_var    = tk.BooleanVar(value=SETTINGS['show_wordcount'])
        win_w_var     = tk.IntVar(value=SETTINGS['win_width'])
        win_h_var     = tk.IntVar(value=SETTINGS['win_height'])

        # ── Helpers UI ────────────────────────────────────────────────────────────
        H_BG   = STATUS_BG
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
                    font=('Consolas', 11), cursor='hand2',
                ).pack(side='left', padx=(0, 12))

        def make_toggle(parent, var, row, col=1):
            f = tk.Frame(parent, bg=H_BG)
            f.grid(row=row, column=col, sticky='w')
            for label, val in [(tr('on'), True), (tr('off'), False)]:
                tk.Radiobutton(
                    f, text=label, variable=var, value=val,
                    bg=H_BG, fg=FG, selectcolor=TAB_BG,
                    activebackground=H_BG, activeforeground=FG,
                    font=('Consolas', 11), cursor='hand2',
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
                highlightbackground=SEP_FG, cursor='hand2',
            )
            om['menu'].config(bg=TAB_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
            om.grid(row=row, column=col, sticky='w', pady=4)

        # ── Layout principal : nav gauche + contenu droite ────────────────────────
        outer = tk.Frame(dlg, bg=H_BG)
        outer.pack(fill='both', expand=True)

        # Panneau de navigation (gauche)
        nav_bg = TAB_BG
        nav = tk.Frame(outer, bg=nav_bg, width=160)
        nav.pack(side='left', fill='y')
        nav.pack_propagate(False)

        # Zone de contenu (droite)
        content_area = tk.Frame(outer, bg=H_BG)
        content_area.pack(side='left', fill='both', expand=True)

        # Frame courante affichée
        _current_page = [None]
        _nav_btns = []

        sections = [
            ('section_language',   '🌐'),
            ('section_appearance', '🎨'),
            ('section_editor',     '✏️'),
            ('section_interface',  '🖥️'),
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

        # Créer les boutons de navigation
        tk.Frame(nav, bg=nav_bg, height=12).pack()  # spacer
        for i, (key, icon) in enumerate(sections):
            label = tr(key).replace(icon, '').strip()
            btn = tk.Label(
                nav, text=f"  {icon}  {label}",
                font=('Consolas', 11),
                bg=nav_bg, fg=TAB_FG,
                anchor='w', cursor='hand2',
                padx=8, pady=10,
            )
            btn.pack(fill='x')
            idx = i
            btn.bind('<Button-1>', lambda e, i=idx: show_page(i))
            btn.bind('<Enter>', lambda e, b=btn, i=idx: b.config(bg=TAB_ACTIVE) if i != _nav_btns.index(b) or _current_page[0] != pages[i] else None)
            btn.bind('<Leave>', lambda e, b=btn, i=idx: b.config(bg=TAB_ACTIVE if _current_page[0] == pages[i] else nav_bg))
            _nav_btns.append(btn)

        # ── Page 0 : Langue ───────────────────────────────────────────────────────
        p0 = tk.Frame(content_area, bg=H_BG)
        row_label(p0, tr('settings_language'), 2)
        make_radiogroup(p0, lang_var, [("Français", 'fr'), ("English", 'en')], row=2)

        # ── Page 1 : Apparence ────────────────────────────────────────────────────
        p1 = tk.Frame(content_area, bg=H_BG)
        row_label(p1, tr('settings_theme'), 2)
        make_radiogroup(p1, theme_var, [
            (tr('theme_dark'),  'dark'),
            (tr('theme_light'), 'light'),
        ], row=2)

        # ── Page 2 : Éditeur ──────────────────────────────────────────────────────
        p2 = tk.Frame(content_area, bg=H_BG)

        row_label(p2, tr('settings_font_family'), 2)
        font_options = ['Consolas', 'Courier', 'Monaco', 'Menlo', 'DejaVu Sans Mono', 'Arial', 'Helvetica']
        make_optionmenu(p2, font_fam_var, font_options, row=2)

        row_label(p2, tr('settings_font_size'), 4)
        make_spinbox(p2, font_size_var, 8, 48, row=4)

        row_label(p2, tr('settings_line_wrap'), 6)
        make_radiogroup(p2, wrap_var, [
            (tr('wrap_word'), 'word'),
            (tr('wrap_char'), 'char'),
            (tr('wrap_none'), 'none'),
        ], row=6)

        row_label(p2, tr('settings_padding'), 8)
        make_spinbox(p2, padding_var, 0, 200, row=8)

        # ── Page 3 : Interface ────────────────────────────────────────────────────
        p3 = tk.Frame(content_area, bg=H_BG)

        row_label(p3, tr('settings_show_status'), 2)
        make_toggle(p3, status_var, row=2)

        row_label(p3, tr('settings_show_wordcount'), 4)
        make_toggle(p3, wcount_var, row=4)

        row_label(p3, tr('settings_win_size'), 6)
        size_f = tk.Frame(p3, bg=H_BG)
        size_f.grid(row=6, column=1, sticky='w', pady=4)
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

        pages = [p0, p1, p2, p3]
        show_page(0)

        # ── Séparateur + boutons ──────────────────────────────────────────────────
        tk.Frame(dlg, bg=SEP_FG, height=1).pack(fill='x')
        btn_frame = tk.Frame(dlg, bg=H_BG, padx=20, pady=14)
        btn_frame.pack(fill='x')

        def _sbtn(parent, text, cmd, primary=False):
            if primary:
                bg   = ACCENT
                bg_h = '#3a6090' if current_theme == 'dark' else '#145299'
            else:
                bg   = '#3a3a3a' if current_theme == 'dark' else '#9e9e9e'
                bg_h = '#4a4a4a' if current_theme == 'dark' else '#7a7a7a'
            b = tk.Label(
                parent, text=text,
                bg=bg, fg='#ffffff',
                font=('Consolas', 11, 'bold' if primary else 'normal'),
                padx=16, pady=6, cursor='hand2', relief='flat',
            )
            b.bind('<Button-1>', lambda e: cmd())
            b.bind('<Enter>',    lambda e: b.config(bg=bg_h))
            b.bind('<Leave>',    lambda e: b.config(bg=bg))
            return b

        def do_cancel():
            dlg.destroy()

        def do_apply():
            global current_language, current_theme, SETTINGS
            global BG, FG, CURSOR_CLR, SELECT_BG, STATUS_BG, STATUS_FG
            global TAB_BG, TAB_ACTIVE, TAB_FG, TAB_FG_ACT
            global C_H1, C_H2, C_H3, C_H4, C_CODE, C_BOLD, C_ITALIC
            global C_LIST, C_QUOTE, C_LINK, C_HR, C_UNDERLINE, C_STRIKE
            global FONT_BODY, FONT_H1, FONT_H2, FONT_H3, FONT_H4
            global FONT_CODE, FONT_BOLD, FONT_ITALIC

            # ── Langue ────────────────────────────────────────────────────────────
            current_language = lang_var.get()

            # ── Thème ─────────────────────────────────────────────────────────────
            new_theme = theme_var.get()
            if new_theme != current_theme:
                current_theme = new_theme
                BG         = THEMES[current_theme]['BG']
                FG         = THEMES[current_theme]['FG']
                CURSOR_CLR = THEMES[current_theme]['CURSOR_CLR']
                SELECT_BG  = THEMES[current_theme]['SELECT_BG']
                STATUS_BG  = THEMES[current_theme]['STATUS_BG']
                STATUS_FG  = THEMES[current_theme]['STATUS_FG']
                TAB_BG     = THEMES[current_theme]['TAB_BG']
                TAB_ACTIVE = THEMES[current_theme]['TAB_ACTIVE']
                TAB_FG     = THEMES[current_theme]['TAB_FG']
                TAB_FG_ACT = THEMES[current_theme]['TAB_FG_ACT']
                C_H1 = THEMES[current_theme]['C_H1']; C_H2 = THEMES[current_theme]['C_H2']
                C_H3 = THEMES[current_theme]['C_H3']; C_H4 = THEMES[current_theme]['C_H4']
                C_CODE  = THEMES[current_theme]['C_CODE']; C_BOLD  = THEMES[current_theme]['C_BOLD']
                C_ITALIC = THEMES[current_theme]['C_ITALIC']
                C_LIST  = THEMES[current_theme]['C_LIST']; C_QUOTE = THEMES[current_theme]['C_QUOTE']
                C_LINK  = THEMES[current_theme]['C_LINK']; C_HR    = THEMES[current_theme]['C_HR']
                C_UNDERLINE = THEMES[current_theme]['C_UNDERLINE']
                C_STRIKE    = THEMES[current_theme]['C_STRIKE']
                tab_bar.toggle_theme.__func__  # juste pour éviter l'appel complet
                # Appliquer manuellement (même logique que toggle_theme)
                tab_bar.update_theme()
                for tab in tab_bar.tabs:
                    tab.update_theme()
                status_bar.config(bg=STATUS_BG)
                status_file.config(bg=STATUS_BG, fg=STATUS_FG)
                status_pos.config(bg=STATUS_BG, fg=STATUS_FG)
                status_words.config(bg=STATUS_BG, fg=STATUS_FG)
                win.config(bg=BG)
                editor_area.config(bg=BG)
                menubar.config(bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
                tab_bar.theme_button.config(
                    image=tab_bar.dark_icon if current_theme == 'dark' else tab_bar.light_icon
                )
                entry_bg = THEMES[current_theme]['TAB_BG'] if current_theme == 'dark' else THEMES[current_theme]['STATUS_BG']
                entry_border = "#555555" if current_theme == 'dark' else "#aaaaaa"
                search_bar.config(bg=STATUS_BG)
                search_entry.config(bg=entry_bg, fg=FG, insertbackground=FG,
                                    highlightbackground=entry_border, highlightcolor=SELECT_BG)
                search_count.config(bg=STATUS_BG, fg=STATUS_FG)
                btn_prev.config(bg=STATUS_BG, fg=FG)
                btn_next.config(bg=STATUS_BG, fg=FG)
                btn_close_search.config(bg=STATUS_BG, fg=STATUS_FG)

            # ── Éditeur ───────────────────────────────────────────────────────────
            new_ff   = font_fam_var.get()
            new_fs   = font_size_var.get()
            new_wrap = wrap_var.get()
            new_pad  = padding_var.get()

            SETTINGS['font_family']  = new_ff
            SETTINGS['font_size']    = new_fs
            SETTINGS['line_wrap']    = new_wrap
            SETTINGS['padding']      = new_pad

            FONT_BODY   = (new_ff, new_fs)
            FONT_H1     = (new_ff, int(new_fs * 1.9), 'bold')
            FONT_H2     = (new_ff, int(new_fs * 1.55), 'bold')
            FONT_H3     = (new_ff, int(new_fs * 1.33), 'bold')
            FONT_H4     = (new_ff, int(new_fs * 1.1), 'bold')
            FONT_BOLD   = (new_ff, new_fs, 'bold')
            FONT_ITALIC = (new_ff, new_fs, 'italic')

            tk_wrap = {'word': 'word', 'char': 'char', 'none': 'none'}.get(new_wrap, 'word')
            for tab in tab_bar.tabs:
                tab.text.config(
                    wrap=tk_wrap,
                    padx=new_pad,
                    font=(new_ff, new_fs),
                )
                tab._configure_tags()
                tab.highlight_markdown()

            # ── Interface ─────────────────────────────────────────────────────────
            SETTINGS['show_status']    = status_var.get()
            SETTINGS['show_wordcount'] = wcount_var.get()
            SETTINGS['win_width']      = win_w_var.get()
            SETTINGS['win_height']     = win_h_var.get()

            if SETTINGS['show_status']:
                status_bar.pack(fill='x', side='bottom')
            else:
                status_bar.pack_forget()

            status_words.pack(side='right') if SETTINGS['show_wordcount'] else status_words.pack_forget()

            win.geometry(f"{SETTINGS['win_width']}x{SETTINGS['win_height']}")

            # ── Rebuild menu + fermeture ──────────────────────────────────────────
            rebuild_menu()
            dlg.destroy()

        _sbtn(btn_frame, tr('settings_cancel'), do_cancel).pack(side='left')
        _sbtn(btn_frame, tr('settings_apply'),  do_apply, primary=True).pack(side='right')

        # ── Centrage ──────────────────────────────────────────────────────────────
        dlg.update_idletasks()
        w, h = dlg.winfo_width(), dlg.winfo_height()
        x = win.winfo_x() + (win.winfo_width()  - w) // 2
        y = win.winfo_y() + (win.winfo_height() - h) // 2
        dlg.geometry(f'+{x}+{y}')
        dlg.focus_force()
        dlg.bind('<Escape>', lambda e: do_cancel())

    # ── Raccourcis ────────────────────────────────────────────────────────────────
    # Détecter l'OS pour utiliser les bonnes touches de modification
    is_macos = platform.system() == 'Darwin'
    mod_key = 'Command' if is_macos else 'Control'
    mod_display = 'Cmd+' if is_macos else 'Ctrl+'

    if is_macos:
        try:
            win.createcommand('::tk::mac::Quit', on_quit)
        except Exception:
            pass

    # ── Barre de recherche ────────────────────────────────────────────────────────
    search_bar = tk.Frame(win, bg=STATUS_BG, height=36)
    search_bar._visible = False

    search_entry_bg = get_color('TAB_BG') if current_theme == 'dark' else get_color('STATUS_BG')
    search_entry_border = "#555555" if current_theme == 'dark' else "#aaaaaa"
    search_entry = tk.Entry(
        search_bar,
        bg=search_entry_bg, fg=FG,
        insertbackground=FG,
        relief='flat', bd=0,
        font=('Consolas', 12),
        highlightthickness=1,
        highlightbackground=search_entry_border,
        highlightcolor=SELECT_BG,
        width=30,
    )
    search_entry.pack(side='left', padx=(10, 6), pady=6, ipady=3)

    search_count = tk.Label(search_bar, text="", bg=STATUS_BG, fg=STATUS_FG, font=('Consolas', 11))
    search_count.pack(side='left', padx=(0, 6))

    btn_prev = tk.Label(search_bar, text="↑", bg=STATUS_BG, fg=FG, font=('Consolas', 14), cursor='hand2', padx=6)
    btn_prev.pack(side='left')
    btn_next = tk.Label(search_bar, text="↓", bg=STATUS_BG, fg=FG, font=('Consolas', 14), cursor='hand2', padx=6)
    btn_next.pack(side='left')

    btn_close_search = tk.Label(search_bar, text="✕", bg=STATUS_BG, fg=STATUS_FG, font=('Arial', 11), cursor='hand2', padx=10)
    btn_close_search.pack(side='right')

    _search_matches  = []
    _search_index    = [0]   # liste pour mutabilité dans les closures
    _search_last_query = [""]  # tracker du dernier texte de recherche

    def _search_do(query=None, reset_index=True):
        t = current_tab()
        if not t:
            return
        if query is None:
            query = search_entry.get()

        t.text.tag_remove('search_match',    '1.0', 'end')
        t.text.tag_remove('search_current',  '1.0', 'end')
        t.text.tag_configure('search_match',   background="#b6c511", foreground='#000000')
        t.text.tag_configure('search_current', background="#00e8f4", foreground='#000000')

        _search_matches.clear()
        if not query:
            search_count.config(text="")
            _search_last_query[0] = ""
            return

        content = t.text.get('1.0', 'end-1c')
        for m in re.finditer(re.escape(query), content, re.IGNORECASE):
            start = f'1.0+{m.start()}c'
            end   = f'1.0+{m.end()}c'
            t.text.tag_add('search_match', start, end)
            _search_matches.append((start, end))

        if _search_matches:
            if reset_index or query != _search_last_query[0]:
                _search_index[0] = 0
            _search_highlight_current()
        else:
            search_count.config(text=tr('search_no_results'))
        
        _search_last_query[0] = query

    def _search_highlight_current():
        t = current_tab()
        if not t or not _search_matches:
            return
        t.text.tag_remove('search_current', '1.0', 'end')
        i = _search_index[0]
        start, end = _search_matches[i]
        t.text.tag_add('search_current', start, end)
        t.text.see(start)
        search_count.config(text=f"{i + 1} / {len(_search_matches)}")

    def _search_next(event=None):
        if not _search_matches:
            return
        _search_index[0] = (_search_index[0] + 1) % len(_search_matches)
        _search_highlight_current()

    def _search_prev(event=None):
        if not _search_matches:
            return
        _search_index[0] = (_search_index[0] - 1) % len(_search_matches)
        _search_highlight_current()

    def open_search(event=None):
        if not search_bar._visible:
            search_bar.pack(fill='x', side='top', after=tab_bar.frame)
            search_bar._visible = True
        search_entry.focus_set()
        search_entry.select_range(0, 'end')
        # Lancer la recherche si texte déjà présent
        if search_entry.get():
            _search_do()
        return 'break'

    def close_search(event=None):
        t = current_tab()
        if t:
            t.text.tag_remove('search_match',   '1.0', 'end')
            t.text.tag_remove('search_current', '1.0', 'end')
        _search_matches.clear()
        search_count.config(text="")
        search_bar.pack_forget()
        search_bar._visible = False
        t = current_tab()
        if t:
            t.text.focus_set()
        return 'break'

    def _handle_search_tab(event=None):
        _search_next()
        return 'break'
    
    def _handle_search_shift_tab(event=None):
        _search_prev()
        return 'break'

    search_entry.bind('<KeyRelease>', lambda e: _search_do(reset_index=False))
    search_entry.bind('<Tab>',        _handle_search_tab)
    search_entry.bind('<Shift-Tab>',  _handle_search_shift_tab)
    search_entry.bind('<Escape>',     close_search)
    btn_next.bind('<Button-1>',       lambda e: _search_next())
    btn_prev.bind('<Button-1>',       lambda e: _search_prev())
    btn_close_search.bind('<Button-1>', lambda e: close_search())

    shortcuts = [
        (f'<{mod_key}-s>', save_text),
        (f'<{mod_key}-o>', open_file),
        (f'<{mod_key}-t>', new_tab),
        (f'<{mod_key}-n>', new_window),
        (f'<{mod_key}-S>', save_as),
        (f'<{mod_key}-w>', lambda e: close_tab()),
        (f'<{mod_key}-m>', minimise_win),
        (f'<{mod_key}-z>', lambda e: current_tab() and current_tab().text.edit_undo()),
        (f'<{mod_key}-Z>', lambda e: current_tab() and current_tab().text.edit_redo()),
        (f'<{mod_key}-f>', open_search),
        (f'<{mod_key}-F>', open_search),
        (f'<{mod_key}-=>', zoom_in),
        (f'<{mod_key}-)>', zoom_out),
        # Cmd/Ctrl+Shift+T : rouvrir le dernier onglet fermé
        (f'<{mod_key}-T>', reopen_last_closed_tab),
        ('<Command-q>',    lambda e: on_quit()),   # Cmd+Q  (macOS)
        ('<Command-Q>',    lambda e: on_quit()),
        ('<Alt-F4>',       lambda e: on_quit()),   # Alt+F4 (Windows/Linux)
    ]

    for seq, cmd in shortcuts:
        win.bind(seq, cmd)

    # Cmd/Ctrl+Alt/Opt+S : tout sauvegarder (séparé car syntaxe conditionnelle)
    save_all_seq = '<Command-Option-s>' if is_macos else '<Control-Alt-s>'
    win.bind(save_all_seq, save_all)

    # Ctrl+Tab / Ctrl+Shift+Tab : onglet suivant / précédent
    def _next_tab(event=None):
        tabs = tab_bar.tabs
        if len(tabs) < 2:
            return 'break'
        idx = tabs.index(current_tab())
        tab_bar.select(tabs[(idx + 1) % len(tabs)])
        return 'break'

    def _prev_tab(event=None):
        tabs = tab_bar.tabs
        if len(tabs) < 2:
            return 'break'
        idx = tabs.index(current_tab())
        tab_bar.select(tabs[(idx - 1) % len(tabs)])
        return 'break'

    win.bind('<Control-Tab>',       _next_tab)
    win.bind('<Control-Shift-Tab>', _prev_tab)


    # ── Menu ──────────────────────────────────────────────────────────────────────
    menubar = tk.Menu(win, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG, bd=0)

    mf = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    mf.add_command(label=tr('menu_new_window'),  accelerator=f"{mod_display}N",          command=new_window)
    mf.add_command(label=tr('menu_new_tab'),     accelerator=f"{mod_display}T",          command=new_tab)
    mf.add_command(label=tr('menu_reopen_tab'),  accelerator=f"{mod_display}Shift+T",    command=reopen_last_closed_tab)
    mf.add_command(label=tr('menu_open'),        accelerator=f"{mod_display}O",          command=open_file)
    mf.add_command(label=tr('menu_close_tab'),   accelerator=f"{mod_display}W",          command=close_tab)
    mf.add_separator()
    mf.add_command(label=tr('menu_save'),        accelerator=f"{mod_display}S",          command=save_text)
    mf.add_command(label=tr('menu_save_all'),    accelerator=f"{mod_display}Alt+S",      command=save_all)
    mf.add_command(label=tr('menu_save_as'),     accelerator=f"{mod_display}Shift+S",    command=save_as)
    menubar.add_cascade(label=tr('menu_file'), menu=mf)

    me = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    me.add_command(label=tr('menu_undo'),  accelerator=f"{mod_display}Z",       command=lambda: current_tab() and current_tab().text.edit_undo())
    me.add_command(label=tr('menu_redo'),  accelerator=f"{mod_display}Shift+Z", command=lambda: current_tab() and current_tab().text.edit_redo())
    me.add_separator()
    me.add_command(label=tr('menu_find'), accelerator=f"{mod_display}F",       command=open_search)
    menubar.add_cascade(label=tr('menu_edit'), menu=me)

    mg = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    mg.add_command(label=tr('menu_minimize'), accelerator=f"{mod_display}M", command=lambda: minimise_win())
    menubar.add_cascade(label=tr('menu_window'), menu=mg)

    ms = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    ms.add_command(label=tr('menu_open_settings'), command=open_settings)
    menubar.add_cascade(label=tr('menu_settings'), menu=ms)

    win.config(menu=menubar)

    # ── Init ──────────────────────────────────────────────────────────────────────
    tab_bar.update_theme()
    new_tab()
    update_title()
    update_status()

    win.mainloop()