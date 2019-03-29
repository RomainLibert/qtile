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
}


layout_theme = {
    'border_width': 2,
    'margin': 3,
    'border_focus': '#005F0C',
    'border_normal': '#555555'
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
        widget.GroupBox(borderwidth=0, padding=3, margin=0,
            highlight_method='block', rounded=False,
            this_current_screen_border=colors['color'][6],
            urgent_borer=colors['color'][9],
            active=colors['color'][4],
            background=colors['background']),
        widget.CurrentScreen(),
        widget.Prompt(),
        widget.TaskList(),
        widget.Pacman(),
        widget.Volume(),
        widget.Memory(),
        widget.CPUGraph(),
        widget.ThermalSensor(),
        widget.DF(visible_on_warn=False),
        widget.Net(interface=interface),
        widget.Notify(),
        widget.Clock(),
        widget.CurrentLayoutIcon(),
    ], 24),
]
