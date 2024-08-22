def validar_ip(ip):
    ## Verifica se IP é válido
    is_ip_valid = True

    if len(ip) > 15 or len(ip) < 1:
        is_ip_valid = False

    for i in range(0, 15, 4):
        if int(ip[i : i + 3]) > 255:
            is_ip_valid = False
            break

    for i in range(0, 15):
        if i != 0 and (i + 1) % 4 == 0:
            if ip[i] != ".":
                is_ip_valid = False
                break
        else:
            try:
                int(ip[i])
            except:
                is_ip_valid = False
                break

    return is_ip_valid


def validar_mascara(mascara):
    is_submask_valid = True

    if len(mascara) > 15 or len(mascara) < 1:
        is_submask_valid = False

    for i in range(0, 15):
        if i != 0 and (i + 1) % 4 == 0:
            if mascara[i] != ".":
                is_submask_valid = False
                break
        else:
            try:
                int(mascara[i])
            except:
                is_submask_valid = False
                break

    return is_submask_valid


def calcular_rede(ip, mascara):
    binary_ip = "".join([format(int(sect), "08b") for sect in ip.split(".")])
    binary_webmask = "".join([format(int(sect), "08b") for sect in mascara.split(".")])

    web_address = "".join(str(int(binary_ip[i]) & int(binary_webmask[i])) for i in range(32))

    return web_address


def calcular_broadcast(ip, mascara):
    broadcast_address = ""

    binary_web_address = calcular_rede(ip, mascara)
    print(binary_web_address)

    binary_webmask = "".join([format(int(sect), "08b") for sect in mascara.split(".")])
    inverted_webmask_arr = ""

    for e in binary_webmask:
        if e == "1":
            inverted_webmask_arr += "0"
        else:
            inverted_webmask_arr += "1"

    for i in range(32):
        bit_temp = int(binary_web_address[i]) | int(inverted_webmask_arr[i])
        broadcast_address += str(bit_temp)

    return broadcast_address

def calcular_endereço_rede(ip, mascara):
    subweb_step = 256 - int(mascara[12:16])
    network_address = 0
    broadcast_address = subweb_step - 1
    while not(int(ip[12:16]) >= network_address and int(ip[12:16]) < broadcast_address):
        network_address += subweb_step
        broadcast_address += subweb_step
        
    return network_address


def numero_de_hosts(mascara):
    arr = mascara.split(".")
    for i in range(len(arr)):
        arr[i] = str(format(int(arr[i]), '08b'))

    subnet_binary = "".join(arr)
    subnet_bits = 0
    for i in range(len(subnet_binary)):
        if subnet_binary[i] == "0":
            subnet_bits += 1

    hosts_bits = 2 ** subnet_bits

    return hosts_bits


def listar_ips_rede(ip, mascara):
    rede = calcular_rede(ip, mascara)
    broadcast = calcular_broadcast(ip, mascara)
    
    rede_int = sum([int(sect) << (8 * i) for i, sect in enumerate(rede.split(".")[::-1])])
    broadcast_int = sum([int(sect) << (8 * i) for i, sect in enumerate(broadcast.split(".")[::-1])])
    
    available_IPs = []
    
    for ip_int in range(rede_int + 1, broadcast_int):
        sects = [str((ip_int >> (8 * i)) & 0xFF) for i in range(4)][::-1]
        available_IPs.append(".".join(sects))
    
    return available_IPs


def calcular_faixa_de_rede(ip):
    web_range = ""
    IPsArray = ip.split(".")
    IPsArray = [int(e) for e in IPsArray]

    if IPsArray[0] == 0:
        web_range = "Rede privada"

    elif IPsArray[0] == 10 or (IPsArray[0] == 172 and IPsArray[1] == 16) or (IPsArray[0] == 192 and IPsArray[1] == 168):
        web_range = "Endereçamento privado"

    elif IPsArray[0] == 127:
        web_range = "Endereçamento de realimentação (loopback)"
    
    elif IPsArray[0] == 169 and IPsArray[1] == 254:
        web_range = "Zeroconf/APIPA"

    elif IPsArray[0] == 240 or (IPsArray[0] == 192 and IPsArray[1] == 0 and IPsArray[2] == 0):
        if IPsArray[0] == 240:
            web_range = "Reservado (Classe E)"
        else:
            web_range = "Reservado"

    elif (IPsArray[0] == 192 and IPsArray[1] == 0 and IPsArray[2] == 2) or (IPsArray[0] == 198 and IPsArray[1] == 51 and IPsArray[2] == 100) or (IPsArray[0] == 203 and IPsArray[1] == 0 and IPsArray[2] == 113):
        web_range = "Documentação e exemplos"

    elif IPsArray[0] == 192 and IPsArray[1] == 88 and IPsArray[2] == 99:
        web_range = "6to4 (Mecanismo de transição de endereços IPv4 em IPv6)"

    elif IPsArray[0] == 198 and IPsArray[1] == 18:
        web_range = "Equipamentos para teste de rede"

    elif IPsArray[0] == 224:
        web_range = "Multicast (Classe D)"

    else:
        web_range = "IP não especial"

    return web_range


def main():
    ip = ""
    subweb_mask = ""
    available_ips = 0

    print("Formato ex. 192.168.100.100")
    ip = input("Digite seu endereço de IP: ")
    validacao = validar_ip(ip)
    while not validacao:
        if not validacao:
            print("IP is in wrong format\n")

        print("Formato ex. 192.168.100.100")
        ip = input("Digite seu endereço de IP: ")
        validacao = validar_ip(ip)


    print("\nFormato ex. 255.255.000.000")
    subweb_mask = input("Digite sua máscara de rede: \n")
    validacao = validar_mascara(subweb_mask)
    while not validacao: 
        if not validacao:
            print("Submask is in wrong format")

        print("\nFormato ex. 255.255.000.000")
        subweb_mask = input("Digite sua máscara de rede: \n")
        validacao = validar_mascara(subweb_mask)

    
    web_address = calcular_rede(ip, subweb_mask)
    print(f"Endereço de rede: {web_address}")

    broadcast_address = calcular_broadcast(ip, subweb_mask)
    print(f"Endereço de broadcast: {broadcast_address}")

    number_hosts = numero_de_hosts(subweb_mask)
    print(f"Numero de hosts: {number_hosts}")

    available_ips = listar_ips_rede(ip, subweb_mask)
    print("IPs válidos:")
    for available_ip in available_ips:
        print(f"    {available_ip}")

    web_range = calcular_faixa_de_rede(ip)
    print(f"Faixa de rede: {web_range}")

if __name__ == "__main__":
    main()