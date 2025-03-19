import pygame
import pygame_gui
from data_extraction import log_debug_info
from utils import display_text_correctly

# Function to render information in the info_pane
def render_info_pane(bid_info, info_pane, manager):
    # Clear all elements in the info_pane
    for element in info_pane.get_container().elements:
        element.kill()

    # Resize the info_pane
    info_pane.set_dimensions((info_pane.get_relative_rect().width, info_pane.get_relative_rect().height))

    y_offset = 0
    for key, value in bid_info.items():
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, y_offset), (info_pane.get_relative_rect().width, 30)), 
            text=f"<b>{key}:</b> {value}", 
            manager=manager, 
            container=info_pane
        )
        y_offset += 40
        log_debug_info(f"Rendered {key}: {value}", 'blue')
