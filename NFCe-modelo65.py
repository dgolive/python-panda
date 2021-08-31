from re import split
import pandas as pd
from tika import parser
import time

print('Reading PDF file')

pdf_path = '/dev/python/scraping/pdf/notasfiscais/'
pdf_file = 'nfce-mod65-n742020.pdf'
pdf_data = parser.from_file(pdf_path + pdf_file)
content = (pdf_data['content'])

output = content.encode('utf-8',errors='ignore')

with open(pdf_file + '.txt', 'w') as the_file:
    the_file.write(str(output))

time.sleep(2)

filename=('/dev/python/scraping/' + pdf_file + '.txt') 
with open(filename) as f:
    df_list = [list(map(str, row.split('DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR'))) for row in f.read().split(r'\n')]
df_list = [i for i in df_list if i !=['']]
df_list = [i for i in df_list if i !=['b"']]
df_list = [i for i in df_list if i !=['"']]
df_list = [i for i in df_list if i !=[' ']]
df_list = [i for i in df_list if i !=['NaN']]


#DATAFRAME
df = pd.DataFrame(columns = ['mercado'])
df 
#criando a lista de produtos 
produto_list=[]
valor_compra_list=[]
qtde_list=[]
vl_total_line = [i for i, x in enumerate(df_list) if x == ['Vl. Total ']] #identificando aonde esta o Vl Total 
#loop para criar as listas de produtos, valores e codigo
for i in vl_total_line:
  produto_i=i-2
  valor_compra_i=i+1
  qtde_i=i-1
  produto_list.append(df_list[produto_i][0])
  valor_compra_list.append(df_list[valor_compra_i][0])
  qtde_list.append(df_list[qtde_i][0])
#addicionando as colunas de produto, valor e codigo
df['produto'] = produto_list
df['valor_compra'] = valor_compra_list
df['qtde'] = qtde_list
#flat list 
df_list_flat = [item for sublist in df_list for item in sublist] #flat a lista
matches = [match for match in df_list_flat if "CNPJ" in match] #procurar a palavra cnpj
df['mercado'] = matches[0].split(": ")[1]
#outras informacoes (valor,qtde compra,produto e produto codigo)
df['qtde_compra']=df["qtde"].str.split("UN", n=4,expand=True)[0].str.split('.:',expand=True)[1] 
df['valor_unitario']=df["qtde"].str.split(r" \\xc2\\xa0", n=2,expand=True)[1]
df['produto_codigo']=df["produto"].str.split("digo: ",n=5,expand=True)[1].str.split(')',n=2,expand=True)[0]
df["produto_nome"]=df["produto"].str.split("\(C",n=3,expand=True)[0]
df.drop(['produto','qtde'],axis=1)
df = df[['mercado', 'produto_nome', 'produto_codigo', 'qtde_compra', 'valor_unitario','valor_compra']]

print(df)