Модуль для расчета прйскуранта ЦВ 

код для функций:
price_em.py

словари:
dictemeralds.py

таблицы размерностей:
size_em_sto.xlsx
sizes_ruby_sap_sto.xlsx

таблицы прейскурантов в виде бд:
df_pr_emeralds_sto_173_20-04-2023.xlsx

папка для прейскурантов:
прейскуранты обработка

./папка для кода и вспомогательных файлов для обработк прейскурантов в вид БД:
./прейскуранты обработка/промежуточные


К описанию функций в общем файле сборки 
# результат функции (стандартный лист, рапорт распознавания ) 
df_test['make_list_ruby20'] = df_test.vst.apply(lambda x: price_sap_ruby2.make_list_ruby(x))
# стандартный лист
df_test['list_std_ruby20'] = df_test['make_list_ruby20'].apply(lambda x: x[0])
# рапорт распознавания 
df_test['report_ruby20'] = df_test['make_list_ruby20'].apply(lambda x: x[1])
#  результат функции (рапорт применения прейскуранта) 
df_test['count_price_ruby20']=df_test['make_list_ruby20'].apply(lambda x: price_sap_ruby2.count_price_report(x))
# прейскурантая стоимсоть float или ошибка 
df_test['prruby_cost'] = df_test['count_price_ruby20'].apply(lambda x: 0 if len(x)==0 else x.split(";")[0]) #map(len)!=0]