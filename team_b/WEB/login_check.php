<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>전자 명부 대시보드</title>
</head>
<body>
  <?php 
    session_start();    // 세션 시작

    include 'config.php';   // DB 연동

    $username = $_POST['username'];   // post로 넘겨받은 값을 변수에 저장
    $phone = $_POST['phone'];

    $sql = "select person_name from person_info where person_name = '$username' and phone_num like '%$phone';"    // 입력받은 값과 DB에 저장된 값을 비교 --> 일치하는 행의 person_name값을 가져오라는 뜻
    $res = mysqli_query($con, $sql);   // mysqli_query: 쿼리 실행시키는 함수
    $row = mysqli_fetch_array($res);    // mysqli_fetch_array: mysqli_query를 통해 얻은 레코드를 가져오는 함수

    if($row != null){   // $row값이 존재한다면
      $_SESSION['username'] = $row['person_name'];    // 그 값을 세션에 저장 
      echo "<script>location.replace('index.php');</script>";   // index.php로 이동 --> 로그인 성공
      exit;
    }

    if($row == null){   // $row값이 존재하지 않는다면
      echo "<script>alert('로그인 실패 : 다시 입력하세요')</script>";   // alert(안내창) 메세지 출력
      echo "<script>location.replace('login.php');</script>";   // alert 확인 버튼 누르면 login.php로 이동 --> 로그인 실패 (대시보드 접근 불가)
      exit; 
    }
  ?>
</body>
</html>
