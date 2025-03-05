import random
import json
import time
import requests
import os
import sys
from typing import Dict, Any, List
from colorama import Fore, init
from datetime import datetime, timezone, timedelta
from fake_useragent import UserAgent

# Initialize colorama
init(autoreset=True)

# Configuration
BASE_URL = "https://www.magicnewton.com/portal/api"
ENDPOINTS = {
    "user": "/user",
    "quests": "/quests",
    "user_quests": "/userQuests"
}
ROLL_QUEST_ID = "f56c760b-2186-40cb-9cbc-3af4a3dc20e2"
MIN_TASK_DELAY = 7  # seconds
MAX_TASK_DELAY = 14  # seconds
MIN_LOOP_DELAY = 24 * 60 * 60  # 24 hours in seconds
MAX_LOOP_DELAY = (24 * 60 * 60) + (77 * 60)  # 24 hours + 77 minutes in seconds

# Rainbow Banner
def rainbow_banner():
    os.system("clear" if os.name == "posix" else "cls")
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = """
  _______                          
 |     __|.--.--.---.-.-----.---.-.|
 |__     ||  |  |  _  |-- __|  _  |
 |_______||___  |___._|_____|___._|
          |_____|                   
    """

    banner_lines = banner.split('\n')

    for line in banner_lines:
        color_line = ""
        for i, char in enumerate(line):
            color_line += colors[i % len(colors)] + char
        sys.stdout.write(color_line + "\n")
        sys.stdout.flush()
        time.sleep(0.05)

# Utility functions
def log_info(message: str):
    print(f"{Fore.CYAN}[INFO] {message}")

def log_success(message: str):
    print(f"{Fore.GREEN}[SUCCESS] {message}")

def log_warning(message: str):
    print(f"{Fore.YELLOW}[WARNING] {message}")

def log_error(message: str):
    print(f"{Fore.RED}[ERROR] {message}")

def countdown_timer(seconds: int):
    for remaining in range(seconds, 0, -1):
        print(f"\r{Fore.YELLOW}⏱️ Waiting: {timedelta(seconds=remaining)}", end='')
        time.sleep(1)
    print(f"\r{Fore.GREEN}✅ Wait complete!{' ' * 20}")

def get_random_delay(min_sec: int, max_sec: int) -> int:
    return random.randint(min_sec, max_sec)

def format_separator(length: int = 70):
    return f"{Fore.CYAN}{'━' * length}"

# Class to manage API with cookies
class APIClient:
    def __init__(self, base_url: str, cookie: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.cookie = cookie

    def get_headers(self) -> Dict[str, str]:
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "id-ID,id;q=0.9",
            "content-type": "application/json",
            "cookie": self.cookie,
            "referer": "https://www.magicnewton.com/portal/rewards",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": UserAgent().random,
        }

    def make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                log_info(f"Sending GET request to {endpoint}")
                response = self.session.get(url, headers=self.get_headers(), timeout=30)
            else:  # POST
                log_info(f"Sending POST request to {endpoint}")
                response = self.session.post(url, headers=self.get_headers(), json=data, timeout=30)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            log_error(f"Request failed: {str(e)}")
            return {"error": str(e)}

    def roll_dice(self) -> Dict[str, Any]:
        data = {
            "questId": ROLL_QUEST_ID,
            "metadata": {
                "action": "ROLL"
            }
        }
        return self.make_request("/userQuests", method="POST", data=data)

    def complete_quest(self, quest_id: str) -> Dict[str, Any]:
        """Mencoba menyelesaikan tugas dengan mengirim permintaan POST ke /userQuests."""
        data = {
            "questId": quest_id,
            "metadata": {
                "action": "COMPLETE"  # Coba action "COMPLETE"
            }
        }
        return self.make_request(ENDPOINTS["user_quests"], method="POST", data=data)


