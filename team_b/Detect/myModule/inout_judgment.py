def inout(temper, idx):
    if idx == 4:#미등록 인원일때 상태 표기
        if temper > 37.5:   return '4'
        else:   return '3'

    else:#등록 인원일때 상태 표기
        if temper > 37.5:   return '2'
        else:   return '1' #전에 상태가 in이였으면 out
