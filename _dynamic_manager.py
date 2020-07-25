import importlib
import traceback

from dragonfly import *

from log import logger


class DynamicContext(Context):
    def __init__(self, fallback, focus_context):
        super(Context, self).__init__()
        self.fallback = fallback
        self.focus_context = focus_context

    def matches(self, executable, title, handle):
        if not self.is_dynamic_active(executable, title, handle):
            return self.fallback.matches(executable, title, handle) if self.fallback is not None else True
        return True

    def is_dynamic_active(self, executable, title, handle):
        if self.focus_context is None:
            return True
        return self.focus_context.matches(executable, title, handle)


class DynamicGrammarStateManager(RecognitionObserver):

    def __init__(self, grammars_grouped_by_module, modules_by_name, dynamic_context):
        super(RecognitionObserver, self).__init__()
        self.is_dynamic_active = False
        self.context = dynamic_context
        self.grammars_grouped_by_module = grammars_grouped_by_module
        self.modules_by_name = modules_by_name
        self.static_grammar_states = self.get_current_grammar_states()
        self.states_to_restore_on_window_focus = {name: [False for _ in grammars]
                                                  for name, grammars in grammars_grouped_by_module.iteritems()}
        self.states_to_restore_on_manual_enable = self.get_current_grammar_states()
        self.module_is_enabled = {name: False for name in grammars_grouped_by_module}

    def dynamic_enable(self, module_name):
        logger.info("dynamic enable" + module_name)
        if self.module_is_enabled[module_name]:
            return
        self.module_is_enabled[module_name] = True
        logger.info(self.states_to_restore_on_manual_enable[module_name])
        self.apply_states_to_grammars(self.grammars_grouped_by_module[module_name],
                                      self.states_to_restore_on_manual_enable[module_name])
        for name in self.grammars_grouped_by_module:
            if name == module_name:
                continue
            self.dynamic_disable(name)

    def dynamic_disable(self, module_name):
        logger.info("dynamic disable" + module_name)
        if not self.module_is_enabled[module_name]:
            return
        self.module_is_enabled[module_name] = False
        self.states_to_restore_on_manual_enable[module_name] = [grammar.enabled for grammar in
                                                                self.grammars_grouped_by_module[module_name]]
        self.apply_states_to_grammars(self.grammars_grouped_by_module[module_name],
                                      [False for _ in self.grammars_grouped_by_module[module_name]])

    def get_current_grammar_states(self):
        return {name: [grammar.enabled for grammar in grammars]
                for name, grammars in self.grammars_grouped_by_module.iteritems()}

    def on_begin(self):
        window = Window.get_foreground()
        if self.is_dynamic_active and not self.context.is_dynamic_active(window.executable, window.title,
                                                                         window.handle):
            self.is_dynamic_active = False
            self.states_to_restore_on_window_focus = self.get_current_grammar_states()
            self.set_current_grammar_states(self.static_grammar_states)
        elif not self.is_dynamic_active and self.context.is_dynamic_active(window.executable, window.title,
                                                                           window.handle):
            self.is_dynamic_active = True
            self.static_grammar_states = self.get_current_grammar_states()
            self.set_current_grammar_states(self.states_to_restore_on_window_focus)

    @staticmethod
    def apply_states_to_grammars(grammars, states):
        for grammar, enabled in zip(grammars, states):
            grammar.disable()
            if enabled:
                grammar.enable()

    def set_current_grammar_states(self, grammar_states):
        for name, grammars in self.grammars_grouped_by_module.iteritems():
            self.apply_states_to_grammars(grammars, grammar_states[name])


dynamic_module_names = ['chrome', 'pycharm', 'visual_studio']
dynamic_modules = {}
for mod_name in dynamic_module_names:
    try:
        logger.info('dynamic loading ' + mod_name)
        dynamic_modules[mod_name] = importlib.import_module(mod_name)
    except Exception as exception:
        what = traceback.format_exc()
        logger.exception(what)
dynamic_modules = {name: importlib.import_module(name) for name in dynamic_module_names}

dynamic_module_grammars = {name: dynamic_modules[name].EXPORT_GRAMMARS for name in dynamic_module_names}
citrix_context = AppContext(executable='notepad')
nomachine_context = AppContext(executable='nxplayer')
citrix_or_nomachine_context = citrix_context | nomachine_context

for mod_name, export_grammars in dynamic_module_grammars.iteritems():
    for gram in export_grammars:
        if not isinstance(gram._context, DynamicContext):
            gram._context = DynamicContext(fallback=gram._context, focus_context=citrix_or_nomachine_context)

manager = DynamicGrammarStateManager(dynamic_module_grammars, dynamic_modules,
                                     DynamicContext(fallback=None, focus_context=citrix_or_nomachine_context))
manager.register()

spoken_modules = {"chrome": "chrome", "pycharm": "pycharm", "visual studio": "visual_studio"}


class DynamicMappingRule(MappingRule):
    mapping = {
        "enable <module_name> grammar": Function(manager.dynamic_enable),
        "disable <module_name> grammar": Function(manager.dynamic_disable),
    }
    extras = [Choice("module_name", spoken_modules)]


dynamic_grammar = Grammar('dynamic grammar')
dynamic_grammar.add_rule(DynamicMappingRule())
dynamic_grammar.load()


# Unload function which will be called at unload time.
def unload():
    global dynamic_grammar
    if dynamic_grammar: dynamic_grammar.unload()
    dynamic_grammar = None

    global dynamic_modules
    if dynamic_modules:
        for name, module in dynamic_modules.iteritems():
            logger.info('dynamic unloading ' + name)
            module.unload()
    dynamic_modules = None
