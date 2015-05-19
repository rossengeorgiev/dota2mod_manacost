#!/usr/bin/env python

import os
import errno
import fnmatch
import shutil

from PIL import Image, ImageFont, ImageDraw
import vdf
import vpk

# configs
vpk_path = '/d/Steam/steamapps/common/dota 2 beta/dota/pak01_dir.vpk'
vpk_img_root = 'resource/flash3/images/'
fill_blue = "#1f496f"
fill_green = "#26721b"
font = ImageFont.truetype('Exo-SemiBold.ttf', 13)
src_root = "./src/"
src_preimages_root = "./prerendered_items/"
out_root = "./out/"


# helper functions
def mktree(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

# clear output directory
if os.path.exists("./out"):
    shutil.rmtree("./out")
mktree("./out/items")
mktree("./out/spellicons")

# load game asset index
pak1 = vpk.VPK(vpk_path)

# load items.txt schema and save a local copy to track in repo
with pak1.get_file("scripts/npc/items.txt") as vpkfile:
    vpkfile.save(os.path.join(src_root, 'items.txt'))
    items = vdf.load(vpkfile)['DOTAAbilities']

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

            # if manacost is 0, and item doesn't require health
            # there is no point rendering an image for that item
            continue
        except:
            color = fill_green  # sacrifice health, health is green, we use green

    # handle items that are upgradable (costs for each level is separated by whitespaces)
    else:
        if ' ' in cost:
            costs = cost.split(' ')

            try:
                idx = int(item_name[-1]) - 1  # e.g. item_dagon, item_dagon_2, item_dagon_3
            except:
                idx = 0

            cost = costs[idx]

    # center text in our little box
    text_pos_padding = (3 - len(cost)) * 4
    filename = "%s.png" % item_name[5:]  # removes 'item_' prefix

    # first we check for an available prerendered src image, and fallback to the ones from Dota 2
    image_src_path = os.path.join(src_preimages_root, filename)

    if os.path.exists(image_src_path):
        image_src_file = open(image_src_path, 'rb')
    else:
        image_src_file = pak1.get_file(os.path.join(vpk_img_root, "items", filename))

    # open the image
    img = Image.open(image_src_file)

    # add info in the bottom left corner
    d = ImageDraw.Draw(img)
    d.polygon([(0, 50), (20, 50), (25, 64), (0, 64)], fill=color)
    d.text((text_pos_padding, 48), cost, font=font, fill="#ffffff")
    del d

    # save the image in the ouput directory
    img.save(os.path.join(out_root, "items", filename))
    img.close()


# add color coded damage type in the top right corner

# RED physical
# BLUE magic
# PURPLE pure
dmg_type_color = {
    "DAMAGE_TYPE_PHYSICAL": "#FF0000",
    "DAMAGE_TYPE_MAGICAL": "#007FFF",
    "DAMAGE_TYPE_PURE": "#DF00FF",
}

# load npc_abilities.txt schema and save a local copy to track in repo
with pak1.get_file("scripts/npc/npc_abilities.txt") as vpkfile:
    vpkfile.save(os.path.join(src_root, 'npc_abilities.txt'))
    abilities = vdf.load(vpkfile)['DOTAAbilities']

src_files = [path for path in pak1 if path.startswith("resource/flash3/images/spellicons/")]

for name in abilities:

    if type(abilities[name]) is not dict:
        continue

    cur = abilities[name]

    if 'AbilityUnitDamageType' not in cur:
        continue
    if cur['AbilityUnitDamageType'] not in dmg_type_color:
        continue

    color = dmg_type_color[cur['AbilityUnitDamageType']]

    for filepath in fnmatch.filter(src_files, "*%s.png" % name):
        img = Image.open(pak1.get_file(filepath))

        d = ImageDraw.Draw(img)
        d.polygon([(128-42, 0), (128, 0), (128, 42)], fill="#191C22")
        d.polygon([(128-38, 0), (128, 0), (128, 38)], fill=color)
        del d

        # save the image in the ouput directory
        filepath = os.path.join(out_root, filepath.replace(vpk_img_root, ''))
        # recreate the relative path
        mktree(os.path.join(*filepath.split('/')[:-1]))

        img.save(filepath)
        img.close()
