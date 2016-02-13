#!/usr/bin/env python

from PIL import Image, ImageOps, ImageDraw, ImageFont

final_size = (600, 600)
profile_image_size = (150, 150)
social_image_size = (50, 50)
text_size = (final_size[0], 26)
edge_padding = 10

def resize_aspect_fill(f_in, f_out='tmp/cropped_image.png', size=final_size):
	image = Image.open(f_in)
	image.thumbnail(size, Image.ANTIALIAS)
	thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))
	thumb.save(f_out)
	return f_out

def rounded_thumbnail(f_in, f_out='tmp/rounded_thumbnail.png', size=profile_image_size):
	mask = Image.new('L', size, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + size, fill=255)
	im = Image.open(f_in)
	output = ImageOps.fit(im, mask.size, Image.ANTIALIAS, (0.5, 0.5))
	output.putalpha(mask)
	output.save(f_out)
	return f_out

def draw_text(text='Sample Name', f_out='tmp/profile_name.png', size=text_size):
	img = Image.new('RGBA', text_size)
	draw = ImageDraw.Draw(img) 
	font = ImageFont.truetype('fonts/Helvetica.ttf', text_size[1])
	draw.text((0, 0), text, (255, 255, 255), font=font)
	img.save(f_out)
	return f_out

def composite_full_image(main_image_file, profile_image_file, profile_name, social_image_file, size=final_size):
	canvas = Image.new('RGBA', final_size, (255, 255, 255, 255))
	main_image = Image.open(resize_aspect_fill(main_image_file))
	canvas.paste(main_image, (0, 0)) # Paste main image in to context 'canvas'

	profile_thumbnail = Image.open(rounded_thumbnail(profile_image_file))
	thumbnail_x, thumbnail_y = profile_thumbnail.size
	profile_thumbnail.thumbnail((thumbnail_x/2, thumbnail_y/2), Image.ANTIALIAS)
	canvas.paste(profile_thumbnail, (edge_padding, edge_padding), profile_thumbnail) # Paste profile thumbnail, second time 'profile_image' is passed, it acts like a mask

	username_image = Image.open(draw_text(profile_name))
	username_x, username_y = username_image.size
	username_image.thumbnail((username_x, username_y), Image.ANTIALIAS)
	origin_x = (thumbnail_x/2) + 2*edge_padding
	origin_y = (thumbnail_y/2)/2 # Vertically aligned with profile image
	canvas.paste(username_image, ( origin_x, origin_y), username_image) # Paste profile thumbnail, second time 'profile_image' is passed, it acts like a mask

	social_image = Image.open(social_image_file)
	social_x, social_y = social_image_size # Set at the top of the file
	social_image.thumbnail((social_x, social_y), Image.ANTIALIAS)
	origin_x = final_size[0] - social_x - edge_padding
	origin_y = final_size[1] - social_y	- edge_padding
	canvas.paste(social_image, (origin_x, origin_y), social_image) # Paste social thumbnail icon, second time 'social_image' is passed, it acts like a mask

	output_file = 'tmp/final_image.png' 
	canvas.save(output_file)
	return output_file

final_output = composite_full_image('images/image001.png', 'images/image002.png', 'Drunk Uncle', 'images/social-instagram.png')
print final_output
