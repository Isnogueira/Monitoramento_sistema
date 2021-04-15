import os, psutil, socket, pickle, time
import PySimpleGUI as sg

host = socket.gethostname()
porta = 8899
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tema = "LightBlue 7"

# FUNÇÃO CPU, RAM E DISCO
def mostrar_info_cpu_memoria():
    
    bytes = socket_cliente.recv(1024)
    dados_cpu_mem = pickle.loads(bytes)
    
    sg.theme(tema)
    
    layout_cpu_mem = [[sg.Text("Informações sobre CPU", font='Helvetica 15', justification='center')],
        [sg.Text(str(dados_cpu_mem[0]))],
        [sg.Text("Informações sobre memória RAM",font='Helvetica 15', justification='center')],
        [sg.Text(str(dados_cpu_mem[1]))],
        [sg.Text("Informações sobre disco rígido", font='Helvetica 15', justification='center')],
        [sg.Text(str(dados_cpu_mem[2]))]]
    
    window_cpu_mem = sg.Window("CPU e Memória", layout_cpu_mem)
    
    while True:
        event_cpu_mem, values_cpu_mem = window_cpu_mem.read()
        if event_cpu_mem == sg.WIN_CLOSED or event_cpu_mem == "Exit": 
            window_cpu_mem.close()
            break

# FUNÇÃO ARQUIVOS E DIRETÓRIOS
def mostrar_info_arquivos_diretorios():
            
    sg.theme(tema)
    
    layout_arq_dir = [[sg.Text("Informe o nome do diretório"), sg.InputText(key=("nome_diretorio"))],
    [sg.Text("Informe o caminho do diretorio"), sg.InputText(key=("caminho_diretorio")), sg.OK()],
    [sg.Text("NOME     TAMANHO(kb)      DATA DE CRIAÇÃO       DATA DE MODIFICAÇÃO")],
            [sg.Output(size=(70, 8))]]
    
    window_arq_dir = sg.Window('Informações sobre arquivos em diretórios', layout_arq_dir)
    
    while True:
        event_arq_dir, values_arq_dir = window_arq_dir.read()
        nome_diretorio = values_arq_dir["nome_diretorio"] # 
        caminho_diretorio = values_arq_dir["caminho_diretorio"] 
        
        if event_arq_dir == "OK":
            try:
                socket_cliente.send(nome_diretorio.encode("UTF8"))
                socket_cliente.send(caminho_diretorio.encode("UTF8"))
                bytes = socket_cliente.recv(1024)
                dados_dir = pickle.loads(bytes)
                for dic in dados_dir:
                    for i in dic:
                        print(f"{i}      {dic[i][0]}          {dic[i][1]}       {dic[i][2]}") 
                break
            except:
                for j in dados_dir:
                    print(j) 
                break
        
        elif event_arq_dir == sg.WIN_CLOSED or event_arq_dir == 'Exit':
            window_arq_dir.close()
            break

# FUNÇÃO PROCESSOS
def mostrar_info_processos():
    
    sg.theme(tema)
    
    layout_proc = [[sg.Text("Informe o pid do processo"), sg.Input(size=(10, 0), key=("p")), sg.OK()],
        [sg.Output(size=(70, 10))]]
    
    window_proc = sg.Window('Informações sobre processos', layout_proc)
    
    while True:
        event_proc, values_proc = window_proc.read()
        pid = values_proc["p"]
        if event_proc == "OK":
            socket_cliente.send(pid.encode("UTF-8"))
            bytes = socket_cliente.recv(1024)
            dados_proc = pickle.loads(bytes)
            print()
            print("Processo encontrado...")
            print()
            print(f"{str(dados_proc[0])}\n{str(dados_proc[1])}\n{str(dados_proc[2])}\n{str(dados_proc[3])}")
            break
        elif event_proc == sg.WIN_CLOSED or event_proc == 'Exit':
            window_proc.close()
            break

# FUNÇÃO SCANNER DE REDE
def mostrar_scanner_portas():
    
    sg.theme(tema)
    
    layout_scanner = [[sg.Text("Informe o ip alvo:"), sg.Input(size=(15, 0), key=("ip_alvo"))],
            [sg.Text("Informe o intervalo das portas:"), sg.Input(size=(5, 0), key=("porta_min")), sg.Text("a"), sg.Input(size=(5, 0), key=("porta_max")), sg.Button("Scan")],
            [sg.Output(size=(45, 10))]]
    
    window_scanner = sg.Window("Scanner de portas", layout_scanner)
    
    while True:
        
        event_scanner, values_scanner = window_scanner.read()
        ip_alvo = values_scanner["ip_alvo"]
        porta_min = values_scanner["porta_min"]
        porta_max = values_scanner["porta_max"]
        
        if event_scanner == "Scan":
            socket_cliente.send(ip_alvo.encode("UTF-8"))
            socket_cliente.send(porta_min.encode("UTF-8"))
            socket_cliente.send(porta_max.encode("UTF-8"))
            bytes = socket_cliente.recv(4096)
            dados_scanner = pickle.loads(bytes)
            print("Iniciando mapeamento das portas...")
            time.sleep(2)
            for i in dados_scanner:
                print(i)
                time.sleep(2)
            print("Finalizando o mapeamento...")
            time.sleep(2)
            print("FIM")
            break
        elif event_scanner == sg.WIN_CLOSED or event_scanner == 'Exit':
            window_scanner.close()
            break

# FUNÇÃO MENU PRINCIPAL
def mostrar_menu():

    sg.theme(tema)
    
    layout_menu = [[sg.Text('Escolha uma opção para começar...', justification='center')],
            [sg.Button("CPU e memória"), sg.Button('Arquivos em diretórios')],
            [sg.Button("Processos"), sg.Button("Scanner de rede")]]
    
    window_menu = sg.Window('Monitoramento de sistema', layout_menu)
    
    try:
        socket_cliente.connect((host, porta))
        while True:
            event_menu, values_menu = window_menu.read()
            if (event_menu == "CPU e memória"):
                socket_cliente.send(event_menu.encode("UTF-8")) 
                mostrar_info_cpu_memoria()
                
            elif (event_menu == "Arquivos em diretórios"):
                socket_cliente.send(event_menu.encode("UTF-8")) 
                mostrar_info_arquivos_diretorios()

            elif(event_menu == "Processos"):
                socket_cliente.send(event_menu.encode("UTF-8")) 
                mostrar_info_processos()
            
            elif(event_menu == "Scanner de rede"):
                socket_cliente.send(event_menu.encode("UTF-8")) 
                mostrar_scanner_portas()
        
            elif event_menu == sg.WIN_CLOSED or event_menu == "Exit":
                window_menu.close()
                socket_cliente.close()
                break
    except Exception as erro:
        print(str(erro))

if __name__ == '__main__':
    mostrar_menu()
    
