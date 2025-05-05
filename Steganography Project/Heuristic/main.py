import wave
import numpy as np


def analyze_lsb(input_wav):
    audio = wave.open(input_wav, mode='rb')
    n_frames = audio.getnframes()
    frame_bytes = np.frombuffer(audio.readframes(n_frames), dtype=np.uint8)
    audio.close()

    lsb_array = frame_bytes & 1  # sadece LSB’leri al
    ones = np.sum(lsb_array)
    zeros = len(lsb_array) - ones
    ratio = ones / (ones + zeros)

    print(f"\n🔍 Dosya: {input_wav}")
    print(f"Toplam bit sayısı: {len(lsb_array)}")
    print(f"1’lerin oranı: {ratio:.4f}")

    # %45–55 arası normal, dışı şüpheli
    if 0.45 < ratio < 0.55:
        print("✅ Muhtemelen steganografi yok (doğal LSB dağılımı).")
    else:
        print("⚠️ Şüpheli LSB dağılımı! Mesaj gömülmüş olabilir.")


if __name__ == "__main__":
    files_to_check = ['input_or_stego.wav', 'input_or_stego2.wav']

    for file in files_to_check:
        try:
            analyze_lsb(file)
        except Exception as e:
            print(f"\n❌ {file} dosyası analiz edilirken hata oluştu: {e}")
