body { padding: 0; margin: 0; background: #DFDCD1; font-family: "Lucida Grande", Helvetica, Arial,Verdana, sans-serif; color: #444340; }
h1 { font-size: 1.3em; padding: 15px 10px; margin: 0; }
h2 { font-size: 1.1em; padding: 10px; margin: 0; }
img { border: none; }
a { color: #444340; }

#Header { background: #EEBF02; height: 61px; padding: 0; border-bottom: 1px solid #3c3c3c;  }
#Header img { display: block; margin: 0 auto 0; }

#MainContent { background: #ffffff; padding-bottom: 30px; }

#Footer { padding: 10px; border-top: none; } 

#SocialLinks { padding: 10px 0 0 0; }
#SocialLinks:after { clear: both; content: "."; display: block; height: 0; visibility: hidden; }
#SocialLinks a { display: block; float: left; padding-right: 15px; }

.gallery { list-style: none; padding: 0; margin: 0; }
.gallery:after { clear: both; content: "."; display: block; height: 0; visibility: hidden; }
.gallery li { float: left; width: ${rpercent}; }
.gallery li a { display: block; margin: 5px; border: 1px solid #3c3c3c; }
.gallery li img { display: block; width: 100%; height: auto; }


/* For inline examples only */
#PhotoSwipeTarget { width: 100%; height: 200px; }

#Indicators { text-align: center; margin-top: 20px; }
#Indicators span { display: inline-block; height: 10px; width: 10px; margin: 0 10px 0 0; padding: 0; -webkit-border-radius:5px; -moz-border-radius:5px; -o-border-radius:5px; border-radius:5px; background: #c5c5c5; overflow:hidden; }
#Indicators span.current{ background: #EEBF02; }
