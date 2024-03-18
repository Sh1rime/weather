import weaher
repeat = True
while repeat:
    print('1. Средняя температура в каждой стране за всё время наблюдений')
    print('2. Год с самой низкой среднегодовой температурой в каждой стране')
    print('3. Самый холодный месяц в каждой стране')
    print('4. Месяц с самой низкой среднегодовой температурой среди всех стран')
    print('5. Страна с самым большим среднегодовым разбросом температуры')
    print('6. Минимальная  и  максимальная  температура  в  каждой  стране  за  всё время наблюдений')
    print('0. Выход')
    try:
        numb = int(input('Выберите номер:'))
    except ValueError:
        print('Ошибка ввода(введите число)')
        continue
    if numb == 1:
        for info in weaher.WeatherData.info1:
            print(info)
    elif numb == 2:
        for info in weaher.WeatherData.info2:
            print(info)
    elif numb == 3:
        for info in weaher.WeatherData.info3:
            print(info)
    elif numb == 4:
        print(weaher.WeatherData.info4)
    elif numb == 5:
        print(weaher.WeatherData.info5)
    elif numb == 6:
        for info in weaher.WeatherData.info6:
            print(info)
    elif numb == 0:
        repeat = False
    else:
        print('Неверный номер')
