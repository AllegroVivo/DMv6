from typing     import List
################################################################################

__all__ = ("_EVENT_REFERENCE",)

################################################################################
# This list denotes all registered event names within the application.
# The comment column provides the type of context expected by the callback
# subscribed to a given event.
# ===========================================================================
_EVENT_REFERENCE: List[str] = [
    "on_attack",
    "on_death",
]
################################################################################
