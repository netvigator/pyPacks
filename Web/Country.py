#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# Web functions Country
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# The GNU General Public License is available from:
#   The Free Software Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston MA 02110-1301 USA
#
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2004-2016 Rick Graves
#

def _getCountryCodeTuple( bUpper = False ):
    #
    # http://www.iana.org/domains/root/db/#
    # updated last 2010-02-13
    # some countries include an apostrophe
    # use _getCodesFromTextFile()
    # some may need manual correction, like 'Venezuela, Bolivarian Republic of'
    # http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
    # updated last 2013-12-31
    
    tlCountryCodes = (
        ('ac', 'Ascension Island'),
        ('ad', 'Andorra'),
        ('ae', 'United Arab Emirates'),
        ('af', 'Afghanistan'),
        ('ag', 'Antigua and Barbuda'),
        ('ai', 'Anguilla'),
        ('al', 'Albania'),
        ('am', 'Armenia'),
        ('an', 'Netherlands Antilles'),
        ('ao', 'Angola'),
        ('aq', 'Antarctica'),
        ('ar', 'Argentina'),
        ('as', 'American Samoa'),
        ('at', 'Austria'),
        ('au', 'Australia'),
        ('aw', 'Aruba'),
        ('ax', 'Aland Islands'),
        ('az', 'Azerbaijan'),
        ('ba', 'Bosnia and Herzegovina'),
        ('bb', 'Barbados'),
        ('bd', 'Bangladesh'),
        ('be', 'Belgium'),
        ('bf', 'Burkina Faso'),
        ('bg', 'Bulgaria'),
        ('bh', 'Bahrain'),
        ('bi', 'Burundi'),
        ('bj', 'Benin'),
        ('bl', 'Saint Barthelemy'),
        ('bm', 'Bermuda'),
        ('bn', 'Brunei Darussalam'),
        ('bo', 'Bolivia'),
        ('br', 'Brazil'),
        ('bs', 'Bahamas'),
        ('bt', 'Bhutan'),
        ('bv', 'Bouvet Island'),
        ('bw', 'Botswana'),
        ('by', 'Belarus'),
        ('bz', 'Belize'),
        ('ca', 'Canada'),
        ('cc', 'Cocos (Keeling) Islands'),
        ('cd', 'Congo, The Democratic Republic of the'),
        ('cf', 'Central African Republic'),
        ('cg', 'Congo'),
        ('ch', 'Switzerland'),
        ('ci', "Cote d'Ivoire"),
        ('ck', 'Cook Islands'),
        ('cl', 'Chile'),
        ('cm', 'Cameroon'),
        ('cn', 'China'),
        ('co', 'Colombia'),
        ('cr', 'Costa Rica'),
        ('cu', 'Cuba'),
        ('cv', 'Cape Verde'),
        ('cx', 'Christmas Island'),
        ('cy', 'Cyprus'),
        ('cz', 'Czech Republic'),
        ('de', 'Germany'),
        ('dj', 'Djibouti'),
        ('dk', 'Denmark'),
        ('dm', 'Dominica'),
        ('do', 'Dominican Republic'),
        ('dz', 'Algeria'),
        ('ec', 'Ecuador'),
        ('ee', 'Estonia'),
        ('eg', 'Egypt'),
        ('eh', 'Western Sahara'),
        ('er', 'Eritrea'),
        ('es', 'Spain'),
        ('et', 'Ethiopia'),
        ('eu', 'European Union'),
        ('fi', 'Finland'),
        ('fj', 'Fiji'),
        ('fk', 'Falkland Islands (Malvinas)'),
        ('fm', 'Micronesia, Federated States of'),
        ('fo', 'Faroe Islands'),
        ('fr', 'France'),
        ('ga', 'Gabon'),
        ('gb', 'United Kingdom'),
        ('gd', 'Grenada'),
        ('ge', 'Georgia'),
        ('gf', 'French Guiana'),
        ('gg', 'Guernsey'),
        ('gh', 'Ghana'),
        ('gi', 'Gibraltar'),
        ('gl', 'Greenland'),
        ('gm', 'Gambia'),
        ('gn', 'Guinea'),
        ('gp', 'Guadeloupe'),
        ('gq', 'Equatorial Guinea'),
        ('gr', 'Greece'),
        ('gs', 'South Georgia and the South Sandwich Islands'),
        ('gt', 'Guatemala'),
        ('gu', 'Guam'),
        ('gw', 'Guinea-Bissau'),
        ('gy', 'Guyana'),
        ('hk', 'Hong Kong'),
        ('hm', 'Heard Island and McDonald Islands'),
        ('hn', 'Honduras'),
        ('hr', 'Croatia'),
        ('ht', 'Haiti'),
        ('hu', 'Hungary'),
        ('id', 'Indonesia'),
        ('ie', 'Ireland'),
        ('il', 'Israel'),
        ('im', 'Isle of Man'),
        ('in', 'India'),
        ('io', 'British Indian Ocean Territory'),
        ('iq', 'Iraq'),
        ('ir', 'Iran, Islamic Republic of'),
        ('is', 'Iceland'),
        ('it', 'Italy'),
        ('je', 'Jersey'),
        ('jm', 'Jamaica'),
        ('jo', 'Jordan'),
        ('jp', 'Japan'),
        ('ke', 'Kenya'),
        ('kg', 'Kyrgyzstan'),
        ('kh', 'Cambodia'),
        ('ki', 'Kiribati'),
        ('km', 'Comoros'),
        ('kn', 'Saint Kitts and Nevis'),
        ('kp', "Korea, Democratic People's Republic of"),
        ('kr', 'Korea, Republic of'),
        ('kw', 'Kuwait'),
        ('ky', 'Cayman Islands'),
        ('kz', 'Kazakhstan'),
        ('la', "Lao People's Democratic Republic"),
        ('lb', 'Lebanon'),
        ('lc', 'Saint Lucia'),
        ('li', 'Liechtenstein'),
        ('lk', 'Sri Lanka'),
        ('lr', 'Liberia'),
        ('ls', 'Lesotho'),
        ('lt', 'Lithuania'),
        ('lu', 'Luxembourg'),
        ('lv', 'Latvia'),
        ('ly', 'Libyan Arab Jamahiriya'),
        ('ma', 'Morocco'),
        ('mc', 'Monaco'),
        ('md', 'Moldova, Republic of'),
        ('me', 'Montenegro'),
        ('mf', 'Saint Martin'),
        ('mg', 'Madagascar'),
        ('mh', 'Marshall Islands'),
        ('mk', 'Macedonia, The Former Yugoslav Republic of'),
        ('ml', 'Mali'),
        ('mm', 'Myanmar'),
        ('mn', 'Mongolia'),
        ('mo', 'Macao'),
        ('mp', 'Northern Mariana Islands'),
        ('mq', 'Martinique'),
        ('mr', 'Mauritania'),
        ('ms', 'Montserrat'),
        ('mt', 'Malta'),
        ('mu', 'Mauritius'),
        ('mv', 'Maldives'),
        ('mw', 'Malawi'),
        ('mx', 'Mexico'),
        ('my', 'Malaysia'),
        ('mz', 'Mozambique'),
        ('na', 'Namibia'),
        ('nc', 'New Caledonia'),
        ('ne', 'Niger'),
        ('nf', 'Norfolk Island'),
        ('ng', 'Nigeria'),
        ('ni', 'Nicaragua'),
        ('nl', 'Netherlands'),
        ('no', 'Norway'),
        ('np', 'Nepal'),
        ('nr', 'Nauru'),
        ('nu', 'Niue'),
        ('nz', 'New Zealand'),
        ('om', 'Oman'),
        ('pa', 'Panama'),
        ('pe', 'Peru'),
        ('pf', 'French Polynesia'),
        ('pg', 'Papua New Guinea'),
        ('ph', 'Philippines'),
        ('pk', 'Pakistan'),
        ('pl', 'Poland'),
        ('pm', 'Saint Pierre and Miquelon'),
        ('pn', 'Pitcairn'),
        ('pr', 'Puerto Rico'),
        ('ps', 'State of Palestine'),
        ('pt', 'Portugal'),
        ('pw', 'Palau'),
        ('py', 'Paraguay'),
        ('qa', 'Qatar'),
        ('re', 'Reunion'),
        ('ro', 'Romania'),
        ('rs', 'Serbia'),
        ('ru', 'Russian Federation'),
        ('rw', 'Rwanda'),
        ('sa', 'Saudi Arabia'),
        ('sb', 'Solomon Islands'),
        ('sc', 'Seychelles'),
        ('sd', 'Sudan'),
        ('se', 'Sweden'),
        ('sg', 'Singapore'),
        ('sh', 'Saint Helena'),
        ('si', 'Slovenia'),
        ('sj', 'Svalbard and Jan Mayen'),
        ('sk', 'Slovakia'),
        ('sl', 'Sierra Leone'),
        ('sm', 'San Marino'),
        ('sn', 'Senegal'),
        ('so', 'Somalia'),
        ('sr', 'Suriname'),
        ('st', 'Sao Tome and Principe'),
        ('su', 'Soviet Union (being phased out)'),
        ('sv', 'El Salvador'),
        ('sy', 'Syrian Arab Republic'),
        ('sz', 'Swaziland'),
        ('tc', 'Turks and Caicos Islands'),
        ('td', 'Chad'),
        ('tf', 'French Southern Territories'),
        ('tg', 'Togo'),
        ('th', 'Thailand'),
        ('tj', 'Tajikistan'),
        ('tk', 'Tokelau'),
        ('tl', 'Timor-Leste'),
        ('tm', 'Turkmenistan'),
        ('tn', 'Tunisia'),
        ('to', 'Tonga'),
        ('tp', 'Portuguese Timor (being phased out)'),
        ('tr', 'Turkey'),
        ('tt', 'Trinidad and Tobago'),
        ('tv', 'Tuvalu'),
        ('tw', 'Taiwan'),
        ('tz', 'Tanzania, United Republic of'),
        ('ua', 'Ukraine'),
        ('ug', 'Uganda'),
        ('uk', 'United Kingdom'),
        ('um', 'United States Minor Outlying Islands'),
        ('us', 'United States'),
        ('uy', 'Uruguay'),
        ('uz', 'Uzbekistan'),
        ('va', 'Holy See (Vatican City State)'),
        ('vc', 'Saint Vincent and the Grenadines'),
        ('ve', 'Venezuela, Bolivarian Republic of'),
        ('vg', 'Virgin Islands, British'),
        ('vi', 'Virgin Islands, U.S.'),
        ('vn', 'Viet Nam'),
        ('vu', 'Vanuatu'),
        ('wf', 'Wallis and Futuna'),
        ('ws', 'Samoa'),
        ('ye', 'Yemen'),
        ('yt', 'Mayotte'),
        ('yu', 'Yugoslavia (being phased out)'),
        ('za', 'South Africa'),
        ('zm', 'Zambia'),
        ('zw', 'Zimbabwe'),
    )
    #
    if bUpper:
        #
        from Iter.Get import getItemIterWithKeysConsistentCase
        #
        tlCountryCodes = tuple(
            getItemIterWithKeysConsistentCase( tlCountryCodes, bUpper = True ) )
        #
    #
    return tlCountryCodes




