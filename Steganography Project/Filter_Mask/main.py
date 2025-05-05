import wave
import numpy as np

def message_to_bits(message):
    return ''.join(format(ord(c), '08b') for c in message)

def bits_to_message(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])

def embed_message(input_wav, output_wav, message):
    if len(message) != 160:
        raise ValueError("Mesaj tam olarak 160 karakter olmalıdır!")

    audio = wave.open(input_wav, mode='rb')
    n_frames = audio.getnframes()
    frame_bytes = np.frombuffer(audio.readframes(n_frames), dtype=np.uint8).copy()  # <== DÜZELTME BURADA
    audio.close()

    bits = message_to_bits(message)
    low_amp_indices = np.where(frame_bytes < 20)[0]  # düşük genlikli noktalar

    if len(low_amp_indices) < len(bits):
        raise ValueError("Yeterli düşük genlikli örnek yok!")

    for i, bit in enumerate(bits):
        idx = low_amp_indices[i]
        frame_bytes[idx] = (frame_bytes[idx] & 0b11111110) | int(bit)

    output_audio = wave.open(output_wav, 'wb')
    with wave.open(input_wav, 'rb') as in_audio:
        output_audio.setparams(in_audio.getparams())
    output_audio.writeframes(frame_bytes.tobytes())
    output_audio.close()
    print(f"\n✅ Mesaj başarıyla '{output_wav}' dosyasına gömüldü.")

def extract_message(stego_wav, message_length):
    audio = wave.open(stego_wav, mode='rb')
    n_frames = audio.getnframes()
    frame_bytes = np.frombuffer(audio.readframes(n_frames), dtype=np.uint8).copy()
    audio.close()

    low_amp_indices = np.where(frame_bytes < 20)[0]
    bits = ''
    for i in range(message_length * 8):
        idx = low_amp_indices[i]
        bits += str(frame_bytes[idx] & 1)

    message = bits_to_message(bits)
    print(f"\n📢 Gömülü Mesaj: {message}")

if __name__ == "__main__":
    input_file = 'input.wav'
    output_file = 'output_mask.wav'
    secret_message = (
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
        "qwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzxqwertyuopasdfghjklzx"
    )

    embed_message(input_file, output_file, secret_message)
    extract_message(output_file, len(secret_message))
