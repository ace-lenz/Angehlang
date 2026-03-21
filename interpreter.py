import sys
import copy
import time
import re
import os
import json

# ─── ANSI Colour Palette ────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    MAGENTA= "\033[95m"
    BLUE   = "\033[94m"
    DIM    = "\033[2m"


ANGEH_VERSION = "2.1.0"
ANGEH_AUTHOR  = "Longbian Lennon"


class Symbol(str): pass

ENTANGLED_GROUPS = {}
ENTANGLED_GROUPS_MAP = {}
CHECKPOINTS = {}

def tokenize(code):
    """Splits the code into tokens properly handling strings."""
    # handle comments
    code = '\n'.join(line.split(';')[0] for line in code.split('\n'))
    # token splits: strings, parens, quotes, or contiguous other characters
    token_pattern = r'(?:"[^"]*")|\(|\)|\'|[^\s()]+'
    return re.findall(token_pattern, code)

paren_counter = 0

def parse_from_tokens(tokens):
    """Parses a list of tokens into an AST."""
    global paren_counter
    if not tokens:
        return None
    token = tokens.pop(0)
    # print(f"Token: {token}, Counter: {paren_counter}")
    if token == "'":
        return ['quote', parse_from_tokens(tokens)]
    if token == '(':
        paren_counter += 1
        ast = []
        while tokens and tokens[0] != ')':
            ast.append(parse_from_tokens(tokens))
        if not tokens:
            raise SyntaxError("Unexpected EOF, missing ')'")
        tokens.pop(0)  # Pop ')'
        paren_counter -= 1
        return ast
    elif token == ')':
        paren_counter -= 1
        raise SyntaxError(f"Unexpected ')', next tokens: {tokens[:5]}")
    else:
        return atom(token)

def atom(token):
    """Converts a token into a number, a literal string, or a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            if token.startswith('"') and token.endswith('"'):
                return str(token[1:-1]) # Literal string, stripped of quotes
            return Symbol(token) # Variable or function symbol

class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env."""
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer
        self._updating_entanglement = False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        state_key = f"{id(self)}_{key}"
        if state_key in ENTANGLED_GROUPS and not self._updating_entanglement:
            self._updating_entanglement = True
            group_id = ENTANGLED_GROUPS[state_key]
            for e, k in ENTANGLED_GROUPS_MAP[group_id]:
                if e is not self or k != key:
                    e[k] = value
            self._updating_entanglement = False

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            return None


def pretty_print_ast(ast, indent=0):
    if isinstance(ast, list):
        print(' ' * indent + '(')
        for i, item in enumerate(ast):
            pretty_print_ast(item, indent + 2)
        print(' ' * indent + ')')
    else:
        print(' ' * indent + str(ast))

def evaluate(x, env):
    """Evaluates an expression in an environment."""
    if isinstance(x, Symbol):      # variable reference
        env_found = env.find(x)
        if env_found is None:
             # Fallback edge case, return symbol as standard string
            return str(x)
        return env_found[x]
    elif not isinstance(x, list):  # constant literal (int, float, string)
        return x
    op, *args = x
    if op == 'quote':
        return args[0]
    if op in special_forms:
        return special_forms[op](args, env)
    else:
        proc = evaluate(op, env)
        if hasattr(proc, '__len__') and len(proc) > 0 and proc[0] == 'macro':
            _, params, body = proc
            local_env = Env(params, args, env)
            expanded = None
            for expr in body:
                expanded = evaluate(expr, local_env)
            return evaluate(expanded, env)
            
        vals = [evaluate(arg, env) for arg in args]
        if callable(proc):
            return proc(*vals)
        elif isinstance(proc, list) and proc[0] == 'lambda':
            _, params, body = proc
            val = None
            for expr in body:
                val = evaluate(expr, Env(params, vals, env))
            return val
        else:
            raise TypeError(f"{proc} is not a function")

