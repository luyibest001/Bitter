#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;
use List::Util qw/min max/;
#use CSS::Compressor qw(css_compress);
warningsToBrowser(1);

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();
print page_bodystyle();

$dataset_size = "small";
$users_dir = "dataset-$dataset_size/users";
$bleats_dir = "dataset-$dataset_size/bleats";

chdir $users_dir;
exec("ls");
print "<br>\n<br>\n";
$username = "Loy";
mkdir $username;
exec("ls");

# display users' details
print page_trailer();

exit 0;


#
# HTML placed at bottom of every screen
#
sub page_header {
return header,
start_html("-title"=>"Infinity Bleat",-style=>{-src=>['http://cgi.cse.unsw.edu.au/~z5038771/ass2/bitter.css']}),"\n",
"<link href='http://cgi.cse.unsw.edu.au/~z5038771/ass2/bitter.css' type='text/css' rel='stylesheet' />\n",
"<h1 class='bitter_heading'>Infinity Bleat</h1>\n";
}

sub page_bodystyle{
return "<body>\n";
}




sub page_trailer {
my $html = "";
$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
$html .= end_html;
return $html;
}