def getCountryCodeDict( bUpper = False ):
    #
    tlCountryCodes = _getCountryCodeTuple( bUpper )
    #
    return dict( tlCountryCodes )





dCountryCodes = getCountryCodeDict()


def getCountryDict( dCountryCodes = dCountryCodes ):
    #
    '''
    returns a dict with country names as keys.
    you may need to massage the country names,
    depending on your needs.
    you can import dCountryCodes from here, massage,
    then pass the massaged dict to this function.
    '''
    from Dict.Get import getReverseDictGotUniqueItems
    #
    return( getReverseDictGotUniqueItems( dCountryCodes ) )




def _getCodesFromTextFile( *sFileSpec, **kwargs ):
    #
    from os.path        import join
    #
    from Dir.Get        import sDurableTempDir
    from File.Get       import getFileObject
    from File.Spec      import getFullSpecDefaultOrPassed
    from File.Write     import MakeTemp
    from Iter.AllVers   import iMap, iZip, tFilter
    from String.Get     import getTextAfter, getTextWithin
    #
    if 'sDefault' not in kwargs:
        kwargs['sDefault'] = join( sDurableTempDir, 'country_codes.txt' )
    #
    sFileSpec           = getFullSpecDefaultOrPassed( *sFileSpec, **kwargs )
    #
    oFile               = getFileObject( sFileSpec )
    #
    lCodes              = []
    #
    def getThisLine( sLine ):
        return ' country-code ' in sLine
    #
    tLines              = tFilter( getThisLine, oFile )
    #
    lCodes              = [ getTextWithin( sLine, '.', ' ' ).lower()
                            for sLine in tLines ]
    #
    lCountries          = [ getTextAfter( sLine, 'country-code  ' ).strip()
                            for sLine in tLines ]
    #
    tCodesCountries     = tuple( iMap( tuple, iZip( lCodes, lCountries ) ) )
    #
    MakeTemp( repr( tCodesCountries ).replace( '), (', '),\n(' ) )
    #
    return tCodesCountries



