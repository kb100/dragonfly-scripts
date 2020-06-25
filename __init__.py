import sys
import logging
root = logging.getLogger()
log_level = logging.INFO
root.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
formatter = logging.Formatter('[%(asctime)s %(name)s %(levelname)s] %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
