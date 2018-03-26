#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Session; 

warningsToBrowser(1);

# print start of HTML ASAP to assist debugging if there is an error in the script

$q = CGI->new(); # new query object 
$session = CGI::Session->new($q); # load existing session or create a new session;    
$session->expire("3h"); # set expiration time (optional).

#print $session->header(); 
print page_header();
print page_bodystyle();


# some globals used through the script
$debug = 1;
$flag = 1;

$dataset_size = "small"; 
$users_dir = "dataset-$dataset_size/users";
$bleats_dir = "dataset-$dataset_size/bleats";

my $search_string = param('search_string');
#print h1(param('search_string'),"hahahahhahahhahhahhahah"),"\n";
my @users = glob("$users_dir/*");
$search_string = lc($search_string);

if($session->param('username')){
	print "<h4 class='welcome'>Welcome! $user</h4>\n";
	
	my $count = 0;
	foreach my $user (@users){
		$user =~ s/$users_dir\///;
		$user2 = lc($user);
		if($user2 =~ /$search_string/){
			chomp($user);
			print "<form action='see_other_home_page.cgi' method='POST'>\n";
			print "<h3 class='login_font'>$user\n";
			print hidden('user_home_to_go',$user);
			print "<input type='submit' class='user_page_button' name='go to his home' 
			value='VISIT HIS/HER HOME'></h3>\n";
			print end_form,"\n";
			$count++;
		}else{
			chomp($user);
			my $detail = "$users_dir/$user/details.txt";
			open my $f,"$detail";
			my @details = <$f>;
			
			foreach my $line (@details){
				if($line =~ /^full_name:/){
					my $full_name = $line;
					$full_name =~ s/full_name: //;
					$full_name = lc($full_name);
					if($full_name =~ /$search_string/){
						
						print "<form action='see_other_home_page.cgi' method='POST'>\n";
						print "<h3 class='login_font'>$user\n";
						print hidden('user_home_to_go',$user);
						print "<input type='submit' class='user_page_button' name='go to his home' 
							value='VISIT HIS/HER HOME'></h3>\n";
						print end_form,"\n";
						$count++;
					}
				}
			}
		}
	}
	
	if($count == 0){
		print "<center><p class='wrong_info'>Sorry, no users match!<br><\p></center>";
		print "<a href='bitter.cgi'>BACK HOME</a>\n";
	}else{
		print "<center><p color='gray'>There are $count results</p></center>\n";
		print "<a href='bitter.cgi'>BACK HOME</a>\n";
	}
	
	print start_form(-action=>"logout_page.cgi"); # send to a new script index3.cgi 
    print "<right><input type='submit' value='Log Out' name='logout' class='logout_button'></right>\n";
    print end_form(); 
     
	
}else{
	print "<form action='bitter.cgi' method='POST'>";
    print "<center><p class='wrong_info'>Sorry, Time out! Please log in again!</p>\n";
    print "<input type='submit' class='user_page_button' name='time 
    	out login again' class='login_font' value='Go To Log In'></center>\n";
    print end_form,"\n";
}


# display users' details 
print page_trailer();

exit 0; 


#
# HTML placed at bottom of every screen
#
sub page_header {
    return $session->header(),
        start_html("-title"=>"Infinity Bleat",-style=>{-src=>['http://cgi.cse.unsw.edu.au/~z5038771/ass2/bitter.css']}),"\n",
        "<link href='http://cgi.cse.unsw.edu.au/~z5038771/ass2/bitter.css' type='text/css' rel='stylesheet' />\n",
        "<h1 class='bitter_heading'>Infinity Bleat</h1>\n";
}

sub page_bodystyle{
    return "<body class='login_page'>\n";
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}
