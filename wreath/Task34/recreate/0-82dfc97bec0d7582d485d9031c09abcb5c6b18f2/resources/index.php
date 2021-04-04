<?php

	if(isset($_POST["upload"]) && is_uploaded_file($_FILES["file"]["tmp_name"])){
		$target = "uploads/".basename($_FILES["file"]["name"]);

		$finfo = finfo_open(FILEINFO_MIME_TYPE);
		$type = finfo_file($finfo, $_FILES["file"]["tmp_name"]);
		finfo_close($finfo);
		
		if(!in_array($type, ["image/jpeg", "image/jpg", "image/png", "image/gif"])){
			header("location: ./?msg=Fail");
			die();
		}
		move_uploaded_file($_FILES["file"]["tmp_name"], $target);	
		header("location: ./?msg=Success");
		die();
	} else if ($_SERVER["REQUEST_METHOD"] == "post"){
		header("location: ./?msg=Method");
	}


	if(isset($_GET["msg"])){
		$msg = $_GET["msg"];
		switch ($msg) {
			case "Success":
				$res = "File uploaded successfully!";
				break;
			case "Fail":
				$res = "Invalid File Type";
				break;
			case "Method":
				$res = "No file sendt";
				break;
		
		}
	}
?>
<!DOCTYPE html>
<html lang=en>
	<!-- ToDo:
		  - Finish the styling: it looks awful
		  - Get Ruby more food. Greedy animal is going through it too fast
		  - Upgrade the filter on this page. Can't rely on basic auth for everything
		  - Phone Mrs Walker about the neighbourhood watch meetings
	-->
	<head>	
		<title>Ruby Pictures</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" type="text/css" href="assets/css/Andika.css">
		<link rel="stylesheet" type="text/css" href="assets/css/styles.css">
	</head>
	<body>
		<main>
			<h1>Welcome Thomas!</h1>
			<h2>Ruby Image Upload Page</h2>
			<form method="post" enctype="multipart/form-data">
				<input type="file" name="file" id="fileEntry" required>
				<input type="submit" name="upload" id="fileSubmit" value="Upload">
			</form>
			<p id=res><?php if (isset($res)){ echo $res; };?></p>
		</main>	
	</body>
</html>

