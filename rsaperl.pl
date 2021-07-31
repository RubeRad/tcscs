#!/usr/bin/perl -s

# RSA in 5 lines of 'pure perl', copied and expanded from
# http://www.cypherspace.org/rsa/pureperl.html
# Deleting all the comments and debug ($g) sections below,
# and eliminating whitespace, packs all the perl into just 5 lines
# (plus shebang = 6), thusly:
#
# #!/usr/local/bin/perl -s
# do 'bigint.pl';($_,$n)=@ARGV;s/^.(..)*$/0$&/;($k=unpack('B*',pack('H*',$_)))=~
# s/^0*//;$x=0;$z=$n=~s/./$x=&badd(&bmul($x,16),hex$&)/ge;while(read(STDIN,$_,$w
# =((2*$d-1+$z)&~1)/2)){$r=1;$_=substr($_."\0"x$w,$c=0,$w);s/.|\n/$c=&badd(&bmul
# ($c,256),ord$&)/ge;$_=$k;s/./$r=&bmod(&bmul($r,$r),$x),$&?$r=&bmod(&bmul($r,$c
# ),$x):0,""/ge;($r,$t)=&bdiv($r,256),$_=pack(C,$t).$_ while$w--+1-2*$d;print}

# See also http://www.cypherspace.org/adam/rsa/rsa-details.html
# for some example keys (as hexadecimals).
# Here is an example command for a roundtrip test (note echo -n omits newline):
# echo -n TCS | rsaperl.pl 10001 1967cb529 | rsaperl.pl -d ac363601 1967cb529
#######  ^msg^              ^e^     ^n^                       ^d^      ^n^
#
# Or to do it in multiple steps with -g triggering lots of STDERR printing:
########## encrypt message TCS, write into binary file
# echo -n TCS | rsaperl.pl -g 10001 1967cb529 > ciphertxt.bin
########## doublecheck ciphertext as hex matches what rsaperl.pl -g just said
# od -h --endian big ciphertxt.bin
########## decrypt ciphertext, print to screen
# cat ciphertxt.bin | rsaperl.pl -g -d ac363601 1967cb529

#######################################################################
## Below this point is the original script
## Except every occurrence of "$g" indicates added debugging
## STDERR printouts triggered by commandline switch -g
#######################################################################

#Shebang: full path for perl (may need to be changed on local system).
#       -s switch enables simple switch processing, which sets $d to 1
#        if "-d" is on the command line (it also removes the switch from ARGV).
#        if  -d  is not given $d is undefined (acts like 0)

#Load the standard bigint library.  Unlike require, do will not complain if
#the library is not present.  The space between do and the quotes is required
#(ha ha) in 4.036.
#Provides bigint arithmetic functions badd, bmul, bmod, bdiv, etc.
do 'bigint.pl';

#Set $_ to the key (e or d), and $n to n.
($_,$n)=@ARGV;

#For $_ (the key), if there are an odd number of characters,
#then add a leading zero.  This is needed for the pack below.
s/^.(..)*$/0$&/;

#pack hex digits to 8-bit binary, then unpack to ASCII binary, store in $k
#The outer parens are needed for precedence.
($k=unpack('B*',pack('H*',$_)))
#remove any leading zeros from $k
        =~s/^0*//;

if ($g) { # activate debug section with -g
    if ($d) {
        print STDERR "\nBeginning DECRYPTION\n";
    } else {
        print STDERR "\nBeginning ENCRYPTION\n";
    }
    print STDERR "Hex exponent $_ expands to binary $k\n";
}

#Extract $x (bigint version of $n).
#   $x=0;    Initialize bigint (needed?)
#   $z=      result of search/replace--the number of characters
#            (hex digits) in $n
#   $n=~s/./      for each character in $n...
#      $x=&badd(&bmul($x,16),hex$&)  ...mult old total and add digit ($&)
#   /ge;

if ($g) {
    $nhex = $n;
    print STDERR "\nConverting modulus n=0x$nhex to decimal:\n";
    $ndec = 0;
    print STDERR "Start with 0\n";
    while ($nhex =~ /(.)/sg) { # for each hex digit in the character string $nhex
        $hexdig = $1;
        $oldndec = $ndec;         # for printing
        $ndec = bmul($ndec,16);
        $ndec = badd($ndec, hex($hexdig));
        print STDERR "$oldndec * 16 + 0x$hexdig = $ndec\n";
    }
    print STDERR "Final n as big decimal: $ndec\n";
}

$x=0;
$z=$n=~s/./$x=&badd(&bmul($x,16),hex$&)/ge;

print STDERR "Check n expansion:      $n\n" if $g;
print STDERR "Check z index:          $z\n" if $g;
print STDERR "Check n as big decimal: $x\n" if $g;



