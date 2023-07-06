from __future__ import annotations

from pygame     import Vector2
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

        battle_room = self.game.get_room_at(Vector2(4, 1))
        battle_room.deploy(self.game.spawn.monster("Bat", room=Vector2(4, 1)))
        battle_room.deploy(self.game.spawn.monster("Bat", room=Vector2(4, 1)))
        battle_room.deploy(self.game.spawn.monster("Bat", room=Vector2(4, 1)))

################################################################################
    def handle_event(self, event: Event) -> None:

        if event.type == KEYDOWN:
            if event.key == K_TAB:
                self.game.spawn_hero()
            elif event.key == K_INSERT:
                for hero in self.game.dungeon.heroes:
                    hero._moving = True
        elif event.type == KEYUP:
            if event.key == K_INSERT:
                for hero in self.game.dungeon.heroes:
                    hero._moving = False

################################################################################
    def draw(self, screen: Surface) -> None:

        screen.fill(BLACK)
        self.game.dungeon.draw(screen)

################################################################################
    def update(self, dt: float) -> None:

        self.game.dungeon.update(dt)
        self.game.battle_manager.update(dt)

################################################################################
