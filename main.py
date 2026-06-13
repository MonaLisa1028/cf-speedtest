import socket
import time
from concurrent.futures import ThreadPoolExecutor

# 读取 IP 列表
with open("hk_ips.txt", "r", encoding="utf-8") as f:
    ips = [line.strip() for line in f if line.strip()]

def test_ip(ip_line):
    # 解析 IP 和端口
    target = ip_line.split('#')[0].strip()
    host = target.split(':')[0]
    port = int(target.split(':')[1]) if ':' in target else 443
    
    try:
        # 使用 Socket 直接测 TCP 延迟（最稳妥，不会报错）
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        latency = (time.time() - start) * 1000
        s.close()
        return (ip_line, latency)
    except:
        return (ip_line, 9999)

# 并发测试
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(test_ip, ips))

# 过滤失败的，按延迟排序
results = [r for r in results if r[1] < 9999]
results.sort(key=lambda x: x[1])

# 保存结果
with open("result.txt", "w", encoding="utf-8") as f:
    f.write("IP 列表 | 延迟(ms)\n")
    for ip, lat in results:
        f.write(f"{ip} | {lat:.0f}ms\n")
