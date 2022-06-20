from tkinter import * 

  # ================================================|Error window|========================================================
def error_menssage(titulo='Menssagem de erro', texto='Erro'):
    error_window = Tk()
    error_window.title(titulo)
    error_window.geometry('+300+300')
    error_window.maxsize(445, 100)
    error_window.iconbitmap('KSP.ico')
        
    error_label = Label(error_window, borderwidth=20, font='Arial 11', text=texto).pack()

  # ===================================================|Head|============================================================

window = Tk()
window.geometry('311x600+0+0')
window.minsize(311, 300)
window.maxsize(311, 650)
window.title('KRpc')
window.iconbitmap('KSP.ico')
window['background'] = 'black'

  # ===================================================|Body|============================================================

h1 = Label(
    window,
    text=' KSP-KRPC   ',
    background='#1F2328',
    foreground='white',
    font='Times 44 normal'
)
h1.pack()

conexão_button = Button(
    window,
    width=28,
    text='Conectar',
    borderwidth=0,
    font='Times 15 bold',
    background='black',
    foreground='white',
    activebackground='#1F2328',
    activeforeground='white',
)
conexão_button.pack()

  # ==============================================|Main Frame|========================================================

mainFrame = Frame(
    window,
    background='black'
)
mainFrame.pack()

missão = Label(
  mainFrame,
  background='black',
  width=7,
  foreground='red',
  anchor=E,
  font='times 13 normal',
  borderwidth=3,
  text='Missão'
)

nome = Label(
  mainFrame,
  background='black',
  foreground='white',
  font='times 13 normal',
  borderwidth=3,
)

linha = Frame(
  mainFrame,
  background='#1F2328',
  width=200,
  height=1,
  borderwidth=15
)

liftoff_button = Button(
  mainFrame,
  text='Decolagem',
  borderwidth=0,
  font='Times 15 bold',
  background='#1F2328',
  foreground='white',
  activebackground='grey',
  activeforeground='white',
)

check_value1 = BooleanVar() 

calculo_check = Checkbutton(
  mainFrame,
  background='black',
  activebackground='black',
  borderwidth=0,
  relief='flat',
  pady=10,
  var=check_value1
)

check_label1 = Label(
  mainFrame,
  background='black',
  foreground='white',
  font='times 11 normal',
  text='Calcular orbita automaticamente            '
)

check_value2 = BooleanVar() 

booster_check = Checkbutton(
  mainFrame,
  background='black',
  activebackground='black',
  borderwidth=0,
  relief='flat',
  var=check_value2
)

check_label2 = Label(
  mainFrame,
  background='black',
  foreground='white',
  font='times 11 normal',
  text='Combustivel sólido                                 '
)

etapa = Label(
  mainFrame,
  background='black',
  width=7,
  foreground='red',
  anchor=E,
  font='times 13 normal',
  borderwidth=3,
  text='Estagio'
)

ângulo = Label(
  mainFrame,
  background='black',
  width=7,
  foreground='red',
  anchor=E,
  font='times 13 normal',
  borderwidth=3,
  text='Ângulo'
)

apoastro_label = Label(
  mainFrame,
  background='black',
  width=7,
  foreground='red',
  anchor=E,
  font='times 13 normal',
  borderwidth=3,
  text='Apoastro'
)

apoastro_value = StringVar()

apoastro_entry = Entry(
  mainFrame,
  textvariable=apoastro_value,
  font='helvetica 12',
  background='black',
  foreground='white',
  relief='flat',
  insertbackground='white'
)

direção_label = Label(
  mainFrame,
  background='black',
  width=7,
  foreground='red',
  anchor=E,
  font='times 13 normal',
  borderwidth=3,
  text='Direção'
)

direção_value = StringVar()

direção_entry = Entry(
  mainFrame,
  textvariable=direção_value,
  font='helvetica 12',
  background='black',
  foreground='white',
  relief='flat',
  insertbackground='white'
)
