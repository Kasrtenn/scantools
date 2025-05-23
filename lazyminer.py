import os
import subprocess
import shutil
import requests  # Menambahkan pustaka requests untuk notifikasi Telegram
from time import sleep

# Definisikan tools dan repository instalasinya sesuai dengan GitHub ProjectDiscovery
TOOLS = {
    "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder",
    "httpx": "github.com/projectdiscovery/httpx/cmd/httpx",
    "nuclei": "github.com/projectdiscovery/nuclei/v2/cmd/nuclei"
}

# Folder output
OUTPUT_FOLDER_SUBDO = "subdomain"
OUTPUT_FOLDER_ACTIVE = "active"
OUTPUT_FOLDER_NUCLEI = "nuclei"
os.makedirs(OUTPUT_FOLDER_SUBDO, exist_ok=True)
os.makedirs(OUTPUT_FOLDER_ACTIVE, exist_ok=True)
os.makedirs(OUTPUT_FOLDER_NUCLEI, exist_ok=True)

def check_go():
    """Memeriksa apakah Go terinstal sebelum menginstal tools."""
    if not shutil.which("go"):
        print("[❌] Go belum terinstal! Silakan instal Go terlebih dahulu.")
        exit(1)

def check_and_install_tools():
    """Memeriksa dan menginstal tools jika belum ada."""
    for tool, repo in TOOLS.items():
        if not shutil.which(tool):
            print(f"[⚠️] {tool} belum terinstall. Menginstall...")
            install_cmd = f"go install -v {repo}@latest"
            result = subprocess.run(install_cmd, shell=True)
            if result.returncode != 0:
                print(f"[❌] Gagal menginstall {tool}. Pastikan Go sudah terinstall dan PATH sudah diset.")
            else:
                print(f"[✅] {tool} berhasil diinstall.")
        else:
            print(f"[✅] {tool} sudah terinstall.")

