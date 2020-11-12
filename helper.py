def cleanUp(df):
    '''
    Minor cleaning on the dataset, handling edge cases/test card anomalies
    '''
    df['rarity'] = df['rarity'].replace(['Land'],'Common')
    df['cardType'] = df['cardType'].replace(['instant'],'Instant')
    df['cardType'] = df['cardType'].replace(['Eaturecray', 'Scariest Creature You'],'Creature')
    df['subType'] = df['subType'].replace(['Igpay'],'Pig')
    df = df[~df.cardType.str.contains("Token", na=False)] # fix code so this applies

def convertSymbol(imgAlt):
    ''' 
    Coverts a card symbol image to its corresponding text -
    Black = B, Blue = U, Red = R, Green = G, White = W, Variable Colorless = X, Colorless = C, Phyrexian Red = P, Tap = Tap, 
    E = Energy
    '''   
    if (imgAlt == "Variable Colorless"):
        return('X')
    elif (imgAlt == "Blue"):
        return('U')
    elif (imgAlt == "Tap"):
        return('Tap')
    elif (imgAlt.isnumeric()): # number can be multiple digits
        return(imgAlt)
    return(imgAlt[0])

def formatRules(rules):
    for p in rules:
        # Convert rule symbols to text
        for image in p.findAll("img"):
            convertedAlt = convertSymbol(image['alt'])
            image.replaceWith(convertedAlt)
        index = rules.index(p)
        rules[index] = p.text.strip()  
    return("\n".join(rules))

def getSuperType(cardType, superType, supertypes):
    '''
    Splits cardType string into card type and supertype; returns those values
    '''
    if any(supertype in cardType for supertype in supertypes):
        typeSplit = cardType.split()
        superType = (superType + ' ' + typeSplit[0]).strip()
        cardType = ' '.join(typeSplit[1:])
        
    return(cardType, superType)


def splitSetAndRarity(setAndRarity):
    '''
    Splits and returns set and rarity string
    '''
    srSplit = setAndRarity.split("(")
    cardSet = srSplit[0].strip()
    rarity = srSplit[-1].strip(') ')
    return cardSet, rarity