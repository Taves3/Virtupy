import ast, uuid

def build_vobject_ast():
    return  ast.ClassDef(
                name="Vobject",
                bases=[],
                keywords=[],
                decorator_list=[],
                body=[
                    # __new__
                    ast.FunctionDef(
                        name="__new__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[
                                ast.arg(arg="cls"),
                            ],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                            vararg=ast.arg(arg="args"),
                            kwarg=ast.arg(arg="kwargs"),
                        ),
                        body=[
                            ast.Assign(
                                targets=[ast.Name(id="self", ctx=ast.Store())],
                                value=ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Call(
                                            func=ast.Name(id="super", ctx=ast.Load()),
                                            args=[],
                                            keywords=[]
                                        ),
                                        attr="__new__",
                                        ctx=ast.Load()
                                    ),
                                    args=[ast.Name(id="cls", ctx=ast.Load())],
                                    keywords=[]
                                )
                            ),
                            ast.Assign(
                                targets=[
                                    ast.Attribute(
                                        value=ast.Name(id="self", ctx=ast.Load()),
                                        attr="__vdict__",
                                        ctx=ast.Store()
                                    )
                                ],
                                value=ast.Dict(keys=[], values=[])
                            ),
                            ast.Return(value=ast.Name(id="self", ctx=ast.Load()))
                        ],
                        decorator_list=[]
                    ),

                    # __init__
                    ast.FunctionDef(
                        name="__init__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="self")],
                            vararg=ast.arg(arg="args"),
                            kwarg=ast.arg(arg="kwargs"),
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Pass()],
                        decorator_list=[]
                    ),

                    # __del__
                    ast.FunctionDef(
                        name="__del__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="self")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Pass()],
                        decorator_list=[]
                    ),

                    # __repr__
                    ast.FunctionDef(
                        name="__repr__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="self")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[
                            ast.Return(
                                value=ast.JoinedStr(values=[
                                    ast.Constant(value="<Vobject at "),
                                    ast.FormattedValue(
                                        value=ast.Call(
                                            func=ast.Name(id="hex", ctx=ast.Load()),
                                            args=[
                                                ast.Call(
                                                    func=ast.Name(id="id", ctx=ast.Load()),
                                                    args=[ast.Name(id="self", ctx=ast.Load())],
                                                    keywords=[]
                                                )
                                            ],
                                            keywords=[]
                                        ),
                                        conversion=-1
                                    ),
                                    ast.Constant(value=">")
                                ])
                            )
                        ],
                        decorator_list=[]
                    ),

                    # __str__
                    ast.FunctionDef(
                        name="__str__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="self")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[
                            ast.Return(
                                value=ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Name(id="self", ctx=ast.Load()),
                                        attr="__repr__",
                                        ctx=ast.Load()
                                    ),
                                    args=[],
                                    keywords=[]
                                )
                            )
                        ],
                        decorator_list=[]
                    ),

                    # __getattribute__
                    ast.FunctionDef(
                        name="__getattribute__",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="self"), ast.arg(arg="name")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[
                            ast.If(
                                test=ast.BoolOp(
                                    op=ast.And(),
                                    values=[
                                        ast.Call(
                                            func=ast.Attribute(
                                                value=ast.Name(id="name", ctx=ast.Load()),
                                                attr="startswith",
                                                ctx=ast.Load()
                                            ),
                                            args=[ast.Constant("__")],
                                            keywords=[]
                                        ),
                                        ast.Call(
                                            func=ast.Attribute(
                                                value=ast.Name(id="name", ctx=ast.Load()),
                                                attr="endswith",
                                                ctx=ast.Load()
                                            ),
                                            args=[ast.Constant("__")],
                                            keywords=[]
                                        )
                                    ]
                                ),
                                body=[
                                    ast.Return(
                                        value=ast.Call(
                                            func=ast.Attribute(
                                                value=ast.Call(
                                                    func=ast.Name(id="super", ctx=ast.Load()),
                                                    args=[],
                                                    keywords=[]
                                                ),
                                                attr="__getattribute__",
                                                ctx=ast.Load()
                                            ),
                                            args=[ast.Name(id="name", ctx=ast.Load())],
                                            keywords=[]
                                        )
                                    )
                                ],
                                orelse=[]
                            ),
                            ast.Assign(
                                targets=[ast.Name(id="vdict", ctx=ast.Store())],
                                value=ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Call(
                                            func=ast.Name(id="super", ctx=ast.Load()),
                                            args=[],
                                            keywords=[]
                                        ),
                                        attr="__getattribute__",
                                        ctx=ast.Load()
                                    ),
                                    args=[ast.Constant("__vdict__")],
                                    keywords=[]
                                )
                            ),
                            ast.If(
                                test=ast.Compare(
                                    left=ast.Name(id="name", ctx=ast.Load()),
                                    ops=[ast.In()],
                                    comparators=[ast.Name(id="vdict", ctx=ast.Load())]
                                ),
                                body=[
                                    ast.Return(
                                        value=ast.Subscript(
                                            value=ast.Name(id="vdict", ctx=ast.Load()),
                                            slice=ast.Name(id="name", ctx=ast.Load()),
                                            ctx=ast.Load()
                                        )
                                    )
                                ],
                                orelse=[]
                            ),
                            ast.Raise(
                                exc=ast.Call(
                                    func=ast.Name(id="AttributeError", ctx=ast.Load()),
                                    args=[ast.Name(id="name", ctx=ast.Load())],
                                    keywords=[]
                                ),
                                cause=None
                            )
                        ],
                        decorator_list=[]
                    ),
                ]
            )

