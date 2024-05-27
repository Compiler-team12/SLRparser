class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self._str(0)

    def _str(self, level):
        ret = "\t" * level + repr(self.symbol) + "\n"
        for child in self.children:
            ret += child._str(level + 1)
        return ret
    
class SLRParser:
    def __init__(self, parsing_table, grammar): 
        self.parsing_table = parsing_table
        self.grammar = grammar
        self.stack = []
        self.input_tokens = []
        self.position = 0
        self.tree_stack = []

    def parse(self, tokens): 
        self.input_tokens = tokens
        self.position = 0
        self.stack = [0]
        self.tree_stack = []

        while True:
            state = self.stack[-1]
            current_token = self.input_tokens[self.position] if self.position < len(self.input_tokens) else '$'

            action = self.parsing_table.get((state, current_token)) 
            
            if not action: # REJECT
                print(f"There is no ACTION for ({state}, {current_token})")
                print("current stack state: ",self.stack)
                print()
                return

            if action[0] == 's': # SHIFT
                self.stack.append(int(action[1:])) 
                self.position += 1
                self.tree_stack.append(TreeNode(current_token))
            elif action[0] == 'r': # REDUCE
                production = self.grammar[int(action[1:])] 
                lhs, rhs = production

                node = TreeNode(lhs)
                
                if rhs != ['ε']:
                    for _ in range(len(rhs)):
                        self.stack.pop()
                        node.add_child(self.tree_stack.pop())

                node.children.reverse()
                self.tree_stack.append(node)

                state = self.stack[-1]
                self.stack.append(self.parsing_table[(state, lhs)]) # GOTO
            elif action == 'acc': # ACCEPT
                print("ACCEPT")
                for i in self.tree_stack:
                    print(i)
                return
            
