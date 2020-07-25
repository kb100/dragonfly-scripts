from dragonfly import RecognitionObserver

from log import logger


class RecognitionLogger(RecognitionObserver):
    def on_post_recognition(self, words, rule, node, results):
        logger.info(str(rule) + ' recognized: ' + ' '.join(words))


recog_logger = RecognitionLogger()
recog_logger.register()


def unload():
    global recog_logger
    if recog_logger:
        recog_logger.unregister()
    recog_logger = None
