import sqlite3

class DB:
    def __init__(self, db_filename):

        self.conn = sqlite3.connect(db_filename)
        self.conn.text_factory = str
        self.conn.isolation_level = None

        self.execute("create table if not exists breakpoint(id integer primary key, className TEXT, method TEXT, lineNumber integer,  suspiciousValues real)")
        self.execute("create table if not exists testcase(id integer primary key autoincrement, tc_name TEXT, all_result integer)")
        self.execute("create table if not exists bp_tc(id integer primary key autoincrement, bp_id integer, lineNumber TEXT, tc_id integer, val TEXT)")
        self.execute("CREATE UNIQUE INDEX if not exists bp_tc_I ON bp_tc(tc_id, bp_id)")
        self.conn.commit()

    def execute(self,  cmd):
        return self.conn.execute(cmd)

    def insertTestcase(self, tc_name):
        self.execute("insert into testcase(tc_name, all_result) values ('%s', 1)"%tc_name)
        self.conn.commit()

    def executeMany(self, sql, datalist):
        return self.conn.executemany(sql, datalist)

    def insertVarValue(self, tc_id,  breakpoint, val):
        val = str(val)
        val = val.replace("'",'"')
        sqlcmd = "insert into bp_tc(tc_id,  breakpoint, val) values (%s, '%s', '%s')"%(tc_id,  breakpoint.strip(), val)
        self.execute(sqlcmd)
        self.conn.commit()

    def closeDB(self):
        self.conn.close()

    def droptable(self, tablename):
        self.execute("drop table if exists " + tablename)
