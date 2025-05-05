import wave


def message_to_bits(message):
    return ''.join(format(ord(c), '08b') for c in message)


def bits_to_message(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])


def embed_and_extract(input_wav, output_wav, message):
    if len(message) != 160:
        raise ValueError("Mesaj tam olarak 160 karakter olmalıdır!")

    audio = wave.open(input_wav, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    bits = message_to_bits(message)

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)

    modified = wave.open(output_wav, 'wb')
    modified.setparams(audio.getparams())
    modified.writeframes(bytes(frame_bytes))
    modified.close()
    audio.close()
    print(f"\n✅ Mesaj başarıyla '{output_wav}' dosyasına gömüldü.")

    # Mesajı geri çıkar
    audio = wave.open(output_wav, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted = [str(frame_bytes[i] & 1) for i in range(160 * 8)]
    recovered_message = bits_to_message(''.join(extracted))
    audio.close()

    print(f"\n📢 Gömülü Mesaj: {recovered_message}")


if __name__ == "__main__":
    input_file = 'input.wav'
    output_file = 'output.wav'
    secret_message = (
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
    )

    embed_and_extract(input_file, output_file, secret_message)
