import matplotlib.pyplot as plt
from matplotlib import rc
#한글깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

name = ["활석","석고","방해석","형석","인회석","정장석","석영","황옥","강옥","금강석"]
b = [1,2,9,21,48,72,100,200,400,1500]

plt.xlabel("광물 이름")
plt.ylabel("광물의 절대 굳기")
plt.title("모스 굳기계 광물의 절대 굳기")

plt.plot(name,b)
plt.show()