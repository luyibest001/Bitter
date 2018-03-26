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


### three login status
my $username_password_correct = 0;
my $no_such_user = 1;
my $password_incorrect = 2;
my $invalid_username = 3;

my $UserName;

#if(!param('login') && !param('register')){ #!=1  didn't login neither register
 #   home_login_page();
#}

if(!$session->param('username')){
    if(defined param('go to my home page')){
        print "<center><p class='wrong_info'>Please log in first</p></center>\n";
        home_login_page();
    }else{
        home_login_page();
    }
}else{
    if(defined param('go to my home page')){
        user_home_page();
    }else{
        my $user = $session->param('username');
        print "<h4 class='welcome'>Welcome! $user</h4>\n";
        home_login_page();
    }
    
}

sub home_login_page{
    
    if(param('username') && param('password')){
        if(authenticate_username_password() == $username_password_correct){
            $username = param('username');
            param('login', 1);
            param('register',1);
            $session->param('username', $username); 
            
            if ($session->param('username')){  
                #print "You said you are " . $session->param('username'). ". <br> <br>";
                user_home_page();
            } else { 

                print "No name in session! "; 
            }

            
        }elsif(authenticate_username_password() == $invalid_username){
            print start_form,"\n";
            print "<center><h3 class='wrong_info'>Invalid username!(An username is made up of letters, 0-9 or '_'.)</h3></center>\n";
            
            login_screen();
        }elsif(authenticate_username_password() == $no_such_user){
            print start_form,"\n";           
            print "<center><h3 class='wrong_info'>Sorry username doesn't exist! Please try again...</h3></center>","\n";
            print hidden('password',''),"\n";
            print hidden('username',''),"\n";
            print end_form,"\n";
            login_screen();
        }elsif(authenticate_username_password() == $password_incorrect){
            print start_form,"\n";
            print "<center><h3 class='wrong_info'>Sorry! Incorrect password.Please try again...</h3></center>","\n";
            print hidden('password',''),"\n";
            print hidden('username',''),"\n";
            print end_form,"\n";
            login_screen();
        }
        
    }else{
        login_screen();
    }
    return;
}

#authenticate_username_password()
sub authenticate_username_password{
    my $retVal=0;
    my $username = param('username');
    my $password = param('password');
    chomp($username);
    chomp($password);
    
    if($username =~ /[^a-zA-Z0-9_]/){
        $retVal = $invalid_username;
    }else{
        $UserName = $username;
        my $detail = "$users_dir/$username/details.txt";
        
        ### if the input is just the username of the user
        if(open my $G ,"<$detail"){
            my @details = <$G>;
            foreach my $line (@details){
                ### gain the correct password according to the user 
                if($line =~ /^password:/){
                    my $passwd = $line;
                    $passwd =~ s/password: //g;
                    chomp($passwd);
                    if($passwd eq $password){
                        $retVal = $username_password_correct;
                    }else{
                        $retVal = $password_incorrect;
                    } 
                }
            }
            
        }else{   
            $retVal = $no_such_user;
        }
    }
    #print h1($retVal),"\n";
    return $retVal;
}


sub login_screen{
	
    print "<form action='bitter.cgi' method='POST'>\n";
    print "<input type='submit' class='login_button' name='go to my home page' value='My Home'>\n";
    print end_form,"\n";

    print start_form, "\n";
    
    print "<center><h3 class='login_font'>Enter your username and password to log in.<br>\n";
    print "<br>Username:\n", textfield('username'), "<br>\n";
    print "<br>Password: \n", password_field('password'), "<br><br><h3></center>\n";
    
    print "<br>\n";
    print "<center><input type='submit' class='login_button' name='Login' value='Log In'>","\n";
    print "<input type='reset' class='login_button' name='Reset' value='Reset'></center>","\n<br>\n<br/>\n";
    
    print "<center><a href='forgetPassword.cgi'>Forget password?</a></center>","\n";
    print end_form,"\n";
        
    print qq(<form action="register_page.cgi" method='POST'>),"\n";
    print "<br>\n";
    print "<hr color='#990000'>\n";
    print "<center><h3 color='#8B4513'>Don't have an account? Create one now! </h3></center>","\n";
    print "<br>\n";
    print "<center><input type='submit' class='login_button' name='Register Now' value='Register Now'>","</center>\n";
    print "<center><h3 class='login_description'>Join us now<br>Free your heart from bitter<br></h3></center>\n";

    print end_form, "\n";
    
}