class VirtualSelf:
    def __init__(self, cls: ast.ClassDef, interpreter):
        self.interpreter = interpreter
        self.node = cls
        self.binds = {}
    
    def bind(self, proxy):
        print(f"added bind {proxy._iid} to {self}")
        self.binds[proxy._iid] = proxy
    
    def __repr__(self):
        return f"<'VSelf' for class '{self.node.name}'>"

class ClassProxyInstance:
    def __init__(self, vclass: "Vclass", args):
        self.cls = vclass.vself
        self.vclass: Vclass = vclass
        self.args = args
        self._iid = str(uuid.uuid4())
        self.mempos = hex(self.cls.interpreter.cpi)
        self.attributes = {"__class__": self.__class__}
    
    @property
    def __class__(self):
        return f"<{self.cls.interpreter.name}.{self.vclass.body.name} object at {self.mempos}>"

    def __repr__(self):
            return self.__class__

class Vfunction:
    def __init__(self, body: ast.FunctionDef, cls: "Vclass", memorypos: int):
        self.body = body
        self.cls = cls
        self.args = body.args.args
        self.mempos = hex(memorypos)
        self.attributes = {"__class__": self.__class__, "__repr__": self.__repr__}
    
    @property
    def __class__(self):
        return f"<function {self.body.name} at {self.mempos}>"
    
    def __repr__(self):
        return self.__class__

class Vclass:
    def __init__(self, body: ast.ClassDef, funcs: dict[str, Vfunction], memorypos: int):
        self.vself: VirtualSelf = None
        self.body = body
        self.funcs = funcs
        self.mempos = hex(memorypos)
        self.attributes = {"__class__": self.__class__, "__repr__": self.__repr__}
    
    @property
    def __class__(self):
        return f"<class '__main__.{self.body.name}'>"

    def __repr__(self):
        return self.__class__

class forge_classdef:
    def __init__(self, name: str):
        self.name = name
        self.bases = []
        self.body = [

        ]
        self.decorator_list = []

class forge_functiondef:
    def __init__(self, name: str):
        self.name = name
        self.args = ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
        self.body = []
        self.decorator_list = []

class ReturnSignal:
    def __init__(self, value):
        self.value = value
