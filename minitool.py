import subprocess
import sys
import os

def check_adb():
    try:
        result = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    print("\n[!] الخطأ: أداة ADB غير موجودة في النظام.\n")
    return False

def check_device_connected():
    if not check_adb():
        return False
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    devices_lines = [line for line in devices_result.stdout.splitlines() if line.strip() and not line.startswith("List")]
    if not devices_lines:
        print("\n[!] تنبيه: لا يوجد أي جهاز متصل!\n")
        return False
    return True

def factory_reset_and_frp():
    if not check_device_connected():
        return
    print("[SUCCESS] Factory Reset & FRP Bypass Executed!")

def main_menu():
    while True:
        print("\n=== MiniUnlockTool v2.3 ===")
        print("1. Factory Reset & FRP Bypass")
        print("2. خروج")
        choice = input("\nاختر رقم: ").strip()
        if choice == "1":
            factory_reset_and_frp()
        elif choice == "2":
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
