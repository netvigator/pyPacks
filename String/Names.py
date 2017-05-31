#!/usr/bin/pythonTest
# -*- coding: utf-8 -*-
#
# String Names
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
# Copyright 2007-2016 Rick Graves
#

from six            import print_ as print3

from Dict.Get       import getReverseDictCarefully

class Finished( Exception ): pass

dNickProper = dict( (
    ('ab', ('abner', 'abigail')),
    ('abbie', ('abner', 'abigail')),
    ('abby', ('abigail',)),
    ('abe', ('abel', 'abraham', 'abram')),
    ('abertina', ('alberta',)),
    ('abram', ('abraham',)),
    ('ada', ('adaline',)),
    ('addie', ('adelaide',)),
    ('addy', ('agatha',)),
    ('adela', ('della', 'dell', 'adaline')),
    ('adelaide', ('dell', 'della')),
    ('adeline', ('aline',)),
    ('ag', ('agatha',)),
    ('aggie', ('agatha',)),
    ('aggy', ('augustina', 'augusta', 'agatha', 'agnes')),
    ('agnes', ('inez', 'agatha', 'nancy')),
    ('aileen', ('helena', 'helen')),
    ('al', ('albert', 'allan', 'alan', 'alonzo', 'alanson', 'alfred', 'allen', 'alexander', 'alfonse')),
    ('albert', ('adelbert',)),
    ('albertine', ('alberta',)),
    ('alec', ('alexander',)),
    ('alex', ('alexandra', 'alexander')),
    ('alexandra', ('sandra',)),
    ('alf', ('alfred',)),
    ('alfie', ('alfred',)),
    ('alfy', ('alfreda',)),
    ('algy', ('algernon',)),
    ('alice', ('elsie',)),
    ('alicia', ('alice',)),
    ('aline', ('adaline',)),
    ('alla', ('alexandria',)),
    ('allie', ('alberta', 'alicia', 'almena', 'alice')),
    ('alphonzo', ('alonzo',)),
    ('ana', ('anastasia',)),
    ('andy', ('andrew',)),
    ('angelica', ('angela',)),
    ('angelina', ('angela',)),
    ('angeline', ('angela',)),
    ('ann', ('antonia', 'rosaenna', 'roxanne', 'roxanna', 'rosaenn', 'nancy', 'agnes', 'antoinette')),
    ('anna', ('annette',)),
    ('annie', ('anne', 'ann')),
    ('anselm', ('ansel',)),
    ('antonia', ('antoinette',)),
    ('ara', ('arabella',)),
    ('archie', ('archibald',)),
    ('arnie', ('arnold',)),
    ('art', ('arthur',)),
    ('assene', ('asenath',)),
    ('babs', ('barbara',)),
    ('baldie', ('archibald',)),
    ('barbie', ('barbery', 'barbara')),
    ('barby', ('barbara',)),
    ('barney', ('bernard', 'barnard', 'barnabas')),
    ('bart', ('bartholomew',)),
    ('bartel', ('bartholomew',)),
    ('barth', ('bartholomew',)),
    ('bat', ('bartholomew',)),
    ('bea', ('beatrice',)),
    ('becca', ('rebecca',)),
    ('becky', ('rebecca',)),
    ('bell', ('belinda',)),
    ('bella', ('arabella', 'isabella', 'rosabella', 'isabelle')),
    ('belle', ('rosabel', 'arabella', 'isabella', 'isabelle', 'isabel', 'belinda')),
    ('ben', ('benedict', 'benjamin')),
    ('bennett', ('benedict',)),
    ('bennie', ('benedict',)),
    ('berny', ('bernard',)),
    ('berry', ('greenberry', 'littleberry')),
    ('bert', ('roberta', 'norbert', 'elbert', 'egbert', 'albert', 'herbert', 'delbert', 'hubert', 'alberta', 'gilbert')),
    ('bertie', ('alberta', 'bertha', 'roberta')),
    ('bess', ('elizabeth',)),
    ('beth', ('elizabeth',)),
    ('betsy', ('elizabeth',)),
    ('betty', ('elizabeth',)),
    ('bette', ('elizabeth',)),
    ('bias', ('tobias',)),
    ('biddie', ('obedience',)),
    ('biddy', ('bridget',)),
    ('bill', ('william',)),
    ('bird', ('albert',)),
    ('birdie', ('bertha', 'roberta')),
    ('bob', ('robert',)),
    ('bobbie', ('roberta', 'barbara')),
    ('brad', ('bradford',)),
    ('bridie', ('bridget',)),
    ('brie', ('bridget',)),
    ('bryan', ('brian',)),
    ('bryant', ('brian',)),
    ('burt', ('egbert',)),
    ('cal', ('caleb', 'calvin')),
    ('cam', ('campbell',)),
    ('cammy', ('camille',)),
    ('candy', ('candace',)),
    ('carl', ('charles',)),
    ('carlotta', ('charlotte',)),
    ('carol', ('caroline', 'carolyn')),
    ('carrie', ('caroline', 'carolyn')),
    ('casper', ('jasper',)),
    ('cass', ('caswell', 'cassandra')),
    ('cassie', ('cathleen', 'caroline', 'catherine', 'carolyn', 'cassandra')),
    ('cathy', ('katherina', 'kathleen', 'catherine', 'cathleen', 'katherine', 'katharine')),
    ('ceall', ('lucille',)),
    ('cecilia', ('sheila',)),
    ('celia', ('celeste', 'cecilia')),
    ('chad', ('charles',)),
    ('charles', ('carl',)),
    ('charlie', ('charles',)),
    ('charlotta', ('lotta', 'lotty')),
    ('charlotte', ('lotta', 'lotty')),
    ('chaz', ('charles',)),
    ('chet', ('chester',)),
    ('chick', ('charles',)),
    ('chris', ('christina', 'christian', 'christine', 'christiana', 'kristin', 'christopher', 'kristen')),
    ('christian', ('christopher',)),
    ('christopher', ('christian',)),
    ('christy', ('christiana', 'christine')),
    ('chuck', ('charles',)),
    ('cilla', ('priscilla', 'cicely')),
    ('cille', ('lucille',)),
    ('cindy', ('cynthia', 'lucinda')),
    ('cissy', ('clarissa', 'cecilia')),
    ('claire', ('clara',)),
    ('clara', ('clarissa', 'clarinda')),
    ('clarice', ('clara',)),
    ('clarissa', ('clara',)),
    ('clem', ('clementine',)),
    ('cliff', ('clifton', 'clifford')),
    ('clo', ('chloe',)),
    ('connie', ('constance',)),
    ('cora', ('corinne',)),
    ('cordelia', ('delia',)),
    ('cordy', ('cordelia',)),
    ('corny', ('cornelia',)),
    ('court', ('courtney',)),
    ('crissy', ('chrintina', 'christiana', 'christine', 'chrintine')),
    ('curg', ('lecurgus',)),
    ('curt', ('curtis', 'courtney')),
    ('cy', ('cyrus',)),
    ('daisy', ('margaret',)),
    ('dan', ('sheridan', 'daniel')),
    ('danny', ('sheridan', 'daniel')),
    ('daph', ('daphne',)),
    ('daphie', ('daphne',)),
    ('dave', ('david',)),
    ('davey', ('david',)),
    ('davy', ('david',)),
    ('deannie', ('geraldine',)),
    ('deb', ('deborah', 'debra')),
    ('debbie', ('deborah', 'debra')),
    ('debby', ('deborah',)),
    ('dee', ('audrey', 'dorothy', 'delores')),
    ('deedee', ('deidre',)),
    ('del', ('delbert',)),
    ('delia', ('fidelia', 'cordelia')),
    ('delilah', ('dell', 'della')),
    ('dell', ('delilah',)),
    ('della', ('adela', 'delilah')),
    ('delphia', ('philadelphia',)),
    ('di', ('diana', 'diane')),
    ('diah', ('obadiah', 'jedediah')),
    ('dicey', ('edith',)),
    ('dick', ('zadock', 'melchizedek', 'richard')),
    ('dina', ('geraldine',)),
    ('dolly', ('dorothy',)),
    ('dolph', ('randolph', 'rudolph', 'adolph')),
    ('don', ('donald',)),
    ('dora', ('dorothea', 'eudora', 'theodora', 'dorothy', 'eldora', 'isadora', 'medora', 'doris')),
    ('dorothea', ('dorothy',)),
    ('dosia', ('theodosia',)),
    ('dot', ('dorothy',)),
    ('dotha', ('dorothy',)),
    ('dottie', ('dorothy',)),
    ('dotty', ('dorothy',)),
    ('drew', ('andrew',)),
    ('dyer', ('obadiah', 'jedediah')),
    ('eb', ('ebenezer',)),
    ('eben', ('ebenezer',)),
    ('ed', ('eduardo', 'edwin', 'edgar', 'edmond', 'edward', 'edmund')),
    ('edie', ('edith',)),
    ('edith', ('adaline',)),
    ('edny', ('edna',)),
    ('eileen', ('helena', 'helen')),
    ('elaine', ('eleanor', 'helena', 'helen')),
    ('eleanor', ('helena', 'ellie', 'ella', 'helen')),
    ('elenor', ('leonore', 'leonora')),
    ('eli', ('elijah', 'elisha', 'elias')),
    ('eliza', ('louise',)),
    ('ella', ('eleanor', 'luella', 'gabrielle')),
    ('ellen', ('eleanor', 'helena', 'helen')),
    ('ellis', ('elisha',)),
    ('eloise', ('heloise', 'louise')),
    ('elsie', ('elizabeth', 'alice')),
    ('emanuel', ('manuel',)),
    ('emily', ('amelia', 'emeline')),
    ('emma', ('emeline', 'emily')),
    ('emmanuel', ('immanuel',)),
    ('emmy', ('emeline',)),
    ('eph', ('ephraim',)),
    ('erin', ('aaron',)),
    ('erma', ('emma',)),
    ('ernie', ('ernest', 'earnest')),
    ('erwin', ('irwin',)),
    ('essy', ('estella',)),
    ('esther', ('hester',)),
    ('etta', ('henrietta', 'loretta')),
    ('eve', ('evelyn', 'genevieve')),
    ('ez', ('ezekiel',)),
    ('fanny', ('frances',)),
    ('fay', ('faith',)),
    ('ferdie', ('ferdinand',)),
    ('fidelia', ('delia',)),
    ('field', ('winfield',)),
    ('fina', ('josephine',)),
    ('flo', ('florence',)),
    ('flora', ('florence',)),
    ('floss', ('florence',)),
    ('flossie', ('florence',)),
    ('ford', ('clifford',)),
    ('fran', ('francis', 'francine', 'frances')),
    ('francie', ('francis', 'francine', 'frances')),
    ('frank', ('francis', 'franklin')),
    ('frankie', ('frances',)),
    ('franky', ('veronica',)),
    ('fred', ('frederick', 'winnifred', 'wilfred', 'alfred')),
    ('freddie', ('ferdinand', 'frederick', 'frieda')),
    ('fredric', ('frederick',)),
    ('frieda', ('alfreda',)),
    ('frish', ('frederick',)),
    ('fritz', ('frederick',)),
    ('frona', ('sophronia',)),
    ('fronia', ('sophronia',)),
    ('gabbie', ('gabrielle',)),
    ('gabby', ('gabriella', 'gabrielle')),
    ('gabe', ('gabriel',)),
    ('gabriella', ('ellie', 'ella')),
    ('gail', ('abigail',)),
    ('gatty', ('gertrude',)),
    ('gency', ('genevieve',)),
    ('gene', ('eugene',)),
    ('geoff', ('geoffrey', 'jeffrey')),
    ('georgiana', ('georgia',)),
    ('gerrie', ('geraldine',)),
    ('gerry', ('gerald', 'geraldine')),
    ('gertie', ('gertrude',)),
    ('gil', ('gilbert',)),
    ('gilbert', ('wilber',)),
    ('ginger', ('virginia',)),
    ('ginny', ('virginia',)),
    ('glory', ('gloria',)),
    ('green', ('greenberry',)),
    ('greg', ('gregory',)),
    ('greta', ('margaret',)),
    ('gum', ('montgomery',)),
    ('gus', ('augustine', 'augustus')),
    ('gusie', ('augustina', 'augusta')),
    ('gwen', ('gwendolyn',)),
    ('hal', ('harold', 'howard')),
    ('hank', ('henrietta', 'henry')),
    ('hannah', ('ann', 'susannah', 'anna')),
    ('hans', ('john',)),
    ('harold', ('harry',)),
    ('harry', ('harold', 'henry')),
    ('hattie', ('harriet',)),
    ('hatty', ('harriet',)),
    ('helen', ('eileen', 'ella', 'eleanor', 'ellie', 'elaine', 'elena', 'aileen')),
    ('heloise', ('eloise', 'lois')),
    ('henry', ('harry',)),
    ('herb', ('herbert',)),
    ('hessy', ('hester',)),
    ('hester', ('esther',)),
    ('hetty', ('mehitabel', 'hester')),
    ('hez', ('hezekiah',)),
    ('honey', ('honora',)),
    ('horatio', ('horace',)),
    ('howie', ('howard',)),
    ('hugh', ('hubert',)),
    ('hugo', ('hubert',)),
    ('humey', ('posthuma',)),
    ('ian', ('john',)),
    ('ib', ('isabella', 'isabelle')),
    ('iggy', ('ignatius',)),
    ('ike', ('isaac',)),
    ('irving', ('irvin',)),
    ('irwin', ('erwin',)),
    ('issy', ('isadora', 'isabella', 'isabelle')),
    ('ivan', ('john',)),
    ('izzy', ('isidore',)),
    ('jack', ('john',)),
    ('jackie', ('jacqueline',)),
    ('jake', ('jacob',)),
    ('jamie', ('james',)),
    ('jane', ('jessie', 'joanna', 'virginia')),
    ('janet', ('jane', 'jessie')),
    ('janie', ('jane',)),
    ('jasper', ('casper',)),
    ('jayhugh', ('john',)),
    ('jean', ('john', 'joanna')),
    ('jeanne', ('jeanette',)),
    ('jed', ('jedediah',)),
    ('jeff', ('geoffrey', 'jeffrey')),
    ('jeffrey', ('geoffrey',)),
    ('jehu', ('john',)),
    ('jemma', ('jemima',)),
    ('jennie', ('jean', 'virginia', 'jennifer')),
    ('jenny', ('jane', 'genevieve')),
    ('jeremy', ('jeremiah',)),
    ('jerry', ('gerald', 'geraldine', 'jeremiah')),
    ('jesse', ('jessica',)),
    ('jessica', ('jessie',)),
    ('jessie', ('jane', 'jessica')),
    ('jill', ('julia',)),
    ('jim', ('james',)),
    ('jimmie', ('james',)),
    ('jinsey', ('genevieve',)),
    ('jo', ('josephine',)),
    ('joan', ('joanna',)),
    ('joanna', ('jane', 'jean')),
    ('jody', ('joanna',)),
    ('joe', ('joshua', 'joseph')),
    ('joey', ('josephine', 'josophine', 'joseph')),
    ('johanna', ('joanna',)),
    ('john', ('ivan', 'ian', 'jonathan', 'johannes')),
    ('johnny', ('johannes', 'john', 'jonathon')),
    ('jon', ('jonathan',)),
    ('jonathan', ('johannes', 'nathaniel')),
    ('jorge', ('george',)),
    ('josephine', ('pheney',)),
    ('josey', ('josephine', 'josophine')),
    ('josh', ('joshua',)),
    ('joy', ('joyce',)),
    ('judie', ('judith',)),
    ('judy', ('judith',)),
    ('julie', ('julia',)),
    ('juliet', ('julia',)),
    ('justus', ('justin',)),
    ('karl', ('carl',)),
    ('kate', ('katherina', 'kathleen', 'catherine', 'katelyn', 'cathleen', 'katherine', 'katharine', 'katelin')),
    ('katharine', ('kathleen', 'cathleen', 'catherine', 'katherina')),
    ('kathleen', ('katherina', 'catherine', 'cathleen', 'katherine', 'katharine')),
    ('kathy', ('kathleen', 'kathryn', 'katherine')),
    ('katie', ('katherina', 'kathleen', 'catherine', 'cathleen', 'katherine', 'katharine')),
    ('katy', ('kathleen', 'katherine')),
    ('kay', ('katherina', 'kathleen', 'catherine', 'katelyn', 'cathleen', 'katherine', 'katharine', 'katelin')),
    ('ken', ('kenneth',)),
    ('kim', ('kimberly', 'kimberley')),
    ('kit', ('katherina', 'christian', 'kathleen', 'catherine', 'cathleen', 'christopher', 'katharine', 'katherine')),
    ('kittie', ('katherina', 'kathleen', 'catherine', 'cathleen', 'katherine', 'katharine')),
    ('kristi', ('kristine',)),
    ('ky', ('hezekiah',)),
    ('l.b.', ('littleberry',)),
    ('lanna', ('eleanor',)),
    ('lanson', ('alanson',)),
    ('larry', ('laurence', 'lawrence')),
    ('lars', ('lawrence',)),
    ('laura', ('laurinda', 'loretta', 'lorinda')),
    ('laurie', ('laura','laurinda', 'loretta', 'lorinda')),
    ('laurence', ('lawrence',)),
    ('lee', ('leroy',)),
    ('lem', ('lemuel',)),
    ('lena', ('helena', 'helen', 'madeline', 'arlene')),
    ('lenny', ('leonard',)),
    ('leo', ('leonard',)),
    ('leon', ('napoleon', 'leonidas', 'leonard', 'lionel')),
    ('leonora', ('eleanor',)),
    ('les', ('leslie', 'lester')),
    ('lester', ('leslie',)),
    ('lettice', ('letitia',)),
    ('lettie', ('letitia',)),
    ('letty', ('charlotte',)),
    ('lewis', ('louis',)),
    ('libby', ('elizabeth',)),
    ('lige', ('elijah',)),
    ('lil', ('lillian', 'delilah')),
    ('lila', ('delilah',)),
    ('lilly', ('lillian',)),
    ('linda', ('melinda', 'belinda')),
    ('lindy', ('melinda',)),
    ('link', ('lincoln',)),
    ('lisa', ('melissa', 'alice')),
    ('lish', ('elisha',)),
    ('little', ('littleberry',)),
    ('livia', ('olivia',)),
    ('liz', ('elizabeth',)),
    ('liza', ('elizabeth',)),
    ('lizabeth', ('elizabeth',)),
    ('lizzie', ('eliza', 'elizabeth')),
    ('lloyd', ('floyd',)),
    ('lodi', ('melody',)),
    ('lois', ('heloise', 'louise')),
    ('lola', ('delores',)),
    ('lolly', ('lillian',)),
    ('lon', ('alonzo', 'zebulon', 'lawrence')),
    ('lonzo', ('alonzo',)),
    ('lorie', ('loretta', 'lorraine')),
    ('lorrie', ('loretta', 'lorraine')),
    ('lorry', ('lawrence',)),
    ('lotta', ('charlotte',)),
    ('lottie', ('charlotte', 'carlotta')),
    ('lou', ('louis', 'louise')),
    ('louie', ('louis',)),
    ('louise', ('eloise', 'lois')),
    ('lucas', ('lucias',)),
    ('lucy', ('lucille', 'lucia', 'lucinda')),
    ('luella', ('ellie', 'ella')),
    ('luke', ('lucias', 'lucas')),
    ('lulu', ('louise',)),
    ('lum', ('columbus',)),
    ('lura', ('lurana',)),
    ('lynn', ('caroline', 'carolyn')),
    ('mabel', ('mehitabel',)),
    ('maddie', ('madeline',)),
    ('maddy', ('madeline', 'madelyn')),
    ('madge', ('margaret', 'madeline', 'margaretta', 'magdelina')),
    ('madie', ('madeline', 'madelyn')),
    ('mae', ('may', 'mary')),
    ('maggie', ('margaret', 'madeline')),
    ('maggy', ('margaret',)),
    ('maisie', ('margaret',)),
    ('mamie', ('mary',)),
    ('manda', ('amanda',)),
    ('mandy', ('amanda', 'miranda')),
    ('manny', ('emanuel', 'manuel')),
    ('manuel', ('immanuel', 'emanuel')),
    ('margaret', ('gretchen', 'daisy')),
    ('marge', ('margaret', 'marjorie', 'margaretta')),
    ('margie', ('margaret', 'marjorie')),
    ('margo', ('margaret',)),
    ('margy', ('margaret', 'marjorie')),
    ('maria', ('mariah', 'mary')),
    ('mariah', ('mary',)),
    ('marianna', ('marian',)),
    ('marie', ('mary',)),
    ('marietta', ('mary',)),
    ('marion', ('mary',)),
    ('mark', ('marcus',)),
    ('marty', ('martha', 'martin')),
    ('marv', ('marvin',)),
    ('mary', ('mariah', 'mitzi', 'miriam', 'marilyn', 'maureen')),
    ('mat', ('martha', 'matilda')),
    ('matt', ('mathew', 'matthew')),
    ('matthias', ('matthew',)),
    ('mattie', ('martha',)),
    ('matty', ('matilda',)),
    ('maud', ('madeline', 'matilda')),
    ('maureen', ('mary',)),
    ('maury', ('maurice',)),
    ('may', ('mary',)),
    ('meg', ('margaret', 'megan')),
    ('megan', ('margaret',)),
    ('mehitabel', ('mabel',)),
    ('mel', ('amelia', 'melissa', 'melinda')),
    ('melchizedek', ('zadock',)),
    ('melia', ('amelia',)),
    ('mena', ('almena',)),
    ('merci', ('mercedes',)),
    ('mercy', ('mercedes',)),
    ('mert', ('myrtle',)),
    ('merv', ('marvin', 'mervin')),
    ('mervyn', ('marvin',)),
    ('michael', ('mitchell',)),
    ('mickey', ('michelle', 'michael')),
    ('middy', ('madeline',)),
    ('midge', ('margaret',)),
    ('mike', ('michael',)),
    ('millie', ('camille', 'amelia', 'emeline')),
    ('milly', ('millicent', 'mildred', 'melissa', 'armilda')),
    ('mimi', ('jemima',)),
    ('mina', ('wilhelmina', 'minerva')),
    ('mindy', ('melinda',)),
    ('minerva', ('manerva',)),
    ('minnie', ('wilhelmina', 'minerva')),
    ('mira', ('elmira', 'miranda')),
    ('missy', ('melissa',)),
    ('mitch', ('mitchell',)),
    ('mitchell', ('michael',)),
    ('mitty', ('mehitabel', 'submit')),
    ('mitzi', ('mary', 'miriam')),
    ('molly', ('mary',)),
    ('mona', ('ramona',)),
    ('monty', ('lamont', 'montgomery')),
    ('morris', ('maurice',)),
    ('mort', ('mortimer',)),
    ('mose', ('moses',)),
    ('moss', ('moses',)),
    ('mur', ('muriel',)),
    ('myra', ('almira',)),
    ('myrt', ('myrtle',)),
    ('nabby', ('abigail',)),
    ('nace', ('ignatius',)),
    ('nada', ('nadine',)),
    ('nan', ('hannah', 'ann', 'anna', 'nancy')),
    ('nana', ('ann', 'anna')),
    ('nancy', ('ann', 'anna')),
    ('nannie', ('nancy',)),
    ('nanny', ('hannah', 'ann', 'anna')),
    ('nap', ('napoleon',)),
    ('nat', ('jonathan', 'nathaniel')),
    ('nate', ('nathan', 'nathaniel')),
    ('nathan', ('jonathan', 'nathaniel')),
    ('natty', ('nathaniel',)),
    ('ned', ('edward', 'edmund')),
    ('neil', ('cornelius',)),
    ('nell', ('eleanor', 'helena', 'helen')),
    ('nelle', ('cornelia',)),
    ('nellie', ('eleanor', 'helena', 'helen')),
    ('nelly', ('cornelia',)),
    ('nels', ('nelson',)),
    ('neppie', ('penelope',)),
    ('nerva', ('manerva', 'minerva')),
    ('nervie', ('manerva', 'minerva')),
    ('nessie', ('agnes',)),
    ('nettie', ('jeanette', 'henrietta', 'antonia', 'natalie', 'antoinette')),
    ('newt', ('newton',)),
    ('nib', ('isabella', 'isabelle')),
    ('nicey', ('vernisee',)),
    ('nick', ('dominic', 'nicholas', 'nicodemus')),
    ('nickie', ('nicholas',)),
    ('nicky', ('nicholas',)),
    ('nita', ('juanita',)),
    ('noel', ('nowell',)),
    ('nora', ('leonore', 'leonora', 'eleanor')),
    ('obe', ('obadiah',)),
    ('obed', ('obadiah', 'obedience')),
    ('obie', ('obadiah', 'obediah')),
    ('odo', ('odell',)),
    ('olive', ('olivia',)),
    ('ollie', ('oliver',)),
    ('ophi', ('theophilus',)),
    ('ora', ('aurelia',)),
    ('orlando', ('roland',)),
    ('ossy', ('oswald',)),
    ('oswald', ('waldo',)),
    ('ote', ('otis',)),
    ('ozzy', ('oswald',)),
    ('paddy', ('patrick',)),
    ('pam', ('pamela',)),
    ('pat', ('patience', 'patricia', 'patrick')),
    ('patsy', ('patrick', 'martha', 'patricia')),
    ('patty', ('patience', 'martha', 'patricia')),
    ('peggie', ('margaret',)),
    ('peggy', ('margaret',)),
    ('penny', ('penelope',)),
    ('perce', ('percival',)),
    ('percy', ('percival',)),
    ('pete', ('peter',)),
    ('peter', ('patrick',)),
    ('phelia', ('orphelia',)),
    ('phil', ('phillip', 'philip')),
    ('philadelphia', ('delpha',)),
    ('pokey', ('pocahontas',)),
    ('polly', ('paulina', 'mary')),
    ('pres', ('prescott',)),
    ('prissy', ('priscilla',)),
    ('prudy', ('prudence',)),
    ('rae', ('rachel',)),
    ('rafe', ('ralph',)),
    ('raff', ('raphael',)),
    ('randall', ('randolph',)),
    ('randy', ('randolph', 'miranda')),
    ('ray', ('rachel', 'raymond')),
    ('reba', ('rebecca',)),
    ('reg', ('reginald',)),
    ('reggie', ('reginald',)),
    ('reginald', ('reynold',)),
    ('rena', ('irene',)),
    ('rennie', ('irene',)),
    ('retta', ('henrietta', 'loretta')),
    ('reynold', ('reginald',)),
    ('rich', ('aldrich', 'richard')),
    ('richie', ('aldrich', 'richard')),
    ('rick', ('derick', 'eric', 'richard', 'ricardo', 'frederick')),
    ('ricky', ('derick', 'eric', 'broderick', 'richard')),
    ('rilla', ('avarilla',)),
    ('rita', ('margarita',)),
    ('rob', ('robert', 'roberto')),
    ('robbie', ('roberta',)),
    ('robby', ('robert',)),
    ('robin', ('robert',)),
    ('rod', ('roderick', 'rodney', 'broderick')),
    ('rodie', ('rhoda',)),
    ('roland', ('orlando',)),
    ('rolf', ('rudolph',)),
    ('rollo', ('rudolph',)),
    ('ron', ('ronald', 'veronica', 'aaron')),
    ('ronna', ('veronica',)),
    ('ronnie', ('ronald', 'veronica', 'aaron')),
    ('ronny', ('ronald', 'veronica')),
    ('rose', ('rosabel', 'roseanna', 'rosabella', 'roseann', 'roxanna', 'roxanne', 'rosalyn')),
    ('rowland', ('roland',)),
    ('rox', ('roxane',)),
    ('roxie', ('roxane',)),
    ('roy', ('leroy',)),
    ('roz', ('rosabel', 'rosabella', 'rosalyn')),
    ('rube', ('reuben',)),
    ('rudy', ('rudolph',)),
    ('rupert', ('robert',)),
    ('russ', ('russell',)),
    ('rusty', ('russell',)),
    ('sabe', ('isabella', 'isabelle')),
    ('sabra', ('isabella', 'isabelle')),
    ('sadie', ('sarah',)),
    ('sal', ('sarah', 'solomon', 'salvador')),
    ('sallie', ('sarah',)),
    ('salmon', ('solomon',)),
    ('sam', ('samson', 'samuel', 'sampson')),
    ('sammy', ('samuel',)),
    ('sandra', ('cassandra',)),
    ('sandy', ('alexander', 'cassandra', 'sandra')),
    ('sara', ('sarah',)),
    ('scott', ('prescott',)),
    ('sene', ('asenath',)),
    ('shelly', ('michelle', 'rachel', 'shelton')),
    ('si', ('silas', 'sylvester')),
    ('sid', ('sidney',)),
    ('sig', ('sigismund',)),
    ('silla', ('drusilla',)),
    ('sim', ('simeon',)),
    ('simon', ('simeon',)),
    ('sis', ('frances',)),
    ('sly', ('sylvester',)),
    ('sol', ('solomon',)),
    ('solly', ('solomon',)),
    ('sophia', ('sophronia',)),
    ('stacia', ('eustacia',)),
    ('stacy', ('eustacia',)),
    ('stella', ('estella',)),
    ('steve', ('stephen', 'steven')),
    ('steven', ('stephen',)),
    ('sue', ('susannah', 'suzanne', 'susan')),
    ('sukey', ('susannah',)),
    ('sully', ('sullivan',)),
    ('surry', ('sarah',)),
    ('susan', ('susannah',)),
    ('susanna', ('ann', 'anna')),
    ('susannah', ('hannah',)),
    ('susie', ('susannah', 'suzanne', 'susan')),
    ('suzanne', ('susannah',)),
    ('syl', ('sylvester',)),
    ('tabby', ('tabitha',)),
    ('tad', ('thaddeus',)),
    ('tavia', ('octavia',)),
    ('ted', ('theodore', 'edward', 'edmund')),
    ('teddy', ('theodore',)),
    ('terry', ('teresa', 'theresa', 'terence')),
    ('tess', ('teresa', 'theresa')),
    ('tessa', ('teresa', 'theresa')),
    ('tessie', ('teresa', 'theresa')),
    ('thad', ('thaddeus',)),
    ('theo', ('theodore', 'theodosia')),
    ('thom', ('thomas',)),
    ('thursa', ('theresa',)),
    ('tibbie', ('isabella', 'isabelle')),
    ('ticy', ('theresa',)),
    ('tilda', ('matilda',)),
    ('tillie', ('matilda',)),
    ('tim', ('timothy',)),
    ('timmy', ('timothy',)),
    ('tina', ('augustina', 'christine', 'christiana', 'christina', 'augusta', 'martina', 'ernestine')),
    ('tish', ('letitia',)),
    ('titia', ('letitia',)),
    ('tobe', ('tobias',)),
    ('toby', ('tobias',)),
    ('tom', ('thomas',)),
    ('tommy', ('thom', 'thomas')),
    ('tony', ('anthony',)),
    ('tori', ('victoria',)),
    ('torie', ('victoria',)),
    ('torri', ('victoria',)),
    ('torrie', ('victoria',)),
    ('tory', ('victoria',)),
    ('tracy', ('theresa',)),
    ('tricia', ('patricia',)),
    ('trina', ('katherina', 'kathleen', 'catherine', 'cathleen', 'katherine', 'katharine')),
    ('trisha', ('beatrice', 'patricia')),
    ('trixie', ('beatrice', 'patricia')),
    ('trudy', ('gertrude',)),
    ('val', ('valentina', 'valeri', 'valerie')),
    ('vallie', ('valentina',)),
    ('van', ('vanessa',)),
    ('vannie', ('vanessa',)),
    ('verna', ('laverne',)),
    ('vester', ('sylvester',)),
    ('vi', ('vivian',)),
    ('vic', ('victor',)),
    ('vick', ('victor',)),
    ('vicki', ('victoria',)),
    ('vin', ('vincent',)),
    ('vina', ('melvina',)),
    ('vince', ('vincent',)),
    ('viney', ('lavinia',)),
    ('virgie', ('virginia',)),
    ('virginia', ('jane',)),
    ('vonnie', ('veronica',)),
    ('waldo', ('oswald',)),
    ('wallie', ('wallace',)),
    ('wally', ('wallace','walter')),
    ('wat', ('walter',)),
    ('webb', ('webster',)),
    ('wendy', ('gwendolyn',)),
    ('wilber', ('gilbert',)),
    ('will', ('william', 'wilson', 'wilbur')),
    ('willie', ('wilhelmina', 'william', 'wilson', 'wilfred', 'wilbur')),
    ('wilma', ('wilhelmina',)),
    ('win', ('winfield',)),
    ('winnet', ('winifred',)),
    ('winnie', ('winifred', 'winnifred')),
    ('winny', ('winnifred', 'winfield')),
    ('zach', ('zachariah',)),
    ('zacharias', ('zachariah',)),
    ('zachary', ('zachariah',)),
    ('zadock', ('melchizedek',)),
    ('zeb', ('zebulon',)),
    ('zed', ('zedediah',)),
    ('zeke', ('isaac', 'ezekiel', 'zachariah')),
    ('zeph', ('zepaniah',)),
    ('zolly', ('solomon',)) ) )

