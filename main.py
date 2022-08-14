import os
import platform
import shutil
import subprocess
from pathlib import Path

import flet
import log
import requests
from flet import Column, ElevatedButton, Image, Page, Row, Text, TextField


PREVIEW_URL = "https://api.memegen.link/images/preview.jpg"
CREATE_URL = "https://api.memegen.link/images"

DOWNLOADS_PATH = Path.home() / "Downloads"


def main(page: Page):
    page.title = "Memegen.link Flet Client"
    page.padding = 50
    page.update()

    def update_preview(e):
        preview.src = (
            PREVIEW_URL
            + f"?template={template.value}"
            + f"&text[]={line_1.value or ' '}"
            + f"&text[]={line_2.value or ' '}"
        )
        page.update()

    def download_image(e):
        response = requests.post(
            CREATE_URL,
            data={
                "template_id": template.value,
                "text": [line_1.value, line_2.value],
                "extension": "png",
                "redirect": True,
            },
            stream=True,
        )
        if response.status_code != 201:
            log.error(f"API response: {response}")
            return

        path = DOWNLOADS_PATH / f"{template.value or 'meme'}.png"
        with path.open("wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        launch(path)

    template = TextField(label="Template", on_change=update_preview)
    line_1 = TextField(label="Line one", on_change=update_preview)
    line_2 = TextField(label="Line two", on_change=update_preview)
    preview = Image(src=PREVIEW_URL, height=250)
    button = ElevatedButton("Download Image", on_click=download_image)

    page.add(
        Row(
            [
                Column([template, line_1, line_2]),
                Column([preview]),
            ],
            alignment="spaceBetween",
        ),
        button,
    )


def launch(path: Path):
    path = str(path)
    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", path))
    elif platform.system() == "Windows":  # Windows
        os.startfile(path)
    else:  # Linux variants
        subprocess.call(("xdg-open", path))


flet.app(target=main)
