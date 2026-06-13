import json
import re
import os

# 1. Stopwords for keyword extraction
STOPWORDS = {
    "and", "of", "the", "in", "a", "to", "for", "due", "under", "by", "with", 
    "an", "its", "at", "from", "on", "or", "as", "is", "are", "about", "their",
    "its", "these", "those", "that", "this", "which", "who", "whom", "whose",
    "using", "method", "concept", "basic", "introduction", "study", "to",
    "determine", "measurement", "effect", "theory", "law", "principle", 
    "concept", "general", "properties", "etc"
}

def extract_keywords(text):
    # Split by any non-word character and filter out stopwords
    words = re.findall(r'[a-zA-Z]+', text.lower())
    return set(w for w in words if w not in STOPWORDS and len(w) > 2)

# 2. Text clean up rules from cleanup_physics_questions.py
def clean_question_text(q_text):
    q_text = re.sub(r"--- Page \d+ ---", "", q_text)
    q_text = re.sub(r"Page \d+ of \d+", "", q_text)
    q_text = re.sub(r"(?i)Click here to visit our (website|contributor)", "", q_text)
    q_text = re.sub(r"(?i)Banaras Hindu University\s*[A-Z0-9-:]*(\s*Physics)?", "", q_text)
    q_text = re.sub(r"(?i)BANARAS HINDU UNIVERSITY", "", q_text)
    q_text = re.sub(r"(?i)B\.Sc\.\s*\(Hons\.\)\s*Semester\s*[IVX]+\s*Examination,?\s*\d{4}-\d{2}", "", q_text)
    q_text = re.sub(r"(?i)Paper No\.\s*[A-Z0-9-]*:?", "", q_text)
    q_text = re.sub(r"(?i)Instructions:\s*.*", "", q_text)
    
    q_text = re.sub(r"\s*\[\d+(\.\d+)?\]\s*$", "", q_text.strip())
    q_text = re.sub(r"\s*\[\d+(\.\d+)?\]\s*OR\s*$", "", q_text.strip())
    q_text = re.sub(r"\s*\bOR\b\s*$", "", q_text.strip())
    
    # Specific known typos
    replacements = {
        "the1sstate": "the 1s state",
        "1ststate": "1st state",
        "firststate": "first state",
        "whereais": "where $a$ is",
        "whereis": "where $r$ is",
        "whereis the": "where $r$ is the",
        "whereas": "where $a$ is",
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
    }
    
    if "ψ100(r) = 1√ πa3e-r/a" in q_text or "ψ100(r)" in q_text:
        q_text = q_text.replace("ψ100(r) = 1√ πa3e-r/a", "$\\psi_{100}(r) = \\frac{1}{\\sqrt{\\pi a^3}} e^{-r/a}$")
        q_text = q_text.replace("ψ100(r)", "$\\psi_{100}(r)$")
        
    for uni, lat in unicode_map.items():
        q_text = q_text.replace(uni, lat)

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
    
    q_text = re.sub(r"\b([0-9.]+)([a-zA-Z]{1,3})\b", r"\1 \2", q_text)
    
    q_text = re.sub(r"\s+", " ", q_text).strip()
    return q_text

