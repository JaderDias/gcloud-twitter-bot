use strict;
use warnings;
use 5.012;
 
my $title;
my $section;
my $language;
my @definitions;

my $file = 'enwiktionary-20220301-pages-articles.xml';
open my $fh, '<', $file or die "Could not open '$file' $!\n";

while (my $line = <$fh>) {
   chomp $line;

   my ($new_title) = $line =~ /<title>([^<]+)</;
   if ( $new_title ) {
	   if (@definitions) {
		   say(join("\t", $title, @definitions));

	   }
	   $title = $new_title =~ /^[a-záčćđíľňôšťúýž]+$/
	   	? $new_title
		: undef;
	   $language = undef;
	   $section = undef;
	   @definitions = ();
	   next;
   }

   if ( !$title ) {
	   next;
   }

   my ( $new_language) = $line =~ m#^==([^=]+)==$#;
   if ( $new_language ) {
	   $language = $new_language;
	   $section = undef;
	   next;
   }

   if (!$language || $language ne 'Serbo-Croatian') {
	   next;
   }

   my ( $new_section) = $line =~ m#^===(.+)===$#;
   if ( $new_section ) {
	   $section = $new_section;
	   next;
   }

   if ( !$section || $section ne 'Noun' ) {
	   next;
   }

   my ($definition) = $line =~ /^\# ([^{<]+)/;
   if ( $definition ) {
	   $definition =~ s/\[\[[^|\]]+\|//g;
	   $definition =~ s/\[\[//g;
	   $definition =~ s/\]\]//g;
	   if ( $definition !~ /Serbian/
		   && $definition !~ /[(']/
	   	   && $definition !~ /$title/i) {
		   push @definitions, $definition;
	   }
   }
}

close $fh;
