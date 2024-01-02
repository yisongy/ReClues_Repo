import pexpect
import os
import re
expect_list = ["main\[1\]", pexpect.EOF, pexpect.TIMEOUT] 
TIMEOUT = 60
def getLocalVars(p, stack_height):
    vars = {}
    p.sendline("locals")
    index = p.expect(expect_list, timeout=TIMEOUT)
    if index != 0:
        return {}, False
    raw_data = p.before.decode()
    for line in raw_data.split(os.linesep):
        equal_index = line.find("= ")
        if equal_index != -1:
            val_name = line[:equal_index-1].strip()
            val_value = line[equal_index+2:].strip()
            vars[val_name] = val_value
            if val_value.find("instance")!=-1:
                p.sendline("dump "+val_name)
                index = p.expect(expect_list, timeout=TIMEOUT)
                if index != 0:
                    return {}, False
                temp = p.before.decode()
                if temp.find("= ") == -1:
                    vars[val_name] = val_value
                else:
                    vars[val_name] = temp[temp.find("= ")+2:]
    return vars, True

def get_stack_height(p, testCase):
    p.sendline("where")
    p.expect(expect_list, timeout=TIMEOUT)
    raw_data = p.before.decode()
    raw_data = raw_data.split('\n')
    temp = []
    for line in raw_data:
        if line.find(testCase) != -1 or line.find('setUp') != -1:
            temp = re.findall("\[(\d+)\]", line)
            break
    if len(temp) != 0:
        stack_height = (int)(temp[-1])
    else:
        stack_height = 0
    return stack_height