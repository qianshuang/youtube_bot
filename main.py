# -*- coding: utf-8 -*-

import os

from prompt_helper import *
from openai_helper import *

from typing import List
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class Context(BaseModel):
    subject: str
    history: List[str]


class QueryBody(BaseModel):
    siteId: str
    query: str
    context: Context
    dataAI: bool = False  # 默认不开启数据洞察


def extract_query(json_obj):
    content4emb, email_history = [], []
    content4emb.append(json_obj["subject"])

    if_chat = all(":" in element for element in json_obj["history"])

    for email_content in json_obj["history"]:
        if if_chat:
            colon_first_idx = email_content.find(":")
            if email_content[:colon_first_idx].strip().lower() == "user":
                content4emb.append(email_content[colon_first_idx + 1:].strip())
            email_history.append(email_content.strip())
        else:
            content4emb.append(email_content.strip())
            email_history.append("Question:" + email_content.strip())

    # 取最新轮
    # if len(content4emb) > 1:
    #     if len(content4emb[-1].strip().split()) <= 4:
    #         content4emb = content4emb[-2:]
    #     else:
    #         content4emb = content4emb[-1:]
    return content4emb, email_history


@app.post("/query")
def query(qb: QueryBody):
    print("{} is processing...".format(os.getpid()))
    bot_name = "site_" + str(qb.siteId)
    bot_path = os.path.join(BOT_SRC_DIR, bot_name)
    if not os.path.exists(bot_path):
        return {'code': -2, 'msg': "site {} agent doesn't exist...".format(qb.siteId)}

    try:
        # 记忆填充
        qb.context.history.append(qb.query)

        json_obj = qb.context.dict()
        content4emb, email_history = extract_query(json_obj)
        email_history = "\n".join(email_history).strip()

        # 生成答案
        remain_ctx = load_json_file(os.path.join(bot_path, "youtube_captions.json"))
        retrieve_prompt = gen_retrieve_prompt(remain_ctx, email_history)
        logger.info(retrieve_prompt)

        retrieve_chat_res = get_chatgpt_res(retrieve_prompt)
        retrieve_chat_res = parse_json(retrieve_chat_res)
        if "reply" not in retrieve_chat_res:
            retrieve_chat_res["reply"] = retrieve_chat_res["reasoning"]

        return {
            'code': 0,
            'msg': 'success',
            'data': retrieve_chat_res["reply"]
        }
    except:
        logger.exception("call query failed......")
        return {'code': -1, 'msg': "call query failed......"}