#   ('karen', ('katherina', 'kathleen', 'catherine', 'cathleen', 'katherine', 'katharine')),


for sNick in dNickProper:
    #
    dNickProper[ sNick ] = frozenset( dNickProper[ sNick ] )
    #


setMenNames = \
    frozenset( (
        'aaron', 'abraham', 'adam', 'adrian', 'ahmed', 'al', 'alan', 'albert',
        'alberto', 'alec', 'alejandro', 'alex', 'alexander', 'alfonso',
        'alfred', 'alfredo', 'allan', 'allen', 'alvin', 'anders', 'andre',
        'andreas', 'andres', 'andrew', 'andy', 'anthony', 'antonio', 'arnold',
        'arthur', 'austin', 'avery', 'barry', 'bart', 'ben', 'benjamin',
        'bennett', 'bernard', 'bert', 'bill', 'billy', 'blair', 'blake', 'bob',
        'bobby', 'brad', 'bradford', 'bradley', 'brandon', 'brendan', 'brent',
        'bret', 'brett', 'brian', 'bruce', 'bryan', 'byron', 'calvin',
        'cameron', 'campbell', 'carl', 'carlos', 'carlton', 'casey', 'cecil',
        'cesar', 'chad', 'charles', 'charlie', 'chester', 'chris',
        'christian', 'christopher', 'clarence', 'clark', 'claude', 'clay',
        'clayton', 'clifford', 'clyde', 'cody', 'colin', 'conrad', 'corey',
        'cory', 'craig', 'curtis', 'dale', 'dan', 'daniel', 'danny', 'darrell',
        'darren', 'darryl', 'dave', 'david', 'davis', 'dean', 'denis',
        'dennis', 'derek', 'derrick', 'diego', 'dimitri', 'dirk', 'dominic',
        'don', 'donald', 'doug', 'douglas', 'duane', 'duncan', 'dustin',
        'dwayne', 'dwight', 'dylan', 'earl', 'ed', 'eddie', 'edgar', 'edmund',
        'eduardo', 'edward', 'edwin', 'eli', 'eliot', 'elliot', 'elliott',
        'elmer', 'emanuel', 'emmanuel', 'enrique', 'eric', 'erik', 'ernest',
        'ernesto', 'ethan', 'eugene', 'evan', 'everett', 'fernando',
        'fitzgerald', 'floyd', 'forrest', 'francis', 'francisco', 'frank',
        'franklin', 'fred', 'frederic', 'frederick', 'fredrick', 'gabriel',
        'garrett', 'gary', 'gene', 'geoffrey', 'george', 'gerald', 'gerard',
        'gilbert', 'giovanni', 'glen', 'glenn', 'gordon', 'graham', 'grant',
        'greg', 'gregg', 'gregory', 'guido', 'guy', 'hamilton', 'hans',
        'harold', 'harris', 'harrison', 'harry', 'harvey', 'henry', 'herbert',
        'herman', 'howard', 'hugh', 'hunter', 'ian', 'ira', 'isaac', 'ivan',
        'jack', 'jackson', 'jacob', 'jacques', 'james', 'jamie', 'jared',
        'jason', 'jay', 'jeff', 'jeffery', 'jeffrey', 'jeremiah', 'jeremy',
        'jerome', 'jerry', 'jesse', 'jesus', 'jim', 'jimmie', 'jimmy', 'joe',
        'joel', 'johan', 'johannes', 'john', 'johnny', 'johnson', 'jon',
        'jonah', 'jonathan', 'jonathon', 'jordan', 'jorge', 'jose', 'josef',
        'joseph', 'josh', 'joshua', 'juan', 'julian', 'julio', 'julius',
        'justin', 'karl', 'keith', 'ken', 'kendall', 'kenneth', 'kent',
        'kerry', 'kevin', 'kirk', 'kurt', 'kyle', 'lance', 'larry', 'lars',
        'laurence', 'lawrence', 'lee', 'leland', 'leo', 'leon', 'leonard',
        'leroy', 'lester', 'lewis', 'liam', 'lloyd', 'lou', 'louis', 'lucas',
        'luis', 'luke', 'mackenzie', 'malcolm', 'manuel', 'marc', 'marco',
        'marcus', 'mario', 'mark', 'markus', 'marshall', 'martin', 'marvin',
        'mathew', 'matt', 'matthew', 'maurice', 'max', 'maxwell', 'melvin',
        'michael', 'micheal', 'miguel', 'mike', 'miles', 'milton', 'mitchell',
        'mohamed', 'mohammad', 'mohammed', 'morgan', 'morris', 'murray',
        'nathan', 'nathaniel', 'neal', 'neil', 'nelson', 'nicholas', 'nick',
        'nicolas', 'noah', 'noel', 'norman', 'omar', 'oscar', 'owen', 'paolo',
        'patrick', 'paul', 'pedro', 'perry', 'peter', 'phil', 'philip',
        'philippe', 'phillip', 'pierce', 'pierre', 'rafael', 'ralph', 'ramon',
        'randall', 'randolph', 'randy', 'raul', 'ray', 'raymond', 'reed',
        'reginald', 'ricardo', 'richard', 'richardo', 'rick', 'ricky', 'rob',
        'robert', 'roberto', 'roderick', 'rodney', 'roger', 'roland', 'rolf',
        'ron', 'ronald', 'ronnie', 'ross', 'roy', 'russ', 'russell', 'ryan',
        'sam', 'samuel', 'scot', 'scott', 'sean', 'sebastian', 'sergio',
        'seth', 'shane', 'shawn', 'sheldon', 'sherman', 'sidney', 'simon',
        'simone', 'spencer', 'stan', 'stanley', 'stefan', 'stephan', 'stephen',
        'sterling', 'steve', 'steven', 'stewart', 'stuart', 'sydney', 'taylor',
        'ted', 'terence', 'terrence', 'terry', 'theodore', 'thomas', 'tim',
        'timothy', 'toby', 'todd', 'tom', 'tommy', 'tony', 'travis', 'trevor',
        'troy', 'tyler', 'tyrone', 'vernon', 'victor', 'vincent', 'wade',
        'walker', 'wallace', 'walter', 'ward', 'warren', 'wayne', 'wesley',
        'will', 'willard', 'william', 'willie', 'wilson', 'winston',
        'wolfgang', 'zachary') )

