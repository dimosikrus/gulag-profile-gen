#import block
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

uid = int(input("user id (3-34) = "))
#domain = 'nyalachai.ga'
domain = 'okayu.me'
umode = int(input("modes:\n0 = vn!std\n4 = rx!std\n8 = ap!std\n1 = vn!taiko\n5 = rx!taiko\n2 = vn!catch\n6 = rx!catch\n3 = vn!mania\ninput mode: "))

reqa = requests.get(f'https://api.{domain}/get_player_info?id={uid}&scope=all').json()

#request var block
nickname = reqa['player']['info']['name']
pp = reqa['player']['stats'][f'{umode}']['pp']
xah = reqa['player']['stats'][f'{umode}']['xh_count']
xa = reqa['player']['stats'][f'{umode}']['x_count']
sah = reqa['player']['stats'][f'{umode}']['sh_count']
sa = reqa['player']['stats'][f'{umode}']['s_count']
a = reqa['player']['stats'][f'{umode}']['a_count']
acc = reqa['player']['stats'][f'{umode}']['acc']
top = reqa['player']['stats'][f'{umode}']['rank']
ctop = reqa['player']['stats'][f'{umode}']['country_rank']
country = reqa['player']['info']['country']
country = str.upper(country)
acc = round(acc, 2)
acc = str(f'{acc}%')

#format 999+1 block
pp = '{:,}'.format(pp).replace(',', ' ')
xah = '{:,}'.format(xah).replace(',', ' ')
xa = '{:,}'.format(xa).replace(',', ' ')
sah = '{:,}'.format(sah).replace(',', ' ')
sa = '{:,}'.format(sa).replace(',', ' ')
a = '{:,}'.format(a).replace(',', ' ')
top = '{:,}'.format(top).replace(',', ' ')
ctop = '{:,}'.format(ctop).replace(',', ' ')

#font block
font1 = ImageFont.truetype("arial.ttf", 40)
font2 = ImageFont.truetype("arial.ttf", 35)
font3 = ImageFont.truetype("arial.ttf", 30)

#function with corners radius
def add_corners(hium, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', hium.size, 255)
    w, h = hium.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    hium.putalpha(alpha)
    return hium

#user mode int to str
if umode == 0:
    mmode = 'vn!std'
elif umode == 1:
    mmode = 'vn!taiko'
elif umode == 2:
    mmode = 'vn!catch'
elif umode == 3:
    mmode = 'vn!mania'
elif umode == 4:
    mmode = 'rx!std'
elif umode == 5:
    mmode = 'rx!taiko'
elif umode == 6:
    mmode = 'rx!catch'
elif umode == 8:
    mmode = 'ap!std'
else:
    mmode = 'error'

#images block
img = Image.open('profile3.png')
rescimg =requests.get(f'https://osu.{domain}/static/images/flags/{country}.png')
cimg = Image.open(BytesIO(rescimg.content))
respimg = requests.get(f'https://a.{domain}/{uid}')
pimg = Image.open(BytesIO(respimg.content))
newpimg = pimg.resize((184,184))
hium =  add_corners(newpimg, 40)

#put images block
img.paste(cimg, (235,60), mask=cimg)
img.paste(hium, (25, 24), mask=hium)
d = ImageDraw.Draw(img)

#fontsize block (for center text)
ppw, qwe = d.textsize(pp, font=font2)
accw, qwe = d.textsize(acc, font=font2)
xahw, qwe = d.textsize(xah, font=font2)
xaw, qwe = d.textsize(xa, font=font2)
sahw, qwe = d.textsize(sah, font=font2)
saw, qwe = d.textsize(sa, font=font2)
aw, qwe = d.textsize(a, font=font2)
topw, qwe = d.textsize(top, font=font2)
ctopw, qwe = d.textsize(ctop, font=font2)

#put text block
d.text((320,61), nickname, fill=(255, 255, 255), font=font1)
d.text((650,250), "PP", fill=(255, 255, 255), font=font2)
d.text((672-(ppw/2),300), pp, fill=(240, 219, 228), font=font2)
d.text((276-(xahw/2),460), xah, fill=(255, 255, 255), font=font3)
d.text((406-(xaw/2),460), xa, fill=(255, 255, 255), font=font3)
d.text((539-(sahw/2),460), sah, fill=(255, 255, 255), font=font3)
d.text((672-(saw/2),460), sa, fill=(255, 255, 255), font=font3)
d.text((805-(aw/2),460), a, fill=(255, 255, 255), font=font3)
d.text((50,250), "Топ в мире", fill=(255, 255, 255), font=font2)
d.text((128-(topw/2),300), top, fill=(240, 219, 228), font=font2)
d.text((290,250), "Топ по стране", fill=(255, 255, 255), font=font2)
d.text((400-(ctopw/2),300), ctop, fill=(240, 219, 228), font=font2)
d.text((235,130), f'{mmode}', fill=(240, 219, 228), font=font1)
d.text((850,250), "Acc", fill=(255, 255, 255), font=font2)
d.text((885-(accw/2),300), acc, fill=(240, 219, 228), font=font2)

 #save block
img.save(f'U{uid}-M{umode}.png')