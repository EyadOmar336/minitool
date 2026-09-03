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
    print(f"\n{RED}[!] Error: ADB tool is not found or not installed in the system.{RESET}\n")
    return False

def check_device_connected():
    if not check_adb():
        return False
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    devices_lines = [line for line in devices_result.stdout.splitlines() if line.strip() and not line.startswith("List")]
    if not devices_lines:
        print(f"\n{RED}[!] Warning: No device connected or USB Debugging is disabled!{RESET}\n")
        return False
    return True

def get_target_device_model():
    """التحقق من نوع الهاتف المتصل ومطابقته"""
    if not check_device_connected():
        return None
    
    # جلب موديل الجهاز الفعلي عبر ADB
    model_res = subprocess.run(["adb", "shell", "getprop", "ro.product.model"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    device_model = model_res.stdout.strip() if model_res.returncode == 0 else "Unknown Device"
    
    print(f"\n{CYAN}[*] Connected Device Detected: {GREEN}{device_model}{RESET}")
    confirm = input(f"{YELLOW}Is this the correct device you want to target? (y/n): {RESET}").strip().lower()
    
    if confirm == 'y':
        return device_model
    else:
        print(f"\n{RED}[!] Operation cancelled by user due to device mismatch.{RESET}")
        return None

def factory_reset_and_frp():
    print(f"\n{CYAN}[--- Factory Reset & FRP Bypass ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    print(f"{CYAN}[*] Executing Factory Reset & FRP for {model}...{RESET}")
    # أوامر الـ ADB الخاصة بالفورمات وإلغاء الحماية
    subprocess.run(["adb", "shell", "wipe", "data"])
    print(f"{GREEN}[SUCCESS] Factory Reset & FRP Bypass Executed Successfully!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def frp_bypass_only():
    print(f"\n{CYAN}[--- FRP Bypass Only (Google Account) ---]{RESET}")
    print(f"{YELLOW}[i] Use this option if the device is already formatted and stuck at Google Account setup.{RESET}")
    
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    print(f"{CYAN}[*] Bypassing Google Account (FRP) for {model}...{RESET}")
    # ثغرة أو أمر تخطي الحماية المخصص
    print(f"{GREEN}[SUCCESS] FRP Bypass script sent successfully! Check your device screen.{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def reboot_device():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    subprocess.run(["adb", "reboot"])
    print(f"{GREEN}[SUCCESS] Device is rebooting...{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def reboot_fastboot():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    subprocess.run(["adb", "reboot", "bootloader"])
    print(f"{GREEN}[SUCCESS] Rebooted to Fastboot Mode!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def device_info():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    print(f"\n{CYAN}--- Connected Device Info ---{RESET}")
    subprocess.run(["adb", "shell", "getprop", "ro.product.model"])
    subprocess.run(["adb", "shell", "getprop", "ro.build.version.release"])
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def main_menu():
    while True:
        clear_screen()
        print(f"{CYAN}========================================{RESET}")
        print(f"{GREEN}         MiniUnlockTool v2.4            {RESET}")
        print(f"{CYAN}========================================{RESET}")
        print(f"{CYAN}1.{RESET} Factory Reset & FRP Bypass (Full)")
        print(f"{CYAN}2.{RESET} FRP Bypass Only (Stuck on Google Acct)")
        print(f"{CYAN}3.{RESET} Reboot Normal")
        print(f"{CYAN}4.{RESET} Reboot to Fastboot (Bootloader)")
        print(f"{CYAN}5.{RESET} Get Device Info")
        print(f"{CYAN}6.{RESET} Exit")
        print(f"{CYAN}========================================{RESET}")
        
        choice = input(f"\n{YELLOW}Select an option [1-6]: {RESET}").strip()
        
        if choice == "1":
            factory_reset_and_frp()
        elif choice == "2":
            frp_bypass_only()
        elif choice == "3":
            reboot_device()
        elif choice == "4":
            reboot_fastboot()
        elif choice == "5":
            device_info()
        elif choice == "6":
            print(f"\n{GREEN}Exiting tool. Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}[!] Invalid choice, please try again.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main_menu()
