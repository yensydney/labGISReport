import sys
import findReadibleShps
import shapefile
import json
import os

def getRealKey( dictKeys, targetKeys ):
    for k in dictKeys:
        if k in targetKeys:
            return k
    return ""

def parseSFWithKey( sf, phrase, word, loc, fileName ):

    # retrieving records from sf
    records = sf.records()
    recordsDictList = []

    # retreiving shapes from sf shapes
    shapes = sf.shapes()

    # turning each record into a dictionary and adding it to a list
    for i in range(len(records)):
        currentRecord = sf.record(i)
        if currentRecord == None:
            print( "ERROR: Failed to retrieve record from", fileName )
            return -1

        # print(currentRecord)
        dic = currentRecord.as_dict()
        recordsDictList.append(dic)
        
    # sorted list using lambda, will sort in alphabetical order
    # so that the common phrases can be grouped together and parse easier
    sortedRecordDicList = sorted(recordsDictList, key=lambda x: x[phrase])

    # make dict of dict
    annotation_dict = {}
    phraseIndex = -1
    currentPhrase = ''
    shapeIdx = 0
    for i in sortedRecordDicList:

        if i[phrase] == '' or i[word] == '' or i[loc] == None:
            print( "ERROR: Found empty record field in", fileName, ":", i, ", skip the entry" )
            continue
       
        # if there is a new phrase then make a new dictionary for it
        if currentPhrase != i[phrase]:
            phraseIndex += 1
            annotation_dict [phraseIndex] = {}
            currentPhrase = i[phrase]

        # word index is the text location
        wordLoc = i[loc]

        # get shape type from the target shape
        shape = shapes[shapeIdx]
        shapeIdx = shapeIdx +1

        # print( "shapeType:", shape.shapeType, "shapeTypeName:", shape.shapeTypeName )

        # make the dictionary
        annotation_dict[phraseIndex][wordLoc] = {'text_label': i[word], 'shape': shape.shapeType }
       
    # make into json file
    with open( "output/" + fileName + ".json", "w" ) as f:
        json.dump( annotation_dict, f, indent = 4 )

    return 0

def getRecordDictKeys( sf, fileName ):

    # retrieve records from the sf argument
    records = sf.records()
    firstRecord = records[0]
    recordDict = firstRecord.as_dict()
    dictKeys = recordDict.keys()

    # using get real key function to find the real keys by comparing it to the supported phrase keys
    supportedPhraseKeys = [ 'PHRASE', 'phrase', 'Text', 'Phrase' ]
    realPhraseKey = getRealKey( dictKeys, supportedPhraseKeys )

    supportedWordKeys = [ 'TXT', 'txt', 'text', 'Name' ]
    realWordKey = getRealKey( dictKeys, supportedWordKeys )

    supportedLocKeys = [ 'TXT_LOC', 'txt_loc', 'Position' ]
    realLocKey = getRealKey( dictKeys, supportedLocKeys )

    # unsupported keys case
    if realPhraseKey == '' or realLocKey == '' or realWordKey == '': 
        print("ERROR: Found unsupported keys from ", sf.shapeName )
        print("ERROR: Its keys are ", dictKeys )
        return None

    return { 'phrase': realPhraseKey, 'word': realWordKey, 'loc': realLocKey }


def main():
    # needs a shape file directory, cannot be blank
    if len(sys.argv) <=1:
        print("Usage:", sys.argv[0], " <shape file dir>")
        return 0

    targetDir = sys.argv[1]

    # letting you know the shape file you inserted
    print( 'shape file dir:', targetDir )
    print( "output folder: output/" )
    print()

    # make output directory, use default mode, set exist_ok to True (it's ok if the folder already existed)
    os.makedirs( "output", 511, True )

    # calling function to look for available DBFs from the file to make into a list
    targetShps = findReadibleShps.fromDir( targetDir, True )

    FailureCount = 0
    # looping through the list of DBFs
    for shapeFile in targetShps:
 
        #calling function to read the file
        sf = shapefile.Reader( shapeFile )

        # empty sf case
        if sf is None or len( sf.records() ) <= 0:
            print("ERROR: Found invalid record: ", shapeFile )
            FailureCount += 1
            continue

        # getting the basename of the file to name json file
        fileName = os.path.basename(sf.shapeName)

        print()
        print( "parsing", fileName )

        # calling parse function to find real keys
        realKeyDict = getRecordDictKeys( sf, fileName )
        if realKeyDict == None:
            print( "ERROR: Failed to find real keys from", fileName, ". Skipped for now." )
            FailureCount += 1
            continue

        #print( "record dict keys: ", realKeyDict)

        # calling function to create json file
        ret = parseSFWithKey( sf, realKeyDict['phrase'], realKeyDict['word'], realKeyDict['loc'], fileName )
        if ret == 0:
            print( " ... ok" )
        else:
            print( " ... failed" )
            FailureCount += 1
        
    print()
    print( "Total", len( targetShps ), "shape folders parsed. ", FailureCount, "failure." )

    return 0

if __name__ == "__main__":
    sys.exit(main())