def let_form(args, env):
    bindings = args[0]
    body = args[1:]
    local_env = Env(outer=env)
    for var, val_expr in bindings:
        local_env[var] = evaluate(val_expr, local_env)
    
    val = None
    for expr in body:
        val = evaluate(expr, local_env)
    return val

def begin_form(args, env):
    val = None
    for expr in args:
        val = evaluate(expr, env)
    return val

def def_form(args, env):
    var, val_expr = args
    val = evaluate(val_expr, env)
    env[var] = val

def defn_form(args, env):
    name, params, *body = args
    env[name] = ['lambda', params, body]

def set_form(args, env):
    var, val_expr = args
    env.find(var)[var] = evaluate(val_expr, env)

def inc_form(args, env):
    var = args[0]
    env.find(var)[var] += 1

def cond_form(args, env):
    for clause in args:
        test = clause[0]
        if test == 'else' or evaluate(test, env):
            res = None
            for expr in clause[1:]:
                res = evaluate(expr, env)
            return res
    return None

def while_form(args, env):
    condition, body = args
    val = None
    while evaluate(condition, env):
        val = evaluate(body, env)
    return val

def if_form(args, env):
    if len(args) == 3:
        condition, then_expr, else_expr = args
        if evaluate(condition, env):
            return evaluate(then_expr, env)
        else:
            return evaluate(else_expr, env)
    elif len(args) == 2:
        condition, then_expr = args
        if evaluate(condition, env):
            return evaluate(then_expr, env)
        else:
            return None

def dolist_form(args, env):
    var_list, body = args
    var, l = var_list
    for item in evaluate(l, env):
        local_env = Env(outer=env)
        local_env[var] = item
        evaluate(body, local_env)

def and_form(args, env):
    val = True
    for arg in args:
        val = evaluate(arg, env)
        if not val:
            return False
    return val

def or_form(args, env):
    val = False
    for arg in args:
        val = evaluate(arg, env)
        if val:
            return True
    return val

def entangle_form(args, env):
    group_id = time.time()
    ENTANGLED_GROUPS_MAP[group_id] = []
    for sym in args:
        if isinstance(sym, list) and sym[0] == 'quote': sym = sym[1]
        found_env = env.find(sym)
        if not found_env:
            env[sym] = None
            found_env = env
        state_key = f"{id(found_env)}_{sym}"
        ENTANGLED_GROUPS[state_key] = group_id
        ENTANGLED_GROUPS_MAP[group_id].append((found_env, sym))
    return True

def checkpoint_form(args, env):
    name = evaluate(args[0], env) if isinstance(args[0], list) else args[0]
    if isinstance(name, list) and name[0] == 'quote': name = name[1]
    CHECKPOINTS[name] = {k: copy.deepcopy(v) for k, v in env.items() if not callable(v) and not str(k).startswith('__')}
    print(f"⏳ [TIME-TRAVEL] Checkpoint saved: '{name}'")
    return name

def rewind_form(args, env):
    name = evaluate(args[0], env) if isinstance(args[0], list) else args[0]
    if isinstance(name, list) and name[0] == 'quote': name = name[1]
    if name in CHECKPOINTS:
        env.update(copy.deepcopy(CHECKPOINTS[name]))
        print(f"⏱️ [TIME-TRAVEL] Time rewound to checkpoint: '{name}'")
        return True
    return False
    
def map_form(args, env):
    fn_expr, list_expr = args
    f = evaluate(fn_expr, env)
    l = evaluate(list_expr, env)
    return [_angeh_call(f, [x], env) for x in l]

def filter_form(args, env):
    fn_expr, list_expr = args
    f = evaluate(fn_expr, env)
    l = evaluate(list_expr, env)
    return [x for x in l if _angeh_call(f, [x], env)]

def foreach_form(args, env):
    fn_expr, list_expr = args
    f = evaluate(fn_expr, env)
    l = evaluate(list_expr, env)
    for x in l:
        _angeh_call(f, [x], env)
    return None

