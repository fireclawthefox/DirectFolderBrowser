import os
from panda3d.core import Filename

class Theme:
    icon_dir = ""
    main_background = (0.2, 0.2, 0.2, 1)
    entry_background = (0.2, 0.2, 0.2, 1)
    default_text_color = (0.8, 0.8, 0.8, 1)
    icon_button_background = (
        (0.2, 0.2, 0.2, 1),
        (0.3, 0.3, 0.5, 1),
        (0.2, 0.2, 0.5, 1),
        (0.1, 0.1, 0.1, 1))
    text_button_background = (
        (0.12, 0.12, 0.12, 1), # Normal
        (0.2, 0.2, 0.4, 1), # Click
        (0.2, 0.2, 0.4, 1), # Hover
        (0.1, 0.1, 0.1, 1)) # Disabled
    scrollbar_controlls_color = (
        (0.12, 0.12, 0.12, 1), # Normal
        (0.2, 0.2, 0.4, 1), # Click
        (0.2, 0.2, 0.4, 1), # Hover
        (0.1, 0.1, 0.1, 1)) # Disabled
    scroll_background = (0.2, 0.2, 0.2, 1)
    popup_frame_background = (0.25, 0.25, 0.25, 1)

    folder_background = (
        (0, 0, 0, 0), # Normal
        (0.15, 0.15, 0.25, 1), # Click
        (0.15, 0.15, 0.25, 1), # Hover
        (0.1, 0.1, 0.1, 1)) # Disabled
    file_background = (
        (0, 0, 0, 0), # Normal
        (0.15, 0.15, 0.25, 1), # Click
        (0.15, 0.15, 0.25, 1), # Hover
        (0.1, 0.1, 0.1, 1)) # Disabled
    unknown_image_tint = (0.9, 0.5, 0.5, 1)
    dialog_color = (0.18, 0.18, 0.18, 1)
    selected_background = (
        (0.15, 0.15, 0.15, 1),
        (0.25, 0.25, 0.45, 1),
        (0.15, 0.15, 0.35, 1),
        (0.05, 0.05, 0.05, 1))

    def __init__(self):
        fn = Filename.fromOsSpecific(os.path.dirname(__file__))
        fn.makeTrueCase()
        self.icon_dir = str(fn) + "/icons_dark"
