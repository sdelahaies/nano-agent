import json
from huggingface_hub import InferenceClient
from tools import FUNCTION_REGISTRY,TOOLS
from typing import Dict
SYSTEM_PROMPT = """You are a highly capable AI assistant that can perform complex tasks by breaking them down into smaller steps. 
You have access to various tools to help you accomplish your goals. 

Guidelines:
1. Think step by step to solve complex problems
2. Use tools when needed to gather information or perform actions
3. If a tool fails, try alternative approaches
4. Always verify your work before providing final answers
5. Ask clarifying questions if the user request is ambiguous

Available tools:
{TOOLS}
"""


def execute_tool(tool_call):
    """Execute a registered function based on the tool call"""
    tool_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    func = FUNCTION_REGISTRY.get(tool_name)
    if not func:
        return f"Error: Unknown tool '{tool_name}'"
    
    try:
        return func(**args)
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"


class LLMAgent:
    def __init__(self, 
                #  model: str = "deepseek-ai/DeepSeek-V3-0324"
                base_url: str = "http://localhost:11434/",
                model:str="qwen3:0.6b",
                headers: Dict = {"model":"qwen3:0.6b"}
                 
                 ):
        self.client = InferenceClient(headers=headers,base_url=base_url)
        self.model = model
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT.format(TOOLS=TOOLS)}
        ]
    
    def run(self, user_input: str, max_iterations: int = 5) -> str:
        """Run the agent with the given user input"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        for step in range(max_iterations):
            # print("step",step)
            response = self.client.chat_completion(
                model=self.model,
                messages=self.conversation_history,
                tools=TOOLS
            )
            
            assistant_message = response.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": getattr(assistant_message, "tool_calls", None)
            })

            if not getattr(assistant_message, "tool_calls", None):
                return assistant_message.content
            print("tool call:",assistant_message.tool_calls)
            tool_responses = []
            for tool_call in assistant_message.tool_calls:
                tool_result = execute_tool(tool_call)
                tool_responses.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": tool_result
                })

            self.conversation_history.extend(tool_responses)

            print("result:",tool_responses)
            # Let LLM decide what to do next after seeing the tool output
            response = self.client.chat_completion(
                model=self.model,
                messages=self.conversation_history,
                tools=TOOLS,
                temperature=0.1
            )
            assistant_message = response.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": getattr(assistant_message, "tool_calls", None)
            })

            if not getattr(assistant_message, "tool_calls", None):
                return assistant_message.content

        return "Maximum iterations reached without completing the task."

    def clear_history(self):
        """Reset the conversation history"""
        self.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT.format(TOOLS=TOOLS)}
        ]





                                                                                                   
                                                                                                   
                                                                                                   
                                            
                                                                                                                  
                                                                                                                  

