'''
parametrs = {'ШТУК':'ШТУК','ОГРАНКА':'ОГРАНКА', 'КАРАТ':'КАРАТ', 'ПО': 'ПО', 'Ц':'Ц', 'Д':'Д'}
rusian price of diamond v14-10-21 
def rpdiamonds({'id':1,'ОГРАНКА':['Кр-57А'], 'Ц':[3], 'Д':['7а'], 'ПО': 'A','ШТУК':[1],'КАРАТ':0.35})
'''
#
#import numpy as np
import pandas as pd
#import re
#import os
from rusprice.dictdiamonds import dcol_dia, dcla_dia, dpo_dia, dogr_dia_discount

parametrs = {'ШТУК':'ШТУК','ОГРАНКА':'ОГРАНКА', 'КАРАТ':'КАРАТ', 'ПО': 'ПО', 'Ц':'Ц', 'Д':'Д'}

#init globals 1
#carat_to_grp = pd.read_excel("rusprice/CARtoKVG.xlsx", sheet_name= 3).iloc[:,0:3]
carat_to_grp = pd.read_csv("rusprice/CARtoKVG.csv").drop(columns = 'Unnamed: 0')
carat_to_grp.columns = ['grp','caratmin','caratmax']


#init globals 2
#KVG57ct = pd.read_excel('rusprice/KVG57ct.xlsx')
KVG57ct = pd.read_csv('rusprice/KVG57ct.csv')
##ogrdiscount_f = pd.read_excel('rusprice/ogrdiscount_f.xlsx')
#ogrdiscount = pd.read_excel('rusprice/ogrdiscount_f.xlsx')
ogrdiscount = pd.read_csv('rusprice/ogrdiscount_f.csv')
ogrdiscount.rename(columns={'Ogr':'ogrdisc'},inplace =True)
PRD = pd.read_csv('rusprice/PR2019_270921.csv').set_index('Код')
PRD.columns = ['OGR', 'GRUP', 'KVG', 'PO', 'Col', 'Cla', 'Pst', 'Carat', 'Pr2018',
       'Pr2019']
PRD[['Pr2018','Pr2019']] = PRD[['Pr2018','Pr2019']].astype('float64')
PRD.rename(columns={'OGR':'ogrbasic','GRUP':'Grp', 'PO':'Po','Pst':'ШТУК','Carat':"КАРАТ"}, inplace=True)


class DataError(Exception):
    pass

def checkdata(df):
    if not set(parametrs.keys()) <= set(df.columns): 
        raise DataError('проверьте состояние параметров ОГРЦДПОШК',df.columns)
    ch ={}
    ch['col'] = df.Ц.apply(lambda x: x in dcol_dia).unique()
    ch['cla'] = df.Д.apply(lambda x: x in dcla_dia).unique()
    ch['po']  = df.ПО.apply(lambda x: x in dpo_dia).unique()
    ch['ogr'] = df.ОГРАНКА.apply(lambda x: x in dogr_dia_discount).unique()
    ch['shtuk'] = [True]
    ch['carat'] = [True]
    status = ''
    err = 1
    for i in ch.keys():
        status += ' {} - {} ;'.format(i,(ch[i][0] and len(ch[i]) == 1))
        err*=(ch[i][0] and len(ch[i]) == 1)
    if not err:
        raise DataError('проверьте Ц Д ПО ОГРАНКА', status)
        
    return err, status

def dogr_dia_basic(freeogr):
    
    real_ogr = dogr_dia_discount[freeogr]
    return real_ogr if real_ogr == 'Кр-57' or real_ogr == 'Кр-17' else 'Кр-57'

def grp_dia(pcs, carat):
    global  carat_to_grp
    acarat = round(carat/pcs,5)+0.00001
    res1 = carat_to_grp[round(carat_to_grp.caratmin,4) < acarat].grp.index.max()
    res2 = carat_to_grp[round(carat_to_grp.caratmax,4) > acarat].grp.index.min()
    return carat_to_grp.iloc[res1,0] if res2 == res1 else 'round error grp file'
