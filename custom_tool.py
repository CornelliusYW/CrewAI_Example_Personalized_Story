from pydantic import BaseModel
import os 
from crewai.tools.structured_tool import CrewStructuredTool
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

class StableDiffusionInput(BaseModel):
    text_prompt: str
API_HOST = "https://api.stability.ai"
API_KEY = os.getenv("STABILITY_AI_API_KEY")
ENGINE_ID = "stable-diffusion-v1-6"

def stable_diffusion_wrapper(*args, **kwargs):
    """
    This function receives stable diffusion parameters (e.g., from Pydantic),
    calls the Stability AI API, and returns the path or data to the generated image.
    """

    text_prompt = kwargs["text_prompt"]

    response = requests.post(
        f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_prompt
                }
            ],
        },
    )

    if response.status_code != 200:
        raise Exception(f"Non-200 response: {response.text}")

    data = response.json()

    encoded_image = data["artifacts"][0]["base64"]

    decoded_bytes = base64.b64decode(encoded_image)

    output_path = "output.png"
    with open(output_path, "wb") as f:
        f.write(decoded_bytes)
        
    return f"Image generated and saved to {output_path}"


def create_stable_diffusion_tool():
    return CrewStructuredTool.from_function(
        name="stable_diffusion_tool",
        description=(
            "Generates an image using Stable Diffusion. "
            "Provide text prompt."
        ),
        args_schema=StableDiffusionInput,
        func=stable_diffusion_wrapper
    )
