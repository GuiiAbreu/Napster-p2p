from napster_server import NapsterServer

if __name__ == '__main__':
    print("Iniciando servidor Napster melhorado na porta 1234...")
    try:
        NapsterServer().start()
    except KeyboardInterrupt:
        print("\nServidor encerrado manualmente.")
