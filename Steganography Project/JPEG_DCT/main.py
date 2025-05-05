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

    if h < 8 or w < 8:
        raise ValueError("Resim en az 8x8 boyutunda olmalıdır!")
    if h % 8 != 0 or w % 8 != 0:
        raise ValueError("Resmin genişliği ve yüksekliği 8’in katı olmalıdır (örn. 64x64, 128x128).")

    bits = message_to_bits(message)
    bit_idx = 0

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if bit_idx >= len(bits):
                break
            block = np.float32(img[i:i+8, j:j+8])
            dct_block = cv2.dct(block)
            coeff = dct_block[4, 4]
            coeff = np.floor(coeff)
            coeff = coeff - coeff % 2 + int(bits[bit_idx])
            dct_block[4, 4] = coeff
            idct_block = cv2.idct(dct_block)
            img[i:i+8, j:j+8] = np.uint8(idct_block)
            bit_idx += 1

    cv2.imwrite(output_path, img)
    print(f"\n✅ Mesaj başarıyla '{output_path}' dosyasına gömüldü.")

def extract_message(image_path, message_length):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    bits = ''
    bit_count = message_length * 8

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if len(bits) >= bit_count:
                break
            block = np.float32(img[i:i+8, j:j+8])
            dct_block = cv2.dct(block)
            coeff = dct_block[4, 4]
            bit = int(abs(coeff)) % 2
            bits += str(bit)

    message = bits_to_message(bits)
    print(f"\n📢 Gömülü Mesaj: {message}")

if __name__ == "__main__":
    input_image = 'input.jpg'
    output_image = 'output.jpg'
    secret_message = (
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
    )

    embed_message(input_image, output_image, secret_message)
    extract_message(output_image, len(secret_message))
