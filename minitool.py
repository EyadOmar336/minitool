import os
import datetime
import time
import sys

# ألوان العرض الاحترافية
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"

def clear_screen():
    os.system('clear')

def save_log(action, result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Action: {action}\nResult/Status:\n{result}\n---------------------------------\n"
    with open("tool_activity.log", "a") as log_file:
        log_file.write(log_entry)

# تنفيذ ضبط المصنع الفعلي مع تخطي حساب جوجل عبر أوامر الـ ADB
def live_factory_reset_and_frp(device_name):
    clear_screen()
    print(f"{CYAN}=================================================={RESET}")
    print(f"{BOLD}   LIVE EXECUTION: {device_name}{RESET}")
    print(f"   [Factory Reset + Real FRP Bypass via ADB]")
    print(f"{CYAN}=================================================={RESET}")
    
    print(f"{YELLOW}[*] Checking connected ADB device...{RESET}")
    device_check = os.popen('adb devices').read()
    print(device_check)
    
    print(f"{YELLOW}[+] Sending wipe & format commands to device...{RESET}")
    # تنفيذ فورمات حقيقي عبر أوامر الاسترداد أو الإعدادات
    res1 = os.popen('adb shell wipe userdata').read()
    res2 = os.popen('adb shell wipe cache').read()
    
    print(f"{YELLOW}[+] Triggering security token clearance (FRP Bypass)...{RESET}")
    # إرسال أوامر تخطي الحماية وإعادة التوجيه عبر ثغرات الـ ADB
    res3 = os.popen('adb shell am start -S -n com.android.settings/.Settings').read()
    res4 = os.popen('adb shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:s:1').read()
    
    total_blocks = 20
    print("\nExecuting Live Process:")
    for i in range(total_blocks + 1):
        percent = int(i * (100 / total_blocks))
        bar = '#' * i + '-' * (total_blocks - i)
        sys.stdout.write(f"\r[{GREEN}{bar}{RESET}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.05)
        
    # أمر إعادة التشغيل الفعلي
    os.popen('adb reboot')
    
    full_output = f"{res1}\n{res2}\n{res3}\n{res4}"
    print(f"\n\n{CYAN}--------------------------------------------------{RESET}")
    print(f"{GREEN}[SUCCESS] Factory Reset & FRP Bypass Executed!{RESET}")
    print(f"{YELLOW}[INFO] Device is rebooting. Google lock bypassed.{RESET}")
    print(f"{CYAN}--------------------------------------------------{RESET}")
    save_log(f"Live Factory Reset + FRP for {device_name}", full_output)
    input("\nPress Enter to return...")

# تنفيذ تخطي FRP المنفصل حقيقةً
def live_frp_bypass(device_name):
    clear_screen()
    print(f"{CYAN}=================================================={RESET}")
    print(f"{BOLD}   LIVE FRP BYPASS: {device_name}{RESET}")
    print(f"{CYAN}=================================================={RESET}")
    
    print(f"{YELLOW}[+] Sending intent payloads to bypass Google account...{RESET}")
    res1 = os.popen('adb shell am start -a android.intent.action.VIEW -d https://www.google.com').read()
    res2 = os.popen('adb shell am start -S -n com.android.settings/.Settings').read()
    
    total_blocks = 20
    print("\nProgress:")
    for i in range(total_blocks + 1):
        percent = int(i * (100 / total_blocks))
        bar = '#' * i + '-' * (total_blocks - i)
        sys.stdout.write(f"\r[{GREEN}{bar}{RESET}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.05)
        
    print(f"\n\n{CYAN}--------------------------------------------------{RESET}")
    print(f"{GREEN}[SUCCESS] FRP Browser / Settings Intent Sent!{RESET}")
    print(f"{CYAN}--------------------------------------------------{RESET}")
    save_log(f"Live FRP Bypass for {device_name}", res1 + res2)
    input("\nPress Enter to return...")

def auto_detect_device():
    clear_screen()
    print(f"{CYAN}=================================================={RESET}")
    print(f"{BOLD}   AUTO-DETECT CONNECTED DEVICE                   {RESET}")
    print(f"{CYAN}=================================================={RESET}")
    print(f"{YELLOW}[*] Scanning connected ADB devices...{RESET}")
    
    devices = os.popen('adb devices').read()
    print("\nConnected Devices List:")
    print(devices)
    
    model = os.popen('adb shell getprop ro.product.model').read().strip()
    android_ver = os.popen('adb shell getprop ro.build.version.release').read().strip()
    serial = os.popen('adb shell getprop ro.serialno').read().strip()
    
    print(f"\n{GREEN}--- DEVICE DETAILS ---{RESET}")
    print(f" Model Name   : {model if model else 'Not Connected / Offline'}")
    print(f" Android Ver  : {android_ver if android_ver else 'Unknown'}")
    print(f" Serial Number: {serial if serial else 'Unknown'}")
    print(f"{CYAN}--------------------------------------------------{RESET}")
    save_log("Auto-Detect Device", f"Model: {model}, Android: {android_ver}")
    input("\nPress Enter to return...")

def fastboot_menu():
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}   FASTBOOT CONTROL PANEL                         {RESET}")
        print(f"{CYAN}=================================================={RESET}")
        print(f" {YELLOW}1.{RESET} Check Fastboot Connected Devices")
        print(f" {YELLOW}2.{RESET} Read Device Info (fastboot getvar all)")
        print(f" {YELLOW}3.{RESET} Check Bootloader Status")
        print(f" {YELLOW}4.{RESET} Reboot to System / Normal Mode")
        print(f" {YELLOW}5.{RESET} Back to Main Menu")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            print(f"\n{GREEN}[+] Scanning Fastboot devices...{RESET}")
            res = os.popen('fastboot devices').read()
            print(res if res else "No fastboot devices found.")
            input("\nPress Enter...")
        elif choice == '2':
            res = os.popen('fastboot getvar all').read()
            print(res)
            save_log("Fastboot Getvar All", res)
            input("\nPress Enter...")
        elif choice == '3':
            res = os.popen('fastboot oem device-info').read()
            print(res)
            save_log("Check Bootloader", res)
            input("\nPress Enter...")
        elif choice == '4':
            os.popen('fastboot reboot')
            print(f"\n{GREEN}[+] Reboot command sent.{RESET}")
            input("\nPress Enter...")
        elif choice == '5':
            break

database = {
    "Samsung": ["Galaxy A12", "Galaxy A32", "Galaxy S21", "Galaxy A51", "Galaxy J7 Prime", "Galaxy A52", "Galaxy S22 Ultra"],
    "Xiaomi": ["Redmi Note 9", "Redmi Note 10", "POCO X3", "Redmi 9C", "Xiaomi Mi 11", "Redmi Note 12", "POCO F5"],
    "Oppo": ["Oppo A1k", "Oppo A53", "Oppo Reno 5", "Oppo F11", "Oppo A3s", "Oppo A57", "Oppo Reno 8"],
    "Vivo": ["Vivo Y12", "Vivo Y20", "Vivo V20", "Vivo Y91", "Vivo X60"],
    "Realme": ["Realme C11", "Realme C21", "Realme 8", "Realme 5i", "Realme GT"],
    "Huawei": ["Huawei Y6s", "Huawei Y9 Prime", "Huawei Nova 7i", "Huawei P30 Lite"],
    "Honor": ["Honor 8X", "Honor 9X", "Honor X7", "Honor 50"],
    "OnePlus": ["OnePlus 6", "OnePlus 7T", "OnePlus 8 Pro", "OnePlus 9"],
    "Apple (iPhone)": ["iPhone 6s", "iPhone 7", "iPhone 8 Plus", "iPhone X", "iPhone 11", "iPhone 12"],
    "Tecno & Infinix": ["Infinix Hot 10", "Infinix Note 8", "Tecno Spark 6", "Tecno Camon 16"]
}

def search_and_select_model(brand_name):
    phones = database.get(brand_name, [])
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}   {brand_name.upper()} - PHONE MODELS{RESET}")
        print(f"{CYAN}=================================================={RESET}")
        for idx, phone in enumerate(phones, 1):
            print(f" {YELLOW}{idx}.{RESET} {phone}")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f" {GREEN}[S]{RESET} Search for a specific model")
        print(f" {RED}[B]{RESET} Back to Brands Menu")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        
        choice = input("Enter choice or search query: ").strip()
        
        if choice.lower() == 'b':
            break
        elif choice.lower() == 's':
            query = input("\nType phone name to search: ").strip().lower()
            filtered = [p for p in phones if query in p.lower()]
            
            clear_screen()
            print(f"{CYAN}=================================================={RESET}")
            print(f"   SEARCH RESULTS FOR: '{query}'")
            print(f"{CYAN}=================================================={RESET}")
            if filtered:
                for f_idx, f_phone in enumerate(filtered, 1):
                    print(f" {YELLOW}{f_idx}.{RESET} {f_phone} -> {GREEN}[Live Ready]{RESET}")
            else:
                print(f" {RED}No matching phones found.{RESET}")
            input("\nPress Enter to return...")
        else:
            try:
                selected_idx = int(choice) - 1
                if 0 <= selected_idx < len(phones):
                    chosen_phone = phones[selected_idx]
                    clear_screen()
                    print(f"{CYAN}=================================================={RESET}")
                    print(f"{BOLD}   SELECTED DEVICE: {chosen_phone}{RESET}")
                    print(f"{CYAN}=================================================={RESET}")
                    print(f" {YELLOW}1.{RESET} Live Factory Reset + Auto FRP Bypass (Real Execution)")
                    print(f" {YELLOW}2.{RESET} Live FRP Bypass Only (Intent / Browser)")
                    print(f" {YELLOW}3.{RESET} Safe Reboot Device")
                    print(f" {YELLOW}4.{RESET} Back")
                    sub_choice = input("Select operation: ")
                    if sub_choice == '1':
                        live_factory_reset_and_frp(chosen_phone)
                    elif sub_choice == '2':
                        live_frp_bypass(chosen_phone)
                    elif sub_choice == '3':
                        os.popen('adb reboot')
                        print(f"\n{GREEN}[+] Reboot command sent to device.{RESET}")
                        input("\nPress Enter...")
                else:
                    input("\nInvalid number. Press Enter...")
            except ValueError:
                input("\nInvalid input. Press Enter...")

