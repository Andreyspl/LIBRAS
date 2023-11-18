# Importar o módulo App do Kivy
from kivy.app import App

# Importar os widgets e layouts do Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
import mediapipe as mp
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2

# Definir uma classe que herda de Image e que usa o MediaPipe para capturar e atualizar o vídeo da câmera
class CameraMP(Image):

    # Definir um método de inicialização que não recebe nenhum argumento
    def __init__(self, **kwargs):
        # Chamar o método de inicialização da classe pai
        super(CameraMP, self).__init__(**kwargs)
        # Criar um objeto de captura de vídeo com o índice 0 da câmera
        self.capture = cv2.VideoCapture(0)
        # Criar um objeto de solução de mãos do MediaPipe
        self.hands = mp.solutions.hands.Hands()
        # Criar um objeto de desenho do MediaPipe
        self.drawer = mp.solutions.drawing_utils
        # Definir uma função de callback que será executada a cada quadro do vídeo
        self.callback = self.update
        # Agendar a execução da função de callback a cada 0.1 segundos
        Clock.schedule_interval(self.callback, 0.1)

    # Definir um método que atualiza o vídeo da câmera
    def update(self, dt):
        # Ler um quadro do vídeo da câmera
        ret, frame = self.capture.read()
        # Verificar se o quadro foi lido corretamente
        if ret:
            # Converter o quadro de BGR para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Passar o quadro para o objeto de solução de mãos
            results = self.hands.process(frame)
            # Verificar se há alguma mão detectada
            if results.multi_hand_landmarks:
                # Desenhar as anotações das mãos no quadro
                for hand_landmarks in results.multi_hand_landmarks:
                    self.drawer.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            # Converter o quadro de RGB para BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)

            # Redimensionar o quadro para o tamanho do widget
            frame = cv2.resize(frame, (int(self.width), int(self.height)))
            # Converter o quadro para um buffer de bytes
            buffer = frame.tostring()
            # Atualizar a fonte de imagem do widget com o buffer de bytes
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            self.texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

# Definir uma classe que herda de App
class MyApp(App):

    # Definir um método que retorna o widget raiz do aplicativo
    def build(self):
        # Criar um layout BoxLayout com orientação vertical
        box = BoxLayout(orientation="vertical")
        
        # Criar um layout GridLayout com 2 colunas e 1 linha
        grid = GridLayout(cols=2, rows=1)
        
        # Criar um widget Button com o texto "Iniciar/Parar"
        button = Button(text="Iniciar/Parar")
        
        # Criar um widget CameraMP sem nenhum argumento
        camera = CameraMP()
        
        # Criar um widget Label com o texto "Tradução"
        label = Label(text="Tradução")
        
        # Criar um widget Popup com o título "Menu"
        popup = Popup(title="Menu")
        
        # Criar um layout BoxLayout com orientação vertical
        menu = BoxLayout(orientation="vertical")
        
        # Criar um widget Button com o texto "Configurações"
        settings = Button(text="Configurações")
        
        # Criar um widget Button com o texto "Ajuda"
        help = Button(text="Ajuda")
        
        # Definir uma função de callback para o botão de configurações
        def settings_callback(instance):
            # Imprimir uma mensagem no terminal
            print("Você clicou no botão de configurações")
            # Fechar o popup
            popup.dismiss()
        
        # Definir uma função de callback para o botão de ajuda
        def help_callback(instance):
            # Imprimir uma mensagem no terminal
            print("Você clicou no botão de ajuda")
            # Fechar o popup
            popup.dismiss()
        
        # Associar as funções de callback aos botões
        settings.bind(on_release=settings_callback)
        help.bind(on_release=help_callback)
        
        # Adicionar os botões ao layout do menu
        menu.add_widget(settings)
        menu.add_widget(help)
        
        # Definir o conteúdo do popup como o layout do menu
        popup.content = menu
        
        # Associar o popup ao botão que vai chamá-lo
        popup.caller = button
        
        # Definir uma função de callback para o botão que vai chamar o popup
        def popup_callback(instance):
            # Abrir o popup
            popup.open()
        
        # Associar a função de callback ao botão que vai chamar o popup
        button.bind(on_release=popup_callback)
        
        # Adicionar o botão e a câmera ao grid
        grid.add_widget(button)
        grid.add_widget(camera)
        
        # Adicionar o grid, o label e o menu ao box
        box.add_widget(grid)
        box.add_widget(label)
        
        # Retornar o layout box
        return box

# Criar uma instância da classe MyApp
app = MyApp()

# Executar o aplicativo
app.run()