setWomenNames = \
    frozenset( (
        'abby', 'abigail', 'adele', 'adriana', 'adrienne', 'agnes', 'aileen',
        'aimee', 'alana', 'alberta', 'alejandra', 'alessandra', 'alexa',
        'alexandra', 'alexandre', 'alexandria', 'alexis', 'ali', 'alice',
        'alicia', 'alisa', 'alison', 'alissa', 'allison', 'allyson', 'alma',
        'alyce', 'alyssa', 'amanda', 'amber', 'amelia', 'ami', 'amy', 'ana',
        'anastasia', 'andrea', 'angel', 'angela', 'angelica', 'angelina',
        'angelique', 'angie', 'anita', 'ann', 'anna', 'annabel', 'annabelle',
        'anne', 'annemarie', 'annette', 'annie', 'annika', 'antoinette',
        'antonia', 'april', 'ariane', 'ariel', 'arielle', 'arlene', 'ashleigh',
        'ashley', 'athena', 'audrey', 'autumn', 'barbara', 'beatrice', 'becky',
        'belinda', 'bernadette', 'bernice', 'bertha', 'bessie', 'beth',
        'bethany', 'betsy', 'betty', 'beverly', 'bianca', 'bonnie', 'brandi',
        'brandy', 'brenda', 'bridget', 'brigitte', 'brittany', 'brittney',
        'brooke', 'caitlin', 'camille', 'candace', 'candice', 'cara', 'carla',
        'carmela', 'carmen', 'carol', 'carole', 'carolina', 'caroline',
        'carolyn', 'carrie', 'carroll', 'cassandra', 'caterina', 'catharine',
        'catherine', 'cathleen', 'cathy', 'cecelia', 'cecile', 'cecilia',
        'celeste', 'celia', 'charlene', 'charlotte', 'chelsea', 'cher',
        'cherie', 'cheryl', 'chloe', 'christa', 'christiane', 'christie',
        'christina', 'christine', 'christy', 'cindy', 'claire', 'clara',
        'clare', 'clarissa', 'claudia', 'colette', 'colleen', 'connie',
        'constance', 'corinne', 'courtney', 'cristina', 'crystal', 'cynthia',
        'daisy', 'dana', 'daniela', 'daniele', 'danielle', 'daphne', 'dara',
        'darcy', 'darlene', 'dawn', 'deanna', 'debbie', 'deborah', 'debra',
        'dee', 'deirdre', 'delores', 'dena', 'denise', 'desiree', 'diana',
        'diane', 'dianne', 'dina', 'dolores', 'dominique', 'donna', 'doreen',
        'doris', 'dorothy', 'edith', 'edna', 'eileen', 'elaine', 'eleanor',
        'elena', 'elisa', 'elisabeth', 'elise', 'elissa', 'eliza',
        'elizabeth', 'ella', 'ellen', 'ellyn', 'eloise', 'elsa', 'elsie',
        'elyse', 'emilia', 'emilie', 'emily', 'emma', 'erica', 'erika',
        'erin', 'estelle', 'esther', 'ethel', 'eugenia', 'eva', 'eve',
        'evelyn', 'faith', 'fanny', 'fatima', 'fay', 'faye', 'felicia', 'fern',
        'fiona', 'florence', 'fran', 'frances', 'francesca', 'francine',
        'francois', 'francoise', 'gabriela', 'gabriele', 'gabriella',
        'gabrielle', 'gail', 'gale', 'gayle', 'genevieve', 'georgia',
        'georgina', 'geraldine', 'gertrude', 'gillian', 'gina', 'ginger',
        'giovanna', 'gladys', 'glenda', 'gloria', 'grace', 'greta', 'gretchen',
        'gwen', 'gwendolyn', 'hanna', 'hannah', 'harriet', 'hazel', 'heather',
        'heidi', 'helen', 'helena', 'helene', 'hilary', 'hilda', 'hillary',
        'holly', 'hope', 'ida', 'ilana', 'ilene', 'ines', 'ingrid', 'irene',
        'iris', 'isabel', 'isabella', 'isabelle', 'jaclyn', 'jacqueline',
        'jacquelyn', 'jaime', 'jamie', 'jana', 'jane', 'janelle', 'janet',
        'janice', 'janine', 'janis', 'jasmine', 'jayne', 'jean', 'jeanette',
        'jeanne', 'jeannette', 'jenna', 'jennie', 'jennifer', 'jenny',
        'jessica', 'jessie', 'jill', 'jillian', 'jo', 'joan', 'joann',
        'joanna', 'joanne', 'jocelyn', 'jodi', 'jody', 'joelle', 'johanna',
        'josephine', 'joy', 'joyce', 'juanita', 'judith', 'judy', 'julia',
        'juliana', 'julianne', 'julie', 'juliet', 'juliette', 'june',
        'justine', 'kara', 'karen', 'karin', 'karla', 'katarina', 'kate',
        'katharina', 'katharine', 'katherine', 'kathleen', 'kathryn', 'kathy',
        'katia', 'katie', 'katrina', 'katy', 'kay', 'kayla', 'kelli',
        'kellie', 'kelly', 'kelsey', 'kim', 'kimberley', 'kimberly',
        'kirsten', 'kitty', 'krista', 'kristen', 'kristi', 'kristin',
        'kristina', 'kristine', 'kristy', 'krystal', 'lara', 'larissa',
        'latoya', 'laura', 'laurel', 'lauren', 'laurie', 'lea', 'leah',
        'leanne', 'leigh', 'leila', 'leilani', 'lena', 'leslie', 'liana',
        'lila', 'lillian', 'lillie', 'lily', 'linda', 'lindsay', 'lindsey',
        'lisa', 'lise', 'liz', 'liza', 'lois', 'lora', 'loraine', 'loren',
        'loretta', 'lori', 'lorraine', 'louisa', 'louise', 'lucia', 'lucie',
        'lucille', 'lucy', 'luisa', 'lydia', 'lyn', 'lynda', 'lynette',
        'lynn', 'lynne', 'madeleine', 'madeline', 'mae', 'magdalena',
        'maggie', 'mara', 'marcia', 'margaret', 'margarita', 'margo',
        'margot', 'marguerite', 'mari', 'maria', 'mariah', 'marian',
        'mariana', 'marianna', 'marianne', 'marie', 'marilyn', 'marina',
        'marion', 'marisa', 'marissa', 'marjorie', 'marla', 'marlene',
        'marsha', 'marta', 'martha', 'martina', 'mary', 'maryam', 'maryann',
        'maura', 'maureen', 'maxine', 'may', 'maya', 'meemie', 'meg', 'megan',
        'meghan', 'mei', 'melanie', 'melinda', 'melissa', 'melody', 'mercedes',
        'meredith', 'meryl', 'mia', 'michaela', 'michele', 'michelle',
        'mildred', 'mindy', 'miranda', 'mireille', 'miriam', 'misty', 'moira',
        'molly', 'mona', 'monica', 'monika', 'monique', 'muriel', 'myra',
        'myrtle', 'nadia', 'nadine', 'nancy', 'nanette', 'naomi', 'natalia',
        'natalie', 'natasha', 'nathalie', 'nell', 'nellie', 'new', 'nichole',
        'nicola', 'nicole', 'nikki', 'nina', 'noelle', 'nora', 'norma', 'olga',
        'oliver', 'olivia', 'paige', 'pam', 'pamela', 'patrice', 'patricia',
        'patsy', 'patti', 'paula', 'paulette', 'pauline', 'pearl', 'peggy',
        'penelope', 'penny', 'phyllis', 'polly', 'priscilla', 'rachael',
        'rachel', 'rachelle', 'ramona', 'raquel', 'rebecca', 'rebekah',
        'regina', 'rene', 'renee', 'rhonda', 'rita', 'roberta', 'robin',
        'robyn', 'rochelle', 'rosa', 'rosalie', 'rose', 'rosemarie',
        'rosemary', 'roxanne', 'ruby', 'ruth', 'sabina', 'sabine', 'sabrina',
        'sally', 'samantha', 'sandra', 'sara', 'sarah', 'sasha', 'shana',
        'shannon', 'shari', 'sharon', 'shauna', 'sheila', 'shelley', 'shelly',
        'sheri', 'sherri', 'sherry', 'sheryl', 'shirley', 'silvia', 'sofia',
        'sonia', 'sonja', 'sonya', 'sophia', 'sophie', 'stacey', 'stacy',
        'stefanie', 'stella', 'stephanie', 'sue', 'susan', 'susana', 'susanna',
        'susannah', 'susanne', 'suzan', 'suzanne', 'sybil', 'sylvia', 'tamara',
        'tammy', 'tania', 'tanya', 'tara', 'tatiana', 'teresa', 'terese',
        'teri', 'terri', 'terry', 'tessa', 'thelma', 'theresa', 'therese',
        'tiffany', 'tina', 'toni', 'tonya', 'tracey', 'tracy', 'tricia',
        'trisha', 'ursula', 'valerie', 'vanessa', 'vera', 'veronica', 'vicki',
        'vickie', 'victoria', 'viola', 'violet', 'virginia', 'vivian', 'wanda',
        'wendy', 'whitney', 'willie', 'wilma', 'winifred', 'xavier', 'yolanda',
        'yvette', 'yvonne', 'zoe', 'zulema' ) )



