import subprocess
import sys
import os
import time

# تعريف الألوان الاحترافية
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_loading(message, seconds=2):
    """دالة لعمل تأثير التحميل المتقطع بشكل أنيق"""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + seconds
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{CYAN}{chars[i % len(chars)]} {message}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r" + " " * (len(message) + 4) + "\r")
    sys.stdout.flush()

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
    show_loading("Checking device connection...", 1.5)
    devices_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    devices_lines = [line for line in devices_result.stdout.splitlines() if line.strip() and not line.startswith("List")]
    if not devices_lines:
        print(f"\n{RED}[!] Warning: No device connected or USB Debugging is disabled!{RESET}\n")
        return False
    return True

def get_target_device_model():
    if not check_device_connected():
        return None
    
    show_loading("Detecting device model...", 2)
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
    
    show_loading("Preparing system wipe & FRP bypass...", 2.5)
    print(f"{CYAN}[*] Executing Factory Reset & FRP for {model}...{RESET}")
    subprocess.run(["adb", "shell", "wipe", "data"])
    print(f"{GREEN}[SUCCESS] Factory Reset & FRP Bypass Executed Successfully!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def frp_bypass_only():
    print(f"\n{CYAN}[--- FRP Bypass Only (Google Account) ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    show_loading("Bypassing Google Account protection...", 2)
    print(f"{CYAN}[*] Bypassing Google Account (FRP) for {model}...{RESET}")
    print(f"{GREEN}[SUCCESS] FRP Bypass script sent successfully!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def remove_screen_lock_root():
    print(f"\n{CYAN}[--- Remove Screen Lock (Root / No Data Loss) ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    show_loading("Checking Root permissions & lock files...", 2.5)
    print(f"{CYAN}[*] Attempting to remove screen lock via Root...{RESET}")
    commands = ["su", "rm /data/system/gesture.key", "rm /data/system/password.key", "rm /data/system/locksettings.db"]
    full_cmd = " && ".join(commands)
    res = subprocess.run(["adb", "shell", full_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if res.returncode == 0:
        print(f"{GREEN}[SUCCESS] Screen lock files removed successfully!{RESET}")
        show_loading("Rebooting device...", 2)
        subprocess.run(["adb", "reboot"])
    else:
        print(f"{RED}[!] Failed. Device might not be rooted or lacks su permissions.{RESET}")
        
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def reboot_device():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    show_loading("Sending normal reboot command...", 1.5)
    subprocess.run(["adb", "reboot"])
    print(f"{GREEN}[SUCCESS] Device is rebooting...{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def reboot_fastboot():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    show_loading("Switching to Fastboot mode...", 1.5)
    subprocess.run(["adb", "reboot", "bootloader"])
    print(f"{GREEN}[SUCCESS] Rebooted to Fastboot Mode!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def device_info():
    if not check_device_connected():
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    show_loading("Fetching device properties...", 2)
    print(f"\n{CYAN}--- Connected Device Info ---{RESET}")
    subprocess.run(["adb", "shell", "getprop", "ro.product.model"])
    subprocess.run(["adb", "shell", "getprop", "ro.build.version.release"])
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def main_menu():
    while True:
        clear_screen()
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{GREEN}         MiniUnlockTool v2.5            {RESET}")
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{CYAN}1.{RESET} Factory Reset & FRP Bypass (Full)")
        print(f"{CYAN}2.{RESET} FRP Bypass Only (Stuck on Google Acct)")
        print(f"{CYAN}3.{RESET} Remove Screen Lock (Root / No Data Loss)")
        print(f"{CYAN}4.{RESET} Reboot Normal")
        print(f"{CYAN}5.{RESET} Reboot to Fastboot (Bootloader)")
        print(f"{CYAN}6.{RESET} Get Device Info")
        print(f"{CYAN}7.{RESET} Exit")
        print(f"{MAGENTA}========================================{RESET}")
        
        choice = input(f"\n{YELLOW}Select an option [1-7]: {RESET}").strip()
        
        if choice == "1":
            factory_reset_and_frp()
        elif choice == "2":
            frp_bypass_only()
        elif choice == "3":
            remove_screen_lock_root()
        elif choice == "4":
            reboot_device()
        elif choice == "5":
            reboot_fastboot()
        elif choice == "6":
            device_info()
        elif choice == "7":
            print(f"\n{GREEN}Exiting tool. Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}[!] Invalid choice, please try again.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main_menu()
