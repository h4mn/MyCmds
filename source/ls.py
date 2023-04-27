# script que emula no windows o comando ls do linux
import os

def main():
  for item in os.listdir('.'):
    print(item)

if __name__ == '__main__':
  main()
