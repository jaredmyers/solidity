
'''
Art Generation

Ordering:
SWORDS, BASE, SCARS, TATTOOS, EYEBROWS, MOUTH, EYES, GLASSES, HEADGEAR

jjm
'''
from svgimgutils import SVGImgUtils
import glob
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import random
import collections
import json

# - Paths -
completed_art = '/Users/ice/Desktop/nft_stuff/art/'
metadata = '/Users/ice/Desktop/nft_stuff/metadata/'
tmp = '/Users/ice/Desktop/nft_stuff/tmp/'

metadata_template = '/Users/ice/Desktop/nft_stuff/data_template.json'

attr_root = '/Users/ice/Desktop/nft_stuff/attributes/'
base_root = attr_root + 'base/'
eyes_root = attr_root + 'eyes/'
mouth_root = attr_root + 'mouth/'
headgear_root = attr_root + 'headgear/'
scars_root = attr_root + 'scars/'
tattoo_root = attr_root + 'tattoos/'
eyebrows_root = attr_root + 'eyebrows/'
glasses_root = attr_root + 'glasses/'
swords_root = attr_root + 'swords/'

filenames_dict = {'base_filenames': os.listdir(base_root),
    'eyes_filenames': os.listdir(eyes_root),
    'mouth_filenames': os.listdir(mouth_root),
    'headgear_filenames': os.listdir(headgear_root),
    'scars_filenames': os.listdir(scars_root),
    'tattoo_filenames': os.listdir(tattoo_root),
    'eyebrows_filenames': os.listdir(eyebrows_root),
    'glasses_filenames': os.listdir(glasses_root),
    'swords_filenames': os.listdir(swords_root)
    }


def output_metadata(selected_attrs, token_id):
    '''create the metadata for the corresponding nft'''
    # mandatory attrs: ['base_filenames', 'eyes_filenames', 'mouth_filenames', 'eyebrows_filenames']
    # random attrs: ['headgear_filenames', 'scars_filenames', 'tattoo_filenames', 'glasses_filenames', 'swords_filenames']

    # load up template
    with open(metadata_template, 'r') as file:
        template = json.load(file)

    template['name'] = f'BosomBuddy #{token_id}'
    template['tokenId'] = int(token_id)

    # mandatory first
    template['attributes'][0]['trait_type'] = 'Body'
    template['attributes'][0]['value'] = selected_attrs['base_filenames'].split('.')[0]

    template['attributes'].append({'trait_type': 'Eyes', 'value': selected_attrs['eyes_filenames'].split('.')[0]})
    template['attributes'].append({'trait_type': 'Mouth', 'value': selected_attrs['mouth_filenames'].split('.')[0]})
    template['attributes'].append({'trait_type': 'EyeBrows', 'value': selected_attrs['eyebrows_filenames'].split('.')[0]})

    mandatory = ['base_filenames', 'eyes_filenames', 'mouth_filenames', 'eyebrows_filenames']

    for key in selected_attrs:
        if key not in mandatory:
            category = key.split('_')[0].capitalize()
            template['attributes'].append({'trait_type': category, 'value': selected_attrs[key].split('.')[0]})
    
    with open(metadata + token_id, 'w') as file:
        json.dump(template, file)


def use_svg(selected_attrs, filename):
    '''
    uses svgimgutils to merge svgs    
    '''
    # Create SVG Image Utils for each SVG image 
    base_template = SVGImgUtils.fromfile(base_root + selected_attrs['base_filenames'])

    # In proper layering order of:
    # SWORDS, BASE, SCARS, TATTOOS, EYEBROWS, MOUTH, EYES, GLASSES, HEADGEAR
    #if 'swords_filenames' in selected_attrs:
    #    swords = SVGImgUtils.fromfile(swords_root + selected_attrs['swords_filenames'])
    #    base_template.append(swords)

    if 'scars_filenames' in selected_attrs:
        scars = SVGImgUtils.fromfile(scars_root + selected_attrs['scars_filenames'])
        base_template.append(scars)

    if 'tattoo_filenames' in selected_attrs:
        tattoo = SVGImgUtils.fromfile(tattoo_root + selected_attrs['tattoo_filenames'])
        base_template.append(tattoo)

    eyebrows = SVGImgUtils.fromfile(eyebrows_root + selected_attrs['eyebrows_filenames'])
    base_template.append(eyebrows)

    mouth = SVGImgUtils.fromfile(mouth_root + selected_attrs['mouth_filenames'])
    base_template.append(mouth)

    eyes = SVGImgUtils.fromfile(eyes_root + selected_attrs['eyes_filenames'])
    base_template.append(eyes)

    if 'glasses_filenames' in selected_attrs:
        glasses = SVGImgUtils.fromfile(glasses_root + selected_attrs['glasses_filenames'])
        base_template.append(glasses)

    if 'headgear_filenames' in selected_attrs:
        headgear = SVGImgUtils.fromfile(headgear_root + selected_attrs['headgear_filenames'])
        base_template.append(headgear)

    # Save new merged SVG image
    base_template.save(completed_art+filename)

    truncate_ext = filename.split('.')
    token_id = truncate_ext[0]
    output_metadata(selected_attrs, token_id)


# Main Entry #
'''
SWORDS, BASE, SCARS, TATTOOS, EYEBROWS, MOUTH, EYES, GLASSES, HEADGEAR
'''
desired_amount = 50
count = 0
mandatory_attr_categories = ['base_filenames', 'eyes_filenames', 'mouth_filenames', 'eyebrows_filenames']
random_attr_categories = ['headgear_filenames', 'scars_filenames', 'tattoo_filenames', 'glasses_filenames', 'swords_filenames']
selected_attrs = {}
check_for_dups = []

while count <= desired_amount:

    # randomly select an attribute from each of mandatory attribute categories
    for mand in mandatory_attr_categories:
        rando_idx = (random.randint(0, len(filenames_dict[mand])-1))
        selected_attrs[mand] = filenames_dict[mand][rando_idx]
    
    # randomly select a number for additional attributes categories
    rando_category_number = random.randint(0, len(random_attr_categories)-1)

    for num in range(rando_category_number):
        # select an attr category at random
        rando_idx = random.randint(0, len(random_attr_categories)-1)
        selected_category = random_attr_categories[rando_idx]

        rando_idx = random.randint(0, len(filenames_dict[selected_category])-1)
        selected_attrs[selected_category] = filenames_dict[selected_category][rando_idx]

    # puttinng selections in tmp for duplicate comparison
    tmp = []
    for i in selected_attrs.values():
        tmp.append(i)
    
    # checking for duplicates by comparing to longer term storage
    is_duplicate = False
    for i in check_for_dups:
        if collections.Counter(i) == collections.Counter(tmp):
            is_duplicate = True
            break
    
    if not is_duplicate:
        check_for_dups.append(tmp)
    
        # generate the image, write svgs to filesystem   
        filename = str(count+1) + '.svg'
        use_svg(selected_attrs, filename)

        count = count + 1
