function showFile(imgDOM,e) {
	var files = e.target.files;
	for (var i = 0, f; f = files[i]; i++) {
		if (!f.type.match('image.*')) continue;
		var fr = new FileReader();
		fr.onload = (function(theFile) {
			return function(e) {
				document.getElementById(imgDOM).src = e.target.result;
	}
  })(f);

  fr.readAsDataURL(f);
}
}

function setCheckbox(e){

}