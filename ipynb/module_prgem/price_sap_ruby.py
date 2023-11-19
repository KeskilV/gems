import numpy as np
import pandas as pd
import re
import os
import importlib
#from module_prgem.dictgems import dcla_em_sto, dcol_em_sto, dcla_sap, dcol_sap, dgem
import module_prgem.dictgems as mds
#Globals
#загрузка таблицы определения размерностей для сапфиров и рубинов
df_sizes_sap_ruby = pd.read_excel('module_prgem/sizes_ruby_sap_sto.xlsx') 
#загрузка прейскуранта для сапфиров и рубинов
pr_em_sto = pd.read_excel('module_prgem/df_pr_sap_ruby_ 64_65_13-02-2020.xlsx',
                          dtype={'цвет':'str', 'чистота':'str'})
df_pr_sapruby = pd.read_excel('module_prgem/df_pr_sap_ruby_ 64_65_13-02-2020.xlsx',
                          dtype={'цвет':'str', 'чистота':'str'})

def size_sap_ruby(carat_1):
    '''функция для определения размерной группы сапфира и рубина, carat_1'''   
    return df_sizes_sap_ruby[(df_sizes_sap_ruby.low_grade<=carat_1)].sort_values('low_grade').iloc[-1,0]

def make_list_sap(t):
    #последний рабочий pattern_sap
    pattern_sap =  r"""(?ix)(?P<N>\d{,3})# штуки 
               (?P<Gem>сапфир[A-яA-z.]{0,5})[-]+  #gem
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
        '''функцая обнаружения ошибок при re распозаваниb сапфиров
        сопоставляет количество пойманных чисто для  # чисто для сапфирП и Н и 
        #последний рабочий pattern_sap'''

        len_p = len(re.findall(pattern_sap, t ))
        len_j = len(re.findall(pattern_jsap, t ))
        return f"bylens:error:{len_p}!={len_j}" if len_p!=len_j else f"ok:{len_p}!={len_j}"

    
    def check_vstlistsapryby(l):
        '''функция для вывода стандартного листа и отчет проверки соответствия словарям '''                           
        #проверка на пусто или []
        if l is np.nan or len(l)==0:
            return 'нет распознанных'
        #создать внутренний dfx
        dfx = pd.DataFrame({'vstlist':l})
        cols = ["PCS","GEM","CARAT", "FORM", "CQ"]
        for c in range(len(cols)):
            dfx[cols[c]] = dfx.vstlist.apply(lambda x: x[c].lower().strip())
        dfx['C'] = dfx['CQ'].apply(lambda x: x.split('/')[0].lower().strip())
        dfx['Q'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[0].strip())
        dfx['C_add'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[-1].strip()\
                                      if x.__contains__('*') else np.nan)

        #пустить проверки по словарям  dcla_sap, dcol_sap, dgem
        report = ''
        report += 'C:ok;' if dfx['C'].apply(lambda x: x in mds.dcol_sap).all() \
                          else f"C:error:{' '.join(dfx.loc[~dfx['C'].apply(lambda x: x in mds.dcol_sap), 'C'].to_list())};"
        report+='Q:ok;' if dfx['Q'].apply(lambda x: x in mds.dcla_sap).all()\
                          else f"Q:error:{' '.join(dfx.loc[~dfx['Q'].apply(lambda x: x in mds.dcla_sap), 'Q'].to_list())};"
        report+='PCS:ok;' if dfx['PCS'].apply(lambda x: x!='').all()\
                          else 'PCS:error:'';'
        report += 'GEM:ok;' if dfx['GEM'].apply(lambda x: x in mds.dgem).all() \
                          else f"GEM:error:{' '.join(dfx.loc[~dfx['GEM'].apply(lambda x: x in mds.dgem), 'GEM'].to_list())};"
        return report 

    def sap_list2std(l):
        '''функция для вывода стандартного листа и отчет проверки соответствия словарям 
        на выходе кортеж 0 - лист со стандартизированными форма, цв, кач ['PCS', 'GEM', 'CARAT', 'FORM', 'C', 'Q',  'C_add']
        1- отчет '''                           
        #проверка на пусто или []
        if l is np.nan or len(l)==0:
            return [],'нет распознанных'
        #создать внутренний dfx
        dfx = pd.DataFrame({'vstlist':l})
        cols = ["PCS","GEM","CARAT", "FORM", "CQ"]
        for c in range(len(cols)):
            dfx[cols[c]] = dfx.vstlist.apply(lambda x: x[c].lower().strip())
        dfx['C'] = dfx['CQ'].apply(lambda x: x.split('/')[0].lower().strip())
        dfx['Q'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[0].strip())
        dfx['C_add'] = dfx['CQ'].apply(lambda x: x.split('/')[1].lower().strip().split('*')[-1].strip()\
                                      if x.__contains__('*') else np.nan)

        #пустить проверки по словарям  dcla_sap, dcol_sap, dgem
        report = ''
        report += 'C:ok;' if dfx['C'].apply(lambda x: x in mds.dcol_sap).all() \
                          else f"C:error:{' '.join(dfx.loc[~dfx['C'].apply(lambda x: x in mds.dcol_sap), 'C'].to_list())};"
        report+='Q:ok;' if dfx['Q'].apply(lambda x: x in mds.dcla_sap).all()\
                          else f"Q:error:{' '.join(dfx.loc[~dfx['Q'].apply(lambda x: x in mds.dcla_sap), 'Q'].to_list())};"
        report+='PCS:ok;' if dfx['PCS'].apply(lambda x: x!='').all()\
                          else 'PCS:error:'';'
        report += 'GEM:ok;' if dfx['GEM'].apply(lambda x: x in mds.dgem).all() \
                          else f"GEM:error:{' '.join(dfx.loc[~dfx['GEM'].apply(lambda x: x in mds.dgem), 'GEM'].to_list())};"
        dfx['GEM_s'] = dfx['GEM'].map(mds.dgem)
        dfx['C_s'] = dfx['C'].map(mds.dcol_sap)
        dfx['Q_s'] = dfx['Q'].map(mds.dcla_sap)
        std_list = dfx[['PCS', 'GEM_s', 'CARAT', 'FORM', 'C_s', 'Q_s', 'C_add']].to_numpy().tolist()
        return std_list, report 

    report = error_by_lens_patts(t)
    rawlist = vst2listsap_notna(t)
    #готовим вывод стандартного листа вставок
    res = sap_list2std(rawlist)
    report += ';'+res[1]
    std_list = res[0]
    
      
    return res[0],report
    
def count_price(stdl):
    #создать внутренний dfx
    dfx = pd.DataFrame({'vstlist':stdl})
    cols = ['PCS', 'GEM', 'CARAT', 'FORM', 'C', 'Q']
    try:
        for c in range(len(cols)):
            dfx[cols[c]] = dfx.vstlist.apply(lambda x: x[c].lower().strip())
    
    
        
       # if stdl.__contains__('NaN'):
       #     raise ValueError("имеется ошибка")
         
        dfx['CARAT'] = dfx['CARAT'].str.replace(',','.').astype('float')
        dfx['PCS'] = dfx['PCS'].astype('int')
        dfx['C'] = dfx['C'].map(mds.dcol_sap)
        dfx['Q'] = dfx['Q'].map(mds.dcla_sap)
        dfx['GEM'] = dfx['GEM'].map(mds.dgem)
        dfx['CARAT_1'] = dfx[['CARAT','PCS']].apply(lambda x: round(x['CARAT']/x['PCS'],3) , axis=1)
        dfx['size'] = dfx['CARAT_1'].apply(lambda x:size_sap_ruby(x)) 
        df_pr_sapruby['GEM'] = df_pr_sapruby['gemstone'].str.lower().map(mds.dgem)
        df_pr_sapruby['C'] = df_pr_sapruby['цвет'].str.lower().map(mds.dcol_sap)
        df_pr_sapruby['Q'] = df_pr_sapruby['чистота'].str.lower().map(mds.dcla_sap)
        
        dfxm = pd.merge(left=dfx, right=df_pr_sapruby[['size', 'price','GEM', 'C', 'Q']],
            how='left', 
            left_on=['GEM','size', 'C', 'Q'],
            right_on=['GEM','size', 'C', 'Q'])
        dfxm['prcost'] = dfxm['CARAT']*dfxm['price']
        #Проверка сработки и правильности
        if len(dfxm)!=len(dfx):
            return 'ошибка мерже'
        elif any(dfxm['price'].isna()):
            return 'не сработал'
        elif len(df_pr_sapruby[['GEM','size', 'C', 'Q']].sum(axis=1).unique())!= len(df_pr_sapruby):
            return 'ошибка прейск'    
            
 

    except:
        return 'error '
    return f"{dfxm['prcost'].sum():,.2f}; {((dfxm['CARAT'].astype('str')+'+').sum()).strip('+')}; \
price:{((dfxm['price'].astype('str')+'+').sum()).strip('+')}; size:{((dfxm['size']+'+').sum()).strip('+')}"   
   # return f"{dfxm['prcost'].sum():,.2f}; carat = {dfxm['CARAT'].sum():,.3f}" 
    
    
 
    
#    return f";{dfx['CARAT'].sum():,.3f};Ok; \
# size:{((dfx['size']+'+').sum()).strip('+')}; price:{((dfx['price'].astype('str')+'+').sum()).strip('+')}; "+report
    #return dfx['CARAT'].sum(),dfx['prcost'].sum(),(dfx['price'].astype('str')+'-').sum(),list(dfx['size']),report
