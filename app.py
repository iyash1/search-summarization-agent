import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from utils.helpers import user_input

# ------------------------------------
# Load environment variables
# ------------------------------------
print(f"{Fore.YELLOW}➡️ Loading environment variables... {Style.RESET_ALL}")

load_dotenv()
init(autoreset=True)

# Set environment variables (especially useful for LangChain integrations)
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
IS_AUTO_TEST_MODE = os.getenv("AUTOMATED_TESTING", "False").lower() == "true"

if not openai_api_key:
    raise ValueError(f"{Fore.RED} ➡️__OPENAI_API_KEY not found in environment variables. ❌ {Style.RESET_ALL}")
elif not tavily_api_key:
    raise ValueError(f"{Fore.RED} ➡️__TAVILY_API_KEY not found in environment variables. ❌ {Style.RESET_ALL}")
else:
    print(f""" {Fore.GREEN} ➡️__All API keys loaded successfully. ✅ {Style.RESET_ALL}""")

print(f"{Fore.YELLOW} ➡️__AUTO TEST MODE__ {Style.RESET_ALL}") if IS_AUTO_TEST_MODE else print(f"{Fore.YELLOW} ➡️__MANUAL MODE__ {Style.RESET_ALL}")
# --------------------------------
# Import workflows
# --------------------------------
from workflows.summarization import workflow_summarize
from workflows.summary_and_translation import workflow_summarize_and_translate
from workflows.summary_and_sentiment import workflow_summarize_and_analyze_sentiment
from tools.tavily_search import search_graph_tool
from tools.calculator_tool import calculator_tool

# ------------------------------------
# Start the application
# ------------------------------------
if __name__ == "__main__":
    try:
        # Welcome message with styling
        print(f"{Fore.YELLOW} --------------------------------------{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} 🤖__Welcome to the Search and Summarization Agent!__ {Style.RESET_ALL}")
        print(f"{Fore.YELLOW} --------------------------------------{Style.RESET_ALL}")

        # Main loop for user prompts
        while True:
            print(f"""
                {Fore.CYAN} 
                --------------------------------------
                SELECT A WORKFLOW TO RUN:
                --------------------------------------
                1. Summarize only
                2. Summarize and Translate to Spanish
                3. Summarize and Analyze Sentiment
                4. Search web for latest happenings
                5. Calculator tool
                6. Exit
                {Style.RESET_ALL}   
                   """)
            workflow_choice = input(f"{Fore.CYAN} ➡️ Enter the number of the workflow you want to run (1, 2, 3, 4, 5 or 6 to exit): {Style.RESET_ALL}").strip()
            if workflow_choice.strip() not in ["1", "2", "3", "4", "5", "6"]:
                print(f"{Fore.RED} ➡️ Invalid workflow choice. Please enter 1, 2, 3, 4, 5, or 6. ❌ {Style.RESET_ALL}")
                continue

            match workflow_choice.strip():
                case "1":
                    workflow_summarize(user_input(IS_AUTO_TEST_MODE))
                case "2":
                    workflow_summarize_and_translate(user_input(IS_AUTO_TEST_MODE))
                case "3":
                    workflow_summarize_and_analyze_sentiment(user_input(IS_AUTO_TEST_MODE))
                case "4":
                    search_graph_tool(user_input())
                case "5":
                    calculator_tool(user_input())
                case "6":
                    print(f"{Fore.RED} ➡️ Exiting the Search and Summarization Agent. Goodbye! 👋 {Style.RESET_ALL}")
                    break

    except Exception as e:
        print(f"{Fore.RED} ➡️ An error occurred: {e} ❌ {Style.RESET_ALL}")
