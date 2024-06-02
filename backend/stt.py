import io
import torch
import uvicorn
import torchaudio
from fastapi import FastAPI, UploadFile, File
from transformers import Wav2Vec2ForCTC, AutoProcessor


app = FastAPI()

model_id = "facebook/mms-1b-all"
processor = AutoProcessor.from_pretrained(model_id)
model = Wav2Vec2ForCTC.from_pretrained(model_id)


def chunk_audio(audio_data, chunk_length):
    chunks = []
    num_chunks = audio_data.shape[1] // chunk_length

    for i in range(num_chunks):
        chunks.append(audio_data[:, i * chunk_length:(i + 1) * chunk_length])
    if audio_data.shape[1] % chunk_length != 0:
        chunks.append(audio_data[:, num_chunks * chunk_length:])

    return chunks


@app.post("/stt")
async def stt(lang_code: str, wav_file: UploadFile = File(...)):
    try:
        audio_data, original_sampling_rate = torchaudio.load(io.BytesIO(await wav_file.read()))
        resampled_audio_data = torchaudio.transforms.Resample(original_sampling_rate, 16000)(audio_data)

        processor.tokenizer.set_target_lang(lang_code)
        model.load_adapter(lang_code)

        chunk_length = 16000 * 30  # 30-second chunks
        chunks = chunk_audio(resampled_audio_data, chunk_length)
        transcriptions = []

        for chunk in chunks:
            inputs = processor(chunk.numpy(), sampling_rate=16000, return_tensors="pt")

            with torch.no_grad():
                outputs = model(**inputs).logits
            ids = torch.argmax(outputs, dim=-1)[0]
            transcriptions.append(processor.decode(ids))

        transcription = " ".join(transcriptions)
        return {"transcription": transcription}
    
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, timeout_keep_alive=2400)
    