# SLR parsing table 
parsing_table = {
    (0, 'vtype'): 's5',
    (0, '$'): 'r2',
    (0, 'DECLS'): 1,
    (0, 'DECL'): 2,
    (0, 'VDECL'): 3,
    (0, 'FDECL'): 4,
    (1, '$'): 'acc',
    (2, 'vtype'): 's5',
    (2, '$'): 'r2',
    (2, 'DECLS'): 6,
    (2, 'DECL'): 2,
    (2, 'VDECL'): 3,
    (2, 'FDECL'): 4,
    (3, 'vtype'): 'r3',
    (3, '$'): 'r3',
    (4, 'vtype'): 'r4',
    (4, '$'): 'r4',
    (5, 'id'): 's7',
    (5, 'ASSIGN'): 8,
    (6, '$'): 'r1',
    (7, 'semi'): 's9',
    (7, 'assign'): 's11',
    (7, 'lparen'): 's10',
    (8, 'semi'): 's12',
    (9, 'vtype'): 'r5',
    (9, 'id'): 'r5',
    (9, 'rbrace'): 'r5',
    (9, 'if'): 'r5',
    (9, 'while'): 'r5',
    (9, 'return'): 'r5',
    (9, '$'): 'r5',
    (10, 'vtype'): 's14',
    (10, 'rparen'): 'r21',
    (10, 'ARG'): 13,
    (11, 'id'): 's23',
    (11, 'literal'): 's17',
    (11, 'character'): 's18',
    (11, 'boolstr'): 's19',
    (11, 'lparen'): 's22',
    (11, 'num'): 's24',
    (11, 'RHS'): 15,
    (11, 'EXPR'): 16,
    (11, 'TERM'): 20,
    (11, 'FACTOR'): 21,
    (12, 'vtype'): 'r6',
    (12, 'id'): 'r6',
    (12, 'rbrace'): 'r6',
    (12, 'if'): 'r6',
    (12, 'while'): 'r6',
    (12, 'return'): 'r6',
    (12, '$'): 'r6',
    (13, 'rparen'): 's25',
    (14, 'id'): 's26',
    (15, 'semi'): 'r7',
    (16, 'semi'): 'r8',
    (16, 'addsub'): 's27',
    (17, 'semi'): 'r9',
    (18, 'semi'): 'r10',
    (19, 'semi'): 'r11',
    (20, 'semi'): 'r13',
    (20, 'addsub'): 'r13',
    (20, 'multdiv'): 's28',
    (20, 'rparen'): 'r13',
    (21, 'semi'): 'r15',
    (21, 'addsub'): 'r15',
    (21, 'multdiv'): 'r15',
    (21, 'rparen'): 'r15',
    (22, 'id'): 's23',
    (22, 'lparen'): 's22',
    (22, 'num'): 's24',
    (22, 'EXPR'): 29,
    (22, 'TERM'): 20,
    (22, 'FACTOR'): 21,
    (23, 'semi'): 'r17',
    (23, 'addsub'): 'r17',
    (23, 'multdiv'): 'r17',
    (23, 'rparen'): 'r17',
    (24, 'semi'): 'r18',
    (24, 'addsub'): 'r18',
    (24, 'multdiv'): 'r18',
    (24, 'rparen'): 'r18',
    (25, 'lbrace'): 's30',
    (26, 'rparen'): 'r23',
    (26, 'comma'): 's32',
    (26, 'MOREARGS'): 31,
    (27, 'id'): 's23',
    (27, 'lparen'): 's22',
    (27, 'num'): 's24',
    (27, 'TERM'): 33,
    (27, 'FACTOR'): 21,
    (28, 'id'): 's23',
    (28, 'lparen'): 's22',
    (28, 'num'): 's24',
    (28, 'FACTOR'): 34,
    (29, 'addsub'): 's27',
    (29, 'rparen'): 's35',
    (30, 'vtype'): 's42',
    (30, 'id'): 's43',
    (30, 'rbrace'): 'r25',
    (30, 'if'): 's40',
    (30, 'while'): 's41',
    (30, 'return'): 'r25',
    (30, 'VDECL'): 38,
    (30, 'ASSIGN'): 39,
    (30, 'BLOCK'): 36,
    (30, 'STMT'): 37,
    (31, 'rparen'): 'r20',
    (32, 'vtype'): 's44',
    (33, 'semi'): 'r12',
    (33, 'addsub'): 'r12',
    (33, 'multdiv'): 's28',
    (33, 'rparen'): 'r12',
    (34, 'semi'): 'r14',
    (34, 'addsub'): 'r14',
    (34, 'multdiv'): 'r14',
    (34, 'rparen'): 'r14',
    (35, 'semi'): 'r16',
    (35, 'addsub'): 'r16',
    (35, 'multdiv'): 'r16',
    (35, 'rparen'): 'r16',
    (36, 'return'): 's46',
    (36, 'RETURN'): 45,
    (37, 'vtype'): 's42',
    (37, 'id'): 's43',
    (37, 'rbrace'): 'r25',
    (37, 'if'): 's40',
    (37, 'while'): 's41',
    (37, 'return'): 'r25',
    (37, 'VDECL'): 38,
    (37, 'ASSIGN'): 39,
    (37, 'BLOCK'): 47,
    (37, 'STMT'): 37,
    (38, 'vtype'): 'r26',
    (38, 'id'): 'r26',
    (38, 'rbrace'): 'r26',
    (38, 'if'): 'r26',
    (38, 'while'): 'r26',
    (38, 'return'): 'r26',
    (39, 'semi'): 's48',
    (40, 'lparen'): 's49',
    (41, 'lparen'): 's50',
    (42, 'id'): 's51',
    (42, 'ASSIGN'): 8,
    (43, 'assign'): 's11',
    (44, 'id'): 's52',
    (45, 'rbrace'): 's53',
    (46, 'id'): 's23',
    (46, 'literal'): 's17',
    (46, 'character'): 's18',
    (46, 'boolstr'): 's19',
    (46, 'lparen'): 's22',
    (46, 'num'): 's24',
    (46, 'RHS'): 54,
    (46, 'EXPR'): 16,
    (46, 'TERM'): 20,
    (46, 'FACTOR'): 21,
    (47, 'rbrace'): 'r24',
    (47, 'return'): 'r24',
    (48, 'vtype'): 'r27',
    (48, 'id'): 'r27',
    (48, 'rbrace'): 'r27',
    (48, 'if'): 'r27',
    (48, 'while'): 'r27',
    (48, 'return'): 'r27',
    (49, 'boolstr'): 's58',
    (49, 'lparen'): 's57',
    (49, 'COND'): 55,
    (49, 'PRIMARYCOND'): 56,
    (50, 'boolstr'): 's58',
    (50, 'lparen'): 's57',
    (50, 'COND'): 59,
    (50, 'PRIMARYCOND'): 56,
    (51, 'semi'): 's9',
    (51, 'assign'): 's11',
    (52, 'rparen'): 'r23',
    (52, 'comma'): 's32',
    (52, 'MOREARGS'): 60,
    (53, 'vtype'): 'r19',
    (53, '$'): 'r19',
    (54, 'semi'): 's61',
    (55, 'rparen'): 's62',
    (55, 'comp'): 's63',
    (56, 'rparen'): 'r31',
    (56, 'comp'): 'r31',
    (57, 'boolstr'): 's58',
    (57, 'lparen'): 's57',
    (57, 'COND'): 64,
    (57, 'PRIMARYCOND'): 56,
    (58, 'rparen'): 'r33',
    (58, 'comp'): 'r33',
    (59, 'rparen'): 's65',
    (59, 'comp'): 's63',
    (60, 'rparen'): 'r22',
    (61, 'rbrace'): 'r36',
    (62, 'lbrace'): 's66',
    (63, 'boolstr'): 's58',
    (63, 'lparen'): 's57',
    (63, 'PRIMARYCOND'): 67,
    (64, 'rparen'): 's68',
    (64, 'comp'): 's63',
    (65, 'lbrace'): 's69',
    (66, 'vtype'): 's42',
    (66, 'id'): 's43',
    (66, 'rbrace'): 'r25',
    (66, 'if'): 's40',
    (66, 'while'): 's41',
    (66, 'return'): 'r25',
    (66, 'VDECL'): 38,
    (66, 'ASSIGN'): 39,
    (66, 'BLOCK'): 70,
    (66, 'STMT'): 37,
    (67, 'rparen'): 'r30',
    (67, 'comp'): 'r30',
    (68, 'rparen'): 'r32',
    (68, 'comp'): 'r32',
    (69, 'vtype'): 's42',
    (69, 'id'): 's43',
    (69, 'rbrace'): 'r25',
    (69, 'if'): 's40',
    (69, 'while'): 's41',
    (69, 'return'): 'r25',
    (69, 'VDECL'): 38,
    (69, 'ASSIGN'): 39,
    (69, 'BLOCK'): 71,
    (69, 'STMT'): 37,
    (70, 'rbrace'): 's72',
    (71, 'rbrace'): 's73',
    (72, 'vtype'): 'r35',
    (72, 'id'): 'r35',
    (72, 'rbrace'): 'r35',
    (72, 'if'): 'r35',
    (72, 'while'): 'r35',
    (72, 'else'): 's75',
    (72, 'return'): 'r35',
    (72, 'ELSE'): 74,
    (73, 'vtype'): 'r29',
    (73, 'id'): 'r29',
    (73, 'rbrace'): 'r29',
    (73, 'if'): 'r29',
    (73, 'while'): 'r29',
    (73, 'return'): 'r29',
    (74, 'vtype'): 'r28',
    (74, 'id'): 'r28',
    (74, 'rbrace'): 'r28',
    (74, 'if'): 'r28',
    (74, 'while'): 'r28',
    (74, 'return'): 'r28',
    (75, 'lbrace'): 's76',
    (76, 'vtype'): 's42',
    (76, 'id'): 's43',
    (76, 'rbrace'): 'r25',
    (76, 'if'): 's40',
    (76, 'while'): 's41',
    (76, 'return'): 'r25',
    (76, 'VDECL'): 38,
    (76, 'ASSIGN'): 39,
    (76, 'BLOCK'): 77,
    (76, 'STMT'): 37,
    (77, 'rbrace'): 's78',
    (78, 'vtype'): 'r34',
    (78, 'id'): 'r34',
    (78, 'rbrace'): 'r34',
    (78, 'if'): 'r34',
    (78, 'while'): 'r34',
    (78, 'return'): 'r34',
}

