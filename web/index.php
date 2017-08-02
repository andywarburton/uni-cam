
<!DOCTYPE html>
<html>
	<head>
		<title>UNICAM!</title>
		<link rel="stylesheet" href="css.css" />
    <script src="jquery-3.2.1.min.js"></script>
    <script>
      $(document).ready(function(){

				$wrapper = $("#wrapper");
				var all_images = [];

				jQuery.ajaxSetup({
						beforeSend: function() {
							$('#loading').show();
						},
						complete: function(){
							$('#loading').hide();
						},
						success: function() {},
						cache: true
					});

					$.getJSON('image_all_json.php', function(data) {
						$.each(data, function(i, image) {
							$wrapper.append('<a href="/pics/' + image + '"><img src="/thumbs/' + image + '"></a>');
							all_images.push(image);
						});
					});

					frequency = 2000;
					setInterval(function() {
						$.getJSON('image_latest_json.php', function(data) {
							$.each(data, function(i, image) {
								$.get('/thumbs/' + image)
							    .done(function() {
							        // Do something now you know the image exists.
											if(!all_images.includes(image)) {
												$wrapper.prepend('<a href="/pics/' + image + '"><img src="/thumbs/' + image + '"></a>');
												all_images.push(image);
												console.log(all_images);
											}
							    }).fail(function() {
							        // Image doesn't exist - do something else.
							    })
							});
						});
					}, frequency);


      });
    </script>
	</head>

	<body>

		<div id="wrapper">

		</div>

	</body>

</html>
