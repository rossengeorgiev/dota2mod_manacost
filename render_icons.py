#!/usr/bin/env python

import Image, ImageFont, ImageDraw
import sys, os
sys.path.append("./tools")
import KeyValue

fill_blue = "#1f496f"
fill_green = "#26721b"
font = ImageFont.truetype('Exo-SemiBold.ttf', 13)
src_image_path = "./src/items/"
presrc_image_path = "./prerendered_items/"
out_image_path = "./items/"

# clear output directory
if os.path.exists("./items"):
    for root, dirs, files in os.walk("./items"):
        for name in files:
            os.remove(os.path.join(root, name))
else:
    os.mkdir("./items")

# parse items.txt
items = KeyValue.parse(open("./src/items.txt"))['DOTAAbilities']

# find all items with mana or health requirements
for key in items:

    if type(items[key]) is not dict:
        continue

    item = items[key]

    if 'AbilityManaCost' not in item:
        continue

    cost = item['AbilityManaCost']
    color = fill_blue

    # some items require 0 mana, like blink or soul ring
    # however, there are special cases like soul ring
    if cost == '0':
        # ok, we look if the items sacrifice health, e.g. soul ring
        try:
            for skey in item['AbilitySpecial']:
                for sskey in item['AbilitySpecial'][skey]:
                    if sskey == "health_sacrifice":
                        cost = item['AbilitySpecial'][skey][sskey]
                        raise Exception("Found a sacrifice, lol") # quick and dirty way to exit the loops once we find a health_sacrifice entry
            continue
        except:
            color = fill_green # sacrifice health, health is green, we use green

    # handle items that are upgradable
    else:
        if cost.find(' ') != -1:
            costs = cost.split(' ')

            try:
                idx = int(key[-1]) - 1
            except:
                idx = 0

            cost = costs[idx]

    # center text in our little box
    text_pos_padding = (3 - len(cost)) * 4
    filename = key[5:]

    # open image
    if os.path.exists(os.path.join(presrc_image_path, "%s.png" % filename)):
        img = Image.open(os.path.join(presrc_image_path, "%s.png" % filename))
    else:
        img = Image.open(os.path.join(src_image_path, "%s.png" % filename))

    # add info in the bottom left corner
    d = ImageDraw.Draw(img)
    d.polygon([(0,50),(20,50),(25,64),(0,64)], fill=color)
    d.text((text_pos_padding,48), cost, font=font,fill="#ffffff")
    del d

    # save the image in the ouput directory
    img.save(os.path.join(out_image_path, "%s.png" % filename))
