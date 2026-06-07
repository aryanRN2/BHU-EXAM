import os
import requests

api_key = os.getenv("HF_API_KEY")
# Let's use Qwen2.5-72B-Instruct or Llama-3-8B-Instruct
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
url = f"https://api-inference.huggingface.co/models/{model_id}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWrite a short greeting.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    "parameters": {
        "max_new_tokens": 50,
        "return_full_text": False
    }
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
