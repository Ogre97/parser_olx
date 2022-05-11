import requests
import datetime
import csv
import time
import token_telefona_olx as Token
from bs4 import BeautifulSoup


# Для запроса на сайт чтобы думал что мы не робат
headers_silki = {
	
    'Accept':'*/*',
    'Host': 'www.olx.uz',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43', 
    'X-Platform-Type': 'mobile-html5',

}

klok = Token.token()
headers_telefoni = {
	
    'Accept':'*/*',
    'Host': 'www.olx.uz',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43', 
    'X-Platform-Type': 'mobile-html5',
    'Authorization': f'Bearer {klok}',

    # Bearer 9868a480bbc52754fad1ce7f86eae70504c1b1a6
    # Bearer 4c22ec9bd91f8905abbf9cad2420f69f3324ea7c
    # Bearer 95372109a0af6e4139b4ac58a07d9978b2275cda
    # Bearer 9868a480bbc52754fad1ce7f86eae70504c1b1a6
    # 9868a480bbc52754fad1ce7f86eae70504c1b1a6


}

# Проверка есть такой айди в баззе данных есть есть то верни True если нет то нечего не возращай 

def proverka(id_obyavlenia, id_kol):
	with open('ID_ojekt.csv', 'r', newline='', encoding='UTF-8') as file:
		ID_ojekt = csv.reader(file)
		for id_spisok in ID_ojekt:
			if str(id_obyavlenia) == str(id_spisok[0]):
				print('Такое обьявление в базе есть')
				print(id_kol)
				return False
			elif id_kol == 40:
				print('Новых обьявлений нет')
				return True

#Счет публикаций
schet_kartochek = 0

print('Программа Работает')
# Открываем сайт и записываем все в html файл для дальнейшей работы с ним 
def hreh_silki():
	url = f'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/?search%5Bprivate_business%5D=private&page=1'
	req = requests.get(url, headers=headers_silki)
	src = req.text
	return src
#Гланая функция
def main():
	id_kol = 0
#Глобальная переменная
	global schet
	global schet_kartochek
	schet = 0

# Записываем в переменную со значение суппа из файла
	sup = BeautifulSoup(hreh_silki(), 'lxml')
# Собираем все все заголовки с сылками 
	link_href_sup = sup.find_all('a', class_='marginright5 link linkWithHash detailsLink')
	all_rayon = sup.find('table', id ='offers_table').find_all('p', class_='lheight16')
	time.sleep(6) # Время на которое замедляется программа

#Создаем список страницы с районами
	all_rayon_text = []
	for i in all_rayon:
		x = i.find('span')
		if x != None:
			all_rayon_text.append(x.text)
	print('Собрал все районы')

#Добавляем все ссылки в список
	all_href = [] 
	for i in link_href_sup:
		item_href = i.get('href') # Извлекаем только ссылки 
		all_href.append(item_href) # Добавляем ссылки в список
	print('Собрал все ссылки')
	
# Переходит по сыллки для записе в переменную
	for i in all_href:
		time.sleep(6) # Замеделение программы
		silka_ = i
		req = requests.get(i, headers=headers_silki)
		src_1 = req.text
		sup_1 = BeautifulSoup(src_1, 'lxml')

#Берем все значения комнат этаж и тд
		vse_znacenia_kv = sup_1.find('div', class_='css-1wws9er').find('ul', class_='css-sfcl1s').find_all('li', class_='css-ox1ptj')
		vse_znacenia_kv_spisok = []
		for i in vse_znacenia_kv:
			a = i.find('p', class_='css-xl6fe0-Text eu5v0x0').text
			vse_znacenia_kv_spisok.append(a.split(':'))

#Срезаем первое значение бизнес или часстник 
		vse_znacenia_kv_spisok = vse_znacenia_kv_spisok[1:]
#Создаем список со словарем
		slovar_znacheniyami = dict(vse_znacenia_kv_spisok)

#Район 	
		try:
			rayon = all_rayon_text[schet] # Берем элемент из списка по счетку
		except:
			rayon = '*'

#Id объявления
		id_obyavlenia = sup_1.find('span', class_='css-9xy3gn-Text eu5v0x0').text[4:]
