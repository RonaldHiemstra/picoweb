def unquote_plus(s):
    # TODO: optimize
    s = s.replace("+", " ")
    arr = s.split("%")
    arr2 = [chr(int(x[:2], 16)) + x[2:] for x in arr[1:]]
    return arr[0] + "".join(arr2)

def parse_qs(s):
    res = {}
    if s:
        pairs = s.split("&")
        for p in pairs:
            vals = [unquote_plus(x) for x in p.split("=", 1)]
            if len(vals) == 1:
                vals.append(True)
            old = res.get(vals[0])
            if old is not None:
                if not isinstance(old, list):
                    old = [old]
                    res[vals[0]] = old
                old.append(vals[1])
            else:
                res[vals[0]] = vals[1]
    return res

#print(parse_qs("foo"))
#print(parse_qs("fo%41o+bar=+++1"))
#print(parse_qs("foo=1&foo=2"))


# copied from https://github.com/micropython/micropython-lib/blob/master/pkg_resources/pkg_resources.py
import uio

c = {}

def resource_stream(package, resource):
    if package not in c:
        try:
            if package:
                p = __import__(package + ".R", None, None, True)
            else:
                p = __import__("R")
            c[package] = p.R
        except ImportError:
            if package:
                p = __import__(package)
                d = p.__path__
            else:
                d = "."
#            if d[0] != "/":
#                import uos
#                d = uos.getcwd() + "/" + d
            c[package] = d + "/"

    p = c[package]
    if isinstance(p, dict):
        return uio.BytesIO(p[resource])
    return open(p + resource, "rb")