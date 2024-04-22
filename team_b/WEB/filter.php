<?php 
include 'config.php';   // 데이터베이스 연결

## Read value
$draw = $_POST['draw'];   
$row = $_POST['start'];   
$rowperpage = $_POST['length'];   // Rows display per page
$columnIndex = $_POST['order'][0]['column'];  // Column index
$columnName = $_POST['columns'][$columnIndex]['data']; // Column name
$columnSortOrder = $_POST['order'][0]['dir']; // asc or desc
$searchValue = mysqli_real_escape_string($con, $_POST['search']['value']);  // 검색할 데이터
// mysqli_real_escape_string: 입력창에 delete나 drop등의 명령어를 입력했을 경우 DB 데이터가 손실될 가능성이 있어서 escape상태로 만들어주는 함수

## Date search value --> post로 넘겨받은 값을 변수에 저장
$searchByFromdate = mysqli_real_escape_string($con, $_POST['searchByFromdate']);  
$searchByTodate = mysqli_real_escape_string($con, $_POST['searchByTodate']);

## Search --> 검색할 단어가 입력되면 searchQuery변수에 sql문 저장
$searchQuery = "";
if($searchValue != ''){
    $searchQuery = " and (Date like '%".$searchValue."%' or person_name like '%".$searchValue."%' or phone_num like'%".$searchValue."%' or state like '%".$searchValue."%' ) ";
} 

## Date filter --> 검색할 날짜가 입력되면 searchQeury변수에 sql문 저장
if($searchByFromdate != '' && $searchByTodate != ''){
  $searchQuery .= " and (Date between '".$searchByFromdate."' and '".$searchByTodate."') ";
}

## Total number of records without filtering --> 검색기능을 사용안할때는 DB에 저장된 모든 데이터의 행 개수를 보여줌
$sel = mysqli_query($con,"select count(*) as allcount from electronic_list");
$records = mysqli_fetch_assoc($sel);
$totalRecords = $records['allcount'];

## Total number of records with filtering --> 검색기능을 사용할때는 검색 조건에 맞는 데이터의 행 개수를 보여줌
$sel = mysqli_query($con,"select count(*) as allcount from electronic_list WHERE 1 ".$searchQuery);
$records = mysqli_fetch_assoc($sel);
$totalRecordwithFilter = $records['allcount'];

## Fetch records --> 최종 sql실행문
$tbQuery = "select * from electronic_list WHERE 1 ".$searchQuery." order by ".$columnName." ".$columnSortOrder." limit ".$row.",".$rowperpage;
$tbRecords = mysqli_query($con, $tbQuery);
$data = array();

while ($row = mysqli_fetch_assoc($tbRecords)) {     // 쿼리 실행 결과를 $row변수에 저장
  $data[] = array(
    "No" => $row['No'],     // key값=>value값 (value값을 key값에 저장한다고 생각하면 됨)
    "Date" => $row['Date'], // key: [index.php] 파일 - <script> - dataTable - column - data에서 사용됨
    "Time" => $row['Time'],
    "person_name" => $row['person_name'],
    "phone_num" => $row['phone_num'],
    "addr" => $row['addr'],
    "sex" => $row['sex'],
    "temperature" => $row['temperature'],
    "accuracy" => $row['accuracy'],
    "img" => '<img src="data:image/jpeg;base64,'.base64_encode($row['img']).'" />',
  );
}

## Response --> 결과 전송
$response = array(
  "draw" => intval($draw),
  "iTotalRecords" => $totalRecords,
  "iTotalDisplayRecords" => $totalRecordwithFilter,
  "aaData" => $data
);

echo json_encode($response);
die;

?>
