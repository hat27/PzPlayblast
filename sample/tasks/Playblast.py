import os
from puzzle2.PzLog import PzLog

def main(event, context):
    data = event["data"]
    logger = context.get("logger")
    if not logger:
        logger = PzLog().logger

    if data["start_frame"] == 0 and data["end_frame"] == 0:
        logger.critical("skip: start and end frame is 0")
        return {"return_code": 2}

    if "output_path" in data:
        logger.debug("playblast to: {}".format(data["output_path"]))

    else:
        d, f = os.path.split(data["file_path"])
        f, ext = os.path.splitext(f)
        logger.debug("playblast to: {}/{}.avi".format(d, f))
    
    logger.debug("start: {}".format(data["start_frame"]))
    logger.debug("end: {}".format(data["end_frame"]))