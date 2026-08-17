
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from playsound import playsound


def calcular_imc():
        peso = float(entry_peso.get().replace(',', '.'))
        altura = float(entry_altura.get().replace(',', '.'))
        
        imc = peso / (altura ** 2)
        
        if imc < 18.5:
            classificacao = "ABAIXO DE PESO"
        elif imc < 25:
              classificacao = "PESO NORMAL"
        elif imc < 30:
            classificacao = "SOBREPESO"
        else:
            classificacao = "OBESIDADE"
        
        label_resultado.config(text=f"IMC: {imc:.2f} ({classificacao})")

tocar_musica = True

def tocar_audio_loop(caminho):
    while tocar_musica:
        playsound(caminho)

def atualizar_video():
    ret, frame = cap.read()

    # Se o vídeo chegar ao fim, reinicia do primeiro quadro (loop)
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    if ret:
        # Converte de BGR (OpenCV) para RGB (Pillow)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Redimensiona o quadro do vídeo
        imagem = Image.fromarray(frame_rgb)
        imagem_redimensionada = imagem.resize((150, 150))
        
        # Converte para formato Tkinter
        photo = ImageTk.PhotoImage(image=imagem_redimensionada)
        
        label_video.config(image=photo)
        label_video.image = photo

    # Executa esta função novamente após 30 milissegundos (~33 fps)
    janela.after(30, atualizar_video)    

def ao_fechar():
    global tocar_musica
    tocar_musica = False  # Para o loop da música
    if 'cap' in globals() and cap.isOpened():
        cap.release()
    janela.destroy()  

# Configuração da Janela Principal
janela = tk.Tk()
janela.title("RATA DO IMC")
janela.geometry("680x468")
janela.resizable(False, False)


#tentando colocar a imagem de fundo
caminho_video = "c:/Users/Noll de Oliveira/Desktop/DAIANE IMC/video.mp4"  # Coloque o vídeo na mesma pasta do script (ou use caminho completo)

label_video = tk.Label(janela)
label_video.pack(pady=15)

if os.path.exists(caminho_video):
    cap = cv2.VideoCapture(caminho_video)
    atualizar_video()  # Inicia o loop do vídeo
else:
    label_video.config(text=f"Vídeo não localizado:\n{os.path.abspath(caminho_video)}", fg="red")
# Rótulos e Campos de Entrada
tk.Label(janela, text="Peso (kg):", font=("Arial", 10)).pack(pady=5)
entry_peso = tk.Entry(janela, font=("Arial", 10), justify="center")
entry_peso.pack(pady=5)

tk.Label(janela, text="Altura (m, ex: 1.75):", font=("Arial", 10)).pack(pady=5)
entry_altura = tk.Entry(janela, font=("Arial", 10), justify="center")
entry_altura.pack(pady=5)

# Botão de Calcular
btn_calcular = tk.Button(janela, text="Calcular", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=calcular_imc)
btn_calcular.pack(pady=15)

# Rótulo de Resultado
label_resultado = tk.Label(janela, text="", font=("Arial", 11, "bold"))
label_resultado.pack(pady=5)

janela.mainloop()
