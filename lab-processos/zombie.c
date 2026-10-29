#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

int main() {
    pid_t child_pid = fork();
    
    if (child_pid > 0) {
        printf("PAI: Meu PID e %d\n", getpid());
        printf("PAI: O PID do meu filho e %d\n", child_pid);
        printf("PAI: Vou dormir por 60 segundos. O filho vai virar zumbi!\n");
        sleep(60);
        printf("PAI: Acordei. Vou limpar o zumbi agora.\n");
        wait(NULL);
        printf("PAI: Zumbi enterrado com sucesso.\n");
        sleep(10);
    } else if (child_pid == 0) {
        printf("FILHO: Meu PID e %d. Vou morrer agora!\n", getpid());
        exit(0);
    }
    return 0;
}
