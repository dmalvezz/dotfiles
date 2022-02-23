# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.layout.floating import Floating
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

from max_margins import MaxMargins

# from libqtile.command import lazy
from datetime import datetime as dt
import os
import subprocess
import time
# from libqtile.utils import send_notification
from libqtile.log_utils import logger

# Get the number of connected screens
def get_monitors():
    xr = subprocess.check_output('xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors

monitors = get_monitors()

#Check if another instance of an app is running, otherwise start a new one.
def run_once(cmdline):
    cmd = cmdline.split(' ')
    try:
        subprocess.check_call(['pgrep', cmd[0]])
    except:
        subprocess.Popen(cmd)


# Run autorandr --change and restart Qtile on screen change
@hook.subscribe.screen_change
def set_screens(event):
    subprocess.run(["autorandr", "--change"])
    # lazy.spawn("mydock")
    qtile.restart()

# When application launched automatically focus it's group
@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break

# Hook to fallback to the first group with windows when last window of group is killed
#@hook.subscribe.client_killed
#def fallback(window):
#    if window.group.windows != [window]:
#        return
#    idx = qtile.groups.index(window.group)
#    for group in qtile.groups[idx - 1::-1]:
#        if group.windows:
#            qtile.current_screen.toggle_group(group)
#            return
#    qtile.current_screen.toggle_group(qtile.groups[0])

# Workspaces
workspaces = [
    {"name": " ₁", "key": "1", "layout": "monadtall"},
    {"name": " ₂", "key": "2", "layout": "monadtall"},
    {"name": " ₃", "key": "3", "layout": "monadtall"},
    {"name": " ₄", "key": "4", "layout": "monadtall"},
    {"name": " ₅", "key": "5", "layout": "monadtall"},
    {"name": "阮 ₆", "key": "6", "layout": "monadtall"},
    {"name": " ₇", "key": "7", "layout": "monadtall"},
    {"name": " ₈", "key": "8", "layout": "monadtall"},
    {"name": " ₉", "key": "9", "layout": "monadtall"},
]

# Move window to dedicated workspaces
@hook.subscribe.client_new
def slight_delay(window):
    wmclass = window.window.get_wm_class()[0]

    match = {
        'spotify': 5,
        'telegram-desktop': 3,
    }

    if wmclass in match.keys():
        ws = workspaces[match[wmclass]]
        window.togroup(ws['name']) 

    # Work around for matching Spotify
    time.sleep(0.04)
       
# Autostart
@hook.subscribe.startup_complete
def autostart():
    run_once('picom')
    run_once('telegram-desktop')
    run_once('spotify')

# Date format
def custom_date():
    return dt.now().strftime('%A %d %B %Y - %H:%M')


mod = "mod4"
terminal = guess_terminal()
home = os.path.expanduser('~')

MYCOLORS = [
    '#073642',
    '#dc322f',
    '#00ff2a',
    '#b58900',
    '#268bd2',
    '#d33682',
    '#2aa198',
    '#eee8d5'
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

keys = [
    Key([mod], "Up", lazy.layout.up(), desc="Move focus down in stack pane"),    
    Key([mod], "Down", lazy.layout.down(), desc="Move focus up in stack pane"),
    Key([mod], "Left", lazy.layout.left(), desc="Move focus left in stack pane"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus right in stack pane"),

    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc='Shuffle down'),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc='Shuffle up'),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc='Shuffle left'),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc='Shuffle right'),

    Key([mod, "control"], "Down", lazy.layout.grow(), desc='Grow down'),
    Key([mod, "control"], "Up", lazy.layout.shrink(), desc='Grow up'),
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc='Grow left'),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc='Grow right'),

    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggle bars"),
    Key([mod], "f", lazy.group.setlayout('max'), lazy.hide_show_bar(position='all'), desc='Toggle fullscreen and the bars'),
    Key([mod], "n", lazy.layout.normalize(), desc='Normalize window size ratios'),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle window between minimum and maximum sizes'),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),    
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "space", lazy.layout.next(), desc="Switch window focus to other pane(s) of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),    

    # Qtile system keys
    Key([mod, "shift", "control"], "Right", lazy.spawn("betterlockscreen -l"), desc="Lock screen"),    
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),    
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),    
    Key([mod, "control"], "p", lazy.spawn("" + home + "/.local/bin/powermenu"), desc="Launch Power menu"),

    # ------------ Hardware Configs ------------
    # Volume
    Key([], "XF86AudioMute", lazy.spawn(home + "/.local/bin/statusbar/volumecontrol mute"), desc='Mute audio' ),
    Key([], "XF86AudioLowerVolume", lazy.spawn(home + "/.local/bin/statusbar/volumecontrol down"), desc='Volume down' ),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(home + "/.local/bin/statusbar/volumecontrol up"), desc='Volume up' ),

    # Media keys
    Key([], "XF86AudioPlay", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.PlayPause"), desc='Audio play' ),
    Key([], "XF86AudioNext", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Next"), desc='Audio next' ),
    Key([], "XF86AudioPrev", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Previous"), desc='Audio previous' ),

    # Brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol down"), desc='Brightness down' ),
    Key([], "XF86MonBrightnessUp", lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol up"), desc='Brightness up' ),

    # Screenshots
    # Save screen to clipboard
    Key([], "Print", lazy.spawn("escrotum -C"), desc='Save screen to clipboard' ),
    # Save screen to screenshots folder
    Key([mod], "Print", lazy.spawn("escrotum " + home + "/Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png"), desc='Save screen to screenshots folder' ),
    # Capture region of screen to clipboard
    Key([mod, "shift"], "Print", lazy.spawn("escrotum --select " + home + "/Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png"), desc='Capture region of screen to clipboard' ),
]

# Groups with matches
groups = []
for workspace in workspaces:
    layouts = workspace["layout"] if "layout" in workspace else None
    groups.append(Group(workspace["name"], layout=layouts))

    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))

# Move focus to screen
for i in range(monitors):
    keys.extend([Key(["mod1"], str(i+1), lazy.to_screen(i))])

# Move window to screen with Mod, Alt and number+1
for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i+1), lazy.window.toscreen(i))])

