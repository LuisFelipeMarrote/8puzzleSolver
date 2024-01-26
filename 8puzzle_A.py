import copy #mz = copy.deepcopy(m) -> copia a matriz e não a sua referencia
from queue import PriorityQueue

#Funcoes do BFS:-----------------------------------------------------------------------------------------------------------------------------------------------------------

#enfilera os próximos passos que não retornem à um estado anterior:
def adiciona(queue, visitados, atual):
  if(atual.column < 2 and not visitado(NovoEstado('right', atual), visitados)):
    queue.append([atual, 'right'])
  if(atual.row < 2 and not visitado(NovoEstado('down', atual), visitados)):
    queue.append([atual, 'down'])
  if(atual.column > 0 and not visitado(NovoEstado('left', atual), visitados)):
    queue.append([atual, 'left'])
  if(atual.row > 0 and not visitado(NovoEstado('up', atual), visitados)):
    queue.append([atual, 'up'])
  return


#função que chama os passos:
def solve(inicial_state):
  queue = []  # fila: [estado inicial, ação]  -> dica do professor: guardar numero de passos (ex. ta no 6 e chegou p cima, procura um 5 na posição anterior)
  visitados = [] # vetor de estados visitados
  acertou = False
  caminho = []
  teste = inicial_state

  adiciona(queue, visitados, inicial_state)  #inicia a fila

  while queue and not acertou:
    iteracao = queue.pop(0)                       #remove da fila: (estado / ação)
    proximo = NovoEstado(iteracao[1], iteracao[0])
    proximo.parent = iteracao[0] 
    acertou = avalia(proximo)                 #avalia se este estado é o final
    visitados.append(proximo)
    adiciona(queue, visitados, proximo)                    #adiciona
    teste = proximo

  while teste:
    caminho.append([teste.board, teste.step])
    teste = teste.parent 
  return caminho


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#Estado = Tabuleiro atual + posição do vazio
class state:  
  
  def __init__(self, board, empty, step, parent = None ,profundidade = 0):
    self.board = board
    self.row = empty[0]
    self.column = empty[1]
    self.step = step      #step tha led to this state
    self.parent = parent 
    self.profundidade = profundidade

  def __lt__(self, other):
    # Compare instances based on the custo value
    return (heuristica(self.board) + self.profundidade) < (heuristica(other.board) + other.profundidade)

#imprime uma matriz
def printm(matrix):

  for x in matrix:
    print(x)

#recebe um estado e retorna se é a solução:
def avalia(estado):
  solucao = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', "x"]] # vetor com a solucao
  atual = estado.board
  if(atual  == solucao):
    return True
  return False

#recebe um estado e retorna se está na lista de já visitados ou não:
def visitado(estado, visitados):
  for anterior in visitados:
    if(anterior.board == estado.board):
      return True
  return False

#recebe uma matriz e duas pozições e troca elas
def swap(board, current_row, current_column, new_row, new_column):
  temp = board[current_row][current_column]
  board[current_row][current_column] = board[new_row][new_column]
  board[new_row][new_column] = temp
  return

#Recebe o estado atual e a acao, e retorna o próximo estado
def NovoEstado(action, current_state):
    board = copy.deepcopy(current_state.board)
    row = current_state.row
    column = current_state.column
    if action == 'left':
        if column > 0:
            new_column = column - 1
            swap(board, row, column, row, new_column)
            column = new_column
        else:
            print("Borda da esquerda!")
    elif action == 'right':
        if column < 2:
            new_column = column + 1
            swap(board, row, column, row, new_column)
            column = new_column
        else:
            print("Borda da direita!")
    elif action == 'up':
        if row > 0:
            new_row = row - 1
            swap(board, row, column, new_row, column)
            row = new_row
        else:
            print("Borda de cima!")
    elif action == 'down':
        if row < 2:
            new_row = row + 1
            swap(board, row, column, new_row, column)
            row = new_row
        else:
            print("Borda de baixo!")
    else:
        print('inválido')
    return state(board, [row, column], action)

#Funcoes A*:----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Distancia de Manhattan:
def heuristica(board):
    dist_m = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0:
                row = (board[i][j] - 1) // 3              #linha correta do numero
                column = (board[i][j] - 1) % 3            #coluna correta do numero
                dist_m += abs(row - i) + abs(column - j)  #distancia (em modulo) do numero atualmente e sua posicao correta incrementa dist_m
    return dist_m #dist manhattam = soma distancias de todos os numeros ate seu lugar correto

def adiciona_estrela(visitados, atual):
  queue = []
  if(atual.column < 2 and not visitado(NovoEstado('right', atual), visitados)):
    queue.append('right')
  if(atual.row < 2 and not visitado(NovoEstado('down', atual), visitados)):
    queue.append('down')
  if(atual.column > 0 and not visitado(NovoEstado('left', atual), visitados)):
    queue.append('left')
  if(atual.row > 0 and not visitado(NovoEstado('up', atual), visitados)):
    queue.append('up')
  return queue

#A*:
def A_estrela(initial_state):
  filaDePrioridade = PriorityQueue()
  visitados = []
  caminho = []
  teste = initial_state

  final_state =  state([[1, 2, 3], [4, 5, 6], [7, 8, 0]], [2, 2], 'inicio') 

  initial_state.profundidade = 0
  filaDePrioridade.put(((heuristica(initial_state.board)), initial_state))


  while filaDePrioridade:
      item = filaDePrioridade.get()
      current_state = item[1]
      teste = current_state
      if current_state.board == final_state.board:
          print('chegou no final:')
          while teste:
            print(teste.board)
            caminho.append([teste.board, teste.step])
            teste = teste.parent 
          return caminho
      visitados.append(current_state)
      
      queue = adiciona_estrela(visitados, current_state)
      for acao in queue:
          new_state = NovoEstado(acao, current_state)
          if new_state not in visitados:
              new_state.parent = current_state
              new_state.profundidade = current_state.profundidade + 1
              #teste = new_state
              custo = heuristica(new_state.board) + new_state.profundidade
              filaDePrioridade.put((custo, new_state))
              


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#main: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
inicial = state([[1, 2, 3], [4, 5, 6], [7, 8, 0]], [2, 2], 'inicio')  # Tabuleiro inicial geral (template)
test2 = state([[0,2,3],[1,4,6],[7,5,8]], [0,0], 'inicio')    # Configuração Inicial à ser testada
test1 = state([[1, 2, 3],[4, 8, 0],[7, 6, 5]], [1, 2], 'inicio')    # Configuração Inicial à ser testada
solucao = []
passos = []

#solucao = solve(test) #Solucao BFS
solucao = A_estrela(test2)

#Print Caminho
for it in reversed(solucao):
   print()
   print(it[1], ':')
   printm(it[0])
   passos.append(it[1])

passos.pop(0)
print('\ntodos os passos: ', passos)
