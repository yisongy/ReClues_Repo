import xlrd
from numpy import *
import numpy as np
import xlsxwriter
def kmedoidsCluster(versionDir, failed, formula, k):
    m = len(failed)

    read_distanceDict = {}
    distance_list = []
    table = xlrd.open_workbook(versionDir+'distance.csv').sheets()[0]
    row = table.nrows
    for key in range(row):
        read_distanceDict[table.row_values(key)[0]] = table.row_values(key)[1]

    distances = {}
    for i in range(row):
        distances[table.row_values(i)[0]] = table.row_values(i)[1]
    for i in range(m):
        for j in range(i+1,m):
            distance_list.append(distances['t' + str(int(failed[i])) + '_t' + str(int(failed[j]))])

    centroids = ['1', '6']

    clusterAssment = mat(zeros((m, 2)))
    medoidsChanged_sign = True
    z = 1
    while medoidsChanged_sign:
        medoidsChanged_sign = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = read_distanceDict['t' + str(failed[i]) + '_t' + str(centroids[j])]

                if distJI < minDist:
                    minDist = distJI
                    minIndex = j

            clusterAssment[i, :] = failed[i], minIndex

        medoidsChanged_num = 0
        currentChanged = 0
        for cent in range(k):
            ptsInClust = np.array(failed)[nonzero(clusterAssment[:, 1].A == cent)[0]]

            sumMin = 0
            for otherPoint in ptsInClust:
                sumMin += read_distanceDict['t' + str(centroids[cent]) + '_t' + str(otherPoint)]

            for newMedoids_candidate in ptsInClust:
                sumReplace = 0
                for otherPoint in ptsInClust:
                    sumReplace += read_distanceDict['t' + str(newMedoids_candidate) + '_t' + str(otherPoint)]

                if sumReplace < sumMin:
                    sumMin = sumReplace
                    centroids[cent] = str(newMedoids_candidate)
                    medoidsChanged_sign = True
                    currentChanged = 1
            medoidsChanged_num += currentChanged
            currentChanged = 0
        z += 1


    f = xlsxwriter.Workbook(versionDir + formula + '_clustering.xls')
    sheet1 = f.add_worksheet(u'sheet1')
    [h, l] = clusterAssment.shape
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, clusterAssment[i, j])
    f.close()
    return clusterAssment