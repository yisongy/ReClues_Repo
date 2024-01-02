import pickle as pkl
from numpy import *
from Phase1.getSpectrum import *
import os
from DB import DB
import xlsxwriter
def exeDStar(path, failed, succ):
    with open(path, 'rb') as f:
        coverage_file = pkl.load(f)
    exline = coverage_file.shape[0]

    succ_table_sum = zeros((exline, 10))
    for succ_number in succ:
        succ_table = single(succ_number, 0, exline, coverage_file)
        succ_table_sum[:, 1:] += succ_table[:, 1:]

    table_sum = succ_table_sum
    for failed_number in failed[:-1]:
        failed_table = single(failed_number, 1, exline, coverage_file)
        table_sum[:, 1:] += failed_table[:, 1:]

    table_sum += single(failed[-1], 1, exline, coverage_file)

    ranking = OTH13_dstar(table_sum,exline)
    return ranking, coverage_file.index.values.tolist(), coverage_file.columns.values.tolist()

def OTH13_dstar(table_sum,exline):
    ranking = zeros((exline, 3))
    i = 0
    for line in table_sum:
        line = mat(line).flatten().A[0]
        ranking[i, 1] = line[0]
        fz = pow(line[2], 2)
        fm = line[4] + line[1]
        ranking[i, 2] = fz / fm

        i += 1
    ranking = ranking[ranking[:, 2].argsort()[::-1]]
    for i in range(0, exline):
        ranking[i, 0] = i + 1
    return ranking

def custom_sort(row):
    return (-row[2], row[1])

def get_spectrum(db_base_path):
    cov_file_path = db_base_path + "input/Example.csv"
    home_path = os.getcwd()
    os.chdir(db_base_path)
    Label0 = getLabel(cov_file_path)
    failed, succ = getfailedAndsucc(Label0)
    ranking, row_index, column_index = exeDStar(db_base_path+'input/example.pkl', failed, succ)
    break_points = {}
    ranking = sorted(ranking, key=custom_sort)
    for i in range( len(ranking) ):
        tmp = eval(row_index[ (int)(ranking[i][1])-1 ])
        s = tmp[0]
        break_points[ s + ":" + str(int(tmp[1])) ] = ranking[i][2]
    os.chdir(home_path)
    f = xlsxwriter.Workbook(db_base_path + "output/suspiciousness.xls")
    sheet1 = f.add_worksheet(u'sheet1')
    dict_row = 0
    for k, v in break_points.items():
        sheet1.write(dict_row, 0, k)
        sheet1.write(dict_row, 1, v)
        dict_row += 1
    f.close()
    return


def get_bps(db_base_path):
    cov_file_path = db_base_path + "input/Example.csv"
    db_file_path = db_base_path + "output/variableInformation.db"
    home_path = os.getcwd()
    os.chdir(db_base_path)
    Label0 = getLabel(cov_file_path)
    failed, succ = getfailedAndsucc(Label0)
    ranking, row_index, column_index = exeDStar(db_base_path+'input/example.pkl', failed, succ)
    db = DB(db_file_path)
    break_points = {}
    bp_value = []
    ranking = sorted(ranking, key=custom_sort)
    for i in range( int(len(ranking)*0.1)+1 ):
        tmp = eval(row_index[ (int)(ranking[i][1])-1 ])
        s = tmp[0]
        break_points[ s + ":" + str(int(tmp[1])) ] = i+1
        bp_value.append( (s, "process", str(int(tmp[1])), ranking[i][2]) )
    sqlcmd = "insert into breakpoint(className, method, lineNumber, suspiciousValues) values (?, ?, ?, ?);"
    db.executeMany(sqlcmd, bp_value)
    db.closeDB()
    os.chdir(home_path)
    return break_points

def get_failed_testcases(db_base_path):
    failed_testcases = []
    db_path = db_base_path + "/output/variableInformation.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    db = DB( db_path )
    db.conn.commit()
    for i in range(1, 7):
        if i <= 4:
            db.insertTestcase("exampleTest.exampleTest.testCase"+str(i))
        else:
            db.insertTestcase("exampleTest.exampleTest.testCase"+str(i))
        failed_testcases.append("exampleTest.exampleTest.testCase"+str(i))
    return failed_testcases, db