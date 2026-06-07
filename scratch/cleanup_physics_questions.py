import json
import re

def clean_question_text(q_text):
    # 1. Strip out exam page numbers, contributors, headers, footers
    q_text = re.sub(r"--- Page \d+ ---", "", q_text)
    q_text = re.sub(r"Page \d+ of \d+", "", q_text)
    q_text = re.sub(r"(?i)Click here to visit our (website|contributor)", "", q_text)
    q_text = re.sub(r"(?i)Banaras Hindu University\s*[A-Z0-9-:]*(\s*Physics)?", "", q_text)
    q_text = re.sub(r"(?i)BANARAS HINDU UNIVERSITY", "", q_text)
    q_text = re.sub(r"(?i)B\.Sc\.\s*\(Hons\.\)\s*Semester\s*[IVX]+\s*Examination,?\s*\d{4}-\d{2}", "", q_text)
    q_text = re.sub(r"(?i)Paper No\.\s*[A-Z0-9-]*:?", "", q_text)
    q_text = re.sub(r"(?i)Instructions:\s*.*", "", q_text)
    
    # 2. Strip marks indications like [8], [3.5], [12.5], [6] at the end of lines
    q_text = re.sub(r"\s*\[\d+(\.\d+)?\]\s*$", "", q_text.strip())
    q_text = re.sub(r"\s*\[\d+(\.\d+)?\]\s*OR\s*$", "", q_text.strip())
    q_text = re.sub(r"\s*\bOR\b\s*$", "", q_text.strip())
    
    # 3. Fix specific known typos and run-together words
    replacements = {
        "the1sstate": "the 1s state",
        "1ststate": "1st state",
        "firststate": "first state",
        "whereais": "where $a$ is",
        "whereis": "where $r$ is",
        "whereis the": "where $r$ is the",
        "whereas": "where $a$ is",  # specific to "whereas is the Bohr radius"
        "restmass": "rest mass",
        "atomicmass": "atomic mass",
        "wavefunction": "wave function",
        "wavefunctions": "wave functions",
        "kineticenergy": "kinetic energy",
        "potentialenergy": "potential energy",
        "angularmomentum": "angular momentum",
        "centrifugalforce": "centrifugal force",
        "coriolisforce": "coriolis force",
        "Workouttheaction": "Work out the action",
        "aanda†": "$a$ and $a^\\dagger$",
        "aanda": "$a$ and $a$",
        "anda†": "and $a^\\dagger$",
        "covers1mile": "covers 1 mile",
        "in50 s": "in 50 s",
        "speedof0.95c": "speed of $0.95c$",
        "speedof": "speed of ",
        "energy1MeV": "energy 1 MeV",
        "energyof1MeV": "energy of 1 MeV",
        "gain change of20%": "gain change of 20%",
        "gain ofAv": "gain of $A_v$",
        "gain ofAv = − 1000has": "gain of $A_v = -1000$ has",
        "feedback fraction ofβ": "feedback fraction of $\\beta$",
        "fraction ofβ=−0.1": "fraction of $\\beta = -0.1$",
        "resistanceR B1": "resistance $R_{B1}$",
        "resistanceRBB": "resistance $R_{BB}$",
        "resistancesC1 andC 2": "resistances $C_1$ and $C_2$",
        "capacitancesC1 andC 2": "capacitances $C_1$ and $C_2$",
        "gainAv": "gain $A_v$",
        "operatorLz": "operator $L_z$",
        "eigenvaluemℏ": "eigenvalue $m\\hbar$",
        "operatorL2": "operator $L^2$",
        "energyE": "energy $E$",
        "widtha": "width $a$",
        "heightU": "height $U$",
        "massm": "mass $m$",
        "chargeq": "charge $q$",
        "difference ofVvolts": "difference of $V$ volts",
        "difference ofV": "difference of $V$",
        "mass excess of alpha is2.4249MeV": "mass excess of alpha is $2.4249\\text{ MeV}$",
        "excess masses of the daughter and parent are−21.759MeV and−10.381MeV": "excess masses of the daughter and parent are $-21.759\\text{ MeV}$ and $-10.381\\text{ MeV}$",
    }
    
    for old, new in replacements.items():
        q_text = q_text.replace(old, new)
        
    # 4. Clean up unicode symbols and convert to LaTeX
    unicode_map = {
        "\u03c8": "\\psi",      # ψ
        "\u03c0": "\\pi",       # π
        "\u221a": "\\sqrt",     # √
        "\u2212": "-",          # −
        "\u03b8": "\\theta",    # θ
        "\u03b5": "\\varepsilon",# ε
        "\u03c3": "\\sigma",    # σ
        "\u03b1": "\\alpha",    # α
        "\u03b2": "\\beta",     # β
        "\u03bb": "\\lambda",    # λ
        "\u03c9": "\\omega",    # ω
        "\u221e": "\\infty",    # ∞
        "\u2202": "\\partial",  # ∂
        "\u2207": "\\nabla",    # ∇
        "\u2127": "\\Omega",    # Ω
        "\u2032": "'",          # ′
        "\u2033": "''",         # ″
        "\u2245": "\\cong",     # ≅
        "\u221d": "\\propto",   # ∝
        "\u222b": "\\int",      # ∫
        "\u2265": "\\ge",       # ≥
        "\u2264": "\\le",       # ≤
        "\u2260": "\\neq",      # ≠
        "\u2248": "\\approx",   # ≈
        "\u2211": "\\sum",      # ∑
        "\u03b7": "\\eta",      # η
        "\u03d5": "\\phi",      # ϕ
        "\u03c6": "\\phi",      # φ
        "\u03bc": "\\mu",       # µ
        "\\hbar": "\\hbar",
        "\\dagger": "\\dagger",
    }
    
    # Replace math expressions and surround with $
    # For example, if we see things like "ψ100(r) = 1\sqrt \pi a3e-r/a"
    # let's write clean LaTeX replacement rules for known patterns
    if "ψ100(r) = 1√ πa3e-r/a" in q_text or "ψ100(r)" in q_text:
        # Given the normalized wave function for the 1s state of the Hydrogen atom: \psi_{100}(r) = \frac{1}{\sqrt{\pi a^3}} e^{-r/a} ...
        q_text = q_text.replace("ψ100(r) = 1√ πa3e-r/a", "$\\psi_{100}(r) = \\frac{1}{\\sqrt{\\pi a^3}} e^{-r/a}$")
        q_text = q_text.replace("ψ100(r)", "$\\psi_{100}(r)$")
        
    for uni, lat in unicode_map.items():
        # Only replace if not already part of a LaTeX word (avoiding double backslashes)
        q_text = q_text.replace(uni, lat)

    # 5. MathJax delimiter formatting for specific equations
    # If the text has equations like H=ℏω ( a†a+ 1 2 ) or similar:
    q_text = q_text.replace("H=ℏω ( a†a+ 1 2 )", "$H = \\hbar\\omega (a^\\dagger a + 1/2)$")
    q_text = q_text.replace("a= √mω 2ℏ ( x+ ip mω )", "$a = \\sqrt{\\frac{m\\omega}{2\\hbar}} \\left(x + \\frac{ip}{m\\omega}\\right)$")
    q_text = q_text.replace("a †= √mω 2ℏ ( x−ip mω )", "$a^\\dagger = \\sqrt{\\frac{m\\omega}{2\\hbar}} \\left(x - \\frac{ip}{m\\omega}\\right)$")
    
    q_text = q_text.replace("xL′′ n(x) + (1−x)L′ n(x) + nLn(x) = 0", "$x L_n''(x) + (1-x) L_n'(x) + n L_n(x) = 0$")
    q_text = q_text.replace("y(x) = e−x/2Ln(x)", "$y(x) = e^{-x/2} L_n(x)$")
    q_text = q_text.replace("Ln(x)", "$L_n(x)$")
    
    q_text = q_text.replace("g(x,t ) = e2xt−t2 = ∑∞ n=0 Hn(x) n! tn", "$g(x,t) = e^{2xt-t^2} = \\sum_{n=0}^{\\infty} \\frac{H_n(x)}{n!} t^n$")
    q_text = q_text.replace("∫ ∞ −∞ e−x2 [Hn(x)]2dx= 2 nn!√π", "$\\int_{-\\infty}^{\\infty} e^{-x^2} [H_n(x)]^2 dx = 2^n n! \\sqrt{\\pi}$")
    q_text = q_text.replace("Hn(x)", "$H_n(x)$")
    
    q_text = q_text.replace("Av = − 1000", "$A_v = -1000$")
    q_text = q_text.replace("β=−0.1", "$\\beta = -0.1$")
    
    q_text = q_text.replace("R21(r) =Cre −r/2a", "$R_{21}(r) = C r e^{-r/2a}$")
    q_text = q_text.replace("ψ(r,θ,ϕ) =Ne−r/a", "$\\psi(r,\\theta,\\phi) = N e^{-r/a}$")
    
    # Add space to single letter numbers or variables in math contexts
    q_text = re.sub(r"\b([0-9.]+)([a-zA-Z]{1,3})\b", r"\1 \2", q_text) # e.g. 1sstate to 1 s state or similar
    
    # 6. General LaTeX wrapping for remaining mathematical symbols
    # Wrap standard single character variables like x, y, z, r, a, T, t when they are part of equations
    # We will do some heuristic wrapping or keep it simple.
    
    # Remove double spaces, clean remaining formatting artifacts
    q_text = re.sub(r"\s+", " ", q_text).strip()
    return q_text

# Load exams-data.js
with open("js/exams-data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}")
EXAMS = json.loads(content[json_start:json_end+1])

physics_keys = [
    "phymj11", "phymn11",
    "phymj21", "phymn21",
    "phymj31",
    "phymj32",
    "phymj41", "phymn41",
    "phymj42",
    "phymj51",
    "phymj52",
    "phymj53",
    "phymj61",
    "phymj62",
    "phymj63",
    "phymj64",
    "phymj75"
]

print("Starting clean up of physics questions...")
updated_count = 0

for k in physics_keys:
    exam = EXAMS.get(k)
    if not exam or "questions" not in exam:
        continue
        
    for q in exam["questions"]:
        original = q["question"]
        cleaned = clean_question_text(original)
        if original != cleaned:
            q["question"] = cleaned
            updated_count += 1

print(f"Cleaned up {updated_count} questions!")

# Write back
output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
with open("js/exams-data.js", "w", encoding="utf-8") as f:
    f.write(output_str)

print("exams-data.js successfully cleaned and saved!")
