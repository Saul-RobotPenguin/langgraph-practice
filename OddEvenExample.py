from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph


class OddOrEvenState(TypedDict):
    number: int
    even: bool


def check_odd_or_even(state: OddOrEvenState):
    if state["number"] % 2 == 0:
        state["even"] = True
    return state


def print_even(state: OddOrEvenState):
    print(
        f"YAY its an even number {state['number']} is divisible by 2 with no remainder"
    )


def print_odd(state: OddOrEvenState):
    print(f"Gasp  {state['number']} is an odd number")


def router(state: OddOrEvenState):
    if state["even"]:
        return "print_even"
    return "print_odd"


builder = StateGraph(OddOrEvenState)
builder.add_node("check_odd_or_even", check_odd_or_even)
builder.add_node("print_even", print_even)
builder.add_node("print_odd", print_odd)
builder.add_conditional_edges("check_odd_or_even", router)
builder.add_edge(START, "check_odd_or_even")
builder.add_edge("print_even", END)
builder.add_edge("print_odd", END)


graph = builder.compile()
graph.invoke({"number": 12, "even": False})
