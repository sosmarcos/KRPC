from math import *
from time import sleep
import krpc

commando = krpc.connect('Decolagem Orbital')
nau = commando.space_center.active_vessel

curva = {
    'altitude inicial': 250,
    'alltitude final': 45000,
    'apoastro': 150000
}

ut = commando.add_stream(getattr, commando.space_center, 'ut')

  # configuraçoes para a telemetria
altitude = commando.add_stream(getattr, nau.flight(), 'mean_altitude')
apoastro = commando.add_stream(getattr, nau.orbit, 'apoapsis_altitude')
booster = nau.resources_in_decouple_stage(stage=0, cumulative=False)
combustivel_solido = commando.add_stream(booster.amount, 'SolidFuel')

  # configurações de pre-lançamento
nau.control.sas = False
nau.control.rcs = False
nau.control.throttle = 1.0

for contagem in range(5, 0, -1):
    print(contagem)
    sleep(1)
print('lançamento')

  # ativação do primeiro estagio
nau.control.activate_next_stage()
nau.auto_pilot.engage()
nau.auto_pilot.target_pitch_and_heading(90, 90)

  # loop principal
separação = False
ângulo_de_curva = 0
while True:
      # curva gravitacional
    if curva['altitude inicial'] < altitude() < curva['alltitude final']:
        frac = ((altitude() - curva['altitude inicial']) / (curva['alltitude final'] - curva['altitude inicial']))
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
    
    if apoastro() > curva['apoastro'] * 0.9:
        print('fim da curva. aguardando o apoastro')
        break

  # Desabilitar os motores quando o apoastro alvo for atingido
nau.control.rcs = True
nau.control.throttle = 0.25
while apoastro() < curva['apoastro']:
    pass

print('apoastro atingido')
nau.control.throttle = 0.0

while altitude() < 70500:
    pass

print('escapando da atmosfera de kerbin')

  # planejando orbita
print('planejando orbita')
mu = nau.orbit.body.gravitational_parameter
r = nau.orbit.apoapsis
a1 = nau.orbit.semi_major_axis
a2 = r
v1 = sqrt(mu*((2./r)-(1./a1)))
v2 = sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
nó = nau.control.add_node(ut() + nau.orbit.time_to_apoapsis, prograde=delta_v)

  # calculando tempo de queima
F = nau.available_thrust
Isp = nau.specific_impulse * 9.82
m0 = nau.mass
m1 = m0 / exp(delta_v/Isp)
quociente_de_vazão = F / Isp
tempo_de_queima = (m0 - m1) / quociente_de_vazão

nau.auto_pilot.reference_frame = nó.reference_frame
nau.auto_pilot.target_direction = (0, 1, 0)
nau.auto_pilot.wait()

print('Aguardando a queima de circularização')
queima_ut = ut() + nau.orbit.time_to_apoapsis - (tempo_de_queima/2)
espera = 5
commando.space_center.warp_to(queima_ut - espera)

print('pronto para executar a manobra')
tempo_ate_apoastro = commando.add_stream(getattr, nau.orbit, 'time_to_apoapsis')
while tempo_ate_apoastro() - (tempo_de_queima/2) > 0:
  pass

print('iniciando queima')
nau.control.throttle = 1.0
sleep(tempo_de_queima - 0.1)

nau.control.throttle = 0.05
queima_restante = commando.add_stream(nó.remaining_burn_vector, nó.reference_frame)
while queima_restante()[1] > 0:
  pass
nau.control.throttle = 0.0
nó.remove()
print('lançamento completo')
