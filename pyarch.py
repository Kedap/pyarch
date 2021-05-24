#!/bin/python3
# Script de instalacion en python para arch y solo sistemas efi
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
	particion = ["boot", "swap", "root", "home"]
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

	subtitulo("Particion de discos", "Verificacion de particiones")
	print("Es correcta la tabla de particiones?")
	print(particion[0] + "\tBooteable\tMas de 260Mib (particion boot)\tDe tipo linux")
	if particion[1] == False:
		print("No Seleccionada (no se va a usar)\tNo Booteable\tMas de 512Mib (particion swap)\tDe tipo swap linux")
	else:
		print(particion[1] + "\tNo Booteable\tMas de 512Mib (particion swap)\tDe tipo swap linux")
	if particion[3] == False:
		print(particion[2] + "\tNo Booteable\tDepende de su gusto (particion root y home)\tDe tipo linux")
	else:
		print(particion[2] + "\tNo Booteable\tDepende de su gusto (particion root)\tDe tipo linux")
		print(particion[3] + "\tNo Booteable\tDepende de su gusto (particion home)\tDe tipo linux")
	continuar = pregunta("Estas seguro de continuar con este esquema de particiones?")
	if continuar == True:
		return particion
	else:
		error("Ok... Abortando :(")
		exit(1)

def formateo_partciones(particiones_arr):
	banner_titulo("Formateo de partciones")
	info("Iniciando el formateo de partciones...")
	info("Formateando en ext4...")
	dual_boot = pregunta("Se va a instalar junto a otro OS? (dual boot)")
	if dual_boot == True:
		info("No se va a formatear la partcion boot")
	else:
		info("Fomartenado ext4 a la partcion boot [" + particiones_arr[0] + "]...")
		system("mkfs.ext4 " + particiones_arr[0])
	if particiones_arr[1] == False:
		info("No se creara un particion swap, puesto a que no se creo.")
	else:
		info("Creando partcion swaaap en la partcion " + particiones_arr[1])
		system("mkswap " + particiones_arr[1])
		info("Activando la particion swap")
		system("swapon " + particiones_arr[1])
	if particiones_arr[3] == False:
		info("Se utilizara una particion para root y home...")
		info("Formatiando la partcion con ext4 " + particiones_arr[2])
		system("mkfs.ext4 " + particiones_arr[2])
	else:
		info("Utilizando la particion " + particiones_arr[2] + " Para root")
		info("Utilizando la particion " + particiones_arr[3] + " Para home")
		info("Formatiando la partcion " + particiones_arr[2])
		system("mkfs.ext4 " + particiones_arr[2])
		info("Formatiando la particion " + particiones_arr[3])
		system("mkfs.ext4 " + particiones_arr[3])
	info("El formateo de partciones se ejecuto de manera correcta!")

def montado_partciones(particiones_arr):
	banner_titulo("Montando particiones")
	info("Montando partciones...")
	info("Montando la partcion efi")
	system("mkdir -p /mnt/efi")
	system("mount " + particiones_arr[0] + " /mnt/efi")
	if particiones_arr[3] == False:
		info("Montando la partcion root...")
		system("mount " + particiones_arr[2] + " /mnt")
	else:
		info("Montando la partcion home...")
		system("mkdir -p /mnt/home")
		system("mount " + particiones_arr[3] + " /mnt/home")
		info("Montando la partcion root...")
		system("mount " + particiones_arr[2] + " /mnt")
	info("La montancion de partciiones a sido correcta")

def descarga():
	banner_titulo("Descarga de archlinux")
	network = pregunta("Quieres instalar networkmanager?")
	if network == True:
		system("pacstrap /mnt base linux linux-firmware vim networkmanager grub")
	else:
		system("pacstrap /mnt base linux linux-firmware vim grub")

def idioma():
	banner_titulo("Generando locales")
	print("Elimina tu idioma y pais")
	input("Enter cuando estes listo")
	system("vim /mnt/etc/locale.gen")
	locale = input("Ingresa tu nombre e idioma [es_ES.UTF-8]")
	system("echo 'LANG=" + locale + "' > /mnt/etc/locale.conf")
	info("Generando locales...")
	system("locale-gen")

def host():
	banner_titulo("Informacion host")
	hostname = input("Ingresa el nombre de tu equipo")
	system("echo " + hostname + " > /mnt/etc/hostname")
	info("Modificando el archivo /etc/hosts")
	system('echo -e "127.0.0.1\tlocalhost" >> /mnt/etc/hosts')
	system('echo -e "::1\tlocalhost" >> /mnt/etc/hosts')
	system('echo -e "127.0.0.1\t' + hostname + '" >> /mnt/etc/hosts')

tabla_de_particion = particion_de_discos()
formateo_partciones(tabla_de_particion)
montado_partciones(tabla_de_particion)
descarga()
system("genfstab -U /mnt >> /mnt/etc/fstab")
info("Cambiando al nuevo entorno root...")
idioma()
hosts()
info("instalando grub...")
system("grub-install /dev/sda --target=x86_64-efi --efi-directory=/mnt/efi --bootloader-id=GRUB")
system("grub-mkconfig -o /mnt/boot/grub/grub.cfg")
system("arch-chroot /mnt")
system("mkinitcpio -P")
info("Creando contraseña root")
system("passwd")
info("Instalacion completa!")