from typing import Protocol
from tussle.completions.event_listeners.completion_event import CompletionEvent


class CompletionEventListenerBase(Protocol):
    """
    This is a base class for any code that needs to events coming from completions as they
    are being generated.

    This is used, for example, to send SSE events down to a client for a completion.
    This allows the user to see what the AI is producing in near realtime
    on the client, rather than waiting for the entire event.
    """

    def __call__(self, event: CompletionEvent):
        raise NotImplementedError("__call__ is not implemented - this is an abstract base class")




