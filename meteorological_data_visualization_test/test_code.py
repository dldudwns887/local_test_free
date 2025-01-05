import matplotlib.pyplot as plt

# 2 개의 리스트 추가
a = [1,2,3,4,5]
b = [2,3,4,5,6]

# 간단한 직선 그래프 표시
plt.plot(a,b) #x,y 축
plt.show()

# 그림 저장 방식, dpi는 사진 품질
plt.savefig("경로", dpi=300)