# -*- coding: utf-8 -*-

import json

import requests


def call_azure(prompt_messages, api_url="https://comm100gpt.openai.azure.com/openai/deployments/Summary/chat/completions?api-version=2023-03-15-preview", key="3a4cc360c1f8427c9a22225197744697"):
    query_body = {"temperature": 0, "messages": prompt_messages}
    headers = {'content-type': 'application/json', 'api-key': key}
    response = requests.post(api_url, json=query_body, headers=headers, timeout=300)
    json_res = json.loads(response.text)
    try:
        return json_res["choices"][0]["message"]["content"]
    except:
        print("call_azure failed, prompt: {}, returned json result: {}".format(prompt_messages[1]["content"], json_res))
        raise RuntimeError("Failed to call_azure...")


p_ = [{"role": "user", "content": "What is 12 + 64?"}]
print(call_azure(p_))
