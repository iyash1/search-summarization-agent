import os
from colorama import Fore, Style, init
from dotenv import load_dotenv
from utils.sample_prompts import sample_text

init(autoreset=True)

# Check if the input text is valid (not empty and not just whitespace)
def valid_input(text: str) -> bool:
    return bool(text and text.strip())

def user_input(is_auto_test: bool = False) -> str:
    if is_auto_test:
        return sample_text
    text = input(f"{Fore.CYAN}► Enter your query here : {Style.RESET_ALL}").strip()
    while not valid_input(text):
        print(f"{Fore.RED}❌ Invalid input! Please enter some text to summarize.{Style.RESET_ALL}")
        text = input(f"{Fore.CYAN}► Enter your query here : {Style.RESET_ALL}").strip()
    return text
