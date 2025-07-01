import sys
import signal
from nanoAgent import LLMAgent, TOOLS  # Assumes your agent is saved in agent.py
from model_selector import select_model
import yaml

ASCII_ART = r"""
 _______ _______ _______ _______ _______ 
|   _   |     __|    ___|    |  |_     _|
|       |    |  |    ___|       | |   |  
|___|___|_______|_______|__|____| |___|                                          
"""


def print_tools():
    print("\n🛠️  Available Tools:")
    for tool in TOOLS:
        func = tool["function"]
        print(f" - {func['name']}: {func['description']}")

def handle_exit(signal_received, frame):
    print("\n👋 Exiting Agent. Goodbye!")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handle_exit)

    print(ASCII_ART)
    print("🤖 Welcome to your terminal AI Agent!")
    print("I can use tools and help solve complex tasks by breaking them down.")
    print_tools()
    print()

    file_path="./config.yml"
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    models=data.get("models",[])
    base_url=data.get("base_url","")

    model = select_model(models)

    agent = LLMAgent(base_url=base_url,model=model)

    while True:
        try:
            user_input = input("\n🧑 You: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            print("\n🤖 Agent is thinking...\n")
            response = agent.run(user_input)
            print(f"🤖 Agent: {response}")
        except KeyboardInterrupt:
            handle_exit(None, None)

if __name__ == "__main__":
    main()

                                                                                                   