def getCountryOffHost( sHost ): # just gets the country part of a host name
    #
    # not used anywhere
    #
    from Test import isDotQuad
    #
    sCountry                    = ''
    #
    if not isDotQuad( sHost ):
        #
        if sHost is None:       sHost = ''
        #
        lParts                  = sHost.split( '.' )
        #
        sLastPart               = lParts[ -1 ].lower()
        #
        if len( sLastPart ) == 2 and sLastPart in dCountryCodes:
            #
            sCountry            = sLastPart
        #
    #
    return sCountry



setTheCountries = frozenset(
    (   'Bahamas',
        'Islands',
        'Kingdom',
        'Maldives',
        'Netherlands',
        'Philippines',
        'Republic',
        'Federation',
        'States' ) )



def getSayMaybeTheCountry( sCountry ):
    #
    lParts = sCountry.split()
    #
    if ( lParts and
          ( lParts[-1].title() in setTheCountries or
            lParts[0].title() == 'United' ) ):
        #
        sCountry = 'the %s' % sCountry
        #
    #
    return sCountry



if __name__ == "__main__":
    #
    from six            import print_ as print3
    #
    from Collect.Test   import AllMeet
    from Collect.Get    import getKeyIterOffItems
    from Dict.Test      import getHasKeyTester
    from Numb.Test      import areClose
    from Utils.Result   import sayTestResult
    #
    lProblems           = []
    #
    tCountries          = _getCountryCodeTuple(      )
    tUpperCountry       = _getCountryCodeTuple( True )
    #
    if          type( tCountries ) != tuple   or \
                len(  tCountries ) < 200      or \
                tCountries   [0][0].isupper() or \
                tUpperCountry[0][0].islower() or \
            not tCountries   [0][0].islower() or \
            not tUpperCountry[0][0].isupper():
        #
        lProblems.append( '_getCountryCodeTuple()' )
        #
    #
    dUpperCountry       = getCountryCodeDict( 1 )
    #
    hasKeyCountries     = getHasKeyTester( dCountryCodes )
    hasKeyUpperCountry  = getHasKeyTester( dUpperCountry )
    #
    iCodesLower         = getKeyIterOffItems( tCountries    )
    iCodesUpper         = getKeyIterOffItems( tUpperCountry )
    #
    if          type( dCountryCodes ) != dict               or \
                len(  dCountryCodes ) != len( tCountries )  or \
            not AllMeet( iCodesLower, hasKeyCountries    )      or \
            not AllMeet( iCodesUpper, hasKeyUpperCountry ):
        #
        lProblems.append( 'getCountryCodeDict()' )
        #
    if      getCountryOffHost( 'google.co.th' ) != 'th' or \
            getCountryOffHost( 'google.com'   ) != '':
        #
        lProblems.append( 'getCountryOffHost()' )
        #
    #
    dCountries = getCountryDict()
    #
    if dCountries.get( 'Trinidad and Tobago' ) != 'tt':
        #
        lProblems.append( 'getCountryDict() Trinidad and Tobago not there' )
        #
    #
    if not areClose( len( dCountryCodes ), len( dCountries ) ):
        #
        print3( 'len( dCountries ):', len( dCountries ) )
        print3( 'len( dCountryCodes ):', len( dCountryCodes ) )
        lProblems.append( 'getCountryDict() too short' )
        #
    #
    if getSayMaybeTheCountry( 'Belgium' )     != 'Belgium':
        #
        lProblems.append( 'getSayMaybeTheCountry() Belgium' )
        #
    #
    if getSayMaybeTheCountry( 'Netherlands' ) != 'the Netherlands':
        #
        lProblems.append( 'getSayMaybeTheCountry() the Netherlands' )
        #
    #
    if getSayMaybeTheCountry( 'Russian Federation' ) != 'the Russian Federation':
        #
        lProblems.append( 'getSayMaybeTheCountry() the Russian Federation' )
        #
    #
    sayTestResult( lProblems )