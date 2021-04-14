## Monitoramento de Sistema

  O sistema foi desenvolvido totalmente na linguagem [**Python**](https://docs.python.org/3/) e tem como objetivo captar informações do sistema operacional da máquina servidor conforme as requisições do cliente e mostrá-las através de uma interface de usuário. 

### Módulos utilizados

* [**Psutil**](https://psutil.readthedocs.io/en/latest/) - Biblioteca de plataforma cruzada para recuperar informações sobre os processos em execução e a utilização do sistema (CPU, memória, discos, rede, sensores) em Python.
* [**OS**](https://docs.python.org/pt-br/3/library/os.html) - Fornece a linguagem python uma maneira simples de usar funcionalidades que são dependentes de sistema operacional.
* [**Socket**](https://docs.python.org/3/library/socket.html) - Fornece acesso à interface de soquete BSD, responsável pela troca de informações entre cliente e servidor.
* [**Pickle**](https://docs.python.org/3/library/pickle.html) - Responsável pela conversão de bytes para dados, implementa protocolos binários para serializar e desserializar uma estrutura de objeto Python.
* [**Time**](https://docs.python.org/3/library/time.html) - Fornece várias funções relacionadas ao tempo.
* [**Cpuinfo**](https://github.com/workhorsy/py-cpuinfo) - Fornece informações específicas da CPU.
* [**Nmap**](https://pypi.org/project/python-nmap/) - Fornece um mapeamento da rede.
* [**PySimpleGUI**](https://pysimplegui.readthedocs.io/en/latest/) - Responsável pela interface com o usuário.

### **Informações coletadas**

* **CPU :** Retorna o nome, modelo, arquitetura, palavra e núcleos.  
* **ARMAZENAMENTO :** Retorna o espaço total, livre e ocupado da memória RAM e do Disco Rígido.  
* **ARQUIVOS E DIRETÓRIOS :** 
  * Realiza uma busca através do nome e do caminho do arquivo/diretório informados pelo usuário.
  * Retorna seu tamanho, data de criação e data de modificação.
* **PROCESSOS :**
  * Realiza uma busca através do PID do processo informado pelo usuário.
  * Retorna seu nome, executável, memória consumida e CPU consumido.  
* **REDE :** A parte do programa relacionada a redes contém um scanner de portas que percorre um intervalo de portas informado pelo usuário e retorna o número e o status de cada porta.

### **Detalhamento sobre os métodos**

#### Lado cliente

* `mostrar_menu()`

  1. Define o layout da janela de menu através de uma lista contendo outras listas. Uma lista com um título como texto e outra lista com os títulos dos botões.
  2. Define a janela setando o título e o layout
  3. Se conecta ao servidor usando o connect()
  4. Itera a leitura dos eventos e dos valores da janela e envia os títulos dos botões como requisição ao servidor de acordo com os eventos de click em casa botão.
  
* `mostrar_info_cpu_memória()`

  1. Recebe os bytes contendo a resposta do servidor
  2. Carrega a resposta em forma de uma lista de strings
  3. Define o layout da janela de cpu e memória através de uma lista contendo outras listas. Uma lista com o título de cada sessão e outra lista com as informações acessadas pelo índice da lista dos dados recebidos, todas como texto.
  4. Define a janela setando o título e o layout
  5. Itera a leitura dos eventos e dos valores da janela

* `mostrar_info_arquivos_diretorios()`

  1. Define o layout da janela de arquivos/diretórios através de uma lista contendooutras listas. Uma lista com um texto de solicitação e um input de usuário para requerer o nome do arquivo, outra lista com um texto de solicitação, um input de usuário para requerer o caminho do arquivo e um botão OK e mais uma definindo uma tela de output.
  2. Define a janela setando o título e o layout
  3. Itera a leitura dos eventos e dos valores da janela e seta os inputs de usuário
  em variáveis como valores
  4. Envia os inputs para o servidor, recebe a lista de resposta e printa no output os dados acessados pelo índice da lista de resposta quando disparado o evento do
  botão OK
  
* `mostrar_info_processos()`

  1. Define o layout da janela de arquivos/diretórios através de uma lista contendo
  outras listas. Uma lista com um texto de solicitação e um input de usuário para
  requerer o PID do processo e um botão OK e outra definindo uma tela de
  output.
  2. Define a janela setando o título e o layout
  3. Itera a leitura dos eventos e dos valores da janela e seta o input de usuário e uma variável como valor
  4. Envia o input para o servidor, recebe a lista de resposta e printa no output os dados acessados pelo índice da lista de resposta quando disparado o evento do botão OK
  
* `mostrar_scanner_portas():`

  1. Define o layout da janela de scanner de portas através de uma lista contendo outras listas. Uma lista com um texto de solicitação e um input de usuário para requerer o Ip alvo, outra lista com um texto de solicitação e dois inputs para requerer o valor de porta mínima e porta máxima e um botão SCAM e outrdefinindo uma tela de output.
  2. Define a janela setando o título e o layout
  3. Itera a leitura dos eventos e dos valores da janela e seta os inputs de usuário
  em variáveis como valores
  4. Envia os inputs para o servidor, recebe a lista de resposta e printa, a cada dois segundos, no output os dados acessados pelo índice da lista de resposta quando   disparado o evento do botão SCAM
 
 #### Lado Servidor
 
 * `conexao_cliente()`
 
    1. Define o ip do host
    2. Define a porta de conexão
    3. Abre o socket
    4. Concatena host e porta
    5. Inicia a escuta de conexões e printa a mensagem de espera no console
    6. Quando o cliente se conecta, o servidor aceita a conexão, definindo host cliente e seu endereço após isso imprime a mensagem de “conectado” no console
    7. Itera o recebimento das requisições dos eventos captados pelo menu do cliente
    8. De acordo com cada requisição recebida, envia as respostas processadas porcada método do servidor

* `dados_cpu()`

  1. Coleta as informações da CPU com o cpuinfo.get_cpu_info()
  2. Define o número total de nucleos com o psutil.cpu_count()
  3. Define os núcleos físicos com o psutil.cpu_count(logical=False)
  4. Monta os dados da CPU em string
  5. Retorna os dados da CPU  

* `dados_memoria_ram()`

  1. Coleta as informações sobre memória RAM com o psutil.virtual.memory()
  2. Calcula a memória total
  3. Calcula a memória utilizada
  4. Calcula o espaço de memória livre
  5. Monta os dados de memória em uma string
  6. Retorna os dados de memória

* `dados_disco()`

  1. Coleta as informações sobre disco com o psutil.disk_usage(“.”)
  2. Calcula o espaço total de disco
  3. Calcula o espaço utilizado
  4. Calcula o espaço livre
  5. Monta os dados de disco em uma string
  6. Retorna os dados de disco

* `dados_cpu_memoria()`

  1. Define uma lista de resposta vazia
  2. Adiciona os dados da CPU na lista de resposta
  3. Adiciona os dados da memória RAM na lista de resposta
  4. Adiciona os dados do disco rígido na lista de resposta
  5. Retorna a lista de resposta

* `dados_arquivos_diretorios(PARAM: cliente - conexão com o cliente)`

  1. Recebe o nome do arquivo/diretório
  2. Recebe o caminho do arquivo/diretório
  3. Define a lista de resposta vazia
  4. Coleta os arquivos/diretórios da pasta corrente com o os.listdir(“.”)
  5. Percorre a lista de arquivos/diretórios e coleta suas informações com o os.stat() colocando o caminho como parâmetro
  6. Se o nome do arquivo/diretório da lista for igual ao nome recebido, adiciona o tamanho, a data de criação e a data de modificação do arquivo/diretório na lista de resposta
  7. Retorna a lista de resposta

* `dados_processos(PARAM: cliente - conexão com o cliente)`

  1. Recebe o PID do processo
  2. Define a lista de resposta vazia
  3. Coleta a lista de pids da máquina com o psutil.pids()
  4. Percorre a lista de pids coletando o processo de cada pid
  5. Se o pid da lista for igual ao pid recebido, adiciona o nome, o executável, a memória consumida e o cpu consumido do processo a lista de resposta
  6. Retorna a lista de resposta

* `dados_scanner_rede(PARAM: cliente - conexão com o cliente)`

  1. Recebe o ip alvo
  2. Recebe a porta mínima
  3. Recebe a porta máxima
  4. Define o scanner com o nmap.PortScanner()
  5. Define a lista de resposta vazia
  6. Percorre o intervalo das portas mínima e máxima
  7. Define o ip e a porta que serão escaneadas com nmap.scan
  8. Coleta os status de ip e porta
  9. Adiciona a porta escaneada e seu status na lista de resposta
  10. Retorna a lista de resposta


## Imagens das telas de execução

![menu](https://user-images.githubusercontent.com/62779108/114598527-616d0a80-9c68-11eb-9f78-e96960023da9.png)

![cpu_memoria](https://user-images.githubusercontent.com/62779108/114598551-6a5ddc00-9c68-11eb-8e06-b3ad03f9430f.png)

![arquivos-diretorios](https://user-images.githubusercontent.com/62779108/114598594-73e74400-9c68-11eb-9113-293a2328eec2.png)

![processo](https://user-images.githubusercontent.com/62779108/114598613-79dd2500-9c68-11eb-96ab-8bd02edb8c3b.png)

![scanner-portas](https://user-images.githubusercontent.com/62779108/114598632-7ea1d900-9c68-11eb-8856-a6bc2c591689.png)
