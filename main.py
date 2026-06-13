import socket
import time

def test_speed(target_ip):
    # 模拟 Cloudflare 的下载请求
    request = b"GET /__down?bytes=10000000 HTTP/1.1\r\nHost: speed.cloudflare.com\r\nConnection: close\r\n\r\n"
    try:
        start_time = time.time()
        # 建立底层连接
        s = socket.create_connection((target_ip, 443), timeout=10)
        s.sendall(request)
        
        # 接收数据并计算流量
        total_received = 0
        while True:
            data = s.recv(4096)
            if not data: break
            total_received += len(data)
        
        duration = time.time() - start_time
        speed_mbps = (total_received * 8) / (duration * 1000000)
        s.close()
        return f"{target_ip} | {speed_mbps:.2f} Mbps"
    except Exception as e:
        return f"{target_ip} | 测速失败 (原因: {str(e)[:15]})"

# 读取 IP
with open("hk_ips.txt", "r") as f:
    ip = f.read().strip()

# 执行测速
result = test_speed(ip)
with open("result.txt", "w") as f:
    f.write(result)
