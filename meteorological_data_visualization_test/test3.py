import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd


# 엑셀 파일 경로
file_path = "C:\\Users\\dldud\\Downloads\\[Hilow]202405_DT_0002.xls"

# 엑셀 파일을 읽어서 데이터프레임 생성
df = pd.read_excel(
    io=file_path,
    sheet_name="202405",  # 시트 이름
    index_col=3  # 3번째 열을 인덱스로 설정
)

# 데이터 확인
print(df.iloc[0:2])
#
df= df.drop(index=df.index[0:2])

print(df.iloc[0:2])