def update_tools():
    """Memperbarui tools sebelum digunakan."""
    print("[??] Mengecek update untuk semua tools...")
    for tool in TOOLS:
        update_cmd = f"{tool} -update"
        subprocess.run(update_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run("nuclei -update-templates", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[✅] Semua tools telah diperbarui.")

def print_logo():
    logo = r"""
 ██▓    ▄▄▄      ▒███████▒▓██   ██▓ ███▄ ▄███▓ ██▓ ███▄    █ ▓█████  ██▀███  
▓██▒   ▒████▄    ▒ ▒ ▒ ▄▀░ ▒██  ██▒▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
▒██░   ▒██  ▀█▄  ░ ▒ ▄▀▒░   ▒██ ██░▓██    ▓██░▒██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
▒██░   ░██▄▄▄▄██   ▄▀▒   ░  ░ ▐██▓░▒██    ▒██ ░██░▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
░██████▒▓█   ▓██▒▒███████▒  ░ ██▒▓░▒██▒   ░██▒░██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
░ ▒░▓  ░▒▒   ▓▒█░░▒▒ ▓░▒░▒   ██▒▒▒ ░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░ ▒  ░ ▒   ▒▒ ░░░▒ ▒ ░ ▒ ▓██ ░▒░ ░  ░      ░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
  ░ ░    ░   ▒   ░ ░ ░ ░ ░ ▒ ▒ ░░  ░      ░    ▒ ░   ░   ░ ░    ░     ░░   ░ 
    ░  ░     ░  ░  ░ ░     ░ ░            ░    ░           ░    ░  ░   ░     
                 ░         ░ ░                                               
    """
    print(logo)

def get_target_url():
    """Meminta input URL/domain dan memastikan URL valid.""" 
    while True:
        target_url = input("Masukkan URL/domain target (contoh: example.com): ").strip()
        if target_url:
            return target_url
        print("[❌] URL tidak valid! Masukkan URL yang benar.")

def send_telegram_notification(message, token, chat_id):
    """Kirim pesan ke Telegram"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("[✅] Notifikasi terkirim ke Telegram.")
    else:
        print(f"[❌] Gagal mengirim notifikasi ke Telegram. Status Code: {response.status_code}")

def send_whatsapp_notification(message, phone_number):
    """Kirim pesan ke WhatsApp menggunakan CallMeBot API"""
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={message}&apikey=YOUR_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        print("[✅] Notifikasi terkirim ke WhatsApp.")
    else:
        print(f"[❌] Gagal mengirim notifikasi ke WhatsApp. Status Code: {response.status_code}")

def get_telegram_credentials():
    """Meminta token dan chat ID Telegram"""
    token = input("Masukkan token Telegram Bot Anda: ").strip()
    chat_id = input("Masukkan chat ID Telegram Anda: ").strip()
    return token, chat_id

def choose_notification_method():
    """Meminta pilihan notifikasi via Telegram atau WhatsApp"""
    while True:
        notif_choice = input("Apakah Anda ingin menggunakan fitur notifikasi? (y/n): ").strip().lower()
        if notif_choice == 'y':
            print("Pilih metode notifikasi:")
            print("1. Telegram")
            print("2. WhatsApp")
            method_choice = input("Pilih metode (1/2): ").strip()
            return method_choice
        elif notif_choice == 'n':
            return None
        else:
            print("[❌] Pilihan tidak valid. Silakan pilih 'y' atau 'n'.")

def process_domain(target_url, notif_method, token=None, chat_id=None, phone_number=None):
    """Melakukan scanning untuk satu domain dan mengirim notifikasi setelah selesai"""
    subdomain_file = os.path.join(OUTPUT_FOLDER_SUBDO, f"{target_url}.txt")
    active_file = os.path.join(OUTPUT_FOLDER_ACTIVE, f"active_{target_url}.txt")
    nuclei_output = os.path.join(OUTPUT_FOLDER_NUCLEI, f"nuc_active_{target_url}.txt")

    print(f"\n[??] Mencari subdomain untuk: {target_url}")
    subprocess.run(["subfinder", "-d", target_url, "-o", subdomain_file])

    print("[??] Mengecek subdomain yang aktif...")
    subprocess.run(["httpx", "-l", subdomain_file, "-o", active_file])

    print("[??] Menjalankan Nuclei scan...")
    subprocess.run([
        "nuclei", 
        "-l", active_file, 
        "-severity", "low,medium,high,critical", "-ept", "ssl", "-o", nuclei_output])

    print(f"[✅] Scanning selesai untuk: {target_url}\n")

    # Membaca output Nuclei dan mengirimkan notifikasi jika ada kerentanannya
    with open(nuclei_output, "r") as f:
        output = f.read()

    if output:
        message = f"Telah ditemukan kerentanannya di situs {target_url}:\n{output}"
        if notif_method == '1':  # Telegram
            send_telegram_notification(message, token, chat_id)
        elif notif_method == '2':  # WhatsApp
            send_whatsapp_notification(message, phone_number)
    else:
        print(f"[❌] Tidak ada kerentanan ditemukan untuk: {target_url}")

def main():
    # Kosongkan layar terlebih dahulu
    os.system('cls' if os.name == 'nt' else 'clear')

    # Proses pengecekan dan update tools
    print("[??] Mengecek dan mengupdate tools...")
    check_go()
    check_and_install_tools()
    update_tools()

    # Setelah proses pengecekan selesai, tampilkan logo
    print_logo()

    target_url = get_target_url()

    # Pilihan notifikasi
    notif_method = choose_notification_method()
    if notif_method == '1':  # Telegram
        token, chat_id = get_telegram_credentials()
        process_domain(target_url, notif_method, token=token, chat_id=chat_id)
    elif notif_method == '2':  # WhatsApp
        phone_number = input("Masukkan nomor WhatsApp (termasuk kode negara, misalnya: +6281234567890): ").strip()
        process_domain(target_url, notif_method, phone_number=phone_number)
    else:
        process_domain(target_url, None)

if __name__ == "__main__":
    main()

