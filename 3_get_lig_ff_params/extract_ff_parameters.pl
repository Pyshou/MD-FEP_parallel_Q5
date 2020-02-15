#!/usr/bin/perl 
# By Jens Carlsson, 2011

# Input files
open(FF, $ARGV[0]) or die "can't openfile: $!\n"; 
# Library file
open(LIB, ">LIG.lib") or die "can't openfile: $!\n"; #  .lib
# parameter files
open(NBON,">NBON.prm") or die "can't openfile: $!\n"; 
open(BOND,">BOND.prm") or die "can't openfile: $!\n";  
open(THET,">THET.prm") or die "can't openfile: $!\n";   
open(PHI,">PHI.prm") or die "can't openfile: $!\n"; 
open(IPHI,">IPHI.prm") or die "can't openfile: $!\n"; 

open(PRM, ">PRM") or die "can't openfile: $!\n"; #  .lib

# Hash for atoms types to masses. Add new atoms below.
%atomtype2mass = (
	# Carbon
        CA => '12.01',
	CQ => '12.01',
	CS => '12.01',
	CT => '12.01',
	CW => '12.01',
	C5 => '12.01',
	# Hydrogen
	H3 => '1.01',
	HA => '1.01',
	HC => '1.01',
	HO => '1.01',
	'H ' => '1.01',
	# Nitrogen
	N2 => '14.01',
	NA => '14.01',
	NC => '14.01',
	NP => '14.01',
	# Oxygen
	OH => '16.00',
	OS => '16.00',
);

$TORSION = "PHI";
$nt=1;

# Print residue name
print LIB "{$ARGV[0]}\n";
print LIB "[info]\n";
print LIB "SYBYLtype  RESIDUE     !SYBYL substructure type\n";

