import socket
import threading
import os
import json


class NapsterClient:
    def __init__(self, server_ip='127.0.0.1', server_port=1234, file_port=1235):
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_port = file_port
        self.public_dir = 'public'
        self.download_dir = 'downloads'
        os.makedirs(self.public_dir, exist_ok=True)
        os.makedirs(self.download_dir, exist_ok=True)
        self.my_ip = self.get_local_ip()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'

    def connect_to_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server_ip, self.server_port))
        return s

    def send_json(self, sock, obj):
        sock.send(json.dumps(obj).encode())

    def recv_json(self, sock):
        return json.loads(sock.recv(4096).decode())

    def start(self):
        s = self.connect_to_server()
        self.send_json(s, {"command": "JOIN", "ip": self.my_ip})
        print(self.recv_json(s))

        for f in os.listdir(self.public_dir):
            path = os.path.join(self.public_dir, f)
            if os.path.isfile(path):
                self.send_json(s, {
                    "command": "CREATEFILE",
                    "filename": f,
                    "size": os.path.getsize(path)
                })
                print(self.recv_json(s))

        threading.Thread(target=self.file_server, daemon=True).start()

        while True:
            cmd = input("\n1: search <termo>\n2: download <arquivo> <ip>\n3: quit\n> ").strip()
            if cmd.startswith('search'):
                _, term = cmd.split(maxsplit=1)
                self.send_json(s, {"command": "SEARCH", "pattern": term})
                res = self.recv_json(s)
                files = res.get("files", [])
                if files:
                    print("\nArquivos encontrados:")
                    for i, file in enumerate(files, 1):
                        print(f"{i}. {file['filename']} ({file['size']} bytes) - {file['ip_address']}")
                else:
                    print("Nenhum arquivo encontrado.")
            elif cmd.startswith('download'):
                try:
                    _, fname, ip = cmd.split()
                    self.download_file(fname, ip)
                except ValueError:
                    print("Uso correto: download <arquivo> <ip>")
            elif cmd == 'quit':
                self.send_json(s, {"command": "LEAVE"})
                print(self.recv_json(s))
                s.close()
                break
            else:
                print("Comando inválido.")

    def file_server(self):
        """Servidor local que envia arquivos para outros peers"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.my_ip, self.file_port))
        s.listen()
        print(f"[+] Servidor de arquivos escutando em {self.my_ip}:{self.file_port}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=self.send_file, args=(conn,), daemon=True).start()

    def send_file(self, conn):
        try:
            req = conn.recv(1024).decode().strip().split()
            if req and req[0] == 'GET':
                fname = os.path.basename(req[1])
                path = os.path.join(self.public_dir, fname)
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        while chunk := f.read(1024):
                            conn.send(chunk)
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")
        finally:
            conn.close()

    def download_file(self, fname, ip):
        """Baixa arquivo de outro cliente"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, self.file_port))
            s.send(f"GET {fname}\n".encode())
            with open(os.path.join(self.download_dir, fname), 'wb') as f:
                while True:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            s.close()
            print(f"✅ Arquivo '{fname}' baixado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao baixar '{fname}' de {ip}: {e}")


if __name__ == '__main__':
    NapsterClient().start()