# 3. Physically accurate answer key generation mapping
def get_custom_answer_key(key, question):
    q_lower = question.lower()
    
    if "coriolis" in q_lower:
        return (
            "1. **Coriolis Force Definition**:\n"
            "- A fictitious force acting on objects in motion within a rotating frame of reference, perpendicular to velocity:\n"
            "  $$\\vec{F}_{\\text{cor}} = -2m(\\vec{\\omega} \\times \\vec{v}')$$\n"
            "2. **Derivation**:\n"
            "- Differentiate the position vector twice: $\\vec{a}_i = \\vec{a}' + 2\\vec{\\omega} \\times \\vec{v}' + \\vec{\\omega} \\times (\\vec{\\omega} \\times \\vec{r}') + \\dot{\\vec{\\omega}} \\times \\vec{r}'$.\n"
            "- Identifying forces gives the Coriolis acceleration term $2\\vec{\\omega} \\times \\vec{v}'$.\n"
            "3. **Physical Significance**:\n"
            "- Explains the rotation of cyclones, currents, and lateral track wear on railroads."
        )
    elif "carnot" in q_lower:
        return (
            "1. **Carnot Cycle Processes**:\n"
            "- Reversible cycle with 4 stages: Isothermal expansion ($T_h$), Adiabatic expansion ($T_h \\to T_c$), Isothermal compression ($T_c$), and Adiabatic compression ($T_c \\to T_h$).\n"
            "2. **Efficiency**:\n"
            "- Derived from heat and temperature ratios: $\\eta = 1 - \\frac{Q_c}{Q_h} = 1 - \\frac{T_c}{T_h}$.\n"
            "3. **Carnot Theorem**:\n"
            "- No engine operating between two temperatures can be more efficient than a reversible Carnot engine."
        )
    elif "entropy" in q_lower:
        return (
            "1. **Entropy Definition**:\n"
            "- State variable defined by $dS = dQ_{\\text{rev}}/T$, representing microscopic thermal disorder.\n"
            "2. **Entropy Increase**:\n"
            "- In an isolated system undergoing any process, $dS_{\\text{universe}} \\ge 0$. It is constant for reversible and increases for irreversible processes.\n"
            "3. **Thermodynamic Limit**:\n"
            "- Connected to statistical mechanics via Boltzmann relation: $S = k_B \\ln \\Omega$."
        )
    elif "maxwell" in q_lower and ("relations" in q_lower or "thermodynamic" in q_lower):
        return (
            "1. **Thermodynamic Potentials**:\n"
            "- $dU = TdS - PdV$, $dH = TdS + VdP$, $dF = -SdT - PdV$, $dG = -SdT + VdP$.\n"
            "2. **Maxwell Relations**:\n"
            "- Derived by equating cross-derivatives of potentials: \n"
            "  - $(\\partial T/\\partial V)_S = -(\\partial P/\\partial S)_V$\n"
            "  - $(\\partial T/\\partial P)_S = (\\partial V/\\partial S)_P$\n"
            "  - $(\\partial S/\\partial V)_T = (\\partial P/\\partial T)_V$\n"
            "  - $(\\partial S/\\partial P)_T = -(\\partial V/\\partial T)_P$."
        )
    elif "interference" in q_lower or "fringe" in q_lower or "newton" in q_lower:
        return (
            "1. **Interference Conditions**:\n"
            "- Waves must be coherent, maintain constant phase relation, and have similar amplitude.\n"
            "2. **Path Difference**:\n"
            "- Bright fringes: $\\Delta x = n\\lambda$. Dark fringes: $\\Delta x = (2n+1)\\lambda/2$.\n"
            "3. **Fringe Width**:\n"
            "- $\\beta = \\frac{\\lambda D}{d}$ where $D$ is distance to screen and $d$ is slit spacing."
        )
    elif "diode" in q_lower or "junction" in q_lower or "zener" in q_lower:
        return (
            "1. **P-N Junction Barrier**:\n"
            "- Diffusion of carriers across the junction creates a depletion region with a potential barrier $V_0$.\n"
            "2. **Diode Equation**:\n"
            "- $I = I_0(e^{qV/k_BT} - 1)$, where $I_0$ is reverse saturation current.\n"
            "3. **Zener Voltage Regulation**:\n"
            "- Works in reverse breakdown region to keep voltage constant across load."
        )
    elif "waveguide" in q_lower:
        return (
            "1. **Rectangular Waveguide Boundary Conditions**:\n"
            "- Conducting walls force tangential electric field to zero ($E_{\\text{tan}} = 0$).\n"
            "2. **TEM Mode Exclusion**:\n"
            "- Requires $E_z = H_z = 0$. Using Laplace uniqueness theorem, this requires electric potential inside to be zero, hence no TEM mode exists.\n"
            "3. **Cutoff Frequency**:\n"
            "- $f_c = \\frac{c}{2}\\sqrt{(m/a)^2 + (n/b)^2}$ where $a, b$ are waveguide dimensions."
        )
    elif "analytic" in q_lower or "cauchy-riemann" in q_lower:
        return (
            "1. **Analyticity**:\n"
            "- A complex function $f(z) = u(x,y) + iv(x,y)$ is analytic if it is differentiable at every point in a region.\n"
            "2. **Cauchy-Riemann Conditions**:\n"
            "- Real and imaginary parts must satisfy partial differential equations:\n"
            "  $$\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}, \\quad \\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$$\n"
            "3. **Laplace Equation**:\n"
            "- Leads to $\\nabla^2 u = 0$ and $\\nabla^2 v = 0$ (harmonic functions)."
        )
    elif "uncertainty" in q_lower or "heisenberg" in q_lower:
        return (
            "1. **Uncertainty Principle**:\n"
            "- Formulated by Heisenberg: $\\Delta x \\cdot \\Delta p \\ge \\hbar/2$.\n"
            "2. **Physical Explanation**:\n"
            "- Measurement of position perturbs the momentum due to wave-particle characteristics of the probe.\n"
            "3. **Applications**:\n"
            "- Explains the zero-point energy and why electrons cannot reside inside the nucleus."
        )
    elif "schrodinger" in q_lower or "schrödinger" in q_lower:
        return (
            "1. **Time-Independent Schrödinger Equation**:\n"
            "- $-\\frac{\\hbar^2}{2m} \\nabla^2 \\psi + V\\psi = E\\psi$, an eigenvalue equation for Hamiltonian $\\hat{H}$.\n"
            "2. **Statistical Interpretation**:\n"
            "- Wave function $\\psi$ is normalized: $\\int |\\psi|^2 d^3r = 1$, and $|\\psi|^2$ is probability density.\n"
            "3. **Boundary Conditions**:\n"
            "- $\\psi$ must be continuous, single-valued, and normalizable."
        )
    elif "lagrangian" in q_lower or "euler-lagrange" in q_lower:
        return (
            "1. **Lagrangian Definition**:\n"
            "- $L = T - V$ where $T$ is kinetic energy and $V$ is potential energy.\n"
            "2. **Euler-Lagrange Equations**:\n"
            "- Derived from Hamilton's principle of least action:\n"
            "  $$\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{q}_i}\\right) - \\frac{\\partial L}{\\partial q_i} = 0$$\n"
            "3. **Symmetries**:\n"
            "- Cyclic coordinates lead directly to conserved generalized momentum (Noether's theorem)."
        )
    elif "statistics" in q_lower or "partition" in q_lower:
        return (
            "1. **Partition Function**:\n"
            "- Canonical partition function $Z = \\sum_i e^{-\\beta E_i}$ links microstates to thermodynamics.\n"
            "2. **Bose-Einstein vs Fermi-Dirac**:\n"
            "- Bosons (spin-integer, no restriction): $n_i = 1 / (e^{\\beta(E_i - \\mu)} - 1)$.\n"
            "- Fermions (spin-half, Pauli exclusion): $n_i = 1 / (e^{\\beta(E_i - \\mu)} + 1)$.\n"
            "3. **Free Energy**:\n"
            "- Helmholtz free energy: $F = -k_BT \\ln Z$."
        )
    elif "bragg" in q_lower:
        return (
            "1. **Bragg's Law**:\n"
            "- Condition for constructive interference of X-rays diffracted by crystal planes:\n"
            "  $$2d\\sin\\theta = n\\lambda$$\n"
            "2. **Miller Indices**:\n"
            "- $d = a / \\sqrt{h^2 + k^2 + l^2}$ for a cubic lattice of parameter $a$.\n"
            "3. **Reciprocal Space**:\n"
            "- Corresponds to Laue condition $\\Delta \\vec{k} = \\vec{G}$."
        )
    elif "deuteron" in q_lower:
        return (
            "1. **Deuteron Bound State**:\n"
            "- Bound system of proton and neutron with ground state $J^\\pi = 1^+$, binding energy $BE \\approx 2.22\\text{ MeV}$.\n"
            "2. **Tensor Force**:\n"
            "- Non-zero electric quadrupole moment indicates non-central tensor component in nuclear force.\n"
            "3. **Triplet State**:\n"
            "- Bound state occurs only in spin triplet state ($S=1$, $L=0$ mixed with $L=2$)."
        )
    elif "confinement" in q_lower or "nanoparticle" in q_lower:
        return (
            "1. **Quantum Confinement**:\n"
            "- Reduction of dimensions below exciton Bohr radius causes discretization of electronic band energy.\n"
            "2. **Density of States (DOS)**:\n"
            "- 3D (bulk) $\\propto E^{1/2}$, 2D (well) step function, 1D (wire) $\\propto E^{-1/2}$, 0D (dots) delta peaks.\n"
            "3. **Optical Shift**:\n"
            "- Causes blue shift in optical absorption/emission spectra as particle size shrinks."
        )

    # General Physics Fallback Template
    return (
        "1. **Core Physical Setup**:\n"
        "- Define the coordinates, variables, and physical constraints of the system.\n"
        "- Establish the governing equations (Euler-Lagrange, Schrödinger, or Maxwell equations).\n\n"
        "2. **Mathematical Derivation**:\n"
        "- Integrate the equations of motion or solve the eigenvalue problem.\n"
        "- Apply appropriate boundary conditions and evaluate constant coefficients.\n\n"
        "3. **Physical Interpretation & Limits**:\n"
        "- Analyze the final state, check dimension/unit consistency, and evaluate limiting approximations."
    )