# nonambiguoous CFG
grammar = [
    ('CODE', ['DECLS']),
    ('DECLS', ['DECL', 'DECLS']),
    ('DECLS', ['ε']),
    ('DECL', ['VDECL']),
    ('DECL', ['FDECL']),
    ('VDECL', ['vtype', 'id', 'semi']),
    ('VDECL', ['vtype', 'ASSIGN', 'semi']),
    ('ASSIGN', ['id', 'assign', 'RHS']),
    ('RHS', ['EXPR']),
    ('RHS', ['literal']),
    ('RHS', ['character']),
    ('RHS', ['boolstr']),
    ('EXPR', ['EXPR', 'addsub', 'TERM']),
    ('EXPR', ['TERM']),
    ('TERM', ['TERM', 'multdiv', 'FACTOR']),
    ('TERM', ['FACTOR']),
    ('FACTOR', ['lparen', 'EXPR', 'rparen']),
    ('FACTOR', ['id']),
    ('FACTOR', ['num']),
    ('FDECL', ['vtype', 'id', 'lparen', 'ARG', 'rparen', 'lbrace', 'BLOCK', 'RETURN', 'rbrace']),
    ('ARG', ['vtype', 'id', 'MOREARGS']),
    ('ARG', ['ε']),
    ('MOREARGS', ['comma', 'vtype', 'id', 'MOREARGS']),
    ('MOREARGS', ['ε']),
    ('BLOCK', ['STMT', 'BLOCK']),
    ('BLOCK', ['ε']),
    ('STMT', ['VDECL']),
    ('STMT', ['ASSIGN', 'semi']),
    ('STMT', ['if', 'lparen', 'COND', 'rparen', 'lbrace', 'BLOCK', 'rbrace', 'ELSE']),
    ('STMT', ['while', 'lparen', 'COND', 'rparen', 'lbrace', 'BLOCK', 'rbrace']),
    ('COND', ['COND', 'comp', 'PRIMARYCOND']),
    ('COND', ['PRIMARYCOND']),
    ('PRIMARYCOND', ['lparen', 'COND', 'rparen']),
    ('PRIMARYCOND', ['boolstr']),
    ('ELSE', ['else', 'lbrace', 'BLOCK', 'rbrace']),
    ('ELSE', ['ε']),
    ('RETURN', ['return', 'RHS', 'semi']),
]

# 파일 받아서 텍스트 파일로 구현하기
# Example input sequence
# ACCEPT tokens = ['vtype', 'id', 'semi', 'vtype', 'id', 'lparen', 'rparen', 'lbrace', 'if', 'lparen', 'boolstr', 'comp', 'boolstr', 'rparen', 'lbrace', 'rbrace', 'return', 'id', 'semi', 'rbrace']
# REJECT tokens = ['vtype', 'id', 'vtype', 'id', 'lparen', 'rparen', 'lbrace', 'if', 'lparen', 'boolstr', 'comp', 'boolstr', 'rparen', 'lbrace', 'rbrace', 'return', 'id', 'semi', 'rbrace']

parser = SLRParser(parsing_table, grammar)
parser.parse(tokens)
