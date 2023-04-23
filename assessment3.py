#Write your program here 👇👇

# EOF (end-of-file) token is used to indicate that
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        # String representation of the class instance.
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = conv(self.value)
        )

    def __conv__(self):
        return self.__str__()


class Interpret(object):
    def __init__(self, text):
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid Character')

    def advance(self):
        # Advance the pos pointer and set the current_char variable
        self.pos += 1
        if self.pos > len(self.text) - 1:
          # Indicates end of input
          self.current_char = None 

        else:
          self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()

    def integer(self):
        # Return an integer
        result = ''
        while self.current_char != None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        # For breaking the string 
        while self.current_char != None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


class BT(object):
    pass


class BinaryTree(BT):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right 


class Num(BT):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, interpret):
        self.interpret = interpret
        # set current token to the first token taken from the input
        self.current_token = self.interpret.get_next_token()

    def error(self):
        raise Exception('Invalid Syntax')

    def replace(self, token_type):
        # compare the current token type with the past token type
        if self.current_token.type == token_type:
          # if they match then replace the current token
          self.current_token = self.interpret.get_next_token()
        else:
          # otherwise raise an exception.
          self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.replace(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.replace(LPAREN)
            node = self.expr()
            self.replace(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.replace(MUL)
            elif token.type == DIV:
                self.replace(DIV)

            node = BinaryTree(left = node, op = token, right = self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.replace(PLUS)
            elif token.type == MINUS:
                self.replace(MINUS)

            node = BinaryTree(left = node, op = token, right = self.term())

        return node

    def process(self):
        return self.expr()


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Convert(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryTree(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.process()
        return self.visit(tree)



def main():
    while True:
        try:
            try:
                text = raw_input('expression> ')
            except NameError:  
                text = input('expression> ')
        except EOFError:
            break
        if not text:
            continue

        interpret = Interpret(text)
        parser = Parser(interpret)
        convert = Convert(parser)
        result = convert.interpret()
        print(result)


if __name__ == '__main__':
    main()