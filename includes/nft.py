import re
from PIL import Image
import os
import json
import yaml

config = ''
with open("./includes/config.yaml", 'r') as file:
  config = yaml.safe_load(file)

class Nft:
    metadata = ''
    number = 0
    layers = ''
    dnaPaths = ''
    folder_path = ''
    attributes_count = 0
    filteredAttributes = []

    def __init__(self, number, name, attributes, filteredAttributes,jsonTemplate, dnaPath, layers, attributes_count, folder_path, nft_type):
        self.metadata = jsonTemplate
        self.dnaPaths = dnaPath
        self.layers = layers
        self.name = name
        self.attributes = attributes
        self.filteredAttributes = filteredAttributes
        self.number = number
        self.folder_path = folder_path
        self.attributes_count = attributes_count
        self.nft_type = nft_type

    def CreateImage(self):
        self.layers = ['0-Background', '1-Neck', '2-Clothing', '3-Skin', '4-Skull', '5-Face Plate', '6-Eyes', '7-Head']
        subdirectory = ''
        need_reorder = False
        need_reverse_reorder = self.Check_Reverse_Reorder()
        need_reorder_eyes = False

        self.Check_Black()
        shadowPath = self.dnaPaths[2][:-4] + "_black" + self.dnaPaths[2][-4:]

        if 'man' in self.nft_type:
            subdirectory = 'Man/'
            need_reorder = self.Check_Reorder()
            need_reorder_eyes = self.Reorder_Eyes_Man()
        elif 'female' in self.nft_type:
            subdirectory = 'Female/'
            need_reorder_eyes = self.Reorder_Eyes_Female()

        if need_reorder:
            layer_to_move = self.layers.pop(7)
            dna_to_move = self.dnaPaths.pop(7)
            self.layers.insert(1, layer_to_move)
            self.dnaPaths.insert(1, dna_to_move)

        if need_reorder_eyes:
            layer_to_move = self.layers.pop(7)
            dna_to_move = self.dnaPaths.pop(7)
            self.layers.insert(6, layer_to_move)
            self.dnaPaths.insert(6, dna_to_move)
            
        baseLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + self.layers[0] + '/' + self.dnaPaths[0])
        baseLayer = baseLayer.convert('RGBA')

        # Insert Shadows
        frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '2-Clothing/' + shadowPath)
        frontLayer = frontLayer.convert('RGBA')
        baseLayer = Image.alpha_composite(baseLayer, frontLayer)

        for i in range(1, len(self.layers)):
            if need_reverse_reorder and i == 1:
                if '3-Einstein A.png' in self.dnaPaths:
                    frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/3-Einstein B.png')
                    frontLayer = frontLayer.convert('RGBA')
                    baseLayer = Image.alpha_composite(baseLayer, frontLayer)
                elif '2-Viking Grey A.png' in self.dnaPaths:
                    frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/2-Viking Grey B.png')
                    frontLayer = frontLayer.convert('RGBA')
                    baseLayer = Image.alpha_composite(baseLayer, frontLayer)
                elif '3-Viking Brown A.png' in self.dnaPaths:
                    frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/3-Viking Brown B.png')
                    frontLayer = frontLayer.convert('RGBA')
                    baseLayer = Image.alpha_composite(baseLayer, frontLayer)
                elif '4-Fro A.png' in self.dnaPaths:
                    frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/4-Fro B.png')
                    frontLayer = frontLayer.convert('RGBA')
                    baseLayer = Image.alpha_composite(baseLayer, frontLayer)
                
                # Insert Shadows
                frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '2-Clothing/' + shadowPath)
                frontLayer = frontLayer.convert('RGBA')
                baseLayer = Image.alpha_composite(baseLayer, frontLayer)
         
            frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + self.layers[i] + '/' + self.dnaPaths[i])
            frontLayer = frontLayer.convert('RGBA')
            baseLayer = Image.alpha_composite(baseLayer, frontLayer)

        # Applies for Einstein, Viking, Fro
        if need_reorder:
            if '3-Einstein B.png' in self.dnaPaths:
                frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/3-Einstein A.png')
                frontLayer = frontLayer.convert('RGBA')
                baseLayer = Image.alpha_composite(baseLayer, frontLayer)
            elif '2-Viking Grey B.png' in self.dnaPaths:
                frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/2-Viking Grey A.png')
                frontLayer = frontLayer.convert('RGBA')
                baseLayer = Image.alpha_composite(baseLayer, frontLayer)
            elif '3-Viking Brown B.png' in self.dnaPaths:
                frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/3-Viking Brown A.png')
                frontLayer = frontLayer.convert('RGBA')
                baseLayer = Image.alpha_composite(baseLayer, frontLayer)
            elif '4-Fro B.png' in self.dnaPaths:
                frontLayer = Image.open(os.path.dirname(__file__) + '/../input/assets/' + subdirectory + '7-Head/4-Fro A.png')
                frontLayer = frontLayer.convert('RGBA')
                baseLayer = Image.alpha_composite(baseLayer, frontLayer)

        baseLayer = baseLayer.resize((1600,1600),Image.ANTIALIAS)
        baseLayer.save(os.path.dirname(__file__) + '/../output/nfts/' + self.folder_path + '/' + str(self.number) + '.png', quality = 100)
        
        if need_reorder:
            layer_to_move = self.layers.pop(1)
            dna_to_move = self.dnaPaths.pop(1)
            self.layers.append(layer_to_move)
            self.dnaPaths.append(dna_to_move)

        if need_reorder_eyes:
            layer_to_move = self.layers.pop(7)
            dna_to_move = self.dnaPaths.pop(7)
            self.layers.insert(6, layer_to_move)
            self.dnaPaths.insert(6, dna_to_move)

    def CreateMetadata(self):
        with open(os.path.dirname(__file__) + '/../output/nfts/' + self.folder_path + '/' + str(self.number) + '.json', 'w') as jsonFile:
            # The following two lines make this project compatible with new features in CMv2 (Candy Machine version 2)
            # The JSON metadata new requirement is named image files.  Code will work only with png files.
            # Change Date: 01/19/2022 - ck256-2000
            self.metadata['name'] = f"DROID #{self.number}"
            self.metadata['image'] = str(self.number) + '.png'
            self.metadata['properties']['files'][0] = {"uri" : str(self.number) + ".png", "type":"image/png"}
            json.dump(self.metadata, jsonFile, indent = 4)

    def Check_Reorder(self):
        if '3-Einstein B.png' in self.dnaPaths or '2-Viking Grey B.png' in self.dnaPaths or '3-Viking Brown B.png' in self.dnaPaths or '4-Fro B.png' in self.dnaPaths:
            return True
        else:
            return False

    def Check_Reverse_Reorder(self):
        if '3-Einstein A.png' in self.dnaPaths or '2-Viking Grey A.png' in self.dnaPaths or '3-Viking Brown A.png' in self.dnaPaths or '4-Fro A.png' in self.dnaPaths:
            return True
        else:
            return False

    def Reorder_Eyes_Man(self):
        if '2-Glasses Pixel.png' in self.dnaPaths or '3-Mohawk Blue.png' in self.dnaPaths or '3-Mohawk Red.png' in self.dnaPaths or '4-Viking Horns.png' in self.dnaPaths or '4-Moonbrain.png' in self.dnaPaths:
            return True
        else:
            return False

    def Reorder_Eyes_Female(self):
        if '5-3D.png' in self.dnaPaths or '2-Glasses Pixel.png' in self.dnaPaths or '8-Mohawk Violet.png' in self.dnaPaths or '8-Groovy.png' in self.dnaPaths or '4-Top Hat.png' in self.dnaPaths or '8-Viking Horns.png' in self.dnaPaths or '3-Moonbrain.png' in self.dnaPaths:
            return True
        else:
            return False

    def Check_Black(self):
        self.dnaPaths[2] = re.sub(r"_black", "", self.dnaPaths[2], 1)
