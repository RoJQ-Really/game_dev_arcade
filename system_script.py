import pathlib

from PIL import ImageDraw, Image, ImageFont


def _draw_button_texture(path_to_font: pathlib.Path, size: int, color, text, margin: int = 3, radius: int = 15) -> Image.Image:
    fnt = ImageFont.truetype(path_to_font, size, encoding="UTF-8")
    text_size = fnt.getbbox(text)  # Получаем ограничивающую рамку

    im_width = text_size[2]
    im_height = text_size[3]
    new_image = Image.new("RGBA", size=(im_width + margin*2, im_height + margin*2), color=color)

    do_draw = ImageDraw.Draw(new_image, "RGBA")
    rounded_rectangle_size = (0, 0, text_size[2] + margin, text_size[3] + margin)
    do_draw.rounded_rectangle(xy=rounded_rectangle_size, fill="orange", radius=radius)

    do_draw.text((margin * 2 + 1, 0), text, font=fnt)

    return new_image

