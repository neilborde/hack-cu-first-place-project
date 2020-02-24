url = 'http://127.0.0.1:5000/api/'

scoreboard();

function scoreboard() {
	$.ajax({
	type: 'POST',
	url: url + 'topten',
	contentType: false,
	cache: false,
	processData: false,
	success: function(data) {

	    	board = document.getElementById('leaderboard');
	    	board.style.visibility = 'visible';

	    	positions = document.getElementById('positions');
	    	positions.innerHTML = "";
	    	for (let i = 0; i < 10; i++) {
		    		if (data[i].score >= 0) {
		    		positions.innerHTML += '<tr><td>'+ (i+1) + '</td><td class="username" onmouseout=out(\'user'+i+'\') onmouseover=img(\'user'+i+'\') id=user'+i+'>' + data[i].username + '</td><td>' + data[i].score + '</td></tr>';
		    	}
	    	}
	}});
}

function file_upload() {
		// var form_data = new FormData($('#upload-file')[0]);
		var filelist = document.getElementById("upload-file");
		var user = document.getElementById("user").value.toString();
		let loading = document.getElementsByClassName("loading");
		let results = document.getElementsByClassName("result");
		var f = filelist.files[0]
		var filename = f.name
		console.log(user)
		var form_data = new FormData();
		form_data.append('file', filelist.files[0]);
		form_data.append('user',user)

		for (var i = loading.length - 1; i >= 0; i--) {
			loading[i].style.display = 'block';
		}

		u = url + 'browser_upload'
	    $.ajax({
	        type: 'POST',
	        url: u,
	        data: form_data,
	        contentType: false,
	        cache: false,
	        processData: false,
	        success: function(data) {

	            if (data.status) {
	            	let loading = document.getElementsByClassName("loading");
					let results = document.getElementsByClassName("result");
	            	for (var i = loading.length - 1; i >= 0; i--) {
						loading[i].style.display = 'none';
					}
					for (var i = results.length - 1; i >= 0; i--) {
						results[i].style.display = 'block';
					}
					let score_element = document.getElementById("result")
					score_element.innerText = data.score;
					let img = document.getElementById("resultImg")
					img.src = data.filepath;
					scoreboard();
	            } else {
	            	alert('Could not upload file...')
	            }
	        },
	        error: function(data) {
	        	alert('file could not be uploaded')
	        }
	    });
}


function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  }
  // else {
  //   removeUpload();
  // }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}
$('.image-upload-wrap').bind('dragover', function () {
        $('.image-upload-wrap').addClass('image-dropping');
    });
    $('.image-upload-wrap').bind('dragleave', function () {
        $('.image-upload-wrap').removeClass('image-dropping');
});

 function out(tag) {
	let d = document.getElementById('display');
	d.style.visibility = 'hidden';
}

function img(tag) {
	let d = document.getElementById('display');
	d.style.visibility = 'visible';

	let user = document.getElementById(tag);
	let u = user.innerText;

	var form_data = new FormData();
	form_data.append('user',u)
	$.ajax({
	        type: 'POST',
	        url: url+"serveimage",
	        data: form_data,
	        contentType: false,
	        cache: false,
	        processData: false,
	        success: function(data) {

	            if (data.status) {
	            	let img = document.getElementById('displayIMG');
	            	img.src = data.filepath;
	            }
	        }
	    });
}
