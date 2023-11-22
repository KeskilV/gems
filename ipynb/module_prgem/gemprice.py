def gemprice(df_orig, colname_vst):
    '''функция расчета прейскурантной стоимости цветных камней'''
    import numpy as np
    import pandas as pd
    import re
    import os
    import importlib
    import module_prgem.price_em as price_em
    import module_prgem.price_sap_ruby as price_sap_ruby
    import module_prgem.dictgems as mds

    def float_numeric(s):
        if type(s) == type('s'):
            return float(s) if s.replace('.','').isnumeric() else s
        else:
            return s

    def sum_str(l):
        sumstr = '' 
        for x in [z for z in l if type(z) == type('s')]:
            if not (x.replace('.','').isnumeric()):
                sumstr+=x+';'
        if sumstr == '':
            return sum([float(x) for x in l if x!=np.nan])
        else:
            return sumstr

    
    df = df_orig.rename(columns = {colname_vst:'vst'}).copy(deep=True)
    
            
    #Быстрый повтор сапфиров
    df['make_list_sap_20'] = df.vst.apply(lambda x: price_sap_ruby.make_list_sap(x))
    df['list_std_sap20'] = df['make_list_sap_20'].apply(lambda x: x[0])
    df['report_sap20'] = df['make_list_sap_20'].apply(lambda x: x[1])
    df['count_price_sap20']=df['make_list_sap_20'].apply(lambda x: price_sap_ruby.count_price_report(x))
    df['prsap_cost'] = df['count_price_sap20'].apply(lambda x: 0 if len(x)==0 else x.split(";")[0]) #map(len)!=0]

    # результат функции (стандартный лист, рапорт распознавания ) 
    df['make_list_ruby20'] = df.vst.apply(lambda x: price_sap_ruby.make_list_ruby(x))
    # стандартный лист
    df['list_std_ruby20'] = df['make_list_ruby20'].apply(lambda x: x[0])
    # рапорт распознавания 
    df['report_ruby20'] = df['make_list_ruby20'].apply(lambda x: x[1])
    #  результат функции (рапорт применения прейскуранта) 
    df['count_price_ruby20']=df['make_list_ruby20'].apply(lambda x: price_sap_ruby.count_price_report(x))
    # прейскурантая стоимсоть float или ошибка 
    df['prruby_cost'] = df['count_price_ruby20'].apply(lambda x: 0 if len(x)==0 else x.split(";")[0]) #map(len)!=0]

    #  результат функции (рапорт применения прейскуранта) 
    df['count_price_ruby20']=df['make_list_ruby20'].apply(lambda x: price_sap_ruby.count_price_report(x))
    # прейскурантая стоимсоть float или ошибка 
    df['prruby_cost'] = df['count_price_ruby20'].apply(lambda x: 0 if len(x)==0 else x.split(";")[0]) #map(len)!=0]
    # результат функции (стандартный лист, рапорт распознавания ) 
    df['make_list_em20'] = df.vst.apply(lambda x: price_em.list2std_em_sap_ruby(price_em.vst2list(x)))
    # стандартный лист
    df['list_std_em20'] = df['make_list_em20'].apply(lambda x: x[0])
    # рапорт распознавания 
    df['report_em20'] = df['make_list_em20'].apply(lambda x: x[1])
    # не стандартный лист (только изумруд)
    df['prem_vst2list'] = df.vst.map(price_em.vst2list)
    #  результат функции (рапорт применения прейскуранта) 
    df['count_price_em20']=df['prem_vst2list'].map(price_em.check_vstlist)
    # прейскурантая стоимсоть float или ошибка 
    #df['prem_cost'] = df['prem_cost'] = df['count_price_em20'].apply(lambda x: float(x.split(';')[0].replace('prcost:','').replace(',',''))  if type(x)==type('s')else 0)
    # прейскурантая стоимсоть float или ошибка 
    #df['prem_cost'] = df['prem_cost'] = df['count_price_em20'].apply(lambda x: float(x.split(';')[0].replace('prcost:','').replace(',',''))  if type(x)==type('s')else 0)
    df['prem_cost'] = df['count_price_em20'].apply(lambda x: 0 if len(x)==0 else x.split(";")[0]) #map(len)!=0]


    df['prruby_cost2'] = df['prruby_cost'].map(float_numeric)

    df['prsap_cost2'] = df['prsap_cost'].map(float_numeric)

    df['prem_cost2'] = df['prem_cost'].map(float_numeric)

    df['sum_pr2'] = df[['prruby_cost2','prsap_cost2','prem_cost2' ]].apply(lambda x: sum_str(x), axis=1)

    # суммирование листа всех ДК
    df['list_sum'] = df[['list_std_ruby20','list_std_sap20','list_std_em20' ]]\
    .apply(lambda x: x['list_std_ruby20']+x['list_std_sap20']+x['list_std_em20'], axis=1)

    #суммирование репортов всех ДК
    df['report_sum'] = df[['report_ruby20','report_sap20','report_em20' ]]\
    .apply(lambda x: f"r:{x['report_ruby20']}; s:{x['report_sap20']}; e:{x['report_em20']}", axis=1)
    return df[['Код','vst', 'list_sum', 'report_sum', 'sum_pr2']]
