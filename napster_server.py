import socket
import threading
import json
import os
from typing import Dict, List


class NapsterServer:
    def __init__(self, host='0.0.0.0', port=1234, db_file='server_data.json'):
        self.host = host
        self.port = port
        self.db_file = db_file
        self.all_files: Dict[str, List[Dict]] = self.load_data()
        self.lock = threading.Lock()

    def load_data(self):
        """Carrega o banco de arquivos persistente"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_data(self):
        """Salva o estado atual em disco"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_files, f, indent=2)

    def start(self):
        """Inicia o servidor"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("\nServidor encerrando...")
        finally:
            server_socket.close()
            self.save_data()

    def handle_client(self, conn: socket.socket, addr):
        """Gerencia comunicação com um cliente"""
        ip = addr[0]
        try:
            while True:
                raw = conn.recv(4096)
                if not raw:
                    break
                try:
                    data = json.loads(raw.decode())
                    response = self.process_command(data, ip)
                    if response:
                        conn.send(json.dumps(response).encode())
                except json.JSONDecodeError:
                    conn.send(json.dumps({
                        "status": "error",
                        "message": "invalid json"
                    }).encode())
        except Exception as e:
            print(f"[!] Erro com {ip}: {e}")
        finally:
            self.remove_user(ip)
            conn.close()
            print(f"[-] {ip} desconectado")

    def process_command(self, data: dict, ip: str) -> dict:
        """Processa um comando JSON do cliente"""
        cmd = data.get("command")

        if cmd == "JOIN":
            with self.lock:
                self.all_files[ip] = []
            return {"status": "ok", "message": "CONFIRMJOIN"}

        elif cmd == "CREATEFILE":
            file = {
                "filename": os.path.basename(data["filename"]),
                "size": int(data["size"])
            }
            with self.lock:
                self.all_files.setdefault(ip, []).append(file)
            return {
                "status": "ok",
                "message": f"CONFIRMCREATEFILE {file['filename']}"
            }

        elif cmd == "DELETEFILE":
            with self.lock:
                if ip in self.all_files:
                    self.all_files[ip] = [
                        f for f in self.all_files[ip]
                        if f["filename"] != data["filename"]
                    ]
            return {
                "status": "ok",
                "message": f"CONFIRMDELETEFILE {data['filename']}"
            }

        elif cmd == "SEARCH":
            pattern = data["pattern"].lower()
            result = []
            with self.lock:
                for user_ip, files in self.all_files.items():
                    for f in files:
                        if pattern in f["filename"].lower():
                            result.append({
                                "filename": f["filename"],
                                "ip_address": user_ip,
                                "size": f["size"]
                            })
            return {
                "status": "ok",
                "files": result or []
            }

        elif cmd == "LEAVE":
            self.remove_user(ip)
            return {"status": "ok", "message": "CONFIRMLEAVE"}

        return {"status": "error", "message": "UNKNOWN COMMAND"}

    def remove_user(self, ip: str):
        """Remove o IP da lista de arquivos ativos"""
        with self.lock:
            if ip in self.all_files:
                del self.all_files[ip]
