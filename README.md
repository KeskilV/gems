# gems
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

(порядок обратный)
20-11-2023 по 23-11-2023

Создан модуль для оценки ЦВДК релиз 2023-11-23 ..\gems_git\gems\ipynb\module_prgem
Данные для тестирования - ..\gems_git\gems\ЦВДК\выгрузка17_11_2023_все_склады_ДК_17_11_2023_08_01_res_pr.xlsx  (Свод данных из наличия ДК+версии W:\DAS\Desktop\GM TMP\Analytics\Общее\Выгрузки\23-11-16 16-00 Сводка ЮИ .xlsx)
Результат теста - ..\gems_git\gems\ЦВДК\2023-11-22 res total
Гит – ссылка на коммит - https://github.com/KeskilV/gems/commit/8976abbabbaf278e209e4b4d685a39f6bef64eca
TODO начата работа по другой концепции – чтобы на входе функции был текст Вставки - 5.1  Разработка def list_gem для всех камней - ..\gems_git\gems\ipynb\gem22.ipynb 
Проблема – выводить стоимость не из стандартного листа, а результата работы функции price_sap_ruby.make_list_ruby(vst_text), т к на выходе используется массив из стандартного листа и отчета о процедуре re и стандартизации – это важно чтобы не пропустить несоответствия в оценке и поставить – «возможно проблема см репорт!»

17-11-2023

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


