# -*-coding: utf8-*-

import os
from puzzle2.PzLog import PzLog

def main(event, context):
    data = event["data"]
    logger = context.get("logger")
    if not logger:
        logger = PzLog().logger

    logger.debug("set HUD")