def validar_ip(ip):
    ## Verifica se IP é válido
    is_ip_valid = True

    if len(ip) > 15:
        is_ip_valid = False

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

    if len(mascara) > 15:
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
    binary_submask = "".join([format(int(sect), "08b") for sect in mascara.split(".")])

    web_address = "".join(str(int(binary_ip[i]) & int(binary_submask[i])) for i in range(32))

    return web_address


def calcular_broadcast(ip, mascara):
    subweb_step = 256 - int(mascara[12:16])
    network_address = 0
    broadcast_address = subweb_step - 1
    while not(int(ip[12:16]) > network_address and int(ip[12:16]) < broadcast_address):
        network_address += subweb_step
        broadcast_address += subweb_step
    return broadcast_address


def numero_de_hosts(mascara):

    subweb_binary = str(bin(int(mascara[12:16])))
    subweb_bits = 0
    for i in range(8):
        if subweb_binary[i] == "1":
            subweb_bits += 1

    hosts_bits = 8 - subweb_bits

    return hosts_bits


def listar_ips_rede(ip, mascara):
    subweb_step = 256 - int(mascara[12:16])
    network_address = 0
    broadcast_address = subweb_step - 1
    available_ips = -2

    for i in range(1, 255):
        if not (i / network_address == 0 or i / broadcast_address == 0):
            available_ips += 1

    return available_ips


def main():
    ip = ""
    subweb_mask = ""
    number_hosts = 0
    available_ips = 0

    validacao = validar_ip(ip)
    while not validacao:
        print("Formato ex. 192.168.100.100")
        ip = input("Digite seu endereço de IP: ")
        validacao = validar_ip(ip)
        if not validacao:
            print("IP is in wrong format")

    validacao = validar_mascara(subweb_mask)
    while not validacao: 
        print("\nFormato ex. 255.255.000.000")
        subweb_mask = input("Digite sua máscara de rede: ")
        validacao = validar_mascara(subweb_mask)
        if not validacao:
            print("Submask is in wrong format")

    
    web_address = calcular_rede(ip, subweb_mask)
    print(web_address)

    broadcast_address = calcular_broadcast(ip, subweb_mask)
    print(broadcast_address)

    number_hosts = numero_de_hosts(subweb_mask)
    print(number_hosts)

    available_ips = listar_ips_rede(ip, subweb_mask)


if __name__ == "__main__":
    main()