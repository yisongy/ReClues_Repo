class StateGDB(GDB):
    CHAR_PATTERN    = re.compile(r"(?P<value>\d+) +(?P<character>'.*')")
    STRING_PATTERN  = re.compile('(?P<pointer>0x[^ ]+) +(?P<string>".*")')
    POINTER_PATTERN = re.compile(".*(?P<value>0x[0-9a-f]+)")
    FUNCTION_POINTER_PATTERN = re.compile(".*(?P<value>0x[0-9a-f]+) <(?P<identifier>[^>]*)>")

    def _fetch_values(self, name, frame, value, vars):
        value = string.strip(value)

        m = self.CHAR_PATTERN.match(value)
        if m is not None:
            vars[(name, frame)] = m.group('character')
            return

        m = self.STRING_PATTERN.match(value)
        if m is not None:
            vars[(name, frame)] = m.group('string')
            return

        m = self.FUNCTION_POINTER_PATTERN.match(value)
        if m is not None:
            vars[(name, frame)] = m.group('identifier')
            return

        if self.POINTER_PATTERN.match(value):
            self._unfold_pointer(name, frame, value, vars)
            return
        
        vars[(name, frame)] = value

    def _fetch_variables(self, frame, vars):
        SEP = " = "
        IDENTIFIER = re.compile("[a-zA-Z_]")

        for query in ["info locals", "info args"]:
            list = self.question(query)

            lines = string.split(list, "\n")
            
            for i in range(1, len(lines)):
                while lines[i] != "" and not IDENTIFIER.match(lines[i][0]):
                    lines[i - 1] = lines[i - 1] + string.strip(lines[i])


            for line in lines:
                separator = string.find(line, SEP)
                if separator > 0:
                    name  = line[0 : separator]
                    value = line[separator + len(SEP) : ]
                    self._fetch_values(name, frame, value, vars)

        return vars

    def state(self):
        vars = {}
        temp = self.question("bt")
        temp = re.findall(r'#(\d+)', temp)
        frame = 0
        if len(temp) != 0:
            frame = int(temp[-1]) + 1

        self._fetch_variables(frame, vars)

        t.outcome = str(len(vars.keys())) + " variables"
        return vars