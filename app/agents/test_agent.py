
from app.agents.graph import research_graph


def main():
    initial_state = {
        "topic": "Artificial Intelligence",
        "research_plan": [],
        "status": "pending",
    }

    result = research_graph.invoke(initial_state)

    print("\nRESEARCH AGENT OUTPUT")
    print("---------------------")

    print("Topic:", result["topic"])
    print("Status:", result["status"])

    print("\nResearch Plan:")

    for index, task in enumerate(result["research_plan"], start=1):
        print(f"{index}. {task}")


if __name__ == "__main__":
    main()
