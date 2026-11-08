# Diário de Bordo - DevOps Lab

## Ambiente
- Sistema: Debian 13 (Trixie)
- Usuário: leonardo
- CPUs: 8
- RAM: 11 GiB
- Disco: 222 GB (203 GB livres)
- Swap: 11 GiB
- Data de início: 22/09/2026

## Estrutura
- lab-processos/       → Processos zumbis
- lab-oom/             → OOM Killer
- lab-disco/           → Disco vs inodes
- lab-rede/            → Portas TCP
- lab-load/            → Load Average
- lab-cgroups/         → Cgroups
- lab-systemd/         → Serviços e timers
- lab-bash/            → Scripts
- lab-troubleshooting/ → Cenários reais
- lab-seguranca/       → Firewall e SSH
- lab-kernel/          → sysctl e tuning
- docker-lab/          → Dockerfiles
- compose-lab/         → Docker Compose
- multi-stage-lab/     → Multi-stage builds
- python-api-lab/      → CLI em Python
- lab-diary/           → Este diário

## Progresso
- [x] Estrutura criada
- [ ] Ferramentas instaladas
- [ ] Linux fundamentos
- [ ] Docker
- [ ] Kubernetes
# Experimento 2: OOM Killer (19/10/2026)
- Instalei o Docker no Debian 13.
- Criei o script comedor.py que aloca memória em blocos de 50MB.
- Rodei o container com limite estrito de 256MB de RAM.
- O processo alocou memória até estourar o cgroup e o kernel o matou.
- Verifiquei o código de saída (137 = SIGKILL), confirmando a ação do OOM Killer.

**Lógica:** Quando o container atinge o memory.max, o OOM Killer do kernel atua dentro do namespace do cgroup, matando o processo mais pesado (SIGKILL). É o mesmo mecanismo do OOMKilled no Kubernetes.
## Experimento 3: Disco vs Inodes (21/10/2026)
- Criei um disco virtual ext4 limitado a 50 inodes.
- Tentei criar 60 arquivos pequenos.
- Ao chegar no 51º arquivo, o sistema retornou "No space left on device".
- O comando `df -h` mostrou espaço livre, mas o `df -i` mostrou 100% de uso.

**Lógica:** Cada arquivo consome 1 inode. Não importa o tamanho do arquivo. Se os inodes acabarem, não é possível criar novos arquivos, mesmo com espaço em disco sobrando. Isso acontece muito com sessões PHP ou caches que criam milhões de arquivos minúsculos.
## Experimento 4: Portas TCP - CLOSE_WAIT (21/10/2026)
- Criei um servidor Python que não fecha o socket após enviar a resposta.
- Gerei múltiplas conexões com curl.
- Usei `ss -tanp` e vi várias conexões no estado CLOSE-WAIT.
- Isso prova um bug de código (vazamento de file descriptors).

