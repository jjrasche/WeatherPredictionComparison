<?php
	if(isset($_POST['hour']) and isset($_POST['option'])) {
	  $hour = $_POST['hour'];
	  $option = $_POST['option'];

	  //$QueryCommand = "SELECT $option FROM stats s where (s.ttp=-$hour );";
	  $QueryCommand = "SELECT $option, COUNT(*) as count FROM stats s WHERE (s.ttp=-$hour) GROUP BY $option;";
	  //echo $QueryCommand;
	} else {
	  echo "one of the variables is null";
	}

	$conn=mysqli_connect("localhost","root","password","WUnderground");
	if (mysqli_connect_errno()) {
	  echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}

	$result = mysqli_query($conn, $QueryCommand);
	if (!$result) {
	    printf("Error: %s\n", mysqli_error($conn));
	    exit();
	}


	$label = array();
	$data = array();
	while($row = mysqli_fetch_array($result)) {
		$l = $row[0];
		$c = $row[1];
		$label[] = $l;
		$data[] = $c;
	}
	echo json_encode(array('rows'=>$result->num_rows,'label'=>$label,'data'=>$data));

	mysqli_close($conn);
?>
