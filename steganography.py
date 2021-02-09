import cv2
import numpy as np

#CONVERTIR DATOS A FORMATO BINARIO.A
def to_bin(data):
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
    #LECTURA DE IMÁGEN ORIGINAL
    image = cv2.imread(image_name)
    #NÚMERO MÁXIMODE BYTES A CODIFICAR
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    #CRITERIO PARA DETENER PROCESO
    secret_data += "====="
    data_index = 0
    #CONVERTIR A BINARIO
    binary_secret_data = to_bin(secret_data)
    #TAMAÑO DE INFORMACIÓN A ESCONDER
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            #CONVERTIR VALORES RGB A BINARIO
            r, g, b = to_bin(pixel)
            #MODIFICAR BIT MENOS SIGNIFICATIVO SI QUEDAN DATOS A ALMACENAR.
            if data_index < data_len:
                #BIT DE PIXEL ROJO MENOS SIGNIFICATIVO.
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                #BIT DE PIXEL VERDE MENOS SIGNIFICATIVO.
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                #BIT DE PIXEL AZUL MENOS SIGNIFICATIVO.
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            #SI LOS DATOS ESTÁN CADIFICADOS, SALIR DEL BUCLE.
            if data_index >= data_len:
                break
    return image

def decode(image_name):
    print("[+] Decoding...")
    #LEER IMÁGEN
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    #DIVIDIR EN GRUPOS DE 8 BITS
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    #CONVERTIR BITS A CARACTERES
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

if __name__ == "__main__":
    #IMAGEN ORIGINAL.
    input_image = "image.PNG"
    #NOMBRE IMAGEN DE SALIDA
    output_image = "encoded_image.PNG"
    #INFORMACIÓN A OCULTAR
    secret_data = "This is a top secret message."
    encoded_image = encode(image_name=input_image, secret_data=secret_data)
    cv2.imwrite(output_image, encoded_image)
    #OBTENER INFORMACIÓN OCULTA DE LA IMAGEN DE SALIDA.
    decoded_data = decode(output_image)
    print("[+] Decoded data:", decoded_data)
