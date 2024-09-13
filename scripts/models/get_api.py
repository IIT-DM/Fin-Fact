import os
import traceback
from dotenv import load_dotenv
import base64
from openai import OpenAI

import google.generativeai as genai
from PIL import Image

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_openai_text_response(
    prompt,
    image_file_list,
    model,
    system_prompt="You are a helpful assistant.",
    temperature=0.0,
):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        if len(image_file_list) == 0:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        elif len(image_file_list) == 1:
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[0])}"
                            },
                        },
                    ],
                },
            ]
        elif len(image_file_list) == 2:
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[0])}"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[1])}"
                            },
                        },
                    ],
                },
            ]
        elif len(image_file_list) >= 3:
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[0])}"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[1])}"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(image_file_list[2])}"
                            },
                        },
                    ],
                },
            ]

        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return None


def get_gemini_text_response(
    prompt,
    image_file_list,
    model="gemini-1.5-flash",
    system_prompt="You are a helpful assistant.",
    temperature=0.0,
):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model, system_instruction=system_prompt)

        if len(image_file_list) == 0:
            response = model.generate_content(
                [
                    prompt,
                ],
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=temperature,
                ),
            )
        elif len(image_file_list) == 1:
            image1 = Image.open(image_file_list[0])
            response = model.generate_content(
                [
                    prompt,
                    image1,
                ],
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=temperature,
                ),
            )
        elif len(image_file_list) == 2:
            image1 = Image.open(image_file_list[0])
            image2 = Image.open(image_file_list[1])
            response = model.generate_content(
                [prompt, image1, image2],
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=temperature,
                ),
            )
        elif len(image_file_list) >= 3:
            image1 = Image.open(image_file_list[0])
            image2 = Image.open(image_file_list[1])
            image3 = Image.open(image_file_list[2])
            response = model.generate_content(
                [prompt, image1, image2, image3],
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=temperature,
                ),
            )

        response.resolve()
        result = response.text
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        return None
