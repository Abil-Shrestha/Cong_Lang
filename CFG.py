KEYWORDS = {'if', 'then', 'else', 'print'}
OPERATORS = {'+', '~', 'x', '/', '=', 'is'}
NUMBERS = '0123456789'

print("Context-Free Grammar Visualization:")
print("                                   ")
print("Program ::= StatementList")
print("StatementList ::= Statement | Statement StatementList")
print("Statement ::= Assignment | Declaration | IfStatement | WhileLoop | ForLoop | FunctionDefinition | ExpressionStatement")
print("Assignment ::= ID '=' Expression")
print('Expression ::= Term | Expression "+" Term | Expression "-" Term')
print('Term ::= Factor | Term "*" Factor | Term "/" Factor')
print("Factor ::= '(' Expression ')' | NUM | ID")
print('IfStatement ::= "if" "(" Expression ")" "{" StatementList "}" | "if" "(" Expression ")" "{" StatementList "}" "else" "{" StatementList "}"')
print('WhileLoop ::= "while" "(" Expression ")" "{" StatementList "}"')
print("ForLoop ::= 'for' '(' Statement Expression ';' Statement ')' '{' StatementList '}'")
print("KEYWORDS =", KEYWORDS)
print("OPERATORS =", OPERATORS)
print("NUMBERS =", NUMBERS)
print("")
print(" Input Tokens ")
print("""
[ID: 2Pencil]
[OP: =]
[ID: 1Pencil]
[OP: x]
[NUM: 2]
""")

class ASTNode:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        if self.type == "EXPR":
            ret = "\t" * level + f"[{self.type}: {self.value}]" + "\n" + "\t" * level + f"                         ↓" + "\n" 
            for child in self.children:
                ret += child.__repr__(level + 1)
        elif self.type == "ID":
            ret = "\t" * level + f"[{self.type}: {self.value}] "
            ret += " ".join(child.__repr__(level).strip() for child in self.children)
        elif self.type == "OP" and self.value != "=":
            ret = f"[{self.type}: {self.value}] "
            ret += " ".join(child.__repr__(level).strip() for child in self.children)
        elif self.type == "NUM":
            ret = f"[{self.type}: {self.value}] "
            ret += " ".join(child.__repr__(level).strip() for child in self.children)
        else:
            ret = "\t" * level + f"[{self.type}: {self.value}]" + "\n"
            for child in self.children:
                ret += child.__repr__(level + 1)
        return ret


root = ASTNode("ID", "2Pencil")
root.add_child(ASTNode("OP", "="))

expr_node = ASTNode("EXPR", "")
expr_node.add_child(ASTNode("ID", "1Pencil"))
expr_node.add_child(ASTNode("OP", "x"))
expr_node.add_child(ASTNode("NUM", "2"))

root.add_child(expr_node)

print(" Parser AST ")
print(" ")
print(root)
