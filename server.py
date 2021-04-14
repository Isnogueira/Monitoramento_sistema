import os, psutil, socket, pickle, cpuinfo, time, nmap

def dados_cpu():
    
    info_cpu = cpuinfo.get_cpu_info()
    nucleos_total = psutil.cpu_count()
    nucleos_fisicos = psutil.cpu_count(logical=False)
    resp_cpu = f"Nome: {str(info_cpu['brand_raw'])}"
    resp_cpu = resp_cpu + f"\nArquitetura: {str(info_cpu['arch'])}"
    resp_cpu = resp_cpu + f"\nPalavra(bits): {str(info_cpu['bits'])}"
    resp_cpu = resp_cpu + f"\nNúcleos: {nucleos_total}" 
    resp_cpu = resp_cpu + f"({nucleos_fisicos})"
    
    return resp_cpu


def dados_memoria_ram():
    
    mem = psutil.virtual_memory()
    total = round(mem.total/(1024 ** 3), 2)
    used = round(mem.used/(1024 ** 3), 2)
    free = round(mem.free/(1024 ** 3), 2)
    
    resp_ram = f"Total de memória RAM: {total} GB"
    resp_ram = resp_ram + f"\nEspaço utilizado: {used} GB"
    resp_ram = resp_ram + f"\nEspaço livre: {free} GB"
    
    return resp_ram

def dados_disco():
    
    disco = psutil.disk_usage(".")
    total = round(disco.total/(1024 ** 3), 2)
    used = round(disco.used/(1024 ** 3), 2)
    free = round(disco.free/(1024 ** 3), 2)
    
    resp_disco = f"Espaço total em disco: {total} GB"
    resp_disco = resp_disco + f"\nEspaço utilizado: {used} GB"
    resp_disco = resp_disco + f"\nEspaço livre: {free} GB"
    
    return resp_disco

def dados_cpu_memoria():

    resposta = []
    resposta.append(dados_cpu())
    resposta.append(dados_memoria_ram())
    resposta.append(dados_disco())
    
    return resposta


def dados_arquivos_diretorios(cliente):
    
    nome_arquivo = cliente.recv(1024).decode("UTF-8")
    caminho_arquivo = cliente.recv(1024).decode("UTF-8")
    
    resposta = []
    arq_dir = os.listdir(".")
    try:
        for i in arq_dir:
            if i == nome_arquivo:
                status = os.stat(caminho_arquivo)
                resposta.append(f"Tamanho: {round((status.st_size/1000), 2)} MB")
                resposta.append(f"Data de Criação: {time.ctime(status.st_atime)}")
                resposta.append(f"Data de Modificação: {time.ctime(status.st_mtime)}")
                return resposta          
    except Exception as erro:
        print(str(erro))

def dados_processos(cliente):
    
    p = cliente.recv(1024).decode("UTF-8")
    resposta = []
    lista_pids = psutil.pids()
    for i in lista_pids:
        if i == int(p) :
            proc = psutil.Process(int(p))
            resposta.append(f"Nome do processo: {proc.name()}")
            resposta.append(f"Nome do executável: {proc.exe()}")
            resposta.append(f"Porcentagem de memória consumida: {round(proc.memory_percent(), 2)}%")
            resposta.append(f"Porcentagem de CPU consumido: {proc.cpu_percent()}%")
            return resposta


def dados_scanner_rede(cliente):
    
    ip_alvo = cliente.recv(1024).decode("UTF-8")
    porta_min = cliente.recv(1024).decode("UTF-8")
    porta_max = cliente.recv(1024).decode("UTF-8")
    
    nm = nmap.PortScanner()
    resposta = []
    try:
        for porta in range(int(porta_min), int(porta_max) + 1):
            scan = nm.scan(ip_alvo, str(porta))
            port_state = (scan["scan"][ip_alvo]["tcp"][porta]["state"])
            resposta.append(f"Porta: {porta}  -------------------------------------------------  {port_state}")
        return resposta
    except Exception as erro:
        print(str(erro))


def conexao_cliente():
    
    host = socket.gethostname()
    porta = 8899
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_servidor.bind((host, porta))

    socket_servidor.listen()
    print(f"Servidor {host} esperando conexão na porta {porta}")

    cliente, endereco = socket_servidor.accept()
    print(f"Contectado a {str(endereco)}")

    while True :
        event = cliente.recv(1024)
        if event.decode("UTF-8") == "CPU e memória":
            resposta = dados_cpu_memoria()
            bytes = pickle.dumps(resposta)
            cliente.send(bytes)
            
        elif event.decode("UTF-8") == "Arquivos e Diretórios":
            resposta = dados_arquivos_diretorios(cliente)
            bytes = pickle.dumps(resposta)
            cliente.send(bytes)
            
        elif event.decode("UTF-8") == "Processos":
            resposta = dados_processos(cliente)
            bytes = pickle.dumps(resposta)
            cliente.send(bytes)

        elif event.decode("UTF-8") == "Scanner de rede":
            resposta = dados_scanner_rede(cliente)
            bytes = pickle.dumps(resposta)
            cliente.send(bytes)

        elif event.decode("UTF-8") == "Exit":
            cliente.close()
            socket_servidor.close()
            break
        

if __name__ == '__main__':
    conexao_cliente()