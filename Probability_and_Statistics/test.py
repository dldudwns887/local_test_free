import numpy as np
import pandas as pd

# 데이터 생성
# 이산형 양적 변수: 주사위의 눈
np.random.seed(42)  # 재현성을 위해
rolls = np.random.randint(1, 7, size=1000)  # 주사위 1000번 굴리기

# 연속형 양적 변수: 키 (단위: cm)
heights = np.random.normal(loc=170, scale=10, size=1000)  # 평균 170, 표준편차 10

# 범주형 변수: 음식 종류
foods = np.random.choice(['짜장면', '짬뽕', '우동', '볶음밥'], size=1000, p=[0.4, 0.3, 0.2, 0.1])

# 데이터프레임 생성
data = pd.DataFrame({
    '주사위 눈': rolls,
    '키(cm)': heights,
    '음식 종류': foods
})

# 통계량 계산
# 1. 이산형 양적 변수: 주사위 눈
roll_stats = data['주사위 눈'].describe()
roll_counts = data['주사위 눈'].value_counts().sort_index()

# 2. 연속형 양적 변수: 키
height_stats = data['키(cm)'].describe()

# 3. 범주형 변수: 음식 종류
food_counts = data['음식 종류'].value_counts()

# 결과 출력
print("주사위 눈 통계량:")
print(roll_stats)
print("\n주사위 눈 빈도수:")
print(roll_counts)

print("\n키 통계량:")
print(height_stats)

print("\n음식 종류 빈도수:")
print(food_counts)