def discont_po (po):
    dpo_dia = {'A': 'А', 'a': 'А', 'А': 'А', 'а': 'А', 'б': 'Б', 'Б': 'Б', 'В': 'В', 'в': 'В', 'В': 'В', 'г': 'Г', 'Г': 'Г' }
    dic_discont_po = {'А':1, 'Б':0.85, 'В':0.80, 'Г':0.75}
    return round(dic_discont_po[dpo_dia[po]],2)
def fillgrp(grps,grpe):
    global KVG57ct 
    l=list()
    def correctgrp(g):
        return g if g!='4.0-3.3' else '4-3.4'
    grps = correctgrp(grps)
    grpe = correctgrp(grpe)
    for i in range(KVG57ct[KVG57ct.Grp == grps].index[0],KVG57ct[KVG57ct.Grp == grpe].index[0]+1):
        l.append(KVG57ct.iloc[i,0])
    return l

def rpdiamonds(df_original, error_msg = True):
    '''DataFrame -> DataFrame with prpr prcost, error_msg = True'''
    df = df_original.copy()
    try:
        status = checkdata(df)
        if not status[0]:
            raise DataError(status[1])
    except DataError as e:
        print(e)
    #обработка ошибок
    #print(df[~df.ОГРАНКА.apply(lambda x: x in dogr_dia_discount)].ОГРАНКА.unique())
    #print(df[~df.ПО.apply(lambda x: x in dpo_dia)].ПО.unique())
    #print(df[~df.Ц.apply(lambda x: x in dcol_dia)].Ц.unique())
    #print(df[~df.Д.apply(lambda x: x in dcla_dia)].Д.unique())
    #a.loc[df.ОГРАНКА == 'Р-57','ОГРАНКА']
    df['СРКАРАТ'] = df.КАРАТ/df.ШТУК
    #df.loc[df.СРКАРАТ > 0.3000,'СРКАРАТ'].sort_values().unique()
    print(df.СРКАРАТ.min(),' - ', end = '')#sort_values().unique()
    print(df.СРКАРАТ.max())
    #print(df.loc[a.СРКАРАТ > 2,['id7c','vstavki','vs_dict','gem','ШТУК','ОГРАНКА','КАРАТ','СРКАРАТ','ЦД','ПО','Ц','Д']].sort_values('СРКАРАТ',ascending = False))
    diamonds = df
    diamonds['Col'] = diamonds.Ц.map(dcol_dia)
    diamonds['Cla'] = diamonds.Д.map(dcla_dia)
    diamonds['Po'] = diamonds.ПО.map(dpo_dia)
    diamonds['ogrdisc']= diamonds.ОГРАНКА.map(dogr_dia_discount)
    diamonds['Grp'] = diamonds[['ШТУК','КАРАТ']].apply(lambda x: grp_dia(x.ШТУК,x.КАРАТ), axis=1)
    diamonds['discont_po'] = diamonds.Po.map(discont_po)
    diamonds['ogrbasic'] = diamonds.ОГРАНКА.apply(lambda x: dogr_dia_basic(x))
    res0 = pd.merge(diamonds,PRD[['ogrbasic','Grp','Col','Cla','Pr2019']], how='left',left_on=['ogrbasic','Grp','Col','Cla'], right_on=['ogrbasic','Grp','Col','Cla'])
    res=pd.merge(res0,ogrdiscount[['ogrdisc','Grp','ogrdiscount']], how = 'left', left_on = ['ogrdisc','Grp'], right_on =  ['ogrdisc','Grp'])
    res['prpr'] = round(res.Pr2019*res.ogrdiscount*res.discont_po+0.0000001,0)
    res['prcost'] = round(res.prpr*res.КАРАТ,2)
    print('не сработал прейскурант на строках:\n  ', res.loc[pd.isna(res.prpr),['ШТУК',
       'ОГРАНКА', 'КАРАТ', 'ПО', 'Ц', 'Д', 'СРКАРАТ', 'Col',
       'Cla', 'Po', 'ogrdisc', 'Grp', 'discont_po', 'ogrbasic', 'Pr2019',
       'ogrdiscount', 'prpr', 'prcost']].index)
    return res