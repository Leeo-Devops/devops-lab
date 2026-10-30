# DevOps Lab

Laboratório prático de estudos em Linux, Docker e Troubleshooting, construído do zero para consolidar conhecimentos de infraestrutura, automação e containers.

## Tecnologias e Ferramentas
- **Sistemas Operacionais:** Linux (Debian 13)
- **Containers:** Docker, Docker Compose, Docker Hub
- **Linguagens/Scripts:** Bash, Python (Flask, subprocess)
- **Rede e Troubleshooting:** TCP/IP, `ss`, `tcpdump`, `nftables`

## Estrutura do Laboratório

O repositório está dividido em módulos práticos:

### 1. Fundamentos do Linux (`lab-processos`, `lab-oom`, `lab-disco`, `lab-rede`, `lab-load`)
Documentação e scripts de simulação de incidentes reais:
- **Processos Zumbis:** Criação e diagnóstico de processos em estado `Z`.
- **OOM Killer:** Simulação de esgotamento de memória e limites de cgroups.
- **Disco e Inodes:** Demonstração de falha por inodes esgotados (`df -i` vs `df -h`).
- **Portas TCP:** Identificação de vazamento de sockets (estado `CLOSE_WAIT`).
- **Load Average:** Análise de carga de CPU vs I/O bloqueado (`vmstat`, `mpstat`).

### 2. Docker (`docker-lab`, `compose-lab`, `multi-stage-lab`)
- Criação de imagens personalizadas via Dockerfile.
- Otimização de imagens com Multi-Stage Build.
- Orquestração local de serviços (Nginx + Redis) com Docker Compose.

### 3. Diário de Bordo (`lab-diary`)
A past

a `lab-diary` contém um log de tudo que foi estudado e resolvido, detalhando a lógica por trás de cada comando.

## Como executar
Cada pasta possui seus próprios arquivos. Para testar a orquestração:
```bash
cd compose-lab
docker compose up -d
