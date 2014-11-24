import glob
import os
import time
from random import randint
from PIL import Image

def printAll( strings ) :
    for name in strings :
        print name;
    print "----";
    return;

def getNewRandomIndex( max, currentIndices ) :
    if max <= len(currentIndices) :
        num = 0;
    else :
        num = randint(0, max);
        
        while currentIndices.count(num) : 
            num = randint(0, max);
    
    return num;

def generateCard( nbSlots, maxIndex ) :

    currentCard = [];
    
    for i in range(0, nbSlots) :
        currentCard.append(getNewRandomIndex(maxIndex, currentCard));
        
    return currentCard;

def generateAllCardIndices( nbSlots, nbImages, nbCards ) :

    allCards = [];
    
    for i in range(0, nbCards) :
        singleCard = generateCard(nbSlots, nbImages - 1);
        
        while allCards.count(singleCard) >= 1 :
            singleCard = generateCard(nbSlots, nbImages - 1);
    
        allCards.append(singleCard);
    
    return allCards;
    
def generateCardImage(indices, imagePaths, nbRows, nbCols, skipMiddle) :
    
    sources = [];
    maxSize = [0, 0];
    
    for index in indices :
        src = Image.open(imagePaths[index]);
        sources.append(src);
        
        if (src.size[0] > maxSize[0]) :
            maxSize[0] = src.size[0];
            
        if (src.size[1] > maxSize[1]) :
            maxSize[1] = src.size[1];

    image = Image.new("RGBA", (maxSize[0] * nbCols, maxSize[1] * nbRows));

    currentIndex = 0;
    
    for col in range(0, nbCols) :
        for row in range(0, nbRows) :
            if ((skipMiddle and col == nbCols / 2 and row == nbRows / 2) == False) :
                position = (maxSize[0] * col + maxSize[0] / 2 - sources[currentIndex].size[0] / 2, maxSize[1] * row + maxSize[1] / 2 - sources[currentIndex].size[1] / 2);
                image.paste(sources[currentIndex], position);
                currentIndex = currentIndex + 1;
    
    return image;
    
    
    
################################
# Script directory
pwd = os.path.dirname(__file__);

# list of image paths
srcImages = pwd + '/images';
outImages = pwd + '/result/' + time.strftime("%Y%m%d-%H%M%S") + '/';
imagePaths = glob.glob(srcImages + '/*');
nbImages = len(imagePaths);

print nbImages, "images found";

# number of images in each card
nbSlots = 24;

# number of cards
nbCards = 100;

# number of rows
nbRows = 5;

# number of columns
nbCols = 5;

# Skip middle
skipMiddle = True;

print "Generating {} cards with {} indices each".format(nbCards, nbSlots);
allCards = generateAllCardIndices(nbSlots, nbImages, nbCards);

if (os.path.exists(outImages) == False) :
    os.makedirs(outImages);

cardNum = 0;

for indices in allCards:
    result = generateCardImage(indices, imagePaths, nbRows, nbCols, skipMiddle);
    result.save(outImages + 'card{}.png'.format(cardNum));
    cardNum = cardNum + 1;