dBegsNicks = \
    dict(
        ty      = 'ty',
        ed      = 'ed',
        jo      = 'jo',
        rod     = 'rod',
        wil     = 'willie',
        es      = 'essy',
        mac     = ( 'mac', 'mack' ),
        mc      = ( 'mac', 'mack' ) )

#       is      = 'issy',
#       max     = ( 'maxine', 'max' )

dBegsNicks[ 'is'  ] = 'issy'
dBegsNicks[ 'max' ] = ( 'maxine', 'max' )


dNicksBegs = getReverseDictCarefully( dBegsNicks )


dEndsNicks = \
    dict(
        field   = 'field',
        leen    = ( 'lena', 'lynn' ),
        lina    = ( 'lena', 'lina', 'lynn' ),
        lena    = 'lina',
        lene    = 'lynn',
        lyn     = 'lynn',
        rita    = 'rita',
        tina    = 'tina',
        tine    = 'tina' )


dNicksEnds = getReverseDictCarefully( dEndsNicks )


dWithinsNicks = \
    dict(
         wood   = ( 'woody', 'woodrow', 'elwood' ),
         scott  = 'scott' )


dNicksWithins = getReverseDictCarefully( dWithinsNicks )




def _testNames( sName1, sName2, dOthersNicks, dNicksOthers, fGetSlice ):
    #
    from Collect.Test   import ContainsAny
    from Iter.AllVers   import iRange
    #
    if      sName1 in dNicksOthers and \
            sName2 in dNicksOthers and \
            ContainsAny(
                dNicksOthers[ sName1 ], dNicksOthers[ sName2 ] ):
        #
        raise Finished
        #
    #
    for i in iRange( 2, 6 ):
        #
        if len( sName1 ) < i and len( sName2 ) < i: break
        #
        sName1Part = fGetSlice( sName1, i )
        sName2Part = fGetSlice( sName2, i )
        #
        if      sName1Part == sName2Part and \
                sName1Part in dOthersNicks and \
                ( sName1 == sName1Part or sName2 == sName1Part ):
            #
            raise Finished
            #
        #
        if      sName1Part in dOthersNicks and \
                sName2 in dNicksOthers and \
                sName1Part in dNicksOthers[ sName2 ]:
            #
            raise Finished
        #
        if      sName2Part in dOthersNicks and \
                sName1 in dNicksOthers and \
                sName2Part in dNicksOthers[ sName1 ]:
            #
            raise Finished
        #
        if      sName1Part in dOthersNicks and \
                sName2Part in dOthersNicks and \
                ( sName1 == sName1Part or sName2 == sName1Part ) and \
                ContainsAny(
                    dOthersNicks[ sName1Part ], dOthersNicks[ sName2Part ] ):
            #
            raise Finished
        #




