<html>
    <head>
	<link rel="Stylesheet" type="text/css" href="./style.css" />
        <title>Search Results</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="mobile-web-app-capable" content="yes">
	<link rel="shortcut icon" type="image/png" href="../images/favicon.png"/>
	<meta name="viewport" content="width=device-width, initial-scale=1" /> 
    </head>
<body>

<h1>Search</h1>

<form action="#" method="post">
<input type="text" name="name" placeholder="Search...">
<input type="submit" name="submit">
</form>


</body>
</html>

<?php

function print_result($title, $url, $snippet){
echo '<li class="results"><div class="caption"><h2><a href="'.$url.'">'.$title.'</a></h2><div class="attribution"><cite>'.$url.'</cite></div><div class="snippet"><p>'.$snippet.'</div></div></li>';
}

if(isset($_POST['submit'])){
// Fetching variables of the form which travels in URL
$name = $_POST['name'];
header("Location:http://localhost:8000/index.php?q=".$_POST['name']);
}
else{
$servername = "localhost";
$username = "vishnu";
$password = "CrapWeasel";
$dbname = "search_index";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
$queries = array();
parse_str($_SERVER['QUERY_STRING'], $queries);
$sql = "SELECT url,title,body, MATCH (url,title,body) AGAINST ('$queries[q]' IN NATURAL LANGUAGE MODE) AS score FROM itsie_index WHERE MATCH (url,title,body) AGAINST ('$queries[q]' IN NATURAL LANGUAGE MODE) LIMIT 30;";
$exp= "[^.]* $queries[q] [^.]*\.";
$result = $conn->query($sql);
echo '<h3>Search Results for: '.$queries['q'].'</h3>';
if (!empty($result) && $result->num_rows > 0) {
// if ($result->num_rows > 0) {
	// output data of each row
	$matches = array();
	while($row = $result->fetch_assoc()) {
		// echo $row["body"];
			// echo $exp;
		if (preg_match("/\.().*?$queries[q].*?(\n|\.)/", $row["body"], $matches)) {
			// echo "Yes";
			// var_dump($matches);
}
	// preg_match($exp, $row["body"], $matches);
// echo '<li><a href="'. $row["url"].'">'.$row["title"]."</a> (".$row["url"].")</li>\n";
print_result($row["title"], $row["url"], array_pop(array_reverse($matches)));
			// echo array_pop(array_reverse($matches));
  }
} else {
  echo "0 results";
}
$conn->close();
}
?>
