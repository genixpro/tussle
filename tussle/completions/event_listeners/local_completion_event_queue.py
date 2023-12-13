from .completion_event_listener_base import CompletionEventListenerBase
import queue

class LocalCompletionEventQueue(CompletionEventListenerBase):
    def __init__(self):
        self.queue = queue.Queue()

    def __call__(self, event):
        self.queue.put(event)

    def get(self, *args, **kwargs):
        return self.queue.get(*args, **kwargs)

    def empty(self):
        return self.queue.empty()