def _getPartBeg( s, i ): return s[    : i ]
def _getPartEnd( s, i ): return s[ -i :   ]



def isNickName( sName1, sName2 ):
    #
    from Collect.Query  import get1stThatMeets
    from Collect.Test   import ContainsAny
    from Dict.Get       import getKeyIter
    from String.Test    import getItemFoundInString
    #
    sName1, sName2  = sName1.lower(), sName2.lower()
    #
    bNickNames      = False
    #
    tHaveNicks = ( sName1 in dNickProper, sName2 in dNickProper )
    #
    try:
        #
        if tHaveNicks == ( False, False ):
            #
            pass # most common result, bypass other tests of tHaveNicks
            #
        elif tHaveNicks == ( True, True ):
            #
            setPropers1   = dNickProper[ sName1 ]
            setPropers2   = dNickProper[ sName2 ]
            #
            if      setPropers1 == setPropers2              or \
                    ContainsAny( setPropers1, setPropers2 ) or \
                    sName2 in dNickProper[ sName1 ]         or \
                    sName1 in dNickProper[ sName2 ]:
                #
                raise Finished
                #
            #
        elif tHaveNicks == ( True, False ):
            #
            if sName2 in dNickProper[ sName1 ]:
                #
                raise Finished
                #
            #
        elif tHaveNicks == ( False, True ):
            #
            if sName1 in dNickProper[ sName2 ]:
                #
                raise Finished
                #
            #
        #
        # _testNames wull raise Finished if bNickNames set to True
        _testNames( sName1, sName2, dBegsNicks, dNicksBegs, _getPartBeg )
        # _testNames wull raise Finished if bNickNames set to True
        #
        # _testNames wull raise Finished if bNickNames set to True
        _testNames( sName1, sName2, dEndsNicks, dNicksEnds, _getPartEnd )
        # _testNames wull raise Finished if bNickNames set to True
        #
        if sName1 in dNicksWithins:
            #
            def name2HasSubstring( sub ): return sub in sName2
            #
            if get1stThatMeets(
                    getKeyIter( dWithinsNicks ), name2HasSubstring ):
                raise Finished
        #
        if sName2 in dNicksWithins:
            #
            def name1HasSubstring( sub ): return sub in sName1
            #
            if get1stThatMeets(
                    getKeyIter( dWithinsNicks ), name1HasSubstring ):
                raise Finished
        #
        #
        #
    except Finished:
        #
        bNickNames  = True
        #
    #
    return bNickNames



