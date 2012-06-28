<!DOCTYPE html>
<html>
<head>
	<title>${title}</title>
	<meta http-equiv="refresh" content=300 />
	<meta name="author" content="Ste Brennan - Code Computerlove - http://www.codecomputerlove.com/" />
	<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0;" name="viewport" />
	<meta name="apple-mobile-web-app-capable" content="yes" />
	<link href="styles.css" type="text/css" rel="stylesheet" />
	
	<link href="../photoswipe.css" type="text/css" rel="stylesheet" />
	
	<script type="text/javascript" src="../lib/klass.min.js"></script>
	<script type="text/javascript" src="../code.photoswipe-3.0.5.min.js"></script>
	
	
	<script type="text/javascript">
		(function(window, PhotoSwipe){
			document.addEventListener('DOMContentLoaded', function(){
				var options = {},
				instance = PhotoSwipe.attach( window.document.querySelectorAll('#Gallery a'), options );
			
			}, false);
		}(window, window.Code.PhotoSwipe));
	</script>
	
</head>
<body>

<div id="Header">
	<a href="${site}"><img src="${sitelogo}" width="230" height="48" alt="Code Computerlove" /></a>
</div>

<div id="MainContent">
	<div class="page-content">
		<h1>${title}</h1>
	</div>
	
	<ul id="Gallery" class="gallery">
	${expand()}
	</ul>
</div>	
</body>
</html>
