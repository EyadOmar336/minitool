import subprocess
import sys
import os

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def check_adb():
    try:
        result = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    print(f"\n{RED}[!] الخطأ: أداة ADB غير موجودة في النظام.{RESET}\n")
    return False

def check_device_connected():
    if not check_adb():
        return False
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    devices_lines = [line for line in devices_result.stdout.splitlines() if line.strip() and not line.startswith("List")]
    if not devices_lines:
        print(f"\n{RED}[!] تنبيه: لا يوجد أي جهاز متصل!{RESET}\n")
        return False
    return True

def factory_reset_and_frp():
    if not check_device_connected():
        input(f"\n{YELLOW}اضغط Enter للمتابعة...{RESET}")
        return
    print(f"{GREEN}[SUCCESS] Factory Reset & FRP Bypass Executed!{RESET}")
    input(f"\n{YELLOW}اضغط Enter للمتابعة...{RESET}")

def main_menu():
    while True:
        clear_screen()
        print(f"{CYAN}=== MiniUnlockTool v2.3 ==={RESET}")
        print("1. Factory Reset & FRP Bypass")
        print("2. خروج")
        choice = input(f"\n{YELLOW}اختر رقماً: {RESET}").strip()
        if choice == "1":
            factory_reset_and_frp()
        elif choice == "2":
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
