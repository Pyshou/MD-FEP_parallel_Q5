#!/usr/bin/perl -w
# Perl script to prepare PDB file for docking
# Version 2, Nov 2009

use strict;

if ($#ARGV  != 1) {
	print "prepare_pdbfile.pl <PDB> <RES_CHANGE>\n";
	print "\nPurpose: Prepare PDB file for rundockblaster\n";
	print "<PDB> is the input PDB file.\n";
	print "<RES_CHANGE> is a text file that modifies residue names. Format: Residue_number New_residue_name\n";
	print "Prints rec.pdb as output file.\n\n";
	exit;
}
# Variables. Needs cleanup.
# index
my $i=1;
my $j=0;
my $k=0;
# Hash 
my $residue;
my $state;
# PDB format
my $atomnumber;
my $atomtype;
my $resnumber;
my $restype;
my $x;
my $y;
my $z;
# Disulfide bridges
my $ss=0;
my @x_cys;
my @y_cys;
my @z_cys;
my $distance;
# Other
my $prev_res_number=0;
my $q=0;
my $gap=0;
my @residue;

# Files
open (PDB,$ARGV[0]) || die "can't open pdb file\n";
open (IONIZE,$ARGV[1]) || die "can't open ionization file\n";
open (PDBOUT,">rec.pdb") || die "can't open pdbout file\n";

# Read changes in residue names
my %hash = ();
while(<IONIZE>) {
    ($residue,$state) = split(/\s/);
    chomp($state);
    $hash{$residue} = $state;
}

print "\nResidue changes:\n";
while(<PDB>) {
    if(/^GAP/){
	printf PDBOUT "GAP\n";
    }
    if(/^ATOM/ or /^HETATM/){
	# Extract data, format from pdb homepage. Safer than regexp.
	$atomnumber = substr $_,6,5;
	$atomtype = substr $_,12,4;
	$restype = substr $_,17,3;
	$resnumber = substr $_,22,4;
	$x = substr $_,30,8;
	$y = substr $_,38,8;
	$z = substr $_,46,8;
        
	# Remove spaces from residue number
	$resnumber =~ s/\s+//;         

	    # Look for disulfide bridges
	    if( ($restype eq 'CYS') && $atomtype eq ' SG ' ) {
		$residue[$i]=$resnumber;
		$x_cys[$i]=$x;
		$y_cys[$i]=$y;
		$z_cys[$i]=$z;
		$i++;	  
	    }
            
	    if( $atomtype eq ' CA ' ) {
		if( $prev_res_number+1 != $resnumber ) {
		    $gap++;
		    print "Missing residues between $prev_res_number to $resnumber\n";
		}
		$prev_res_number = $resnumber;
	    }

	    # Look for ionizable residues and disulfide bridges
	    if( $hash{$resnumber} ) {
		if( $atomtype eq ' CA ' ) {
		    print "$resnumber was $restype and is now $hash{$resnumber}.\n";
		    if($restype eq 'CYS'){$ss++};
		}
		if( $restype eq 'POP' or $restype eq 'HOH' ){ 
		}else{
			$restype = $hash{$resnumber};
		}
	    }

	    if( ($restype eq 'HIS') && ($atomtype eq ' CA ')){print "WARNING: $restype $resnumber is not set in <RES_CHANGE>\n";}
   
	    # Calculate charge
	    if( ($atomtype eq ' CA ') && (($restype eq 'ASP') || ($restype eq 'GLU' )) ) {$q--;}
	    if( ($atomtype eq ' CA ') && (($restype eq 'HIP') || ($restype eq 'LYS') || ($restype eq 'ARG')) ) {$q++;}
	    # Print PDB file again
	    printf PDBOUT "ATOM  $atomnumber $atomtype $restype  %4d    $x$y$z\n",$resnumber;
    }
}

# Check disulfide bridges
print "\nDisulfide bridges identified (SD-SD < 2.5 Ang):\n";
for($j=1;$j<$i;$j++){
    for($k=$j+1;$k<$i;$k++){
	$distance = ( ($x_cys[$j]-$x_cys[$k])**2 + ($y_cys[$j]-$y_cys[$k])**2 + ($z_cys[$j]-$z_cys[$k])**2 )**(0.5);
	if( $distance < 2.5 ) {
        printf "S-S pair: $residue[$j], $residue[$k]: distance = %3.2f Ang.\n",$distance;
	}
    }
}
$ss=$ss/2;
print "Number of disulfide bridges created in <RES_CHANGE>: $ss\n";
# Print total charge
print "\nTotal charge is: $q\n";
print "Number of gaps are: $gap\n";





