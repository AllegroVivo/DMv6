from __future__ import annotations

from typing     import TYPE_CHECKING, List, Optional, Tuple

from ._menu     import MenuState
from utilities  import *

if TYPE_CHECKING:
    from dm.core        import DMGame
    from pygame         import Surface
    from pygame.event   import Event
    from pygame.font    import Font
################################################################################

__all__ = ("VerticalMenuState",)

################################################################################
class VerticalMenuState(MenuState):

    def __init__(
        self,
        game: DMGame,
        options: List[str],
        title: Optional[str] = None,
        x_offset: int = 0,
        y_offset: int = 0,
        title_font: Optional[Font] = None,
        option_font: Optional[Font] = None,
        bg_fill: Optional[Tuple[int, int, int, int]] = None
    ):

        super().__init__(
            game, options, title, x_offset, y_offset,
            title_font, option_font, bg_fill)

################################################################################
    def handle_event(self, event: Event) -> Optional[str]:

        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selection = max(self.selection - 1, 0)
            elif event.key == K_DOWN:
                self.selection = min(self.selection + 1, len(self.options) - 1)

        return

################################################################################
    def update(self, dt: float) -> bool:

        pass

################################################################################
    def draw(self, screen: Surface) -> None:

        super().draw(screen)

        for i, option in enumerate(self.options):
            color = RED if i == self.selection else WHITE
            text = self.option_font.render(option, True, color)

            text_rect = text.get_rect()
            text_rect.center = (
                (SCREEN_WIDTH // 2) + self.x_offset,
                (SCREEN_HEIGHT // 2 + i * 50) + self.y_offset
            )

            screen.blit(text, text_rect)

################################################################################
