from functools import partial
from tkinter import *
import manobra
import krpc
import pages


def conectar():
  try:
    conexão = krpc.connect('KSP-KRPC')

    try:
      nau = conexão.space_center.active_vessel

    except krpc.error.RPCError:
      pages.error_menssage(texto='Nenhum veiculo encontrado')

    else: 
      pages.conexão_button.destroy()

      decolagem = manobra.Decolagem(conexão, nau, pages.mainFrame)
      decolagem.etapa_label['text'] = 'Coneção estabelecida'   

      pages.nome['text'] = str(nau.name)
      pages.missão.grid(row=0, column=0, sticky=W)
      pages.nome.grid(row=0, column=1, columnspan=2, sticky=W)

      pages.linha.grid(row=1, column=0, columnspan=2, sticky=E)
      
      pages.etapa.grid(row=2, column=0, sticky=W)
      decolagem.etapa_label.grid(row=2, column=1, columnspan=2, sticky=W)

      pages.apoastro_label.grid(row=3, column=0, sticky=W)
      pages.apoastro_entry.grid(row=3, column=1, columnspan=2, sticky=W)
      pages.apoastro_entry.insert(0,'100000')

      pages.direção_label.grid(row=4, column=0, sticky=W)
      pages.direção_entry.grid(row=4, column=1, columnspan=2, sticky=W)
      pages.direção_entry.insert(0,'90')

      pages.check_value1.set(True)
      pages.calculo_check.grid(row=5, column=0, sticky=W + E)
      pages.check_label1.grid(row=5, column=0, columnspan=3)

      pages.check_value2.set(True)
      pages.booster_check.grid(row=6, column=0, sticky=W + E)
      pages.check_label2.grid(row=6, column=0, columnspan=3)
      
      pages.liftoff_button['command'] = partial(decolagem.ativar)
      pages.liftoff_button.grid(row=7, column=0, columnspan=3, sticky=W + E)
     
  except ConnectionRefusedError:
    pages.error_menssage(texto='O centro espacial não foi encontrado')


pages.conexão_button['command'] = conectar
pages.window.mainloop()
