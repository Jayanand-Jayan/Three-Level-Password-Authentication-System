<?php

require 'requires/PHPMailer.php';
require 'requires/Exception.php';
require 'requires/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

session_start();
$con=mysqli_connect('localhost','root','Monkey.D.Luffy','tresecura');
$email=$_POST['email'];
$res=mysqli_query($con, "select * from users where mail =  '$email'");
$count=mysqli_num_rows($res);
if($count>0){
	$otp=rand(100000, 999999);
	mysqli_query($con,"update users set otp='$otp' where mail='$email'");
	$html="Hi there!<br>Your OTP verification code is: <h2>".$otp ."</h2>";
	$_SESSION['EMAIL']=$email;
	smtp_mailer($email,'OTP Verification',$html);
	echo "yes";
}else{
	echo "not_exist";
}

function smtp_mailer($to, $subject, $msg) {
	$mail = new PHPMailer(true); 
	$mail->IsSMTP(); 
	$mail->Host = "smtp.gmail.com";
	$mail->SMTPAuth = true; 
	$mail->Username = "ism.tressecura@gmail.com";
	$mail->Password = "ptubxasoyrugxgvt";
	$mail->SMTPSecure = 'ssl'; 
	$mail->Port = 465; 
	$mail->SetFrom("tressecura@gmail.com", "Tres Secura");
	$mail->AddAddress($to);
	$mail->IsHTML(true);
	$mail->CharSet = 'UTF-8';
	$mail->Subject = $subject;
	$mail->Body =$msg;
	if(!$mail->Send()){
		return 0;
	}else{
		return 1;
	}
}
?>