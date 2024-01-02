from Phase4.k_medoids import kmedoidsCluster
import sqlite3
if __name__ == "__main__":
    failed = []
    db_base_path = "../runningExample_code/output/"
    conn = sqlite3.connect(db_base_path+"variableInformation.db")
    cursor = conn.cursor()
    sql = "select id from testcase where all_result = '1'"
    cursor.execute(sql)
    for c in cursor:
        failed.append(c[0])
    kmedoidsCluster(db_base_path, failed, "ReClues", 2)