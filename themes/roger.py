from datetime import datetime

from libqtile import bar, widget


theme = {
    "bg_dark": [
        "#505050",
        "#303030",
        "#202020",
        "#101010",
        "#202020",
        "#303030",
        "#505050"
    ],
    "bg_light": [
        "#707070",
        "#505050",
        "#505050",
        "#505050",
        "#505050",
        "#707070"
    ],
    "font_color": [
        "#ffffff",
        "#ffffff",
        "#cacaca",
        "#707070"
    ],
    # groupbox
    "gb_selected": [
        "#707070",
        "#505050",
        "#404040",
        "#303030",
        "#404040",
        "#505050",
        "#707070"
    ],
    "gb_urgent": [
        "#ff0000",
        "#820202",
        "#820202",
        "#820202",
        "#820202",
        "#ff0000"
    ]
}

widget_defaults = {
    'font': 'sans',
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

# Define one Bar per supported screens, the last one will be duplicated if needed
top_bars = [
    bar.Bar(
        [
            widget.TextBox(text=u"◥", fontsize=40, padding=-1,
                           font="Arial",
                           foreground=theme["bg_dark"]),
            widget.GroupBox(borderwidth=0, padding=3, margin=0,
                            highlight_method="block", rounded=False,
                            this_current_screen_border=theme["gb_selected"],
                            urgent_border=theme["gb_urgent"],
                            active=theme["font_color"],
                            background=theme["bg_dark"],
                            ),
            widget.TextBox(text=u"◣", fontsize=40, padding=-1,
                           font="Arial",
                           foreground=theme["bg_dark"]),

            widget.DF(partition="/"),
            widget.Prompt(),
            widget.Clipboard(),
            widget.Clipboard(selection="PRIMARY"),

            widget.TextBox(text="", name="info"),

            widget.TextBox(text=u"◥", fontsize=40, padding=-1,
                           font="Arial",
                           foreground=theme["bg_dark"]),
            widget.TaskList(borderwidth=2, padding=2,
                            margin=2, highlight_method="border",
                            border=theme["gb_selected"],
                            background=theme["bg_dark"],
                            ),

            widget.Countdown(date=datetime(2014, 8, 22, 21, 0),
                             background=theme["bg_dark"],
                             final=False,
                             format="\xef\x84\x9b {D}d {H}h {M}m"),

            # system usage
            widget.CPUGraph(core=0, width=21, line_width=2,
                            graph_color='#0066FF',
                            fill_color=['#0066FF', '#001111'],
                            margin_x=0, border_width=1,
                            background=theme["bg_dark"],
                            ),
            widget.CPUGraph(core=1, width=21, line_width=2,
                            graph_color='#0066FF',
                            fill_color=['#0066FF', '#001111'],
                            margin_x=0, border_width=1,
                            background=theme["bg_dark"],
                            ),
            widget.MemoryGraph(width=42, line_width=2,
                               graph_color='#22BB44',
                               fill_color=['#11FF11', "#002200"],
                               border_width=1,
                               background=theme["bg_dark"],
                               ),
            widget.SwapGraph(width=42, line_width=2,
                             graph_color='#CC2020',
                             fill_color=['#FF1010', '#221010'],
                             border_width=1,
                             background=theme["bg_dark"],
                             ),

            widget.TextBox(text=u" ", background=theme["bg_dark"]),
            widget.TextBox(text=u"◣", fontsize=40, padding=-1,
                           font="Arial",
                           foreground=theme["bg_dark"]),

            widget.Volume(update_interval=0.2, emoji=True),

            widget.Systray(icon_size=14),
            widget.Clock(format='%d-%m-%y %H:%M', fontsize=13, padding=6),
        ],
        size=22,
        opacity=0.9
    )
]
