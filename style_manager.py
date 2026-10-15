import copy
import json
import os
import re


STYLE_ELEMENTS = (
    ('text', 'Text', '', 'theme:FG', False, False, False, False),
    ('h1', 'Header 1', '#', 'theme:C_H1', True, False, False, False),
    ('h2', 'Header 2', '##', 'theme:C_H2', True, False, False, False),
    ('h3', 'Header 3', '###', 'theme:C_H3', True, False, False, False),
    ('h4', 'Header 4', '####', 'theme:C_H4', True, False, False, False),
    ('h5', 'Header 5', '#####', 'theme:C_H4', True, False, False, False),
    ('h6', 'Header 6', '######', 'theme:C_H4', True, False, False, False),
    ('bold', 'Bold', '**', 'theme:C_BOLD', True, False, False, False),
    ('italic', 'Italic', '*', 'theme:C_ITALIC', False, True, False, False),
    ('inline_code', 'Inline Code', '`', 'theme:C_CODE', False, False, False, False),
    ('code_block', 'Code Block', '```', 'theme:C_CODE', False, False, False, False),
    ('quote', 'Blockquote', '>', 'theme:C_QUOTE', False, True, False, False),
    ('link', 'Link', '[', 'theme:C_LINK', False, False, True, False),
    ('list', 'Bullet List', '•', 'theme:C_LIST', False, False, False, False),
    ('underline', 'Underline', '-:', 'theme:C_UNDERLINE', False, False, True, False),
    ('strike', 'Strikethrough', '~~', 'theme:C_STRIKE', False, False, False, True),
    ('hr', 'Horizontal Rule', '---', 'theme:C_HR', False, False, False, False),
)

# Keep the built-in profile aligned with the palettes in main.py (THEMES).
# These are intentionally separate so Default remains readable in either theme.
THEME_COLOR_PAIRS = {
    'text': ('#000000', '#d4d4d4'),
    'h1': ('#1e90ff', '#39BBD8'),
    'h2': ('#1e90ff', '#39BBD8'),
    'h3': ('#1e90ff', '#39BBD8'),
    'h4': ('#1e90ff', '#39BBD8'),
    'h5': ('#1e90ff', '#39BBD8'),
    'h6': ('#1e90ff', '#39BBD8'),
    'bold': ('#000000', '#ffffff'),
    'italic': ('#666666', '#c8c8c8'),
    'inline_code': ('#ff4500', '#DE7316'),
    'code_block': ('#ff4500', '#DE7316'),
    'quote': ('#228b22', '#6A9955'),
    'link': ('#006400', '#4ec9b0'),
    # The light palette's C_LIST was white, which is invisible on its white background.
    'list': ('#000000', '#ffffff'),
    'underline': ('#000000', '#ffffff'),
    'strike': ('#666666', '#c8c8c8'),
    'hr': ('#cccccc', '#555555'),
}

ELEMENT_DEFAULTS = {
    key: {
        'marker': marker,
        'light_color': THEME_COLOR_PAIRS.get(key, (color, color))[0],
        'dark_color': THEME_COLOR_PAIRS.get(key, (color, color))[1],
        'bold': bold,
        'italic': italic,
        'underline': underline,
        'strikethrough': strikethrough,
        'font_size': 0,
    }
    for key, _label, marker, color, bold, italic, underline, strikethrough
    in STYLE_ELEMENTS
}


