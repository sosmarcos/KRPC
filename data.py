def data_convert(data_str):
    data = data_str.split('/')
    data_int = list()
    for index in enumerate(data):
        num = list()
        for c in range(0, len(index[1])):
            if index[1][c] == '0':
                num.append(0)
            elif index[1][c] == '1':
                num.append(1)
            elif index[1][c] == '2':
                num.append(2)
            elif index[1][c] == '3':
                num.append(3)
            elif index[1][c] == '4':
                num.append(4)
            elif index[1][c] == '5':
                num.append(5)
            elif index[1][c] == '6':
                num.append(6)
            elif index[1][c] == '7':
                num.append(7)
            elif index[1][c] == '8':
                num.append(8)
            elif index[1][c] == '9':
                num.append(9)
        for c in range(0, len(num)):
            if len(num) == 2:
                if c == 0:
                    num[0] = num[0] * 10
            else:
                if c == 0:
                    num[0] = num[0] * 1000
                elif c == 1:
                    num[1] = num[1] * 100
                elif c == 2:
                    num[2] = num[2] * 10
        if len(num) == 2:
            num = num[0] + num[1]
        else:
            num = num[0] + num[1] + num[2] + num[3]
        data_int.append(num)
    return data_int


data_inicial = data_convert(input('data inicial: '))
data_final = data_convert(input('data final: '))

anos_total = data_final[2] - data_inicial[2] + 1
mes_inicial = data_inicial[1]
mes_final = data_final[1]
dia_inicial = data_inicial[0]
dia_final = data_final[0]
dias = 0
for anos in range(0, anos_total):
    ano_teste = data_inicial[2] + anos
    if ano_teste % 4 == 0 and ano_teste % 100 != 0 or ano_teste % 400 == 0:
        bissexto = True
    else:
        bissexto = False
    ano = [['janeiro', 31],
            ['fevereiro', 28],
            ['março', 31],
            ['abril', 30],
            ['maio', 31],
            ['junho', 30],
            ['julho', 31],
            ['agosto', 31],
            ['setembro', 30],
            ['outubro', 31],
            ['novembro', 30],
            ['dezembro', 31]]
    if bissexto:
        ano[1][1] = 29
    for mes in enumerate(ano):
        for dia in range(0, mes[1][1]):
            if anos_total == 1:
                if mes_inicial == mes_final == mes[0] + 1:
                    if dia_inicial <= dia + 1 <= dia_final:
                        dias += 1
                elif mes_final >= mes[0] + 1 >= mes_inicial:
                    if mes_inicial == mes[0] + 1 and dia_inicial <= dia + 1:
                        dias += 1
                    elif mes_final == mes[0] + 1 and dia_final >= dia + 1:
                        dias += 1
                    elif mes_final > mes[0] + 1 > mes_inicial:
                        dias += 1
            else:
                if anos == 0:
                    if mes_inicial == mes[0] + 1:
                        if dia_inicial <= dia + 1:
                            dias += 1
                    elif mes_inicial < mes[0] + 1:
                        dias += 1
                elif anos == anos_total - 1:
                    if mes_final == mes[0] + 1:
                        if dia_final >= dia + 1:
                            dias += 1
                    elif mes_final > mes[0] + 1:
                        dias += 1
                elif 0 < anos < anos_total - 1:
                    dias += 1
print(f'\ndias de vida: {dias}')
while True:
    if input('>') == 'sair':
        break

