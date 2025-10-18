import os
from helium import start_chrome
from selenium.webdriver import ChromeOptions
from skyscope_sentinel.core.agent import SentinelAgent
from skyscope_sentinel.proactive.defense import start_proactive_agents

def main():
    """
    Initializes and runs the SkyScope Sentinel agent.
    """
    print("🚀 Starting SkyScope Sentinel...")

    # --- Browser control ---
    chrome_opts = ChromeOptions()
    chrome_opts.add_argument("--window-size=1200,900")
    chrome_opts.add_argument("--disable-infobars")
    chrome_opts.add_argument("--no-sandbox")

    try:
        start_chrome(headless=True, options=chrome_opts)
        print("🌐 Browser interface initialized.")
    except Exception as e:
        print(f"⚠️  Could not start browser. Some tools may not work. Error: {e}")


    # Initialize proactive agents
    start_proactive_agents()

    # Initialize the main agent
    sentinel = SentinelAgent()

    print("✅ SkyScope Sentinel is operational. Type 'exit' or 'quit' to end the session.\n")

    try:
        while True:
            task = input("🌌 Sentinel > ").strip()
            if task.lower() in ["exit", "quit"]:
                break

            if not task:
                continue

            response = sentinel.run_task(task)
            print(f"\n{response}\n")

    finally:
        sentinel.shutdown()
        print("👋 SkyScope Sentinel session terminated.")

if __name__ == "__main__":
    main()