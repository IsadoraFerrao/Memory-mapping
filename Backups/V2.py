#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import sys, argparse

parser = argparse.ArgumentParser(description='Simulação de MPSoc')

parser.add_argument('entrada', type=str, help='Nome do arquivo de entrada')
parser.add_argument('dimensao',type=int, help='Dimensão da matriz (nxn)')
args = parser.parse_args()

class MPSoc:
	def __init__(self, arquivo, linhas, colunas):
		self.arquivo = arquivo			#Arquivo de entrada
		self.grafo = defaultdict(list)	#Grafo de entrada
		self.MPSoc = [[None for x in range(colunas)] for y in range(linhas)] #MPSoc em execucao
		self.linhas = linhas			#Linhas do MPSoc
		self.colunas = colunas			#Colunas do MPSoc
		self.canais = dict()			#Canais entre os EPs
		self.entrada = self.leEntrada() #Armazena a entrada lida do arquivo


	def debugEntrada(self):
		"""IMPRIME A ENTRADA"""
		print("ENTRADA DE TXT:")
		for i in range(len(self.entrada)):
			print(self.entrada[i])

	def debugMPSoc(self):
		for i in self.MPSoc:
			print(i)
		return

	"""PERCORRE OS VALORES DE ENTRADA E ARMAZENA NO GRAFO"""
	def inicializaGrafo(self):
		for i in range(len(self.entrada)): #Percorre as linhas da entrada
			for j in range(2):
				if(self.entrada[i][j] not in self.grafo): #Se o nº ainda nao estiver no grafo, adiciona ele
					for k in range(2): #Inicializa a posicao X e Y como -1
						self.grafo[self.entrada[i][j]].append(-1)

		for i in range(len(self.entrada)):
			self.grafo[self.entrada[i][0]].append(self.entrada[i][1:6])

		print("GRAFO POR PARTES")
		for i in self.grafo:
			print(i, self.grafo[i])


	# def firstFree(self):
	# 	print(len(self.grafo))
	# 	for chave in range(len(self.grafo)): # Para cada vértice do grafo
	# 		print (chave)
	# 		for linha in self.MPSoc: # Para cada linha do MPSoc
	# 			# print(chave, linha)
	# 			if chave in linha: # Se o vértice já está no MPSoc, OK
	# 				break
	# 		else: # (Sim, um else do for) Se o vértice ainda não está na matriz MPSoc
	# 			for linha in range(self.linhas): # Percorre a matriz e encontra o primeiro espaço vazio
	# 				for col in range(self.colunas):
	# 					if not self.MPSoc[linha][col]: # Se a posição do MPSoc está vazia
	# 						self.MPSoc[linha][col] = chave # Coloca o vértice no espaço vazio
	#

	def leEntrada(self):
		"""LE O ARQUIVO DE ENTRADA"""
		with open(self.arquivo, 'r') as arq: #Abre e ja fecha o arquivo
			entrada = arq.readlines() 	#Le todas linhas do arquivo
			for i in range(len(entrada)):
				entrada[i] = list(map(int,entrada[i].rstrip("\n").split())) # Remove \n, quebra strings e converte pra inteiro
			print(entrada)
		return entrada

			#if self.canais.get(chave) == None:

				# for tarefa in range(2,len(grafo[i])): # Para cada aresta do grafo
				# 	self.canais.get()

''' -----------------> FIM DA CLASSE MPSOC <----------------- '''


"""FUNCAO PRINCIPAL"""
def main():
	"""CRIA O OBJETO E INICIALIZA A EXECUCAO"""
	objMPSoc = MPSoc(args.entrada, args.dimensao, args.dimensao) #Cria o objeto, passando a entrada, as linhas e as colunas
	objMPSoc.inicializaGrafo()		#Percorre a entrada e inicializa o grafo
	# objMPSoc.debugEntrada()
	# objMPSoc.firstFree()
	# objMPSoc.debugMPSoc()

"""CHAMA A FUNCAO PRINCIPAL"""
if __name__ == '__main__':
	main()
