#!/usr/bin/env python

from PIL import Image, ImageFont, ImageDraw
import sys, os, fnmatch, shutil
sys.path.append("./tools")
import vdf

# configs
fill_blue = "#1f496f"
fill_green = "#26721b"
font = ImageFont.truetype('Exo-SemiBold.ttf', 13)
src_image_root = "./src/"
src_preimages_root = "./prerendered_items/"
out_image_root = "./out/"

# clear output directory
if os.path.exists("./out"):
    shutil.rmtree("./out")
os.mkdir("./out")
os.mkdir("./out/items")
os.mkdir("./out/spellicons")

# parse items.txt
items = vdf.parse(open("./src/items.txt"))['DOTAAbilities']

# find all items with mana or health requirements
for item_name in items:

    if type(items[item_name]) is not dict:
        continue

    item = items[item_name]

    if 'AbilityManaCost' not in item:
        continue

    cost = item['AbilityManaCost']
    color = fill_blue

    # some items require 0 mana, like 'blink dagger' or 'soul ring'
    if cost == '0':
        # ok, we look if the items sacrifice health, e.g. soul ring
        try:
            for xv in item['AbilitySpecial'].itervalues():
                if type(xv) is not dict:
                    continue

                if "health_sacrifice" in xv:
                    cost = xv['health_sacrifice']
                    raise Exception

            # if manacost is 0, and item doesn't require health there is no point rendering an image for that item
            continue
        except:
            color = fill_green # sacrifice health, health is green, we use green

    # handle items that are upgradable (costs for each level is separated by whitespaces)
    else:
        if ' ' in cost:
            costs = cost.split(' ')

            try:
                idx = int(item_name[-1]) - 1 #e.g. item_dagon, item_dagon_2, item_dagon_3
            except:
                idx = 0

            cost = costs[idx]

    # center text in our little box
    text_pos_padding = (3 - len(cost)) * 4
    filename = "%s.png" % item_name[5:] # removes 'item_' prefix

    # first we check for an available prerendered src image, and fallback to the ones from Dota
    image_src_path = os.path.join(src_preimages_root, filename)

    if not os.path.exists(image_src_path):
        image_src_path = os.path.join(src_image_root, "items", filename)

    # open the image
    img = Image.open(image_src_path);

    # add info in the bottom left corner
    d = ImageDraw.Draw(img)
    d.polygon([(0,50),(20,50),(25,64),(0,64)], fill=color)
    d.text((text_pos_padding,48), cost, font=font,fill="#ffffff")
    del d

    # save the image in the ouput directory
    img.save(os.path.join(out_image_root, "items", filename))


# add color coded damage type in the top right corner

# RED physical
# BLUE magic
# PURPLE pure
dmg_type_color = {
    "DAMAGE_TYPE_PHYSICAL": "#FF0000",
    "DAMAGE_TYPE_MAGICAL": "#007FFF",
    "DAMAGE_TYPE_PURE": "#DF00FF",
}

abilities = vdf.parse(open("./src/npc_abilities.txt"))['DOTAAbilities']
src_files = os.walk(os.path.join(src_image_root, "spellicons"), topdown=True).next()[2]

for name in abilities:

    if type(abilities[name]) is not dict:
        continue

    cur = abilities[name]

    if 'AbilityUnitDamageType' not in cur:
        continue
    if cur['AbilityUnitDamageType'] not in dmg_type_color:
        continue

    color = dmg_type_color[cur['AbilityUnitDamageType']]

    for filename in fnmatch.filter(src_files, "%s*" % name):
        img = Image.open(os.path.join(src_image_root,"spellicons",filename));

        d = ImageDraw.Draw(img)
        d.polygon([(128-42,0),(128,0),(128,42)], fill="#191C22")
        d.polygon([(128-38,0),(128,0),(128,38)], fill=color)
        del d

        # save the image in the ouput directory
        img.save(os.path.join(out_image_root, "spellicons", filename))
