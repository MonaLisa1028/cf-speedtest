import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 你的 IP 列表文件
IP_FILE = "hk_ips.txt"

def test_speed(ip_line):
    # 解析 IP
    target = ip_line.split('#')[0].strip()
    try:
        # 下载 1MB 测试文件
        start = time.time()
        # 强制使用该 IP 进行请求
        res = requests.get("https://speed.cloudflare.com/__down?bytes=1000000", 
                           proxies={"https": f"https://{target}"}, 
                           timeout=5, verify=False)
        duration = time.time() - start
        # 计算 Mbps
        speed = (1 / duration) * 8
        return f"{ip_line} | {speed:.2f} Mbps"
    except:
        return f"{ip_line} | 测速失败"

# 读取 IP
with open(IP_FILE, "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

# 并发测速
print(f"正在使用 GitHub 服务器测速 {len(ips)} 个 IP...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(test_speed, ips))

# 直接写入结果，不做任何排序
with open("result.txt", "w", encoding="utf-8") as f:
    for res in results:
        f.write(res + "\n")
