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
vpk_img_root = 'resource/flash3/images'
fill_blue = "#1f496f"
fill_green = "#26721b"
fill_gold = "#7a4b4e"
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
mktree("./out/manacost/items")
mktree("./out/goldcost/items")
mktree("./out/combined/items")
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

    filename = "%s.png" % item_name[5:]  # removes 'item_' prefix

    # skip recipies, since they all sahre the same icon image
    if filename.startswith("recipe_"):
        continue

    # first we check for an available prerendered src image, and fallback to the ones from Dota 2
    image_src_path = os.path.join(src_preimages_root, filename)

    if os.path.exists(image_src_path):
        image_src_file = open(image_src_path, 'rb')
    else:
        image_src_file = pak1.get_file('/'.join([vpk_img_root, "items", filename]))

    manacost_img = None
    color = fill_blue
    # generate manacost banner
    if 'AbilityManaCost' in item:
        manacost = item['AbilityManaCost']

        # some items require 0 mana, like 'blink dagger' or 'soul ring'
        if manacost == '0':
            # ok, we look if the items sacrifice health, e.g. soul ring
            try:
                for xv in item['AbilitySpecial'].itervalues():
                    if type(xv) is not dict:
                        continue

                    if "health_sacrifice" in xv:
                        manacost = xv['health_sacrifice']
                        raise Exception
            except:
                color = fill_green  # sacrifice health, health is green, we use green

        # handle items that are upgradable (manacosts for each level is separated by whitespaces)
        else:
            if ' ' in manacost:
                manacosts = manacost.split(' ')

                try:
                    idx = int(item_name[-1]) - 1  # e.g. item_dagon, item_dagon_2, item_dagon_3
                except:
                    idx = 0

                manacost = manacosts[idx]

        if manacost != '0':
            # center text in our little box
            text_pos_padding = (3 - len(manacost)) * 4

            # open the image
            manacost_img = Image.open(image_src_file)

            # add info in the bottom left corner
            d = ImageDraw.Draw(manacost_img)
            d.polygon([(0, 50), (20, 50), (25, 64), (0, 64)], fill=color)
            d.text((text_pos_padding, 49), manacost, font=font, fill="#ffffff")
            del d

            # save the image in the ouput directory
            savepath = out_root, 'manacost', 'items', filename
            mktree(os.path.join(*savepath[:-1]))
            manacost_img.save(os.path.join(*savepath))

    # generate itemcost banner
    if 'ItemCost' not in item or item['ItemCost'] == '0':
        continue

    image_src_file.seek(0)
    itemcost_img = Image.open(image_src_file)

    pad = 8 * len(item['ItemCost'])

    d = ImageDraw.Draw(itemcost_img)
    d.polygon([(84-pad, 50), (88, 50), (88, 64), (82-pad, 64)], fill=fill_gold)
    d.text((86-pad, 49), item['ItemCost'], font=font, fill='#ffffff')
    del d

    savepath = out_root, 'goldcost', 'items', filename
    mktree(os.path.join(*savepath[:-1]))
    itemcost_img.save(os.path.join(*savepath))

    # generate combined version if needed
    if manacost_img is not None:
        manacost_img.paste(Image.new("RGBA", (124, 64), (0, 0, 0, 0)), (30, 0))
        itemcost_img.paste(manacost_img, manacost_img)

    savepath = out_root, 'combined', 'items', filename
    mktree(os.path.join(*savepath[:-1]))
    itemcost_img.save(os.path.join(*savepath))


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
        filepath = os.path.split(os.path.join(out_root, filepath.replace(vpk_img_root+'/', '')))
        # recreate the relative path
        mktree(os.path.join(*filepath[:-1]))

        img.save(os.path.join(*filepath))
        img.close()
