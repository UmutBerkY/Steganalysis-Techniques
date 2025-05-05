import cv2
import numpy as np

def message_to_bits(message):
    return ''.join(format(ord(c), '08b') for c in message)

def bits_to_message(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])

def embed_message(image_path, output_path, message):
    if len(message) != 160:
        raise ValueError("Mesaj tam olarak 160 karakter olmalıdır!")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    flat_img = img.flatten()

    bits = message_to_bits(message)
    if len(bits) > len(flat_img):
        raise ValueError("Resim çok küçük, mesaj sığmıyor.")

    # 7. bit düzlemini kullan (0 tabanlı: bit 6)
    for i, bit in enumerate(bits):
        flat_img[i] = (flat_img[i] & 0b10111111) | (int(bit) << 6)

    new_img = flat_img.reshape((h, w))
    cv2.imwrite(output_path, new_img)
    print(f"\n✅ Mesaj başarıyla '{output_path}' dosyasına gömüldü.")
    

def extract_message(image_path, message_length):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    flat_img = img.flatten()

    bits = ''
    for i in range(message_length * 8):
        bit = (flat_img[i] >> 6) & 1
        bits += str(bit)

    message = bits_to_message(bits)
    print(f"\n📢 Gömülü Mesaj: {message}")

if __name__ == "__main__":
    input_image = 'input_bpcs.png'
    output_image = 'output_bpcs.png'
    secret_message = (
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
    )

    embed_message(input_image, output_image, secret_message)
    extract_message(output_image, len(secret_message))
