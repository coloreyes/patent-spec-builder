"""Convert LaTeX-like formulas to Word OMath XML."""
from lxml import etree

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
OM = f"{{{MATH_NS}}}"

GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ",
    r"\Delta": "Δ", r"\eta": "η", r"\theta": "θ", r"\lambda": "λ",
    r"\mu": "μ", r"\sigma": "σ", r"\tau": "τ", r"\omega": "ω",
}

SYMBOLS = {
    r"\cdot": "·", r"\times": "×", r"\div": "÷",
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠",
    r"\sum": "∑", r"\prod": "∏",
    r"\in": "∈", r"\notin": "∉", r"\subset": "⊂",
    r"\rightarrow": "→", r"\leftarrow": "←",
    r"\le": "≤", r"\ge": "≥",
}

def O(tag, attrib=None):
    el = etree.Element(f"{OM}{tag}")
    if attrib:
        for k, v in attrib.items():
            el.set(k, v)
    return el

def run_text(text):
    r = O("r"); t = O("t"); t.text = text; r.append(t); return r

def run_italic(text):
    r = O("r"); rPr = O("rPr"); i = O("i"); rPr.append(i); r.append(rPr)
    t = O("t"); t.text = text; r.append(t); return r

def run_upright(text):
    r = O("r"); rPr = O("rPr"); sty = O("sty", {"val": "r"}); rPr.append(sty); r.append(rPr)
    t = O("t"); t.text = text; r.append(t); return r

def _extract_brace(text, pos):
    if pos >= len(text) or text[pos] != '{':
        return "", pos
    depth = 0
    for i in range(pos, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0: return text[pos+1:i], i+1
    return text[pos+1:], len(text)

def _parse(text, parent):
    i = 0
    base_parts = []
    pending_sup = pending_sub = None

    while i < len(text):
        if text[i:].startswith(r"\frac"):
            i += 5; ns, i = _extract_brace(text, i); ds, i = _extract_brace(text, i)
            _flush(parent, base_parts, pending_sup, pending_sub)
            base_parts = []; pending_sup = pending_sub = None
            ne = O("num"); _parse(ns, ne); de = O("den"); _parse(ds, de)
            fr = O("f"); fr.append(ne); fr.append(de); parent.append(fr)
        elif text[i:].startswith(r"\bar{"):
            i += 4; cs, i = _extract_brace(text, i)
            _flush(parent, base_parts, pending_sup, pending_sub)
            base_parts = []; pending_sup = pending_sub = None
            ce = O("e"); _parse(cs, ce)
            bar = O("bar"); bar.append(O("chr", {"val": "0304"})); bar.append(ce); parent.append(bar)
        elif text[i:].startswith(r"\mathrm{"):
            i += 8; cs, i = _extract_brace(text, i)
            _flush(parent, base_parts, pending_sup, pending_sub)
            base_parts = []; pending_sup = pending_sub = None
            parent.append(run_upright(cs))
        elif text[i:].startswith(r"\text{"):
            i += 5; cs, i = _extract_brace(text, i)
            parent.append(run_text(cs))
        elif text[i:].startswith(r"\tag{"):
            i += 5; _, i = _extract_brace(text, i)
        elif any(text[i:].startswith(k) for k in GREEK):
            m = next(k for k in GREEK if text[i:].startswith(k))
            base_parts.append(GREEK[m]); i += len(m)
        elif any(text[i:].startswith(k) for k in SYMBOLS):
            m = next(k for k in SYMBOLS if text[i:].startswith(k))
            if SYMBOLS[m]: base_parts.append(SYMBOLS[m])
            i += len(m)
        elif text[i] == '^' and i+1 < len(text):
            i += 1
            if text[i] == '{': i += 1; pending_sup, i = _extract_brace(text, i)
            else: pending_sup = text[i]; i += 1
        elif text[i] == '_' and i+1 < len(text):
            i += 1
            if text[i] == '{': i += 1; pending_sub, i = _extract_brace(text, i)
            else: pending_sub = text[i]; i += 1
        elif text[i] == '{':
            cs, i = _extract_brace(text, i); _parse(cs, parent)
        elif text[i] == '}':
            i += 1
        else:
            base_parts.append(text[i]); i += 1

    _flush(parent, base_parts, pending_sup, pending_sub)

def _flush(parent, base_parts, pending_sup, pending_sub):
    if not base_parts and not pending_sup and not pending_sub:
        return
    bt = "".join(base_parts)
    if pending_sup and pending_sub:
        sSub = O("sSub"); e = O("e")
        sSup = O("sSup"); ie = O("e"); ie.append(run_italic(bt)); sSup.append(ie)
        su = O("sup"); su.append(O("ctrlPr")); _parse(pending_sup, su); sSup.append(su)
        e.append(sSup); sSub.append(e)
        sub = O("sub"); sub.append(O("ctrlPr")); _parse(pending_sub, sub); sSub.append(sub)
        parent.append(sSub)
    elif pending_sup:
        sSup = O("sSup"); e = O("e"); e.append(run_italic(bt)); sSup.append(e)
        su = O("sup"); su.append(O("ctrlPr")); _parse(pending_sup, su); sSup.append(su)
        parent.append(sSup)
    elif pending_sub:
        sSub = O("sSub"); e = O("e"); e.append(run_italic(bt)); sSub.append(e)
        sub = O("sub"); sub.append(O("ctrlPr")); _parse(pending_sub, sub); sSub.append(sub)
        parent.append(sSub)
    else:
        if bt: parent.append(run_italic(bt))

def formula_to_omath(latex):
    latex = latex.strip()
    if latex.startswith(r"\[") and latex.endswith(r"\]"): latex = latex[2:-2].strip()
    if latex.startswith(r"\(") and latex.endswith(r"\)"): latex = latex[2:-2].strip()
    oMath = O("oMath"); _parse(latex, oMath); return oMath
