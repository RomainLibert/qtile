from libqtile.command import lazy

BROWSER = 'google-chrome'

registered_functions = {
    'open_browser': lazy.spawn(BROWSER),
}
