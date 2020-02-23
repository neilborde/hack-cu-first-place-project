url = 'http://127.0.0.1:5000/api/'


function file_upload() {
		// var form_data = new FormData($('#upload-file')[0]);
		var filelist = document.getElementById("upload-file");
		console.log($('#upload-file')[0]);
		var form_data = new FormData();
		form_data.append('file', filelist.files[0]);
		u = url + 'browser_upload'
	    $.ajax({
	        type: 'POST',
	        url: u,
          name: name,
	        data: form_data,
	        contentType: false,
	        cache: false,
	        processData: false,
	        success: function(data) {

	            if (data.status) {
	            	alert('File uploaded!')
	            } else {
	            	alert('Could not upload file...')
	            }
	        },
	        error: function(data) {

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
