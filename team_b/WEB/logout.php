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
  session_destroy();  // 세션 종료

  echo "<script> location.replace('index.php'); </script>"    // index.php로 이동
?>
</body>
</html>
