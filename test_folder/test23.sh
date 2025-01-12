# Conda로 설치 가능한 패키지 설치
conda install -n <가상환경이름> \
    numpy=1.26.0 \
    pandas=2.1.3 \
    matplotlib=3.8.0 \
    seaborn=0.13.2 \
    scikit-learn=1.6.0 \
    sqlalchemy=1.4.49 \
    django=5.0.4 \
    requests=2.31.0 \
    boto3=1.34.145 \
    -y

# Conda로 설치 불가능한 패키지 pip로 설치
pip install \
    folium==0.17.0 \
    django-ebhealthcheck==2.0.2 \
    selenium==4.19.0
