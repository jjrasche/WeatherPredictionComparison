<?php
	include 'functions.php';

	if ($_SERVER['HTTP_CLIENT_IP']!="") 			$ip = $_SERVER['HTTP_CLIENT_IP'];
	elseif ($_SERVER['HTTP_X_FORWARDED_FOR']!="")  	$ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
	else 											$ip = $_SERVER['REMOTE_ADDR'];

	if(isset($_POST['hour']) and isset($_POST['option'])) {
	  $hour = $_POST['hour'];
	  $option = $_POST['option'];
	} else {
	  echo "one of the variables is null";
	  echo json_encode(performStatsQuery(10, "temp", null));
	  exit();
	}

	echo json_encode(performStatsQuery($hour, $option, $ip));
?>
