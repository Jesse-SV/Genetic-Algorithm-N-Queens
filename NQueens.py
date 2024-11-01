import random
from random import randint
import numpy as np
import math
from math import log, sqrt
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def corrige(cromossomo : list, n : int):
  cromossomoCorrigido = cromossomo
  qnts = [0 for i in range(n)]

  for i in range(len(cromossomoCorrigido)):
    qnts[cromossomoCorrigido[i]] = qnts[cromossomoCorrigido[i]] + 1

  for i in range(len(cromossomoCorrigido)):
    if qnts[cromossomoCorrigido[i]] > 1:
      pos = 0
      controle = True
      while pos < (n) and controle:
        if qnts[pos] == 0:
          controle = False
        else:
          pos = pos + 1
      qnts[cromossomoCorrigido[i]] = qnts[cromossomoCorrigido[i]] - 1
      qnts[pos] = qnts[pos] + 1
      cromossomoCorrigido[i] = pos

  return cromossomoCorrigido

# One point Crossover
def opx(pais : list, n : int):
  posicao = randint(1, n - 1)
  cromossomo = []
  cromossomo.extend(pais[0][:posicao])
  cromossomo.extend(pais[1][posicao:])
  cromossomo = corrige(cromossomo, n)
  return np.array(cromossomo)

# Order Based Crossover
def obx(pais : list, n : int):
  cromossomo = []

  x = randint(2, n)

  for i in range(x):
    cromossomo.append(pais[0][i])

  for i in range(n):
    if pais[1][i] not in cromossomo:
      cromossomo.append(pais[1][i])

  return np.array(cromossomo)

# Uniform Crossover
def ulx(pais : list, n : int):
  pais[0] = corrige(pais[0], n)
  pais[1] = corrige(pais[1], n)
  cromossomo = [-1 for i in range(n)]

  for i in range(n):
    if pais[0][i] == pais[1][i]:
      cromossomo[i] = pais[1][i]

  for i in range(n):
    if cromossomo[i] == -1:
      paisPossiveis = []
      for j in range(2):
        if pais[j][i] not in cromossomo:
          paisPossiveis.append(pais[j])
      if len(paisPossiveis) == 2:
        pai = randint(0, 1)
        cromossomo[i] = paisPossiveis[pai][i]
      elif len(paisPossiveis) == 1:
        pai = 0
        cromossomo[i] = paisPossiveis[0][i]

  for i in range(n):
    if i not in cromossomo:
      pos = randint(0, n - 1)

      while cromossomo[pos] != -1:
        pos = randint(0, n - 1)
      cromossomo[pos] = i

  return np.array(cromossomo)

class MabUcb1():
  def __init__(self, nOperadores: int):
    self.nOperadores = nOperadores
    self.nVezesUsado = [0 for i in range(self.nOperadores)]
    self.nJogadasTotal = 0
    self.somasRecompensas = [0 for i in range(self.nOperadores)]

  def selectArm(self):
    if self.nJogadasTotal < self.nOperadores:
      op = randint(0, self.nOperadores - 1)
      while self.nVezesUsado[op] > 0:
        op = randint(0, self.nOperadores - 1)
      self.nVezesUsado[op] += 1
      self.nJogadasTotal += 1
      return op

    maquinas = []
    for i in range(self.nOperadores):
      recompensaMedia = self.somasRecompensas[i] / self.nVezesUsado[i]
      maquinas.append(recompensaMedia + sqrt(2 * log(self.nJogadasTotal) / self.nVezesUsado[i]))
    maior = 0
    count = 1
    while count < self.nOperadores:
      if maquinas[count] > maquinas[maior]:
        maior = count
      count += 1
    self.nJogadasTotal += 1
    self.nVezesUsado[maior] += 1

    return maior

  def addReward(self, arm : int, reward : float):
    try:
      self.somasRecompensas[arm] += reward
    except:
      print("Erro na atribuição de recompensa")

