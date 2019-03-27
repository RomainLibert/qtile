import os
import importlib.util
import re

from libqtile import layout, bar, widget
from libqtile.config import Screen, Group, Drag, Click, EzKey as Key
from libqtile.command import lazy
from libqtile.utils import QtileError


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

mod = "mod4"
PLUGIN_DIR = '~/.config/qtile/plugins'
THEME_DIR = '~/.config/qtile/themes'
KEYMAP = '~/.config/qtile/keymap.conf'
SELECTED_THEME = 'roger'
TERMINAL = "xterm"
GROUPS = ('1', '2', '3', '4')

def parse_keymap(fname=KEYMAP):
    fname = os.path.expanduser(fname)
    with open(fname, 'r') as config:
        for line in config:
            _command, *_keys, _ = re.split(r'\s+', line)
            if not _command or not _keys:
                continue
            yield (_command, _keys)

def load_module(fname, directory):
    if not fname.endswith('py'):
        return None
    path = os.path.join(os.path.expanduser(directory), fname)

    spec = importlib.util.spec_from_file_location(fname.split('.')[0], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

# ====================================================
# Misc Configurations
# ====================================================

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# ====================================================
# Loading Theme
# ====================================================

theme = load_module('%s.py' % SELECTED_THEME, THEME_DIR)

# ====================================================
# Widgets Configuration
# ====================================================

widget_defaults = theme.widget_defaults
extension_defaults = widget_defaults.copy()

# ====================================================
# Layout definition
# ====================================================

layout_theme = theme.layout_theme

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(**layout_theme),
]

floating_layout = layout.Floating(**layout_theme)

# ====================================================
# Known functions
# ====================================================
registered_functions = {
    # Group Functions
    'next_layout': lazy.next_layout(),
    'prev_layout': lazy.prev_layout(),
    'next_group': lazy.screen.next_group(),
    'prev_group': lazy.screen.prev_group(),
    'toggle_group': lazy.screen.toggle_group(),
    'increase_ratio': lazy.layout.increase_ratio(),
    'decrease_ratio': lazy.layout.decrease_ratio(),
    # Window Functions
    'window_kill': lazy.window.kill(),
    'layout_next': lazy.layout.next(),
    'toggle_floating': lazy.toggle_floating(),
    'toggle_fullscreen': lazy.toggle_fullscreen(),
    # ???
    'layout_down': lazy.layout.down(),
    'layout_up': lazy.layout.up(),
    'layout_shuffle_down': lazy.layout.shuffle_down(),
    'layout_shuffle_up': lazy.layout.shuffle_up(),
    'layout_rotate': lazy.layout.rotate(),
    'layout_toggle_split': lazy.layout.toggle_split(),
    # General Functions
    'restart': lazy.restart(),
    'shutdown': lazy.shutdown(),
    'spawncmd': lazy.spawncmd(),
    # Applications
    'open_terminal': lazy.spawn(TERMINAL),
}

# ====================================================
# Registering plugins into know functions
# ====================================================

for plugin_name in os.listdir(os.path.expanduser(PLUGIN_DIR)):
    plugin = load_module(plugin_name, PLUGIN_DIR)

    if plugin:
        registered_functions.update(plugin.registered_functions)

# ====================================================
# Screens/Bars Configuration
# ====================================================

default_bar = bar.Bar(
    [
        widget.GroupBox(),
        widget.Prompt(),
        widget.WindowName(),
        widget.TextBox("default config", name="default"),
        widget.Systray(),
        widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
    ],
    24,
)

if theme.top_bar:
    top_bars = theme.top_bars or [default_bar]
if theme.bottom_bar:
    bottom_bars = theme.bottom_bars or [default_bar]

def create_screen(n, *args, **kwargs):
    values = {}
    if theme.top_bar and top_bars:
        values['top'] = top_bars.pop(0)
    if theme.bottom_bar and bottom_bars:
        values['bottom'] = bottom_bars.pop(0)

    if n == 0 and not theme.top_bar and not theme.bottom_bar:
        theme['bottom'] = default_bar

    if 'top' not in values and 'bottom' not in values:
        values['top'] = bar.Gap(24)
    values.update(kwargs)
    return Screen(*args, **values)

# TODO Autodetect how many screens there are
_screens = 1
screens = [create_screen(n) for n in range(_screens)]

# ====================================================
# Generating Groups and their associated commands
# ====================================================
groups = [Group(g) for g in GROUPS]

for idx, g in enumerate(groups):
    registered_functions['goto_group_%d' % (idx + 1)] = lazy.group[g.name].toscreen()
    registered_functions['moveto_group_%d' % (idx + 1)] = lazy.window.togroup(g.name)

# ====================================================
# Generating keybindings
# ====================================================
keys = []

for command, keysyms in parse_keymap():
    try:
        _keys = [Key(keysym, registered_functions[command]) for keysym in keysyms]
    except KeyError:
        # TODO Make a system that enables to see errors
        print("There was an error for command %s" % command)
    except QtileError as e:
        print("For command %s" % command)
        print(e)
    else:
        keys.extend(_keys)
