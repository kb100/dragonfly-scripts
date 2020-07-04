import importlib

from dragonfly import *


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
        self.states_to_restore_on_window_focus = {name: [False for grammar in grammars]
                                                  for name, grammars in grammars_grouped_by_module.iteritems()}
        self.states_to_restore_on_manual_enable = self.get_current_grammar_states()
        self.module_is_enabled = {name: False for name in grammars_grouped_by_module}

    def dynamic_enable(self, module_name):
        print "dynamic enable", module_name
        if self.module_is_enabled[module_name]:
            return
        self.module_is_enabled[module_name] = True
        print self.states_to_restore_on_manual_enable[module_name]
        self.apply_states_to_grammars(self.grammars_grouped_by_module[module_name],
                                      self.states_to_restore_on_manual_enable[module_name])
        for name in self.grammars_grouped_by_module:
            if name == module_name:
                continue
            self.dynamic_disable(name)

    def dynamic_disable(self, module_name):
        print "dynamic disable", module_name
        if not self.module_is_enabled[module_name]:
            return
        self.module_is_enabled[module_name] = False
        self.states_to_restore_on_manual_enable[module_name] = [grammar.enabled for grammar in
                                                                self.grammars_grouped_by_module[module_name]]
        self.apply_states_to_grammars(self.grammars_grouped_by_module[module_name],
                                      [False for grammar in self.grammars_grouped_by_module[module_name]])

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

    def apply_states_to_grammars(self, grammars, states):
        for grammar, enabled in zip(grammars, states):
            grammar.disable()
            if enabled:
                grammar.enable()

    def set_current_grammar_states(self, grammar_states):
        for name, grammars in self.grammars_grouped_by_module.iteritems():
            self.apply_states_to_grammars(grammars, grammar_states[name])


dynamic_module_names = ["_chrome", "_gvim"]
dynamic_modules = {name: importlib.import_module(name) for name in dynamic_module_names}
dynamic_module_grammars = {name: dynamic_modules[name].EXPORT_GRAMMARS for name in dynamic_module_names}
citrix_context = AppContext(executable='notepad')
nomachine_context = AppContext(executable='nxplayer')
focus_context = citrix_context | nomachine_context

for name, grammars in dynamic_module_grammars.iteritems():
    for grammar in grammars:
        grammar._context = DynamicContext(fallback=grammar._context, focus_context=focus_context)

manager = DynamicGrammarStateManager(dynamic_module_grammars, dynamic_modules,
                                     DynamicContext(fallback=None, focus_context=focus_context))
manager.register()

spoken_modules = {"chrome": "_chrome", "(pycharm|gvim)": "_gvim"}


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

# if __name__ == '__main__':
#     print dir(Window.get_foreground())
#     print dynamic_module_grammars
