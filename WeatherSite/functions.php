<?php

	function performStatsQuery($hour, $option, $ip) {
		$startTime = microtime(True);
	  	$QueryCommand = "SELECT $option, COUNT(*) as count FROM stats s WHERE (s.ttp=-$hour) GROUP BY $option;";


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
		
	  	$totalRows = mysqli_query($conn, "SELECT * FROM stats;")->num_rows;

		mysqli_close($conn);

		$endTime = microtime(True);
		$searchTime = $endTime - $startTime;

		$ret = array('rows'=>$totalRows,'label'=>$label,'data'=>$data, 
					 'searchTime'=>$searchTime, 'userIP'=>$ip, "cmd"=>$QueryCommand);
		return $ret;
	}
?>