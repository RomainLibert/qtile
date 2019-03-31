from libqtile import bar, widget

colors = {
  "color": [
    "#0b1e14",
    "#684228",
    "#2c5c4b",
    "#c87d3d",
    "#5f9a87",
    "#46b434",
    "#3dc48d",
    "#baece5",
    "#779898",
    "#b1411c",
    "#407a69",
    "#ecba72",
    "#87c8ba",
    "#67cd43",
    "#45eabb",
    "#d9ffff"
  ],
  "foreground": "#93a1a1",
  "background": "#2f3f37"
}

widget_defaults = {
    'font': 'Arial',
    'fontsize': 12,
    'padding': 3,
    'foreground': colors['foreground'],
    'background': colors['background'],
}


layout_theme = {
    'border_width': 2,
    'margin': 0,
    'border_focus': colors['color'][9],
    'border_normal': colors['color'][2],
}

top_bar = True
bottom_bar = False

def _get_interface():
    with open('/proc/net/dev', 'r') as f:
        for line in f:
            info = line.split()
            if len(info) > 10 and info[0] not in ['lo:', 'face'] and float(info[1]) > 0:
                return info[0][:-1]

interface = _get_interface()

top_bars = [
    bar.Bar([
        widget.CurrentScreen(
            active_color=colors['color'][13],
        ),
        widget.Sep(padding=8, linewidth=2),
        widget.GroupBox(borderwidth=0, padding=3, margin=0,
            highlight_method='block',
            this_current_screen_border=colors['color'][1],
            urgent_border=colors['color'][9],
            active=colors['color'][13],
            inactive=colors['color'][12]),
        widget.Prompt(),
        widget.TaskList(highlight_method='block', 
            urgent_border=colors['color'][9], 
            icon_size=0, 
            border=colors['color'][10],
            foreground=colors['color'][7],
        ),
        widget.Pacman(),
        widget.TextBox(text='Updates'),
        widget.Sep(padding=4),
        widget.TextBox(text='Vol'),
        widget.Volume(),
        widget.Sep(padding=4),
        widget.DF(visible_on_warn=False,
            format='Disk free {r:.1f}%'
        ),
        widget.Sep(padding=4),
        widget.Memory(),
        widget.CPUGraph(graph_color=colors['color'][11], 
            border_width=0
        ),
#        widget.ThermalSensor(),
        widget.Net(interface=interface),
        widget.Notify(),
        widget.Sep(padding=8),
        widget.Clock(format='%H:%M %d-%m-%Y', padding=6),
        widget.CurrentLayoutIcon(),
    ], 24),
]
