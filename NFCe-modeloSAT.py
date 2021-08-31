from re import split
import pandas as pd
from tika import parser
import time

print('Reading PDF file')
pdf_path = '/dev/python/scraping/pdf/notasfiscais/'
pdf_file = 'nfce-modsat-n409723.pdf'
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
  df_list = [i for i in df_list if i !=['b']] 
  df_list = [i for i in df_list if i !=['"']] 
  df_list = [i for i in df_list if i !=[' ']] 
  df_list = [i for i in df_list if i !=['NaN']] 
  df_list = [i for i in df_list if i !=['-----------------']] 
  df_list = [i for i in df_list if i !=['X']] 
  df_list = [i for i in df_list if any("0000" in s for s in i)] 


#DATAFRAME
df_produtos = pd.DataFrame(df_list,columns=['primeira'])
df_produtos['primeira'].str.split(" ", n=1, expand=True) 

df_produtos.head(2)
df_produtos['test']=df_produtos['primeira'].str.split(" ", n=1, expand=True)[1]
df_produtos.drop(['primeira'],axis=1,inplace=True)

df_produtos['codigo']=df_produtos['test'].str.split(" ", n=1, expand=True)[0]
df_produtos['produto']=df_produtos['test'].str.split(" ", n=1, expand=True)[1].str.split(",0000", n=1, expand=True)[0].str[:-1]
df_produtos['vl_total']=df_produtos['test'].str.split("(", n=1, expand=True)[1].str.split(" ", n=1, expand=True)[1]
df_produtos['tributo']=df_produtos['test'].str.split("(", n=1, expand=True)[1].str.split(")", n=1, expand=True)[1]
df_produtos['unidade']=df_produtos['test'].str.split(",0000", n=1, expand=True)[1].str.split(" ", n=1, expand=True)[1].str.split("(", n=1, expand=True)[0].str.split(" ", n=1, expand=True)[0]
df_produtos['vl_unit']=df_produtos['test'].str.split(",0000", n=1, expand=True)[1].str.split(" ", n=1, expand=True)[1].str.split("(", n=1, expand=True)[0].str.split(" ", n=1, expand=True)[1]
df_produtos.drop(['test'],axis=1,inplace=True)


