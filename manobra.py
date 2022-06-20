from math import *
from tkinter import *
from time import sleep
import pages


class Decolagem:
    def __init__(self, conexão, nau, frame, inicio=250, final=45000):
        self.etapa = 'ativação'
        self.conexão = conexão
        self.nau = nau

        self.inicio = inicio
        self.final = final
        self.alvo = None
        self.direção = None

        self.altitude = self.conexão.add_stream(getattr, self.nau.flight(), 'mean_altitude')
        self.apoastro = self.conexão.add_stream(getattr, self.nau.orbit, 'apoapsis_altitude')
        self.booster = self.nau.resources_in_decouple_stage(stage=0, cumulative=True)
        self.combustivel_solido = self.conexão.add_stream(self.booster.amount, 'SolidFuel')

        self.pré_lançamento = False
        self.separação = False
        self.ângulo_de_curva = 0

        self.frame = frame
        self.etapa_label = Label(
            frame,
            width=28,
            anchor='w',
            background='black',
            foreground='white',
            font='times 13 normal',
            borderwidth=3
        )
        self.ângulo_label = Label(
            frame,
            width=28,
            anchor='w',
            background='black',
            foreground='white',
            font='times 13 normal',
            text=f'{self.ângulo_de_curva}º',
            borderwidth=3
        )


    def lançamento(self):
        '''Função interna. Responsavel por ativar o primeiro estagio, e posicionar o foguete no zenith'''

        self.nau.control.sas = False
        self.nau.control.rcs = False
        self.nau.control.throttle = 1.0
        
        if str(self.nau.situation).split('.')[1] == 'pre_launch':
            self.nau.control.activate_next_stage()
        self.nau.auto_pilot.engage()
        self.nau.auto_pilot.target_pitch_and_heading(90, self.direção)

        self.etapa_label['text'] = 'Decolagem'
        self.etapa = 'curva'


    def curva(self):
        '''funcão interna. Responsavel por controlar o foguete de forma precisa durante a curva orbital'''
        
        # curva gravitacional
        if self.inicio < self.altitude() < self.final:
            frac = ((self.altitude() - self.inicio) / (self.final - self.inicio))
            novo_ângulo_de_curva = frac * 90
            if abs(novo_ângulo_de_curva - self.ângulo_de_curva) > 0.5:
                self.ângulo_de_curva = novo_ângulo_de_curva
                self.nau.auto_pilot.target_pitch_and_heading(90 - self.ângulo_de_curva, self.direção)
        
        if self.apoastro() > self.alvo * 0.9:
            self.etapa_label['text'] = 'Fim da curva. Aguardando apoastro'
            
            self.nau.control.throttle = 0.25  
            self.etapa = 'aguardo'


    def calculo(self):
        ut = self.conexão.add_stream(getattr, self.conexão.space_center, 'ut')

        self.etapa_label['text'] = 'Planejando orbita'
        self.etapa = 'planejamento'
        mu = self.nau.orbit.body.gravitational_parameter
        r = self.nau.orbit.apoapsis
        a1 = self.nau.orbit.semi_major_axis
        a2 = r
        v1 = sqrt(mu*((2./r)-(1./a1)))
        v2 = sqrt(mu*((2./r)-(1./a2)))
        delta_v = v2 - v1
        nó = self.nau.control.add_node(ut() + self.nau.orbit.time_to_apoapsis, prograde=delta_v)

        # calculando tempo de queima
        F = self.nau.available_thrust
        Isp = self.nau.specific_impulse * 9.82
        m0 = self.nau.mass
        m1 = m0 / exp(delta_v/Isp)
        quociente_de_vazão = F / Isp
        tempo_de_queima = (m0 - m1) / quociente_de_vazão

        self.nau.auto_pilot.engage()
        self.nau.auto_pilot.reference_frame = nó.reference_frame
        self.nau.auto_pilot.target_direction = (0, 1, 0)

        self.etapa_label['text'] = 'Aguardando a queima'
        self.etapa = ''
    

    def ativar(self):
        try:
            if self.etapa == 'ativação':
                if pages.apoastro_value.get() == '':
                    pages.error_menssage(
                        titulo='Valor invalido',
                        texto='Digite um valor para o apoastro'
                    )

                elif int(pages.apoastro_entry.get()) < 70000:
                    pages.error_menssage(
                        titulo='Valor invalido',
                        texto='Digite uma altitude acima de 70.000 metros'
                    )

                else:
                    if pages.direção_value.get() == '':
                        pages.error_menssage(
                            titulo='Valor invalido',
                            texto='Digite um valor para a direção'
                        )

                    elif 0 > int(pages.direção_value.get()) or int(pages.direção_value.get()) > 360:
                        pages.error_menssage(
                            titulo='Valor invalido',
                            texto='Digite uma direção entre 0 e 360 graus'
                        )

                    else:
                        self.direção = int(pages.direção_value.get())
                        self.alvo = int(pages.apoastro_value.get())

                        self.pré_lançamento = True

        except ValueError:
            pages.error_menssage(
                titulo='Erro de entrada de dados', 
                texto='A caixa de entrada do apoastro apenas recebe valores númericos'
            )
        
        if self.pré_lançamento:                
            # separação do booster
            if pages.check_value2.get():
                if not self.separação:
                    if self.combustivel_solido() < 0.1:
                        self.nau.control.activate_next_stage()
                        self.separação = True
                        self.etapa_label['text'] = ('Separação do Booster')

            if self.etapa == 'ativação':
                pages.apoastro_label.grid_remove()
                pages.apoastro_entry.grid_remove()

                pages.direção_label.grid_remove()
                pages.direção_entry.grid_remove()

                pages.booster_check.grid_remove()
                pages.check_label2.grid_remove()

                self.etapa_label.grid(row=2, column=1, columnspan=2, sticky=W)

                pages.ângulo.grid(row=3, column=0, sticky=W)
                self.ângulo_label.grid(row=3, column=1, columnspan=2, sticky=W)

                pages.liftoff_button['command'] = self.desativar
                pages.liftoff_button['text'] = 'Desativar decolagem'

                self.lançamento()

            elif self.etapa == 'curva':
                self.curva()

            elif self.etapa == 'aguardo':
                if self.apoastro() > self.alvo:
                    self.etapa_label['text'] = 'Apoastro atingido'

                    self.nau.control.sas = True
                    self.nau.control.throttle = 0.0
                    self.nau.auto_pilot.disengage()

                    self.etapa = 'calculo'

            elif self.etapa == 'calculo' and self.altitude() > 70000:
                if pages.check_value1.get():
                    self.calculo()
            
            else:
                pages.ângulo.grid_remove()
                self.ângulo_label.grid_remove()

                pages.liftoff_button['command'] = self.finalizar
                pages.liftoff_button['text'] = 'Finalizar decolagem'
            
        self.ângulo_label['text'] = f'{int(self.ângulo_de_curva)}º de inclinação'
        self.after_id = self.frame.after(1, self.ativar)    

    def desativar(self):
        if self.after_id:
            self.frame.after_cancel(self.after_id)
            self.after_id = None

            self.nau.control.sas = True
            self.nau.control.throttle = 0.0
            self.nau.auto_pilot.disengage()

            self.etapa = 'ativação'
            self.etapa_label['text'] = 'Decolagem desativada'

            self.ângulo_label.grid_remove()
            pages.ângulo.grid_remove()

            pages.apoastro_label.grid(row=3, column=0, sticky=W)
            pages.apoastro_entry.grid(row=3, column=1, columnspan=2, sticky=W)
            pages.apoastro_entry.delete(0,END)
            pages.apoastro_entry.insert(0,'100000')

            pages.direção_label.grid(row=4, column=0, sticky=W)
            pages.direção_entry.grid(row=4, column=1, columnspan=2, sticky=W)
            pages.direção_entry.delete(0, END)
            pages.direção_entry.insert(0,'90')

            pages.booster_check.grid(row=6, column=0, sticky=W + E)
            pages.check_label2.grid(row=6, column=0, columnspan=3)

            pages.liftoff_button['command'] = self.ativar
            pages.liftoff_button['text'] = 'Decolagem'


    def finalizar(self):
        if self.after_id:
            self.frame.after_cancel(self.after_id)
            self.after_id = None
            
            self.nau.control.sas = True

            self.nau.control.throttle = 0.0
            self.nau.auto_pilot.disengage()

            self.etapa = 'finalizado'
            self.etapa_label['text'] = 'lançamento completo'
