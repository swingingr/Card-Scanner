import numpy as np
from imagehash import hex_to_hash
#from PIL import Image, ImageOps
#from PIL import Image 
#import os 
import csv
#import requests

def compareCards(hashes):
    cutoff = 18  # Arbitrarily set cutoff value; was found through testing


    # Create arrays of size=4 that store hash differences for each orientation; every hashing method gets its own array
    # Change the parenthases back to four later
    #avghashesDists = np.zeros(4)
    #whashesDists = np.zeros(4)
    phashesDists = np.zeros(1)
    dhashesDists = np.zeros(1)

    maxHashDists = []  # An array that will store the maximum of the minimum hash difference for each card

    SetData = open('SetData.csv', 'r')
    csvreader = csv.reader(SetData)
    start_time = time.time()
    for row in csvreader:
        cardName = row[0]
        cardSet = row[1]
        #avghash1 = row[2]
        #avghash2 = row[3]
        #avghash3 = row[4]
        #avghash4 = row[5]

        #whash1 = row[6]
        #whash2 = row[7]
        #whash3 = row[8]
        #whash4 = row[9]
        
        phash1 = row[10]
        #phash2 = row[11]
        #phash3 = row[12]
        #phash4 = row[13]

        dhash1 = row[14]
        #dhash2 = row[15]
        #dhash3 = row[16]
        #dhash4 = row[17]
            # Convert each hash from a String to a hash and find the distance from the scanned image
        #avghashesDists[0] = hashes[0] - hex_to_hash(avghash1)
        #avghashesDists[1] = hashes[0] - hex_to_hash(avghash2)
        #avghashesDists[2] = hashes[0] - hex_to_hash(avghash3)
        #avghashesDists[3] = hashes[0] - hex_to_hash(avghash4)

        #whashesDists[0] = hashes[1] - hex_to_hash(whash1)
        #whashesDists[1] = hashes[1] - hex_to_hash(whash2)
        #whashesDists[2] = hashes[1] - hex_to_hash(whash3)
        #whashesDists[3] = hashes[1] - hex_to_hash(whash4)

        phashesDists[0] = hashes[2] - hex_to_hash(phash1)
        #phashesDists[1] = hashes[2] - hex_to_hash(phash2)
        #phashesDists[2] = hashes[2] - hex_to_hash(phash3)
        #phashesDists[3] = hashes[2] - hex_to_hash(phash4)

        dhashesDists[0] = hashes[3] - hex_to_hash(dhash1)
        #dhashesDists[1] = hashes[3] - hex_to_hash(dhash2)
        #dhashesDists[2] = hashes[3] - hex_to_hash(dhash3)
        #dhashesDists[3] = hashes[3] - hex_to_hash(dhash4)

        # Find the minimum of each hashing method
        # This should make us look at the correct card orientation
        #hashDistances = [min(avghashesDists), min(whashesDists), min(phashesDists), min(dhashesDists)]
        hashDistances = [min(phashesDists), min(dhashesDists)]
        maxHashDists.append(max(hashDistances))  # Find the max of the mins of each hashing method to reduce error
    end_time=time.time()
    print(end_time-start_time)
    if min(maxHashDists) < cutoff:  # If the smallest hash distance is less than the cutoff, we have found our card
        minCardNum = maxHashDists.index(min(maxHashDists)) + 1  # Find the card number of the card
        # Return dictionary with traits about cards
        SetData = open('SetData.csv', 'r')
        csvreader = csv.reader(SetData)
        rows = list(csvreader)
        cardname = rows[minCardNum-1][0]
        cardset = rows[minCardNum-1][1]
        return {'Card Number': rows[minCardNum-1][18],
                'Card Name': cardname,
                'Card Set': cardset
                }
    return None

def compareCards2(hashes):
    cutoff = 25  # Arbitrarily set cutoff value; was found through testing
    # Create arrays of size=4 that store hash differences for each orientation; every hashing method gets its own array
    # Change the parenthases back to four later
    #avghashesDists = np.zeros(4)
    #whashesDists = np.zeros(4)
    combined1 = hashes[2].hash.flatten().tolist() + hashes[3].hash.flatten().tolist()
    combined2 = ""
    for i in range(len(combined1)):
        if combined1[i] == True:
              combined2 = combined2 + "1"
        if combined1[i] == False:
             combined2 = combined2 + "0"
    maxHashDists = []  # An array that will store the maximum of the minimum hash difference for each card
    SetData = open('SetData copy.csv', 'r')
    csvreader = csv.reader(SetData)
    for row in csvreader:
        combined = list(row[20])
        dist = sum(el1 != el2 for el1, el2 in zip(combined, combined2))
        maxHashDists.append(dist)
    if min(maxHashDists) < cutoff:  # If the smallest hash distance is less than the cutoff, we have found our card
        minCardNum = maxHashDists.index(min(maxHashDists)) + 1  # Find the card number of the card
        # Return dictionary with traits about cards
        SetData = open('SetData copy.csv', 'r')
        csvreader = csv.reader(SetData)
        rows = list(csvreader)
        cardname = rows[minCardNum-1][0]
        cardset = rows[minCardNum-1][1]
        return {'Card Number': rows[minCardNum-1][18],
                'Card Name': cardname,
                'Card Set': cardset
                }
    return None



def getHashes(type, url): #USED ONLY FOR POPULATING DATABASE. NEEDS COMMENTED MODULES AT TOP
        # Create an array with self.setSize rows and 4 columns. Each column represents a different hashing method
        arr = np.empty((1,4), dtype=object)
        filename = 'img.jpg'
        img = Image.open(filename)
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

'''
def CheckInventory():
    InvData = open('TcgCollector.csv', 'r')
    csvreader = csv.reader(InvData)  
    for row in csvreader:
         jhgkj'
'''