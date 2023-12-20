operator_precedence = {
    '=': 1, 
    '+': 2,
    '-': 2,  
    'x': 3, 
    '/': 3, 
    'is': 4,  
    '~': 5,
}


class ASTNode:

  def __init__(self, type, value):
    self.type = type
    self.value = value
    self.children = []

  def add_child(self, child):
    self.children.append(child)


def parse_token(token):
    parts = token[1:-1].split(': ', 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid token format: {token}")
    op_type, op_value = parts
    return op_type, op_value


def parse_expression(tokens, index):
    if index >= len(tokens):
        return None, index
    try:
        if tokens[index].startswith('[KEY: then]'):
            unary_expr_node = ASTNode("Then", "")
            op_type, op_value = parse_token(tokens[index])
            operand_expr, index = parse_expression_with_precedence(tokens, index + 1)
            unary_expr_node.add_child(operand_expr)
            return unary_expr_node, index
        elif tokens[index].startswith('[OP'):
            unary_expr_node = ASTNode("Assign", "")
            node, index = parse_assignment(tokens, index)
            unary_expr_node.add_child(node)
            return unary_expr_node, index
        else:
            return parse_expression_with_precedence(tokens, index)
    except Exception as e:
        print(f"Error parsing expression: {e}")
        return None, index
    
def parse_assignment(tokens, index):
    if index + 1 >= len(tokens):
        return None, index

    lhs, index = parse_expression_with_precedence(tokens, index) 
    op_type, op_value = parse_token(tokens[index])
    assign_node = ASTNode("OP :", op_value)
    assign_node.add_child(lhs)

    index += 1  # Skip '=' operator

    rhs, index = parse_expression_with_precedence(tokens, index)  # Parse right-hand side with precedence
    assign_node.add_child(rhs)

    return assign_node, index

def parse_expression_with_precedence(tokens, index, min_precedence=0):
    if index >= len(tokens):
        return None, index

    lhs_type, lhs_value = parse_token(tokens[index])
    lhs_node = ASTNode(lhs_type, lhs_value)
    index += 1

    while index < len(tokens) and tokens[index].startswith('[OP'):
        op_type, op_value = parse_token(tokens[index])
        op_precedence = operator_precedence[op_value]
        if op_precedence < min_precedence:
            break
        index += 1
        next_min_precedence = op_precedence + 1 if op_value != '=' else op_precedence
        rhs_node, index = parse_expression_with_precedence(tokens, index, next_min_precedence)
        binary_op_node = ASTNode("OP", op_value)
        binary_op_node.add_child(lhs_node)
        binary_op_node.add_child(rhs_node)
        lhs_node = binary_op_node

    return lhs_node, index


def parse_if_statement(tokens, index):
    if_node = ASTNode("IF CONDITION", "")
    condition_expr, index = parse_expression_with_precedence(tokens, index + 1)
    if_node.add_child(condition_expr)

    # Skipping'[KEY: then]'
    index += 1

    then_node = ASTNode("THEN", "")
    then_expr, index = parse_expression_with_precedence(tokens, index)
    then_node.add_child(then_expr)

    # Adding 'THEN :' to the IF tree
    if_node.add_child(then_node)

    return if_node, index

def parse_else_statement(tokens, index):
    if_node = ASTNode("ELSE CONDITION", "")

    condition_expr, index = parse_expression_with_precedence(tokens, index + 1)
    if_node.add_child(condition_expr)

    then_expr, index = parse_expression_with_precedence(tokens, index)
    if_node.add_child(then_expr)

    return if_node, index

def parse(tokens):
    ast = []
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token.startswith('[ID') or token.startswith('[NUM') or token.startswith('[OP'):
            node, index = parse_expression(tokens, index)
            if node is not None:
                ast.append(node)
        elif token.startswith('[KEY: if]'):
            node, index = parse_if_statement(tokens, index)
            if node:
                ast.append(node)
            if index < len(tokens) and tokens[index].startswith('[KEY: else]'):
                else_node, index = parse_else_statement(tokens, index)
                if else_node:
                    ast.append(else_node)
        else:
            index += 1
    return ast



# Tokens from project part 1
tokens = [
    '[ID: 2Pencil]', '[OP: =]', '[NUM: 1]','[ID: 1Pencil]', '[OP: =]',
    '[ID: 1Pencil]', '[OP: x]', '[NUM: 2]','[KEY: if]', '[ID: 1box]',
    '[OP: is]', '[NUM: 1]','[KEY: then]','[ID: Pencil-box]', '[OP: =]',
    '[ID: 2Pencil]', '[OP: +]', '[ID: 1box]', '[OP: ~]', '[ID: 1Pencil]',
    '[KEY: else]', '[KEY: print]', '[ID: 2Pencil]',
]
tokens_2 = [
    '[ID: B]', '[OP: =]', '[NUM: 5]', '[OP: -]', '[NUM: 6]', '[OP: x]', '[NUM: 2]', '[OP: /]', '[NUM: 4]',
]
tokens_3 = [
    '[ID: A]', '[OP: =]', '[ID: B]', '[OP: -]', '[ID: C]', '[OP: x]', '[ID: D]',
    '[ID: A]', '[OP: =]', '[ID: B]', '[OP: +]', '[ID: C]', '[OP: /]', '[ID: D]',
]
tokens_4 = [
    '[ID: A]', '[OP: =]', '[ID: B]', '[OP: -]', '[ID: C]', '[OP: x]', '[ID: D]',
    '[ID: E]', '[OP: =]', '[ID: F]', '[OP: +]', '[ID: G]', '[OP: /]', '[ID: H]',
    '[ID: I]', '[OP: =]', '[ID: J]', '[OP: x]', '[ID: K]', '[OP: -]', '[ID: L]',
    '[ID: M]', '[OP: =]', '[ID: N]', '[OP: +]', '[ID: O]', '[OP: x]', '[ID: P]',
    '[ID: Q]', '[OP: =]', '[ID: R]', '[OP: /]', '[ID: S]', '[OP: +]', '[ID: T]',
    '[ID: U]', '[OP: =]', '[ID: V]', '[OP: -]', '[ID: W]', '[OP: /]', '[ID: X]',
    '[ID: Y]', '[OP: =]', '[ID: Z]', '[OP: x]', '[ID: A1]', '[OP: +]', '[ID: B1]',
    '[ID: C1]', '[OP: =]', '[ID: D1]', '[OP: /]', '[ID: E1]', '[OP: -]', '[ID: F1]',
    '[ID: G1]', '[OP: =]', '[ID: H1]', '[OP: +]', '[ID: I1]', '[OP: x]', '[ID: J1]',
    '[ID: K1]', '[OP: =]', '[ID: L1]', '[OP: -]', '[ID: M1]', '[OP: /]', '[ID: N1]',
]

ast = parse(tokens_3)


def print_ast(node, level=0):
    if node is None:
        return
    print("  " * level + f"{node.type} : {node.value}")
    for child in node.children:
        print_ast(child, level + 1)


for node in ast:
  print_ast(node)
