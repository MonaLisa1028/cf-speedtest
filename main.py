import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 强制路径读取，确保一定能找到 hk_ips.txt
import os
file_path = "hk_ips.txt"

if not os.path.exists(file_path):
    print(f"错误：找不到文件 {file_path}")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

print(f"已成功加载 {len(ips)} 个IP节点，开始测速...")

def test_ip(ip_line):
    # 提取 IP:端口
    target = ip_line.split('#')[0].strip()
    try:
        # 测延迟
        start = time.time()
        requests.get(f"https://{target}", timeout=2, verify=False)
        latency = (time.time() - start) * 1000
        
        # 测带宽
        start_bw = time.time()
        res_bw = requests.get("https://speed.cloudflare.com/__down?bytes=500000", timeout=3)
        duration = time.time() - start_bw
        speed = 0.5 / duration 
        
        return (ip_line, latency, speed)
    except:
        return (ip_line, 999, 0)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(test_ip, ips))

# 排序并过滤掉失败的(延迟=999)
results = [r for r in results if r[1] < 999]
results.sort(key=lambda x: (x[1], -x[2]))

with open("result.txt", "w", encoding="utf-8") as f:
    f.write("IP | 延迟(ms) | 带宽(Mbps)\n")
    for ip, lat, spd in results:
        f.write(f"{ip} {lat:.0f}ms {spd:.2f}Mbps\n")
