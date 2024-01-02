from numpy import *
def getLabel(path):
    distribution = path.split('/')[-1]
    a = open("input/result-" + str(distribution))

    Label0 = []
    for line in a:
        Label0 = line

    return Label0

def getfailedAndsucc(Label0):
    failed = []
    sign = 0
    for i in Label0:
        sign += 1
        if i == '1':
            failed.append(sign)

    succ = []
    sign = 0
    for i in Label0:
        sign += 1
        if i == '0':
            succ.append(sign)
    return failed, succ

def single(c, t, exline, coverage_file):
    NUS = 0; NUF = 0; NCS = 0; NCF = 0
    table = zeros((exline, 10))
    k = 0

    allTests = coverage_file.keys()
    currentTest = allTests[c - 1]
    currentTest_coverage = coverage_file[currentTest]

    order = 1
    for hit in currentTest_coverage:
        if t == 1:
            if hit == 0:
                NUF += 1
            else:
                NCF += 1
        else:
            if hit == 0:
                NUS += 1
            else:
                NCS += 1
        NC = NCF + NCS
        NS = NCS + NUS
        NU = NUS + NUF
        NF = NCF + NUF
        N = NC + NU

        table[k, :] = [order, NCS, NCF, NUS, NUF, NC, NS, NU, NF, N]
        NUS = 0; NUF = 0; NCS = 0; NCF = 0
        k += 1
        order += 1
    return table