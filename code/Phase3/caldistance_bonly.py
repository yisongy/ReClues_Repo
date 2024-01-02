import os
import sqlite3
import xlsxwriter

OUTPATH = "your outpath"
BREAKPOINT_PERCENTAGE = 0.1

def StrDistance(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    set1.discard('"')
    set2.discard('"')
    intersection = 0
    for s1 in set1:
        if s1 in set2:
            intersection += 1
    union = len(set1) + len(set2) - intersection

    distance = 1 - round(intersection / union, 2)
    return distance

def BPDistance(bp1, bp2):
    allvariable = []
    samevariable = []

    bp1message = eval(bp1)
    bp2message = eval(bp2)

    for key in bp1message.keys():
        allvariable.append(key)
    for key in bp2message.keys():
        if not key in allvariable:
            allvariable.append(key)
        else:
            samevariable.append(key)

    if len(allvariable) == 0:
        return 1
    distance = 1 - len(samevariable) / len(allvariable)
    return distance

def CalDistance(allbp1, allbp2):
    allkeys = []
    for key in allbp1.keys():
        allkeys.append(key)
    for key in allbp2.keys():
        if not key in allkeys:
            allkeys.append(key)
    if len(allkeys) == 0:
        return 1

    i = 0
    totaldistance = 0
    div = len(allkeys)
    for bp in allkeys:
        if not (allbp1.__contains__(bp)) or not (allbp2.__contains__(bp)):
            totaldistance += 1
            i += 1
            continue
        totaldistance += BPDistance(allbp1[bp], allbp2[bp])
        i += 1
    if div == 0:
        return 1
    distance = totaldistance / div
    return distance

def SingleVersion(inpath, outpath):
    distanceFile = outpath + OUTPATH
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    failed = []
    conn = sqlite3.connect(inpath)
    cursor = conn.cursor()
    sql = "select id from testcase where all_result = '1'"
    cursor.execute(sql)
    for c in cursor:
        failed.append(c[0])
    m = len(failed)
    distance_dict = {}

    allbp = []
    cursor = conn.cursor()
    sql = "select bp_id from bp_tc order by bp_id"
    cursor.execute(sql)
    for c in cursor:
        if len(allbp) == 0 or c[0] != allbp[len(allbp) - 1]:
            allbp.append(c[0])
    mid = allbp[int(len(allbp) * BREAKPOINT_PERCENTAGE)]

    for i in range(0, m):
        locals()[failed[i]] = {}
    cursor = conn.cursor()
    sql = "select bp_id,val,tc_id from bp_tc"
    cursor.execute(sql)
    for c in cursor:
        if c[0] <= mid:
            locals()[c[2]][c[0]] = c[1]

    for i in range(0, m):
        for j in range(i + 1, m):
            dis = CalDistance(locals()[failed[i]], locals()[failed[j]])
            distance_dict['t' + str(failed[i]) + '_t' + str(failed[j])] = dis
            distance_dict['t' + str(failed[j]) + '_t' + str(failed[i])] = dis
    for i in range(0, m):
        distance_dict['t' + str(failed[i]) + '_t' + str(failed[i])] = 0
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    f = xlsxwriter.Workbook(distanceFile)
    sheet1 = f.add_worksheet(u'sheet1')
    dict_row = 0
    for k, v in distance_dict.items():
        sheet1.write(dict_row, 0, k)
        sheet1.write(dict_row, 1, v)
        dict_row += 1
    f.close()