from __future__ import annotations

from pygame.font import Font
from typing     import TYPE_CHECKING

from ..core.game.state import DMState
from utilities          import *

if TYPE_CHECKING:
    from pygame         import Surface
    from pygame.event   import Event

    from ..core.game.game    import DMGame
################################################################################

__all__ = ("_DebugState",)

################################################################################
class _DebugState(DMState):

    def __init__(self, game: DMGame):

        super().__init__(game)

################################################################################
    def handle_event(self, event: Event) -> None:

        if event.type == KEYDOWN:
            if event.key == K_TAB:
                self.game.dungeon.spawn_hero()

################################################################################
    def draw(self, screen: Surface) -> None:

        screen.fill(BLACK)
        self.game.dungeon.draw(screen)

################################################################################
    def update(self, dt: float) -> None:

        pass

################################################################################