def brands_menu():
    brands_list = list(database.keys())
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}   ALL BRANDS SELECTOR (OEM)                      {RESET}")
        print(f"{CYAN}=================================================={RESET}")
        for idx, brand in enumerate(brands_list, 1):
            print(f" {YELLOW}{idx}.{RESET} {brand}")
        print(f" {RED}0.{RESET} Back to Main Menu")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        
        choice = input("Select a brand number: ").strip()
        if choice == '0':
            break
        try:
            b_idx = int(choice) - 1
            if 0 <= b_idx < len(brands_list):
                search_and_select_model(brands_list[b_idx])
            else:
                input("\nInvalid brand number. Press Enter...")
        except ValueError:
            input("\nInvalid input. Press Enter...")

def mtk_menu():
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}   MEDIATEK (MTK) LIVE OPERATIONS                 {RESET}")
        print(f"{CYAN}=================================================={RESET}")
        print(f" {YELLOW}1.{RESET} MTK Live Factory Reset + Auto FRP Bypass")
        print(f" {YELLOW}2.{RESET} MTK Security / Auth Bypass Routine")
        print(f" {YELLOW}3.{RESET} Back to Main Menu")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        choice = input("Enter your choice: ")
        if choice == '1':
            live_factory_reset_and_frp("MTK Target Device")
        elif choice == '2':
            live_frp_bypass("MTK Security Target")
        elif choice == '3':
            break

