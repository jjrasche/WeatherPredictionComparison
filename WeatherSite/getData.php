<?php
	$conn=mysqli_connect("localhost","root","password","WUnderground");
//	echo((string)$conn);
	// Check connection
	if (mysqli_connect_errno()) {
	  echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
//
	  $QueryCommand = "SELECT $option, COUNT($option) AS num FROM stats s where (s.ttp=$hour);";

	$result = mysqli_query($conn,"select temp, count(*) as count from stats s where (s.ttp=-8) group by temp;");// "SELECT cond FROM stats s where (s.ttp=-3);");

	if (!$result) {
	    printf("Error: %s\n", mysqli_error($conn));
	    exit();
	}
	//echo $result->num_rows;

	$label = array();
	$data = array();

	while($row = mysqli_fetch_array($result)) {
    //echo $row[0] . "  " . $row[1];
    //echo "\r\n";
		//echo $row;//. "   " . $row["COUNT($option) AS num"];
		$l = $row[0];
		$c = $row[1];
		$label[] = $l;
		$data[] = $c;
	}
	echo json_encode(array('label'=>$label,'data'=>$data));

?>