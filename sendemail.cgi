#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;

print header;
print start_html("Results");

# Set the PATH environment variable to the same path
# # where sendmail is located:
#
$ENV{PATH} = "/usr/sbin";

# open the pipe to sendmail
open (MAIL, "|/usr/sbin/sendmail -oi -t ") or &dienice("Can't fork for sendmail: $!\n");

# change this to your own e-mail address
my $recipient = 'nullbox@cgi101.com';

# Start printing the mail headers
# You must specify who it's to, or it won't be delivered:

print MAIL "To: $recipient\n";

# From should probably be the webserver, although you could set it 
# to the visitor's email address too.

print MAIL "From: nobody\@cgi101.com\n";

# print out a subject line so you know it's from your form cgi.

print MAIL "Subject: Form Data\n\n";

# Now print the body of your mail message.

foreach my $p (param()) {
   print MAIL "$p = ", param($p), "\n";
}

# Be sure to close the MAIL input stream so that the message
# actually gets mailed.

close(MAIL);

# Now print a thank-you page 

print <<EndHTML;
<h2>Thank You</h2>
<p>Thank you for writing!</p>
<p>Return to our <a href="index.html">home page</a></p>
EndHTML

print end_html;

# The dienice subroutine handles errors.

sub dienice {
    my ($errmsg) = @_;
    print "<h2>Error</h2>\n";
    print "<p>$errmsg</p>\n";
    print end_html;
    exit;
}
