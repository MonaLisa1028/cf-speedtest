import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

# 你的 IP 列表文件
IP_FILE = "hk_ips.txt"

def test_speed(ip_line):
    target = ip_line.split('#')[0].strip()
    
    # 使用 curl 直接测速，获取下载速度
    # --connect-timeout 2: 连接超时
    # --max-time 5: 最长运行 5 秒
    # -o /dev/null: 不保存文件
    # -w: 获取下载速度 (bytes_downloaded / time_spent)
    cmd = f"curl -x {target} -L --connect-timeout 2 --max-time 5 -o /dev/null -s -w '%{{speed_download}}' https://speed.cloudflare.com/__down?bytes=10000000"
    
    try:
        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
        # speed_download 的单位是 bytes/s，转换为 Mbps (bytes * 8 / 1000000)
        speed_mbps = (float(result) * 8) / 1000000
        return f"{ip_line} | {speed_mbps:.2f} Mbps"
    except:
        return f"{ip_line} | 测速失败"

with open(IP_FILE, "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(test_speed, ips))

with open("result.txt", "w", encoding="utf-8") as f:
    for res in results:
        f.write(res + "\n")
