
# 🧬 Algoritmo Genético com Multi-Armed Bandit para o Problema das 8 Rainhas

Este repositório contém uma implementação de **Algoritmo Genético (AG)** para resolver o clássico problema das **8 Rainhas**, com o diferencial de usar uma estratégia de **Multi-Armed Bandit (UCB1)** para selecionar dinamicamente o melhor operador de crossover.

---

## 🧠 Problema das 8 Rainhas

O desafio consiste em posicionar 8 rainhas em um tabuleiro de xadrez 8x8 de forma que nenhuma possa atacar outra. Ou seja, não pode haver duas rainhas na mesma linha, coluna ou diagonal.

---

## 🔧 Tecnologias Utilizadas

- Python 3
- Numpy
- Matplotlib
- Plotly

---

## ⚙️ Parâmetros Configuráveis

```python
tamanho_tabuleiro = 8
tamanho_populacao = 100
taxa_mutacao = 0.1
taxa_cruzamento = 0.5
numero_geracoes = 999999
```

---

## 🚀 Como Funciona

### 1. Geração da População Inicial
Gera cromossomos como permutações válidas dos números de 0 a N-1, representando as posições das rainhas.

### 2. Avaliação de Fitness
A função de fitness penaliza colisões nas diagonais. O objetivo é maximizar o número de pares de rainhas que **não se atacam**.

### 3. Crossover com Seleção Adaptativa

O algoritmo implementa três tipos de **crossover**:
- `OPX` (One-Point Crossover)
- `OBX` (Order-Based Crossover)
- `ULX` (Uniform-Like Crossover)

A escolha do operador é feita com base no algoritmo **UCB1 (Upper Confidence Bound 1)**, que aprende quais operadores estão gerando melhores resultados ao longo das gerações.

### 4. Mutação
Realiza uma troca aleatória entre duas posições do cromossomo com uma certa probabilidade.

### 5. Seleção
Seleciona indivíduos aleatoriamente para reprodução, respeitando a taxa de crossover.

### 6. Substituição e Evolução
Gera uma nova população e continua o processo por até `numero_geracoes` ou até encontrar a solução ótima.

---

## 📊 Visualizações

- **Desempenho do AG (fitness ao longo das gerações)**
- **Uso dos Operadores de Crossover** (frequência de uso de OPX, OBX e ULX)

---

## 📈 Exemplo de Execução

```bash
$ python algoritmo_genetico.py
```

Saída esperada (caso solução seja encontrada):

```
Solução encontrada na geração 123
Cromossomo: [0 4 7 5 2 6 1 3] - Fitness: 28

. Q . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
Q . . . . . . .
. . . Q . . . .
```

---

## 📌 Sobre o UCB1

O algoritmo **UCB1** trata a escolha dos operadores de crossover como um problema de **bandido multi-braço**, onde cada operador é uma "máquina caça-níquel". Ele busca equilibrar **exploração** (testar operadores pouco utilizados) e **exploração** (utilizar os operadores que têm melhor desempenho).

---

## 📂 Estrutura do Código

- `AlgoritmoGenetico`: classe principal que executa o AG
- `MabUcb1`: seleção adaptativa dos operadores
- `opx`, `obx`, `ulx`: operadores de crossover
- `corrige`: garante permutação válida após crossover
- `fitness`, `mutacao`, `selecaoAleatoria`, etc.: funções auxiliares

---

---

## 🤝 Contribuições

Contribuições são bem-vindas! Fique à vontade para abrir issues ou pull requests.
