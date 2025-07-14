# 🔗 Napster P2P com JSON + Persistência

[![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Sistema P2P inspirado no modelo clássico do Napster, que permite:

- Compartilhamento de arquivos entre clientes via sockets TCP
- Registro e busca de arquivos usando um servidor central com persistência
- Comunicação entre clientes para download direto (P2P)
- Protocolo de mensagens baseado em JSON
- Validação de segurança no manuseio de arquivos

---

## 🚀 Como executar

### 1. Instalar dependências (apenas Python 3)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. Preparar estrutura do projeto
```bash
python setup_project.py
```
Isso criará as pastas public/, downloads/ e arquivos de exemplo.

### 3. Rodar o servidor
```bash
python run_server.py
```

### 4. Rodar um ou mais clientes (em outro terminal)
```bash
python run_client.py
```

💬 Comandos do cliente
```yaml
1: search <termo>            → Busca arquivos no servidor
2: download <arquivo> <ip>   → Baixa arquivo de outro peer
3: quit                      → Sai da rede
```

📁 Estrutura do projeto
```php
napster_p2p_json/
├── napster_server_json.py     # Código do servidor
├── napster_client_json.py     # Código do cliente
├── run_server.py              # Script para iniciar o servidor
├── run_client.py              # Script para iniciar o cliente
├── setup_project.py           # Prepara estrutura inicial
├── server_data.json           # Estado do servidor (gerado automaticamente)
├── public/                    # Arquivos públicos do cliente
├── downloads/                 # Arquivos recebidos de outros peers
├── LICENSE                    # Licença do projeto
└── README.md                  # Este arquivo
```

🧪 Exemplo de uso
```bash
> search musica
1. musica.mp3 (32700 bytes) - 192.168.1.12

> download musica.mp3 192.168.1.12
✅ Arquivo 'musica.mp3' baixado com sucesso.
```
📌 Melhorias futuras
```
🔒 Criptografia com SSL (TLS)

🆔 Autenticação de peers

📡 Download segmentado e paralelo

✅ Verificação de integridade com hash (SHA256)

🎨 Interface gráfica (Tkinter, PyQt ou Web)
```

### ⚖️ Licença
Distribuído sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

### 👨‍💻 Autor
Desenvolvido por Guilherme Henrique de Abreu Pessoa — para fins educacionais no contexto de estudos de Sistemas Distribuídos e Redes P2P.
