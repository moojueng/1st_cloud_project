<?php 
session_start();    // 로그인 상태를 유지하기 위해 세션을 시작함

if(!isset($_SESSION['username'])){    // isset() : 설정된 변수인지 확인하는 함수
  echo "<script>location.replace('login.php');</script>";   // username(사용자)이 확인되지 않았으면 로그인 페이지로 이동
} else {    // 사용자가 확인됐을 때
  $username = $_SESSION['username'];    // 세션을 변수에 저장 --> 관리자 이름 띄우기 위한 용도 
}

include 'config.php'  // 데이터베이스 연결
?>
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">    <!-- 반응형 페이지 만들 때 필요함 -->
  <title> 전자 명부 대시보드 </title>

  <!-- favicon -->
  <link rel="icon" href="./favicon.png" type="image/x-icon" />      <!-- title 옆에 보이는 작은 아이콘 적용 -->

  <!-- CSS Link -->
  <link rel="stylesheet" href="./assets/bootstrap.css">
  <link rel="stylesheet" href="./assets/bootstrap-icons.css">
  <link rel="stylesheet" href="./assets/custom.min.css">
  <link rel="stylesheet" href="./assets/prism-okaidia.css">
  <link rel="stylesheet" href="./assets/_variables.scss">
  <link rel="stylesheet" href="./assets/_bootswatch.scss">

  <!-- Font Awesome --> 
	<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet" />

  <!-- Bootstrap Datepicker --> 
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker3.min.css">
  
  <!-- Datatable -->
  <link href="https://cdn.datatables.net/1.10.18/css/dataTables.bootstrap4.min.css" rel="stylesheet">


  <!-- JS LInk -->
  <!-- jQuery -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
  
  <!-- Datatable -->
  <script src="https://cdn.datatables.net/1.10.18/js/jquery.dataTables.min.js"></script>
  
  <!-- Popper -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  
  <!-- Bootstrap Datepicker -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/locales/bootstrap-datepicker.ko.min.js"></script>
  
  <!-- Bootstrap pagination -->
  <script src="https://cdn.datatables.net/1.10.18/js/dataTables.bootstrap4.min.js"></script>
  
  <!-- Templates -->
  <link rel="stylesheet" href="./assets/bootstrap.bundle.min.js">
  <link rel="stylesheet" href="./assets/prism.js">
  <link rel="stylesheet" href="./assets/custom.js">


  <!-- Custom -->
  <style>
    /*  Font  */
    @font-face {
      font-family: 'NanumBarunGothic';
      font-style: normal;
      font-weight: 400;
      src: url('//cdn.jsdelivr.net/font-nanumlight/1.0/NanumBarunGothicWeb.eot');
      src: url('//cdn.jsdelivr.net/font-nanumlight/1.0/NanumBarunGothicWeb.eot?#iefix') format('embedded-opentype'), url('//cdn.jsdelivr.net/font-nanumlight/1.0/NanumBarunGothicWeb.woff') format('woff'), url('//cdn.jsdelivr.net/font-nanumlight/1.0/NanumBarunGothicWeb.ttf') format('truetype');
    }

    body {
      font-family: 'NanumBarunGothic';
      background: linear-gradient(to bottom, #A0B8C5 146px, #EEF2F3 546px);
    }


    /* Datatable */
    /* 표시 건수수 설정 */
    div.dataTables_length {
      text-align : left !important;
      font-size: 12px;
    }

    /* 필터링 (검색) */
    div.dataTables_filter {
      text-align : right !important;
      font-size: 12px;
    }
    div.dataTables_filter input { 
      width: 140px !important; 
    }
    
    /* 데이터 정보 */
    div.dataTables_info {
      text-align : left !important;
      font-size: 12px;
    }

    /* 페이지네이션 */
    div.dataTables_paginate {
      text-align : right !important;
      font-size: 12px;
      padding-top: 5px;
    }

    /* 테이블 수평 중앙 정렬 */
    table.dataTable td {
      vertical-align: middle;
    }

    /* 테이블 행 높이 조절 */
    .table td {
      padding: 5px;
    }
  </style>

</head>
<body>
<!-- header -->
<header class="container">    <!-- 부트스트랩은 class속성에 요소를 입력하여 스타일 지정. container : 작업 영역 설정 (가운데 정렬됨) -->
  <div class="row d-flex justify-content-end">    <!-- row: 컨텐츠영역인 col을 감싸는 요소. d-flex: 자기자신은 block, 자식요소는 inline 속성으로 변환. justify-content-end: 컨텐츠 오른쪽 정렬  -->
    <div class="col-3 col-sm-2"  style="padding: 0;">   <!-- col-3: 뷰포트 xs 크기에서 12영역 중 3영역만큼 자리 차지. col-sm-2: 뷰포트 sm 크기에서 2영역만큼 자리 차지 -->
      <p class="" style="font-size:13px; line-height: 50px; text-align: right; margin:0"><?php echo "관리자 : $username"; ?></p>
    </div>
    <div class="col-3 col-sm-1" style="font-size: 12px; line-height: 50px; height:50px;">
      <button type="button" class="btn btn-sm" style="font-size:12px;" onclick="location.href='logout.php'">LOGOUT</button>   <!-- 로그아웃 버튼 누르면 logout.php 파일 불러옴 -->
    </div>
  </div>
</header>
<!-- header end -->
<!-- contents -->
<div class="container"  style="margin-top: 50px" >
  <div class="bs-docs-section">
    <div class="row">
      <div class="page-header">
        <h1 id="tables">Tables</h1>
        <div class="row d-flex justify-content-end" style="margin: 20px 0;">
          <!-- search: from date -->
          <div class="col-12 col-md-4 col-lg-3 mb-2" style="padding: 0 5px 0 0; box-sizing: border-box;">
            <form class="">
              <div class="input-group date" id="picker1">
                <input type="text" class="form-control" id="from_date" placeholder="FROM DATE"/>
                <span class="input-group-append" style="cursor: pointer;">
                  <span class="input-group-text bg-light d-block">
                    <i class="fa fa-calendar"></i>
                  </span>
                </span>
              </div>
            </form>
          </div>

          <!-- search: to date -->
          <div class="col-12 col-md-4 col-lg-3 mb-2" style="padding: 0 5px 0 0; box-sizing: border-box;">
            <form class="">
              <div class="input-group date" id="picker2" >
                <input type="text" class="form-control" id="to_date" placeholder="TO DATE"/>
                <span class="input-group-append" style="cursor: pointer;">
                <span class="input-group-text bg-light d-block">
                  <i class="fa fa-calendar"></i>
                </span>
                </span>
              </div>
            </form>
          </div>

          <!-- search button -->
          <div class="col col-lg-2 d-grid p-0" style="height: 50px; margin-right: 5px; box-sizing: border-box;">
            <button type="button" id="search" class="btn btn-primary btn-block">Search</button>
          </div>
          
          <!-- search button(all) -->
          <div class="col col-lg-1 d-grid p-0" style="height: 50px; margin-right: 0">
            <button type="button" class="btn btn-primary btn-block" onClick="window.location.reload()">All</button>
          </div>            
        </div>

        <!-- table start (datatable 라이브러리 이용) -->
        <div class="bs-component">
          <table class="table table-hover table-light display dataTable text-center" id="dbtable" style="font-size: 0.8em;">
            <thead>
              <tr>
                <th>No</th>
                <th>Date</th>
                <th>Time</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Addr</th>
                <th>Gender</th>
                <th>Temp</th>
                <th>Accuracy</th>
                <th>Image</th>
              </tr>
            </thead>
          </table>
        </div>
        <!-- table end -->
      </div>
    </div>
  </div>

  <!-- chart -->
  <div class="bs-docs-section" style="margin-top: 30px">
    <!-- pie chart start  -->
    <div class="row">
      <h1 style="color: ">chart</h1>
      <!-- 방문자 수 (total, today) -->
      <div class="col-md-12 col-lg-4">
        <iframe src="http://20.200.184.152:3000/d-solo/g1gFgyw7k/dashboard-img?orgId=1&refresh=5m&from=1651613292113&to=1651634892113&theme=light&panelId=8" width="100%" height="300" frameborder="0"></iframe>
      </div>
      <!-- 외부인 출입 비율 (등록, 미등록) -->
      <div class="col-md-12 col-lg-4">
        <iframe src="http://20.200.184.152:3000/d-solo/g1gFgyw7k/dashboard-img?orgId=1&refresh=5m&from=1651430034177&to=1651451634178&theme=light&panelId=10" width="100%" height="300" frameborder="0"></iframe>
      </div>
      <!-- 정상 체온 비율 (정상, 고열 ) -->
      <div class="col-md-12 col-lg-4">
        <iframe src="http://20.200.184.152:3000/d-solo/g1gFgyw7k/dashboard-img?orgId=1&refresh=5m&from=1651429995128&to=1651451595129&theme=light&panelId=6" width="100%" height="300" frameborder="0"></iframe>
      </div>
    </div>
    <!-- pie chart end -->
  </div>

  <div class="bs-docs-section" style="margin-top: 30px">
    <!-- time series graph start -->
    <div class="row">
      <!-- 시간대별 체온 (시계열 꺾은선) -->
      <div class="col-12">
        <iframe src="http://20.200.184.152:3000/d-solo/g1gFgyw7k/dashboard-img?orgId=1&refresh=5m&theme=light&panelId=2" width="100%" height="300" frameborder="0"></iframe>
      </div>
      <!-- 체온 분포표 (시계열 히트맵) -->
      <div class="col-12">
        <iframe src="http://20.200.184.152:3000/d-solo/g1gFgyw7k/dashboard-img?orgId=1&theme=light&panelId=11" width="100%" height="300" frameborder="0"></iframe>
      </div>
    </div>
    <!-- time series graph end -->
  </div>
</div>
<!-- footer -->
<div style="background: #888; height: 80px; text-align: right; margin-top: 50px;">
  <p style="font-size: 12px; color: #fff; margin-right: 10px; padding-top: 10px">© 2022 한국직업능력교육원 클라우드반 Project B조</p>
</div>
<!-- footer end -->

<!-- Script -->
<script>
  const today = new Date();     // today 변수에 오늘의 날짜 저장

  $(document).ready(function(){
    // Datepicker
    $("#picker1").datepicker({    // id가 picker1인 태그에 datepicker 적용
      format: "yyyy-mm-dd",       // 날짜 속성
      autoclose: true,            // 날짜 선택하면 선택창 자동으로 닫힘
      endDate: today,             // 미래 날짜 선택 방지
      clearBtn: true,             // 선택한 날짜 삭제
      showWeekDays: true,         // 요일 표시
      todayHighlight: true,       // 오늘 날짜 강조
      todayBtn: "linked",         // 버튼 누르면 오늘 날짜 선택됨 
      toggleActive: true,         // 선택한 날짜 한번 더 클릭해서 해제 가능 (토글)
      language: 'ko',             // 한국어 설정
    }).on('changeDate', function(selected){     // changeDate: 날짜가 변경되면 호출되는 이벤트
      var startDate = new Date(selected.date.valueOf());    // startDate에 선택된 날짜를 저장
      $('#picker2').datepicker('setStartDate', startDate);  // #picker2는 startDate에 저장한 날짜부터 선택 가능
    }).on('clearDate', function(selected){      // clearDate: clear 버튼 누르면 호출되는 이벤트
      $('#picker2').datepicker('setStartDate', null);       // #picker2 시작 날짜 제한 X
    });

    $("#picker2").datepicker({
      format: "yyyy-mm-dd",
      autoclose: true,
      endDate: today,
      clearBtn: true,
      showWeekDays: true,
      todayHighlight: true,
      todayBtn: "linked",
      toggleActive: true,
      language: 'ko'
    }).on('changeDate', function(selected){
      var endDate = new Date(selected.date.valueOf());      // endDate에 선택된 날짜 저장
      $('#picker1').datepicker('setEndDate', endDate);      // #picker1 endDate에 저장한 날짜까지만 선택 가능
    }).on('clearDate', function(selected){
      $('#picker1').datepicker('setEndDate', null);         // #picker1 끝날짜 제한 X
    });


    // DataTable
    var dataTable = $('#dbtable').DataTable({      // #dbtable에 datatable 적용
      'processing': true,   // 서버와 통신할 때 응답을 받기 전이라는 ui를 띄울것인지 여부
      'serverSide': true,   // 서버와의 통신 여부, ajax로 서버 데이터 처리
      'serverMethod': 'post',   // 데이터는 post로 넘겨받음
      'order': [[0, 'desc']],   // 인덱스가 0번인 열에 해당하는 데이터 desc(내림차순) 정렬 
      'responsive': true,       // 반응형 true
      'lengthMenu': [ [10, 20, 50, 100], [10, 20, 50, 100] ],   // 데이터 정렬 개수 설정 [[정렬개수][텍스트]]
      'pageLength': 20,   // 한페이지에 20개씩 정렬 고정
      'searching': true,  // 검색 기능
      'autoWidth': false, // 가로 길이 자동 설정
      'scrollX': true,    // 가로 스크롤
      'pagingType': 'simple_numbers',   // 페이지네이션 타입 설정
      'ajax': {
        'url': 'filter.php',    // filter.php로부터 데이터를 넘겨받음
        'data': function(data){
          // Read values
          var from_date = $('#from_date').val();    // 날짜 검색을 위한 변수 설정
          var to_date = $('#to_date').val();

          // Append to data
          data.searchByFromdate = from_date;    // 위에서 저장한 날짜를 data에 추가
          data.searchByTodate = to_date;
        }
      },
      language: {   // 언어 설정 (안하면 영어로 나옴)
        emptyTable: "데이터가 없습니다.",
        lengthMenu: "페이지당 _MENU_ 개씩 보기",
        info: "현재 _START_ - _END_ / _TOTAL_건",
        infoEmpty: "데이터 없음",
        infoFiltered: "( _MAX_건의 데이터에서 필터링됨 )",
        zeroRecords: "일치하는 데이터가 없습니다.",
        loadingRecords: "로딩중...",
        processing: "잠시만 기다려 주세요.",
      },
      'columns': [  // tbody에 들어갈 리스트. filter.php $data[]로 넘겨받은 값
        { data: 'No'},
        { data: 'Date'},
        { data: 'Time'},
        { data: 'person_name'},
        { data: 'phone_num'},
        { data: 'addr'},
        { data: 'sex'},
        { data: 'temperature'},
        { data: 'accuracy'},
        { data: 'img'}
      ],
      'dom': "<'row'<'col-5'l><'col-7'f>>" + "<'row'<'col-12'i>t<'col-12'p>>",    // l : length, f: filter, i: info, t: table, p: paging 순서 및 자리 배치
    });


    // Search button
    $('#search').click(function(){
      dataTable.draw();   // search버튼 누르면 조건에 맞는 테이블 재생성
    });
  });

</script>
</body>
</html>
