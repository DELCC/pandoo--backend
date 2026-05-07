from openai import AsyncOpenAI
from elevenlabs.client import AsyncElevenLabs
import aiofiles
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key_ELEVENLABS = os.getenv("API_KEY_ELEVENLABS")
api_key_OPEN_AI = os.getenv("API_KEY_OPEN_AI")

clientElevenLabs = AsyncElevenLabs(api_key=api_key_ELEVENLABS)
clientOpenAI = AsyncOpenAI(api_key=api_key_OPEN_AI)


async def generate_story(id_child: int, voice_id: str) -> str:
    try:
        response = await clientOpenAI.responses.create(
            model="gpt-4.1-mini",
            input="Explain gravity to a 10 year old."
        )

        generated_text = response.output_text

        audio_stream = clientElevenLabs.text_to_speech.convert(
            text=generated_text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        BASE_DIR = Path(__file__).resolve().parent
        stories_dir = BASE_DIR / "stories_audio"
        stories_dir.mkdir(exist_ok=True)

        filename = stories_dir / f"story_{id_child}.mp3"

        async with aiofiles.open(filename, "wb") as f:
            async for chunk in audio_stream:
                await f.write(chunk)

        return str(filename)

    except Exception as e:
        raise RuntimeError(f"Erreur génération story : {e}")