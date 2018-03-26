#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Session; 

warningsToBrowser(1);

$q = CGI->new(); # new query object 
$session = CGI::Session->new($q); # load existing session or create a new session;    
$session->expire("3h"); # set expiration time (optional).

print page_header();
print page_bodystyle();

$dataset_size = "small"; 
$users_dir = "dataset-$dataset_size/users";
$bleats_dir = "dataset-$dataset_size/bleats";
my $my_home = 1;
my $other_home = 2;

my $user = param('user_home_to_go');
my $who_am_I = $session->param('username');
#print h1($user);
#chomp($user);


if($session->param('username')){
	print "<h4 class='welcome'>Welcome! $who_am_I</h4>\n";
	print "<form action='logout_page.cgi' method='POST'>\n";
	
	print "<input type='submit' class='logout_button' name='logout' value='Log Out'>\n";
	print end_form,"\n";
    print "<a href='bitter.cgi'>BACK TO MY HOME</a>\n";
    print "<a href='ViewListening.cgi'>BACK TO MY LISTENING</a>\n";
    print "<a href='ViewListened.cgi'>BACK TO MY LISTENED</a>\n";
    print "<a href='viewhislistening.cgi'>HIS/HER LISTENING</a>\n";
    print "<a href='viewhislistened.cgi'>HIS/HER LISTENER</a>\n";

    print "<center><h3 class='other_page_sub_heading'><b>$user</b></h3></center>\n";
    
    my $detail = "$users_dir/$user/details.txt";
    #print h2($detail);
    my $image = "$users_dir/$user/profile.jpg";
    open my $p, "$detail";
    my @details = <$p>;
    
    if(open F,"<$image"){
        print "<div id='profile_pic'><center><img SRC='$image'></center></div>","\n";
    }else{
        print "<center><p>No Profile Image</p></center>\n";
    }
    #print start_form,"\n";
    #print "<left><input type='submit' class='user_page_button' name='see_this_user_profile' value='view his/her profile'></left>\n";
    
    #if(defined param('see_this_user_profile')){
    print "<h2 class='ohter_page_sub_heading'>Profile</h2>\n";
    print "<h4 class='login_font'>\n";
    
    foreach my $line (@details){
        if($line =~ /^email:/){
            my $email = $line;
            $email =~ s/email: //;
            #print $email;
            @emails = split(//,$email);
            #print "$emails[11] hahaahah\n";
            my $pos = 3;
            while($pos < $#emails-2){
                if($emails[$pos] ne '@'){
                    $emails[$pos] = "*";
                }
                $pos++;
            }
            print "<br>E-mail: @emails<br>\n";
        }elsif($line =~ /^home_suburb:/){
            my $home_suburb = $line;
            $home_suburb =~ s/home_suburb: //;
            print "<br>Home Suburb: $home_suburb<br>\n";
        }elsif($line =~ /^home_longitude:/){
            my $home_longitude = $line;
            $home_longitude =~ s/home_longitude: //;
            print "<br>Home Longitude: $home_longitude<br>\n";
        }elsif($line =~ /^home_latitude:/){
            my $home_latitude = $line;
            $home_latitude =~ s/home_latitude: //;
            print "<br>Home Longitude: $home_longitude<br>\n";
        }#elsif($line =~ /^full_name:/){
          #  my $full_name = $line;
           # $full_name =~ s/full_name: //;
            #print "<p class='login_font'>Full Name: $full_name</p>\n";
        #}
    }
    #}
    print "<br><br></h4>\n";
    print end_form,"\n";

	print "<h2 class='other_page_sub_heading'>His/Her Bleat</h2><hr color='#990000'>\n";
    #print $user;
    
    ###  the Number of user's bleats
    my $user_bleats_num = "$users_dir/$user/bleats.txt";
    open my $f,"$user_bleats_num" or die "can not open $details_filename: $!";
    
    my @bleats_num = <$f>;
    
    if($#bleats_num+1 == 0){
        print "<center><h4 color='gray'>You have 0 bleat.</h4><br></center>\n";
    }else{
    
        my $count = $#bleats_num+1;
        print "<p class='info'>All bleats($count)</p>\n";
    ### find the bleats on each date

        foreach my $num (@bleats_num){
            my $bleats_by_num = "$bleats_dir/$num";
            open my $c,"$bleats_by_num" or die "can not open $bleats_by_num: $!";
            
            my @bleat_details = join '', <$c>;
            push(@All_bleats,@bleat_details);
            
        }
       
        @All_bleats_reverse = reverse(@All_bleats);
        foreach my $ele (@All_bleats_reverse){
            my @lines = split(/\n/,$ele);
            print "<p class='bitter_user_details'><b>\n";
            
            #foreach my $line (@lines){
           #     if(($line =! /time:/)){
            #        my $time = $line;
             #       $time =~ s/time: //;
            #        print "<center>$time</center><br>\n";
             #   }
            #}
            
            foreach my $line (@lines){
                if(($line !~ /username:/) && ($line !~ /time:/)){
                    print "$line<br>\n";
                }
                
            } 
            print "<form action='reply.cgi' method='POST'>";
            print hidden('which_bleat',$ele);
            print hidden('whose_bleat',$user);
            print "<center><input type='submit' class='bleat_button' value='Reply' name='delete bleat'></center>\n";
            print end_form,"\n";
            print "</b></p>\n";
        }
    }

}else{
    print "<form action='bitter.cgi' method='POST'>";
    print "<center><p class='wrong_info'>Sorry, Time out! Please log in again!</p></center>\n";
    print "<center><input type='submit' class='user_page_button' name='time out login again' class='login_font' value='Go To Log In'></center>\n";
    print end_form,"\n";
}




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
