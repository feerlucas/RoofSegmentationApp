# Importação de bibliotecas necessárias
import cv2  # Para processamento de imagem
import numpy as np  # Para manipulação de matrizes
from tkinter import filedialog  # Para caixa de diálogo de arquivo
from tkinter import Tk, Label, Button  # Para interface gráfica
import os  # Para manipulação de sistema de arquivos
import subprocess  # Para execução de comandos do sistema

# Definição da classe principal da aplicação
class RoofSegmentationApp:
    # Método de inicialização
    def __init__(self, master):
        self.master = master
        master.title("Segmentação de Telhados")  # Define o título da janela
        master.state('zoomed')  # Abre a janela maximizada

        # Elementos da interface gráfica
        self.label = Label(master, text="Selecione uma imagem aérea")
        self.label.pack()

        self.select_button = Button(master, text="Selecionar Imagem", command=self.select_image)
        self.select_button.pack()

        self.open_folder_button = Button(master, text="Abrir Pasta de Imagens", command=self.open_folder)
        self.open_folder_button.pack()

        self.quit_button = Button(master, text="Sair", command=master.quit)  # Botão para fechar a aplicação
        self.quit_button.pack()

        self.credits_label = Label(master, text="")  # Créditos
        self.credits_label.pack()

    # Método para selecionar a imagem
    def select_image(self):
        file_path = filedialog.askopenfilename()  # Abre a caixa de diálogo para seleção de arquivo
        if file_path:
            self.segment_roofs(file_path)  # Chama o método de segmentação

    # Método para segmentação de telhados
    def segment_roofs(self, image_path):
        # Determina o caminho da área de trabalho dependendo do sistema operacional
        if os.name == 'posix':
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        # Cria a pasta 'roofs' na área de trabalho
        save_folder = os.path.join(desktop, 'roofs')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Leitura e processamento da imagem
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Pinta os contornos de verde
        cv2.drawContours(img, contours, -1, (0, 255, 0), -1)

        # Salva a imagem na pasta 'roofs'
        cv2.imwrite(os.path.join(save_folder, 'segmented_roofs.png'), img)
        self.label.config(text=f"Segmentação completa. Imagem salva em {save_folder}")

    # Método para abrir a pasta 'roofs'
    def open_folder(self):
        # Determina o caminho da área de trabalho dependendo do sistema operacional
        if os.name == 'posix':
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        else:
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        save_folder = os.path.join(desktop, 'roofs')

        # Abre a pasta usando o explorador de arquivos do sistema
        subprocess.run(['open', save_folder]) if os.name == 'posix' else subprocess.run(['explorer', save_folder])

# Inicializa a aplicação
if __name__ == "__main__":
    root = Tk()
    app = RoofSegmentationApp(root)
    root.mainloop()
