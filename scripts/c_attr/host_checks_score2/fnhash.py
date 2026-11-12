"""Function-level sha256 of two versions of a Python file (AST dump without line numbers); main() split per statement."""
import ast, hashlib, sys
def units(path):
    t = ast.parse(open(path, encoding="utf-8").read())
    out = {}
    for i, n in enumerate(t.body):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out[f"def {n.name}"] = ast.dump(n)
            if n.name == "main":
                for j, s in enumerate(n.body):
                    out[f"  main stmt {j:02d}"] = ast.dump(s)
        else:
            out[f"module stmt {i:03d} {type(n).__name__}"] = ast.dump(n)
    return out
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
old, new = units(sys.argv[1]), units(sys.argv[2])
fo = {k: v for k, v in old.items() if k.startswith(("def ", "  main"))}
fn = {k: v for k, v in new.items() if k.startswith(("def ", "  main"))}
same = [k for k in fo if k in fn and fo[k] == fn[k]]
print(f"functions+main statements: old {len(fo)}, new {len(fn)}, identical {len(same)}")
for k in sorted(set(fo) | set(fn)):
    if fo.get(k) != fn.get(k):
        print(f"  DIFF {k}: old {h(fo[k]) if k in fo else '-'} new {h(fn[k]) if k in fn else '-'}")
mo = [v for k, v in old.items() if k.startswith("module")]
mn = [v for k, v in new.items() if k.startswith("module")]
print(f"module-level statements: old {len(mo)}, new {len(mn)}, sequence identical {mo == mn}")
for name in sys.argv[3:]:
    print(f"  {name}: {h(fo['def ' + name])} == {h(fn['def ' + name])} {fo['def ' + name] == fn['def ' + name]}")