_LOADED_MODULES = set()

def _import_form(args, env):
    """Load a stdlib or local .angeh module by name, evaluating it into the current env."""
    module_name = str(args[0])
    if module_name in _LOADED_MODULES:
        return module_name  # already loaded, skip re-evaluation

    # Search paths: stdlib/ dir relative to this file, then cwd
    base = os.path.dirname(os.path.abspath(__file__))
    search_paths = [
        os.path.join(base, "..", "stdlib", f"{module_name}.angeh"),
        os.path.join(base, "..", "stdlib", f"{module_name.replace('-','_')}.angeh"),
        os.path.join(os.getcwd(), f"{module_name}.angeh"),
    ]

    for path in search_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            tokens = tokenize(code)
            while tokens:
                try:
                    expr = parse_from_tokens(tokens)
                    if expr is not None:
                        evaluate(expr, env)
                except Exception as e:
                    print(f"{C.YELLOW}⚠  [import {module_name}] {e}{C.RESET}")
            _LOADED_MODULES.add(module_name)
            print(f"{C.DIM}  ↳ loaded module '{module_name}'{C.RESET}")
            return module_name

    print(f"{C.YELLOW}⚠  Module '{module_name}' not found in stdlib/{C.RESET}")
    return None

def _defmodule_form(args, env):
    """Register a module name (used in stdlib files to declare their identity)."""
    module_name = str(args[0])
    env[f"__module__"] = module_name
    return module_name

special_forms = {
    'let': let_form,
    'let*': let_form, # for now, same as let
    'begin': begin_form,
    'def': def_form,
    'def-fn': defn_form,
    'set!': set_form,
    'inc!': inc_form,
    'def-const': def_form,
    'def-type': lambda args, env: None,
    'struct': lambda args, env: None,
    'def-module': _defmodule_form,
    'import': _import_form,
    'cond': cond_form,
    'while': while_form,
    'if': if_form,
    'dolist': dolist_form,
    'and': and_form,
    'or': or_form,
    'def-macro': lambda args, env: env.__setitem__(args[0], ['macro', args[1], args[2:]]),
    'entangle': entangle_form,
    'checkpoint': checkpoint_form,
    'rewind': rewind_form,
    'lambda': lambda args, env: ['lambda', args[0], args[1:]],
    'map': map_form,
    'filter': filter_form,
    'for-each': foreach_form,
}


class VM:
    def __init__(self, bytecode, opcodes):
        self.stack = []
        self.ip = 0
        self.bytecode = bytecode
        self.opcodes = opcodes

    def run(self):
        while self.ip < len(self.bytecode):
            opcode = self.bytecode[self.ip]
            self.ip += 1

            if opcode == self.opcodes['OP_HALT']:
                break
            elif opcode == self.opcodes['OP_PUSH']:
                value = self.bytecode[self.ip]
                self.stack.append(value)
                self.ip += 1
            elif opcode == self.opcodes['OP_POP']:
                self.stack.pop()
            elif opcode == self.opcodes['OP_ADD']:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif opcode == self.opcodes['OP_SUB']:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            else:
                raise Exception(f"Unknown opcode: {opcode}")

AGENTS_REGISTRY = {}
A2A_OMNIBUS = []

# Provider endpoints tried in order
_AI_PROVIDERS = [
    {"name": "Ollama",  "url": "http://localhost:11434/api/generate",  "key": None,       "style": "ollama"},
    {"name": "LMStudio","url": "http://localhost:1234/v1/chat/completions","key": None,    "style": "openai"},
]

def _build_context_prompt(agent):
    """Build a context-aware prompt string from the full memory window."""
    mem_window = agent["memory"][-20:]  # last 20 turns
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in mem_window)