# Main class for automation
class MagicNewtonAutomation:
    def __init__(self):
        log_info("Initializing Magic Newton Automation")
        
        # Load cookies from data.txt file
        self.cookies = self.load_cookies()

    def load_cookies(self) -> List[str]:
        try:
            with open('data.txt', 'r') as f:
                cookies = [line.strip() for line in f if line.strip()]
                if not cookies:
                    raise Exception("Cookie file is empty.")
                return cookies
        except FileNotFoundError:
            raise Exception("Cookie file not found.")

    def display_user_info(self, user_data: Dict[str, Any]):
        if not user_data or 'data' not in user_data:
            log_error("Failed to fetch user data")
            return

        user = user_data['data']
        print(f"\n{format_separator()}")
        log_success(f"User Profile:")
        print(f"🆔 ID: {user.get('id', 'Unknown')}")
        print(f"👤 Name: {user.get('name', 'Unknown')}")
        print(f"📧 Email: {user.get('email', 'Unknown')}")
        print(f"{format_separator()}")
        
    def check_roll_status(self, user_quests_data: Dict[str, Any]) -> bool:
        """Check if the daily dice roll has been completed."""
        if not user_quests_data or 'data' not in user_quests_data:
            log_warning("No quest data available.")
            return False

        roll_quest = next((q for q in user_quests_data['data'] if q['questId'] == ROLL_QUEST_ID), None)
        if roll_quest and roll_quest['status'] == "COMPLETED":
            log_info("Dice roll already completed.")
            return True
        else:
            log_info("Dice roll not completed yet.")
            return False

    def clear_inactive_tasks(self, quests_data: Dict[str, Any]) -> Dict[str, Any]:
        """Menghapus tugas yang tidak aktif dari data."""
        if not quests_data or 'data' not in quests_data:
            log_warning("No quest data available to clear.")
            return {"data": []}
        
        active_tasks = [task for task in quests_data['data'] if task['enabled']]
        log_info(f"Cleared inactive tasks. Remaining tasks: {len(active_tasks)}")
        return {"data": active_tasks}

    def run_automation(self):
        for cookie in self.cookies:
            try:
                api_client = APIClient(BASE_URL, cookie)
                current_time = datetime.now(timezone.utc)
                log_success(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

                # Get user data using cookie
                user_data = api_client.make_request(ENDPOINTS['user'])
                self.display_user_info(user_data)

                # Get quests data
                quests_data = api_client.make_request(ENDPOINTS['quests'])

                # Clear inactive tasks
                cleared_quests_data = self.clear_inactive_tasks(quests_data)

                # Loop melalui setiap quest dan coba selesaikan
                for quest in cleared_quests_data['data']:
                    quest_id = quest['id']
                    log_info(f"Attempting to complete quest with ID: {quest_id}")
                    complete_result = api_client.complete_quest(quest_id)
                    log_success(f"Quest complete result: {complete_result}")

                # Get user quests data
                user_quests_data = api_client.make_request(ENDPOINTS['user_quests'])

                # Check if dice roll is already completed
                if self.check_roll_status(user_quests_data):
                    log_info("Skipping dice roll as it is already completed.")
                    continue

                # Perform dice roll
                roll_result = api_client.roll_dice()
                log_success(f"Dice Roll Result: {roll_result}")

                # Task delay before next run
                task_delay = get_random_delay(MIN_TASK_DELAY, MAX_TASK_DELAY)
                log_info(f"Waiting {task_delay} seconds before processing next account")
                countdown_timer(task_delay)

            except Exception as e:
                log_error(f"Error processing account with cookie '{cookie}': {str(e)}")

if __name__ == "__main__":
    # Display the rainbow banner
    rainbow_banner()

    print(f"\n{Fore.GREEN}{'=' * 70}")
    print(f"{Fore.GREEN}🚀 Starting Magic Newton Automation v1.4")
    print(f"{Fore.GREEN}{'=' * 70}\n")

    automation = MagicNewtonAutomation()
    automation.run_automation()
