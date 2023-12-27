colorfile = 'defaults/colors.txt'


def getcolor():
    colorlist = []
    with open(colorfile, 'r') as file:
        for line in file:
            if not line.startswith('~'):
                colorlist.append(line.strip())
    return colorlist
