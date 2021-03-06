import urwid

from core.hook import Hook
from ui import graphics
from ui.viewmodel import ViewModel, Topic


class HookBox(urwid.WidgetWrap):
    def __init__(self, model: ViewModel, parent: urwid.Frame):
        self.padding = 4
        self.parent = parent
        grid = urwid.GridFlow([], 1, self.padding, 0, 'left')
        padded_grid = urwid.Padding(grid, left=1)
        box = urwid.LineBox(padded_grid, tline='')
        super().__init__(box)
        self._data: ViewModel = None
        self.data = model

    def data(self, data: ViewModel):
        if self._data is not None:
            self._data.unregister(self)
        self._data = data
        self._data.register(self.on_update, topic=Topic.CURRENT_ENTRY)

    data = property(None, data)

    def on_update(self, model):
        with graphics.DRAW_LOCK:
            self._w.base_widget.contents = [(HookCell(hook), self._w.base_widget.options()) for hook in
                                            self._data.current_entry.hooks if hook.label]
            if len(self._w.base_widget.contents) > 0:
                self.update_cell_width()
                self.parent.footer = self
            else:
                self.parent.footer = None

    def update_cell_width(self):
        max_width = 0
        for width in [cell.width for cell, option in self._w.base_widget.contents]:
            max_width = max(max_width, width)
        self._w.base_widget.cell_width = max_width


class HookCell(urwid.WidgetWrap):
    def __init__(self, hook: Hook):
        markup, plain = get_hook_representation(hook)
        cell = urwid.Text(markup)
        self.width = len(plain)
        super().__init__(cell)


def get_hook_representation(hook: Hook):
    spacing = 4
    plain = f"{hook.key:<{spacing}}{hook.label}"
    markup = [('bold', f"{hook.key:<{spacing}}"), f"{hook.label}"]
    # TODO add attributes
    # attributes = [curses.A_UNDERLINE] * len(hook.key)
    # attributes.extend([curses.A_NORMAL] * (spacing - len(hook.key) + len(hook.label)))
    return markup, plain
