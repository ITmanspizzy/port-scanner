import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            try:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner retrieved"
            print(f"[+] Port {port} is OPEN - {banner}")
        sock.close()
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner with Banner Grabbing")
    parser.add_argument("host", help="Target IP or domain")
    parser.add_argument("-p", "--ports", help="Port range (e.g. 20-80)", default="1-1024")
    parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=100)

    args = parser.parse_args()
    start_port, end_port = map(int, args.ports.split("-"))

    print(f"\n[*] Scanning {args.host} from port {start_port} to {end_port} using {args.threads} threads...\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, args.host, port)

if __name__ == "__main__":
    main()