def isWomensName( sName ):
    #
    return sName.lower() in setWomenNames



def isMensName( sName ):
    #
    return sName.lower() in setMenNames



def isNameMisSpelled( sName1, sName2 ):
    #
    from Iter.AllVers import lZip
    from Collect.Query import getBegAndEndIfInOrder
    #
    bNameMisSpelled = True
    #
    # bPrint= ( sName1, sName2 ) == ( 'John', 'Joel' )
    #
    try:
        #
        if not ( sName1 and sName2 ):
            # if bPrint: print3( 'got blank' )
            raise Finished
            #
        #
        if      ( isWomensName( sName1 ) and isMensName( sName2 ) ) or \
                ( isWomensName( sName2 ) and isMensName( sName1 ) ):
            #
            raise Finished
            #
        #
        iLen1, iLen2 = len( sName1 ), len( sName2 )
        #
        # if bPrint: print3( 'sName1, sName2:', sName1, sName2 )
        #
        # if bPrint: print3( 'iLen1, iLen2:', iLen1, iLen2 )
        #
        if min( iLen1, iLen2 ) < 2:
            # if bPrint: print3( 'too short' )
            raise Finished
            #
        #
        if abs( iLen1 - iLen2 ) > 2:
            # if bPrint: print3( 'different lengths' )
            raise Finished
            #
        #
        iHalfLen    = min( iLen1, iLen2 ) // 2
        #
        # if bPrint: print3( 'iHalfLen:', iHalfLen )
        #
        sName1, sName2 = sName1.lower(), sName2.lower()
        #
        #print3( 'iLen1, iLen2, iHalfLen:', iLen1, iLen2, iHalfLen )
        #print3( 'sName1, sName2:', sName1, sName2 )
        #
        if not (    sName1[ : iHalfLen   ] == sName2[ : iHalfLen   ] or
                    sName1[  -iHalfLen : ] == sName2[  -iHalfLen : ] ):
            #
            # if bPrint: print3( 'halfs do not match' )
            raise Finished
            #
        #
        sCommon = getBegAndEndIfInOrder( sName1, sName2 )
        #
        # if bPrint: print3( 'sCommon:', sCommon )
        #
        # if bPrint: print3( 'min( iLen1, iLen2 ):', min( iLen1, iLen2 )
        #
        # if bPrint: print3( 'len( sCommon ):', len( sCommon ) )
        #
        if min( iLen1, iLen2 ) - len( sCommon ) > 1:
            # if bPrint: print3( 'not enough in common with shorter' )
            raise Finished
            #
        #
        # if bPrint: print3( 'min( iLen1, iLen2 ) - len( sCommon ):', min( iLen1, iLen2 ) - len( sCommon ) )
        #
        # if bPrint: print3( 'max( iLen1, iLen2 ):', max( iLen1, iLen2 ) )
        #
        lLenNames = lZip( ( iLen1, iLen2 ), ( sName1, sName2 ) )
        #
        lLenNames.sort()
        #
        sShort = lLenNames[0][1]
        sLong  = lLenNames[1][1]
        #
        # if bPrint: print3( 'sLong, sShort:', sLong, sShort )
        #
        if max( iLen1, iLen2 ) - len( sCommon ) > 1 and \
                not sLong.startswith( sShort ):
            # if bPrint: print3( 'not enough in common with longer' )
            raise Finished
            #
        # if bPrint: print3( 'max( iLen1, iLen2 ) - len( sCommon ):', max( iLen1, iLen2 ) - len( sCommon ) )
        #
    except Finished:
        #
        bNameMisSpelled = False
        #
    #
    return bNameMisSpelled


