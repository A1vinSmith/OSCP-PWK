<?php

	if(isset($_POST["upload"]) && is_uploaded_file($_FILES["file"]["tmp_name"])){
		$target = "uploads/".basename($_FILES["file"]["name"]);
		$goodExts = ["jpg", "jpeg", "png", "gif"];
		if(file_exists($target)){
			header("location: ./?msg=Exists");
			die();
		}
		$size = getimagesize($_FILES["file"]["tmp_name"]);
		if(!in_array(explode(".", $_FILES["file"]["name"])[1], $goodExts) || !$size){
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
			case "Exists":
				$res = "File already exists";
				break;
			case "Method":
				$res = "No file send";
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
				<input type="file" name="file" id="fileEntry" required, accept="image/jpeg,image/png,image/gif">
				<input type="submit" name="upload" id="fileSubmit" value="Upload">
			</form>
			<p id=res><?php if (isset($res)){ echo $res; };?></p>
		</main>	
	</body>
</html>

