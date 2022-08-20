class Theme:
    icon_dir = None
    main_background = (1, 1, 1, 1)
    entry_background = (1, 1, 1, 1)
    default_text_color = (0, 0, 0, 1)
    icon_button_background = (
        (0.8, 0.8, 0.8, 1), # Normal
        (0.9, 0.9, 1, 1), # Click
        (0.8, 0.8, 1, 1), # Hover
        (0.5, 0.5, 0.5, 1)) # Disabled
    text_button_background = (
        (0.8, 0.8, 0.8, 1), # Normal
        (0.9, 0.9, 1, 1), # Click
        (0.8, 0.8, 1, 1), # Hover
        (0.5, 0.5, 0.5, 1))
    scrollbar_controlls_color = (
        (0.8, 0.8, 0.8, 1), # Normal
        (0.9, 0.9, 1, 1), # Click
        (0.8, 0.8, 1, 1), # Hover
        (0.5, 0.5, 0.5, 1)) # Disabled
    scroll_background = (1, 1, 1, 1)
    popup_frame_background = (0.5,0.5,0.5,1)

    folder_background = (
        (0.9, 0.9, 0.9, 0), # Normal
        (0.95, 0.95, 1, 1), # Click
        (0.9, 0.9, 1, 1), # Hover
        (0.5, 0.5, 0.5, 1)) # Disabled
    file_background = (
        (0.9, 0.9, 0.9, 0), # Normal
        (0.95, 0.95, 1, 1), # Click
        (0.9, 0.9, 1, 1), # Hover
        (0.5, 0.5, 0.5, 1)) # Disabled
    unknown_image_tint = (0.9, 0.5, 0.5, 1)
    dialog_color = (0.9, 0.9, 0.9, 1)
    selected_background = (
        (0.05, 0.85, 0.85, 1), # Normal
        (0.95, 0.95, 1, 1), # Click
        (0.85, 0.85, 1, 1), # Hover
        (0.55, 0.55, 0.55, 1)) # Disabled
