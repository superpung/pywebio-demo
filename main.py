import pyperclip
from pywebio import pin, start_server
from pywebio.output import (
    clear,
    put_button,
    put_buttons,
    put_markdown,
    put_row,
    put_scope,
    put_text,
)
from pywebio.pin import put_textarea

from algo import algo1, algo2


class AutoSwitch:
    def __init__(self) -> None:
        self.on = False  # Set default to on or off

    def on_click(self):
        self.on = not self.on
        self.put_ui()

    def put_ui(self):
        clear("auto_transform_switch")
        _button_label = "开" if self.on else "关"
        _button_color = "success" if self.on else "info"
        put_button(
            _button_label,
            color=_button_color,
            onclick=self.on_click,
            scope="auto_transform_switch",
        )


class AlgoManager:
    def __init__(self) -> None:
        self.algo = algo1

    def set_algo(self, algo):
        self.algo = algo
        self.put_ui()

    def put_ui(self):
        clear("algo_switch")
        active_button_color = "success"
        inactive_button_color = "light"
        put_buttons(
            [
                {
                    "label": algo1.__name__,
                    "value": algo1,
                    "color": active_button_color
                    if self.algo.__name__ == algo1.__name__
                    else inactive_button_color,
                },
                {
                    "label": algo2.__name__,
                    "value": algo2,
                    "color": active_button_color
                    if self.algo.__name__ == algo2.__name__
                    else inactive_button_color,
                },
            ],
            onclick=self.set_algo,
            scope="algo_switch",
        )


auto_switch = AutoSwitch()
algo_manager = AlgoManager()


def _update_output(input_text="", load_from_input=False):
    if load_from_input:
        pin.pin_update("output", value=algo_manager.algo(pin.pin["input"]))
    else:
        pin.pin_update("output", value=algo_manager.algo(input_text))


def manual_updat_output():
    _update_output(load_from_input=True)


def auto_update_output_when_on(input_text):
    if auto_switch.on:
        _update_output(input_text)


def copy_output():
    pyperclip.copy(pin.pin["output"])
    put_text("Copied!")


def main():
    put_markdown("# 标题可替换").style("text-align: center")

    put_row(
        [
            put_text("自动运行").style(
                "text-align: right; margin-right: 20px; font-size: 20px"
            ),
            put_scope("auto_transform_switch"),
        ]
    )
    auto_switch.put_ui()

    put_scope("algo_switch")

    algo_manager.put_ui()

    put_row(
        [
            put_textarea(name="input", rows=20, scope="input_area"),
            put_textarea(name="output", rows=20, scope="output_area"),
        ]
    )
    put_row(
        [
            put_button("运行", color="light", onclick=manual_updat_output).style(
                "display: flex; justify-content: flex-end;"
            ),
            put_button("拷贝", color="light", onclick=copy_output),
        ]
    )

    pin.pin_on_change("input", onchange=auto_update_output_when_on)


if __name__ == "__main__":
    start_server(main, port=7777, debug=True)
