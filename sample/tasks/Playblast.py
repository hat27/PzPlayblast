import os
from puzzle2.PzLog import PzLog

def main(event, context):
    data = event["data"]
    logger = context.get("logger")
    if not logger:
        logger = PzLog().logger

    if data["start_frame"] == 0 and data["end_frame"] == 0:
        logger.critical("skip: start and end frame is 0")
        logger.details.set_header(2, "skip     : start and end frame was 0")
        return {"return_code": 2}

    if "output_path" in data:
        logger.debug("playblast to: {}".format(data["output_path"]))

    else:
        d, f = os.path.split(data["file_path"])
        f, ext = os.path.splitext(f)
        logger.debug("playblast to: {}/{}.avi".format(d, f))
    
    logger.details.set_header(0, "successed: {} - {}".format(data["start_frame"], data["end_frame"]))
