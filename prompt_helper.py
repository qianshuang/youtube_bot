# -*- coding: utf-8 -*-


def gen_retrieve_prompt(qa_retrieve_ctx, transed_dialogue):
    prompt_str = """GOAL:
With reference to the CONTEXT (The content in Context is subtitles and other information extracted from YouTube videos, please answer based on this.) below, generate the most appropriate answer based on the DIALOGUE below.
Let's work this out in a step by step way to be sure we have the right answer.

CONTEXT:
{}

DIALOGUE:
{}

You should only respond in JSON format as described below:
{{
    "reasoning": "reasoning",
    "reply": "Reply based on the DIALOGUE and CONTEXT.",
    "can_answer": "True if you can figure out the answer only from the DIALOGUE and CONTEXT, False otherwise."
}}
Ensure the response can be parsed by Python json.loads""".format(qa_retrieve_ctx, transed_dialogue)

    sys_content = """You are a trustworthy AI assistant.
Remember that you should figure out the answer only from the DIALOGUE and CONTEXT (use the original text in the DIALOGUE and CONTEXT as answer as much as possible), if not, set the value of the can_answer field to False. Be sure to answer carefully to avoid mistakes.
If the question in the DIALOGUE is not related to the CONTEXT, set the value of the can_answer field to False."""
    return [{"role": "system", "content": sys_content},
            {"role": "user", "content": prompt_str}]
