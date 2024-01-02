import os
import argparse
import pexpect
from DB import DB
import locale
import time
from Phase1.SBFL_Formula_DStar import *
from Phase1.getSpectrum import *
from Phase2.get_JDB_var import *
import os
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

expect_list = ["main\[1\]", pexpect.EOF, pexpect.TIMEOUT] 
db_base_path = "../runningExample_code/"
TIMEOUT = 60

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--junit_path', type=str, default='lib/junit-4.10.jar:'+'.:lib/:'+'example/:'+'exampleTest/')
    args = parser.parse_args()

    version = 'example'
    class_path = "-classpath " + args.junit_path
    failed_testcases, db = get_failed_testcases(db_base_path)
    break_points = get_bps(db_base_path)

    os.chdir(db_base_path)

    mem_data = []
    for i in range(len(failed_testcases)):
        finalPointPos = failed_testcases[i].find('.')
        shell_command = 'jdb '+ class_path +' SingleJUnitTestRunner '+ 'exampleTest.exampleTest' + '#' + failed_testcases[i][finalPointPos+1:][12:]
        print('exampleTest.exampleTest' + '#' + failed_testcases[i][finalPointPos+1:][12:] + " is running...", end="")
        p = pexpect.spawn(shell_command)
        
        p.expect('>', timeout=TIMEOUT)
        output = p.before.decode() 
        
        flag = True
        p.sendline("stop in " + failed_testcases[i])
        
        p.expect('>', timeout=TIMEOUT)
        output = p.before.decode() 

        p.sendline("run")
        index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
        output = p.before.decode()
        if index != 0:
            continue
        
        for bp in break_points.keys():
            p.sendline("stop at " + bp)
            p.expect("main\[1\]", timeout=TIMEOUT)
            output = p.before.decode()

        p.sendline("cont")
        index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
        output = p.before.decode()
        while True:
            stack_height = get_stack_height(p, failed_testcases[i][finalPointPos+1:])
            if stack_height != 0:
                className = output[output.find(",")+2:output.rfind(".")]
                line_pos = output.rfind("line=")
                if line_pos != -1:
                    lineNum = output[line_pos+5:output.rfind("bci")]
                else:
                    p.sendline("cont")
                    index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
                    if index != 0:
                        break
                    output = p.before.decode()
                    continue
                bp_pos = className + ":" + str(locale.atoi(lineNum))
                output = p.before.decode()
                p.sendline("step")
                index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
                if index != 0:
                    break
                output = p.before.decode()
                val, isEOF = getLocalVars(p, stack_height)
                mem_data.append((i+1, bp_pos, break_points[bp_pos], str(val)))
                if output.find("Breakpoint hit") != -1:
                    continue
                else:
                    p.sendline("cont")
                    index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
                    if index != 0:
                        break
                    output = p.before.decode()
            else:
                p.sendline("cont")
                index = p.expect(["main\[1\]", pexpect.EOF, pexpect.TIMEOUT], timeout=TIMEOUT)
                output = p.before.decode()
        print("Done.")
    sqlcmd = "replace into bp_tc(tc_id, lineNumber, bp_id, val) values (?, ?, ?, ?);"
    db.executeMany(sqlcmd, mem_data)
    db.closeDB()
    end_time = time.time()
    
    print("\n\nDone" + "\nTime cost: " + str(end_time - start_time) + "s.")