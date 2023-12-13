from tussle.completions.event_listeners.completion_event_listener_base import CompletionEventListenerBase


class UnitTestCompletionEventListener(CompletionEventListenerBase):
    """
    This class just stores up the list of events in a local array,
    which can later be queried against.
    """

    def __init__(self):
        """
        This initializes the provider.
        """
        super().__init__()

        self.events = []

    def __call__(self, event):
        self.events.append(event)



