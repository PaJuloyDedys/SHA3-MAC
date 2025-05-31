import sys
from pathlib import Path
from src import hmac_sha3  

def main():
    print("=== HMAC-SHA3 DEMO ===")
    
    key_hex = "00112233445566778899aabbccddeeff"
    key = bytes.fromhex(key_hex)
    print(f"[1] Використовується ключ: {key_hex}")

    msg_text = input("[2] Введіть повідомлення: ").strip()
    msg = msg_text.encode('utf-8')
    print(f"[3] Повідомлення в байтах: {msg.hex()}")

    mac = hmac_sha3.compute_mac(key, msg)
    mac_hex = mac.hex()
    print(f"[4] Згенерований HMAC: {mac_hex}")

    choice = input("\n[5] Оберіть дію: (s) Зберегти MAC | (v) Перевірити MAC у файлі message.mac: ").lower()
    mac_path = Path("message.mac")

    if choice == 's':
        mac_path.write_bytes(mac)
        print("[6] MAC збережено в 'message.mac'")
    elif choice == 'v':
        if not mac_path.exists():
            print("[6] Файл 'message.mac' не знайдено.")
            return
        ref_mac = mac_path.read_bytes()
        print(f"[6] Очікуваний MAC: {ref_mac.hex()}")
        if mac == ref_mac:
            print("[7] Перевірка: ✅ MAC Збігається (OK)")
        else:
            print("[7] Перевірка: ❌ MAC НЕ збігається (FAIL)")
    else:
        print("[!] Невідома дія.")

if __name__ == "__main__":
    main()
