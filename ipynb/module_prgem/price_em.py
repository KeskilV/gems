import numpy as np
import pandas as pd
import re
import os
import importlib
from module_prgem.dictemsapruby import dcla_em_sto, dcol_em_sto, dcla_sap, dcol_sap

#Globals
#загрузка таблицы определения размерностей для изумрудов сто кабашон и фацет
sizes_g = pd.read_excel('module_prgem/size_em_sto.xlsx') 
#загрузка прейскуранта для изумрудов сто кабашон и фацет
pr_em_sto = pd.read_excel('module_prgem/df_pr_emeralds_sto_173_20-04-2023.xlsx', dtype={'цвет':'str'})


def vst2list(t):
    '''функцая распозавания изумрудов'''
    pattern_em =  r"""(?ix)(?P<N>\d{,3})# штуки 
               (?P<Gem>изумру[A-яA-z.]{1,5})[-]+#gem
               (?P<Carat>\d\d?[.,]?\d*)[\s-]+                                 # карат
               (?P<Form>[A-яA-z.\d-]{1,10})[+]+#[+\s-]+ 
               (?P<ColQ>\d+[ /]+(?:\d*[ГгКкKk]*\d*))"""
    res = re.findall(pattern_em, t )
    return res if len(res)!=0 else np.nan 


def size_em_sto(q,carat_1):
    '''функция для определения размерной группы изумруда по сто в зависимоти кабашон или фацет огранка
   q - качество, carat_1'''   
    if q not in dcla_em_sto.values():
        return 'error_size_em_sto: q not in dcla_em_sto'
    
    if q.__contains__('Г'):
        sizex = sizes_g[sizes_g['Огранка']=='фацетный вид огранки']
    else:
        sizex = sizes_g[sizes_g['Огранка']=='кобашенный вид огранки']
            
    return sizex[(sizex.low_grade<=carat_1)].sort_values('low_grade').iloc[-1,0]
                        
def check_vstlist(l):
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
    dfx['Q'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip())
    
    
    #пустить проверки по словарям
    report = ''
    report += 'C:ok;' if dfx['C'].apply(lambda x: x in dcol_em_sto).all() \
                      else f"C:error;"
    report+='Q:ok;' if dfx['Q'].apply(lambda x: x in dcla_em_sto).all()\
                      else 'Q:error;'
    report+='PCS:ok;' if dfx['PCS'].apply(lambda x: x!='').all()\
                      else 'PCS:error;'
    #если есть хоть одна ошибка не считать! 
    
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