def getFirstMiddleLast( s ):
    #
    lParts = s.split()
    #
    sFirst, sMiddle, sLast = '', '', ''
    #
    if lParts:
        #
        sFirst = lParts[  0 ]
        sLast  = lParts[ -1 ]
        #
        if len( lParts ) > 2: sMiddle = ' '.join( lParts[ 1 : -1 ] )
        #
    #
    return sFirst, sMiddle, sLast


def _getInitialOffFront( s ):
    #
    while s and s.strip()[ 1 : 3 ] == '. ':
        #
        s = s.strip()[ 2 : ]
        #
    return s.strip()


def getLastGoBySkipNick( s ):
    #
    sFirst, sMiddle, sLast = getFirstMiddleLast( s )
    #
    sGoBy = sFirst
    #
    if len( sFirst ) == 5 and sFirst[1] == '.' and sFirst[4] == '.':
        #
        pass
        #
    elif len( sFirst ) == 2 and sFirst.endswith( '.' ):
        #
        if sMiddle:
            sGoBy = _getInitialOffFront( sMiddle )
        else:
            sGoBy = _getInitialOffFront( sLast )
        #
    #
    return sLast, sGoBy


def getGoBySkipNick( s ):
    #
    sLast, sGoBy = getLastGoBySkipNick( s )
    #
    return sGoBy



def getGoByNickOK( s ):
    #
    from String.Get import getTextWithin
    #
    sGoBy = getGoBySkipNick( s )
    #
    if '"' in s:
        #
        sGoByMaybe = getTextWithin( s, '"','"' )
        #
        if sGoByMaybe: sGoBy = sGoByMaybe
    #
    return sGoBy


def getLastFirstTitle( s ):
    #
    from Iter.AllVers       import iFilter, tMap
    from String.Split       import getWhiteCleaned
    from String.Get         import getStripped
    from String.Names       import getGoBySkipNick
    #
    s = getWhiteCleaned( s.replace( '.', '. ' ) )
    #
    # print3( s )
    tParts = tMap( getStripped, s.split( ',' ) )
    #
    #print3( tParts )
    sFirst = ' '.join( tParts[ 1 : ] )
    sLast  = tParts[  0 ]
    sTitle = ''
    #
    if len( tParts ) == 3:
        sTitle = tParts[ 1 ]
        sFirst = ' '.join( tParts[ 2 : ] )
    #
    if sLast.endswith( ' Jr.' ):
        #
        sTitle = ', '.join( iFilter( bool, ( sTitle, 'Jr.' ) ) )
        sLast  = sLast[ : -4 ].strip()
        #
    #
    if len( sFirst ) == 5 and sFirst[1] == '.' and sFirst[4] == '.':
        #
        pass
        #
    else:
        #
        sFirst = getGoBySkipNick( sFirst )
        #
    #
    return sLast, sFirst, sTitle