my $search_string = param('search_string');
my $bleat_to_send = param('bleat');
my $search_bleat = param('search_bleat_string');
# user's home page
sub user_home_page{
    #print $session->param('username'),"\n";
    $UserName = $session->param('username'),"\n";
	print "<h4 class='welcome'>Welcome! $UserName</h4>\n";
    
    print "<ul>\n";
    print qq(<li><a href='home.cgi'>HOME</a></li>),"\n";
    print hidden('login',1);
    print hidden('register',1);
    print hidden('username',1);
    print hidden('password',1);
    
    print qq(<li><a href="viewprofile.cgi">MY PROFILE</a></li>),"\n";
    print hidden('login',1);
    print hidden('register',1);
    print hidden('username',1);
    print hidden('password',1);

    
    print qq(<a href="ViewListening.cgi" method="POST">LISTENING</a></li>),"\n";
    print hidden('login',1);
    print hidden('register',1);
    print hidden('username',1);
    print hidden('password',1);
  
    
    print qq(<li><a href="ViewListened.cgi">MY LISTENER</a></li>),"\n";
    print hidden('login',1);
    print hidden('register',1);
    print hidden('username',1);
    print hidden('password',1);

    print qq(<li><a href="viewbleat.cgi">MY BLEAT</a></li>),"\n";
    print hidden('login',1);
    print hidden('register',1);
    print hidden('username',1);
    print hidden('password',1);

    print "</ul>\n";

  	print "<form action='search_user.cgi' method='POST'>,\n";
  	print "<p class='login_font'>Search User: \n";
  	print "<input type='text' name='search_string'>\n";
  	print hidden('search_string',$search_string);
  	print "<input type='submit' class='login_button' name='search user' 
  		value='Search'></p>\n";
  	print  end_form,"\n";
  	
  	print "<form action='search_bleat.cgi' method='POST'>\n";
  	print "<p class='login_font'>Search Bleat: \n";
  	print "<input type='text' name='search_bleat_string'>\n";
  	print hidden('search_bleat_string',$search_bleat);
  	print "<input type='submit' class='login_button' name='search bleat' 
  		value='Search'></p>\n";
  	print end_form,"\n";
  	
    print "<center><h2 class='other_page_sub_heading'><b>$UserName</b></h2></center>\n<br>\n";
    my $profile_image = "$users_dir/$UserName/profile.jpg";
    print hidden('username',$UserName);
    if(open my $P,"<$profile_image"){
        print "<div id='profile_pic'><center><img SRC='$profile_image'></center></div>","\n";
    }else{
        print p("No Profile Image!"),"\n";
    }
        
    print "<br>\n";

    print qq(<form action="sendbleatpage.cgi" method='POST'>),"\n";
    print "<center><textarea style='width:500px; height:200px;
     border:solid 1px #191970; border-radius:20px; resize:none;'
     name='bleat'>Replace this with your bleat...(up to 142 characters)</textarea>\n<br>\n";
    print hidden('bleat',$bleat_to_send);
    print "<input type='submit' class='login_button' name='send bleat' value='Send'></center>\n<br>\n";
    print qq(</form>),"\n";
    
    print "<form action='deleteaccount.cgi' method='POST'>\n";
    print "<input type='submit' class='login_button' name='delete account' value='Delete Account'>\n";
    print end_form,"\n";
    
    print start_form(-action=>"logout_page.cgi"); # send to a new script index3.cgi 
    print "<right><input type='submit' value='Log Out' name='logout' class='logout_button'></right>\n";
    print end_form(); 
     
    return;
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
    return "<body class='other_page'>\n";
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