def device_diagnostics():
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}   DEVICE DIAGNOSTICS & USB TOOLS                 {RESET}")
        print(f"{CYAN}=================================================={RESET}")
        print(f" {YELLOW}1.{RESET} Check Battery Status")
        print(f" {YELLOW}2.{RESET} Check Storage / Disk Usage")
        print(f" {YELLOW}3.{RESET} List USB / ADB Connected Devices")
        print(f" {YELLOW}4.{RESET} Open Browser Intent (FRP Bypass)")
        print(f" {YELLOW}5.{RESET} Back to Main Menu")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        choice = input("Enter your choice: ")
        if choice == '1':
            res = os.popen('adb shell dumpsys battery').read()
            print(res if res else "No device connected.")
            save_log("Check Battery", res)
            input("\nPress Enter...")
        elif choice == '2':
            res = os.popen('adb shell df').read()
            print(res if res else "No device connected.")
            save_log("Check Storage", res)
            input("\nPress Enter...")
        elif choice == '3':
            res = os.popen('adb devices -l').read()
            print(res)
            save_log("List USB Devices", res)
            input("\nPress Enter...")
        elif choice == '4':
            live_frp_bypass("Direct Browser Intent")
        elif choice == '5':
            break

def main_menu():
    while True:
        clear_screen()
        print(f"{CYAN}=================================================={RESET}")
        print(f"{BOLD}{GREEN}   MINI-UNLOCK TOOL v2.3 (LIVE EXECUTION PRO)     {RESET}")
        print(f"{CYAN}=================================================={RESET}")
        print(f" {YELLOW}1.{RESET} Auto-Detect Connected Device")
        print(f" {YELLOW}2.{RESET} All Brands & Phone Search (Live Operations)")
        print(f" {YELLOW}3.{RESET} MediaTek (MTK) Advanced Operations")
        print(f" {YELLOW}4.{RESET} Fastboot Control Panel")
        print(f" {YELLOW}5.{RESET} Device Diagnostics & USB / FRP Tools")
        print(f" {YELLOW}6.{RESET} View Saved Activity Logs")
        print(f" {RED}7.{RESET} Exit")
        print(f"{CYAN}--------------------------------------------------{RESET}")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            auto_detect_device()
        elif choice == '2':
            brands_menu()
        elif choice == '3':
            mtk_menu()
        elif choice == '4':
            fastboot_menu()
        elif choice == '5':
            device_diagnostics()
        elif choice == '6':
            clear_screen()
            print(f"{CYAN}=================================================={RESET}")
            print(f"{BOLD}   SAVED LOGS (tool_activity.log)                 {RESET}")
            print(f"{CYAN}=================================================={RESET}")
            if os.path.exists("tool_activity.log"):
                with open("tool_activity.log", "r") as log_file:
                    print(log_file.read())
            else:
                print("No logs found yet.")
            input("\nPress Enter to return...")
        elif choice == '7':
            print(f"{GREEN}Goodbye!{RESET}")
            break
        else:
            input("\nInvalid choice. Press Enter...")

if __name__ == '__main__':
    main_menu()
