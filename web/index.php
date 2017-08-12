
<!DOCTYPE html>
<html>
	<head>
		<title>UNICAM!</title>
		<link rel="stylesheet" href="css.css" />
    <script src="jquery-3.2.1.min.js"></script>
    <script>
      $(document).ready(function(){

				$thumb = $(".thumb");
				$lightbox = $(".lightbox-wrapper");
				$lightbox_inner = $(".lightbox-inner");
				$lightbox_close = $(".lightbox-close");
				$lightbox_img = $(".lightbox-image");
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
							$wrapper.append('<a class="thumb" href="/pics/' + image + '"><img src="/thumbs/' + image + '"></a>');
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
												$wrapper.prepend('<a class="thumb" href="/pics/' + image + '"><img src="/thumbs/' + image + '"></a>');
												all_images.push(image);
												console.log(all_images);
											}
							    }).fail(function() {
							        // Image doesn't exist - do something else.
							    })
							});
						});
					}, frequency);

					$('body').on('click', ".thumb", function(e) {

						e.preventDefault();

						url = $(this).attr("href");

						$lightbox_img.attr("src", url);
						$lightbox.removeClass("hidden");
						$lightbox_close.removeClass("hidden");
						$lightbox_inner.removeClass("hidden");



					});

					$(".lightbox-wrapper, .lightbox-close").click(function(){
						$lightbox.addClass("hidden");
						$lightbox_close.addClass("hidden");
						$lightbox_inner.addClass("hidden");
					});

      });
    </script>
	</head>

	<body class="">

		<div id="wrapper">

		</div>

		<div class="lightbox-wrapper hidden"></div>
		<div class="lightbox-inner hidden">
			<img src="" class="lightbox-image"/>
		</div>
		<div class="lightbox-close hidden">&times;</div>

	</body>

</html>
