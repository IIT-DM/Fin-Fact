import os
import json
import argparse
import pickle
import re, requests, tempfile, io
from dotenv import load_dotenv
from tqdm import tqdm

from tenacity import retry, wait_random_exponential, stop_after_attempt
from sklearn.metrics import classification_report, confusion_matrix

import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image

import get_api
from prompts import *

load_dotenv()


class MLLM_EXP:
    def __init__(
        self,
        dataset_name,
        model_name,
        prompt_method,
        device,
    ):
        self.dataset_name = dataset_name
        self.model_name = model_name
        self.prompt_method = prompt_method
        self.torch_device = device

        if self.model_name == "llava":
            self.llava_model = LlavaForConditionalGeneration.from_pretrained(
                "llava-hf/llava-1.5-7b-hf",
                torch_dtype=torch.float16,
            ).to(self.torch_device)
            self.llava_processor = AutoProcessor.from_pretrained(
                "llava-hf/llava-1.5-7b-hf"
            )

    def load_data(self):
        with open(f"{self.dataset_name}", "r") as f:
            data = json.load(f)
        return data

    def save_to_pickle(self, data, output_file):
        with open(output_file, "wb") as f:
            pickle.dump(data, f)

    def download_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                image.save(temp_file.name, format="PNG")
            
            return temp_file.name
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def cleanup_image(self, file_path):
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(5))
    def call_gemini(self, claim, text_evidence, image_list):
        if self.prompt_method == "closed_book":
            system_prompt = closed_book_system
            prompt = f"Claim: {claim}"

            response = get_api.get_gemini_text_response(
                prompt,
                image_list,
                model="gemini-1.5-pro",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response
        
        if self.prompt_method == "cot":
            system_prompt = chain_of_thought
            prompt = f"Claim: {claim}"

            response = get_api.get_gemini_text_response(
                prompt,
                image_list,
                model="gemini-1.5-pro",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response
        
        if self.prompt_method == "symbolic":
            system_prompt = chain_of_thought
            prompt = f"Claim: {claim}"

            response = get_api.get_gemini_text_response(
                prompt,
                image_list,
                model="gemini-1.5-pro",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response
        
        if self.prompt_method == "self_help":
            system_prompt = chain_of_thought
            prompt = f"Claim: {claim}"

            response = get_api.get_gemini_text_response(
                prompt,
                image_list,
                model="gemini-1.5-pro",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response

        if self.prompt_method == "open_book":
            system_prompt = open_book_system
            prompt = f"""Claim: {claim}
            Text Evidence: {text_evidence}
            Image Evidence: """

            response = get_api.get_gemini_text_response(
                prompt,
                image_list,
                model="gemini-1.5-pro",
                system_prompt=system_prompt,
                temperature=0.0,
            )
            return response

    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(5))
    def call_openai(self, claim, text_evidence, image_list):
        if self.prompt_method == "closed_book":
            system_prompt = closed_book_system
            prompt = f"Claim: {claim}"

            response = get_api.get_openai_text_response(
                prompt,
                image_list,
                model="gpt-4o-mini",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response
        
        if self.prompt_method == "cot":
            system_prompt = chain_of_thought
            prompt = f"""Claim: {claim}
            Text Evidence: {text_evidence}
            Image Evidence: """

            response = get_api.get_openai_text_response(
                prompt,
                image_list,
                model="gpt-4",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response
        
        if self.prompt_method == "symbolic":
            system_prompt = chain_of_thought
            prompt = f"""Claim: {claim}
            Text Evidence: {text_evidence}
            Image Evidence: """

            response = get_api.get_openai_text_response(
                prompt,
                image_list,
                model="gpt-4",
                system_prompt=system_prompt,
                temperature=0.0,
            )
            return response

        if self.prompt_method == "self_help":
            system_prompt = chain_of_thought
            prompt = f"""Claim: {claim}
            Text Evidence: {text_evidence}
            Image Evidence: """

            response = get_api.get_openai_text_response(
                prompt,
                image_list,
                model="gpt-4",
                system_prompt=system_prompt,
                temperature=0.0,
            )
            return response

        if self.prompt_method == "open_book":
            system_prompt = open_book_system
            prompt = f"""Claim: {claim}
            Text Evidence: {text_evidence}
            Image Evidence: """

            response = get_api.get_openai_text_response(
                prompt,
                image_list,
                model="gpt-40-mini",
                system_prompt=system_prompt,
                temperature=0.0,
            )

            return response

    def call_llava(self, claim, text_evidence, image_list):
        if self.prompt_method == "closed_book":
            system_prompt = closed_book_system
            prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
            ###Human: {system_prompt} \nClaim: {claim}\n###Assistant:"""

            inputs = self.llava_processor(text=prompt, return_tensors="pt").to(
                self.torch_device
            )
            generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
            res = self.llava_processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            return res
        
        if self.prompt_method == "cot":
            system_prompt = chain_of_thought
            prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
            ###Human: {system_prompt} \nClaim: {claim}\n###Assistant:"""

            inputs = self.llava_processor(text=prompt, return_tensors="pt").to(
                self.torch_device
            )
            generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
            res = self.llava_processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            return res
        
        if self.prompt_method == "symbolic":
            system_prompt = chain_of_thought
            prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
            ###Human: {system_prompt} \nClaim: {claim}\n###Assistant:"""

            inputs = self.llava_processor(text=prompt, return_tensors="pt").to(
                self.torch_device
            )
            generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
            res = self.llava_processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            return res
        
        if self.prompt_method == "self_help":
            system_prompt = chain_of_thought
            prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
            ###Human: {system_prompt} \nClaim: {claim}\n###Assistant:"""

            inputs = self.llava_processor(text=prompt, return_tensors="pt").to(
                self.torch_device
            )
            generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
            res = self.llava_processor.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            return res

        if self.prompt_method == "open_book":
            system_prompt = open_book_system

            if len(image_list) >= 1:
                prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
                ###Human: <image> \n{system_prompt} \nClaim: {claim} \nText Evidence: {text_evidence} \n###Assistant:"""

                image = Image.open(image_list[0])

                inputs = self.llava_processor(
                    text=prompt, images=image, return_tensors="pt"
                ).to(self.torch_device)
                generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
                res = self.llava_processor.batch_decode(
                    generate_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )[0]
                return res
            else:
                prompt = f"""A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.
                ###Human: \n{system_prompt} \nClaim: {claim} \nText Evidence: {text_evidence} \n###Assistant:"""

                inputs = self.llava_processor(text=prompt, return_tensors="pt").to(
                    self.torch_device
                )
                generate_ids = self.llava_model.generate(**inputs, max_new_tokens=10000)
                res = self.llava_processor.batch_decode(
                    generate_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )[0]
                return res

    def get_output(self, data):
        results = []

        for entry in tqdm(data, total=len(data), desc="Getting Output"):
            claim = entry["claim"]
            sci_digest = entry.get("sci_digest", [])
            sci_digest_text = sci_digest[0] if sci_digest else ""
            justification = entry.get("justification", "")
            text_evidence = sci_digest_text + " " + justification
            image_list = []
            for img in entry.get("image_data", []):
                img_path = self.download_image(img["image_src"])
                if img_path:
                    image_list.append(img_path)
            try:
                if self.model_name == "gemini":
                    res = self.call_gemini(claim, text_evidence, image_list)
                elif self.model_name == "gpt-4":
                    res = self.call_openai(claim, text_evidence, image_list)
                elif self.model_name == "llava":
                    res = self.call_llava(claim, text_evidence, image_list)
                
                results.append(res)
            except Exception as e:
                print(f"Error processing entry: {e}")
                results.append("")

            for img_path in image_list:
                self.cleanup_image(img_path)

        self.save_to_pickle(
            results,
            f"Output/{self.dataset_name[:-5]}_{self.model_name}_{self.prompt_method}.pkl",
        )

    def evaluate(self, data):
        with open(
            f"Output/{self.dataset_name[:-5]}_{self.model_name}_{self.prompt_method}.pkl",
            "rb",
        ) as f:
            output = pickle.load(f)

        prediction_list = []
        for i in output:
            try:
                if self.model_name in ["gpt-4", "gemini"]:
                    pattern = re.compile(r"Prediction:\s*(.*)", re.IGNORECASE)
                    match = pattern.search(i)
                    if match:
                        prediction_list.append(match.group(1).strip().lower())
                    else:
                        prediction_list.append("")
                elif self.model_name == "llava":
                    match = i.split("Prediction:")[1].split("Explanation:")[0]
                    prediction_list.append(match.strip().lower())
            except:
                prediction_list.append("")

        gold_label = [entry["label"].lower() for entry in data]
        to_remove = []
        for i in range(len(gold_label)):
            if prediction_list[i] not in ["true", "false", "neutral"]:
                to_remove.append(i)
        for index in sorted(to_remove, reverse=True):
            del prediction_list[index]
            del gold_label[index]
        num_correct = sum(1 for pred, gold in zip(prediction_list, gold_label) if pred == gold)
        accuracy = num_correct / len(gold_label)
        print(f"Accuracy: {accuracy}")
        target_names = ["false", "true", "neutral"]
        label_map = {"false": 0, "true": 1, "neutral": 2}
        labels = [label_map[e] for e in gold_label]
        predictions = [label_map[e] for e in prediction_list]
        print("Classification Report")
        print("=" * 60)
        print(
            classification_report(
                labels, predictions, target_names=target_names, digits=4
            )
        )
        print(confusion_matrix(labels, predictions))

    def run(self):
        data = self.load_data()
        if not os.path.exists("Output"):
            os.makedirs("Output")
        self.get_output(data)
        self.evaluate(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        type=str,
        default="finfact.json",
        help="dataset filename",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="model [llava, gpt-4, gemini]",
    )
    parser.add_argument(
        "--prompt_type",
        type=str,
        default="cot",
        help="prompt type [open_book, closed_book, cot, symbolic, self_help]",
    )
    parser.add_argument("--device", type=str, default="cuda:0", help="cuda device")
    args = parser.parse_args()
    print(args)

    mllm = MLLM_EXP(args.dataset, args.model, args.prompt_type, args.device)
    mllm.run()