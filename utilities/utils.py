import glob
import os
import pygame
import re

from dataclasses    import dataclass
from pygame         import Rect, Surface, Vector2
from pygame.font    import Font
from typing         import Any, Dict, List, Tuple, Union

from utilities.constants import GRID_PADDING, ROOM_SIZE, TEXT_ACCENT, WHITE, YELLOW

from PIL    import Image
################################################################################

__all__ = (
    "convert_all_webp",
    "rounded_rect",
    "text_to_multiline_str",
    "text_to_multiline_rect",
    "multicolor_text",
    "pixel_to_grid",
    "grid_to_topleft_pixel",
    "grid_to_center_pixel",
    "center_text",
    "class_to_file_name",
    "lerp",
)

################################################################################
def convert_all_webp() -> None:
    """For internal use as needed, not actually used in the game."""

    base = "assets/sprites"

    for webp_path in glob.glob(base + "/**/*.webp", recursive=True):
        img = Image.open(webp_path)

        parts = os.path.splitext(webp_path)
        extension = "GIF" if parts[0].split("\\")[2] == "idle" else "PNG"
        new_path = parts[0] + f".{extension.lower()}"

        img.save(new_path, extension)
        os.remove(webp_path)

################################################################################
def rounded_rect(
    dimensions: Tuple[int, int],
    color: Tuple[int, int, int, int],
    corner_radius: int = 20,
) -> pygame.Surface:
    """ Draws a rectangle with rounded corners using the provided arguments."""

    surface = pygame.Surface(dimensions)
    surface.fill((0, 0, 0))
    surface.set_colorkey((0, 0, 0))

    rect = surface.get_rect()
    if corner_radius < 0:
        raise ValueError(f"Rounded rectangle can't have negative corner radius")
    elif corner_radius == 0:
        pygame.draw.rect(surface, color, rect)
    else:
        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - 1, rect.top + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - 1, rect.bottom - corner_radius - 1),
                           corner_radius)
        pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius - 1), corner_radius)

        pygame.draw.rect(surface, color, rect.inflate(-2 * corner_radius, 0))
        pygame.draw.rect(surface, color, rect.inflate(0, -2 * corner_radius))

    return surface

################################################################################
def text_to_multiline_str(text: str, max_line_length: int) -> List[str]:

    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line) + ' ' + word) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))  # Add the last line

    return lines

################################################################################
def text_to_multiline_rect(text: str, rect: Rect, max_line_length: int, line_height: int) -> Dict[str, Rect]:

    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line) + ' ' + word) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))  # Add the last line

    line_rects = {}
    for i, line in enumerate(lines):
        line_rect = Rect(rect.x, rect.y + i * line_height, rect.width, line_height)
        line_rects[line] = line_rect

    return line_rects

################################################################################
def multicolor_text(
    text: str,
    surface: pygame.Surface,
    font: Font,
    pos: Union[pygame.Vector2, pygame.Rect]
):

    color_dict = {  # map tags to colors
        '[y]' : YELLOW,
        '[w]' : WHITE,
        '[a]' : TEXT_ACCENT
    }
    tag_pattern = r'\[\/?[a-z]\]'  # pattern to find tags

    lines = text_to_multiline_str(text, 25)  # split text into lines
    y = pos[1] + (surface.get_height() - len(lines) * font.get_height()) // 2

    for line in lines:
        parts = re.split(tag_pattern, line)  # split each line by tags
        tags = re.findall(tag_pattern, line)  # get list of all tags in the line
        color = (255, 255, 255)  # default color is white

        # Determine the total width of the line
        total_width = sum(font.size(part)[0] for part in parts)

        # Set x to the starting x-coordinate of the centered line
        x = pos[0] + (surface.get_width() - total_width) // 2

        for part, tag in zip(parts, tags + ['']):
            if tag in color_dict:
                color = color_dict[tag]
            img = font.render(part, True, color)
            surface.blit(img, (x, y))
            x += img.get_width()  # update x-coordinate

        y += font.get_height() + 3  # update y-coordinate

################################################################################
def pixel_to_grid(screen_position: Vector2) -> Vector2:

    grid_x = (screen_position.x - 50) // (ROOM_SIZE + GRID_PADDING)
    grid_y = (screen_position.y - 50) // (ROOM_SIZE + GRID_PADDING)

    return Vector2(grid_x, grid_y)

################################################################################
def grid_to_topleft_pixel(grid_position: Vector2) -> Vector2:

    pixel_x = (grid_position.x * (ROOM_SIZE + GRID_PADDING)) + 50
    pixel_y = (grid_position.y * (ROOM_SIZE + GRID_PADDING)) + 50

    return Vector2(pixel_x, pixel_y)

################################################################################
def grid_to_center_pixel(grid_x, grid_y):

    pixel_x = (grid_x * (ROOM_SIZE + GRID_PADDING) + ROOM_SIZE // 2) + 50
    pixel_y = (grid_y * (ROOM_SIZE + GRID_PADDING) + ROOM_SIZE // 2) + 50

    return Vector2(pixel_x, pixel_y)

################################################################################
def center_text(surface: Surface, text: Surface):

    text_rect = text.get_rect()
    text_rect.center = (surface.get_width() // 2, surface.get_height() // 2)
    surface.blit(text, text_rect)

################################################################################
def class_to_file_name(obj: Any):

    return ''.join(
        ['_' + i.lower() if i.isupper() else i for i in obj.__class__.__name__]
    ).lstrip('_')

################################################################################
def lerp(a: float, b: float, t: float) -> float:

    return a + (b - a) * t

################################################################################
