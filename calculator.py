import re
from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph

# 2 + (2 ^ 2/ 4) * 2
# (2 * 2) +1


class Equation(TypedDict):
    problem: str
    # total: int


def find_parenthesis(state: Equation):
    problem = state["problem"]
    pattern_for_parenthesis = r"\([^()]*\)"
    found = re.search(pattern_for_parenthesis, problem)
    print(found)
    if found:
        parenthesis_problem = found.group(0)
        print(parenthesis_problem)
        total = problem.replace(parenthesis_problem, str(eval(parenthesis_problem[1:-1])))
        state["problem"] = total
        print(f"using find_parenthesis method: {state['problem']}")
    return state


def add(state: Equation):
    add_one_part = state["problem"].split("+", 1)
    if len(add_one_part) == 2:
        first_num = float(add_one_part[0].strip())
        second_num = float(add_one_part[1].strip())
        total = first_num + second_num
        state["problem"] = str(total)
        print(f"using addition method: {state['problem']}")
    return state


def subtract(state: Equation):
    subtract_one_part = state["problem"].split("-", 1)
    if len(subtract_one_part) == 2:
        first_num = float(subtract_one_part[0].strip())
        second_num = float(subtract_one_part[1].strip())
        total = first_num - second_num
        state["problem"] = str(total)
        print(f"using subtract method: {state['problem']}")
    return state


def router(state: Equation):
    problem = state["problem"]
    if "(" in problem and ")" in problem:
        return "find_parenthesis"
    elif "+" in problem:
        return "add"
    elif "-" in problem:
        return "subtract"
    return END


builder = StateGraph(Equation)
builder.add_node("find_parenthesis", find_parenthesis)
builder.add_node("add", add)
builder.add_node("subtract", subtract)
builder.add_conditional_edges("find_parenthesis", router)
builder.add_conditional_edges("add", router)
builder.add_conditional_edges("subtract", router)


builder.add_edge(START, "find_parenthesis")
builder.add_edge("add", END)


graph = builder.compile()

initial_state = {"problem": "(2 + (2**2/ 4)) - 2", "total": 0}
graph.invoke(initial_state)
