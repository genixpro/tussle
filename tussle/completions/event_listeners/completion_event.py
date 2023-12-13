from dataclasses import dataclass, field

class CompletionEventTypes:
    """ This represents the types of events that are sent while the completion"""
    start_node = "start_node"
    start_node_value_event = "start_node_value"
    word_event = "word"
    finish_node_value_event = "finish_node_value"
    withdraw_node_value_event = "withdraw_node_value"
    finish_all_values_for_node_event = "finish_all_values_for_node"

@dataclass(frozen=True, slots=True, kw_only=True)
class CompletionEvent:
    """ This represents events that are sent during the processing of a node within
    a prompt chart. It includes start and stop events for that node, start and stop
    events for individual completions within that node, and words for each word
    that was generated within a completion.
    """
    event: CompletionEventTypes
    chart_id: str
    node_id: str
    value_index: int | None
    word: str | None
