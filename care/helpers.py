from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.conf import settings

FONT = 'ARIAL.TTF'

def add_watermark(in_file, text, out_file='watermark.jpg', angle=23, opacity=0.25):
	print in_file
	img = Image.open(in_file).convert('RGB')
	watermark = Image.new('RGBA', img.size, (0,0,0,0))
	size = 2
	print settings.STATIC_ROOT + "css/" + FONT
	n_font = ImageFont.truetype(settings.STATIC_ROOT + "css/" + FONT, size)
	n_width, n_height = n_font.getsize(text)
	while n_width+n_height < watermark.size[0]:
		size += 2
		n_font = ImageFont.truetype(settings.STATIC_ROOT + "css/" + FONT, size)
		n_width, n_height = n_font.getsize(text)
	draw = ImageDraw.Draw(watermark, 'RGBA')
	draw.text(((watermark.size[0] - n_width) / 2,
			  (watermark.size[1] - n_height) / 2),
			  text, font=n_font)
	watermark = watermark.rotate(angle,Image.BICUBIC)
	alpha = watermark.split()[3]
	alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
	watermark.putalpha(alpha)
	Image.composite(watermark, img, watermark).save(out_file, 'JPEG')