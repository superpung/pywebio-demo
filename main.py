import pyperclip
from pywebio import pin, start_server
from pywebio.output import (
    clear,
    put_button,
    put_markdown,
    put_row,
    put_scope,
    put_text,
)
from pywebio.pin import put_textarea

from algo import algo


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


auto_switch = AutoSwitch()


def _update_output(input_text="", load_from_input=False):
    if load_from_input:
        pin.pin_update("output", value=algo(pin.pin["input"]))
    else:
        pin.pin_update("output", value=algo(input_text))


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
