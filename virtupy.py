import ast
import dictreader
from classes import *
from filesystem import Environment

VobjectNode = build_vobject_ast()

class Interpreter(ast.NodeVisitor):
    def __init__(self, builtins: dict, name: str | None = None, debug: bool = False):
        self.memory_stack = [{}]
        self.builtins = builtins
        self.unsafe = ['__repr__', '__str__', '__int__', '__float__', '__subclasses__']

        self.debug = False

        _name = name if name != None else "__main__"
        self.name = _name

        self.cpi = 1467090845520

        obj = Vclass(VobjectNode, {}, 0)
        obj.vself = VirtualSelf(VobjectNode, self)
        self.memory[VobjectNode.name] = obj
        for func in VobjectNode.body:
            if isinstance(func, ast.FunctionDef):
                self.add_class_func(func, obj)
            else:
                self.visit(func)

        self.globalscope = {}
        self.globalscope["str"]   = Vclass(forge_classdef("str")  , {**obj.funcs}, 1)
        self.globalscope["int"]   = Vclass(forge_classdef("int")  , {**obj.funcs}, 2)
        self.globalscope["float"] = Vclass(forge_classdef("float"), {**obj.funcs}, 3)
        self.globalscope["list"]  = Vclass(forge_classdef("list") , {**obj.funcs}, 4)
        self.globalscope["dict"]  = Vclass(forge_classdef("dict") , {**obj.funcs}, 5)
        self.globalscope["None"]  = Vclass(forge_classdef("None") , {**obj.funcs}, 6)

        self.memory.update(self.globalscope)

        self.add_vself(self.memory["str"]   )
        self.add_vself(self.memory["int"]   )
        self.add_vself(self.memory["float"] )
        self.add_vself(self.memory["list"]  )
        self.add_vself(self.memory["dict"]  )
        self.add_vself(self.memory["None"]  )

        self.system_variables = {'__name__': self.instance(self.memory["str"], _name)}
        self.debug = debug
  
    @property
    def memory(self):
        return self.memory_stack[-1]
    
    def instance(self, cls, args):
        return ClassProxyInstance(cls, args)

    def add_vself(self, cls):
        cls.vself = VirtualSelf(cls.body, self)

    def Vstr(self, value):
        return self.instance(self.memory["str"], value)

    def VNone(self):
        return self.instance(self.memory["None"], ())

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Delete(self, node):
        # node.target
        targets = node.targets
        for target in targets:
            if isinstance(target, ast.Name):
                self.memory.pop(target.id, None)
            elif isinstance(target, ast.Attribute):
                obj = self.visit(target.value)
                obj.attributes.pop(target.attr, None)

        return self.VNone()
    
    def visit_Assign(self, node):
        value = self.visit(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.memory[target.id] = value
            elif isinstance(target, ast.Attribute):
                target: ast.Attribute
                s: ClassProxyInstance = self.visit(target.value)
                s.attributes[target.attr] = value

    def visit_Constant(self, node):
        value = node.value
        if isinstance(value, int):
            return self.Vint(value)
        if isinstance(value, float):
            return self.Vfloat(value)
        if isinstance(value, str):
            return self.Vstr(value)
        if value == None:
            return self.VNone()
        raise ValueError(f"Type {value} not supported")

    def visit_BinOp(self, node):
        a = self.visit(node.left)
        b = self.visit(node.right)
        op = node.op
        result = 0
        if isinstance(op, ast.Add):
            result = a + b
        elif isinstance(op, ast.Sub):
            result = a - b
        elif isinstance(op, ast.Div):
            result = a / b
        elif isinstance(op, ast.Mult):
            result = a * b
        elif isinstance(op, ast.FloorDiv):
            result = a // b
        else:
            raise TypeError(f"type {type(op)} not supported in BinOp")
        return result

    def visit(self, node):
        if self.debug: print(f"[+] {node.__class__.__name__} {node.__dict__}")
        method = "visit_" + node.__class__.__name__
        func = getattr(self, method, None)

        if not func:
            raise NotImplementedError(f"No visitor for {node.__class__.__name__}")

        return func(node)

    def visit_FunctionDef(self, node):
        self.cpi += 23345
        self.memory[node.name] = Vfunction(node, None, self.cpi)

    def add_class_func(self, node: ast.FunctionDef, cls: "Vclass"):
        #print(f"[+] {node.__class__.__name__} {node.__dict__}")
        self.cpi += 23345
        func = Vfunction(node, cls, self.cpi)
        cls.funcs[node.name] = func

    def visit_ClassDef(self, node):
        self.cpi += 36666
        new = Vclass(node, {}, self.cpi)
        new.vself = VirtualSelf(node, self)
        self.memory[node.name] = new
        for func in node.body:
            if isinstance(func, ast.FunctionDef):
                self.add_class_func(func, new)
            else:
                self.visit(func)

    def visit_withitem(self, node):
        value = self.visit(node.context_expr)
        if node.optional_vars:
            alias = self.visit(node.optional_vars)
            self.memory[alias] = value
            return alias

    def visit_With(self, node):
        names = []
        for item in node.items:
            name = self.visit(item)
            names.append(name)
        for stmt in node.body:
            self.visit(stmt)

        for name in names:
            self.memory.pop(name)

    def visit_Try(self, node):
        try:
            for stmt in node.body:
                self.visit(stmt)
        except:
            for handler in node.handlers:
                self.visit(handler)
    
    def visit_ExceptHandler(self, node):
        if self.debug:
            print(node.__dict__)
            print("Name",[self.visit(n) for n in node.body])
    
    def visit_alias(self, node):
        if self.debug:
            print(node.__dict__)
            print("ALIAS ^")

    def visit_Attribute(self, node):
        #print(node.attr)
        s = self.visit(node.value)
        a = node.attr
        if a not in s.attributes: raise AttributeError(f"Attribute '{a}' not found")
        attr = s.attributes[a]
        
        return attr

    def visit_Dict(self, node):
        new = {}
        for key, item in zip(node.keys, node.values):
            new[self.visit(key)] = self.visit(item)
        return self.Vdict(new)
    
    def visit_Subscript(self, node):
        di = self.visit(node.value)
        return di[self.visit(node.slice)]

    def func(self, func_node: "Vfunction", args: list):
        local_scope = {**self.globalscope}
        for arg, value in zip(func_node.args, args, strict=True):
            name = arg.arg
            local_scope[name] = value
        
        self.memory_stack.append(local_scope)

        output = self.VNone()
        for stmt in func_node.body.body:
            value = self.visit(stmt)
            if isinstance(value, ReturnSignal):
                output = value.value
                break

        self.memory_stack.pop()
        return output

    def visit_Return(self, node):
        return ReturnSignal(self.visit(node.value) if node.value else self.VNone())

    def visit_List(self, node):
        return self.Vlist([self.visit(item) for item in node.elts])

    def visit_Str(self, node):
        return self.Vstr(node.value)

    def visit_FormattedValue(self, node):
        value = self.visit(node.value)
        return value
    
    def visit_JoinedStr(self, node):
        joined = ''
        for val in node.values:
            value = self.visit(val)
            joined += str(value)
        return self.Vstr(joined)
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            return node.id
        sv = self.system_variables.get(node.id)
        if sv != None:
            return sv
        if node.id not in self.memory:
            raise NameError(f"Global {node.id!r} not found")
        return self.memory[node.id]
    
    def visit_arg(self, node):
        return node.arg

    def visit_Expr(self, node):
        return self.visit(node.value)
    
    def visit_Unsafe(self, value, func_name):
        if func_name in self.unsafe:
            if func_name == '__repr__':
                return self.Vstr(value)
            elif func_name == '__str__':
                return self.Vstr(value)
            elif func_name == '__int__':
                return self.Vint(value)
        else:
            return value

    def visit_Global(self, node):
        if self.debug: print(node.__dict__) # ????
        return

    def visit_Call(self, node):
        # evaluate args first
        args_evaluated = [self.visit(arg) for arg in node.args]

        if isinstance(node.func, ast.Attribute):
            proxy = self.visit(node.func.value)
            func_name = node.func.attr

            if isinstance(proxy, ClassProxyInstance):
                proxy: ClassProxyInstance
                vclass = proxy.vclass
                func = vclass.funcs[func_name]
                value = self.func(func, [proxy] + args_evaluated)
                return self.visit_Unsafe(value, func_name)
            
            if isinstance(proxy, Sandbox):
                proxy: Sandbox
                if node.func.attr in proxy.safe:
                    return proxy.__getattribute__(node.func.attr)(*args_evaluated)
                return self.VNone()
            
            if isinstance(proxy, VIO):
                attr = getattr(proxy, func_name)
                value = attr(*args_evaluated)
                return self.visit_Unsafe(value, func_name)
            
            print(proxy, type(proxy), func_name)
            
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            bt = self.builtins.get(func_name)
            if bt:
                # builtin function call
                return bt(*args_evaluated)
            
            func_node = self.memory_stack[0].get(func_name)

            # user function call
            if isinstance(func_node, Vfunction):
                return self.func(func_node, args_evaluated)
            
            if isinstance(func_node, Vclass):
                class_node = func_node.body
                if class_node.name == func_name:
                    proxy = ClassProxyInstance(func_node, args_evaluated)
                    func_node.vself.bind(proxy)
                    init = func_node.funcs["__init__"]

                    self.func(init, [proxy] + args_evaluated)
                    self.cpi += 35996
                    return proxy

        # else: not supported yet
        raise RuntimeError("Unsupported call type", node.func)

class Sandbox:
    def __init__(self):
        self.interpreter = None
    
    def set_interpreter(self, interpreter):
        self.interpreter = interpreter

    def dump_memory(self):
        print(self.interpreter.memory)

class VirtuePy:
    def __init__(self):
        self._compiled = None
        self._source = ''
        self.environment = Environment()
        self.console = ""
        self.sandbox = Sandbox()
        self.builtins = {
            'repr': self.repr,
            'print': self.print, 'open': self.environment.open,
        }
        self.interpreter = Interpreter(builtins=self.builtins, debug=True)
        self.sandbox.set_interpreter(self.interpreter)

    def repr(self, obj: object, /):
        return obj.__repr__()

    def compile(self, code: str):
        self._source = code
        try:
            # compile(code, "<unknown>", "exec", 1024, _feature_version=-1)
            tree = ast.parse(code)
            self._compiled = tree
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error while compiling: {e}")
        return True
    
    def print(self, *values: object, sep: str | None = " ", end: str | None = "\n", file: None = None, flush: False = False) -> None:
        result = ''
        for value in values:
            result += str(value) + str(sep)
        self.console += result[:-1] + str(end)
        return None

    def run(self, *, extra_globals=None):
        if self._compiled is None:
            raise RuntimeError("No compiled code. Call compile(code) first.")

        sandbox_globals = {
            '__builtins__': self.builtins,
        }
        if extra_globals:
            sandbox_globals.update(extra_globals)
        #try:
        #    self.interpreter.visit(self._compiled)
        #except Exception as e:
        #    self.console = f"Error during execution: {e}"
        self.interpreter.visit(self._compiled)
        return Compiled(console=self.console, memory_snapshot=self.interpreter.memory, files=self.environment.tree())

class Compiled:
    def __init__(self, console: str, memory_snapshot: dict, files: list):
        self.console = console
        self.files = files
        self.memory_dump = memory_snapshot

# ----------- Example usage --------------
if __name__ == "__main__":
    code = r"""

def _repr(obj):
    return obj.__repr__()

print(_repr("Hello"))
""" 
    
    compiler = VirtuePy()
    compiler.compile(code)
    result = compiler.run()
    print("Console:")
    print(result.console)
    print("File System:")
    print(result.files)
    print("Memory Dump:")
    print(dictreader.read(result.memory_dump))

    # TODO: Update the environment and folders and files
    
    # [IGNORE] make a minecraft server in a way that runs on another computer and is just transmitted to any other computer
