# -*-coding: utf8-*-
import os
from puzzle2.PzLog import PzLog

def main(event, context):
    data = event["data"]
    logger = context.get("logger")
    if not logger:
        logger = PzLog().logger

    name = "new_panel"
    logger.debug("create panel: {}".format(name))
    update_context = {"new_panel_name": name}
    return {"return_code": 0, "update_context": update_context}