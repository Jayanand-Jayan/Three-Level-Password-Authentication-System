<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>TresSecura - OTP Verification</title>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> 
		<style type="text/css">
			.login-form {
				width: 340px;
				margin: 50px auto;
			}
			.login-form form {
				margin-bottom: 15px;
				background: #f7f7f7;
				box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
				padding: 30px;
			}
			.login-form h2 {
				margin: 0 0 15px;
			}
			.form-control, .btn {
				min-height: 38px;
				border-radius: 2px;
			}
			.btn {        
				font-size: 15px;
				font-weight: bold;
			}
		</style>
	</head>
<body>
	<div class="login-form">
		<img src="Logo.png" style="width: 400px; height=250px; align-items: left;">
		<form  method="post">
			<h2 class="text-center">Log in</h2>       
			<div class="form-group first_box">
				<input type="text" id="email" class="form-control" placeholder="Email" required="required">
				<span id="email_error" class="field_error"></span>
			</div>
			<div class="form-group first_box">
				<button type="button" class="btn btn-primary btn-block" onclick="send_otp()">Acquire OTP</button>
			</div>
			<div class="form-group second_box">
				<input type="text" id="otp" class="form-control" placeholder="OTP" required="required">
				<span id="otp_error" class="field_error"></span>
			</div>
			<div class="form-group second_box">
				<button type="button" class="btn btn-primary btn-block" onclick="submit_otp()">Submit OTP</button>
			</div>       
		</form>
	</div>
	<script>
		function send_otp(){
			var email=jQuery('#email').val();
			jQuery.ajax({
				url:'send_otp.php',
				type:'post',
				data:'email='+ email,
				success:function(result){
					// alert(result);
					if(result=='yes'){
						jQuery('.second_box').show();
						jQuery('.first_box').hide();
					}
					if(result=='not_exist'){
						jQuery('#email_error').html('Please enter a valid email');
					}
				}
			});
		}

		function submit_otp(){
			var otp=jQuery('#otp').val();
			jQuery.ajax({
				url:'check_otp.php',
				type:'post',
				data:'otp='+otp,
				success:function(result){
					if(result=='yes'){
						window.location='http://localhost:8000/display_qr'
					}
					if(result=='not_exist'){
						jQuery('#otp_error').html('Please enter a valid otp');
					}
				}
			});
		}
	</script>
	<style>
		.second_box {
			display:none;
		}
		.field_error {
			color:red;
		}
	</style>
</body>
</html>                                		                            