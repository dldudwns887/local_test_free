import os,sys
import glob
import datetime
import pygrib
import numpy as np

def write_log(msg):
    f = open('error.log','a')
    f.write(msg+'\n')
    f.close()


def main(time_st, time_ed, hh):
    #test 용용
    #time_st = datetime.datetime(2024,7,1)
    #time_ed = datetime.datetime(2024,7,1)

    time_st = datetime.datetime.strptime(time_st,'%Y%m%d')
    time_ed = datetime.datetime.strptime(time_ed,'%Y%m%d')
    time = time_st
    time = time_st

    file_path = '../../TAR/'

    gribcode = [2,3,8,118,119,129,15,16,21,26]

    while time < time_ed:
        date = datetime.datetime.strftime(time,'%Y%m%d')
        files = glob.glob(file_path+f'*{date}{hh}*tar.gz')
        print(date)
        print(files)
        
        for i, file in enumerate(files):
            
            date2 = date+hh
            if os.path.exists(f'./ldps_unis_{date2}.tar.gz'):
                if os.path.getsize(f'./ldps_unis_{date2}.tar.gz') > 180000000:
                    print(f'./ldps_unis_{date2}.tar.gz exists, continue')
                    continue
            
            os.system(f'tar -zxf {file} -C ./tmp_ldps_files/')
            print(f'tar -zxf {file} -C ./tmp_ldps_files/')
            
            os.system(f'rm ./tmp_ldps_files/{date2}_tmp/*pres*')

            unis = glob.glob(f'./tmp_ldps_files/{date2}_tmp/*unis*{date2}.gb2')
            print('./tmp_ldps_files/{date2}/*unis*')

            for f in unis:
                print(f)
                
                df = pygrib.open(f)
                grbout = open(f[:-4] + '_swdr.gb2','wb')
                print(f)

                for code in gribcode:
                #print(len(df.select()))
                #print(code)
                    try:
                        grb = df.message(code)
                        msg = grb.tostring()
                        grbout.write(msg)
                    except:
                        print('error, continue')
                        msg = f'error! {f}'
                        write_log(msg)
                        print(msg)
                        continue
                grbout.close()
                df.close()
                #stop
            #print(unis)
            
            os.system(f'rm ./tmp_ldps_files/{date2}_tmp/*unis*{date2}.gb2')
            #os.system(f'rm ldps_unis_{date2}.tar.gz')
            os.system(f'mv ./tmp_ldps_files/{date2}_tmp ./tmp_ldps_files/{date2}')
            os.system(f'tar -zcf ldps_unis_{date2}.tar.gz ./tmp_ldps_files/{date2}')
            os.system(f'rm ./tmp_ldps_files/{date2}/*')

            #stop


        time += datetime.timedelta(1)


if __name__ == '__main__':
    argv = sys.argv
    time_st = str(argv[1])
    time_ed = str(argv[2])
    hh = str(argv[3])

    main(time_st,time_ed,hh)