# DEFAULT THEME SETTINGS FOR LAYOUTS #
layout_theme = {"border_width": 3,
                "margin": 8,
                "border_focus": BLUE,
                "border_normal": BLACK
                }

layouts = [
    layout.MonadTall(**layout_theme, single_border_width=0),
    #layout.Stack(num_stacks=2, **layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Columns(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.Matrix(),
    layout.MonadWide(**layout_theme),
    MaxMargins(**layout_theme),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(**layout_theme),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu Mono Nerd Font',
    fontsize='14',
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = []

for monitor in range(monitors):
    if monitor == 0:
        screens.append(
            Screen(
                top=bar.Bar(
                    [
                        widget.Spacer(length=10),
                        widget.GroupBox(borderwidth=2, inactive='969696', this_current_screen_border='eee8d5', this_screen_border='eee8d5', font='FiraCode Nerd Font', fontsize=18, highlight_method='line', highlight_color=['00000000', '00000000']),
                        # widget.CurrentLayoutIcon(scale=0.7),
                        # widget.CurrentLayout(**widget_defaults),
                        widget.Spacer(),
                        widget.Prompt(prompt='run:', **widget_defaults),
                        widget.Spacer(),
                        widget.Mpris2(
                            name='spotify',
                            objname="org.mpris.MediaPlayer2.spotify",
                            display_metadata=['xesam:title', 'xesam:artist'],
                            scroll_chars=None,
                            stop_pause_text='',
                            **widget_defaults
                        ),
                        widget.Spacer(length=8),
                        widget.Systray(),
                        widget.Spacer(length=8),
                        widget.GenPollText(update_interval=60, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/update.sh")).decode()),
                        widget.Spacer(length=8),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol down"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol up"), shell=True)}),
                        widget.Spacer(length=8),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/volumecontrol")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol down"), shell=True), 'Button2': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol mute"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol up"), shell=True)}),
                        widget.Spacer(length=8),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/battery.py")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/battery.py --c left-click"), shell=True)}),
                        widget.Spacer(length=8),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/network.sh")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/network.sh ShowInfo"), shell=True), 'Button3': lambda: qtile.cmd_spawn(terminal + ' -e nmtui', shell=True)}),
                        widget.Spacer(length=8),
                        widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh show"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh edit"), shell=True)}),
                        widget.Spacer(length=10),
                    ],
                    24,
                    background="#000000CC",
                    margin=[8, 8, 0, 8],  # N E S W
                ),
                wallpaper='~/.wallpapers/wallpaper.jpg',
                wallpaper_mode='fill',
            )
        )
    else:
        screens.append(
            Screen(
                wallpaper='~/.wallpapers/wallpaper.jpg',
                wallpaper_mode='fill',
            )
        )


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # *layout.Floating.default_float_rules,
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
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
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"

if monitors > 1:
    os.system('~/.screenlayout/vertical.sh')
