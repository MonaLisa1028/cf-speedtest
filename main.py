import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 读取 IP 列表
with open("hk_ips.txt", "r") as f:
    ips = [line.strip() for line in f if line.strip()]

def test_ip(ip_line):
    # 这一行代码能自动从 "91.193.59.164:443#HK..." 中提取出 "91.193.59.164:443"
    target_ip = ip_line.split('#')[0].strip()
    
    try:
        # 1. 测延迟
        start = time.time()
        # 将 target_ip 放入 requests 请求中
        res = requests.get(f"https://{target_ip}", timeout=2, verify=False)
        latency = (time.time() - start) * 1000
        
        # 2. 测带宽
        start_bw = time.time()
        res_bw = requests.get("https://speed.cloudflare.com/__down?bytes=500000", timeout=3)
        duration = time.time() - start_bw
        speed = 0.5 / duration # Mbps
        
        return (ip_line, latency, speed) # 返回原始行，保持完整信息
    except:
        return (ip_line, 999, 0)

# 使用 20 个线程并发测速
print(f"开始测试 {len(ips)} 个节点...")
with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(test_ip, ips))

# 过滤掉失败的节点，按延迟排序，再按带宽排序
results.sort(key=lambda x: (x[1], -x[2]))

# 保存结果
with open("result.txt", "w") as f:
    f.write("IP | 延迟(ms) | 带宽(Mbps)\n")
    for ip, lat, spd in results:
        if lat < 999: # 只显示成功的
            f.write(f"{ip} {lat:.0f}ms {spd:.2f}Mbps\n")
