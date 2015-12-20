import csv

def get_backup_pose(filename):
    p = []
    r = csv.DictReader(open(filename,'r'),delimiter = ';')
    for row in r:
        p.append(row)
    a = {}
    a['CSVPath'] = p[0]["CSVPath"]
    a['cursor'] = int(p[0]["cursor"])
    
    return a
    
def set_backup_pose(filename,dict):
    f = open(filename,'w')
    r = csv.DictWriter(f,delimiter = ';',lineterminator = '\n',fieldnames=["CSVPath","cursor"])
    r.writeheader()
    r.writerow(dict)
    f.close()
    
if __name__ == '__main__':
    a = {"CSVPath":"toto","cursor":5}
    set_backup_pose("test.csv",a)
    
    b = get_backup_pose("test.csv")
    print b