#!/home/rick/bin/pythonTest
# -*- coding: utf-8 -*-

from os     import urandom
from pprint import pprint
from re     import compile as REcompile

from six    import PY2 as PYTHON2

tHexCiphers = ( '315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e',
'234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f',
'32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb',
'32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa',
'3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070',
'32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4',
'32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce',
'315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3',
'271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027',
'466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83',
'32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904')



sExampleKey = '\xd8\xf4a\x16 \xeb0\xa9\xfc\x11\x00/\x83\xf1q{\x82\xea=\\\xe3\xa98\xd4\xea\xca\x0b4\xf4\xde+\x06\x87=\xec\x012\xea\x9a\xde\xe7\xfd`\xf75\x8b\xb7\xb7\xd6\xa4\xbc\xe6o\xa7\xce\xf36\xbf\xa6$A\x1f7\x93\x86l\xef\xd6{Kc%\x87G.T\x83v\x97\\\tF\x14j\xee\xed\\\xf3\x03\x08\xa3\xae\xa88\xb5\x08VV\x86\x1bn\xf5\xce\xda\x9b|\xfc1\xe7Ct\xf6\xbd\xe0h\xe43\x00q\xa3rN\xe1\xe6\x98C\xa9J\xe6\x9f\xe0\x18\xaa\xb1X\xfbGA\x87\x151\xd0u\x94C\xe3{zc\xc6a\x92:\x7f\xa3t\'T\xf0\x0cX\xb9`\x0ec\n#\x0f\x90\xe8\xac\xea\xb3q\xc3\xcb\xadx\xb6\x0c\x94C\x95\x94\xa3\xb2~^\xe5Q\xae)8\x1d\x07e\x8a6m\xc2_\xf8\x9e\x90=U+\x06\x05\xef\x9b\xfa\n\x15\x9d8\xc3\xa1\x1b\x11\\\x17\xb3\xfc\xe4\xfaU`\xaf\x02\x96 L\xd5.\x0e\xb8\xbdN\xad\x89\xf8\xcf\xd9\xb8_\xf8\x0e\x91\xcd\xc2O\xce\x8b\x9c"\x8b.\xe6Qu-4(\x02\x11\xa1\xa5\xc6Y\xf5\x8f\x0ew:\x85%\x9e\x97&\x11\x86\x9b\xac\x0e\xd1*-i\xa8\x08>\xda\x04>\xc1\x0b\x8b\xb7r\xadx\xfd\xba\xcc\xc7\xa8\x94Y\xda .\xa7R\xb7+\xca\xef\xca>\xc7\x10($6}\xdb\xb5o\nB\xcf\xdc\x056\xee\x10\xe6\x1d\x0e\x82\x8f\xb2Q\xe8\xd6c\xb7\x15\xbb\x01\xa7\xa7\xdf\xa7\xd9A\xeb\xa3\xe4\x8b\xc1\x83>\x05a\x8d3\x1cS\xff?\xf5\x9bS\x1a\xa4\xecD\xbd\n\xdb\'\x96R<\xb6\xd2\x1c\xdf\xe4G\x1f5\xef\xbei}t\x89\x15\'5\xacF\x14\xe4\xb0\xa5\xb1\xa0*\xdc\xe2\x9e\xd9\x8b\xd5\xc1\xc4\xc3Sa\xfd\x9c`\xe2\xf0\xc0X\xb0\xd08p\x87\x19\xedvG\xe1s\x07\x0b\xf4\x0b\xe5\xe3m\x97\xe1\xd9\xfa\x9d]\x18\x92\x15i\xeb\xcaBwU\xa7\xd2EEG\x9e\x1es\xb1\x03\x16sb\x14\xee\xfa\xe8\x10KE\xcb\xf1X]f|\xa4"\x14@\x1e2\x99\xa6\xf1\xb9\xb3A\xc2\x19\x97/\xe2\xd6\x05\xb4f6\xd4'






def random(size=16):
    return urandom(size)


def _getByteGotInt( u ):
    #
    if PYTHON2:
        return u
    else: # PYTHON3
        return chr( u )


def _strxor( a, b ):
    #
    s = "".join( [ chr( ord( _getByteGotInt(x) ) ^ ord(y) )
                   for (x, y) in zip(a, b) ] )
    #
    return s