# Extract bonded parameters
while(<FF>) 
{
	# SECTION
	if(/NBON/){
		print "\n ** NONBONDED ** \n";
		print LIB "\n[atoms]\n";
		print NBON "\n! NONBONDED LIG PARAMETERS \n";
	}

	if(/^PHI/){
                $SECTION = 'PHI';
                print PHI "\n ! PROPER TORSION LIG PARAMETERS  \n";
	}

        if(/^IPHI/){
                $SECTION = 'IPHI';
                print "\n ** IMPROPER TORSIONS ** \n";
		print LIB "\n[impropers]\n";
		print IPHI "\n ! IMPROPER TORSION LIG PARAMETERS  \n";
	}

        if(/BOND/){
		print "\n ** BONDS **\n";
        	print LIB "\n[bonds]\n";
		print BOND "\n ! BOND LIG PARAMETERS  \n";
        }

	if(/THET/){
		print "\n ** ANGLES ** \n";
		print THET "\n ! ANGLE LIG PARAMETERS  \n";
	}

	# Atom names and atom types
	if(/\s+\d+\s+\d+ \w\s+/){
		$i = substr $_,0,5;
		$atomtype[$i] = substr $_,13,5;
		$atomtype[$i] =~ s/\s+//;
		$atomname[$i] = substr $_,21,4;
		$atomname[$i] =~ s/_//;
		$atomname[$i] =~ s/_//;
		print "$i a$atomtype[$i]a $atomname[$i]\n";
	}

	# NON BONDED
	if(/\s+\d+\.\d{4}\s+\d+\.\d{4}\s+-?\d+\.\d{6}\s+/){
		$i = substr $_,0,5;
		$sigma = substr $_,8,5;
		$epsilon = substr $_,17,6;
		$charge = substr $_,25,9;
                # Remove space
		$i =~ s/\s+//;
		# Print to library file
		print LIB "$i\t$atomname[$i]\tT$atomname[$i]\t$charge\n";
		# Print to parameter file:
		$Avdw1 = sqrt(4*$epsilon*$sigma**12);
 		$Avdw2 = $Avdw1;
 		$Bvdw1 = sqrt(4*$epsilon*$sigma**6);
 		$Avdw3 = $Avdw1/sqrt(2);
 		$Bvdw2o3 = $Bvdw1/sqrt(2);
		$mass = $atomtype2mass{$atomtype[$i]};
		printf NBON "T%s\t%5.2f\t%5.2f\t%5.2f\t%5.2f\t%5.2f\t%5.2f ! Schrodingar atom type $atomtype[$i]\n", $atomname[$i], $Avdw1, $Avdw2, $Bvdw1, $Avdw3, $Bvdw2o3, $mass; 

		# Print to screen
		print "$i $sigma $epsilon $charge\n";
	}

	# BONDS
	if(/^\s+\d+\s+\d+\s+\d+\.\d{3}/){
                $b1 = substr $_,0,5;
                $b2 = substr $_,5,6;
                $fcb = substr $_,11,10;
                $b0 = substr $_,21,7;
		print "$b1$b2$fcb$b0\n";
		# Remove spaces
		$b1 =~ s/\s+//;
		$b2 =~ s/\s+//;
		# Print to LIB file
		print LIB "$atomname[$b1] $atomname[$b2]\n";
		# Print to PRM file
		$Qfcb = 2*$fcb;
		printf BOND "T%s\tT%s\t%5.1f\t%5.3f\t\n", $atomname[$b1],$atomname[$b2],$Qfcb,$b0; 

	}

	# ANGLES
	if(/^\s+\d+\s+\d+\s+\d+\s+\d+\.\d{5}\s+\d+\.\d{5}/){
                $a1 = substr $_,0,5;
                $a2 = substr $_,5,6;
                $a3 = substr $_,11,6;
		$fca = substr $_,17,12;
                $a0 = substr $_,29,11;
		print "$a1$a2$a3$fca$a0\n";
		# Print to PRM file
		$Qfca = 2*$fca;
		printf THET "T%s\tT%s\tT%s\t%5.1f\t%5.3f\t0.000\t0.000\n", $atomname[$a1],$atomname[$a2],$atomname[$a3],$Qfca,$a0; 
        }
	
	# TORSIONS AND IMPROPERS
	if(/^\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\.\d{5}\s+-?\d+\.\d+\s+-?\d+\.\d+/){
 		# TORSIONS
		if($SECTION eq 'PHI'){
                $t_full[$nt] = substr $_,0,23;
		$t1[$nt] = substr $_,0,5;
                $t2[$nt] = substr $_,5,6;
                $t3[$nt] = substr $_,11,6;
                $t4[$nt] = substr $_,17,6;
                $fct[$nt] = substr $_,23,10;
                $phi[$nt] = substr $_,33,5;
                $multi[$nt] = substr $_,38,4;
		print "$t1[$nt]$t2[$nt]$t3[$nt]$t4[$nt]$fct[$nt]$phi[$nt]$multi[$nt]\n";
		# Print to PRM
		$phi[$nt] =~ s/\s+//;
		$multi[$nt] =~ s/\s+//;
		$Qfct[$nt] = $fct[$nt];
		if($phi[$nt] > 0){
			$phi[$nt]=0.0;
		}else{
			$phi[$nt]=180.0;
		}
#		printf PHI "T%s\tT%s\tT%s\tT%s\t%5.3f\t%5.1f\t%5.1f\t1.000\t\n", $atomname[abs($t1[$nt])], $atomname[abs($t2[$nt])], $atomname[abs($t3[$nt])], $atomname[abs($t4[$nt])], $Qfct[$nt], $multi[$nt], $phi[$nt]; 
		$nt++;
		}
		
		# IMPROPERS
	        if($SECTION eq 'IPHI'){
                $i1 = substr $_,0,5;
                $i2 = substr $_,5,6;
                $i3 = substr $_,11,6;
                $i4 = substr $_,17,6;
                $fci = substr $_,23,10;
                $phi = substr $_,33,5;
                $multi = substr $_,38,4;
                print "$t1$t2$t3$t4$fci$phi$multi\n";
		# Remove spaces
		$i1 =~ s/\s+//;
                $i2 =~ s/\s+//;
                $i3 =~ s/\s+//;
                $i4 =~ s/\s+//;
		print LIB "$atomname[$i2]\t$atomname[$i3]\t$atomname[$i1]\t$atomname[$i4]\n";
		# Print to PRM
                $phi =~ s/\s+//;
                $multi =~ s/\s+//;
                $Qfci = $fci;
                if($phi > 0){
                        $phi=0.0;
                }else{
                        $phi=180.0;
                }
                printf IPHI "T%s\tT%s\tT%s\tT%s\t%5.3f\t%5.1f\t%5.1f\t1.000\t\n", $atomname[$i2], $atomname[$i3], $atomname[$i1], $atomname[$i4], $Qfci, $multi, $phi;
		}

        }

}

# Print torsions

for ($j=1;$j<$nt;$j++){

	if($t_full[$j] eq $t_full[$j+1]){
		printf PHI "T%s\tT%s\tT%s\tT%s\t%5.3f\t%5.1f\t%5.1f\t1.000\t\n", $atomname[abs($t1[$j])], $atomname[abs($t2[$j])], $atomname[abs($t3[$j])], $atomname[abs($t4[$j])], $Qfct[$j], -$multi[$j], $phi[$j];
	} else{
		printf PHI "T%s\tT%s\tT%s\tT%s\t%5.3f\t%5.1f\t%5.1f\t1.000\t\n", $atomname[abs($t1[$j])], $atomname[abs($t2[$j])], $atomname[abs($t3[$j])], $atomname[abs($t4[$j])], $Qfct[$j], $multi[$j], $phi[$j];
	}

}

# Print charge groups
print LIB "\n[charge_groups]";
$nh=1;
for($j=1;$j<=$i;$j++){
	if($atomtype2mass{$atomtype[$j]} < 2){
		$hydrogens[$nh] = "$atomname[$j] ";
		$nh++;
	}else{
		print LIB "\n$atomname[$j] ";

	}
}

print LIB @hydrogens;
