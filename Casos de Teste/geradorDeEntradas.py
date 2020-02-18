#!usr/bin/env/python3
# -*- coding: utf-8 -*-
from random import randint
import argparse, sys

parser = argparse.ArgumentParser(description='Gerador de casos')
parser.add_argument('nome_entrada', type=str, help='Nome dos arquivos de teste')
parser.add_argument('casos',type=int, help='Número de casos de teste')
parser.add_argument('linhas',type=int, help='Número de linhas')
parser.add_argument('simulacao', type=str, help='Qual o tipo de simulacao (p = pipeline,  a = arvore, g = grafo)')

args = parser.parse_args()

if len(sys.argv) < 5:
    parser.print_help()
    sys.exit(1)

num = 1
node = 0
for i in range(args.casos):
    with open (args.nome_entrada+str(num)+'.txt', 'w')  as f:
        #Gera os arquivos de Pipeline
        if (args.simulacao == 'p'):
            for j in range(args.linhas * (i+1)):
                f.write("{} {} 0 {} 0 {}\n".format(node, node+1, randint((i+1)*5,(i+1)*30),randint((i+1)*5,(i+1)*30)))
                node += 1
        #Gera os arquivos de Arvore
        elif (args.simulacao == 'a'):
            control = [] #armazena as conexoes para evitar repeticao
            for j in range(args.linhas * (i+1)):
                f.write("{} {} 0 {} 0 {}\n".format(j, (2*j)+1, randint((i+1)*5,(i+1)*30),randint((i+1)*5,(i+1)*30)))
                f.write("{} {} 0 {} 0 {}\n".format(j, (2*j)+2, randint((i+1)*5,(i+1)*30),randint((i+1)*5,(i+1)*30)))
                node += 1
        #Gera os arquivos de Grafo
        elif (args.simulacao == 'g'):
            control = [] #armazena as conexoes para evitar repeticao
            for j in range(args.linhas * (i+1)): #Para cada um dos elementos
                for k in range(randint(1, 3)): #Sorteia o numero de ligacoes que ele tem
                    while True:
                        valA = randint(1,args.linhas)
                        if (j != valA) and ((j,valA) not in control):
                        	control.append(((j,valA)))
                        	break
                        
                    f.write("{} {} 0 {} 0 {}\n".format(j, valA, randint((i+1)*5,(i+1)*30),randint((i+1)*5,(i+1)*30)))
                    node += 1
        num += 1
        node = 0
