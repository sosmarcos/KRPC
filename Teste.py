import krpc
from time import sleep


def decolagem(commando, nau, altitude_inicial=250, altitude_final=45000, apoastro_alvo=150000):
    # configuraçoes para a telemetria
    print(commando)
    altitude = commando.add_stream(getattr, nau.flight(), 'mean_altitude')
    apoastro = commando.add_stream(getattr, nau.orbit, 'apoapsis_altitude')
    booster = nau.resources_in_decouple_stage(stage=0, cumulative=False)
    combustivel_solido = commando.add_stream(booster.amount, 'SolidFuel')

    # configurações de pre-lançamento
    nau.control.sas = False
    nau.control.rcs = False
    nau.control.throttle = 1.0

    # ativação do primeiro estagio
    nau.control.activate_next_stage()
    nau.auto_pilot.engage()
    nau.auto_pilot.target_pitch_and_heading(90, 90)

    # loop principal
    separação = False
    ângulo_de_curva = 0
    while True:
        # curva gravitacional
        if altitude_inicial < altitude() < altitude_final:
            frac = ((altitude() - altitude_inicial) / (altitude_final - altitude_inicial))
            novo_ângulo_de_curva = frac * 90
            if abs(novo_ângulo_de_curva - ângulo_de_curva) > 0.5:
                ângulo_de_curva = novo_ângulo_de_curva
                nau.auto_pilot.target_pitch_and_heading(90 - ângulo_de_curva, 90)

        # separação do booster
        if not separação:
            if combustivel_solido() < 0.1:
                nau.control.activate_next_stage()
                separação = True
                print('separação do booster')
        
        if apoastro() > apoastro_alvo * 0.9:
            print('fim da curva. aguardando o apoastro')
            break
        print(f'Combustivel Solido: {int(combustivel_solido())}')

    # Desabilitar os motores quando o apoastro alvo for atingido
    nau.control.rcs = True
    nau.control.throttle = 0.25
    while apoastro() < apoastro_alvo:
        pass

    print('apoastro atingido')
    nau.control.throttle = 0.0


commando = krpc.connect()
nau = commando.space_center.active_vessel

while True:
    v_orbital = nau.flight(nau.orbit.body.non_rotating_reference_frame).speed
    v_superficial = nau.flight(nau.orbit.body.reference_frame).speed
    altitude = nau.flight(nau.orbit.body.reference_frame).mean_altitude
    apoastro = nau.orbit.apoapsis_altitude
    periastro = nau.orbit.periapsis_altitude
    tempo_de_apoastro = nau.orbit.time_to_apoapsis
    booster = nau.resources_in_decouple_stage(stage=0, cumulative=False)
    combustivel_solido = commando.add_stream(booster.amount, 'SolidFuel')
    velocidade_vertical = nau.flight(nau.orbit.body.reference_frame).vertical_speed

    print(f'Velocidade Orbital: {int(v_orbital)}m/s')
    print(f'Velocidade Superficial: {int(v_superficial)}m/s')
    print(f'Altitude: {int(altitude)}m')
    print(f'Apoastro de {int(apoastro)}m em {int(tempo_de_apoastro)}s')
    print(f'Periastro: {int(periastro)}m')
    print(f'Combustivel Solido: {int(combustivel_solido())}')
    print('')
    sleep(1.5)

''' if self.after_id:
    self.label.after_cancel(self.after_id)
    print('after cancelado')
    self.after_id = None'''