**Lógica:** TIME_WAIT é normal (segurança do TCP). CLOSE_WAIT é problema: o cliente fechou, mas o servidor não chamou close(). Em produção, CLOSE_WAIT acumulado derruba a aplicação por falta de sockets.
[200~## Experimento 5: Load Average e I/O Wait (21/10/2026)
- Usei o `stress` para gerar carga de CPU e depois de I/O.
- Monitorei com `uptime` e `mpstat`.
- Na carga de CPU, o %usr foi para as alturas.
- Na carga de I/O, o Load subiu, mas o %iowait dominou e o %usr ficou baixo.
- Usei o `vmstat` para ver a coluna 'b' (bloqueados por I/O).

**Lógica:** Load Average não é uso de CPU. Ele conta processos rodando (r) + processos bloqueados em I/O (b). Load alto com CPU baixa significa que o disco está lento e segurando o sistema.
## Experimento 6: Cgroups (21/10/2026)
- Criei um cgroup manual (`lab_teste`) limitando a memória a 50MB.
- Rodei o script Python dentro desse cgroup e o processo foi morto (OOM).
- Inspecionei um container Docker e vi que ele cria um cgroup próprio (memory.max = 64MB).
- Entendi que o Docker e o Kubernetes são apenas "gerentes" em cima dos Cgroups do Linux.

**Lógica:** Cgroups limitam CPU, memória e I/O de grupos de processos. O Kubernetes usa isso para evitar que um pod consuma a RAM de todo o nó.
## Fase 3: Docker Local (23/10/2026)
- Docker instalado com sucesso no Debian 13.
- Rodei o primeiro container Nginx mapeando a porta 8080.
- Acessei via curl e explorei o interior do container (exec).
- Verifiquei logs e limpei o ambiente.

**Lógica:** O container é um processo isolado usando cgroups e namespaces. O Docker gerencia o ciclo de vida (run, ps, logs, exec, rm).
## Dockerfile: Primeira Imagem Própria (23/10/2026)
- Criei um arquivo `index.html` personalizado.
- Escrevi um `Dockerfile` usando `FROM nginx:alpine` e `COPY`.
- Build da imagem com `docker build -t minha-imagem-web:1.0 .`
- Rodei o container e o HTML personalizado respondeu no `curl`.

**Lógica:** O Dockerfile é a receita. O `docker build` constrói a imagem. O `docker run` cria o container. O `COPY` insere o arquivo local na imagem final.
## Docker Compose (24/10/2026)
- Criei um `docker-compose.yml` com dois serviços: Nginx e Redis.
- Subi o ambiente com `docker compose up -d`.
- Acessei o Nginx na porta 8082 e obtive PONG do Redis.
- Derrubei tudo com `docker compose down`.

**Lógica:** O Compose lê o YAML, cria uma rede isolada e sobe todos os serviços de uma vez. O `volumes` mapeia a pasta local para dentro do container. É a base do que o Kubernetes faz, mas local e mais simples.
## Fase 5: Kubernetes (31/10/2026)
- Instalei kubectl e K3d.
- Criei um cluster local com 1 server e 3 agents (4 nós).
- Fiz o deploy de um Nginx com 2 réplicas.
- Expus o serviço e acessei via `kubectl port-forward`.
- Aprendi que a porta 8080 já estava ocupada pelo LoadBalancer do K3d e usei a 8081.

**Lógica:** O Kubernetes orquestra containers. O Deployment mantém o estado desejado (2 réplicas), o Service expõe os pods de forma estável, e o port-forward cria um túnel para debug local.
## Kubernetes: Ingress, ConfigMap e Secret (31/10/2026)
- Criei um ConfigMap e um Secret para separar configuração e dados sensíveis.
- Instalei o Nginx Ingress Controller via Helm.
- Criei um recurso Ingress para rotear o tráfego do host `devopero.local` para o serviço `nginx-web`.
- Testei o roteamento com `curl -H "Host: devopero.local"`.
## Kubernetes: Ingress, ConfigMap e Secret (31/10/2026)
- Criei um ConfigMap (nginx-config) e um Secret (nginx-secret).
- Instalei o Nginx Ingress Controller via Helm.
- Criei um recurso Ingress roteando o host `devopero.local` para o serviço `nginx-web`.
- Testei com `curl -H "Host: devopero.local"` e o Nginx respondeu corretamente.

**Lógica:** O Ingress é a porta de entrada do cluster. Ele lê o cabeçalho HTTP Host e decide para qual serviço interno encaminhar a requisição. O ConfigMap e o Secret mantêm a configuração separada da imagem do container.
## Kubernetes: Persistência (PV e PVC) - 08/11/2026
- Criei um PersistentVolumeClaim (nginx-pvc) pedindo 1Gi de espaço.
- O cluster provisionou automaticamente usando a StorageClass local-path.
- Atualizei o Deployment do Nginx para montar esse volume.
- Escrevi um arquivo dentro do container e matei o Pod.
- O Kubernetes recriou o Pod e o arquivo continuou lá. Persistência confirmada!

**Lógica:** O PV é o disco físico. O PVC é o pedido. O Deployment monta o PVC dentro do container. Quando o Pod morre, o PVC e os dados continuam intactos e são remontados no próximo Pod.
