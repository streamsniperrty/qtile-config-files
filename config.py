# Streamsniperrty's Qtile Config File
# Copyright (c) 2010 Aldo Cortesi
# Qtile was started by Aldo, with many other collaborators.

### IMPORTS ###
from typing import List  # noqa: F401
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.layout import *
from libqtile import hook

import os
import subprocess

### VARIABLES ###
mod = "mod4"
terminal = "urxvt"

### MOUSE ###

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

### KEYBINDS ### 
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Swap windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Window resizing
    Key([mod, "control"], "h", lazy.layout.grow(),
        desc="Resize window to the left"),
    Key([mod, "control"], "l", lazy.layout.shrink(),
        desc="Resize window to the right"),
    Key([mod, "control"], "j", lazy.layout.shrink(),
        desc="Resize window down"),
    Key([mod, "control"], "k", lazy.layout.grow(), desc="Resize window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset window sizes"), 

    # Window Manager Controls
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    # Launch applications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show run"), desc="Spawn rofi launcher"),
]

### WORKSPACES ###
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

### LAYOUTS ###
layouts = [
    layout.MonadTall(
        margin=4,
        border_focus='#bf7ceb',
        border_normal='#0c0d12',
        ),
    layout.Max(),
    layout.Floating(),
    layout.TreeTab(
        font='Hermit',
        fontsize=10,
        bg_color='#0b0c17',
        active_bg='#74c8ef',
        active_fg='#0c0d12',
        inactive_bg='#808080',
        panel_width=220,
        padding_y=6,
        ),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

### FLOATING LAYOUT AND RULES ###
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='mate-calc'), # calculator
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"

### QTILE BAR ###

# Font information
widget_defaults = dict(
    font= 'Hermit',
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()
spacer = widget.TextBox(" ", name="spacer",)
separator = widget.TextBox("|", name="separator", foreground='#ffffff',)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    this_current_screen_border='ef80ac',
                    highlight_method='line',
                    rounded=False,
                    borderwidth=1,
                    inactive='#808080',
                    ),
                separator,
                widget.WindowName(
                    foreground='#74c8ef',
                    ),
                widget.Systray(),
                separator,
                widget.TextBox(
                    "bat :",
                    foreground='#bf7ceb',
                    ),
                widget.Battery(
                    format='{percent:2.0%}',
                    foreground='#bf7ceb',
                    ),
                separator,
                widget.TextBox(
                    "vol :",
                    foreground='#8af331',
                    ),
                widget.Volume(
                    foreground='#8af331',
                    ),
                separator,
                widget.CurrentLayout(
                    foreground='#e184a8',
                    ),
                separator,
                widget.Clock(
                    format='%a %d, %H:%M',
                    foreground='#74c8ef',
                    ),
            ],
            24,
            background='#0b0c17',
        ),
    ),
]

### STARTUP HOOK ###
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("/home/labibmahmud/.config/qtile/autostart.sh") 
    subprocess.call([home])
