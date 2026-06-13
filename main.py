import socket
import time
from concurrent.futures import ThreadPoolExecutor

# 你的 IP 列表文件
IP_FILE = "hk_ips.txt"

def check_ip(ip_line):
    # 只提取 IP 和端口
    target = ip_line.split('#')[0].strip()
    host = target.split(':')[0]
    port = int(target.split(':')[1]) if ':' in target else 443
    
    try:
        # 使用 Socket 尝试 TCP 握手
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port)) # 如果能连通，说明端口开放
        latency = (time.time() - start) * 1000
        s.close()
        return f"{ip_line} | 连通正常 ({latency:.0f}ms)"
    except:
        return f"{ip_line} | 无法连接"

# 读取 IP
with open(IP_FILE, "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(check_ip, ips))

with open("result.txt", "w", encoding="utf-8") as f:
    for res in results:
        f.write(res + "\n")
