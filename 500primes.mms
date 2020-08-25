% Example program ... Table of primes
L	IS	500		% The number of primes to find
t	IS	$255		% Temporary storage

r	GREG	0		% Remainder          reg $254 (last available)
q	GREG	0		% Quotient               $253
pk	GREG	0		% Value of  PRIME[k]     $252
n	GREG	0		% Prime candidate,       $251
k	GREG    0               % Index of test prime    $250
j	GREG	0		% n=PRIME[j]             $249
off	GREG 	0		% off=2j (2 bytes/WYDE)  $248
NP	GREG	0		% number of primes to find $247
NB	GREG	0		% number of bytes (2*NP because wydes) $246

	LOC	Data_Segment	% move the current location to beginning of data
data	GREG	@		% hold on to address of data segment: register $245
PRIME1	WYDE	2		% Populate the first prime (2) into the first two bytes
				% (1 wyde) of data segment

	LOC	PRIME1+2*L	% Set current location @ after where 500 primes will write 
ptop	GREG	@		% Data_Seg+1000 into register $244
BUF	OCTA	0		% Right after last prime, this is the address of memory
				% that will be used for converting each number into decimal

	LOC	#100		
Main	SET	NP,L		% 500 primes to find
	MULU	NB,NP,2		% 1000 bytes will be filled with 500 wyde numbers
	SET	n,3		% P1. Start table. n <- 3 (we already put 2 in the data)
	SET	j,1		% init j <- 1; which prime is the current n
	MULU	off,j,2		% off <- 2*j (2 bytes/WYDE)
2H	STWU	n,data,off	% P2. n is prime. PRIME[j+1] <- n (first time just write 3)
	INCL	j,1		% j <- j+1
	MULU	off,j,2		% off <- 2*j
3H	CMP	t,NP,j		% t <- NP<>j?
	BZ	t,2F		% P3. 500 found? (L-j==0)?
4H	INCL	n,2		% P4. Advance n (by 2 to stay on odds)
5H	SET	k,2		% P5. First check div/3 (don't need to check /2, we skipped evens)
6H	LDW	pk,data,k	% P6. Fetch kth prime from data into pk register
	DIV	q,n,pk		% q <- floor(n/pk), rR <- remainder
	GET	r,rR		% fetch remainder out of special register into general register r
	BZ	r,4B		% To P4 if r==0 (if n/pk has R0, n is not prime. NEXT)
7H	CMP	t,q,pk		% P7. pk large? t <- q<>pk
	BNP	t,2B		% To P2 if q <= pk (because pk got above sqrt(n) --> n is prime)
8H	INCL	k,2		% P8. Advance k. k <- k+1
	JMP	6B		% To P6, try dividing next data prime pk into n
	GREG	@		% Base address
Title	BYTE	"First Five Hundred Primes"
NewLn	BYTE	#a,0		% Newline and string terminator
Blanks	BYTE	"   ",0		% String of three blanks
2H	LDA	t,Title		% P9. Fill t register with address of title.
	TRAP	0,Fputs,StdOut	% Print whatever t points to?
	SET	j,0		% Count # of primes printed
	NEG	off,2		% Initialize offset (-2 so first +2-->0)
3H	ADD	off,off,2	% P10. Print line
	LDA	t,Blanks	% Output "   " (3 blanks)
	TRAP	0,Fputs,StdOut
2H	LDWU	pk,data,off	% pk <- prime to be printed
0H	GREG	#2030303030000000	% " 0000",0,0,0
	STOU	0B,BUF		% Write " 0000" into buffer
	LDA	t,BUF+4		% t <- position of units digit
1H	DIV	pk,pk,10	% pk <- floor(pk/10), divide by 10 so 1's digit is remainder
	GET	r,rR		% fetch remainder out of special register
	INCL	r,'0'		% numerical value 0-9 --> ASCII digit 50-59
	STBU	r,t,0		% Store ASCII character r in the buffer where t is pointing
	SUB	t,t,1		% Move t one byte/ascii character to the left
	PBNZ	pk,1B		% If pk still has a quotient, repeat on remaining digits
	LDA	t,BUF		% Output " " and four digits
	TRAP	0,Fputs,StdOut	
	INCL	j,1		% Count one more prime printed
	INCL	off,2*L/10	% Advance by 50 wydes
	CMP	t,off,NB	% t <- off<>NB (is offset past the end?)
	PBN	t,2B		% if not, do another number on this line, else continue on to...
	LDA	t,NewLn		% ...Output a newline
	TRAP	0,Fputs,StdOut	
	SUBU	off,off,NB	% Back the offset up to beginning of this row
	CMP	t,j,NP		% P11. 500 printed?
	PBNZ	t,3B		% To P10 if not done
	TRAP	0,Halt,0
	
