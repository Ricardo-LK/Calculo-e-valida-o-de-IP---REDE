def main():
    is_ip_valid = False
    ip = ""
    subweb_mask = ""

    ## Verifica se IP é válido
    while not is_ip_valid:
        is_ip_valid = True
        print("Formato ex. 192.168.100.100")
        ip = input("Digite seu endereço de IP: ")

        if len(ip) > 15:
            is_ip_valid = False
            print("IP invalid")

        for i in range(0, 15):
            if i != 0 and (i + 1) % 4 == 0:
                if ip[i] != ".":
                    is_ip_valid = False
                    print("IP is in wrong format")
                    break
            else:
                try:
                    int(ip[i])
                except:
                    print("IP is in wrong format")
                    is_ip_valid = False
                    break

    is_submask_valid = False
    while not is_submask_valid:
        is_submask_valid = True
        print("\nFormato ex. 255.255.000.000")
        subweb_mask = input("Digite sua máscara de rede: ")

        if len(subweb_mask) > 15:
            is_submask_valid = False
            print("Submask invalid")

        for i in range(0, 15):
            if i != 0 and (i + 1) % 4 == 0:
                if subweb_mask[i] != ".":
                    is_submask_valid = False
                    print("Submask is in wrong format")
                    break
            else:
                try:
                    int(subweb_mask[i])
                except:
                    is_submask_valid = False
                    print("Submask is in wrong format")
                    break

    binary_ip = "".join([format(int(sect), "08b") for sect in ip.split(".")])
    binary_submask = "".join([format(int(sect), "08b") for sect in subweb_mask.split(".")])
    print(binary_ip)
    print(binary_submask)

    web_address = "".join(str(int(binary_ip[i]) & int(binary_submask[i])) for i in range(32))
    

if __name__ == "__main__":
    main()