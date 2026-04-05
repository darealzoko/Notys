import tkinter as tk
from tkinter import filedialog
import os
import re
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

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
        'C_LIST': "#BB00FF", 'C_QUOTE': "#6A9955", 'C_LINK': "#4ec9b0", 'C_HR': "#555555"
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
        'C_LIST': "#8a2be2", 'C_QUOTE': "#228b22", 'C_LINK': "#006400", 'C_HR': "#cccccc"
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

FONT_BODY   = ('Consolas', 12)
FONT_H1     = ('Consolas', 28, 'bold')
FONT_H2     = ('Consolas', 22, 'bold')
FONT_H3     = ('Consolas', 18, 'bold')
FONT_H4     = ('Consolas', 14, 'bold')
FONT_CODE   = ('Courier', 11)
FONT_BOLD   = ('Consolas', 12, 'bold')
FONT_ITALIC = ('Consolas', 12, 'italic')
FONT_TAB    = ('Arial', 11)

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
}

ALL_TAGS = ('h1','h2','h3','h4','code','bold','italic','list','quote','link','hr')

# ── Fenêtre principale ────────────────────────────────────────────────────────
if __name__ == '__main__':
    # ── Fenêtre principale ────────────────────────────────────────────────────────
    win = tk.Tk()
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

    FONT_BODY   = ('Consolas', 12)
    FONT_H1     = ('Consolas', 28, 'bold')
    FONT_H2     = ('Consolas', 22, 'bold')
    FONT_H3     = ('Consolas', 18, 'bold')
    FONT_H4     = ('Consolas', 14, 'bold')
    FONT_CODE   = ('Courier', 11)
    FONT_BOLD   = ('Consolas', 12, 'bold')
    FONT_ITALIC = ('Consolas', 12, 'italic')
    FONT_TAB    = ('Arial', 11)

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
    }

    ALL_TAGS = ('h1','h2','h3','h4','code','bold','italic','list','quote','link','hr')

    # ══════════════════════════════════════════════════════════════════════════════
    # Classe Tab
    # ══════════════════════════════════════════════════════════════════════════════
    class Tab:
        _counter = 0

        def __init__(self, file_path=None):
            Tab._counter += 1
            self.id            = Tab._counter
            self.file_path     = file_path
            self.is_modified   = False
            self.highlight_job = None
            # Liste des matches $@color text@$ : (match_start, match_end, color_hex)
            self._color_matches = []

            self.frame = tk.Frame(editor_area, bg=BG)

            self.sb = tk.Scrollbar(self.frame, bg=BG, troughcolor=BG, bd=0, width=8)
            self.sb.pack(side='right', fill='y')

            self.text = tk.Text(
                self.frame,
                bg=BG, fg=FG,
                insertbackground=CURSOR_CLR,
                selectbackground=SELECT_BG,
                bd=0, highlightthickness=0, relief='flat',
                font=FONT_BODY,
                padx=40, pady=30,
                spacing1=2, spacing3=4,
                wrap='word',
                undo=True,
                yscrollcommand=self.sb.set,
            )
            self.text.pack(fill='both', expand=True)
            self.sb.config(command=self.text.yview)

            # Tag pour masquer les symboles $@..@$ (couleur = fond = invisible)
            self.text.tag_configure('hidden', foreground=BG, font=('Andale Mono', 1))

            self._configure_tags()
            self.text.bind('<KeyRelease>', self._on_key)
            self.text.bind('<ButtonRelease>', self._on_cursor_move)
            self.text.bind('<Tab>', self._handle_tab)

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
            t.tag_configure('h1',     foreground=C_H1,    font=FONT_H1)
            t.tag_configure('h2',     foreground=C_H2,    font=FONT_H2)
            t.tag_configure('h3',     foreground=C_H3,    font=FONT_H3)
            t.tag_configure('h4',     foreground=C_H4,    font=FONT_H4)
            t.tag_configure('code',   foreground=C_CODE,  font=FONT_CODE)
            t.tag_configure('bold',   foreground=C_BOLD,  font=FONT_BOLD)
            t.tag_configure('italic', foreground=C_ITALIC,font=FONT_ITALIC)
            t.tag_configure('list',   foreground=C_LIST)
            t.tag_configure('quote',  foreground=C_QUOTE, font=('Andale Mono', 12, 'italic'))
            t.tag_configure('link',   foreground=C_LINK,  underline=True)
            t.tag_configure('hr',     foreground=C_HR)

        def _handle_tab(self, event):
            self.text.insert('insert', '    ')
            return 'break'

        def _on_key(self, event=None):
            self.set_modified(True)
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
            for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                if not in_code_block(m.start(), m.end()):
                    t.tag_add('link', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')

            # ── $@couleur texte@$ ─────────────────────────────────────────────────
            self._color_matches = []

            # Supprimer anciens tags couleur custom
            for tag in t.tag_names():
                if tag.startswith('clr_'):
                    t.tag_remove(tag, '1.0', 'end')

            for m in re.finditer(r'\$@(\w+)\s(.*?)@\$', content, re.DOTALL):
                color_name = m.group(1).lower()
                color_hex  = COLOR_NAMES.get(color_name, None)
                if not color_hex:
                    # Tenter hex direct (#rrggbb)
                    if re.match(r'^#[0-9a-fA-F]{6}$', color_name):
                        color_hex = color_name
                    else:
                        continue

                tag_name = f'clr_{color_name}_{self.id}'
                t.tag_configure(tag_name, foreground=color_hex, font=FONT_BODY)

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

                # Mémoriser les spans des symboles : "$@couleur " et "@$"
                prefix_span = (full_start, color_end)   # "$@couleur "
                suffix_span = (text_end,  suffix_end)   # "@$"

                self._color_matches.append({
                    'full_start':  full_start,
                    'full_end':    suffix_end,
                    'prefix_span': prefix_span,
                    'suffix_span': suffix_span,
                    'text_start':  text_start,
                    'text_end':    text_end,
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

            for match in self._color_matches:
                full_start = match['full_start']
                full_end   = match['full_end']

                # Le curseur est-il dans ce bloc (du $@ jusqu'au @$) ?
                cursor_inside = full_start <= cursor_offset <= full_end

                if not cursor_inside:
                    # Masquer le préfixe "$@couleur " et le suffixe "@$"
                    ps, pe = match['prefix_span']
                    ss, se = match['suffix_span']
                    t.tag_add('hidden', f'1.0+{ps}c', f'1.0+{pe}c')
                    t.tag_add('hidden', f'1.0+{ss}c', f'1.0+{se}c')
                # Sinon : tout est visible (les tags couleur restent, 'hidden' non appliqué)

        @property
        def name(self):
            return os.path.basename(self.file_path) if self.file_path else "Sans titre"

        @property
        def label(self):
            return self.name + (" ●" if self.is_modified else "")

        def set_modified(self, val):
            self.is_modified = val
            tab_bar.refresh()

        def get_content(self):
            return self.text.get('1.0', 'end-1c')

        def set_content(self, content):
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', content)
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

            # Load icons
            dark_drawing = svg2rlg('dark.svg')
            dark_img = renderPM.drawToPIL(dark_drawing)
            dark_img = dark_img.resize((20, 20))  # Resize to desired icon size (modify here)
            self.dark_icon = ImageTk.PhotoImage(dark_img, master=parent)

            light_drawing = svg2rlg('light.svg')
            light_img = renderPM.drawToPIL(light_drawing)
            light_img = light_img.resize((20, 20))  # Resize to desired icon size (modify here)
            self.light_icon = ImageTk.PhotoImage(light_img, master=parent)

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

    status_file  = tk.Label(status_bar, text="Sans titre", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_file.pack(side='left')
    status_pos   = tk.Label(status_bar, text="Ln 1, Col 1", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_pos.pack(side='right')
    status_words = tk.Label(status_bar, text="0 mots", bg=STATUS_BG, fg=STATUS_FG, font=('Andale Mono', 10), padx=10)
    status_words.pack(side='right')


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
        status_words.config(text=f"{words} mot{'s' if words != 1 else ''}")


    def new_tab(event=None, file_path=None, content=None):
        tab = Tab(file_path=file_path)
        tab_bar.add(tab)
        if content:
            tab.set_content(content)
        return tab


    def close_tab(tab=None, event=None):
        if tab is None:
            tab = current_tab()
        if tab is None:
            return
        if len(tab_bar.tabs) == 1:
            tab.file_path = None
            tab.set_content("")
            tab.set_modified(False)
            update_title()
            return
        idx = tab_bar.tabs.index(tab)
        tab_bar.remove(tab)
        if tab_bar.tabs:
            tab_bar.select(tab_bar.tabs[min(idx, len(tab_bar.tabs) - 1)])


    def save_text(event=None):
        t = current_tab()
        if not t:
            return
        if t.file_path is None:
            path = filedialog.asksaveasfilename(
                defaultextension='.md',
                filetypes=[('Markdown', '*.md'), ('Texte', '*.txt'), ('Tous', '*.*')]
            )
            if not path:
                return
            t.file_path = path
            update_title()
        with open(t.file_path, 'w', encoding='utf-8') as f:
            f.write(t.get_content())
        t.set_modified(False)
        status_file.config(fg="#4ec9b0")
        win.after(800, lambda: status_file.config(fg=STATUS_FG))


    def save_as(event=None):
        t = current_tab()
        if not t:
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.md',
            filetypes=[('Markdown', '*.md'), ('Texte', '*.txt'), ('Tous', '*.*')]
        )
        if not path:
            return
        t.file_path = path
        update_title()
        save_text()


    def open_file(event=None):
        path = filedialog.askopenfilename(
            filetypes=[('Markdown', '*.md'), ('Texte', '*.txt'), ('Tous', '*.*')]
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


    # ── Raccourcis ────────────────────────────────────────────────────────────────
    for seq, cmd in [
        ('<Command-s>', save_text),  ('<Control-s>', save_text),
        ('<Command-o>', open_file),  ('<Control-o>', open_file),
        ('<Command-n>', new_tab),    ('<Control-n>', new_tab),
        ('<Command-S>', save_as),    ('<Control-S>', save_as),
        ('<Command-w>', lambda e: close_tab()), ('<Control-w>', lambda e: close_tab()),
    ]:
        win.bind(seq, cmd)


    # ── Menu ──────────────────────────────────────────────────────────────────────
    menubar = tk.Menu(win, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG, bd=0)

    mf = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    mf.add_command(label="Nouvel onglet",     accelerator="Cmd+N", command=new_tab)
    mf.add_command(label="Ouvrir…",           accelerator="Cmd+O", command=open_file)
    mf.add_command(label="Fermer l'onglet",   accelerator="Cmd+W", command=close_tab)
    mf.add_separator()
    mf.add_command(label="Enregistrer",       accelerator="Cmd+S", command=save_text)
    mf.add_command(label="Enregistrer sous…", accelerator="Cmd+Shift+S", command=save_as)
    menubar.add_cascade(label="Fichier", menu=mf)

    me = tk.Menu(menubar, tearoff=0, bg=STATUS_BG, fg=FG, activebackground=SELECT_BG, activeforeground=FG)
    me.add_command(label="Annuler",  accelerator="Cmd+Z",       command=lambda: current_tab() and current_tab().text.edit_undo())
    me.add_command(label="Rétablir", accelerator="Cmd+Shift+Z", command=lambda: current_tab() and current_tab().text.edit_redo())
    menubar.add_cascade(label="Édition", menu=me)

    win.config(menu=menubar)

    # ── Init ──────────────────────────────────────────────────────────────────────
    tab_bar.update_theme()
    new_tab()
    update_title()
    update_status()

    win.mainloop()