# Проверка функции есть ли такое обьявление в базе то закрыть программу
		if proverka(id_obyavlenia, id_kol) == False:
			id_kol += 1
			continue
		elif proverka(id_obyavlenia, id_kol) == True:
				break
# Добавляет айди в базу данных
		with open('ID_ojekt.csv', 'a', newline='', encoding='UTF-8') as file:
			id_x = csv.writer(file, delimiter=',')
			id_x.writerow((str(id_obyavlenia),))
#Описание объявления
		try:
			opisanie = sup_1.find('div', class_='css-g5mtbi-Text').text
			opisanie = opisanie.replace('\n',' ')
		except:
			opisanie = '*'
#Сылка 	
		try:
			silka_objavlenia = silka_
		except:
			silka_objavlenia = '*'
#Комнат
		try:
			kol_komnat = slovar_znacheniyami['Количество комнат'].lstrip()
		except:
			kol_komnat ='*'
#Этаж
		try:
			itaj = slovar_znacheniyami['Этаж'].lstrip()
		except:
			itaj ='*'
#Этажность дома	
		try:
			itajnost = slovar_znacheniyami['Этажность дома'].lstrip()
		except:
			itajnost = '*'
#Общая площадь	
		try:
			kv_m = slovar_znacheniyami['Общая площадь'].lstrip()
		except:
			kv_m = '*'
#Типо строения	
		try:
			tip_stroenia = slovar_znacheniyami['Тип строения'].lstrip()
		except:
			tip_stroenia = '*'
#Ремонт	
		try:
			remont = slovar_znacheniyami['Ремонт'].lstrip()
		except:
			remont = '*'
# Цена
		try:
			cena = sup_1.find('h3', class_='css-okktvh-Text eu5v0x0').text
		except:
			cena = '*'
		time.sleep(5) # Время на которое замедляется программа
# Телефон
		try:
			telefon_spisok = requests.get(f'https://www.olx.uz/api/v1/offers/{id_obyavlenia}/limited-phones/', headers=headers_telefoni).text
			telefon_spisok = telefon_spisok[20:-4]
		except:
			telefon_spisok = '*'
			print('Не удалось получить номер')
		data_dey = datetime.date.today().strftime('%d.%m.%Y') # Дата сегодня
#Запись в файл
		# Условие если файла с таким названием нет, то создай его и потом запиши значения
		# А если такой файл есть просто добавь в него значения
		try:
			# Создаем файл со значениями
			with open(f'Аренда_{data_dey}.csv', 'x', newline='', encoding='UTF-8') as file:
				writer = csv.writer(file, delimiter=',')
				writer.writerow(
					(
						'Id', 
						'Дата записи', 
						'Дата подачи', 
						'Адрес', 
						'Ориентир', 
						'Комнат', 
						'Этаж',
						'Этажность', 
						'Кв.м',
						'Материал', 
						'Ремонт',
						'Описание',
						'Цена',
						'Телефон',
						'Сылка',
					)
				)
				print('Создал файл')
			# Записываем в файл
			with open(f'Аренда_{data_dey}.csv', 'a', newline='', encoding='UTF-8') as file_1:
				writer = csv.writer(file_1, delimiter=',')
				writer.writerow(
					(
						id_obyavlenia, 
						data_dey, 
						'*', 
						rayon[8:], 
						'*', 
						kol_komnat, 
						itaj,
						itajnost, 
						kv_m,
						tip_stroenia, 
						remont,
						opisanie,
						cena,
						telefon_spisok,
						silka_objavlenia,
					)
				)
			print('Записал все в файл')

		except:
			# Записываем в файл
			with open(f'Аренда_{data_dey}.csv', 'a', newline='', encoding='UTF-8' ) as file_2:
				writer = csv.writer(file_2, delimiter=',')
				writer.writerow(
					(
						id_obyavlenia, 
						data_dey, 
						data_dey, 
						rayon[8:], 
						'*', 
						kol_komnat, 
						itaj,
						itajnost, 
						kv_m,
						tip_stroenia, 
						remont,
						opisanie,
						cena,
						telefon_spisok,
						silka_objavlenia,
					)
				)
			print('Записал все в файл')



		# Счетки данных
		schet_kartochek += 1
		schet += 1
		print(f'Спарсилось {schet_kartochek} карточек')


if __name__ == '__main__':
	main()
	hreh_silki()
