import yaml
import logging
import logging.config

def get_logger(fname: str = "logs.log"):
    with open("./lazynotion/configs/log.yml", "r") as f:
        log_config_dict = yaml.safe_load(f)
    log_config_dict["handlers"]["file"]["filename"] = fname
    logging.config.dictConfig(log_config_dict)
    logger = logging.getLogger("all")
    return logger