class StyleManager:
    def __init__(self, config_dir, active_name='default'):
        self.styles_dir = os.path.join(config_dir, 'styles')
        os.makedirs(self.styles_dir, exist_ok=True)
        requested_name = self._valid_name(active_name) or 'default'
        migrated_profile = None
        if requested_name.casefold() not in ('default', 'custom'):
            try:
                migrated_profile = self.load(requested_name)
            except (OSError, ValueError, json.JSONDecodeError):
                pass
        self._ensure_default()
        self._ensure_custom(migrated_profile)
        self.active_name = self._existing_name(requested_name) or 'default'
        self.profile = self.load_active()

    @staticmethod
    def _valid_name(name):
        if not isinstance(name, str):
            return None
        name = name.strip()
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9 _-]{0,39}', name):
            return None
        return name

    @staticmethod
    def normalize(data):
        normalized = {'version': 1, 'elements': copy.deepcopy(ELEMENT_DEFAULTS)}
        if not isinstance(data, dict):
            return normalized
        elements = data.get('elements', data)
        if not isinstance(elements, dict):
            return normalized

        for key, defaults in normalized['elements'].items():
            value = elements.get(key)
            if not isinstance(value, dict):
                continue
            marker = value.get('marker')
            if isinstance(marker, str) and len(marker) <= 12 and (marker.strip() or key == 'text'):
                defaults['marker'] = marker
            # Migrate profiles created by earlier builds (including the first
            # two-column build, which used color_light/color_dark).
            for color_key, legacy_key in (('light_color', 'color_light'), ('dark_color', 'color_dark')):
                color = value.get(color_key, value.get(legacy_key, value.get('color')))
                if isinstance(color, str) and (
                    re.fullmatch(r'#[0-9a-fA-F]{6}', color)
                    or re.fullmatch(r'theme:[A-Z_]+', color)
                ):
                    defaults[color_key] = color
            for flag in ('bold', 'italic', 'underline', 'strikethrough'):
                if isinstance(value.get(flag), bool):
                    defaults[flag] = value[flag]
            size = value.get('font_size')
            if isinstance(size, int) and not isinstance(size, bool) and 0 <= size <= 72:
                defaults['font_size'] = size
        return normalized

    def _path(self, name):
        valid_name = self._valid_name(name)
        if not valid_name:
            raise ValueError('Style names must be 1-40 letters, numbers, spaces, _ or -.')
        return os.path.join(self.styles_dir, f'{valid_name}.json')

    def _existing_name(self, name):
        valid_name = self._valid_name(name)
        if not valid_name:
            return None
        return next((item for item in self.list_styles() if item.casefold() == valid_name.casefold()), None)

    def _ensure_default(self):
        # Default is read-only and built-in: refresh it so existing installations
        # receive the correct paired light/dark palette instead of stale values.
        self._write('default', {'elements': ELEMENT_DEFAULTS})

    def _ensure_custom(self, migrated_profile=None):
        try:
            self.load('custom')
        except (OSError, ValueError, json.JSONDecodeError):
            profile = migrated_profile if migrated_profile is not None else self.load('default')
            self._write('custom', profile)

    def list_styles(self):
        names = {}
        try:
            for filename in os.listdir(self.styles_dir):
                if filename.lower().endswith('.json'):
                    name = self._valid_name(filename[:-5])
                    if name:
                        names.setdefault(name.casefold(), name)
        except OSError:
            pass
        names['default'] = 'default'
        ordered_names = [names.pop('default')]
        if 'custom' in names:
            ordered_names.append(names.pop('custom'))
        extra_names = sorted(
            names.values(),
            key=str.casefold,
        )
        return [*ordered_names, *extra_names]

    def load(self, name):
        path = self._path(name)
        with open(path, 'r', encoding='utf-8') as style_file:
            return self.normalize(json.load(style_file))

    def load_active(self):
        try:
            self.profile = self.load(self.active_name)
        except (OSError, ValueError, json.JSONDecodeError):
            self.active_name = 'default'
            try:
                self.profile = self.load('default')
            except (OSError, ValueError, json.JSONDecodeError):
                self.profile = self.normalize(None)
                self._write('default', self.profile)
        return copy.deepcopy(self.profile)

    def _write(self, name, profile):
        path = self._path(name)
        normalized = self.normalize(profile)
        temporary_path = path + '.tmp'
        with open(temporary_path, 'w', encoding='utf-8') as style_file:
            json.dump(normalized, style_file, indent=2, ensure_ascii=False)
        os.replace(temporary_path, path)
        return copy.deepcopy(normalized)

    def save(self, name, profile):
        valid_name = self._valid_name(name)
        if not valid_name or valid_name.casefold() == 'default':
            raise ValueError('The default style is read-only.')
        existing_name = self._existing_name(valid_name)
        if existing_name is None:
            raise ValueError(f'No style named "{valid_name}" exists.')
        return self._write(existing_name, profile)

    def create(self, name, profile):
        valid_name = self._valid_name(name)
        if not valid_name or valid_name.casefold() == 'default':
            raise ValueError('Choose a name other than Default.')
        if self._existing_name(valid_name) is not None:
            raise FileExistsError(f'A style named "{valid_name}" already exists.')
        return self._write(valid_name, profile)

    def reset(self, name):
        valid_name = self._valid_name(name)
        if not valid_name or valid_name.casefold() == 'default':
            raise ValueError('The default style cannot be reset.')
        existing_name = self._existing_name(valid_name)
        if existing_name is None:
            raise ValueError(f'No style named "{valid_name}" exists.')
        profile = self.load('default')
        profile = self._write(existing_name, profile)
        if self.active_name == existing_name:
            self.profile = profile
        return copy.deepcopy(profile)

    def activate(self, name):
        valid_name = self._valid_name(name)
        existing_name = self._existing_name(valid_name) if valid_name else None
        if existing_name is None:
            raise ValueError('That style profile does not exist.')
        try:
            profile = self.load(existing_name)
        except (OSError, ValueError, json.JSONDecodeError):
            self.active_name = 'default'
            self.profile = self.load('default')
            return copy.deepcopy(self.profile)
        self.active_name = existing_name
        self.profile = profile
        return copy.deepcopy(profile)

    def delete(self, name):
        valid_name = self._valid_name(name)
        if not valid_name or valid_name.casefold() == 'default':
            raise ValueError('The default style cannot be deleted.')
        existing_name = self._existing_name(valid_name)
        if existing_name is None:
            raise ValueError(f'No style named "{valid_name}" exists.')
        os.remove(self._path(existing_name))
        if self.active_name == existing_name:
            self.active_name = 'default'
            self.profile = self.load('default')
