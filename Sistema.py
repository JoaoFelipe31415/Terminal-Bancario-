from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.app import App 
from kivy.lang import Builder
Builder.load_file('my.kv')
user = None
        
class FirstWindow(Screen):
    def entrar(self):
        global user
        userx = self.ids.usuario.text 
        chave = self.ids.senha.text

        usuarios = open('usuarios.txt','r')
        lista = usuarios.readlines()
        for elemento in lista:
            analisado = elemento.split(',')
            usuario_atual = analisado[1]
            senha_atual = analisado[2]
            if userx == usuario_atual:
                if chave == senha_atual:
                    self.manager.transition.direction = 'left'
                    self.manager.current = 'second'
                    user = analisado
                    break
                else:
                    break     
                             
            
        usuarios.close()

class SecondWindow(Screen):
    global user
    __controle = True
    def on_enter(self):
        
        arquivo = open('usuarios.txt','r')
        lista = arquivo.readlines()

        pessoa = lista[int(user[0])-1]
        pessoa = pessoa.split(',')
        saldo = pessoa[3]
        
        arquivo.close()
        
        self.ids.mensagem.text = f'Olá, {user[1]}!'
        
        if user[4][:-1] == 'BR':
            self.ids.valor.text = f'R${saldo}'
        else:
            self.ids.valor.text = f'US${saldo}'
    
    def ocultar(self):
        if SecondWindow.__controle == True:
            self.ids.mostrar.text = 'Revelar'
            self.ids.valor.text = ''
            SecondWindow.__controle = False
        else:
            self.ids.mostrar.text = 'Ocultar'
            if user[4][:-1] == 'BR':
                self.ids.valor.text = f'R${user[3]}'
            else:
                self.ids.valor.text = f'US${user[3]}'
            SecondWindow.__controle = True
    
    
    def transferir(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'quarta'
        
    def deposito(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'quinta'





class TerceiraWindow(Screen):
    def cadastro(self):
        nome = self.ids.usuario_cadastro.text 
        senha = self.ids.senha_cadastro.text
        nacionalidade = self.ids.nacionalidade_cadastro.text
        
        if nome == '' or senha == '' or nacionalidade == '':
            return 0
        
        controle = True
        usuarios = open('usuarios.txt','r+')
        cadastrados = usuarios.readlines()
        for usuario in cadastrados:
            nome_usuario = usuario.split(',')[1]
            if nome == nome_usuario:
                self.ids.usuario_cadastro.text = ''
                self.ids.senha_cadastro.text = ''
                self.ids.nacionalidade_cadastro.text = ''
                self.ids.usuario_cadastro.hint_text = 'Usuário já registrado, insira outro'
                controle = False
                break
        if controle:
            id = len(cadastrados) + 1
            resultado = f'0{id},{nome},{senha},0,{nacionalidade}\n'
            usuarios.write(resultado)
            usuarios.close()
            self.manager.transition.direction = 'right'
            self.manager.current = 'first'
                
    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'first'
    

class QuartaWindow(Screen):
    global user
    
    def on_enter(self):
        if user[4][:-1] == 'USA':
            self.ids.aviso.text = f'{user[1]}, saldo em conta US${user[3]}'
        else:
            self.ids.aviso.text = f'{user[1]}, saldo em conta R${user[3]}'
    
    def transferir(self):
        
        global user

        valor = float(self.ids.valor_transferido.text)
        pessoa_destino = self.ids.pessoa_transferida.text

        arquivo = open('usuarios.txt','r')
        usuarios = arquivo.readlines()

        

        for elemento in usuarios:
            dados = elemento.split(',')
            usuario_nome = dados[1]
            usuario_saldo = float(dados[3])
            usuario_nacionalidade = dados[4][:-1]
            
            if pessoa_destino == user[1]:
                return 0

            if float(user[3]) < valor:
                return 0

            if usuario_nome == pessoa_destino:
                
                if usuario_nacionalidade == user[4][:-1]:
                    temp = valor
                else: 
                    if user[4][:-1] == 'BR':
                        temp = valor/5
                    else:
                        temp = 5 * valor
                
                usuario_saldo += temp
                
                resultado = f'{dados[0]},{usuario_nome},{dados[2]},{usuario_saldo},{dados[4]}'
                
                index = usuarios.index(elemento)
                
                usuarios[index] = resultado

                novo_saldo = float(user[3]) - valor
                
                
                
                novo_resultado = f'{user[0]},{user[1]},{user[2]},{novo_saldo},{user[4]}'

                user = novo_resultado.split(',')

                usuarios[int(user[0])-1] = novo_resultado

                self.ids.valor_transferido.text = ''
                self.ids.pessoa_transferida.text = ''
                
                if user[4][:-1] == 'USA':
                    self.ids.aviso.text = f'{user[1]}, saldo em conta US${user[3]}'
                else:
                    self.ids.aviso.text = f'{user[1]}, saldo em conta R${user[3]}'

                break
        
        arquivo.close()

        arquivo = open("usuarios.txt",'w')
        for elemento in usuarios:
            arquivo.write(elemento)
        
        arquivo.close()
                
    
    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'


class QuintaWindow(Screen):

    global user    
    
    def voltar(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'
    
    def depositar(self):
        
        global user
        
        if self.ids.valor_deposito.text == "":
            return 0

        
        valor = float(self.ids.valor_deposito.text)
        
        
        arquivo = open('usuarios.txt','r+')
        cadastrados = arquivo.readlines()
        
        pessoa_atual = cadastrados[int(user[0])-1]
        pessoa_atual = pessoa_atual.split(',')
        
        for elemento in cadastrados:
            dados = elemento.split(',')
            pessoa_nome = dados[1]
            if pessoa_nome == pessoa_atual[1]:
                dados[3] = str(float(dados[3]) + valor)
                user = dados
                resultado = ','.join(dados)
                cadastrados[int(dados[0])-1] = resultado
                break                
        self.ids.valor_deposito.text = ''
        
        arquivo.close()
        arquivo = open("usuarios.txt",'w')
        
        for elemento in cadastrados:
            arquivo.write(elemento)
        arquivo.close()
 

class Sistema(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstWindow())
        sm.add_widget(SecondWindow())
        sm.add_widget(TerceiraWindow())
        sm.add_widget(QuartaWindow())
        sm.add_widget(QuintaWindow())
        return sm
    


Sistema().run()
