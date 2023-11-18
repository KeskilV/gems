import numpy as np
import pandas as pd
import re
import os
import importlib
from module_prgem.dictemsapruby import dcla_em_sto, dcol_em_sto, dcla_sap, dcol_sap

#Globals
#загрузка таблицы определения размерностей для сапфиров и рубинов
df_sizes_sap_ruby = pd.read_excel('module_prgem/sizes_ruby_sap_sto.xlsx') 
#загрузка прейскуранта для сапфиров и рубинов
pr_em_sto = pd.read_excel('module_prgem/df_pr_sap_ruby_ 64_65_13-02-2020.xlsx',
                          dtype={'цвет':'str', 'чистота':'str'})
#последний рабочий pattern_sap3_
pattern_sap =  r"""(?ix)(?P<N>\d{,3})# штуки 
               (?P<Gem>сапфир[A-яA-z.]{1,5})[-]+  #gem
               (?P<Carat>\d\d?[.,]?\d*)[\s-]+                                 # карат
               (?P<Form>[A-яA-z.\d-]{1,10})[+]+  #[+\s-]+ 
               (?P<ColQ>[A-яA-z]*\d*[A-яA-z]*[ /]+(?:[A-яA-z]*\d*[A-яA-z]*\d*)[*]*[A-яA-z]*)"""

# чисто для сапфирП и Н
pattern_jsap = r"""(?ix)(?P<Gem>сапфир[пПнНhH][^вВbB])+#gem"""

def vst2listsap(t):
    '''функцая распозавания сапфиров вывод если нет то nan'''
    res = re.findall(pattern_sap, t )
    return res if len(res)!=0 else np.nan 

def vst2listsap_notna(t):
    '''функцая распозавания сапфиров вывод если нет то []'''
    res = re.findall(pattern_sap, t )
    return res #not na -> if len(res)!=0 else np.nan 

def error_by_lens_patts(t):
    '''функцая обнаружения ошибок при re распозаваниb сапфиров'''

    len_p = len(re.findall(pattern_sap, t ))
    len_j = len(re.findall(pattern_jsap, t ))
    return f"error{len_p}!={len_j}" if len_p!=len_j else f"ok{len_p}!={len_j}"

def size_sap_ruby(carat_1):
    '''функция для определения размерной группы сапфира и рубина в зависимоти кабашон или фацет огранка
   , carat_1'''   
    return df_sizes_sap_ruby[(df_sizes_sap_ruby.low_grade<=carat_1)].sort_values('low_grade').iloc[-1,0]


def check_vstlistsapryby(l):
    '''функция для проверки соответствия словарям'''                           
    #проверка на пусто или []
    if l is np.nan or len(l)==0:
        return np.nan
    #создать внутренний dfx
    dfx = pd.DataFrame({'vstlist':l})
    
    
    cols = ["PCS","GEM","CARAT", "FORM", "CQ"]
    for c in range(len(cols)):
        dfx[cols[c]] = dfx.vstlist.apply(lambda x: x[c].lower().strip())
    dfx['C'] = dfx['CQ'].apply(lambda x: x.split('/')[0].lower().strip())
    dfx['Q'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[0].strip())
    dfx['C_add'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[-1].strip()\
                                  if x.__contains__('*') else np.nan)
    
    
  
    #пустить проверки по словарям  dcla_sap, dcol_sap
    report = ''
    report += 'C:ok;' if dfx['C'].apply(lambda x: x in dcol_sap).all() \
                      else f"C:error;"
    report+='Q:ok;' if dfx['Q'].apply(lambda x: x in dcla_sap).all()\
                      else 'Q:error;'
    report+='PCS:ok;' if dfx['PCS'].apply(lambda x: x!='').all()\
                      else 'PCS:error;'
    #если есть хоть одна ошибка не считать! 
    return report
'''    
    try:
        if report.__contains__('error'):
            raise ValueError("имеется ошибка")
        dfx['PCS'] = dfx['PCS'].astype('int')
        dfx['CARAT'] = dfx['CARAT'].str.replace(',','.').astype('float')
        dfx['PCS'] = dfx['PCS'].astype('int')
        dfx['C'] = dfx['C'].map(dcol_em_sto)
        dfx['Q'] = dfx['Q'].map(dcla_em_sto)
        dfx['CARAT_1'] = dfx['CARAT']/dfx['PCS']
        dfx['size'] = dfx.apply(lambda x:size_em_sto(x['Q'],x['CARAT_1']),axis=1)
        dfx = pd.merge(left=dfx, right=pr_em_sto,
            how='left', 
            left_on=['size', 'C', 'Q',],
            right_on=['size','цвет', 'чистота'])
        dfx['prcost'] = dfx['CARAT']*dfx['price']

    except:
        return '0;0;except; '+report

    return f"{dfx['prcost'].sum():,.2f};{dfx['CARAT'].sum():,.3f};Ok; \
 size:{((dfx['size']+'+').sum()).strip('+')}; price:{((dfx['price'].astype('str')+'+').sum()).strip('+')}; "+report
    #return dfx['CARAT'].sum(),dfx['prcost'].sum(),(dfx['price'].astype('str')+'-').sum(),list(dfx['size']),report
'''