if __name__ == "__main__":
    #
    lProblems = []
    #
    from Utils.Result   import sayTestResult
    #
    #print3( isNickName( 'mike',   'Michael' )
    tLastGoBy = getLastGoBySkipNick( 'Stephanie Herseth Sandlin' )
    #
    if tLastGoBy != ('Sandlin', 'Stephanie'):
    #
    #
        lProblems.append( 'getLastGoBySkipNick()' )
    #
    #
    if    ( not isNickName( 'bill', 'william'   ) or
        not isNickName( 'jill', 'julie'     ) or
        not isNickName( 'susan', 'sue'      ) or
        not isNickName( 'sue',  'susan'     ) or
        not isNickName( 'rick', 'dick'      ) or
        not isNickName( 'rick', 'richard'   ) or
        not isNickName( 'ed',   'edward'    ) or
        not isNickName( 'tina', 'valentina' ) or
        not isNickName( 'woody','woodrow'   ) or
        not isNickName( 'lena', 'lynn'      ) or
        not isNickName( 'lynn', 'kathleen'  ) or
        not isNickName( 'steven', 'stephen' ) or
        not isNickName( 'carol', 'carolyn'  ) or
        not isNickName( 'julie', 'julia'    ) or
        not isNickName( 'kristi', 'Kristine') or
        not isNickName( 'mike',   'Michael' ) or
        isNickName( 'bill', 'ralph'     ) or
        isNickName( 'chrstine', 'christine' ) ):
    #
        lProblems.append( 'isNickName()' )
    #
    #
    if not isNameMisSpelled( 'kevin', 'kevn' ):
        #
        lProblems.append( 'isNameMisSpelled() kevin/kevn' )
        #
    #
    if not isNameMisSpelled( 'Kimberley', 'Kimberly' ):
    #
        lProblems.append( 'isNameMisSpelled() Kimberley/Kimberly' )
    #
    if not isNameMisSpelled( 'Natalie', 'Nathalie' ):
    #
        lProblems.append( 'isNameMisSpelled() Natalie, Nathalie' )
    #
    if not isNameMisSpelled( 'Panayiotis', 'Panayotis' ):
    #
        lProblems.append( 'isNameMisSpelled() Panayiotis, Panayotis' )
    #
    if not isNameMisSpelled( 'Chrstine', 'Christine' ):
    #
        lProblems.append( 'isNameMisSpelled() Chrstine, Christine' )
    #
    if not isNameMisSpelled( 'Tomas', 'Tom' ):
    #
        lProblems.append( 'isNameMisSpelled() Tomas/Tom' )
    #
    if not isNameMisSpelled( 'Alison', 'Allison' ):
    #
        lProblems.append( 'isNameMisSpelled() Alison/Allison' )
    #
    if not isNameMisSpelled( 'Nanay', 'Nancy' ):
    #
        lProblems.append( 'isNameMisSpelled() Nanay/Nancy' )
    #
    if not isNameMisSpelled( 'Chistopher', 'Christopher' ):
    #
        lProblems.append( 'isNameMisSpelled() Chistopher/Christopher' )
    #
    if not isNameMisSpelled( 'Ann', 'Anne' ):
    #
        lProblems.append( 'isNameMisSpelled() Ann/Anne' )
    #
    if not isNameMisSpelled( 'Carel', 'Carol' ):
    #
        lProblems.append( 'isNameMisSpelled() Carol/Carel' )
    #
    if not isNameMisSpelled( 'Eric', 'Erik' ):
    #
        lProblems.append( 'isNameMisSpelled() Eric/Erik' )
    #
    if not isNameMisSpelled( 'Jeegar', 'Jeeger' ):
    #
        lProblems.append( 'isNameMisSpelled() Jeegar/Jeeger' )
    #
    if not isNameMisSpelled( 'Georgianna', 'Georgiana' ):
    #
        lProblems.append( 'isNameMisSpelled() Georgianna/Georgiana' )
    #
    #
    if not isNameMisSpelled( 'Jacqueline', 'Jaqueline' ):
    #
        lProblems.append( 'isNameMisSpelled() Jacqueline/Jaqueline' )
    #
    if not isNameMisSpelled( 'Josep', 'Joseph' ):
    #
        lProblems.append( 'isNameMisSpelled() Josep/Joseph' )
    #
    if not isNameMisSpelled( 'Beverley', 'Beverly' ):
    #
        lProblems.append( 'isNameMisSpelled() Beverley/Beverly' )
    #
    if not isNameMisSpelled( 'Heid', 'Heidi' ):
    #
        lProblems.append( 'isNameMisSpelled() Heid/Heidi' )
    #
    if not isNameMisSpelled( 'Christine', 'Christina' ):
    #
        lProblems.append( 'isNameMisSpelled() Christine/Christina' )
    #
    if not isNameMisSpelled( 'Kimberley', 'Kimberly' ):
    #
        lProblems.append( 'isNameMisSpelled() Kimberley/Kimberly' )
    #
    if not isNameMisSpelled( 'Paul', 'Paulo' ):
    #
        lProblems.append( 'isNameMisSpelled() Paul/Paulo' )
    #
    if not isNameMisSpelled( 'Dawn', 'Daun' ):
    #
        lProblems.append( 'isNameMisSpelled() Dawn/Daun' )
    #
    if not isNameMisSpelled( 'Takao', 'Taka' ):
    #
        lProblems.append( 'isNameMisSpelled() Takao/Taka' )
    #
    if not isNameMisSpelled( 'Paul', 'Paulk' ):
    #
        lProblems.append( 'isNameMisSpelled() Paul/Paulk' )
    #
    #
    #
    #
    if     isNameMisSpelled( 'John', 'Joel' ):
    #
        lProblems.append( 'isNameMisSpelled() John/Joel' )
    #
    if     isNameMisSpelled( 'Kelsey', 'Kelly' ):
    #
        lProblems.append( 'isNameMisSpelled() Kelsey/Kelly' )
    #
    if     isNameMisSpelled( 'Mark', 'Mary' ):
    #
        lProblems.append( 'isNameMisSpelled() Mark/Mary' )
    #
    if     isNameMisSpelled( 'Maria', 'Maya' ):
    #
        lProblems.append( 'isNameMisSpelled() Maria/Maya' )
    #
    if     isNameMisSpelled( 'John', 'Joan' ):
    #
        lProblems.append( 'isNameMisSpelled() John/Joan' )
    #
    if     isNameMisSpelled( 'Jan', 'Ryan' ):
    #
        lProblems.append( 'isNameMisSpelled() Jan/Ryan' )
    #
    #
    if getFirstMiddleLast(
        'William Jefferson Clinton' ) != \
        ( 'William', 'Jefferson', 'Clinton' ):
    #
        lProblems.append( 'getFirstMiddleLast()' )
    #
    #
    if getGoBySkipNick( 'L. Ron Hubbard' ) != 'Ron':
    #
        lProblems.append( 'getGoBySkipNick()' )
    #
    #
    s = 'Paul "Tex" Yearout'
    #
    if getGoBySkipNick( s ) != 'Paul':
    #
        lProblems.append( 'getGoBySkipNick() got nick' )
    #
    #
    if getGoByNickOK( s ) != 'Tex':
    #
        lProblems.append( 'getGoByNickOK() got nick' )
    #
    #
    s = 'C. W. Bill Young'
    #
    if getGoBySkipNick( s ) != 'Bill':
    #
        lProblems.append( 'getGoBySkipNick() two initials' )
    #
    #
    if getLastGoBySkipNick( s ) != ( 'Young', 'Bill' ):
    #
        lProblems.append( 'getLastGoBySkipNick() two initials' )
    #
    #
    if getLastFirstTitle(
        'Kratovil, Jr., Frank M.' ) != ( 'Kratovil', 'Frank', 'Jr.' ):
    #
        print3( getLastFirstTitle( 'Kratovil, Jr., Frank M.' ) )
        lProblems.append( 'getLastFirstTitle() Kratovil, Jr., Frank M.' )
    #
    #
    #if 0:
    if getLastFirstTitle( 'Kagen, Steve' ) != ( 'Kagen', 'Steve', '' ):
        #
        lProblems.append( 'getLastFirstTitle() Kagen, Steve' )
        #
    #
    if getLastFirstTitle( 'Pascrell Jr., Bill' ) != ( 'Pascrell', 'Bill', 'Jr.' ):
    #
        print3( getLastFirstTitle( 'Pascrell Jr., Bill' ) )
        lProblems.append( 'getLastFirstTitle() Pascrell Jr., Bill' )
    #
    #
    if getLastFirstTitle( 'Barrett, J.Gresham' ) != ( 'Barrett', 'Gresham', '' ):
    #
        print3( getLastFirstTitle( 'Barrett, J.Gresham' ) )
        lProblems.append( 'getLastFirstTitle() Barrett, J.Gresham' )
    #
    #
    if getLastFirstTitle( 'Butterfield, G.K.' ) != ( 'Butterfield', 'G. K.', '' ):
    #
        print3( getLastFirstTitle( 'Butterfield, G.K.' ) )
        lProblems.append( 'getLastFirstTitle() Butterfield, G.K.' )
    #
    # Patrica and Patrick Forster
    #
    if isMensName( "Patricia" ):
        #
        lProblems.append( 'isMensName( "Patricia" )' )
        #
    #
    if isWomensName( "Patrick" ):
        #
        lProblems.append( 'isWomensName( "Patrick" )' )
        #
    #
    if isNameMisSpelled( "Patricia", "Patrick" ):
        #
        lProblems.append( 'isNameMisSpelled( "Patricia", "Patrick" )' )
        #
    #
    if isNickName( "Patricia", "Patrick" ):
        #
        lProblems.append( 'isNickName( "Patricia", "Patrick" )' )
        #
    #
    #
    #
    sayTestResult( lProblems )