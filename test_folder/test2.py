import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
import pygrib
import datetime
import glob
import sys, os
import re

def lon_lat_to_cartesian(lon, lat, R=1):
    """
    Convert longitude and latitude to cartesian coordinates.

    Args:
        lon (np.array): Longitude values
        lat (np.array): Latitude values
        R (float): Radius for conversion

    Returns:
        tuple: x, y, z coordinates
    """
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)

    x = R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)

    return x, y, z

def calculate_weights_indices(xs, ys, zs, xt, yt, zt, k=4):
    """
    Calculate weights and indices using cKDTree.

    Args:
        xs, ys, zs (np.array): Source coordinates
        xt, yt, zt (np.array): Target coordinates
        k (int): Number of nearest neighbors

    Returns:
        tuple: Weights and indices
    """
    tree = cKDTree(np.column_stack((xs, ys, zs)))
    d, inds = tree.query(np.column_stack((xt, yt, zt)), k=k, workers=8)
    w = 1.0 / (d ** 2)
    return w, inds

def process_grib_files(gb2_files, w, inds, var_dict, var_list):
    """
    Process .gb2 files and extract required data.

    Args:
        gb2_files (list): List of grib files to process
        w (np.array): Weights for interpolation
        inds (np.array): Indices for interpolation
        var_dict (dict): Dictionary mapping variable names
        var_list (list): List of variable names

    Returns:
        pd.DataFrame: Processed data in DataFrame
    """
    df = pd.DataFrame(columns=pd.MultiIndex.from_product([var_list, ['p1', 'p2']]))
    for ii, file in enumerate(gb2_files):
        try:
            grbs = pygrib.open(file)
            for g in grbs:
                mapped_var = var_dict.get(g.parameterName)
                if mapped_var:
                    data = g.values
                    interpol_data = np.nansum(w * data.flatten()[inds], axis=1) / np.nansum(w, axis=1)
                    df.loc[ii, (mapped_var, 'p1')] = interpol_data[0]
                    df.loc[ii, (mapped_var, 'p2')] = interpol_data[1]
        except Exception as e:
            print(f"파일 처리 중 오류 발생: {file}, {e}")
    return df

def main(base_dir, time_st, time_ed):
    """
    각 디렉토리 내부의 .gb2 파일 처리
    """
    time_st = datetime.datetime.strptime(time_st, '%Y%m%d')
    time_ed = datetime.datetime.strptime(time_ed, '%Y%m%d')
    time = time_st

    # 출력 디렉토리 설정
    csv_dir = "./csv"
    os.makedirs(csv_dir, exist_ok=True)
    weights_file = os.path.join(base_dir, "w_inds.npz")

    # 가중치 및 인덱스 로드 또는 계산
    if os.path.exists(weights_file):
        w_inds = np.load(weights_file)
        w, inds = w_inds['w'], w_inds['inds']
    else:
        print("가중치 계산 중...")
        sample_file = glob.glob(os.path.join(base_dir, '**', '*.gb2'), recursive=True)[0]
        grb = pygrib.open(sample_file)[1]
        lat, lon = grb.latlons()
        xs, ys, zs = lon_lat_to_cartesian(lon.flatten(), lat.flatten())
        xt, yt, zt = lon_lat_to_cartesian([126.392, 128.04], [34.812, 36.14])
        w, inds = calculate_weights_indices(xs, ys, zs, xt, yt, zt)
        np.savez(weights_file, w=w, inds=inds)

    var_list = ['SWDIR', 'SWDIF', 'NDPCP', 'TCAR', 'TCAM', 'SNOAL', 'UGRD', 'VGRD', 'TMP', 'RH']
    var_dict = {
        "Large scale precipitation (non-convective)": "NDPCP",
        "Relative humidity": "RH",
        "197": "SNOAL",
        "199": "SWDIF",
        "198": "SWDIR",
        "213": "TCAM",
        "212": "TCAR",
        "Temperature": "TMP",
        "u-component of wind": "UGRD",
        "v-component of wind": "VGRD"
    }

    while time <= time_ed:
        time_str = time.strftime('%Y%m%d')
        for hh in ['00', '06', '12', '18']:
            sub_dir = os.path.join(base_dir, time_str[:6], time_str + hh)
            output_file = os.path.join(csv_dir, f"{time_str}{hh}.csv")

            # 이미 파일이 존재하면 다음 날짜로 넘어감
            if os.path.exists(output_file):
                print(f"이미 처리된 파일 : {output_file}")
                continue

            # .gb2 파일 탐색
            gb2_files = sorted(
                glob.glob(os.path.join(sub_dir, "*.gb2")),
                key=lambda x: int(re.search(r'h(\d+)', x).group(1)) if re.search(r'h(\d+)', x) else 0
            )

            if not gb2_files:
                print(f"파일이 존재하지 않음 : {sub_dir}")
                continue

            print(f"{time_str} {hh}시 처리 시작, 파일 개수: {len(gb2_files)}")

            # 파일 처리 및 저장
            df = process_grib_files(gb2_files, w, inds, var_dict, var_list)
            df.to_csv(output_file)
            print(f"저장 완료: {output_file}")

        time += datetime.timedelta(days=1)

if __name__ == "__main__":
    base_dir, time_st, time_ed = sys.argv[1:4]
    main(base_dir, time_st, time_ed)