#! /usr/bin/perl
do 'bigint.pl';sub e{return$a if$_[0]<2;$r=e(bdiv($_[0],2));$r=bmod(bmul($r,$r),
$n);$r=bmod($_[0],2)>0?bmod(bmul($r,$a),$n):$r;}($a,$e,$n)=@ARGV;print e($e)


    ##########################################################################
    ####################        Expansive version       ######################
    ##########################################################################

    # This is more simplistic than RSA in 5 lines of pure Perl from
    #    http://www.cypherspace.org/rsa/pureperl.html,
    # or the famous RSA .sig in 3 lines of Perl (and dc) from
    #    http://www.cypherspace.org/adam/rsa/rsa-details.html.

    # Those implementations spend most of their energy chunking the input into
    # blocks, and converting between hex/binary/decimal/ASCII. It still requires
    # the user to come up with RSA private/public keys and modulus, which is
    # more core to the meaning of RSA than those data-shuffling concerns.

    # A reminder of fundamentals. The user starts with 2 primes p and q, and an
    # encryption exponent E. Semiprime modulus N=pq and E are public. Given p,
    # q, and E, Euclid's algorithm can be used to find a decryption exponent d
    # such that Ed=1 mod (p-1)*(q-1). Then, for any numerical message m,
    # ciphertext can be encrypted as c=m^E mod N, and then the decryption
    # c^d = m mod N again. (Proof that (m^E)^d=m mod N is left to the reader.)
    # As long as the original message m<N, nothing is lost via modulus in the
    # roundtrip.
    
    # Since the assumption is already made that the user can provide an
    # encryption/decryption exponent/key and modulus, this version also makes
    # the samller assumption that the user can navigate between interpreting the
    # message bitstring as either ASCII or an integer, and block their data
    # appropriately so that each block is represented by an integer m<N. This
    # script can then be used to encrypt/decrypt each block integer.

    # Example: message RSA=18,19,01  encryption exponent=683821
    #    modulus=382104874381        decryption exponent=378760340773
    # > rsanum.pl 181901       683821       382104874381 --> prints +360352680879
    # > rsanum.pl 360352680879 378760340773 382104874381 --> prints +181901

    # Without further ado, here's the uncompacted version of the script.
    # The 2-line version is this minus comments and whitespace.

    #-------------------------------rsanum.pl-----------------------------------

    # # Import bigint functions bmul, bmod, bdiv
    # do 'bigint.pl';
    
    # # Modulus Exponentiation function e($k) = $a ^ $k mod $n
    # sub e{                         # Exponent k=$_[0]
    #   return$a if$_[0]<2;          # Recursion bottoms out at a^1
    #   $r=e(bdiv($_[0],2));         # a^(floor(k/2)) mod n
    #   $r=bmod(bmul($r,$r),$n);     # The answer if k is even
    #   $r=bmod($_[0],2)>0           # If k is odd,
    #     ?bmod(bmul($r,$a),$n)      #  we need one more a
    #     :$r;
    # }

    # # Get the base, exponent, and modulus from the command-line. 
    # ($a,$e,$n)=@ARGV;

    # # Base and modulus are available to the function in global variables
    # # $a,$n. The function only needs to be passed the exponent.
    # print e($e)
