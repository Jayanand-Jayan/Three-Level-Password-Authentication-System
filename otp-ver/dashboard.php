<?php
session_start();
if(isset($_SESSION['IS_LOGIN'])){
	echo "<h1 align='center'>Welcome User</h1>";
}else{
	header('location:index.php');
	die();
}
?>
<form action="logout.php">
	<input type="submit" style='font-family: consolas' value="Logout"/>	
</form>
