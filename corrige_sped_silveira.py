from os import system
from time import sleep
from tkinter import filedialog as fd
from tkinter import messagebox as msg

arquivo = fd.askopenfilename(defaultextension=".txt")
novo_sped = []
pular_linha = False
cont_registros = 0
cont_registros_c = 0

system('cls')
try:
    with open(arquivo, 'r', encoding='ASCII', errors='ignore') as sped:
        ler = sped.readlines()

    for linha in ler:
        is_c170 = False
        
        if linha.startswith("|C100|0|"):
            pular_linha = True
            continue
        
        if linha.startswith("|C100|1|"):
            pular_linha = False
            
        if linha.startswith("|C170|"):
            conteudo_linha = linha.split("|")
            if (conteudo_linha[25] == '01' or conteudo_linha[25] == '05') and (conteudo_linha[31] == '01' or conteudo_linha[31] == '05'):
                is_c170 = True
                conteudo_linha[27] = '0,65'
                conteudo_linha[33] = '3' 
                nova_linha = '|'.join(conteudo_linha)
                novo_sped.append(nova_linha)
                cont_registros_c = cont_registros_c+1
                cont_registros = cont_registros+1
        
        if linha.startswith("|C990|"):
            nova_linha = linha.replace(linha, f'|C990|{cont_registros_c+1}|\n')
            novo_sped.append(nova_linha)
            pular_linha = True
                        
        if linha.startswith("|D"):
            pular_linha = False
            
        if linha.startswith("|9999|"):
            nova_linha = linha.replace(linha, f'|9999|{cont_registros+2}|\n')
            novo_sped.append(nova_linha)
            pular_linha = True

        if not pular_linha and not is_c170:
            novo_sped.append(linha)  
            cont_registros = cont_registros+1
            if linha.startswith("|C"):
                cont_registros_c = cont_registros_c+1

    with open(arquivo, "w") as sped_novo:
        sped_novo.writelines(novo_sped)
        sped_novo.close()

except Exception as e:
    msg.showerror("erro", "Não foi possivel abrir o arquivo:\n{}".format(str(e)))
    