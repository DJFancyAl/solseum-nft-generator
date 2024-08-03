from optparse import OptionParser
import sys

def Args(numberNFTs, testRarities, randomizeOutput):
    parser = OptionParser()
    
    parser.add_option('-p', '--public-nfts', dest = 'public_nfts', help = 'Number of candy machine NFTs for public mint. [default=0]', metavar = 'INT', type = 'int')
    parser.add_option('-w', '--whitelist-nfts', dest = 'whitelist_nfts', help = 'Number of candy machine NFTs for whitelisted mint. [default=0]', metavar = 'INT', type = 'int')
    parser.add_option('-g', '--giveaway-nfts', dest = 'giveaway_nfts', help = 'Number of candy machine NFTs for giveways. [default=0]', metavar = 'INT', type = 'int')
    parser.add_option('-t', '--test-rarities', dest = 'test_rarities', help = 'Calculate the rarities without creating NFTs. [default=0]', metavar = 'BOOL (0 or 1)', type = 'int')
    parser.add_option('-r', '--randomize-output', dest = 'randomize_output', help = 'Randomize the output of the nfts (f.e. the 0.json can be the NFT #123) [default = 0]', metavar = 'BOOL (0 or 1)', type = 'int')
    parser.add_option('-m', '--man', action="store_true", help = 'Creates type "Man" NFTs.')
    parser.add_option('-f', '--female', action="store_true", help = 'Creates type "Female" NFTs.')
    parser.add_option('-s', '--saturn', action="store_true", help = 'Creates type "Saturn" NFTs.')
    parser.add_option('-e', '--extras', action="store_true", help = 'Creates type "Extras" NFTs.')
    parser.add_option('-b', '--brain', action="store_true", help = 'Creates type "Moonbrain" NFTs.')
    
    opts, args = parser.parse_args()

    nftType = []
    if not opts.man and not opts.female and not opts.saturn and not opts.brain and not opts.extras:
        print('*************\n')
        print('Please select "man, female, saturn, or extra" NFTs (-m, -f, -s, or -e).\n')
        print('*************')
        sys.exit(1)
    elif opts.saturn and not opts.man and not opts.female:
        print('*************\n')
        print('Please select "man or female" when creating Saturn NFTs(-m, -f).\n')
        print('*************')
        sys.exit(1)
    elif opts.man and opts.female:
        print('*************\n')
        print('Please select either "man or female" when creating NFTs(-m or -f).\n')
        print('*************')
        sys.exit(1)
    elif opts.extras and (not opts.female or not opts.man):
        print('*************\n')
        print('Please select either "man or female" when creating extra NFTs(-m or -f).\n')
        print('*************')
        sys.exit(1)

    if opts.man:
        nftType.append('man')
    if opts.female:
        nftType.append('female')
    if opts.saturn:
        nftType.append('saturn')
    if opts.brain:
        nftType = ['man', 'brain']
    if opts.extras:
        nftType.append('extras')


    if opts.public_nfts:
        numberNFTs[0] = max(0,int(opts.public_nfts))
    if opts.whitelist_nfts:
        numberNFTs[1] = max(0,int(opts.whitelist_nfts))
    if opts.giveaway_nfts:
        numberNFTs[2] = max(0,int(opts.giveaway_nfts))
    if opts.test_rarities:
        testRarities = bool(opts.test_rarities)
    if opts.randomize_output:
        randomizeOutput = bool(opts.randomize_output)

    if testRarities:
        print('TESTING RARITIES ACTIVE... RARITIES WILL BE CALCULATED USING A SAMPLE OF NFTs.')
        print('THIS VERSION WONT CREATE ANY METADATA PAIR.')
        print('USE IT AS A DEBUG ONLY OPTION TO SEE HOW UR TICKET_VALUES FROM UR INPUR ASSETS WORKS.')
        print('TO CALCULATE A REAL DISTRIBUTION OF UR ITEMS RARITY DONT USE THIS OPTION.')
        print()
    
    if randomizeOutput:
        print('RANDOMIZE OUTPUT ACTIVE... NFTs LOCATION WILL BE SHUFFLED BEFORE THE METADATA+PNG IS GENERATED.')
        print('THE MEANING OF THIS IS: YOUR 0.json THAT SHOULD BE NFT #0, CAN BE THE NFT #1234 AND SO ON.')
        print()

    return numberNFTs, testRarities, randomizeOutput, nftType
