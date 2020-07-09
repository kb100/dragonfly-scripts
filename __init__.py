import logging
import sys

from dragonfly import RecognitionObserver

root = logging.getLogger()
log_level = logging.INFO
root.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


class RecognitionLogger(RecognitionObserver):
    def on_post_recognition(self, words, rule, node, results):
        logging.info(str(rule) + ' recognized: ' + ' '.join(words))


recog_logger = RecognitionLogger()
recog_logger.register()


def unload():
    global recog_logger
    if recog_logger:
        recog_logger.unregister()
    recog_logger = None
