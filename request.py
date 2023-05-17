import socket
import json

def send_get_request(url, headers=None):
    # Phân tích URL để lấy thông tin về host và đường dẫn
    host, path = parse_url(url)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, 443))

    # Gửi yêu cầu GET
    request = build_get_request(host, path, headers)
    client_socket.sendall(request.encode())
    
    # Nhận và trả về phản hồi từ máy chủ
    response = receive_response(client_socket)
    
    client_socket.close()
    return response

def parse_url(url):
    # Tách host và path từ URL
    url_parts = url.split('/')
    host = url_parts[2]
    path = '/' + '/'.join(url_parts[3:])
    return host, path

def build_get_request(host, path, headers):
    request = f"GET {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    
    if headers:
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
    
    request += "\r\n"
    return request

def receive_response(client_socket):
    response = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data
    return response.decode()

def get_status_code(response):
    # Tách mã trạng thái từ phản hồi HTTP
    status_line = response.split('\r\n')[0]
    status_code = int(status_line.split(' ')[1])
    return status_code

def response_to_json(response):
    # Tách nội dung phản hồi từ phần header và chuyển đổi sang JSON
    content = response.split('\r\n\r\n', 1)[1]
    json_data = json.loads(content)
    return json_data

# Sử dụng hàm send_get_request() với headers
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {'Accepts': 'application/json',
           'X-CMC_PRO_API_KEY': '83a2a200-4303-4bf8-b9e1-801b84ac7c31'}
response = send_get_request(url, headers)

status_code = get_status_code(response)
print(f"Status code: {status_code}")

json_data = response_to_json(response)
print(json_data)
