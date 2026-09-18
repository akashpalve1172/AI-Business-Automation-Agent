from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from llm_router import llm_route_question
from fast_rag import fast_rag_answer
from llm_sql_generator import generate_sql_with_llm
from sql_tool import execute_sql
from calculator_tool import calculate
from workflow_agent import process_business_request
from validation_agent import validate_result


# =========================================================
# State
# =========================================================

class WorkflowState(TypedDict, total=False):
    question: str
    route: str
    result: str
    validation_status: str
    validation_message: str
    final_answer: str


# =========================================================
# 1. Router Node
# =========================================================

def router_node(state: WorkflowState):
    question = state["question"]

    route = llm_route_question(question)

    return {
        "route": route
    }


# =========================================================
# 2. Fast RAG Node
# =========================================================

def rag_node(state: WorkflowState):
    question = state["question"]

    rag_result = fast_rag_answer(question)

    result = (
        f"Source: {rag_result['source']}\n\n"
        f"Relevant Policy Information:\n"
        f"{rag_result['context']}"
    )

    return {
        "result": result
    }


# =========================================================
# 3. SQL Node
# =========================================================

def sql_node(state: WorkflowState):
    question = state["question"]

    sql = generate_sql_with_llm(question)

    if not sql:
        return {
            "result": "The AI could not generate a SQL query."
        }

    database_result = execute_sql.invoke(sql)

    return {
        "result": (
            f"Generated SQL:\n{sql}\n\n"
            f"Database Result:\n{database_result}"
        )
    }


# =========================================================
# 4. Calculator Node
# =========================================================

def calculator_node(state: WorkflowState):
    question = state["question"]

    import re

    lower_question = question.lower()

    # Try to find a normal mathematical expression
    expression_match = re.search(
        r"\d+(?:\s*[\*\+\-/]\s*\d+)+",
        question
    )

    if expression_match:

        expression = expression_match.group()

    else:

        # Extract numbers from natural-language questions
        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            question
        )

        if len(numbers) < 2:
            return {
                "result": "Could not understand the calculation."
            }

        if (
            "multiply" in lower_question
            or "multiplied" in lower_question
            or "times" in lower_question
        ):
            expression = "*".join(numbers)

        elif (
            "add" in lower_question
            or "plus" in lower_question
        ):
            expression = "+".join(numbers)

        elif (
            "subtract" in lower_question
            or "minus" in lower_question
        ):
            expression = "-".join(numbers)

        elif (
            "divide" in lower_question
            or "divided" in lower_question
        ):
            expression = "/".join(numbers)

        else:
            return {
                "result": "Could not understand the calculation."
            }

    try:
        result = calculate(expression)

        return {
            "result": f"{expression} = {result}"
        }

    except Exception:
        return {
            "result": "Could not understand the calculation."
        }


# =========================================================
# 5. Workflow Node
# =========================================================

def workflow_node(state: WorkflowState):
    question = state["question"]

    result = process_business_request(question)

    return {
        "result": result
    }


# =========================================================
# 6. Unknown Node
# =========================================================

def unknown_node(state: WorkflowState):

    return {
        "result": (
            "I could not determine how to handle this question."
        )
    }


# =========================================================
# 7. Choose Route
# =========================================================

def choose_next_node(state: WorkflowState):

    route = state.get("route", "unknown")

    if route == "rag":
        return "rag"

    if route == "sql":
        return "sql"

    if route == "calculator":
        return "calculator"

    if route == "workflow":
        return "workflow"

    return "unknown"


# =========================================================
# 8. Validation Node
# =========================================================

def validation_node(state: WorkflowState):

    route = state.get("route", "unknown")
    result = state.get("result", "")

    validation = validate_result(
        route,
        result
    )

    return {
        "validation_status": validation["status"],
        "validation_message": validation["message"]
    }


# =========================================================
# 9. Final Response Node
# =========================================================

def final_response_node(state: WorkflowState):

    result = state.get("result", "")
    validation_status = state.get(
        "validation_status",
        "unknown"
    )

    if validation_status == "failed":

        return {
            "final_answer": (
                "The system could not validate the result.\n\n"
                + result
            )
        }

    return {
        "final_answer": result
    }


# =========================================================
# Build Graph
# =========================================================

graph = StateGraph(WorkflowState)


# ---------------------------------------------------------
# Nodes
# ---------------------------------------------------------

graph.add_node("router", router_node)
graph.add_node("rag", rag_node)
graph.add_node("sql", sql_node)
graph.add_node("calculator", calculator_node)
graph.add_node("workflow", workflow_node)
graph.add_node("unknown", unknown_node)
graph.add_node("validation", validation_node)
graph.add_node("final_response", final_response_node)


# ---------------------------------------------------------
# START → Router
# ---------------------------------------------------------

graph.add_edge(
    START,
    "router"
)


# ---------------------------------------------------------
# Router → Branch
# ---------------------------------------------------------

graph.add_conditional_edges(
    "router",
    choose_next_node,
    {
        "rag": "rag",
        "sql": "sql",
        "calculator": "calculator",
        "workflow": "workflow",
        "unknown": "unknown"
    }
)


# ---------------------------------------------------------
# Branch → Validation
# ---------------------------------------------------------

graph.add_edge("rag", "validation")
graph.add_edge("sql", "validation")
graph.add_edge("calculator", "validation")
graph.add_edge("workflow", "validation")
graph.add_edge("unknown", "validation")


# ---------------------------------------------------------
# Validation → Final Response
# ---------------------------------------------------------

graph.add_edge(
    "validation",
    "final_response"
)


# ---------------------------------------------------------
# Final Response → END
# ---------------------------------------------------------

graph.add_edge(
    "final_response",
    END
)


# =========================================================
# Compile
# =========================================================

app = graph.compile()


# =========================================================
# Reusable Assistant Function
# =========================================================

def run_assistant(question: str) -> dict:

    result = app.invoke({
        "question": question
    })

    return result


# =========================================================
# Terminal Version
# =========================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("       TECHNOVA AI BUSINESS ASSISTANT")
    print("==============================================")

    print("\nCapabilities:")
    print("1. Company Policy RAG")
    print("2. Employee SQL Database")
    print("3. Calculator")
    print("4. Business Workflow")

    print("\nType 'exit' to stop.")

    while True:

        question = input("\nYour question: ").strip()

        if question.lower() == "exit":

            print("\nAssistant stopped.")
            break

        if not question:

            print("Please enter a question.")
            continue

        result = run_assistant(question)

        print("\n" + "=" * 55)
        print("ROUTE")
        print("=" * 55)

        print(
            result.get(
                "route",
                "unknown"
            )
        )

        print("\n" + "=" * 55)
        print("FINAL RESULT")
        print("=" * 55)

        print(
            result.get(
                "final_answer",
                "No result."
            )
        )

        print("\n" + "=" * 55)
        print("VALIDATION")
        print("=" * 55)

        print(
            "Status:",
            result.get(
                "validation_status",
                "unknown"
            )
        )

        print(
            "Message:",
            result.get(
                "validation_message",
                "No validation message."
            )
        )