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
    if max < len(currentIndices) :
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
    
def generateCardImage(indices, imagePaths, nbRows, nbCols, skipMiddle, bgPaths, positions) :
    
    sources = [];
    maxSize = [0, 0];
    
    for index in indices :
        src = Image.open(imagePaths[index]);
        sources.append(src);
        
        if (src.size[0] > maxSize[0]) :
            maxSize[0] = src.size[0];
            
        if (src.size[1] > maxSize[1]) :
            maxSize[1] = src.size[1];

    if len(bgPaths) > 0 :
        image = Image.open(bgPaths[0]);
    else :    
        image = Image.new("RGBA", (maxSize[0] * nbCols, maxSize[1] * nbRows));

    currentIndex = 0;
    
    for col in range(0, nbCols) :
        for row in range(0, nbRows) :
            if ((skipMiddle and col == nbCols / 2 and row == nbRows / 2) == False) :
                if len(positions) == 0 :
                    position = (maxSize[0] * col + maxSize[0] / 2 - sources[currentIndex].size[0] / 2, maxSize[1] * row + maxSize[1] / 2 - sources[currentIndex].size[1] / 2);
                else :
                    position = positions[currentIndex];
                    
                image.paste(sources[currentIndex], position);
                currentIndex = currentIndex + 1;
    
    return image;
    
    
    
################################
# Script directory
pwd = os.path.dirname(__file__);

# list of image paths
srcBackgrounds = pwd + '/images/background';
srcImages = pwd + '/images/squares';
outImages = pwd + '/result/' + time.strftime("%Y%m%d-%H%M%S") + '/';
bgPaths = glob.glob(srcBackgrounds + '/*');
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

# Square positions in background
squarePositions = [
    (160, 790), (426, 790), (692, 790), (958, 790), (1218, 790), 
    (160, 1053), (426, 1053), (692, 1053), (958, 1053), (1218, 1053),
    (160, 1318), (426, 1318),             (958, 1318), (1218, 1318),
    (160, 1581), (426, 1581), (692, 1581), (958, 1581), (1218, 1581),
    (160, 1844), (426, 1844), (692, 1844), (958, 1844), (1218, 1844)
    ];

print "Generating {} cards with {} indices each".format(nbCards, nbSlots);
allCards = generateAllCardIndices(nbSlots, nbImages, nbCards);

if (os.path.exists(outImages) == False) :
    os.makedirs(outImages);

cardNum = 0;

for indices in allCards:
    result = generateCardImage(indices, imagePaths, nbRows, nbCols, skipMiddle, bgPaths, squarePositions);
    result.save(outImages + 'card{}.jpg'.format(cardNum));
    cardNum = cardNum + 1;

