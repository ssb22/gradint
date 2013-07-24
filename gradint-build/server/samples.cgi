#!/bin/bash

# Gradint online samples browser v1.1 (c) 2011,2013 Silas S. Brown.  License: GPL

# Works as an "indexing" CGI.
# To set up in Apache, make .htaccess with:
# Options -Indexes
# ErrorDocument 403 /~your-user-ID/cgi-bin/samples.cgi
# <FilesMatch "\.(txt)$">
# ForceType 'text/plain; charset=UTF-8' 
# </FilesMatch>

# and change the /home/ssb22 in the script below.

# To set up in mathopd, configure like this:
#		Control {
#		  Alias /samples
#		  Location /home/userID/gradint/samples/
#		  AutoIndexCommand /home/userID/path/to/samples.cgi
#		}

# and delete the REQUEST_URI logic below.

# You can override this script in selected (sub)directories
# by making index.html files for those.

if ! test "a$REQUEST_URI" == a; then
  cd "/home/ssb22/public_html/$(echo "$REQUEST_URI"|sed -e 's/?.*//')"
fi # else assume the server put us in the right directory, like mathopd does

if echo "$SERVER_SOFTWARE"|grep Apache >/dev/null; then
  echo "Status: 200 OK" # overriding the 403
fi # (mathopd doesn't need this, and not tested with all mathopd versions)

export Filename="$(pwd|sed -e 's,.*/,,').zip"

if test "$QUERY_STRING" == zip || test "a$(echo "$REQUEST_URI"|sed -e 's/.*?//')" == azip; then
  echo Content-type: application/zip
  echo "Content-Disposition: attachment; filename=$Filename"
  echo
  cd .. ; zip -9r - "$(echo "$Filename"|sed -e s/.zip$//)"
else
  echo "Content-type: text/html; charset=utf-8"
  echo
  echo "<HTML><BODY><A HREF=\"..\">Parent directory</A> |"
  echo "<A HREF=\"./?zip\">Download $Filename</A> (expands to $(du -h --apparent-size -s|cut -f1))"
  echo "<h2>Contents of $Filename</h2><UL>"
  cat <<EOF
<script language="Javascript"><!--
function h5a(link) {
 if (!link.nextSibling) return true;
 if (link.nextSibling.src) {
   link.nextSibling.play();
   return false;
 } else {
   var ae = document.createElement('audio');
   var atype;
   if (link.href.match("mp3$")) atype="audio/mpeg";
   else if (link.href.match("wav$")) atype="audio/wav";
   else if (link.href.match("ogg$")) atype="audio/ogg";
   else return true;
   if (ae.canPlayType && function(s){return s!="" && s!="no"}(ae.canPlayType(atype))) {
 ae.setAttribute('src', link.href);
 ae.setAttribute('controls', 'controls');
 link.parentNode.insertBefore(ae,link.nextSibling);
 ae.play();
 return false;
   }
} return true;}
//--></script>
EOF
  for N in *; do
    export Size=$(du -h --apparent-size -s "$N"|cut -f1)
    if echo "$N"|grep '\.txt$'>/dev/null && echo $Size|grep '^[0-9]*$' >/dev/null;then export Size="$(cat "$N")";else export Size="($Size)"; fi
    echo "<LI><A HREF=\"$N\" onClick=\"javascript:return h5a(this)\">$N</A> $Size</LI>"
  done
  echo "</UL></BODY></HTML>"
fi