# 4. Standard physics question banks from generate_physics_questions.py
STANDARD_QUESTION_BANKS = {
    "phymj11": [
        ("Explain the concept of Coriolis force and derive an expression for the acceleration of a particle in a rotating frame of reference.", "I"),
        ("Define inertial and non-inertial frames. Show that in a rotating frame, the effective acceleration has centrifugal and Coriolis terms.", "I"),
        ("Define central forces. Show that the motion under a central force is always confined to a plane.", "II"),
        ("State Kepler's laws of planetary motion and derive Kepler's third law from Newton's law of universal gravitation.", "II"),
        ("Define the moment of inertia tensor. Explain principal axes and principal moments of inertia.", "III"),
        ("Derive Euler's equations of motion for a rotating rigid body with one point fixed.", "III"),
        ("Define Young's modulus, bulk modulus, and Poisson's ratio, and derive the relation between them.", "IV"),
        ("Derive Poiseuille's formula for the rate of flow of a viscous liquid through a capillary tube.", "V"),
        ("State and prove Bernoulli's theorem for the steady flow of an ideal fluid.", "V"),
        ("Describe the Michelson-Morley experiment and discuss its negative result and physical significance.", "V")
    ],
    "phymj21": [
        ("Describe the Carnot cycle and derive the expression for the efficiency of a Carnot engine.", "II"),
        ("State Carnot's theorem and show that no engine working between two given temperatures can be more efficient than a Carnot engine.", "II"),
        ("Define entropy. Show that the entropy of the universe increases in all irreversible processes.", "III"),
        ("Derive Maxwell's thermodynamic relations using thermodynamic potentials.", "IV"),
        ("Derive the Clausius-Clapeyron latent heat equation and discuss its applications.", "IV"),
        ("Explain the Joule-Thomson effect and derive an expression for the Joule-Thomson coefficient.", "IV"),
        ("State Planck's radiation law and show how Wien's law and Rayleigh-Jeans law can be derived from it.", "V"),
        ("State and prove the Stefan-Boltzmann law of blackbody radiation.", "V"),
        ("Derive Wien's displacement law using thermodynamic principles.", "V"),
        ("Explain transport phenomena in gases and derive the expression for the coefficient of viscosity of a gas.", "I")
    ],
    "phymj31": [
        ("Derive the general wave equation for a one-dimensional wave propagating in a medium.", "I"),
        ("Explain the formation of Newton's rings in reflected light and derive expressions for the diameters of dark and bright rings.", "II"),
        ("Describe the construction and working of a Michelson interferometer and explain how it is used to measure wavelength.", "III"),
        ("Explain Fraunhofer diffraction at a single slit and derive the expression for the intensity distribution.", "IV"),
        ("Define resolving power. Derive the expression for the resolving power of a diffraction grating.", "IV"),
        ("Describe the phenomenon of double refraction in uniaxial crystals and explain the Huygens' theory.", "V"),
        ("Explain the construction and working of a Nicol prism as a polarizer and analyzer.", "V"),
        ("Define quarter-wave and half-wave plates and write expressions for their thicknesses.", "V"),
        ("Explain the phenomenon of optical rotation and describe the construction of Laurent's half-shade polarimeter.", "V"),
        ("Explain the Raman effect and discuss its classical and quantum theories.", "V")
    ],
    "phymj32": [
        ("Explain the working of a P-N junction diode under forward and reverse bias conditions.", "II"),
        ("Derive the diode equation and explain the temperature dependence of diode characteristics.", "II"),
        ("What is a Zener diode? Explain its working as a shunt voltage regulator.", "II"),
        ("Describe the construction and working of a Bipolar Junction Transistor (BJT) in Common Emitter configuration.", "III"),
        ("Define the input and output characteristics of a BJT in CE configuration and explain different operating regions.", "III"),
        ("Describe the construction, working, and characteristics of a Junction Field Effect Transistor (JFET).", "IV"),
        ("Explain the difference between depletion-type and enhancement-type MOSFETs.", "IV"),
        ("Explain the working principle of a Light Emitting Diode (LED) and write its applications.", "V"),
        ("Describe the working and characteristics of a solar cell, explaining fill factor.", "V"),
        ("What is the Hall effect? Derive expressions for the Hall coefficient and Hall voltage.", "I")
    ],
    "phymj41": [
        ("State Maxwell's equations in differential and integral forms, explaining the physical significance of each.", "III"),
        ("Define displacement current. Show how Maxwell modified Ampere's law to make it consistent for time-varying fields.", "III"),
        ("State and prove Poynting's theorem for the conservation of electromagnetic energy.", "III"),
        ("Derive the electromagnetic wave equations in a conducting medium and define skin depth.", "IV"),
        ("Derive Fresnel's equations for reflection and refraction of electromagnetic waves at a dielectric boundary.", "IV"),
        ("Define Brewster's angle and show that the reflected wave is completely polarized when the angle of incidence is Brewster's angle.", "IV"),
        ("Show that TEM waves cannot propagate inside a hollow rectangular waveguide.", "IV"),
        ("Derive the cutoff frequency for TE and TM modes in a rectangular waveguide.", "IV"),
        ("State the postulates of the Special Theory of Relativity and derive the Lorentz transformation equations.", "V"),
        ("Derive the formulas for relativistic length contraction and time dilation.", "V")
    ],
    "phymj42": [
        ("State and prove Gauss's divergence theorem and write its physical interpretation.", "I"),
        ("State and prove Stokes' theorem and discuss its physical interpretation.", "I"),
        ("Derive expressions for gradient, divergence, curl, and Laplacian in spherical polar coordinates.", "II"),
        ("Derive the power series solution of Legendre's differential equation and define Legendre polynomials.", "III"),
        ("State and prove the generating function for Legendre polynomials $P_n(x)$.", "IV"),
        ("State and prove the orthogonality property of Legendre polynomials.", "IV"),
        ("Derive the recurrence relations for Bessel functions $J_n(x)$.", "IV"),
        ("Define analytic functions and derive the Cauchy-Riemann conditions in Cartesian coordinates.", "V"),
        ("State and prove Cauchy's integral theorem and Cauchy's integral formula.", "V"),
        ("State and prove the residue theorem and explain its application in evaluating real definite integrals.", "V")
    ],
    "phymj51": [
        ("Explain the photoelectric effect and derive Einstein's photoelectric equation.", "I"),
        ("Explain the Compton effect and derive an expression for the Compton shift.", "I"),
        ("State and explain the Heisenberg uncertainty principle and discuss its applications.", "II"),
        ("What is a wave function? Explain its physical interpretation and state the conditions for a well-behaved wave function.", "II"),
        ("Derive the time-dependent and time-independent Schrödinger wave equations.", "III"),
        ("Solve the Schrödinger equation for a particle in a one-dimensional infinite square well potential.", "IV"),
        ("Solve the Schrödinger equation for a rectangular potential barrier and derive the transmission coefficient (tunneling).", "IV"),
        ("Solve the Schrödinger equation for a quantum harmonic oscillator and find the energy eigenvalues.", "V"),
        ("Define operators in quantum mechanics and show that eigenvalues of a Hermitian operator are always real.", "III"),
        ("State and prove Ehrenfest's theorems relating quantum mechanics to classical mechanics.", "III")
    ],
    "phymj52": [
        ("Define constraints. Distinguish between holonomic, non-holonomic, scleronomic, and rheonomic constraints with examples.", "I"),
        ("State D'Alembert's principle and derive Lagrange's equations of motion for a conservative holonomic system.", "I"),
        ("Apply the Lagrangian formulation to find the equations of motion for a simple pendulum.", "II"),
        ("Apply the Lagrangian formulation to find the equations of motion for a Atwood's machine.", "II"),
        ("Reduce the two-body central force problem to an equivalent one-body problem.", "III"),
        ("Derive the differential equation for the orbit of a particle moving under a central force.", "III"),
        ("Derive Kepler's first and second laws using the Lagrangian formulation for a central force.", "III"),
        ("State Hamilton's principle of least action and derive Lagrange's equations from it.", "IV"),
        ("Define generalized momentum and cyclic coordinates. Show that if a coordinate is cyclic, its conjugate momentum is conserved.", "IV"),
        ("Derive Hamilton's equations of motion from Hamilton's principle.", "V")
    ],
    "phymj53": [
        ("Explain macrostates, microstates, phase space, and ensembles. Define Liouville's theorem.", "I"),
        ("Describe the microcanonical ensemble and derive the entropy of a classical ideal gas using it.", "II"),
        ("Describe the canonical ensemble. Derive the partition function and show its relation to Helmholtz free energy.", "III"),
        ("Describe the grand canonical ensemble. Derive the grand partition function and chemical potential.", "IV"),
        ("State the postulate of equal a priori probability and explain the statistical definition of entropy.", "I"),
        ("Derive the Maxwell-Boltzmann distribution law and state its limitations.", "V"),
        ("Derive the Bose-Einstein distribution law and explain Bose-Einstein condensation.", "V"),
        ("Derive the Fermi-Dirac distribution law and define Fermi energy.", "V"),
        ("Compare Maxwell-Boltzmann, Bose-Einstein, and Fermi-Dirac statistics.", "V"),
        ("Derive the partition function of a system of independent harmonic oscillators.", "III")
    ],
    "phymj61": [
        ("State and prove Thevenin's and Norton's network theorems.", "I"),
        ("State and prove the Maximum Power Transfer theorem for AC circuits.", "I"),
        ("Explain the concept of feedback in amplifiers. Distinguish between positive and negative feedback.", "II"),
        ("Draw the circuit diagram of a CE BJT amplifier and explain its frequency response.", "II"),
        ("State the Barkhausen criterion for self-sustained oscillations.", "III"),
        ("Describe the construction and working of an RC Phase Shift oscillator.", "III"),
        ("Explain the working of a Wien Bridge oscillator and derive the frequency of oscillation.", "III"),
        ("Explain the characteristics of an ideal Operational Amplifier (Op-Amp).", "IV"),
        ("Describe the working of an Op-Amp as an inverting amplifier, non-inverting amplifier, and adder.", "IV"),
        ("Explain De Morgan's laws and show how NAND and NOR gates act as universal gates.", "V")
    ],
    "phymj62": [
        ("Define lattice, basis, unit cell, and Bravais lattices in three dimensions.", "I"),
        ("Define Miller indices. Derive an expression for interplanar spacing in a cubic lattice.", "I"),
        ("State Bragg's law of X-ray diffraction and explain the powder diffraction method.", "II"),
        ("Explain reciprocal lattice and derive reciprocal lattice vectors for a direct BCC lattice.", "II"),
        ("Derive the dispersion relation for a monoatomic linear lattice and define acoustic branch.", "III"),
        ("Explain the Debye theory of specific heat of solids and discuss how it resolves the limitations of the Einstein model.", "III"),
        ("Explain the free electron gas model of metals and derive an expression for Fermi energy.", "IV"),
        ("State and prove the Wiedemann-Franz law relating electrical and thermal conductivities.", "IV"),
        ("Discuss the Kronig-Penney model and explain the origin of energy bands in solids.", "V"),
        ("Explain the concept of effective mass of an electron and classify solids into conductors, semiconductors, and insulators.", "V")
    ],
    "phymj63": [
        ("Explain the vector atom model and describe the significance of L-S and J-J coupling schemes.", "I"),
        ("Explain the normal and anomalous Zeeman effects and derive expressions for the Zeeman shift.", "I"),
        ("Describe the fine structure of hydrogen-like atoms using relativistic corrections and spin-orbit coupling.", "I"),
        ("Explain the Pauli exclusion principle and write down ground-state configurations of multi-electron atoms.", "II"),
        ("Explain the rotational spectra of a rigid diatomic molecule and write the selection rules.", "III"),
        ("Describe the vibrational-rotational spectra of a diatomic molecule, explaining the Born-Oppenheimer approximation.", "III"),
        ("Explain the Raman effect, Stokes and anti-Stokes lines, and state its applications.", "III"),
        ("Derive the relation between Einstein's A and B coefficients for radiative transitions.", "IV"),
        ("Explain the threshold condition for laser action and the concept of population inversion.", "IV"),
        ("Describe the construction and working of a He-Ne laser and a Ruby laser.", "V")
    ],
    "phymj64": [
        ("State the general properties of nuclei: radius, mass, charge, spin, and binding energy.", "I"),
        ("Derive the semi-empirical mass formula based on the liquid drop model.", "I"),
        ("Describe the ground state properties of a deuteron and discuss the nature of nuclear forces.", "II"),
        ("Explain the nuclear shell model, magic numbers, and spin-orbit coupling.", "III"),
        ("State Gamow's theory of alpha decay and discuss the Geiger-Nuttall law.", "IV"),
        ("Describe Fermi's theory of beta decay and explain the neutrino hypothesis.", "IV"),
        ("Explain the classification of elementary particles into leptons, mesons, and baryons.", "V"),
        ("Discuss the conservation laws in particle physics (baryon number, lepton number, strangeness, isospin).", "V"),
        ("Explain the Gell-Mann-Nishijima formula and the Quark model of hadrons.", "V"),
        ("Describe the liquid drop model of nuclear fission.", "III")
    ],
    "phymj75": [
        ("Explain the concept of quantum confinement in nanostructures (quantum wells, quantum wires, quantum dots).", "I"),
        ("Derive the density of states for 0D, 1D, 2D, and 3D systems.", "I"),
        ("How do the optical and magnetic properties of nanoparticles differ from bulk materials?", "II"),
        ("Explain top-down and bottom-up approaches in the synthesis of nanomaterials.", "III"),
        ("Describe the synthesis of nanoparticles using the sol-gel method.", "III"),
        ("Describe the working principle of Scanning Electron Microscopy (SEM).", "IV"),
        ("Describe the working principle of Transmission Electron Microscopy (TEM).", "IV"),
        ("Explain how X-ray diffraction (XRD) is used to estimate nanoparticle crystal size using the Scherrer formula.", "IV"),
        ("Explain the working principle of Atomic Force Microscopy (AFM).", "IV"),
        ("Describe applications of nanotechnology in nanoelectronics and drug delivery.", "V")
    ]
}

