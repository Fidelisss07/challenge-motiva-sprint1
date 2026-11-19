# Olho na Lente — Challenge Motiva × FIAP · Sprints 1 e 2

Turma **1CCPR** · FIAP Ciência da Computação

| Integrante | RM |
|---|---|
| Gustavo Fidelis de Souza e Silva | 574666 |
| Luan Mantovani Ferreira Neres | 574563 |
| Pedro Henrique de Sá | 576731 |
| Fernando Azevedo Costa | 575676 |
| Rafael Meirelles | 574897 |
| Anna Luisa Lima | 575081 |

**Projeto:** Olho na Lente detecta quando uma câmera de CFTV da rodovia está com a imagem ruim e separa falha real (lente suja, teia, desfoque) de condição do tempo (chuva, neblina, sol), comparando com as câmeras vizinhas e a estação meteorológica. As falhas reais alimentam o cálculo de confiabilidade λ e R(t) = e^(−λt). Temas 2.1 + 2 da Motiva.

## Pastas

| Pasta | Disciplina | Conteúdo |
|---|---|---|
| `02-python-allan/` | PCP com Python | 4 questões, diagrama de blocos, cronograma, protótipo Python |
| `03-ml-lucas/` | Machine Learning | base real (UCI Air Quality), notebook, relatório |
| `04-matematica-igor/` | Matemática | cálculos e interpretações |
| `05-cpp-daniel/` | Estruturas de Dados (C++) | `sprint_confiabilidade.cpp` e relatório |
| `06-arquitetura-sandro/` | Arquitetura de Computadores | projeto Pesa Certo |
| `07-cs-mauricio/` | Computational Systems | circuito, expressão, tabela-verdade e prints do simulador |
| `08-energias-luciana/` | Energias | vídeo do pré-projeto, roteiro e entrega |

A disciplina de IA (Prof. Jorge) fica num repositório próprio: [engman-copilot](https://github.com/Fidelisss07/engman-copilot).

## Links

| O quê | Link |
|---|---|
| Vídeo do pré-projeto (Luciana, YouTube, não listado) | https://youtu.be/tFxXDGNCXn0 |
| Código C++ no onlinegdb (Daniel) | https://onlinegdb.com/pahTtOEJx |
| Repositório da disciplina de IA (Jorge) | https://github.com/Fidelisss07/engman-copilot |
| Vídeo do pitch de 1 min (Allan) | a publicar |

## Como rodar

- Protótipo Python: `pip install opencv-python numpy` e `python 02-python-allan/prototipo/prototipo_olho_na_lente.py`
- C++: `g++ 05-cpp-daniel/sprint_confiabilidade.cpp -o conf && ./conf`
- Notebook: abrir `03-ml-lucas/analise_exploratoria_sensores.ipynb` no Jupyter ou Colab.

## Uso de IA

O grupo usou o Claude (Anthropic) como apoio na redação, nos diagramas, no código, na montagem do circuito no simulador e na animação do vídeo. A narração do vídeo da Luciana usa voz de IA (ElevenLabs). Revisão: Gustavo Fidelis.
