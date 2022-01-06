import os
import sys

def fromDir( targetDir, printRealError = False ):

    targetList = []

    dirs = os.listdir(targetDir)
    for d in dirs:
        try:
            shpDir = targetDir + "/" + d
            files = os.listdir(shpDir)
            found = False
            for f in files:
                splitTuple = os.path.splitext(shpDir + "/" + f)
                if splitTuple[1] == ".dbf":
                    targetList.append(splitTuple[0])
                    found = True
            if not found :
                print( "WARN: No .dbf found in ", shpDir)
        except Exception as e:
            print("Find invalid operation in", d)
            if printRealError:
                print("ERROR: ", e)
            continue

    return targetList

def main():
    if len(sys.argv) <=1:
        print(sys.argv[0], " <dir>")
        return 0

    print('Target dir:', sys.argv[1])
    targetDir = sys.argv[1]

    targetShps = fromDir( targetDir )
    for s in targetShps:
        print( s )

    print( "total count:", len( targetShps ) )
    return 0

if __name__ == "__main__":
    sys.exit(main())


