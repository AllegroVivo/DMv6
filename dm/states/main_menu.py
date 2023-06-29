from __future__ import annotations

from typing     import TYPE_CHECKING, Optional

from dm.states._vert_menu import VerticalMenuState
from utilities      import *

if TYPE_CHECKING:
    from pygame.event   import Event

    from dm.core  .game import DMGame
################################################################################

__all__ = ("MainMenuState",)

################################################################################
class MainMenuState(VerticalMenuState):

    def __init__(self, game: DMGame):

        super().__init__(game, ["Debug", "New Game", "Quit"], "Main Menu")

################################################################################
    def handle_event(self, event: Event) -> Optional[str]:

        super().handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if self.selection == 0:
                    convert_all_webp()
                    self.next_state = "debug"
                elif self.selection == 1:
                    self.next_state = "new_game"
                elif self.selection == 2:
                    self.quit = True

        return

################################################################################
