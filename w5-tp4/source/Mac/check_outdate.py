import subprocess

def check_outdated_appstore_apps():
    try:
        # Run 'mas outdated' command
        result = subprocess.run(["mas", "outdated"], capture_output=True, text=True)
        output = result.stdout.strip()

        if not output:
            print("✅ All App Store apps are up to date.")
            return

        print("📦 Outdated App Store applications:\n")
        print(output)
    except FileNotFoundError:
        print("❌ 'mas' is not installed. Please install it using 'brew install mas'.")

if __name__ == "__main__":
    check_outdated_appstore_apps()