# 5. Mirror/Alias codes mapping
active_keys = [
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

unique_to_active = {
    "phymj11": ["phymj11", "phymn11"],
    "phymj21": ["phymj21", "phymn21"],
    "phymj31": ["phymj31"],
    "phymj32": ["phymj32"],
    "phymj41": ["phymj41", "phymn41"],
    "phymj42": ["phymj42"],
    "phymj51": ["phymj51"],
    "phymj52": ["phymj52"],
    "phymj53": ["phymj53"],
    "phymj61": ["phymj61"],
    "phymj62": ["phymj62"],
    "phymj63": ["phymj63"],
    "phymj64": ["phymj64"],
    "phymj75": ["phymj75"]
}

def get_syllabus_code(exam_key):
    # Map active keys to JSON codes
    mappings = {
        "phymj11": "phymj11", "phymn11": "phymn11",
        "phymj21": "phymj21", "phymn21": "phymn21",
        "phymj31": "phymj31", "phymj32": "phymj32",
        "phymj41": "phymj41", "phymn41": "phymj41", # phymn41 is a minor that inherits phymj41 topics
        "phymj42": "phymj42", "phymj51": "phymj51",
        "phymj52": "phymj52", "phymj53": "phymj53",
        "phymj61": "phymj61", "phymj62": "phymj62",
        "phymj63": "phymj63", "phymj64": "phymj64",
        "phymj75": "phymj75"
    }
    return mappings.get(exam_key, exam_key)

# 6. Main Execution Logic
def main():
    # Load the syllabus file
    syllabus_path = "aaa/PHYSICS OUT/physics_syllabus.json"
    if not os.path.exists(syllabus_path):
        print(f"Error: Physics syllabus not found at {syllabus_path}")
        return
        
    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus_data = json.load(f)
        
    syllabus_map = {}
    for sem in syllabus_data["semesters"]:
        for paper in sem["papers"]:
            code = paper["code"].lower()
            syllabus_map[code] = paper
            
    # Load exams-data.js
    exams_js_path = "js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
        
    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])
    
    print("=== Auditing and Fixing Physics Questions ===")
    
    for unique_key, active_list in unique_to_active.items():
        syllabus_code = get_syllabus_code(unique_key)
        paper_data = syllabus_map.get(syllabus_code)
        
        if not paper_data:
            print(f"Warning: No syllabus data found for {unique_key} (code: {syllabus_code})")
            continue
            
        print(f"\nAuditing subject: {unique_key} - {paper_data['name']}")
        
        # Build keywords for the paper
        keywords = set()
        units_topics = [] # List of tuples: (unit_label, topics_text, keywords_set)
        
        roman_nums = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        
        for idx, unit_data in enumerate(paper_data.get("syllabus", [])):
            unit_label = unit_data.get("unit")
            if not unit_label:
                unit_label = roman_nums[idx] if idx < len(roman_nums) else str(idx+1)
            elif isinstance(unit_label, int):
                unit_label = roman_nums[unit_label - 1] if unit_label - 1 < len(roman_nums) else str(unit_label)
                
            topics_text = unit_data.get("topics", "")
            unit_keywords = extract_keywords(topics_text)
            keywords.update(unit_keywords)
            units_topics.append((unit_label, topics_text, unit_keywords))
            
        # Get existing questions for first active key in list
        good_qs = []
        seen_norms = set()
        
        # We check all active keys in the list to collect any valid existing questions
        existing_questions = []
        for act_key in active_list:
            if act_key in EXAMS and "questions" in EXAMS[act_key]:
                existing_questions.extend(EXAMS[act_key]["questions"])
                
        # Check existing questions
        for q_obj in existing_questions:
            q_text = q_obj.get("question", "")
            cleaned = clean_question_text(q_text)
            if not cleaned or len(cleaned) < 20:
                continue
                
            # Filter out placeholders
            if "discuss advanced theoretical foundations" in cleaned.lower() or "discuss the theoretical foundations" in cleaned.lower():
                continue
                
            # Filter out-of-syllabus questions
            # Check keyword overlap
            q_words = set(re.findall(r'[a-zA-Z]+', cleaned.lower()))
            overlap = q_words.intersection(keywords)
            
            # Special check: is it a valid physics question? (contains typical physics terms)
            physics_stop = {"derive", "explain", "discuss", "calculate", "prove", "show", "find", "determine", "state", "define"}
            clean_q_words = q_words - physics_stop
            
            # If overlap is non-empty, keep it
            if len(overlap) > 0:
                norm = cleaned.lower().strip()
                if norm not in seen_norms:
                    seen_norms.add(norm)
                    
                    # Determine unit dynamically based on best keyword overlap
                    best_unit = units_topics[0][0] if units_topics else "I"
                    max_overlap = 0
                    for u_lbl, _, u_kws in units_topics:
                        u_overlap = len(q_words.intersection(u_kws))
                        if u_overlap > max_overlap:
                            max_overlap = u_overlap
                            best_unit = u_lbl
                            
                    good_qs.append((cleaned, best_unit))
                    
        print(f" - Kept {len(good_qs)} valid on-syllabus questions from existing database.")
        
        # Pad with standard question bank if we have fewer than 50
        std_bank = STANDARD_QUESTION_BANKS.get(unique_key, [])
        for q_text, unit in std_bank:
            if len(good_qs) >= 50:
                break
            cleaned = clean_question_text(q_text)
            norm = cleaned.lower().strip()
            if norm not in seen_norms:
                seen_norms.add(norm)
                good_qs.append((cleaned, unit))
                
        print(f" - After standard questions bank padding: {len(good_qs)} questions.")
        
        # If still fewer than 50, generate brand new smart questions from syllabus topics
        if len(good_qs) < 50:
            print(" - Generating new questions from syllabus topics...")
            # We split each unit's topics by commas, semicolons or periods to extract distinct sub-topics
            fallback_idx = 1
            
            # Let's loop through units and generate questions
            unit_cycle = 0
            while len(good_qs) < 50:
                unit_label, topics_text, unit_keywords = units_topics[unit_cycle % len(units_topics)]
                
                # Split topics to find specific phrases
                phrases = [p.strip() for p in re.split(r'[,;.]', topics_text) if len(p.strip()) > 10]
                if not phrases:
                    # Fallback to key terms
                    phrases = list(unit_keywords)[:3]
                    
                if phrases:
                    phrase = phrases[fallback_idx % len(phrases)]
                    # Clean up prefixing text (e.g. "To study", "To determine", "Experiments", "1.", etc.)
                    phrase = re.sub(r'^(To study|To determine|Study of|To measure|To find|Experiments|1\.|2\.|3\.|4\.|5\.|6\.|7\.|8\.|9\.|10\.)\s*', '', phrase, flags=re.IGNORECASE)
                    phrase = phrase.strip()
                    
                    templates = [
                        f"Explain the physical principles and governing equations of {phrase}.",
                        f"Derive the mathematical expressions and discuss the applications of {phrase}.",
                        f"Describe the experimental setup, procedure, and analysis for studying {phrase}.",
                        f"Discuss the theoretical background, significance, and limitations of {phrase} in physics."
                    ]
                    
                    q_text = templates[fallback_idx % len(templates)]
                    cleaned = clean_question_text(q_text)
                    norm = cleaned.lower().strip()
                    if norm not in seen_norms:
                        seen_norms.add(norm)
                        good_qs.append((cleaned, unit_label))
                else:
                    # Generic fallback
                    q_text = f"Explain the core concept and derivations of {paper_data['name']} for Unit {unit_label} (Topic Part {fallback_idx})."
                    cleaned = clean_question_text(q_text)
                    norm = cleaned.lower().strip()
                    if norm not in seen_norms:
                        seen_norms.add(norm)
                        good_qs.append((cleaned, unit_label))
                        
                fallback_idx += 1
                unit_cycle += 1
                
        # Slice to exactly 50
        good_qs = good_qs[:50]
        
        # Structure final questions array
        formatted_questions = []
        for idx, (q_text, unit) in enumerate(good_qs):
            q_id = idx + 1
            ans_key = get_custom_answer_key(unique_key, q_text)
            
            formatted_questions.append({
                "id": q_id,
                "unit": unit,
                "question": q_text,
                "answerKey": ans_key
            })
            
        # Write to all active keys (major/minor copies) and set comingSoon to False
        for active_key in active_list:
            orig = EXAMS.get(active_key, {})
            EXAMS[active_key] = {
                "id": active_key,
                "title": orig.get("title", paper_data["name"]),
                "module": orig.get("module", active_key.upper()),
                "duration": 60,
                "type": "theory",
                "comingSoon": False,
                "questions": formatted_questions
            }
            print(f"   * Exam key '{active_key}' updated (Live: True, count: {len(formatted_questions)})")
            
    # Save back to js/exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2, ensure_ascii=False)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)
        
    print("\n=== Success! js/exams-data.js updated with audited physics questions ===")

if __name__ == "__main__":
    main()
