from __future__ import annotations

import pygame
import sys

from pygame         import Surface, Vector2
from pygame.time    import Clock
from typing         import TYPE_CHECKING, Callable, List, Optional, Type, Union

from dm.core.game.dungeon       import DMDungeon
from dm.core.game.day           import DMDay
from dm.core.game.events        import DMEventManager
from dm.core.game.objpool       import DMObjectPool
from dm.core.game.rng           import DMGenerator
from dm.core.game.state_mgr     import DMStateMachine
from utilities      import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("DMGame",)

################################################################################
class DMGame:
    """The main game class. This is the class that is instantiated and run.
    It is responsible for managing the game loop, the state machine, the
    event manager, and so on.

    Attributes:
    -----------
    _screen: :class:`Surface`
        The main screen surface.

    _clock: :class:`Clock`
        The main game clock.

    _running: :class:`bool`
        Whether or not the game is running. Setting this to True will immediately
        exit the game loop.

    _dungeon: :class:`DMDungeon`
        The main dungeon object. Contains the map grid.

    _state_machine: :class:`DMStateMachine`
        The main state machine. Responsible for managing the game states.

    _inventory: :class:`DMInventory`
        The main inventory object. Contains the Dark Lord's gold, souls, monsters, etc.

    _fateboard: :class:`DMFateBoard`
        The game's Fate Board. 11 x 20 grid of Fate cards. Reset every 20 days.

    _battle_mgr: :class:`DMBattleManager`
        The game's battle manager. Responsible for managing battles.

    _objpool: :class:`DMObjectPool`
        The game's object pool. Responsible for spawning objects.

    _relics: :class:`DMRelicManager`
        The game's relic manager. Responsible for managing relics.

    _day: :class:`DMDay`
        The game's day object. Contains the current day and other related data.

    _events: :class:`DMEventManager`
        The game's event manager. Responsible for managing and dispatching events.

    _dark_lord: :class:`DMDarkLord`
        The game's Dark Lord object. Contains the Dark Lord's stats and other data.

    _rng: :class:`DMGenerator`
        The game's random number generator. Responsible for generating random
        numbers and selections.

    Properties:
    -----------
    spawn: :class:`DMObjectPool`
        The game's object pool. Responsible for spawning objects.

    day: :class:`DMDay`
        The game's day object. Contains the current day and other related data.

    Methods:
    --------
    run() -> None
        Run the game loop.

    quit() -> None
        Quit the game.

    handle_events() -> None
        Handle pygame events.

    subscribe_event(event: str, callback: Callable) -> None
        Subscribe a callback to an event type.


    """

    __slots__ = (
        "_screen",
        "_clock",
        "_running",
        "_dungeon",
        "_state_machine",
        "_inventory",
        "_fateboard",
        "_battle_mgr",
        "_objpool",
        "_relics",
        "_day",
        "_events",
        "_dark_lord",
        "_rng"
    )

################################################################################
    def __init__(self):

        pygame.init()

        self._screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock: Clock = Clock()
        self._running: bool = True

        self._day: DMDay = DMDay(self)

        # Order is important here.
        self._rng: DMGenerator = DMGenerator(self)
        self._events: DMEventManager = DMEventManager(self)
        self._state_machine: DMStateMachine = DMStateMachine(self)
        self._objpool: DMObjectPool = DMObjectPool(self)
        self._dungeon: DMDungeon = DMDungeon(self)
        # self._fateboard: DMFateBoard = DMFateBoard(self)
        # self._dark_lord: DMDarkLord = DMDarkLord(self)
        # self._inventory: DMInventory = DMInventory(self)
        # self._relics: DMRelicManager = DMRelicManager(self)
        # self._battle_mgr: DMBattleManager = DMBattleManager(self)

################################################################################
    def run(self) -> None:
        """Run the game.

        This is the main game loop. It is responsible for updating the game
        states, drawing the game states, and handling pygame events.
        """

        # Start the game in the main menu state.
        self._state_machine.push_state("main_menu")

        # Main game loop.
        while self._running:
            dt = self._clock.tick(FPS) / 1000

            # Check for events in the event queue.
            self.handle_events()

            # Update and draw the current state.
            self._state_machine.update(dt)
            self._state_machine.draw(self._screen)

            # Flip the display.
            pygame.display.flip()

        # If we've exited the game loop, quit the game.
        self.quit()

################################################################################
    def handle_events(self) -> None:
        """Handle pygame events.

        This method is responsible for handling pygame events. It is called
        every frame in the game loop. It is responsible for handling the
        basic quit events, as well as passing all other events to the state
        machine. The state machine is then responsible for handling the events
        in the current state.
        """

        for event in pygame.event.get():
            # Close button was clicked.
            if event.type == pygame.QUIT:
                self._running = False
            # Escape key was pressed.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False

            self._state_machine.handle_event(event)

################################################################################
    @staticmethod
    def quit() -> None:
        """Immediately quit the game.

        This method is responsible for quitting the game. It is called when
        the game loop exits and can potentially be called from other places
        in the game if necessary.
        """

        pygame.quit()
        sys.exit()

################################################################################
    @property
    def spawn(self) -> DMObjectPool:
        """The game's object pool. Responsible for spawning objects.

        This property is a shortcut to the game's object pool. It is used
        to spawn objects in the game.
        """

        return self._objpool

################################################################################
    @property
    def day(self) -> DMDay:
        """The game's day object. Contains the current day and other related data.

        This property is a shortcut to the game's day object. It is used
        to get the current day and other related data.
        """

        return self._day

################################################################################
    @property
    def dungeon(self) -> DMDungeon:
        """The game's dungeon object. Contains the map grid.

        This property is a shortcut to the game's dungeon object. It is used
        to get the map grid and other dungeon-related data.
        """

        return self._dungeon

################################################################################
    def subscribe_event(self, event: str, callback: Callable) -> None:
        """Subscribe a callback to an event type.

        Parameters:
        -----------
        event: :class:`str`
            The event type to subscribe to.

        callback: :class:`Callable`
            The callback to subscribe.
        """

        self._events.subscribe(event, callback)

################################################################################
