#!/usr/bin/env python3

from google.cloud import speech
import os
import sys


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/google/transcricao.json"


def transcrever_audio(arquivo_audio):

    client = speech.SpeechClient()

    with open(arquivo_audio, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="pt-BR",
        enable_automatic_punctuation=True,
        model="latest_long"
    )

    response = client.recognize(
        config=config,
        audio=audio
    )

    texto = ""

    for result in response.results:
        texto += result.alternatives[0].transcript + "\n"

    return texto


def main():

    if len(sys.argv) < 2:
        print("Uso: transcricao.py arquivo.wav")
        sys.exit(1)

    arquivo_audio = sys.argv[1]

    if not os.path.isfile(arquivo_audio):
        print(f"Arquivo nao encontrado: {arquivo_audio}")
        sys.exit(1)

    try:

        print(f"Transcrevendo: {arquivo_audio}")

        texto = transcrever_audio(arquivo_audio)

        arquivo_saida = os.path.splitext(arquivo_audio)[0] + ".txt"

        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto + "\n")

        print(f"Transcricao salva em: {arquivo_saida}")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
