import re

KEYWORDS = {'if', 'then', 'else', 'print'}
OPERATORS = {'+', '~', 'x', '/', '=', 'is'}
NUMBERS = '0123456789'

def is_whitespace(char):
    return char in ' \t\n\r'

def is_alphanumeric(char):
  pattern = r'^[a-zA-Z0-9]$'
  return bool(re.match(pattern, char))

def categorize(word):
    if word in KEYWORDS:
        return f'[KEY: {word}]'
    elif word in OPERATORS:
        return f'[OP: {word}]'
    elif all(ch in NUMBERS for ch in word):
        return f'[NUM: {word}]'
    else:
        return f'[ID: {word}]'

def tokenize(input_code):
    tokens = []
    current_word = ''
    i = 0
    length = len(input_code)

    while i < length:
        char = input_code[i]

        if is_whitespace(char) or (char in OPERATORS and (i == 0 or input_code[i - 1] in OPERATORS or is_whitespace(input_code[i - 1]))):
            if current_word:
                tokens.append(categorize(current_word))
                current_word = ''
            if char in OPERATORS:
                tokens.append(categorize(char))
        elif char in OPERATORS and i < length - 1 and is_alphanumeric(input_code[i + 1]):
            current_word += char
        else:
            current_word += char
        i += 1

    if current_word:
        tokens.append(categorize(current_word))

    return tokens

input_code = '''
1Pencil = 1
2Pencil = 1Pencil x2
if 1box is 1 then
Pencil-box = 2Pencil + 1box ~ 1Pencil
else
print 2Pencil
'''

output = tokenize(input_code)
print((output))

