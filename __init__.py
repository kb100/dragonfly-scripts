import logging

from dragonfly import RecognitionObserver

root = logging.getLogger()
log_level = logging.INFO
root.setLevel(log_level)
logging.getLogger('grammar.decode').propagate = False
logging.getLogger('grammar.begin').propagate = False
logging.getLogger('context.match').propagate = False
logging.getLogger('action.exec').propagate = False


# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(log_level)
# formatter = logging.Formatter('[%(name)s %(asctime)s %(levelname)s] %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)


class RecognitionLogger(RecognitionObserver):
    def on_post_recognition(self, words, rule, node, results):
        print '!!!!!!' + str(rule) + ' recognized: ' + ' '.join(words)
        if rule:
            print str(rule) + ' is enabled: ' + str(rule.enabled)
            print str(rule) + ' is active: ' + str(rule.active)


recog_logger = RecognitionLogger()
recog_logger.register()


def unload():
    global recog_logger
    if recog_logger:
        recog_logger.unregister()
    recog_logger = None
