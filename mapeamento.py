#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys, argparse, operator
from os import system

parser = argparse.ArgumentParser(description='Simulação de MPSoc')

parser.add_argument('entrada', type=str, help='Nome do arquivo de entrada')
parser.add_argument('dimensao',type=int, help='Dimensão da matriz (nxn)')
args = parser.parse_args()

class MPSoc:
	def __init__(self, arquivo, linhas, colunas):
		self.entrada = self.leEntrada(arquivo)				#Armazena a entrada
		self.grafo = defaultdict(list)		#Grafo de entrada
		self.MPSoc = list()					# Lista que guarda a ocupação das posições do MPSoc
		self.execMPSoc = defaultdict(list)	#MPSoc em execucao
		self.linhas = linhas				#Linhas do MPSoc
		self.colunas = colunas				#Colunas do MPSoc

	def exibeMPSoc(self):
		print("GRAFO POR PARTES")
		for i in self.grafo:
			print(i, self.grafo[i])

		print("\nCANAIS DE COMUNICACAO - MPSoc")
		for i in self.execMPSoc:
			print(i,self.execMPSoc[i])

	def exibeEntrada(self):
		"""IMPRIME A ENTRADA"""
		print("ENTRADA DE TXT:")
		for i in range(len(self.entrada)):
			print(entrada[i])

	"""PERCORRE OS VALORES DE ENTRADA E ARMAZENA NO GRAFO"""
	def inicializaGrafo(self):
		for i in range(len(self.entrada)): #Percorre as linhas da entrada
			for j in range(2):
				if(self.entrada[i][j] not in self.grafo): #Se o no ainda nao estiver no grafo, adiciona ele
					for k in range(2): #Inicializa a posicao X e Y como -1
						x = -1
						self.grafo[self.entrada[i][j]].append(x)
		for i in range(len(self.entrada)):
			self.grafo[self.entrada[i][0]].append(self.entrada[i][1:6])

		# print("GRAFO TOTAL INICIALIZADO:")
		# print(self.grafo)

	def leEntrada(self, arquivo):
		"""LE O ARQUIVO DE ENTRADA"""
		with open(arquivo, 'r') as arq: #Abre e ja fecha o arquivo
			entrada = arq.readlines() 	#Le todas linhas do arquivo
			for i in range(len(entrada)):
				entrada[i] = list(map(int,entrada[i].rstrip("\n").split())) # Remove \n, quebra strings e converte pra inteiro
		return entrada

	def atualizaCaminho(self, i_inicial, j_inicial, ii, jj, canalIda, canalVolta):
		''' Atualiza os pesos de ida e volta de uma posição do MPSoc para a outra '''
		j = j_inicial
		i = i_inicial
		N = self.linhas

		if(j != jj): #Percorre em x
			while(j != jj):
				if(j < jj):
					if((i*N+j,i*N+j+1) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,i*N+j+1)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,i*N+j+1)][0] += canalIda
					j += 1

				elif(j > jj):
					if((i*N+j,i*N+j-1) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,i*N+j-1)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,i*N+j-1)][0] += canalIda
					j -= 1

		if(i != ii): #Percorre em y
			while(i != ii):
				if(i < ii):
					if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,(i+1)*N+j)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,(i+1)*N+j)][0] += canalIda
					i += 1

				elif(i > ii):
					if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,(i-1)*N+j)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,(i-1)*N+j)][0] += canalIda
					i -= 1

		if(j != j_inicial): #Percorre em x
			while(j != j_inicial):
				if(j < j_inicial):
					if((i*N+j,i*N+j+1) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,i*N+j+1)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,i*N+j+1)][0] += canalVolta
					j += 1

				elif(j > j_inicial):
					if((i*N+j,i*N+j-1) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,i*N+j-1)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,i*N+j-1)][0] += canalVolta
					j -= 1

		if(i != i_inicial): #Percorre em y
			while(i != i_inicial):
				if(i < i_inicial):
					if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,(i+1)*N+j)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,(i+1)*N+j)][0] += canalVolta
					i += 1

				elif(i > i_inicial):
					if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
						self.execMPSoc[(i*N+j,(i-1)*N+j)].append(0) #Cria a conexao ida
					self.execMPSoc[(i*N+j,(i-1)*N+j)][0] += canalVolta
					i -= 1

	def pathLoad(self):
		flag = 0
		# Coloca a primeira tarefa na posição (0,0)
		self.grafo[0][0] = 0	#Inicializa a pos em 0
		self.grafo[0][1] = 0	#Inicializa a pos em 0
		self.MPSoc.append(0)	#Diz que a pos 0 ta ocupada
		for no in self.grafo: # Para os vértices do grafo
			for lig in range(2, len(self.grafo[no])): #Para cada conexão do nó
				i_inicial = self.grafo[no][0]				#valor da posicao i do nó atual
				j_inicial = self.grafo[no][1]				#valor da posicao j do nó atual
				canalIda = self.grafo[no][lig][2]			#valor de ocupacao do canal de ida até o destino
				canalVolta = self.grafo[no][lig][4]			#valor de ocupacao do canal de volta do destino
				N = self.linhas
				# print(canalIda)

				cargas = {}

				for ii in range(self.linhas): # Percorre as linhas do MPSoc
					for jj in range(self.colunas): # Percorre as colunas do MPSoc
						i = i_inicial
						j = j_inicial

						if i != ii or j != jj: # Se a posição que estamos olhando é diferente da posição do nó atual
							# Agora testamos essa posição para saber seu custo
							custo = 0
							''' TESTA OS CANAIS DE IDA '''

							if(j != jj): #Percorre em x
								while(j != jj): # Enquanto não estiver na linha desejada
									if(j < jj): # Se coord_x atual for menor que a desejada
										if((i*N+j,i*N+j+1) not in self.execMPSoc): # Se esse canal ainda não tiver peso
											custo += canalIda # Adiciona o peso da ida
										else: # Se esse canal já tiver peso
											custo += canalIda + self.execMPSoc[(i*N+j,i*N+j+1)][0]
										j += 1

									elif(j > jj): # Se coord_x atual for menor que desejada
										if((i*N+j,i*N+j-1) not in self.execMPSoc): # Se esse canal ainda não tiver peso
											custo += canalIda
										else: # Se esse canal já tiver peso
											custo += canalIda + self.execMPSoc[(i*N+j,i*N+j-1)][0]
										j -= 1

							if(i != ii): #Percorre em y
								while(i != ii): # Enquanto não estiver na coluna desejada
									if(i < ii): # Se coord_y atual for menor que a desejada
										if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
											custo += canalIda
										else:
											custo += canalIda + self.execMPSoc[(i*N+j,(i+1)*N+j)][0]
										i += 1

									elif(i > ii): # Se coord_y atual for maior que a desejada
										if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
											custo += canalIda
										else:
											custo += canalIda + self.execMPSoc[(i*N+j,(i-1)*N+j)][0]
										i -= 1

							''' TESTA OS CANAIS DE VOLTA '''
							if(j != j_inicial): #Percorre em x
								while(j != j_inicial): # Enquanto não estiver na linha desejada
									if(j < j_inicial): # Se coord_x atual for menor que a desejada
										if((i*N+j,i*N+j+1) not in self.execMPSoc): # Se esse canal ainda não tiver peso
											custo += canalVolta # Adiciona o peso da ida
										else: # Se esse canal já tiver peso
											custo += canalVolta + self.execMPSoc[(i*N+j,i*N+j+1)][0]
										j += 1

									elif(j > j_inicial): # Se coord_x atual for menor que desejada
										if((i*N+j,i*N+j-1) not in self.execMPSoc): # Se esse canal ainda não tiver peso
											custo += canalVolta
										else: # Se esse canal já tiver peso
											custo += canalVolta + self.execMPSoc[(i*N+j,i*N+j-1)][0]
										j -= 1

							if(i != i_inicial): #Percorre em y
								while(i != i_inicial): # Enquanto não estiver na coluna desejada
									if(i < i_inicial): # Se coord_y atual for menor que a desejada
										if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
											custo += canalVolta
										else:
											custo += canalVolta + self.execMPSoc[(i*N+j,(i+1)*N+j)][0]
										i += 1

									elif(i > i_inicial): # Se coord_y atual for maior que a desejada
										if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
											custo += canalVolta
										else:
											custo += canalVolta + self.execMPSoc[(i*N+j,(i-1)*N+j)][0]
										i -= 1

							cargas[(i_inicial*N+j_inicial, ii*N+jj)] = custo

				custos = sorted(cargas.items(), key=operator.itemgetter(1)) # Ordena os custos das possíveis posições

				for c in range(len(custos)):
					if custos[c][0][1] not in self.MPSoc:
						#print(no, self.grafo[no][lig][0])
						novo_j , novo_i =  self.retornaPos(custos[c][0][1])
						self.grafo[self.grafo[no][lig][0]][0] = novo_i
						self.grafo[self.grafo[no][lig][0]][1] = novo_j
						self.MPSoc.append(custos[c][0][1])
						break

				#self.inicializaPesos()
				self.atualizaCaminho(i_inicial, j_inicial, novo_i, novo_j, canalIda, canalVolta)

		#print (self.MPSoc)
		#print (self.grafo)

	def retornaPos(self, pos):
		# sei onde estou(pos), quero saber a posição (x,y) descrita pelo valor passado pra função
		j = pos % self.linhas
		i = int((pos - j) / self.linhas)
		return j,i

	def inicializaPesos(self):
		for no in self.grafo: #Percorre os nos do MPSoc
			for lig in range(2, len(self.grafo[no])): #Para cada no, percorre suas conexoes
				i = self.grafo[no][0]						#valor da posicao i
				j = self.grafo[no][1]						#valor da posicao j
				ii = self.grafo[self.grafo[no][lig][0]][0]	#valor da posicao i do outro no
				jj = self.grafo[self.grafo[no][lig][0]][1]	#valor da posicao j do outro no
				N = self.linhas								#valor de N
				canalIda = self.grafo[no][lig][2]			#valor de ocupacao do canal de ida
				canalVolta = self.grafo[no][lig][4]			#valor de ocupacao do canal de volta

				if(j != jj): #Percorre em x
					while(j != jj):
						if(j < jj):
							if((i*N+j,i*N+j+1) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,i*N+j+1)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,i*N+j+1)][0] += canalIda
							j += 1

						elif(j > jj):
							if((i*N+j,i*N+j-1) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,i*N+j-1)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,i*N+j-1)][0] += canalIda
							j -= 1

				if(i != ii): #Percorre em y
					while(i != ii):
						if(i < ii):
							if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,(i+1)*N+j)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,(i+1)*N+j)][0] += canalIda
							i += 1

						elif(i > ii):
							if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,(i-1)*N+j)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,(i-1)*N+j)][0] += canalIda
							i -= 1

		for no in self.grafo: #Percorre os nos do MPSoc
			for lig in range(2, len(self.grafo[no])): #Para cada no, percorre suas conexoes
				ii = self.grafo[no][0]						#valor da posicao i
				jj = self.grafo[no][1]						#valor da posicao j
				i = self.grafo[self.grafo[no][lig][0]][0]	#valor da posicao i do outro no
				j = self.grafo[self.grafo[no][lig][0]][1]	#valor da posicao j do outro no
				N = self.linhas								#valor de N
				canalIda = self.grafo[no][lig][2]			#valor de ocupacao do canal de ida
				canalVolta = self.grafo[no][lig][4]			#valor de ocupacao do canal de volta

				if(j != jj): #Percorre em x
					while(j != jj):
						if(j < jj):
							if((i*N+j,i*N+j+1) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,i*N+j+1)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,i*N+j+1)][0] += canalVolta
							j += 1

						elif(j > jj):
							if((i*N+j,i*N+j-1) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,i*N+j-1)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,i*N+j-1)][0] += canalVolta
							j -= 1

				if(i != ii): #Percorre em y
					while(i != ii):
						if(i < ii):
							if((i*N+j,(i+1)*N+j) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,(i+1)*N+j)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,(i+1)*N+j)][0] += canalVolta
							i += 1

						elif(i > ii):
							if((i*N+j,(i-1)*N+j) not in self.execMPSoc):
								self.execMPSoc[(i*N+j,(i-1)*N+j)].append(0) #Cria a conexao ida
							self.execMPSoc[(i*N+j,(i-1)*N+j)][0] += canalVolta
							i -= 1

	def firstFree(self):
		''' Essa função mapeia no grafo as posições das tarefas de acordo com a heurística
		first free '''
		flag = 0
		for i in range(self.linhas): #Percorre as linhas do MPSoc
			for j in range(self.colunas): #Percorre as colunas do MPSoc
				if (i*self.linhas+j) < len(self.grafo): #Se a iteracao atual for menor que o tamanho do grafo, mapeia no MPSoc
					self.grafo[i*self.linhas+j][0] = i
					self.grafo[i*self.linhas+j][1] = j
				else: #Senao sai do laco j e autoriza a saida do laco i
					flag = 1
					break
			if flag == 1: #Sai do laco i pois ta autorizado
				break

	def interfaceGrafica(self, nome):
		nomeArquivo = nome + ".dot"
		arq = open(nomeArquivo, 'w')
		arq.write('digraph {\n') #ESCREVE O CABECALHO DO ARQUIVO .DOT

		arq.write('\tbgcolor=darkolivegreen1;\n')
		arq.write('\tnodesep = 0.5; //distribuicao uniforme dos nos\n')
		arq.write('\tnode [ shape = square, width = 0.7, style=filled, fillcolor=darkgreen, fontcolor=white];\n\n')

		for lin in range(self.linhas):
			arq.write('\t{ rank = same; ')
			for col in range(self.colunas):
				if col == (self.colunas - 1): #Se for o ultimo valor da linha, nao coloca o ';'
					arq.write(str(lin*self.linhas+col))
				else:
					arq.write(str(lin*self.linhas+col) + '; ')
			arq.write(' }\n')
		arq.write('\n')


		for lin in range(self.linhas-1): #Liga os nos de CIMA para BAIXO
			for col in range(self.colunas):
				part = lin*self.linhas+col
				dest = (lin+1)*self.linhas+col
				if (part,dest) in self.execMPSoc:
					peso = self.execMPSoc[(part,dest)]
					if peso[0] > 0 and peso[0] < 33:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"darkgreen\"];\n')
					elif peso[0] >= 33 and peso[0] < 66:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"gold\"];\n')
					elif peso[0] >= 66 and peso[0] < 99:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"orange\"];\n')
					else:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"red\"];\n')
				else:
					arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [weight=\"100\",color=\"darkolivegreen3\"];\n')

		for lin in range(self.linhas-1): #Liga os nos de BAIXO para CIMA
			for col in range(self.colunas):
				part = (lin+1)*self.linhas+col
				dest = lin*self.linhas+col
				if (part,dest) in self.execMPSoc:
					peso = self.execMPSoc[(part,dest)]
					if peso[0] > 0 and peso[0] < 33:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"darkgreen\"];\n')
					elif peso[0] >= 33 and peso[0] < 66:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"gold\"];\n')
					elif peso[0] >= 66 and peso[0] < 99:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"orange\"];\n')
					else:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"red\"];\n')
				else:
					arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [weight=\"100\",color=\"darkolivegreen3\"];\n')

		for col in range(self.colunas-1): #Liga os nos da ESQUERDA para DIREITA
			for lin in range(self.linhas):
				part = lin*self.linhas+col
				dest = lin*self.linhas+(col+1)
				if (part,dest) in self.execMPSoc:
					peso = self.execMPSoc[(part,dest)]
					if peso[0] > 0 and peso[0] < 33:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"darkgreen\"];\n')
					elif peso[0] >= 33 and peso[0] < 66:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"gold\"];\n')
					elif peso[0] >= 66 and peso[0] < 99:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"orange\"];\n')
					else:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"red\"];\n')
				else:
					arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [weight=\"100\",color=\"darkolivegreen3\"];\n')

		for col in range(self.colunas-1): #Liga os nos da DIREITA para ESQUERDA
			for lin in range(self.linhas):
				part = lin*self.linhas+(col+1)
				dest = lin*self.linhas+col
				if (part,dest) in self.execMPSoc:
					peso = self.execMPSoc[(part,dest)]
					if peso[0] > 0 and peso[0] < 33:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"darkgreen\"];\n')
					elif peso[0] >= 33 and peso[0] < 66:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"gold\"];\n')
					elif peso[0] >= 66 and peso[0] < 99:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"orange\"];\n')
					else:
						arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [label=\"' + str(peso) + '\",weight=\"100\",color=\"red\"];\n')
				else:
					arq.write('\t' + str(part) + ' -> ' + str(dest) + ' [weight=\"100\",color=\"darkolivegreen3\"];\n')

		arq.write('\n}') #FINALIZA O CABECALHO DO ARQUIVO .DOT
		arq.close()
		nomeImagem = nome + ".png"
		system("dot -Tpng " + nomeArquivo + " -o " + nomeImagem)
		system("rm " + nomeArquivo)

	def grafico(self, nome):
		nomeArquivo = nome + ".dat"
		arq = open(nomeArquivo, 'w')

		acum = 0
		for i in self.execMPSoc:
			acum += self.execMPSoc[i][0]
		media = acum/(self.linhas*self.colunas)
		#print("MEDIA = " + str(acum) + "/" + str(self.linhas) + " " + str(self.colunas) + " = " + str(media))

		cont = 1
		for i in self.execMPSoc:
			arq.write(str(cont) + ' ' + str(self.execMPSoc[i]).strip('[').strip(']') + ' ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(media) + '\n')
			cont += 1
		arq.close()

		system("gnuplot " + str(nome) + ".gnu")
		system("rm " + nomeArquivo)

	def estruturaEntrada(self, nome):
		nomeArquivo = nome + "Grafo.dot"
		arq = open(nomeArquivo, 'w')
		arq.write('digraph {\n') #ESCREVE O CABECALHO DO ARQUIVO .DOT

		for part in self.grafo: #Percorre os nos do MPSoc
			for lig in range(2, len(self.grafo[part])):	#Para cada no, percorre suas conexoes
				dest = self.grafo[part][lig][0]
				arq.write('\t' + str(part) + ' -> ' + str(dest) + ';\n')

		arq.write('\n}') #FINALIZA O CABECALHO DO ARQUIVO .DOT
		arq.close()
		nomeImagem = nome + "Grafo.png"
		system("dot -Tpng " + nomeArquivo + " -o " + nomeImagem)
		system("rm " + nomeArquivo)

"""FUNCAO PRINCIPAL"""
def main():
	GREEN, RED, WHITE, BLUE =  '\033[1;32m', '\033[91m', '\033[0m', '\033[94m'

	"""CRIA O OBJETO E INICIALIZA A EXECUCAO"""
	objMPSoc = MPSoc(args.entrada, args.dimensao, args.dimensao) #Cria o objeto, passando a entrada, as linhas e as colunas
	objMPSoc.inicializaGrafo()		#Percorre a entrada e inicializa o grafo

	print ("""{}
      ___           ___           ___           ___           ___
     /\__\         /\  \         /\  \         /\  \         /\  \
    /::|  |       /::\  \       /::\  \       /::\  \       /::\  \
   /:|:|  |      /:/\:\  \     /:/\ \  \     /:/\:\  \     /:/\:\  \
  /:/|:|__|__   /::\~\:\  \   _\:\~\ \  \   /:/  \:\  \   /:/  \:\  \
 /:/ |::::\__\ /:/\:\ \:\__\ /\ \:\ \ \__\ /:/__/ \:\__\ /:/__/ \:\__\
 \/__/~~/:/  / \/__\:\/:/  / \:\ \:\ \/__/ \:\  \ /:/  / \:\  \  \/__/
       /:/  /       \::/  /   \:\ \:\__\    \:\  /:/  /   \:\  \
      /:/  /         \/__/     \:\/:/  /     \:\/:/  /     \:\  \
     /:/  /                     \::/  /       \::/  /       \:\__\
     \/__/                       \/__/         \/__/         \/__/

""".format('\033[1;32m'))

	print("Escolha o Mapeamento:")
	print("1 - First Free")
	print("2 - Path Load")
	escolha = int(input())

	if escolha == 1:
		system('clear')
		objMPSoc.firstFree()					#Mapeia os elementos no MPSoc
		objMPSoc.inicializaPesos()				#Atribui pesos nas conexões do MPSoc
		objMPSoc.interfaceGrafica("FirstFree")	#Cria o MPSoc
		objMPSoc.estruturaEntrada("FirstFree")	#Cria o Ligacoes da Estrutura
		objMPSoc.grafico("FirstFree")			#Cria o grafico com os resultados e a media
		print("\n\n\n\n\n")
		objMPSoc.exibeMPSoc()
	elif escolha == 2:
		system('clear')
		objMPSoc.pathLoad()
		objMPSoc.interfaceGrafica("PathLoad")	#Cria o MPSoc
		objMPSoc.estruturaEntrada("PathLoad")
		objMPSoc.grafico("PathLoad")
		print("\n\n\n\n\n")
		objMPSoc.exibeMPSoc()
	else:
		print("Opcao invalida!")

"""CHAMA A FUNCAO PRINCIPAL"""
if __name__ == '__main__':
	main()
