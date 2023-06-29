from __future__ import annotations

from pygame.font    import Font
from typing         import TYPE_CHECKING, List, Optional, Tuple

from ..core.game.state  import DMState
from utilities      import *

if TYPE_CHECKING:
    from dm.core        import DMGame
    from pygame         import Surface
    from pygame.event   import Event
################################################################################

__all__ = ("MenuState",)

################################################################################
class MenuState(DMState):
    __slots__ = (
        "title",
        "options",
        "selection",
        "x_offset",
        "y_offset",
        "title_font",
        "option_font",
        "background_fill"
    )

################################################################################
    def __init__(
        self,
        game: DMGame,
        options: List[str],
        title: Optional[str],
        x_offset: int,
        y_offset: int,
        title_font: Optional[Font],
        option_font: Optional[Font],
        bg_fill: Optional[Tuple[int, int, int, int]]
    ):

        super().__init__(game)

        self.title: Optional[str] = title

        self.options: List[str] = options
        self.selection: int = 0

        self.x_offset: int = x_offset
        self.y_offset: int = y_offset
        
        self.title_font: Optional[Font] = title_font or Font(None, 60)
        self.option_font: Optional[Font] = option_font or Font(None, 48)

        self.background_fill: Tuple[int, int, int, int] = bg_fill or BLACK

################################################################################
    def handle_event(self, event: Event) -> Optional[str]:

        pass

################################################################################
    def update(self, dt: float) -> bool:

        pass

################################################################################
    def draw(self, screen: Surface) -> None:

        screen.fill(self.background_fill)

        if self.title is not None:
            title = self.title_font.render(self.title, True, WHITE)
            title_rect = title.get_rect()
            title_rect.center = (
                SCREEN_WIDTH // 2 + self.x_offset,
                SCREEN_HEIGHT // 5 + self.y_offset
            )
            screen.blit(title, title_rect)

################################################################################
