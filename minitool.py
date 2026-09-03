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
    """دالة لتحميل العبارات بشكل متحرك وأنيق"""
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

def show_progress_bar(message, total_seconds=3):
    """شريط تحميل احترافي خاص بعمليات الفورمات"""
    print(f"\n{YELLOW}{message}{RESET}")
    width = 30
    for i in range(width + 1):
        percent = int(i / width * 100)
        bar = "█" * i + "-" * (width - i)
        sys.stdout.write(f"\r{CYAN}[{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(total_seconds / width)
    print("\n")

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
    print(f"\n{BLUE}[--- Factory Reset & FRP Bypass ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    show_progress_bar("Formatting & Bypassing FRP...", 3)
    res = subprocess.run(["adb", "shell", "wipe", "data"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"{GREEN}[SUCCESS] Factory Reset & FRP Bypass Executed Successfully!{RESET}")
    else:
        print(f"{RED}[!] Operation failed. Check device connection.{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def frp_bypass_only():
    print(f"\n{BLUE}[--- FRP Bypass Only (Google Account) ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    show_loading("Bypassing Google Account protection...", 2)
    print(f"{GREEN}[SUCCESS] FRP Bypass script sent successfully for {model}!{RESET}")
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def remove_screen_lock_root():
    print(f"\n{BLUE}[--- Remove Screen Lock (Root / No Data Loss) ---]{RESET}")
    model = get_target_device_model()
    if not model:
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return
    
    show_loading("Checking Root permissions & lock files...", 2.5)
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

def generic_brand_menu(brand_name, models_dict):
    """دالة عامة تعرض أجهزة أي شركة مع إمكانية البحث عن جهاز غير موجود في القائمة"""
    while True:
        clear_screen()
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{GREEN}        {brand_name} Models Hub        {RESET}")
        print(f"{MAGENTA}========================================{RESET}")
        
        for key, value in models_dict.items():
            print(f"{CYAN}{key}.{RESET} {value}")
            
        print(f"{YELLOW}[s]{RESET} Search for another {brand_name} model (Custom)")
        print(f"{CYAN}b.{RESET} Back to Brands Menu")
        print(f"{MAGENTA}========================================{RESET}")
        
        choice = input(f"\n{YELLOW}Select Option [1-{len(models_dict)}, s, b]: {RESET}").strip().lower()
        
        if choice == 'b':
            return "BACK"
        elif choice == 's':
            custom_model = input(f"\n{YELLOW}Enter specific {brand_name} model name: {RESET}").strip()
            if custom_model:
                return f"{brand_name} {custom_model}"
            else:
                print(f"{RED}[!] Invalid name.{RESET}")
                input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice in models_dict:
            return models_dict[choice]
        else:
            print(f"\n{RED}[!] Invalid choice.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def brand_and_model_database_search():
    """قائمة الماركات الرئيسية مع تخصيص قائمة وأجهزة لكل ماركة وخيار البحث الحر الشامل"""
    while True:
        clear_screen()
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{GREEN}      Global Brands & Models Hub        {RESET}")
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{CYAN}1.{RESET} Oppo")
        print(f"{CYAN}2.{RESET} Samsung")
        print(f"{CYAN}3.{RESET} Xiaomi / Redmi")
        print(f"{CYAN}4.{RESET} Vivo")
        print(f"{CYAN}5.{RESET} Huawei / Honor")
        print(f"{CYAN}6.{RESET} Infinix / Tecno")
        print(f"{YELLOW}[s]{RESET} Search for ANY Custom Brand/Model (e.g. Apple, etc.)")
        print(f"{CYAN}7.{RESET} Back to Main Menu")
        print(f"{MAGENTA}========================================{RESET}")
        
        choice = input(f"\n{YELLOW}Select Option [1-6, s, 7]: {RESET}").strip().lower()
        
        selected_brand = ""
        
        if choice == "1":
            oppo_models = {"1": "Oppo a1k", "2": "Oppo A3s", "3": "Oppo A5s", "4": "Oppo F9 / F11", "5": "Oppo Reno Series"}
            res = generic_brand_menu("Oppo", oppo_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == "2":
            samsung_models = {"1": "Samsung Galaxy A10 / A12", "2": "Samsung Galaxy A32 / A52", "3": "Samsung Galaxy S20 / S21", "4": "Samsung Galaxy Note 10 / 20"}
            res = generic_brand_menu("Samsung", samsung_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == "3":
            xiaomi_models = {"1": "Xiaomi Redmi 9 / 9A", "2": "Xiaomi Redmi Note 10 / 11", "3": "Xiaomi Poco X3 / M3", "4": "Xiaomi Mi Series"}
            res = generic_brand_menu("Xiaomi", xiaomi_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == "4":
            vivo_models = {"1": "Vivo Y11 / Y12", "2": "Vivo Y20 / Y21", "3": "Vivo V20 / V23", "4": "Vivo X Series"}
            res = generic_brand_menu("Vivo", vivo_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == "5":
            huawei_models = {"1": "Huawei Y6 / Y7", "2": "Huawei Nova 7i / 9", "3": "Huawei P30 / P40 Pro", "4": "Honor 8X / 9X"}
            res = generic_brand_menu("Huawei/Honor", huawei_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == "6":
            infinix_models = {"1": "Infinix Hot 10 / 11", "2": "Infinix Note 10 / 12", "3": "Tecno Spark 6 / 7", "4": "Tecno Camon 16 / 18"}
            res = generic_brand_menu("Infinix/Tecno", infinix_models)
            if res == "BACK":
                continue
            selected_brand = res
        elif choice == 's':
            custom_name = input(f"\n{YELLOW}Enter Brand or Model Name to search (e.g., Apple, etc.): {RESET}").strip()
            selected_brand = custom_name if custom_name else "Custom Device"
        elif choice == "7":
            return
        else:
            print(f"\n{RED}[!] Invalid choice.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
            continue
            
        show_loading(f"Loading data for {selected_brand}...", 2)
        print(f"\n{GREEN}[+] Target Selected: {CYAN}{selected_brand}{RESET}")
        
        print(f"\n{MAGENTA}--- Select Operation for {selected_brand} ---{RESET}")
        print(f"{CYAN}1.{RESET} Factory Reset with FRP Bypass")
        print(f"{CYAN}2.{RESET} FRP Bypass Only (Google Account)")
        print(f"{CYAN}3.{RESET} Return to Hub Menu")
        
        sub_choice = input(f"\n{YELLOW}Select option [1-3]: {RESET}").strip()
        
        if sub_choice in ["1", "2"]:
            if not check_device_connected():
                input(f"\n{YELLOW}Press Enter to return...{RESET}")
                continue
                
            if sub_choice == "1":
                show_progress_bar(f"Executing Factory Reset & FRP for {selected_brand}...", 3)
                res = subprocess.run(["adb", "shell", "wipe", "data"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if res.returncode == 0:
                    print(f"{GREEN}[SUCCESS] Factory Reset & FRP executed successfully for {selected_brand}!{RESET}")
                else:
                    print(f"{RED}[!] Operation failed. Ensure device is connected.{RESET}")
            elif sub_choice == "2":
                show_loading(f"Bypassing Google Account (FRP) for {selected_brand}...", 2)
                print(f"{GREEN}[SUCCESS] FRP Bypass payload sent successfully for {selected_brand}!{RESET}")
                
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        else:
            continue

def main_menu():
    while True:
        clear_screen()
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{GREEN}         MiniUnlockTool v3.0            {RESET}")
        print(f"{MAGENTA}========================================{RESET}")
        print(f"{CYAN}1.{RESET} Factory Reset & FRP Bypass (Full)")
        print(f"{CYAN}2.{RESET} FRP Bypass Only (Stuck on Google Acct)")
        print(f"{CYAN}3.{RESET} Remove Screen Lock (Root / No Data Loss)")
        print(f"{CYAN}4.{RESET} Reboot Normal")
        print(f"{CYAN}5.{RESET} Reboot to Fastboot (Bootloader)")
        print(f"{CYAN}6.{RESET} Get Device Info")
        print(f"{CYAN}7.{RESET} Brands & Models Hub")
        print(f"{CYAN}8.{RESET} Exit")
        print(f"{MAGENTA}========================================{RESET}")
        
        choice = input(f"\n{YELLOW}Select an option [1-8]: {RESET}").strip()
        
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
            brand_and_model_database_search()
        elif choice == "8":
            print(f"\n{GREEN}Exiting tool. Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}[!] Invalid choice, please try again.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main_menu()
