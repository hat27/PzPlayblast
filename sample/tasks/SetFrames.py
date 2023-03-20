# -*-coding: utf8-*-

from puzzle2.PzLog import PzLog

def main(event, context):
    data = event["data"]
    logger = context.get("logger")
    if not logger:
        logger = PzLog().logger

    update_context = {}
    if data["start_frame"] == 0 and data["end_frame"] == 0:
        logger.debug("set to min max frame")
        update_context["new_start_frame"] = 1
        update_context["new_end_frame"] = 100

    return {"return_code": 0, "update_context": update_context}