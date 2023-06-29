from typing import TYPE_CHECKING, Dict, Type

if TYPE_CHECKING:
    from ..core.game.state import DMState
################################################################################

__all__ = ("_STATE_MAPPINGS",)

################################################################################
from ._debug import _DebugState
from .main_menu import MainMenuState
################################################################################
_STATE_MAPPINGS: Dict[str, Type["DMState"]] = {
    "debug": _DebugState,
    "main_menu": MainMenuState,
}
################################################################################
