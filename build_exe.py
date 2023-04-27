import os
import sys
import subprocess
import shutil

def main():
  # Pegar o caminho completo deste arquivo e extrair o path
  root_dir = os.path.dirname(os.path.realpath(__file__))

  ws_dir = "c:\\_tmp\\build_exe"
  if not os.path.exists(ws_dir):
    os.makedirs(ws_dir)

  # Define o caminho para gerar o executável
  dist_dir = os.path.join(root_dir, "exe\\32")

  # Define o caminho do arquivo .py que será compilado
  py_dir = os.path.join(root_dir, "source")

  # Verifica se o arquivo foi passado como argumento
  # if len(sys.argv) < 2:
  #   print("Nenhum arquivo .py foi passado como argumento!")
  #   return
   
  # Pega o nome do arquivo .py que será compilado
  #script_name = sys.argv[1]
  # Para testar, descomente a linha abaixo
  script_name = 'testes_status.py'

  # Copia o arquivo .py para o diretório ws_dir
  shutil.copy(os.path.join(py_dir, script_name), os.path.join(ws_dir, script_name))

  # Verifica se o arquivo passado como argumento existe
  script_name = os.path.join(ws_dir, script_name)

  if not os.path.exists(script_name):
    print("O arquivo passado como argumento não existe!")
    return

  # Define o comando para compilar o arquivo .py
  cmd = f"pyinstaller --onefile --distpath {ws_dir} {script_name}"

  # Executa o comando
  subprocess.run(cmd, shell=False)

  # Se o diretório não existir, cria
  if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

  # Copia o arquivo .exe gerado no ws_dir para o dist_dir
  exe_name = os.path.join(ws_dir, script_name.split('\\')[-1].split('.')[0] + '.exe')
  if os.path.exists(exe_name):
    shutil.copy(exe_name, os.path.join(dist_dir, exe_name.split('\\')[-1]))
  
  # Remove o diretório ws_dir
  if os.path.exists(ws_dir):
    shutil.rmtree(ws_dir)

  print("Executável gerado com sucesso!")
  
if __name__ == "__main__":
  main()