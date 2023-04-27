import tkinter as tk
from tkinter import ttk
import re
import time
import math

# 
# Classe do componente ProgressCircular
# 
class ProgressCircular(tk.Canvas):
  def __init__(self, parent, size=100, thickness=0, progress=0, countdown_value=0, *args, **kwargs):
    tk.Canvas.__init__(self, parent, width=size, height=size, highlightthickness=0, *args, **kwargs, )
    self.size = size
    self.thickness = thickness
    self.progress = progress
    self.countdown_value = countdown_value
    self.draw_progressbar()
    
  def draw_progressbar(self):
    self.delete("progress")
    angle = (self.progress / 100) * 360
    radians = math.radians(90 - angle)
    x = self.size / 2 + (self.size / 2 - self.thickness / 2) * math.cos(radians)
    y = self.size / 2 - (self.size / 2 - self.thickness / 2) * math.sin(radians)

    self.create_arc(
        self.thickness / 2,
        self.thickness / 2,
        self.size - self.thickness / 2,
        self.size - self.thickness / 2,
        start=90,
        extent=-angle,
        width=0,
        fill="#20a842",
        tags="progress",
    )

  def set_progress(self, progress):
    self.progress = progress
    self.draw_progressbar()

  def set_countdown_value(self, countdown_value):
    self.countdown_value = countdown_value


#
# Classe do aplicativo
#
class Aplicativo:
  def __init__(self, janela):
    # Define o título da janela
    self.tarefa_em_progresso = ""

    # Criação do frame
    self.frame = tk.Frame(janela)
    self.frame.pack(fill=tk.BOTH, expand=True)

    # Criação do componente ProgressCircular
    self.circular_progressbar = ProgressCircular(self.frame, size=100, thickness=10, progress=0, countdown_value=0)
    self.circular_progressbar.grid(row=0, column=0, rowspan=2, sticky=tk.EW, padx=5)

    # Criação do rótulo
    self.rotulo = tk.Label(self.frame, text="")
    self.rotulo.grid(row=0, column=1, sticky=tk.EW, padx=5)

    # Criação da barra de progresso
    self.barra_progresso = ttk.Progressbar(self.frame, mode="determinate", length=100)
    self.barra_progresso.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

    # Define o tamanho da coluna 1
    self.frame.columnconfigure(1, minsize=480)

    # Atualize o progresso circular
    self.update_countdown()

    # Atualize a barra de progresso
    self.atualizar_arquivo()

  # Função para ler o arquivo
  def ler_arquivo(self):
    arquivo = r"Z:\Backup\_tmp\_md\tarefas\3027901.md"

    # Monitoramento dos Testes: Padrão para encontrar os caracteres "[x]" e "[ ]"
    #tarefa_em_progresso = "Revisão dos Links Dinamicos"
    #padrao_pendente = r"\[\s\]"
    #padrao_realizado = r"\[x\]"
    # Monitoramento dos RelDinTpLkp_ServicoProduto: Padrão para encontrar "\] Produto" e "\] Produto [^7]"
    tarefa_em_progresso = "Revisão dos RelDinTpLkp_ServicoProduto"
    padrao_pendente = r"\]\sProduto\n"
    padrao_realizado = r"\]\sProduto\s\[\^7\]\n"

    # Define o título da janela
    janela.title(tarefa_em_progresso)

    qtd_char1 = 0
    qtd_char2 = 0

    try:
      with open(arquivo, "r") as f:
        conteudo = f.read()
        qtd_char1 = len(re.findall(padrao_realizado, conteudo))
        qtd_char2 = len(re.findall(padrao_pendente, conteudo))

    except FileNotFoundError:
      print(f"Arquivo {arquivo} não encontrado.")

    total = qtd_char1 + qtd_char2
    return total, qtd_char1, qtd_char2

  # Função para atualizar a barra de progresso
  def atualizar_arquivo(self):
    total, qtd_char1, qtd_char2 = self.ler_arquivo()

    # Atualize a barra de progresso
    self.barra_progresso["value"] = qtd_char1
    self.barra_progresso["maximum"] = total

    progresso_percentual = (qtd_char1 / total) * 100 if total != 0 else 0
    self.rotulo.config(
      text=f"Verificados: {qtd_char1}, Restantes: {qtd_char2}, Total: {total}, Progresso: {progresso_percentual:.1f}%"
    )

    # Reagende a função para executar novamente em 1 minuto (60000 ms)
    #janela.after(60000, self.atualizar_arquivo)
  
  # Função para redimensionar a barra de progresso
  def on_resize(self, event):
    width = event.width
    self.barra_progresso.configure(length=width-110)
    self.rotulo.configure(wraplength=width-110)

  def update_countdown(self):
    countdown_value = self.circular_progressbar.countdown_value - 1
    if countdown_value < 0:
      countdown_value = 60

    progress = (60 - countdown_value) * (100 / 60)
    self.circular_progressbar.set_countdown_value(countdown_value)
    self.circular_progressbar.set_progress(progress)

    if countdown_value == 0:
      self.atualizar_arquivo()

    janela.after(1000, self.update_countdown)


#
# Função principal
#
if __name__ == "__main__":
    janela = tk.Tk()

    # Define a largura da janela
    #janela.configure(width=480)
    janela.geometry("640x100+100+900")

    janela.resizable(True, False)

    # Define a toplevel da janela
    janela.attributes("-topmost", True)
    janela.attributes("-transparentcolor", "white") # Defina a cor transparente para a janela

    app = Aplicativo(janela)

    # Vincula a função on_resize ao evento de redimensionamento da janela
    janela.bind("<Configure>", app.on_resize)

    janela.mainloop()
