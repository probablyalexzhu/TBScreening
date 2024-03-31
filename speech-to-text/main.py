from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_model_selection_v2(
    project_id: str,
    model: str,
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file."""
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model=model,
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


if __name__ == "__main__":

    print("Transcribing audio file...")

    print(transcribe_model_selection_v2(
        project_id="sage-418803",
        model="latest_long",
        audio_file="gas.mp3",
    ))

    print("Transcription complete.")