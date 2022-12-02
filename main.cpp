#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>

using namespace std;

int main(int argc, char *argv[])
{

    // Especifica��es do Server Socket
    sockaddr_in enderecoServidor;
    bzero((char*)&enderecoServidor, sizeof(enderecoServidor)); // Preenchendo toda a mem�ria do servidor com zeros
    enderecoServidor.sin_addr.s_addr = htonl(INADDR_ANY); // Defini-se que o servidor est� ouvindo todas as interfaces presentes
    enderecoServidor.sin_family = AF_INET; // Definindo o tipo de ip de comunina��o para IPv4

    int porta = 3200; // Porta para estabelecer a conex�o socket
    enderecoServidor.sin_port = htons(porta); // Definindo a porta de comunica��o

    int servidorCFG = socket(AF_INET, SOCK_STREAM, 0); // Definindo protocolo TCP para comunica��o

    if(servidorCFG < 0)
    {
        printf("\n Aconteceu um erro na inicializa��o do Servidor \n");
        exit(0);
    }

    int bStatus = bind(servidorCFG, (struct sockaddr*) &enderecoServidor, sizeof(enderecoServidor)); // Conectando o servidor na porta especificada

    if(bStatus < 0)
    {
        printf("\n Erro ao conectar na porta, pode ser que esteja sendo usada por outra aplica��o. \n");
        exit(0);
    }

    printf("\n Esperando conexao remota. \n");

    listen(servidorCFG, 5); // � espera da conex�o do terceiro

    // Criando comunica��o por mensagem em bits
    sockaddr_in newenderecoSocket;
    socklen_t newenderecoSocketSize = sizeof(newenderecoSocket);
    int estComun = accept(servidorCFG, (sockaddr *)&newenderecoSocket, &newenderecoSocketSize); // Modo de espera por mensagens ativado

    if(estComun < 0)
    {
        printf("\n Comunicacao n�o estabelicida. \n" );
        exit(1);
    }

    printf( "\n Comunicacao estabelicida com sucesso \n");

    int msgLeitura, msgRetornada = 0; //Vari�veis para armazenar mensagens recebidas e retornadas
    char msg[1500]; // Buffer da mensagem

    // Loop para troca de mensagem manopla-terceiro
    while(1)
    {
        printf("\n Aguardando mensagem \n");
        memset(&msg, 0, sizeof(msg)); // Capturando mensagem de terceiro
        msgLeitura += recv(estComun, (char*)&msg, sizeof(msg), 0);

        if(!strcmp(msg, "exit")) // Checa conexao
        {
            printf("\n Client saiu da sess�o...\n" );
            break;
        }

        printf("\n Coordenada x, Coordenada y, Coordenada z: %s \n", msg); // Dados obtidos de teceiro
        msgRetornada += send(estComun, (char*)&msg, strlen(msg), 0); //Envia mensagem recebida de volta para terceiro
    }

    // Encerra sockets
    close(estComun);
    close(servidorCFG);

    printf("\n Conexao finalizada \n");

    return 0;
}