class AlgoritmoGenetico:
    def __init__(self, tamanho_tabuleiro, tamanho_populacao, taxa_mutacao, taxa_cruzamento, numero_geracoes):
      self.tamanho_tabuleiro = tamanho_tabuleiro
      self.tamanho_populacao = tamanho_populacao
      self.taxa_mutacao = taxa_mutacao
      self.taxa_cruzamento = taxa_cruzamento
      self.numero_geracoes = numero_geracoes
      self.melhores_fitness = []
      self.opx = 0
      self.obx = 0
      self.ulx = 0

    def gerarCromossomo(self):
      # Gera uma permutação aleatória de números entre 0 e tamanho_tabuleiro-1 (sem repetição)
      cromossomo = np.random.permutation(self.tamanho_tabuleiro)
      return cromossomo

    def gerarPopulacao(self):
      populacao = []
      for i in range(self.tamanho_populacao):
        populacao.append(self.gerarCromossomo())
      return populacao

    def fitness(self, cromossomo):
      colisoes = 0

      # Contagem de colisões nas diagonais
      for i in range(len(cromossomo)):
          for j in range(i + 1, len(cromossomo)):  # Começar de i + 1 para evitar contar duplicatas
              dx = abs(i - j)
              dy = abs(cromossomo[i] - cromossomo[j])
              if dx == dy:
                  colisoes += 1

      total_pares = (len(cromossomo) * (len(cromossomo) - 1)) // 2
      return total_pares - colisoes

    def mutacao(self, cromossomo):
        if random.random() < self.taxa_mutacao:
            # Escolhe dois índices aleatórios dentro do cromossomo para trocar
            i, j = np.random.choice(len(cromossomo), 2, replace=False)  # Replace garante que a mesma rainha não seja escolhida
            cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]

    def crossover(self, pai1, pai2, ucb):
      operador = ucb.selectArm()
      filho = None
      if operador == 0:
        self.opx+=1
        filho = opx([pai1, pai2], self.tamanho_tabuleiro)
      elif operador == 1:
        self.obx+=1
        filho = obx([pai1, pai2], self.tamanho_tabuleiro)
      elif operador == 2:
        self.ulx+=1
        filho = ulx([pai1, pai2], self.tamanho_tabuleiro)

      if self.fitness(filho) > self.fitness(pai1) and self.fitness(filho) > self.fitness(pai2):
        ucb.addReward(operador, 1.0)
      else:
        ucb.addReward(operador, 0.0)

      return filho

    # Seleciona um indivíduo aleatório da população
    def selecaoAleatoria(self, populacao):
      return random.choice(populacao)

    def exibeCromossomo(self, cromossomo):
      print(f"Cromossomo: {cromossomo} - Fitness: {self.fitness(cromossomo)}")

    def exibeTabuleiro(self, cromossomo):
      tabuleiro = np.full((self.tamanho_tabuleiro, self.tamanho_tabuleiro), '.', dtype=str)

      # Colocar as rainhas de acordo com o cromossomo, de baixo para cima
      for coluna, linha in enumerate(cromossomo):
          tabuleiro[self.tamanho_tabuleiro - 1 - linha][coluna] = 'Q'

      print("\n".join(" ".join(linha) for linha in tabuleiro))
      print()

    def exibir_possibilidades(self):
        # Calcula o fatorial do tamanho do tabuleiro
        possibilidades = math.factorial(self.tamanho_tabuleiro)
        # Exibe o resultado
        print(f"Possibilidades: {possibilidades}")

    def graficoDesempenho(self):
      # Plotar o gráfico de desempenho
        plt.plot(self.melhores_fitness)
        plt.title("Desempenho do Algoritmo Genético")
        plt.xlabel("Geração")
        plt.ylabel("Melhor Fitness")
        plt.grid()
        plt.show()

    def graficoOperadores(self):
      # Nomes das variáveis
      labels = ['obx', 'opx', 'ulx']
      values = [self.obx, self.opx, self.ulx]

      # Definindo cores opacas: vermelho, verde e azul
      cores = [(1, 0, 0, 0.6),  # Vermelho
              (0, 1, 0, 0.6),  # Verde
              (0, 0, 1, 0.6)]  # Azul

      # Criando o gráfico de barras
      x = np.arange(len(labels))  # Localização das barras
      largura = 0.4  # Largura das barras

      plt.bar(x, values, width=largura, color=cores)

      # Adicionando título e rótulos
      plt.title('Desempenho dos Operadores')
      plt.xlabel('Operadores')
      plt.ylabel('Valores')
      plt.xticks(x, labels)  # Definindo rótulos no eixo x
      plt.grid(axis='y')

      # Exibindo o gráfico
      plt.show()

    def run(self):
      ucb1 = MabUcb1(3)
      populacao = self.gerarPopulacao()

      print(f"Fitness meta: {(self.tamanho_tabuleiro * (self.tamanho_tabuleiro - 1)) // 2}")
      self.exibir_possibilidades()

      for geracao in range(self.numero_geracoes):
        # print(f"Geração {geracao}")

        # Ordena a população de acordo com o fitness
        populacao = sorted(populacao, key=lambda x: self.fitness(x), reverse=True)
        self.melhores_fitness.append(self.fitness(populacao[0]))

        # Verifica se encontrou uma solução
        if self.fitness(populacao[0]) == (self.tamanho_tabuleiro * (self.tamanho_tabuleiro - 1)) // 2:
            print(f"Solução encontrada na geração {geracao}")
            self.exibeCromossomo(populacao[0])
            self.exibeTabuleiro(populacao[0])
            self.graficoDesempenho()
            self.graficoOperadores()
            return

        nova_populacao = []
        pais = []

        # Usa a taxa de cruzamento para decidir quantos pais vão realizar crossover
        num_pais = int(self.taxa_cruzamento * self.tamanho_populacao)

        # Seleciona os pais para a nova população
        while len(pais) < num_pais:
            pais.append(self.selecaoAleatoria(populacao))

        # Preenche a nova população com pais selecionados
        nova_populacao.extend(pais)

        # Preenche o restante da nova população com os filhos dos pais
        while len(nova_populacao) < self.tamanho_populacao:
            pai1 = self.selecaoAleatoria(pais)
            pai2 = self.selecaoAleatoria(pais)
            filho = self.crossover(pai1, pai2, ucb1)
            self.mutacao(filho)
            nova_populacao.append(filho)

        # Se precisar garantir que a nova população tenha exatamente o tamanho desejado
        # e se a população for impar, remova um indivíduo aleatório
        if len(nova_populacao) > self.tamanho_populacao:
            nova_populacao.pop()


        # Preenche o restante com indivíduos aleatórios
        while len(nova_populacao) < self.tamanho_populacao:
          nova_populacao.append(self.gerarCromossomo())

        # Substituir a população antiga pela nova
        populacao = nova_populacao

      print("Nenhuma solução encontrada")
      print(f"Geração: {geracao}")
      self.exibeCromossomo(populacao[0])
      self.exibeTabuleiro(populacao[0])
      self.graficoOperadores()

tamanho_tabuleiro = 8
tamanho_populacao = 100
taxa_mutacao = 0.1
taxa_cruzamento = 0.5
numero_geracoes = 999999

# Executando o algoritmo
algoritmo = AlgoritmoGenetico(tamanho_tabuleiro, tamanho_populacao, taxa_mutacao, taxa_cruzamento, numero_geracoes)
algoritmo.run()