def crypt( key, s ):
    #
    c = _strxor( key, s )
    #
    # print( c.encode('hex') )
    #
    return c


def _gotHexStringWantBytes( s ):
    #
    if PYTHON2:
        return s.decode("hex")
    else: # PYTHON3
        return bytes.fromhex( s )



tBytesCiphers = tuple( [ _gotHexStringWantBytes( s ) for s in tHexCiphers ] )



iMaxLen = max( map( len, tBytesCiphers ) )



def _getHexTuple( sHexes ):
    #
    lHexes = []
    #
    lAdd = []
    #
    for s in sHexes:
        #
        lAdd.append( s )
        #
        if len( lAdd ) == 1: continue
        #
        lHexes.append( ''.join( lAdd ) )
        #
        lAdd = []
        #
    #
    return tuple( lHexes )


def _getHexOut( s ):
    #
    if PYTHON2:
        return s.encode('hex')
    else: # PYTHON3
        return s.encode("utf-8").hex()

if __name__ == "__main__":
    #
    from Utils.Config import getConfDict
    #
    # key = random(256)
    bFinalOutput = True # False
    #
    oSpaceFinder = REcompile( ' {8,1024}' ) # 8 or more spaces next to each other
    #
    lKey = [ '00' ] * iMaxLen
    #
    dConfig = getConfDict( sConfigFile = 'crypto_secrets.ini' )
    #
    lKey[  0:155] = _getHexTuple( dConfig['main']['key'] )
    #
    #lKey[278:283] = _getHexTuple( 
    #
    if iMaxLen != len( lKey ):
        #
        print( '### iMaxLen:', iMaxLen, 'len( lKey ):', len( lKey ), ' ###' )
        #
    #
    sCrib = ' your government'
    #
    iBaseMessage = 5
    #
    if 0 <= iBaseMessage < len( tBytesCiphers ) :
        #
        cipher = tBytesCiphers[ iBaseMessage ]
        #
        for i in range( len( cipher ) - len(sCrib) ):
            #
            key_part_maybe = crypt( cipher[ i : i + len(sCrib) ], sCrib )
            #
            iCipherCount = -1
            #
            lOutputs = []
            lAllOuts = []
            #
            for bCipher in tBytesCiphers:
                #
                iCipherCount += 1
                #
                # if iCipherCount == iBaseMessage: continue
                #
                sTest = crypt( bCipher[ i : i + len(sCrib) ], key_part_maybe )
                #
                tNumbs = tuple( map( ord, sTest ) )
                #
                if sTest:
                    lAllOuts.append( ( iCipherCount, sTest ) )
                #
                if    ( sTest and tNumbs and
                        max( tNumbs ) <= 126 and min( tNumbs ) >= 32 and
                        sTest.replace( ' ', '' ).isalpha() ):
                    lOutputs.append( sTest )
                #
            #
            if len( lOutputs ) > 1:
                #
                print( '%s : %s' % ( i, _getHexOut( key_part_maybe ) ) )
                pprint( lAllOuts )
                #
        
    else:
        #
        print( 'hello' )
        #
    #
    lDecrypted = []
    #
    i = 0
    #
    for bCipher in tBytesCiphers:
        #
        lAppend = []
        #
        #print( 'zip( lKey, bCipher ):' )
        #pprint( tuple( zip( lKey, bCipher ) ) )
        #
        for t in zip( lKey, bCipher ):
            #
            if t[0] == '00':
                #
                lAppend.append( ' ' )
                #
            else:
                #
                sKeyChar = _gotHexStringWantBytes( t[0] )
                #
                s = crypt( sKeyChar, _getByteGotInt( t[1] ) )
                #
                if not bFinalOutput and s == ' ':
                    #
                    lAppend.append( '_' ) # show an underscore for a known space
                    #
                else:
                    #
                    lAppend.append( s )
                    #
                #
            #
        #
        sThisMsg = oSpaceFinder.sub( ' ... ', ''.join( lAppend ) )
        #
        lDecrypted.append( sThisMsg )
        #
        print( i )
        print( sThisMsg )
        #
        i += 1
        #

        