#Reading from standard input into $_ until exhausted.
while(read(STDIN,$_
#...$w characters of STDIN ($w set for later use).
#...don't completely understand formula and reasoning yet.
#This might be able to be shortened, but be careful w/ precendence!
,$w=((2*$d-1+$z)&~1)/2))
{
    if ($g) {
        $block = $_;
        if ($d) { # decrypting, block  is not printable
            print STDERR "\nBlock length: $w; binary ciphertext block not printable\n" if $g;
        } else {
            print STDERR "\nBlock length: $w; block: '$block'\n" if $g;
        }
    }
    
#result of calculations (output)
    $r=1;
#Make $_ contain trailing NUL/zero characters up to $w total length.
#The $_ string is only changed when encrypting and the final block is short.
#we save a couple chars by set $c clear/cypher (input) here.
    $_=substr($_."\0"x$w,$c=0,$w);

#Set the clear/cypher text bigint.
#   s/.|\n/     for each character in $_ (need .|\n for 8-bit match)...
#      $c=&badd(&bmul($c,256),ord$&)   ...mult old total, add unsigned char.
#   /ge;

    if ($g) {
        if ($d) { # decrypting, block is not printable
            print STDERR "Converting block to integer value\n";
        } else {
            print STDERR "Converting block '$block' to integer value\n";
        }
        $bdec = 0;
        print STDERR "Start with 0\n";
        while (/(.)/sg) { # for each ASCII character in the string $_
            $asc = $1; # as an ascii character (maybe not printable)
            $oldbdec = $bdec;
            $bdec = bmul($bdec, 256);
            $ord = ord($asc); # decimal value (order/ordinal) of ascii char
            $bdec = badd($bdec, $ord);
            if ($d) { # decrypting
                printf STDERR "HEX %x = DEC %d: $oldbdec * 256 + $ord = $bdec\n", $ord, $ord;
            } else {
                printf STDERR "ASCII $asc = DEC %d: $oldbdec * 256 + $ord = $bdec\n", $ord;
            }
        }
        print STDERR "Final block as decimal: $bdec\n";
    }
    
    s/.|\n/$c=&badd(&bmul($c,256),ord$&)/ge;

    if ($g) {
        print STDERR "Check block as decimal: $c\n";
        if ($d) {
            print STDERR "This is the ciphertext block converted to an integer\n";
        } else {
            print STDERR "This is the message block '$block' converted to an integer\n";
        }
    }


    if ($g) {
        print STDERR "\nUsing repeated squaring to compute block $bdec raised to the binary exponent $k mod $ndec\n";
        $rdec = 1;
        print STDERR "Start with 1\n";
        $_ = "$k";
        while (/(.)/sg) { # for each bit in binary exponent $k
            $kbit = $1;
            print STDERR "Next square $rdec * $rdec mod $ndec --> ";
            $rdec = bmod(bmul($rdec,$rdec), $ndec);
            print STDERR "$rdec\n";
            if ($kbit) {
                print STDERR "Bit is $kbit: $rdec * $bdec mod $ndec --> ";
                $rdec = bmod(bmul($rdec,$bdec), $ndec);
                print STDERR "$rdec\n";
            }
            #else {
            #   print STDERR "Bit is $kbit: do nothing\n";
            #}
        }
        print STDERR "Final exponentiation result: $rdec\n";
    }

    
#Set $_ to copy of $k (key--ascii binary) for big calculation below
    $_=$k;
#Do that RSA thang:
#   s/./
#      $r=&bmod(&bmul($r,$r),$x),
#      $&?
#          $r=&bmod(&bmul($r,$c),$x)
#        :0
#      ,""
#   /ge;

    
#Note: this empties $_, saving a few chars below.
    s/./$r=&bmod(&bmul($r,$r),$x),$&?$r=&bmod(&bmul($r,$c),$x):0,""/ge;

    if ($g) {
        print STDERR "Check exponentiation result: $r\n";
        if ($d) { # decrypting (original block is not printable)
            print STDERR "That is the final decrypted block as an integer\n";
        } else {  # encrypting (original block is printable)
            print STDERR "That is the final encrypted block '$block' as an integer\n";
        }
    }


    if ($g) {
        print STDERR "\nConvert integer to bytes for output\n";
        print STDERR "$rdec converts to:\n";
        $wcopy = $w;
        @byteary = ();
        @asciary = ();
        @charary = ();
        @hexxary = ();
        while ($wcopy--+1-2*$d) {
            $lastbyte = bmod($rdec, 256);  # grab last byte as decimal value
            $rdec = bdiv($rdec, 256);      # shift off last byte
            $lastchar = chr($lastbyte);    # as printable(?) text character
            # convert byte to binary (there must be a simpler way lol)
            $binary  = '';
            $binary .= ($byte & 128 ? '1' : 0);
            $binary .= ($byte &  64 ? '1' : 0);
            $binary .= ($byte &  32 ? '1' : 0);
            $binary .= ($byte &  16 ? '1' : 0);
            $binary .= ($byte &   8 ? '1' : 0);
            $binary .= ($byte &   4 ? '1' : 0);
            $binary .= ($byte &   2 ? '1' : 0);
            $binary .= ($byte &   1 ? '1' : 0); # as binary text string
            unshift @byteary, $binary;
            unshift @asciary, sprintf "%-8d", $lastbyte;
            unshift @charary, sprintf "%-8s", $lastchar;
            unshift @hexxary, sprintf "%-8x", $lastbyte;
        }
        if ($d) {
            print STDERR (join ' ', 'binary: ',    @byteary, "\n");
            print STDERR (join ' ', 'decimal:   ', @asciary, "\n");
            print STDERR (join ' ', 'ASCII:     ', @charary, "\n");
        } else {
            print STDERR (join ' ', 'binary: ',    @byteary, "\n");
            print STDERR (join ' ', 'hex:       ', @hexxary, "\n");
        }
    }
    
    ($r,$t)=&bdiv($r,256),$_=pack(C,$t).$_ while$w--+1-2*$d;

    $divline = '='x20;
    print "\n\nDecrypted plaintext is:\n$divline\n" if $g && $d;
    
    print;  # print the encrypted ciphertext / decrypted plaintext

    print "\n$divline\n" if $g && $d;
}