def _call_ai(agent, prompt):
    """Try each AI provider in order and return (reply, provider_name)."""
    import urllib.request
    context = _build_context_prompt(agent)
    full_prompt = f"{context}\nUSER: {prompt}" if context else prompt

    for provider in _AI_PROVIDERS:
        try:
            if provider["style"] == "ollama":
                body = json.dumps({
                    "model": agent.get("model", "llama3"),
                    "prompt": full_prompt,
                    "system": agent["prompt"],
                    "stream": False
                }).encode()
                req = urllib.request.Request(provider["url"], data=body,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=5) as r:
                    return json.loads(r.read()).get("response", "").strip(), provider["name"]
            elif provider["style"] == "openai":
                messages = [{"role": "system", "content": agent["prompt"]}]
                messages += agent["memory"][-10:]
                messages.append({"role": "user", "content": prompt})
                body = json.dumps({"model": agent.get("model","local-model"), "messages": messages}).encode()
                headers = {"Content-Type": "application/json"}
                if provider["key"]:
                    headers["Authorization"] = f"Bearer {provider['key']}"
                req = urllib.request.Request(provider["url"], data=body, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    return data["choices"][0]["message"]["content"].strip(), provider["name"]
        except Exception:
            continue

    return None, None  # all providers failed

def agent_spawn(name, system_prompt, model=None, tags=None):
    """Instantiate a named AI agent with optional model and classification tags."""
    print(f"{C.MAGENTA}🧬 [AGENT-SPAWN]{C.RESET} Instantiating: {C.CYAN}'{name}'{C.RESET}")
    AGENTS_REGISTRY[name] = {
        "prompt": system_prompt,
        "model":  model or "llama3",
        "tags":   tags or [],
        "memory": [],
        "spawned_at": time.time(),
    }
    return name

def agent_ask(name, prompt):
    """Query a named agent, maintaining full conversation context."""
    if name not in AGENTS_REGISTRY:
        return f"Error: Agent '{name}' not found. Spawn it first with agent-spawn."
    agent = AGENTS_REGISTRY[name]
    print(f"{C.CYAN}🧠 [AGENT-ASK]{C.RESET} Querying {C.BOLD}'{name}'{C.RESET}...")

    reply, provider = _call_ai(agent, prompt)

    if reply:
        print(f"  {C.DIM}[via {provider}]{C.RESET}")
        agent["memory"].append({"role": "user",      "content": prompt})
        agent["memory"].append({"role": "assistant", "content": reply})
        return reply
    else:
        mock = (f"[Mock • {name}] No LLM provider reachable. "
                f"Start Ollama (`ollama serve`) or LM Studio for real responses.")
        agent["memory"].append({"role": "assistant", "content": mock})
        print(f"  {C.YELLOW}[Mock fallback]{C.RESET}")
        return mock

def agent_forget(name, keep_last=0):
    """Clear an agent's memory, optionally keeping the last N exchanges."""
    if name not in AGENTS_REGISTRY: return False
    if keep_last:
        AGENTS_REGISTRY[name]["memory"] = AGENTS_REGISTRY[name]["memory"][-keep_last*2:]
    else:
        AGENTS_REGISTRY[name]["memory"] = []
    return True

def agent_recall(name, n=5):
    """Return the last N user/assistant pairs from an agent's memory as JSON."""
    if name not in AGENTS_REGISTRY: return "[]"
    return json.dumps(AGENTS_REGISTRY[name]["memory"][-n*2:], indent=2)

def agent_list():
    """Return a JSON summary of all active agents."""
    summary = {
        k: {"model": v["model"], "tags": v["tags"], "memory_len": len(v["memory"])}
        for k, v in AGENTS_REGISTRY.items()
    }
    return json.dumps(summary, indent=2)

def agent_clone(source_name, new_name):
    """Fork an existing agent's system prompt into a new agent."""
    if source_name not in AGENTS_REGISTRY:
        return f"Error: Source agent '{source_name}' not found."
    src = AGENTS_REGISTRY[source_name]
    agent_spawn(new_name, src["prompt"], model=src["model"], tags=list(src["tags"]))
    return new_name

def a2a_broadcast(message, target="ALL", sender="SYSTEM"):
    """Broadcast a message to all or specific agents and persist to disk."""
    packet = {
        "sender": sender, "target": target,
        "message": message, "timestamp": time.time()
    }
    A2A_OMNIBUS.append(packet)
    print(f"{C.BLUE}🌐 [A2A]{C.RESET} {C.BOLD}{sender}{C.RESET} → {C.CYAN}{target}{C.RESET}: {message}")
    for agent_name, agent in AGENTS_REGISTRY.items():
        if target == "ALL" or target == agent_name:
            agent["memory"].append({"role": "user",
                "content": f"[A2A from {sender}]: {message}"})
    # Persist to disk for post-hoc analysis
    try:
        with open("a2a_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(packet) + "\n")
    except Exception:
        pass
    return True

def intend_proc(intent, data):
    """Use AI to infer and apply an action based on natural language intent."""
    print(f"{C.MAGENTA}🔮 [INTENT]{C.RESET} Resolving: '{C.YELLOW}{intent}{C.RESET}' on {data}")
    core = "__INTENT_CORE__"
    if core not in AGENTS_REGISTRY:
        agent_spawn(core,
            "You are the Angehlang Intent Resolver. "
            "Given an intent and data, return ONLY the processed output — "
            "no explanation, no markdown, just the result.")
    res = agent_ask(core, f"Intent: {intent}\nData: {data}\nOutput:")

    if "[Mock" in res:
        intent_lc = str(intent).lower()
        if "sort"    in intent_lc: return sorted(data) if isinstance(data, list) else data
        if "reverse" in intent_lc: return list(reversed(data)) if isinstance(data, list) else data
        if "double"  in intent_lc: return [x*2 for x in data] if isinstance(data, list) else data*2
        if "upper"   in intent_lc: return str(data).upper()
        if "lower"   in intent_lc: return str(data).lower()
        if "sum"     in intent_lc: return sum(data) if isinstance(data, list) else data
        return data
    return res


def _angeh_call(f, vals, global_env):
    """Invoke an Angehlang function (Python callable or lambda-list) with given arg values."""
    if callable(f):
        return f(*vals)
    elif isinstance(f, list) and len(f) > 0 and f[0] == 'lambda':
        _, params, body = f
        local_env = Env(params, vals, global_env)  # inherit all builtins
        result = None
        for expr in body:
            result = evaluate(expr, local_env)
        return result
    else:
        raise TypeError(f"Not a function: {f}")


def create_global_env():
    """A default environment with some Scheme-like procedures."""
    env = Env()
    env.update({
        'agent-spawn':  agent_spawn,
        'agent-ask':    agent_ask,
        'agent-forget': agent_forget,
        'agent-recall': agent_recall,
        'agent-list':   agent_list,
        'agent-clone':  agent_clone,
        'a2a-broadcast': a2a_broadcast,
        'intend': intend_proc,
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '=': lambda a, b: a == b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        'print': print,
        'new-list': lambda: [],
        'add!': lambda l, x: l.append(x),
        'add-token!': lambda l, x: l.append(x),
        'get': lambda x, i: x.get(i) if isinstance(x, dict) else x[i],
        '.': lambda x, i: x.get(i) if isinstance(x, dict) else x[i],
        'is-whitespace?': lambda c: c.isspace(),
        'is-digit?': lambda c: c.isdigit(),
        'is-letter?': lambda c: c.isalpha(),
        'is-alphanumeric?': lambda c: c.isalnum(),
        'is-symbol?': lambda x: isinstance(x, str),
        'is-string?': lambda x: isinstance(x, str),
        'is-char?': lambda x: isinstance(x, str) and len(x) == 1,
        'char-code': ord,
        'code-char': chr,
        'string->symbol': lambda s: s,
        'symbol->string': lambda s: s,
        'string-append': lambda *args: "".join(args),
        'string-length': len,
        'string-ref': lambda s, i: s[i],
        'make-string': lambda k, c: c * k,
        'string-copy': lambda s: s,
        'string=?': lambda s1, s2: s1 == s2,
        'string-ci=?': lambda s1, s2: s1.lower() == s2.lower(),
        'string<?': lambda s1, s2: s1 < s2,
        'string-ci<?': lambda s1, s2: s1.lower() < s2.lower(),
        'string>?': lambda s1, s2: s1 > s2,
        'string-ci>?': lambda s1, s2: s1.lower() > s2.lower(),
        'string<=?': lambda s1, s2: s1 <= s2,
        'string-ci<=?': lambda s1, s2: s1.lower() <= s2.lower(),
        'string>=?': lambda s1, s2: s1 >= s2,
        'string-ci>=?': lambda s1, s2: s1.lower() >= s2.lower(),
        'substring': lambda s, start, end: s[start:end],
        'string-fill!': lambda s, c: [c] * len(s),
        'string': lambda *args: "".join(map(str, args)),
        'concat': lambda *args: "".join(map(str, args)),
        'string-to-number': lambda s: float(s) if '.' in str(s) or 'e' in str(s).lower() else int(s),
        'first': lambda l: l[0] if l else None,
        'rest': lambda l: l[1:] if l else [],
        'make-vector': lambda k, fill: [fill] * k,
        'vector': lambda *args: list(args),
        'vector-length': len,
        'vector-ref': lambda v, i: v[i],
        'vector-set!': lambda v, i, x: v.__setitem__(i, x),
        'vector-fill!': lambda v, fill: [fill] * len(v),
        'list->vector': lambda l: l,
        'vector->list': lambda v: v,
        'reduce': lambda f, l, i: __import__('functools').reduce(lambda acc, x: _angeh_call(f, [acc, x], Env(outer=create_global_env())), l, i),
        'apply': lambda f, args: _angeh_call(f, args, create_global_env()),
        'eval': lambda x, env=None: evaluate(x, env if env is not None else create_global_env()),
        'load': lambda f: exec(open(f).read()),
        'is-boolean?': lambda x: isinstance(x, bool),
        'is-procedure?': lambda x: callable(x) or (isinstance(x, list) and len(x) > 0 and x[0] == 'lambda'),
        'is-null?': lambda x: x is None or x == [],
        'is-pair?': lambda x: isinstance(x, list) and len(x) > 0,
        'is-eof-object?': lambda x: x is None,
        'is-port?': lambda x: hasattr(x, 'read'),
        'is-input-port?': lambda x: hasattr(x, 'read'),
        'is-output-port?': lambda x: hasattr(x, 'write'),
        'current-input-port': lambda: sys.stdin,
        'current-output-port': lambda: sys.stdout,
        'open-input-file': lambda f: open(f, 'r'),
        'open-output-file': lambda f: open(f, 'w'),
        'close-input-port': lambda p: p.close(),
        'close-output-port': lambda p: p.close(),
        'read': lambda p=None: (p or sys.stdin).read(),
        'write': lambda x, p=None: (p or sys.stdout).write(str(x)),
        'display': lambda x, p=None: (p or sys.stdout).write(str(x)),
        'newline': lambda p=None: (p or sys.stdout).write('\n'),
        'eof-object': lambda: None,
        'call/cc': lambda f: f(lambda x: x),
        'call-with-current-continuation': lambda f: f(lambda x: x),
        'set-car!': lambda p, x: p.__setitem__(0, x),
        'set-cdr!': lambda p, x: p.__setitem__(1, x),
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda a, b: [a] + b,

        'error': lambda *args: print("ERROR:", *args),
        'number->string': str,
        'list': lambda *args: [*args],
        'first': lambda x: x[0],
        'rest': lambda x: x[1:],
        'len': len,
        'length': len,
        'not': lambda x: not x,
        'new-array': lambda: [],
        'new-map': lambda: {},
        'put!': lambda d, k, v: d.__setitem__(k, v),
        'add-all!': lambda l, items: l.extend(items),
        'is-list?': lambda x: isinstance(x, list),
        'is-number?': lambda x: isinstance(x, (int, float)),
        'string?': lambda x: isinstance(x, str),
        # ── Python interop builtins ──────────────────────────────────────────
        'abs':     abs,
        'max':     lambda *args: max(args) if len(args) > 1 else max(args[0]),
        'min':     lambda *args: min(args) if len(args) > 1 else min(args[0]),
        'round':   round,
        'sorted':  sorted,
        'reversed':lambda l: list(reversed(l)),
        'range':   lambda *args: list(range(*args)),
        'zip':     lambda *args: [list(t) for t in zip(*args)],
        'type-of': lambda x: type(x).__name__,
        'input':   input,
        'exit':    sys.exit,
        'None': None,
        'True': True,
        'False': False,
        '#t': True,
        '#f': False,
        'help': lambda: sorted([k for k in env.keys() if not k.startswith('__')]),
    })
    return env


# ─── AI Auto-Correction ─────────────────────────────────────────────────────
def ai_suggest_fix(bad_code, error_msg):
    """Ask the Oracle agent to suggest a corrected snippet."""
    if "__ERROR_HELPER__" not in AGENTS_REGISTRY:
        agent_spawn("__ERROR_HELPER__",
            "You are the Angehlang syntax advisor. "
            "When given broken code and an error, reply with ONLY the corrected "
            "single-expression snippet, no explanation.")
    suggestion = agent_ask("__ERROR_HELPER__",
        f"Broken code:\n{bad_code}\nError: {error_msg}\nFixed code:")
    if "[Mock AI]" not in suggestion and suggestion.strip():
        return suggestion.strip()
    return None


# ─── Pretty Error Printer ────────────────────────────────────────────────────
def report_error(kind, source, message, bad_code=None):
    print(f"{C.RED}{C.BOLD}✖  {kind}{C.RESET}  {C.DIM}in {source}{C.RESET}")
    print(f"   {C.YELLOW}{message}{C.RESET}")
    if bad_code:
        fix = ai_suggest_fix(bad_code, message)
        if fix:
            print(f"   {C.GREEN}💡 AI suggests:{C.RESET} {C.CYAN}{fix}{C.RESET}")


# ─── Environment Introspection (reflect) ─────────────────────────────────────
def reflect_env(env, query="globals"):
    q = str(query).lower()
    if q == "globals":
        data = {k: type(v).__name__ for k, v in env.items()}
        return json.dumps(data, indent=2)
    elif q == "agents":
        return json.dumps({k: {"memory_len": len(v["memory"])} for k, v in AGENTS_REGISTRY.items()}, indent=2)
    elif q == "a2a":
        return json.dumps(list(A2A_OMNIBUS)[-10:], indent=2)  # last 10 packets
    elif q == "version":
        return f"Angehlang v{ANGEH_VERSION} by {ANGEH_AUTHOR}"
    else:
        val = env.find(query) if hasattr(env, 'find') else None
        return json.dumps({query: type(val).__name__ if val else "undefined"}, indent=2)


# ─── Welcome Banner ──────────────────────────────────────────────────────────
def print_banner():
    print(f"""
{C.BLUE}{C.BOLD}╔══════════════════════════════════════════════════════════╗
║  🌌  A N G E H L A N G  v{ANGEH_VERSION:<6}  Universe OS         ║
║      Created by: {ANGEH_AUTHOR:<38}║
╚══════════════════════════════════════════════════════════╝{C.RESET}
{C.DIM}  Type Angehlang expressions to evaluate them interactively.
  Special commands:  .help  .agents  .a2a  .clear  .exit{C.RESET}
""")


# ─── Interactive REPL ────────────────────────────────────────────────────────
def run_repl(global_env):
    print_banner()
    buffer = ""
    while True:
        try:
            prompt = f"{C.MAGENTA}angeh>{C.RESET} " if not buffer.strip() else f"{C.DIM}  ...>{C.RESET} "
            try:
                line = input(prompt)
            except EOFError:
                print()
                break

            # REPL dot-commands
            stripped = line.strip()
            if stripped == ".exit" or stripped == ".quit":
                print(f"{C.DIM}Goodbye.{C.RESET}")
                break
            elif stripped == ".clear":
                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
                continue
            elif stripped == ".help":
                print(f"""{C.CYAN}
  .help    - Show this help
  .agents  - List active AI agents
  .a2a     - Show last A2A messages
  .clear   - Clear the screen
  .exit    - Quit the REPL

  Language Quick-Reference:
  (help)                     → list all built-in functions
  (def x 42)                 → define variable
  (print (+ x 10))           → arithmetic and print
  (agent-spawn "Bob" "hint") → spawn AI agent
  (agent-ask "Bob" "think") → query AI agent
  (reflect "globals")        → inspect environment
  (a2a-broadcast "msg")      → broadcast to all agents{C.RESET}
""")
                continue
            elif stripped == ".agents":
                print(f"{C.CYAN}{json.dumps({k: {'memory_len': len(v['memory'])} for k, v in AGENTS_REGISTRY.items()}, indent=2)}{C.RESET}")
                continue
            elif stripped == ".a2a":
                print(f"{C.CYAN}{json.dumps(A2A_OMNIBUS[-5:], indent=2)}{C.RESET}")
                continue

            buffer += line + " "
            # Only evaluate when parens are balanced
            open_p = buffer.count("(") - buffer.count(")")
            if open_p > 0:
                continue  # Wait for more input

            code = buffer.strip()
            buffer = ""
            if not code:
                continue

            try:
                tokens = tokenize(code)
                while tokens:
                    expr = parse_from_tokens(tokens)
                    if expr is not None:
                        result = evaluate(expr, global_env)
                        if result is not None:
                            print(f"  {C.GREEN}=> {result}{C.RESET}")
            except SyntaxError as e:
                report_error("Syntax Error", "REPL", str(e), code)
            except Exception as e:
                report_error("Runtime Error", "REPL", str(e), code)

        except KeyboardInterrupt:
            print(f"\n{C.DIM}(Use .exit to quit){C.RESET}")
            buffer = ""


# ─── File Runner ─────────────────────────────────────────────────────────────
def run_file(filename, global_env):
    """Load and evaluate an Angehlang source file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"{C.RED}✖  File not found: {filename}{C.RESET}")
        return False

    if not code.strip():
        return True

    tokens = tokenize(code)
    while tokens:
        try:
            expr = parse_from_tokens(tokens)
            if expr is not None:
                evaluate(expr, global_env)
        except SyntaxError as e:
            report_error("Syntax Error", filename, str(e))
            return False
        except Exception as e:
            report_error("Runtime Error", filename, str(e))
            return False
    return True


# ─── Main Entry Point ────────────────────────────────────────────────────────
def main():
    print(f"{C.CYAN}{C.BOLD}Standalone Engine Operational{C.RESET}")
    global_env = create_global_env()

    # Inject new capabilities into the global env
    global_env['reflect'] = lambda query="globals": reflect_env(global_env, query)
    global_env['version'] = lambda: f"Angehlang v{ANGEH_VERSION} by {ANGEH_AUTHOR}"
    global_env['help']    = lambda: global_env['reflect']('globals')

    if len(sys.argv) >= 2:
        # ── File mode ──────────────────────────────────────────────────────
        target = sys.argv[1]
        run_file(target, global_env)
    else:
        # ── REPL mode ──────────────────────────────────────────────────────
        run_repl(global_env)


if __name__ == '__main__':
    main()
