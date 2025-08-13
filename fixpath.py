#utility for adding cards and their hashes to the database

from pokemontcgsdk import Card
from pokemontcgsdk import Set
import numpy as np
import imagehash
from PIL import Image, ImageOps
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
from PIL import Image 
import os 
import csv
import requests
from time import perf_counter

RestClient.configure('7db61996-e6d4-455b-89aa-f1bf2f71b4fa')

def remove_special_characters(text):
    return "".join(char for char in text if char.isalnum() or char.isspace())

def getHashes(type, url):
        # Create an array with self.setSize rows and 4 columns. Each column represents a different hashing method
        arr = np.empty((1,4), dtype=object)
        #img = Image.open(BytesIO(response.content))
        match type:
        # For each case, find the average hash, whash, phash, & dhash of the image & convert it to a string
                case 'hash':  # Normally oriented card
                    arr[0][0] = str(imagehash.average_hash(img))
                    arr[0][1] = str(imagehash.whash(img))
                    arr[0][2] = str(imagehash.phash(img))
                    arr[0][3] = str(imagehash.dhash(img))
                case 'hashmir':  # Mirrored card
                    imgmir = ImageOps.mirror(img)
                    arr[0][0] = str(imagehash.average_hash(imgmir))
                    arr[0][1] = str(imagehash.whash(imgmir))
                    arr[0][2] = str(imagehash.phash(imgmir))
                    arr[0][3] = str(imagehash.dhash(imgmir))
                case 'hashud':  # Upside down card
                    imgflip = ImageOps.flip(img)
                    arr[0][0] = str(imagehash.average_hash(imgflip))
                    arr[0][1] = str(imagehash.whash(imgflip))
                    arr[0][2] = str(imagehash.phash(imgflip))
                    arr[0][3] = str(imagehash.dhash(imgflip))
                case 'hashudmir':  # Upside down & mirrored card
                    imgmirflip = ImageOps.flip(ImageOps.mirror(img))
                    arr[0][0] = str(imagehash.average_hash(imgmirflip))
                    arr[0][1] = str(imagehash.whash(imgmirflip))
                    arr[0][2] = str(imagehash.phash(imgmirflip))
                    arr[0][3] = str(imagehash.dhash(imgmirflip))
        return arr  # Return self.setSize x 4 array of image hashes for selected orientation
RestClient.configure('7db61996-e6d4-455b-89aa-f1bf2f71b4fa')


allSets = Set.all()
with open('SetData.csv','a',newline='',encoding="utf-8") as file:
    writer = csv.writer(file)
    for i in range(98,len(allSets)):
        set = allSets[i]
        setID = str(set.id)
        print(f"Starting {set.name}..  ")
        query = "set.id:"+setID
        cards2 = Card.where(q=query)
        start_time = perf_counter()
        for card in cards2:
            url = card.images.large
            data = requests.get(url).content
            f = open('img.jpg','wb')
            f.write(data)
         # Loop through each card image
            filename = 'img.jpg'
            img = Image.open(filename)
            hashes = getHashes('hash', url)
            mirhashes = getHashes('hashmir', url)
            udhashes = getHashes('hashud', url)
            udmirhashes = getHashes('hashudmir', url)
            uglyname = card.name
            cleanname = remove_special_characters(uglyname)
            data = [[uglyname,card.set.name,
                 hashes[0][0],mirhashes[0][0],udhashes[0][0],udmirhashes[0][0],     #avg
                 hashes[0][1],mirhashes[0][1],udhashes[0][1],udmirhashes[0][1],     #w
                 hashes[0][2],mirhashes[0][2],udhashes[0][2],udmirhashes[0][2],     #p
                 hashes[0][3],mirhashes[0][3],udhashes[0][3],udmirhashes[0][3],
                 card.number,card.set.id]]    #d
            writer.writerows(data)
        end_time = perf_counter()
        total_time = end_time-start_time
        print(f"Done ({total_time})")


'''
cards = Card.where(q='name:Exeggutor set.name:evolutions')
with open('SetData.csv','a',newline='',encoding="utf-8") as file:
    writer = csv.writer(file)
    for i in cards:
        url = i.images.large
        data = requests.get(url).content
        f = open('img.jpg','wb')
        f.write(data)
        # Loop through each card image
        filename = 'img.jpg'
        img = Image.open(filename)
        hashes = getHashes('hash', url)
        mirhashes = getHashes('hashmir', url)
        udhashes = getHashes('hashud', url)
        udmirhashes = getHashes('hashudmir', url)
        uglyname = i.name
        cleanname = remove_special_characters(uglyname)
        data = [[uglyname,i.set.name,
                 hashes[0][0],mirhashes[0][0],udhashes[0][0],udmirhashes[0][0],     #avg
                 hashes[0][1],mirhashes[0][1],udhashes[0][1],udmirhashes[0][1],     #w
                 hashes[0][2],mirhashes[0][2],udhashes[0][2],udmirhashes[0][2],     #p
                 hashes[0][3],mirhashes[0][3],udhashes[0][3],udmirhashes[0][3]]]    #d
        print(data)
        writer.writerows(data)
'''
