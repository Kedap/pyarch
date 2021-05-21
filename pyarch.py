#!/bin/python3
# Script de instalacion en python para arch
# https://github.com/kedap/pyarch

import os, time
from os import system
from colorama import Fore, init, Style
init(autoreset=True)

# Funciones escenciales
def error(msg):
	print(Fore.RED + "[-] " + msg)

def info(msg):
	print(Fore.CYAN + "[*] " + msg)

def advertencia(msg):
	print(Fore.YELLOW * "[!] " + msg)
def pregunta(pregunta):
	opcion = input(Fore.YELLOW + pregunta + " [S/n] ")
	print(Style.RESET_ALL)
	if opcion == "S" or opcion == "s":
		return True
	else:
		return False

def subtitulo(titulo, subtitulo):
	print("\n\nPyArch > " + titulo + " > " + subtitulo +"\n\n")

def banner_titulo(titulo):
	system('clear')
	print(Fore.BLUE + "." * 50)
	print("\t--==[ PyArch: " + titulo + " ]==--")
	print(Fore.BLUE + "." * 50)
	print("\n\nPyArch > " + titulo + "\n\n")

# Procesos de instalacion
def particion_de_discos():
	banner_titulo("Particion de discos")
	if os.getuid() != 0:
		error("Necesitas ser root para instalar archlinux")
		exit(1)
	print("Listando discos...")
	system("lsblk")
	disco = input("Cual es el disco que quieres particionar? (/dev/xxx) ")
	print("Seleccionando el disco " + disco)
	print("Se debe de particionar de manera manual, pero para ello toma la siguiente guia")
	print("\nSeleciona una opcion segun tu instalacion")
	print("\n1> Instalacion de todo el disco (opcion recomendada)")
	print("2> Instalacion de todo el disco (opcion no tan recomendada)")
	print("3> Instalacion en una particion sin swap (dual boot con otro OS [Windows/MacOS]")
	print("4> ¡No quiero tu guia, solo quiero particionar ya! (Ya tienes una idea de las particiones)")
	opcion = input("\n Opcion: ")

	# Cambiando entre las opciones
	if opcion == "1":
		subtitulo("Particion de discos", "Guia de instalacion disco completo")
		print("/dev/xxx1\tBooteable\tMas de 260Mib (particion boot)\tDe tipo linux")
		print("/dev/xxx2\tNo Booteable\tMas de 512Mib (particion swap)\tDe tipo swap linux")
		print("/dev/xxx3\tNo Booteable\tDepende de su gusto (particion root)\tDe tipo linux")
		print("/dev/xxx4\tNo Booteable\tDepende de su gusto (particion home)\tDe tipo linux")
		input("\nEnter cuando ya lo tengas claro ")
	elif opcion == "2":
		subtitulo("Particion de discos", "Guia de instalacion disco completo")
		print("/dev/xxx1\tBooteable\tMas de 260Mib (parcion boot)\tDe tipo linux")
		print("/dev/xxx2\tNo Booteable\tDepende de su gusto (particion de instalacion archlinux)\tDe tipo linux")
		input("\nEnter cuando ya lo tengas claro ")
	elif opcion == "3":
		subtitulo("Particion de discos", "Guia de instalacion disco completo")
		print("/dev/xxxN\tNo Booteable\tDepende de su gusto (particion de instalacion archlinux)\tDe tipo linux")
		input("\nEnter cuando ya lo tengas claro ")
	elif opcion == "4":
		info("Cargando el particionador de discos...")
	else:
		error("\nIntenta de nuevo :)")
		time.sleep(1)
		particion_de_discos()
	system("cfdisk " + disco)
	subtitulo("Particion de discos", "Seleccionando particiones")
	particion = ["Hola", "Hola", "Hola", "Hola"]
	particion[0] = input("Particion boot [/dev/xxx1] ")
	particion_swap = pregunta("Vas a utilizar una particion swap?")
	if particion_swap == True:
		particion[1] = input("Particion swap ")
	else:
		info("No se va a utilizar una particion swap...")
		particion[1] = False
	particion[2] = input("Particion root ")
	particion_home = pregunta("Vas a utilizar una particion para home?")
	if particion_home == True:
		particion[3] = input("Particion home ")
	else:
		info("No se va a utilizar una particion home...")
		particion[3] = False
	return particion


tabla_de_particion = particion_de_discos()