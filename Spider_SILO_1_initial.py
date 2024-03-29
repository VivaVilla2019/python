import requests, os
import csv
import pandas as pd

lat = str(input('latitude(eg.-30.00):'))
lon = str(input('longitude(eg.135.00):'))
start = int(input('start(eg.20160101):'))
finish = int(input('finish(eg.20160105):'))
username = str(input('username(eg.1059571137846140675):'))
variables = str(input('''variables:
R for daily_rain;
X,N for max_temp and min_temp;
V,D for vp and vp_deficit;
E,S,C for evap_pan,evap_syn,evap_comb,evap_morton_lake;
J for radiation;
H,G for rh_tmax and rh_tmin;
F,T,A,P,W for et_short_crop,et_tall_crop,et_morton_actual,et_morton_potential,et_morton_wet;
M for mslp;
'''))

# 如果想输出所有变量，则去掉variables和comment=部分
api_url = 'https://www.longpaddock.qld.gov.au/cgi-bin/silo'
params = 'format=json&lat=%s&lon=%s&start=%s&finish=%s&comment=%s&username=%s&password=silo'%(lat,lon,start,finish,variables,username)
url =  api_url + '/DataDrillDataset.php?' + params

def get_data():
    req = requests.get(url).json()
    location_dict = req.get('location')
    location = location_dict.items()
    items = req.get('data')
    
#"data": 
#[{"date": "2016-01-01","variables": [{"source": 25,"value": 0,"variable_code": "daily_rain"}]},
# {"date": "2016-01-02","variables": [{"source": 25,"value": 0,"variable_code": "daily_rain"}]},
# {"date": "2016-01-03","variables": [{"source": 25,"value": 0,"variable_code": "daily_rain"}]}]
    
    param = []
    for i in range(len(items)):
        date = items[i].get('date')
        variables = items[i].get('variables')
        var1 = []
        var2 = []
        for j in range(len(variables)):
            variables_value = variables[j].get('value')
            variable_code = variables[j].get('variable_code')     
            var1.append(variable_code)
            var2.append(variables_value)
        param.append([date,*var2])
    return location,param,var1

def save_data():
    headers = ['date',*get_data()[2]]
    with open(r'C:\Users\Viva Villa\Desktop\data.csv', 'w') as f:
        f_csv = csv.writer(f)
        #f_csv.writerow(get_data()[0])
        f_csv.writerow(headers)
        f_csv.writerows(get_data()[1])
        
if __name__ == '__main__':  
    save_data()


# 整理data.csv之后得到output.csv文件
csv_file = r'C:\Users\Viva Villa\Desktop\data.csv'
csv_data = pd.read_csv(csv_file,low_memory = False)
csv_df = pd.DataFrame(csv_data)
csv_df.to_csv(r'C:\Users\Viva Villa\Desktop\output.csv')     

# 打开output.csv文件
with open(r'C:\Users\Viva Villa\Desktop\output.csv','rt') as f:
    reader = csv.reader(f,delimiter=',')        # 以逗号问分隔符按列读出数据
    table = [row for row in reader]
    table1 = list(map(list,zip(*table)))
# 实现行列转换得到output1.csv文件    
with open(r'C:\Users\Viva Villa\Desktop\output1.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(table1)
# 调整格式得到output2.csv文件
csv_file = r'C:\Users\Viva Villa\Desktop\output1.csv'
csv_data = pd.read_csv(csv_file,low_memory = False)
csv_df = pd.DataFrame(csv_data)
csv_df.to_csv(r'C:\Users\Viva Villa\Desktop\output2.csv')     
