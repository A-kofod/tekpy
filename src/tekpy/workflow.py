import re, math

class TexTree:
    """Python infix to LaTex math lines"""
    def __init__(self, expr):
        self.expr = expr

        self.precedence = {
    # Binary
    '+':(1, 'L'),
    '-':(1, 'L'),
    '*':(2, 'L'),
    '/':(2, 'L'),
    '**':(3, 'R'),
    '=':(0, 'L'),
    'res':(0, 'L'),
    'angle': (1, 'L')

 
    }
        self.unary = {
    'math.sqrt':(4, 'R'),
    'sqrt': (4, 'R'),
    'sympy.sqrt': (4, 'R'),
    'math.cos': (4, 'R'),
    'cos': (4, 'R'),
    'math.sin': (4, 'R'),
    'sin': (4, 'R'),
    'math.tan': (4, 'R'),
    'u-': (4, 'R'),
    'ln':(4, 'R'),
    
    }
    
  
        self._round_decimals = 2
        self._latex = self.all_call()
        self.e_notation_onoff = True

    def __str__(self):
        _to_show = self._apply_round(self._latex, self._round_decimals)
        return self.e_notation(_to_show)

    def e_nota(self, choice: bool):
        """True or False"""
        self.e_notation_onoff = choice
        return self

    def find_tokens(self, expr:str):
        tokens = []

        token_patters = r'''
            \d+(?:\.\d+)?(?:e[+-]?\d+)?[A-Za-zµμΩ/^0-9]* | # numbers with optional e-notation + units
            \d+\.\d+                                     | # floats
            \d+                                          | # ints
            \*\*                                         | # exp
            [A-Za-z_]\w*                                 | # letters/variabbles
            [+\-*/=()]                                     # ops
            
        '''
 
        # Token handle for number representation
        
        tokens = re.findall(token_patters, expr, re.VERBOSE)
        for i, token in enumerate(tokens):
            if token == 'angle':
                left = tokens[i - 1]
                right = tokens[i + 1]
                if right == '-':
                    right_val = tokens[i + 2]
                    token_repl = f'{left}\\{token}{right}{right_val}'
                    tokens[i-1:i+3] = [token_repl]
                else:
                    token_repl = f'{left}\\{token}{right}'
                    tokens[i-1:i+2] = [token_repl]
                
            if token == 'math':
                left = token
                right = tokens[i + 1]
                token_repl = f'{left}.{right}'
                tokens[i:i+2] = [token_repl]

                print(f'token_repl = {token_repl}')

        print(f'tokens post handle: {tokens}')
        return tokens

    def infix_to_postfix(self, tokens):
        output_stack = []
        operator_stack = []
        previus_token = [None]

        for token in tokens:
            
            # u- handeling 
            if token == '-':
                if previus_token[0] is None or previus_token[0] in self.precedence or previus_token[0] in self.unary or previus_token[0] in ('('):
                    token = 'u-'
                    operator_stack.append(token)
                    previus_token[0] = token
                    continue

            # Variables or numbers
            if token not in self.precedence and token not in self.unary and token not in ('(', ')'):
                output_stack.append(token)
                previus_token[0] = token
            # function calls
            elif token in self.unary:
                operator_stack.append(token)
                previus_token[0] = token

            # perenthesies handle og function calls
            elif token == '(':
                operator_stack.append(token)
                previus_token[0] = token

            elif token == ')': # pop everythin from operatro_stack until (
                while operator_stack and operator_stack[-1] != '(':
                    output_stack.append(operator_stack.pop())
                    previus_token[0] = token
                    
                    # functions 
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                    previus_token[0] = token
                if operator_stack and operator_stack[-1] in self.unary: # if, after popping, the last item after the ( is in unary, pop it also. 
                    output_stack.append(operator_stack.pop())
                    previus_token[0] = token
                    
                
            elif token in self.precedence:
                token_prec, assoc = self.precedence[token]
                while operator_stack and operator_stack[-1] in self.precedence:
                    top_of_stack = operator_stack[-1]
                    top_of_precedence = self.precedence[top_of_stack][0]

                    if (assoc == 'L' and top_of_precedence >= token_prec) or \
                    (assoc == 'R' and top_of_precedence > token_prec):
                        output_stack.append(operator_stack.pop())
                        previus_token[0] = token
                    else:
                        break
                
                operator_stack.append(token)
                previus_token[0] = token
        
        while operator_stack:
            output_stack.append(operator_stack.pop())
            previus_token[0] = token

        
        #print(f'output stack from infix to postfix = {output_stack}')
        return output_stack


            
    def tree_builder(self, output_stack):
        buffer_stack = []

        for node in output_stack:
            if node not in self.precedence and node not in self.unary: 
                buffer_stack.append(node) # operand or variable
                
            elif node in self.unary:
                right = buffer_stack.pop()
                buffer_stack.append((node, right)) # unary operators
            else:
                right = buffer_stack.pop()
                left = buffer_stack.pop()
                buffer_stack.append((left, node, right)) # binary operators
        # print(f'from tree_builder, buffer stack: {buffer_stack}')        
        return buffer_stack[0]

    # Descriptive SI unit handle - should be improved in the future
    def render_leaf(self, token):
        SI_units = {"m", "s", "kg", "N", "Pa", "J", "W", "A", "V", "C", "F", "H", 'W', 'V', 'Omega', 
}
        m = re.fullmatch(r'(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)([a-zA-Z/^\d]+)?', token)
        if not m:
            return token
        
        val, unit = m.groups()
        if not unit:
            return token
        
        parts = re.split(r'[\/\^]', unit)

        for p in parts:
            if p == '' or p.isdigit():
                continue
            if p not in SI_units:
                return token
        
        return f'{val}\\,\\mathrm{{{unit}}}'

    # Walk the tree and render as latex            
    def tex_render(self, tree):
        # leaf
        if isinstance(tree, str):
            return self.render_leaf(tree)

        if len(tree) == 2:
            node, right = tree
            # Unary
            if node in ('sqrt', 'math.sqrt', 'sympy.sqrt'): 
                return(f'\\sqrt{{{(self.tex_render(right))}}}')
            
            if node in ('cos', 'math.cos', 'sympy.cos'):
                return(f'\\cos{{{right}}}')

            if node in ('sin', 'math.sin', 'sympy.sin'):
                return(f'\\sin{{{(self.tex_render(right))}}}')
            
            if node in ('tan', 'math.tan', 'sympy.tan'):
                return(f'\\tan{{{right}}}')
            
            if node in ('u-'):
                return(f'(-{(self.tex_render(right))})')
            
            if node in ('ln'):
                return(f'\\ln\\left({{{(self.tex_render(right))}}}\\right)')
                
            # fallback
            return f'{node}({self.tex_render((right))})'
        
        else: 
            left, node, right = tree
    
            left_leaf = self.tex_render(left)
            right_leaf = self.tex_render(right)
            
            # Binary
            if node == '-':
                return(f'{left_leaf} - {right_leaf}')
            if node == '+':
                return(f'{left_leaf} + {right_leaf}')
            if node == '*':
                return(f'{left_leaf} \\cdot {right_leaf}')
            if node == '/':
                return(f'\\frac{{{left_leaf}}}{{{right_leaf}}}')
            if node == 'angle':
                return(f'{left_leaf} \\angle {right_leaf}')
            
            if node == '**':
                base_tex = self.tex_render(left)

                if isinstance(left, tuple):
                        base_tex = f'\\left({base_tex}\\right)'

                return f'{base_tex}^{{{right_leaf}}}'
            
            if node == '=':
                return(f'{left_leaf} = {right_leaf}')
            if node == 'res':
                return(f'{left_leaf} = \\underline{{\\underline{{{right_leaf}}}}}')
            

            # Fallback
            return f'{left_leaf}, {node}, {right_leaf}'
            
          
    def pre_fix (self, latex_tree:str) -> str:
        """pre_fix for number presentation"""
        prefix_map = {
            -3: '\\m', # milli
            -6: '\\mu', # micro
            -9: '\\n', # nano
            -12: '\\p' # pico
        }   

        def swap (latex_tree):
            val = latex_tree.group(1)
            exp = int(latex_tree.group(2))
            prefix = prefix_map.get(exp, f'e{exp}')
            return f'{val}{prefix}'
        
        return re.sub(r'(\d+(?:\.\d+)?)e(-?\d+)', swap, latex_tree)

    # find and sub for Greek letters          
    def greek_letters (self, latex_tree:str) -> str:
        """Greek letters for rendereing in latex"""
        symbol_map = {
            'theta': '\\theta',
            'alpha':'\\alpha',
            'alp':'\\alpha',
            'lambda':'\\lambda',
            'kappa': '\\kappa',
            'phi': '\\phi',
            'epsilon': '\\epsilon',
            'mu': '\\mu',
            'Ohm':'\\Omega',
            'Omega':'\\Omega',
            'eta': '\\eta',
            'gamma':'\\gamma',
            'Gamma': '\\Gamma',
            'sigma': '\\Sigma',
            'rho': '\\rho',
            'Delta': '\\Delta',
            'pi': '\\pi',
        }

        pattern = r'[a-zA-Z]+'

        def repl(match):
            word = match.group(0)
            return symbol_map.get(word, word)

        return re.sub(pattern, repl, latex_tree)

    # Handles subscripting for symbolic variables
    def index_handle(self, latex_tree):
        pattern = r'([a-zA-Z0-9,])_([a-zA-Z0-9øØæÆåÅ,]+)'
        return re.sub(pattern, r'\1_{\2}', latex_tree)
    
    # Returns e notation as exponents of 10 for readability 
    def e_notation(self, latex_tree):
        if self.e_notation_onoff == False:
            return latex_tree
        pattern = r'(\d+(?:\.\d+)?)[eE]([+-]?\d+)' 

        return re.sub(
            pattern, lambda m: f'{m.group(1)}\\cdot 10^{{{int(m.group(2))}}}', latex_tree
        )
    def dot_adder(self, latex_tree):
        return re.sub(r'(dot)([A-Za-z])', r'\\dot{\2}', latex_tree)

    
    # call every method needed for parsing + features.
    def all_call(self):
        tokens = self.find_tokens(self.expr)
        postfix = self.infix_to_postfix(tokens)
        tree = self.tree_builder(postfix)
        latex = self.tex_render(tree)
        #latex = self.pre_fix(latex)
        latex = self.greek_letters(latex)
        latex = self.index_handle(latex)
        #latex = self.e_notation(latex)
        latex = self.dot_adder(latex)
        return latex        
    

    # Round entire expression before parsing 
    def _apply_round(self, latex, decimals):
        pattern = r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?'
        self.round_decimals = decimals

        def repl(match):
            n = float(match.group(0))

            if self.e_notation_onoff:

                if n == 0:
                    return '0'

                if abs(n) < 1e-3:
                    return format(n, f'.{decimals+1}g')
                
                if abs(n) >= 1e5:
                    return format(n, f'.{decimals+1}g')
                
                else:
                    return f'{n:.{decimals}f}'.rstrip('0').rstrip('.')
            
            if not self.e_notation_onoff:
                if n == 0:
                    return '0'
                if abs(n) <= 1:
                    exp = math.floor(math.log10(abs(n)))
                    pres = max(decimals - exp - 1, 0)
                    return f'{n:.{pres}f}'.rstrip('0').rstrip('.')
                
                else:
                    return f'{n:.{decimals}f}'.rstrip('0').rstrip('.')


        return re.sub(pattern, repl, latex)

    # Decimals = 2 by defaault
    def round(self, decimals=2):
        """Decimals after decimal point"""
        self._round_decimals = decimals
        return self

