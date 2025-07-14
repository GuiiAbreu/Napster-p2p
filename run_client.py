from napster_client import NapsterClient

if __name__ == '__main__':
    print("Iniciando cliente Napster melhorado...")
    try:
        NapsterClient().start()
    except KeyboardInterrupt:
        print("\nCliente encerrado manualmente.")
