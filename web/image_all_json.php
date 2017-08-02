<?php

# get all the files that match pattern in pics directory
$dir    = './pics/*.jpg';
$files = glob($dir);

# sort them by date
usort($files, function($a, $b) {
    return filemtime($a) < filemtime($b);
});

# remove the file path portion
foreach ($files as $key => $value) {
    $files[$key] = str_replace('./pics/', '', $value);
}

# remove ever

# change content type to json
header('Content-Type: application/json');

# dump out files as json
echo json_encode($files);

?>
