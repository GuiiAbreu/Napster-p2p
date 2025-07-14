# setup_project.py
import os

def create_directories():
    directories = ["public", "downloads"]
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"✅ Pasta '{d}' criada.")
        else:
            print(f"ℹ️ Pasta '{d}' já existe.")

def create_example_files():
    examples = {
        "public/exemplo1.txt": "Este é um arquivo de exemplo 1.",
        "public/musica.mp3": "Dados simulados de um arquivo MP3...",
        "public/documento.pdf": "Simulação de conteúdo PDF..."
    }

    for path, content in examples.items():
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Arquivo de exemplo criado: {path}")
        else:
            print(f"ℹ️ Arquivo já existe: {path}")

if __name__ == "__main__":
    print("🔧 Inicializando estrutura do projeto P2P...")
    create_directories()
    create_example_files()
    print("🏁 Setup concluído!")
