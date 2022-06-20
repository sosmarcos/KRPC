from time import sleep
import manobra
import krpc


def act():
    print('Ativação de Estagios acionada')
    vessel.control.activate_next_stage()


def descartar_booster():
    print('Descarte altomatico do booster acionado')
    combustivel_solido = conexão.get_call(vessel.resources.amount, 'SolidFuel')
    expr = conexão.krpc.Expression.less_than(conexão.krpc.Expression.call(combustivel_solido), conexão.krpc.Expression.constant_float(0.1))
    evento = conexão.krpc.add_event(expr)
    with evento.condition:
        evento.wait()
    act()


def corrigir_direção():
    inclinação = int(input('Inclinação: '))
    print(f'Inclinação do alvo trasferida para {inclinação}º')
    sleep(0.4)
    
    direção = int(input('direção: '))
    print(f'Direção do alvo trasferida para {direção}º')
    sleep(0.4)

    print('\naguardando altitude de manobra...')

    altitude_media = conexão.get_call(getattr, vessel.flight(), 'mean_altitude')
    expr = conexão.krpc.Expression.greater_than(conexão.krpc.Expression.call(altitude_media), conexão.krpc.Expression.constant_double(5000))
    event = conexão.krpc.add_event(expr)
    with event.condition:
        event.wait()
    print('Direção alterada para o alvo')
    vessel.auto_pilot.target_pitch_and_heading(inclinação, direção)


def altitude_final():
    print('Aguardando apoastro de 71km...')
    apoastro = conexão.get_call(getattr, vessel.orbit, 'apoapsis_altitude')
    expr = conexão.krpc.Expression.greater_than(
        conexão.krpc.Expression.call(apoastro), conexão.krpc.Expression.constant_double(71000)
        )
    event = conexão.krpc.add_event(expr)
    with event.condition:
        event.wait()
    vessel.control.throttle = 0
    print('Aceleração em 0%')
    sleep(1)
    vessel.auto_pilot.disengage()

instruções = {
    'sir': 'Encerra o programa',
    'dcl': 'Decolar',
    'act': 'Aciona o proximo estagio',
    'icl': 'Altera a inclinação',
    'dir': 'Altera a direção',
    'dct': 'Altomatiza o descarte do booster',
    'cva': 'Corrige a direção',
    'atf': 'Desativa o piloto no apoastro',
    'obt': 'Manobra orbital'}
    
print('Dicionario:')
for key, value in instruções.items():
    print(f'{key}..........{value}')

conexão = krpc.connect(name='Sub-orbital fligth')
vessel = conexão.space_center.active_vessel
inclinação = 90
direção = 90

sair = False
while not sair:
    instrução = str(input('\nIst: '))
    codigo_de_instrução = instrução.split('.')[0]
    if codigo_de_instrução == "sir":
        sair = True

    elif codigo_de_instrução == 'ist':
        print('\nDicionario')
        for key, value in instruções.items():
            print(f'{key}..........{value}')

    elif codigo_de_instrução == 'dcl':
        manobra.decolagem(
            int(input('Manobra: ')),
            int(input('Altitude: ')),
            int(input('Apoastro: '))
        )

    elif codigo_de_instrução == 'act':
        act()

    elif codigo_de_instrução == 'icl':
        inclinação = int(input('Inclinação: '))
        print(f'Inclinação do alvo trasferida para {inclinação}º')
        vessel.auto_pilot.target_pitch_and_heading(inclinação, direção)
        sleep(0.4)

    elif codigo_de_instrução == 'dir':
        direção = int(input('direção: '))
        print(f'Direção do alvo trasferida para {direção}º')
        vessel.auto_pilot.target_pitch_and_heading(inclinação, direção)
        sleep(0.4)

    elif codigo_de_instrução == 'dct':
        descartar_booster()

    elif codigo_de_instrução == 'cva':
        corrigir_direção()

    elif codigo_de_instrução == 'atf':
        altitude_final()

    elif codigo_de_instrução == 'obt':
        manobra.orbital()

    else:
        print('INSTRUÇÃO INVALIDA')
