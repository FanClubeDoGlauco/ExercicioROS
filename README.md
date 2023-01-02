# Fan Clube do Glauco - Projeto Conexão Remota EPOS

### Colaboradores

Ana Beatriz S. Araujo   11232538 </br>
Arthur Gomes da Silveira  10746939 </br>
Lucas Borgonovi  10685657 </br>
Otávio Augusto Estevão Nascimento    11232285 </br>
Pedro Augusto Queiros de Oliveira    09782382 </br>

### Descrição

Interface para operação com envio de instruções de comando á Controladoras Maxon tipo EPOS, acopladas à um motor de giro. A interface permite comunicação direta com a controladora, podendo ativar funções sem a utilização de um software e maior flexibilidade para aplicações.


### Instalação

#### Para usar o software você deve ter os seguintes pré-requisitos:

- Python >=3.7.x
- EPOS 0, 1, 2, 3, 4, P
- Computador Sistema Operacional Linux ou Windows
- Motor compatível com controladora

A Interface foi desenvolvida utilizando python. As seguintes bibliotecas foram utilizadas:
- CustomTKInter
- ctypes

Para comunicação do programa com a controladora, é necessário o arquivo .dll contendo a biblioteca dinâmica para instruir o programa a executar as funções pré programadas na controladora.

![image](https://user-images.githubusercontent.com/117764269/207456058-7afb5e47-52ed-4aeb-ba1b-c9052bdd56a7.png)

Acima, pode-se observar como é feita a comunicação serial da controladora com o Sistema Operacional e com o motor.

Após estabelecida a comunicação, executa-se o programa .py para controlar o motor.

![image](https://user-images.githubusercontent.com/117764269/208088011-a5fd7b21-02a2-46b3-9d73-1c1dcbc5ef1d.png)

Observa-se instruções para utilização da interface na imagem.

Os parâmetros para conexão podem ser obtidos pelo gerenciamento de dispositivo ou pelo EPOS Studio.

Após preenchimento correto dos parâmetros, o usuário deve selecionar pode optar entre duas funções, ou a quantidade de steps ou definir um perfil de velocidades contínuo. Para isso, ele deve utilizar o 'slider' na parte inferior os parâmetros e clicar no botão "Enviar Comando Steps" para girar a quantidade escolhida ou "Enviar Comando Velocidade" Para girar na velocidade escolhida

Para Embarcar o programa, utilizou-se o PyInstaller (Pode-se ser obtido utilizado o comando 'pip install pyinstaller') e criou-se um executável do programa. Este executável funciona em OS Windows, porém o mesmo procedimento pode ser utilizado para gerar um executável para OS Linux ou Ubuntu. Assim, é possivel executar o programa sem a necessidade de um interpretador, no caso o python, e consequentemente, pode ser utilizado no sistema embarcado.

![image](https://user-images.githubusercontent.com/117764269/208171012-3dbd726d-75f8-49a0-976c-30e1dd3b04e1.png)


