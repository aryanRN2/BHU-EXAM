import json
import re
import os

# 1. Define physics syllabi and standard questions for augmentation
SUBJECT_SYLLABI = {
    "phymj11": {
        "title": "Mechanics & General Properties of Matter",
        "standard_questions": [
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
        ]
    },
    "phymj21": {
        "title": "Thermal Physics",
        "standard_questions": [
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
        ]
    },
    "phymj31": {
        "title": "Wave & Wave Optics",
        "standard_questions": [
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
        ]
    },
    "phymj32": {
        "title": "Physics of Semiconductors and Devices",
        "standard_questions": [
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
        ]
    },
    "phymj41": {
        "title": "Electromagnetic Theory & Special Theory of Relativity",
        "standard_questions": [
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
        ]
    },
    "phymj42": {
        "title": "Mathematical Physics-I",
        "standard_questions": [
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
        ]
    },
    "phymj51": {
        "title": "Quantum Mechanics-I",
        "standard_questions": [
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
        ]
    },
    "phymj52": {
        "title": "Classical Mechanics-I",
        "standard_questions": [
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
        ]
    },
    "phymj53": {
        "title": "Statistical Mechanics-I",
        "standard_questions": [
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
        ]
    },
    "phymj61": {
        "title": "Electronic Circuits and Analysis",
        "standard_questions": [
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
        ]
    },
    "phymj62": {
        "title": "Solid State Physics",
        "standard_questions": [
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
        ]
    },
    "phymj63": {
        "title": "Atomic, Molecular and Laser Physics",
        "standard_questions": [
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
        ]
    },
    "phymj64": {
        "title": "Nuclear & Particle Physics",
        "standard_questions": [
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
        ]
    },
    "phymj75": {
        "title": "Nano Science and Technology",
        "standard_questions": [
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
}

# Define get_custom_answer_key (copied from generate_physics_questions.py)
def get_custom_answer_key(key, question):
    q_lower = question.lower()
    
    # Mechanics phymj11
    if key == "phymj11":
        if "coriolis" in q_lower:
            return "1. **Coriolis Force Definition**:\nFictitious force in rotating frames perpendicular to velocity: $\\vec{F}_{\\text{cor}} = -2m(\\vec{\\omega} \\times \\vec{v}')$.\n2. **Derivation**:\nDifferentiate position in inertial vs rotating frame twice. Acceleration relation: $\\vec{a}_i = \\vec{a}' + 2\\vec{\\omega} \\times \\vec{v}' + \\vec{\\omega} \\times (\\vec{\\omega} \\times \\vec{r}') + \\dot{\\vec{\\omega}} \\times \\vec{r}'$.\n3. **Application**:\nCauses deflection of wind patterns (Coriolis effect) and lateral forces on train tracks."
        if "fictitious" in q_lower or "pseudo" in q_lower:
            return "1. **Pseudo Forces Concept**:\nForces apparent only in non-inertial (accelerated) frames, equal to $-m\\vec{a}_0$ where $\\vec{a}_0$ is frame acceleration.\n2. **Calculation**:\n(i) Moving upwards at $4\\text{ m/s}^2$: $F_{\\text{pseudo}} = -m(a_0) = -5(4) = -20\\text{ N}$ (downwards). Observed weight $F_{\\text{obs}} = m(g + a_0) = 5(9.8 + 4) = 69\\text{ N}$.\n(ii) Moving downwards: $F_{\\text{pseudo}} = -5(-4) = +20\\text{ N}$ (upwards). Observed weight $F_{\\text{obs}} = m(g - a_0) = 5(9.8 - 4) = 29\\text{ N}$."
        if "kepler" in q_lower:
            return "1. **Kepler's Laws Statement**:\nFirst Law: Elliptical orbits with Sun at one focus. Second Law: Areal velocity is constant ($dA/dt = L/2m = \\text{const}$). Third Law: $T^2 \\propto a^3$.\n2. **Derivation**:\nFrom central gravity force $\\vec{F} = -\\frac{GMm}{r^2}\\hat{r}$. Conservation of angular momentum $\\vec{L}$ ensures planar motion and constant areal velocity. Integration of orbit equation gives conic section $r = \\frac{p}{1 + e\\cos\\theta}$."
        if "moment of inertia" in q_lower or "principal" in q_lower:
            return "1. **Moment of Inertia Tensor**:\nA $3 \\times 3$ symmetric matrix $I_{ij} = \\iiint \\rho(r) (r^2 \\delta_{ij} - x_i x_j) dV$ representing rotational inertia about any direction.\n2. **Principal Axes**:\nThe axes along which the inertia tensor is diagonal: $I = \\text{diag}(I_xx, I_yy, I_zz)$. The off-diagonal products of inertia vanish. The eigenvalues are the principal moments of inertia."
        if "elastic" in q_lower or "poisson" in q_lower or "modulus" in q_lower:
            return "1. **Elastic Constants**:\nYoung's modulus ($Y$), Bulk modulus ($K$), Shear modulus ($\\eta$), Poisson's ratio ($\\sigma$).\n2. **Relations**:\n$Y = 3K(1 - 2\\sigma)$ and $Y = 2\\eta(1 + \\sigma)$. Eliminating $\\sigma$ yields $Y = \\frac{9\\eta K}{3K + \\eta}$."
        return "1. **Mechanics Core Principles**:\nDefine coordinates, analyze system using Newton's second law $\\vec{F} = m\\vec{a}$ or conservation laws.\n2. **Mathematical Formulation**:\nSet up boundary conditions. Integrate equations of motion to find position $\\vec{r}(t)$ and velocity $\\vec{v}(t)$.\n3. **Physical Analysis**:\nEvaluate limiting cases (e.g., small oscillations or relativistic limits where $\\gamma \\to 1$)."

    # Thermal phymj21
    elif key == "phymj21":
        if "carnot" in q_lower:
            return "1. **Carnot Cycle Processes**:\nFour reversible processes: (1) Isothermal expansion at $T_h$, (2) Adiabatic expansion from $T_h$ to $T_c$, (3) Isothermal compression at $T_c$, (4) Adiabatic compression back to $T_h$.\n2. **Efficiency**:\nWork done $W = Q_h - Q_c$. Efficiency $\\eta = \\frac{W}{Q_h} = 1 - \\frac{Q_c}{Q_h}$. From adiabatic relations, $Q_h/Q_c = T_h/T_c$, giving $\\eta = 1 - T_c/T_h$."
        if "entropy" in q_lower:
            return "1. **Entropy Definition**:\nThermodynamic state function $dS = \\frac{dQ_{\\text{rev}}}{T}$ representing microscopic disorder.\n2. **Entropy Increase Principle**:\nFor any isolated system in an irreversible process, $dS > 0$. For reversible processes, $dS = 0$. Thus, $dS_{\\text{universe}} \\ge 0$.\n3. **Ideal Gas Entropy**:\n$S(T, V) = C_v \\ln T + R \\ln V + S_0$."
        if "maxwell" in q_lower:
            return "1. **Thermodynamic Potentials**:\n$dU = TdS - PdV$, $dH = TdS + VdP$, $dF = -SdT - PdV$, $dG = -SdT + VdP$.\n2. **Derivations using exact differentials**:\nFrom $dF$: $(\\partial S/\\partial V)_T = (\\partial P/\\partial T)_V$.\nFrom $dG$: $(\\partial S/\\partial P)_T = -(\\partial V/\\partial T)_P$.\nFrom $dU$: $(\\partial T/\\partial V)_S = -(\\partial P/\\partial S)_V$.\nFrom $dH$: $(\\partial T/\\partial P)_S = (\\partial V/\\partial S)_P$."
        if "radiation" in q_lower or "blackbody" in q_lower or "planck" in q_lower:
            return "1. **Planck's Law**:\nEnergy density $u(\\lambda) d\\lambda = \\frac{8\\pi hc}{\\lambda^5} \\frac{1}{e^{hc/\\lambda k T} - 1} d\\lambda$.\n2. **Wien's Law Limit**:\nFor small wavelengths ($hc/\\lambda k T \\gg 1$), the exponential term dominates: $u(\\lambda) \\approx \\frac{8\\pi hc}{\\lambda^5} e^{-hc/\\lambda k T}$.\n3. **Rayleigh-Jeans Limit**:\nFor long wavelengths ($hc/\\lambda k T \\ll 1$), $e^x - 1 \\approx x$: $u(\\lambda) \\approx \\frac{8\\pi k T}{\\lambda^4}$."
        return "1. **Thermodynamic Analysis**:\nApply the First Law $dQ = dU + dW$ and Second Law $dS \\ge dQ/T$.\n2. **Microstate/Macrostate Equations**:\nUse partition functions or ideal gas laws to compute thermodynamic quantities like pressure, volume, and temperature.\n3. **Physical Significance**:\nExplain how the microscopic states map to macroscopic variables using statistical definitions."

    # Waves & Optics phymj31
    elif key == "phymj31":
        if "interference" in q_lower or "slit" in q_lower or "fringe" in q_lower:
            return "1. **Interference Conditions**:\nCoherent sources, constant phase difference. Maxima: path difference $\\Delta = n\\lambda$; Minima: $\\Delta = (2n+1)\\lambda/2$.\n2. **Fringe Width**:\n$\\beta = \\frac{\\lambda D}{d}$, where $D$ is source-to-screen distance, $d$ is source separation. Shape of fringes is hyperbolic, approximating straight lines near the center."
        if "diffraction" in q_lower or "grating" in q_lower:
            return "1. **Fraunhofer Diffraction**:\nDiffraction when wavefronts are plane. Grating equation: $(e+d)\\sin\\theta = n\\lambda$, where $(e+d)$ is grating element.\n2. **Resolving Power**:\n$R = \\frac{\\lambda}{d\\lambda} = nN$, where $n$ is order of diffraction, $N$ is total number of lines on grating illuminated."
        if "polarization" in q_lower or "wave plate" in q_lower:
            return "1. **Polarization Concept**:\nRestriction of transverse waves to a single plane. Unpolarized light becomes polarized via reflection, scattering, or birefringence.\n2. **Wave Plates**:\nIntroduce phase shift between ordinary and extraordinary waves. Quarter-wave plate: path diff $\\lambda/4$, thickness $t = \\frac{\\lambda}{4|n_e - n_o|}$. Half-wave plate: path diff $\\lambda/2$, thickness $t = \\frac{\\lambda}{2|n_e - n_o|}$."
        return "1. **Wave Equations & Superposition**:\nWrite waves as $y = A\\sin(kt - \\omega x)$. Add components algebraically or vectorially.\n2. **Phase / Path Difference**:\nCalculate phase difference: $\\delta = \\frac{2\\pi}{\\lambda} \\Delta x$.\n3. **Intensity Calculation**:\nResulting intensity $I = I_1 + I_2 + 2\\sqrt{I_1 I_2}\\cos\\delta$. Max intensity $I_{\\text{max}} = (A_1 + A_2)^2$, Min intensity $I_{\\text{min}} = (A_1 - A_2)^2$."

    # Semiconductor Devices phymj32
    elif key == "phymj32":
        if "ujt" in q_lower or "standoff" in q_lower:
            return "1. **UJT Standoff Ratio**:\nIntrinsic standoff ratio $\\eta = \\frac{R_{B1}}{R_{B1} + R_{B2}} = \\frac{R_{B1}}{R_{BB}}$.\n2. **Calculation**:\nGiven $R_{BB} = 8\\text{ k}\\Omega$ and $R_{B1} = 4.8\\text{ k}\\Omega$, $\\eta = 4.8 / 8 = 0.60$.\n3. **Peak Voltage**:\n$V_p = \\eta V_{BB} + V_D$, where $V_D$ is diode contact potential."
        if "diode" in q_lower or "junction" in q_lower:
            return "1. **P-N Junction depletion region**:\nDiffusion of majority carriers creates space charge region of immobile ions. depletion width $W = \\sqrt{\\frac{2\\varepsilon V_0}{q} \\left(\\frac{1}{N_d} + \\frac{1}{N_a}\\right)}$.\n2. **Diode Equation**:\n$I = I_0 (e^{qV/\\eta k T} - 1)$, where $I_0$ is reverse saturation current, $V$ is applied voltage."
        if "transistor" in q_lower or "bjt" in q_lower:
            return "1. **BJT Operations**:\nThree-terminal current-controlled device. CB current gain $\\alpha = I_c/I_e$, CE current gain $\\beta = I_c/I_b$. Relation: $\\beta = \\frac{\\alpha}{1-\\alpha}$.\n2. **Operating Regions**:\nActive (emitter base forward, collector base reverse), Cutoff (both reverse), Saturation (both forward)."
        return "1. **Carrier Transport**:\nDrift current density $J_{\\text{drift}} = q(n\\mu_n + p\\mu_p)E$. Diffusion current density $J_{\\text{diff}} = q D_n \\frac{dn}{dx}$.\n2. **Energy Band Diagram**:\nPlot conduction band ($E_c$), valence band ($E_v$), and Fermi energy ($E_f$) across the device.\n3. **I-V Relationship**:\nRelate terminal voltages to current using transport and continuity equations."

    # Electromagnetic Theory phymj41
    elif key == "phymj41":
        if "maxwell" in q_lower or "displacement" in q_lower:
            return "1. **Maxwell's Equations**:\n(i) $\\vec{\\nabla} \\cdot \\vec{E} = \\rho/\\varepsilon_0$, (ii) $\\vec{\\nabla} \\cdot \\vec{B} = 0$, (iii) $\\vec{\\nabla} \\times \\vec{E} = -\\frac{\\partial\\vec{B}}{\\partial t}$, (iv) $\\vec{\\nabla} \\times \\vec{B} = \\mu_0\\vec{J} + \\mu_0\\varepsilon_0 \\frac{\\partial\\vec{E}}{\\partial t}$.\n2. **Displacement Current**:\n$I_d = \\varepsilon_0 \\frac{\\partial\\Phi_E}{\\partial t}$. Resolves charge conservation discontinuity in Ampere's law."
        if "poynting" in q_lower:
            return "1. **Poynting Vector**:\n$\\vec{S} = \\frac{1}{\\mu_0} (\\vec{E} \\times \\vec{B})$ representing energy flow per unit area per unit time.\n2. **Poynting Theorem**:\n$-\\frac{\\partial u}{\\partial t} = \\vec{\\nabla} \\cdot \\vec{S} + \\vec{J} \\cdot \\vec{E}$, stating rate of energy decrease in a volume equals energy flux flowing out plus work done on charges."
        if "waveguide" in q_lower or "tem" in q_lower:
            return "1. **TEM wave exclusion**:\nTEM requires $E_z = 0, H_z = 0$. Since boundary is conducting, potential $\\Phi = 0$ on walls. By Laplace's uniqueness, $\\Phi = 0$ inside waveguide, meaning $\\vec{E} = 0$, so no TEM wave can exist.\n2. **Cutoff Frequency**:\n$f_c = \\frac{c}{2} \\sqrt{(m/a)^2 + (n/b)^2}$."
        return "1. **Electrodynamics Core**:\nApply Maxwell's boundary conditions and wave equations.\n2. **Wave propagation**:\nSolution of wave equation $\\nabla^2 \\vec{E} - \\mu\\varepsilon \\frac{\\partial^2 \\vec{E}}{\\partial t^2} = 0$. Impedance $\\eta = \\sqrt{\\mu/\\varepsilon}$.\n3. **Energy & Momentum**:\nEnergy density $u = \\frac{1}{2}\\varepsilon E^2 + \\frac{1}{2\\mu} B^2$, momentum density $\\vec{g} = \\vec{S}/c^2$."

    # Mathematical Physics phymj42
    elif key == "phymj42":
        if "laplacian" in q_lower or "spherical" in q_lower or "divergence" in q_lower:
            return "1. **Divergence of Curl**:\nUsing Levi-Civita symbol, $\\vec{\\nabla} \\cdot (\\vec{\\nabla} \\times \\vec{A}) = \\partial_i (\\varepsilon_{ijk} \\partial_j A_k) = \\varepsilon_{ijk} \\partial_i \\partial_j A_k = 0$ (contraction of symmetric partial derivatives with antisymmetric tensor).\n2. **Spherical Laplacian**:\n$\\nabla^2 V = \\frac{1}{r^2} \\frac{\\partial}{\\partial r}(r^2 \\frac{\\partial V}{\\partial r}) + \\frac{1}{r^2\\sin\\theta} \\frac{\\partial}{\\partial\\theta}(\\sin\\theta \\frac{\\partial V}{\\partial\\theta}) + \\frac{1}{r^2\\sin^2\\theta} \\frac{\\partial^2 V}{\\partial\\phi^2}$."
        if "legendre" in q_lower or "polynomial" in q_lower:
            return "1. **Legendre Equation**:\n$(1-x^2)y'' - 2xy' + n(n+1)y = 0$.\n2. **Generating Function**:\n$(1 - 2xt + t^2)^{-1/2} = \\sum_{n=0}^{\\infty} P_n(x) t^n$.\n3. **Orthogonality**:\n$\\int_{-1}^{1} P_m(x) P_n(x) dx = \\frac{2}{2n+1} \\delta_{mn}$."
        if "analytic" in q_lower or "cauchy" in q_lower or "residue" in q_lower:
            return "1. **Cauchy-Riemann equations**:\nFor analytic function $f(z) = u + iv$: $\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}$ and $\\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$.\n2. **Residue Theorem**:\n$\\oint_C f(z) dz = 2\\pi j \\sum \\text{Res}(f, z_k)$ where $z_k$ are singular poles enclosed by path $C$."
        return "1. **Mathematical Physics Analysis**:\nSet up coordinate system, determine boundary conditions.\n2. **Differential/Algebraic Equations**:\nUse Frobenius series expansions, coordinate scale factors, or residue calculus to solve.\n3. **Orthogonality & Normalization**:\nApply special function orthogonality relations to evaluate coefficients."

    # Quantum Mechanics phymj51
    elif key == "phymj51":
        if "photoelectric" in q_lower or "compton" in q_lower:
            return "1. **Compton Scattering**:\nPhoton of wavelength $\\lambda$ scatters off an electron at rest. Derived from relativistic energy-momentum conservation: $\\lambda' - \\lambda = \\frac{h}{m_e c}(1 - \\cos\\theta)$.\n2. **Compton Wavelength**:\n$\\lambda_c = \\frac{h}{m_e c} \\approx 0.0242\\text{ \\u00c5}$."
        if "uncertainty" in q_lower or "heisenberg" in q_lower:
            return "1. **Heisenberg Uncertainty Principle**:\nPosition and momentum cannot be measured simultaneously with arbitrary precision: $\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$.\n2. **Applications**:\nExplains why electrons do not fall into nuclei (zero-point kinetic energy prevents collapse), and estimates ground state energy of harmonic oscillator."
        if "box" in q_lower or "infinite" in q_lower or "pot" in q_lower:
            return "1. **Schrödinger Equation Setup**:\n$-\\frac{\\hbar^2}{2m} \\frac{d^2\\psi}{dx^2} = E\\psi$ inside box ($0 < x < L$), with boundary conditions $\\psi(0) = \\psi(L) = 0$.\n2. **Wave Function & Energy**:\n$\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)$ and $E_n = \\frac{n^2\\pi^2\\hbar^2}{2m L^2}$ for $n=1,2,3...$."
        return "1. **Quantum State Representation**:\nDefine wave function $\\psi(\\vec{r}, t)$, normalize it: $\\int |\\psi|^2 d^3r = 1$.\n2. **Schrödinger Operator Equation**:\nApply Hamiltonian operator $\\hat{H}\\psi = E\\psi$. Solve eigenvalue problem.\n3. **Expectation Values**:\nEvaluate $\\langle A \\rangle = \\int \\psi^* \\hat{A} \\psi d^3r$."

    # Classical Mechanics phymj52
    elif key == "phymj52":
        if "constraint" in q_lower:
            return "1. **Constraints Classification**:\n(i) Holonomic: algebraically expressible as $f(r_1, r_2, ..., t) = 0$ (e.g. rigid body constant distance).\n(ii) Non-holonomic: cannot be written as equalities (e.g. gas molecules in box or rolling without slipping, which involves differentials).\n(iii) Scleronomic: independent of time. (iv) Rheonomic: explicitly dependent on time."
        if "lagrangian" in q_lower or "lagrange" in q_lower:
            return "1. **Lagrangian Definition**:\n$L = T - V$ (Kinetic minus Potential energy).\n2. **Euler-Lagrange Equations**:\n$\\frac{d}{dt} \\left( \\frac{\\partial L}{\\partial \\dot{q}_j} \\right) - \\frac{\\partial L}{\\partial q_j} = 0$, where $q_j$ are generalized coordinates. Derived from D'Alembert's principle."
        if "hamiltonian" in q_lower or "hamilton" in q_lower:
            return "1. **Hamiltonian definition**:\nLegendre transform of $L$: $H(q, p, t) = \\sum p_i \\dot{q}_i - L$. For scleronomic conservative systems, $H = T + V$ (total energy).\n2. **Hamilton's Canonical Equations**:\n$\\dot{q}_i = \\frac{\\partial H}{\\partial p_i}$ and $\\dot{p}_i = -\\frac{\\partial H}{\\partial q_i}$."
        return "1. **Classical Mechanics Formulation**:\nIdentify constraints and select generalized coordinates $q_j$.\n2. **Lagrangian / Hamiltonian**:\nWrite kinetic energy $T$ and potential energy $V$. Construct $L = T - V$ or $H = T + V$.\n3. **Equations of Motion**:\nSolve Euler-Lagrange or Hamilton's equations to find system dynamics."

    # Statistical Mechanics phymj53
    elif key == "phymj53":
        if "partition" in q_lower or "ensemble" in q_lower:
            return "1. **Partition Function**:\nCanonical partition function $Z = \\sum_i e^{-\\beta E_i}$.\n2. **Thermodynamic Relations**:\nHelmholtz Free Energy $F = -k T \\ln Z$. Internal energy $U = -\\frac{\\partial \\ln Z}{\\partial \\beta}$. Entropy $S = \\frac{U - F}{T}$.\n3. **Equipartition Theorem**:\nEach quadratic degree of freedom contributes $\\frac{1}{2} k T$ to mean thermal energy."
        if "bose" in q_lower or "fermi" in q_lower:
            return "1. **Quantum Statistics distributions**:\n- Bose-Einstein (bosons, spin-integer, no state limits): $n_i = \\frac{1}{e^{\\beta(E_i - \\mu)} - 1}$.\n- Fermi-Dirac (fermions, spin-half, Pauli exclusion): $n_i = \\frac{1}{e^{\\beta(E_i - \\mu)} + 1}$.\n2. **Bose-Einstein Condensation**:\nPhase transition at low temperatures where macroscopic fraction of particles occupy ground state."
        return "1. **Statistical System Setup**:\nDefine microscopic states, compute energy levels $E_i$.\n2. **Ensemble Partitioning**:\nWrite down partition function $Z$ and calculate thermodynamic variables.\n3. **Thermodynamic Limits**:\nTake limit as $N, V \\to \\infty$ to obtain macroscopic thermodynamic equations."

    # Electronic Circuits phymj61
    elif key == "phymj61":
        if "op-amp" in q_lower or "amplifier" in q_lower:
            return "1. **Ideal Op-Amp Features**:\nInfinite input impedance, zero output impedance, infinite open-loop gain, infinite bandwidth, zero common-mode gain.\n2. **Inverting Amplifier**:\nVirtual ground at negative input: $V_{\\text{out}} = -\\frac{R_f}{R_in} V_{\\text{in}}$. Non-inverting Amplifier: $V_{\\text{out}} = \\left(1 + \\frac{R_f}{R_in}\\right) V_{\\text{in}}$."
        if "oscillator" in q_lower:
            return "1. **Barkhausen Criterion**:\nFor sustained oscillations, loop gain must be unity: $|A\\beta| = 1$ and phase shift around loop must be $0$ or integer multiple of $2\\pi$.\n2. **Wien Bridge Oscillator Frequency**:\nFeedback network phase shift is 0 at resonance: $f = \\frac{1}{2\\pi RC}$."
        return "1. **Network Analysis**:\nApply KCL, KVL, or theorems (Thevenin/Norton) to determine branch currents and voltages.\n2. **Active Device Modeling**:\nUse h-parameter equivalent circuit for BJT or small-signal model for FET.\n3. **Logic Minimization**:\nApply Boolean rules or Karnaugh maps to simplify digital circuits."

    # Solid State Physics phymj62
    elif key == "phymj62":
        if "miller" in q_lower or "crystal" in q_lower:
            return "1. **Miller Indices Definition**:\nReciprocals of fractional intercepts of a crystal plane with unit cell axes, reduced to lowest integers: $(h k l)$.\n2. **Interplanar Spacing**:\nFor cubic lattice: $d_{hkl} = \\frac{a}{\\sqrt{h^2 + k^2 + l^2}}$.\n3. **NaCl Structure**:\nFCC lattice with two-atom basis: Na at $(0,0,0)$ and Cl at $(1/2,0,0)$."
        if "bragg" in q_lower:
            return "1. **Bragg's Law**:\nConstructive interference of X-rays scattered from atomic planes: $2d\\sin\\theta = n\\lambda$, where $d$ is plane spacing, $\\theta$ is Bragg angle.\n2. **Reciprocal Lattice**:\nFourier transform of direct lattice. Bragg's law in reciprocal space is expressed as the Laue condition: $\\Delta \\vec{k} = \\vec{G}$."
        return "1. **Crystal Solid Model**:\nIdentify direct crystal structures and unit cells.\n2. **Reciprocal Space & Waves**:\nConstruct reciprocal lattice vectors, plot dispersion curves $\\omega(k)$ or energy bands $E(k)$.\n3. **Macroscopic Properties**:\nIntegrate density of states $D(E)$ over Fermi-Dirac distribution to obtain heat capacity, electrical conductivity, etc."

    # Atomic & Modern phymj63
    elif key == "phymj63":
        if "coupling" in q_lower or "zeeman" in q_lower:
            return "1. **LS Coupling**:\nSpin-orbit interaction where individual spins couple $\\vec{S} = \\sum \\vec{s}_i$, orbital angular momenta couple $\\vec{L} = \\sum \\vec{l}_i$, then total angular momentum $\\vec{J} = \\vec{L} + \\vec{S}$.\n2. **Zeeman Effect**:\nSplitting of spectral lines in external magnetic field $\\vec{B}$. Normal Zeeman: splits into 3 lines due to orbital magnetic moment interaction: $\\Delta E = \\mu_B B m_l$."
        if "laser" in q_lower or "einstein" in q_lower:
            return "1. **Einstein Coefficients**:\n$A_{21}$ (spontaneous emission rate), $B_{21}$ (stimulated emission rate), $B_{12}$ (absorption rate). Relation: $B_{12} = B_{21}$ and $\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}$.\n2. **Population Inversion**:\nAchieving $N_2 > N_1$ by optical pumping, required for optical amplification."
        return "1. **Atomic/Molecular States**:\nSet up energy eigenvalues using quantum mechanical rules (vector atom model, rigid rotator, Morse potential).\n2. **Radiative Transitions**:\nApply selection rules (e.g., $\\Delta L = \\pm 1, \\Delta J = 0, \\pm 1$) to find allowed spectral lines.\n3. **Spectral Intensity**:\nRelate lines to populations via Boltzmann distribution or transition rates."

    # Nuclear Physics phymj64
    elif key == "phymj64":
        if "formula" in q_lower or "semi-empirical" in q_lower:
            return "1. **Semi-Empirical Mass Formula**:\n$B(A,Z) = a_v A - a_s A^{2/3} - a_c \\frac{Z(Z-1)}{A^{1/3}} - a_a \\frac{(A-2Z)^2}{A} + \\delta(A,Z)$.\n2. **Physical Terms**:\nVolume energy, Surface tension correction, Coulomb repulsion of protons, Asymmetry term, Pairing energy term."
        if "deuteron" in q_lower:
            return "1. **Deuteron Ground State**:\nSimplest bound nuclear system ($J^\\pi = 1^+$, binding energy $B_d = 2.224\\text{ MeV}$). Ground state is primarily $^3S_1$ (orbital $L=0$, spin $S=1$) mixed with a small fraction of $^3D_1$ due to nuclear tensor force.\n2. **Tensor Force**:\nNon-central force, explaining non-zero electric quadrupole moment."
        if "decay" in q_lower or "alpha" in q_lower:
            return "1. **Gamow's Alpha Decay**:\nQuantum mechanical tunneling of alpha particle through Coulomb barrier. Decay constant $\\lambda = f \\cdot P$, where $f$ is collision frequency, $P = e^{-2G}$ is barrier transmission coefficient.\n2. **Geiger-Nuttall law**:\n$\\log \\lambda = A + B \\log E$."
        return "1. **Nuclear System Properties**:\nCalculate binding energy $BE = [Z m_p + (A-Z) m_n - M(A,Z)] c^2$.\n2. **Nuclear Model Calculations**:\nApply shell model configurations to find nuclear spin/parity, or liquid drop model for fission.\n3. **Conservation Laws**:\nCheck conservation of mass-energy, charge, baryon number, strangeness, and parity in decays or reactions."

    # Nanoscience phymj75
    elif key == "phymj75":
        if "confinement" in q_lower or "states" in q_lower:
            return "1. **Quantum Confinement**:\nReduction of nanomaterial size below exciton Bohr radius, creating discrete energy levels.\n2. **Density of States (DOS)**:\n- 3D (bulk): $D(E) \\propto E^{1/2}$.\n- 2D (quantum well): $D(E) = \\text{constant}$ (step-like).\n- 1D (quantum wire): $D(E) \\propto E^{-1/2}$ (Van Hove singularities).\n- 0D (quantum dot): $D(E) \\propto \\delta(E - E_n)$ (delta function peaks)."
        if "sem" in q_lower or "tem" in q_lower or "characterization" in q_lower:
            return "1. **XRD Scherrer Formula**:\nEstimates crystallite size $d = \\frac{K \\lambda}{\\beta \\cos\\theta}$, where $K \\approx 0.9$ is shape factor, $\\beta$ is full-width at half-maximum (FWHM) of diffraction peak.\n2. **TEM vs SEM**:\nSEM detects backscattered/secondary electrons from sample surface (3D topology). TEM detects transmitted electrons through thin sample (atomic lattice structures)."
        return "1. **Nanostructure Analysis**:\nEvaluate quantum confinement dimensions.\n2. **Synthesizing / Structuring**:\nCompare chemical vapor deposition, sol-gel processes, or lithography.\n3. **Properties evaluation**:\nAnalyze shifts in absorption edges (blue shift) or magnetic properties (superparamagnetism)."
        
    return "1. **Core Physics Concepts**:\nAnalyze the problem using fundamental equations and physical boundaries.\n2. **Mathematical Formulation**:\nSet up integration or differential equations. Apply boundary conditions to obtain exact solutions.\n3. **Verification**:\nCross-check variables, check dimensional consistency, and evaluate limiting approximations."

# 3. Parse .tex files directly from PHYSICS OUT
def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean double curly brace typos in transcribed files
    content = content.replace(r'\end{{parts}}', r'\end{parts}')
    content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
    
    # Remove comments
    content = re.sub(r'(?m)^%.*$', '', content)
    
    doc_start = content.find(r'\begin{document}')
    idx = 0
    if doc_start != -1:
        idx = doc_start + len(r'\begin{document}')
    
    subcontent = content[idx:]
    pattern = r'(\\begin\{parts\}|\\end\{parts\}|\\item)'
    tokens = re.split(pattern, subcontent)
    
    stack = []
    current_items = []
    all_questions = []
    
    def clean_text(text):
        # Clean LaTeX accents
        text = text.replace(r'\"{o}', 'ö')
        text = text.replace(r'\'e', 'é')
        text = text.replace(r'\"{a}', 'ä')
        text = text.replace(r'\"o', 'ö')
        text = text.replace(r'\'erot', 'érot') # specifically for Fabry-Perot
        
        # Remove \pts{...}
        text = re.sub(r'\\pts\{[^\}]*\}', '', text)
        # Remove \hfill, \smallskip, \mediumskip, etc.
        text = re.sub(r'\\hfill', '', text)
        text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
        text = re.sub(r'\\noindent', '', text)
        text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
        # Replace LaTeX text formatting (only if NOT inside math mode to be safe)
        text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
        # Replace non-breaking space
        text = text.replace('~', ' ')
        # Replace double backslashes with spaces
        text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    for token in tokens:
        if not token:
            continue
        token_strip = token.strip()
        if token_strip == r'\begin{parts}':
            stack.append(current_items)
            current_items = []
        elif token_strip == r'\end{parts}':
            if stack:
                parent_items = stack.pop()
                if parent_items:
                    # Nested parts: merge into parent's last item
                    last_parent = parent_items[-1]
                    sub_text = " " + " ".join(f"({idx+1}) {clean_text(item)}" for idx, item in enumerate(current_items))
                    parent_items[-1] = last_parent + sub_text
                    current_items = parent_items
                else:
                    # Top-level parts: collect questions
                    for item in current_items:
                        cleaned = clean_text(item)
                        if len(cleaned) > 15:
                            all_questions.append(cleaned)
                    current_items = []
        elif token_strip == r'\item':
            current_items.append("")
        else:
            if current_items:
                current_items[-1] += " " + token
                
    # Collect any leftovers
    for item in current_items:
        cleaned = clean_text(item)
        if len(cleaned) > 15:
            all_questions.append(cleaned)
            
    return all_questions

# Scan PHYSICS OUT directory
subjects_raw_questions = {}
tex_files = [f for f in os.listdir('aaa/PHYSICS OUT') if f.endswith('.tex')]

for file_name in tex_files:
    code = file_name.split("_")[0]
    key = None
    if code.startswith("BPT-101") or code.startswith("BSCU7A"):
        key = "phymj11"
    elif code.startswith("BPT-201") or code.startswith("BP-Anc-I"):
        key = "phymj21"
    elif code.startswith("BPT-301"):
        key = "phymj31"
    elif code.startswith("BPT-401") and "Electromagnetic" in file_name:
        key = "phymj41"
    elif code.startswith("BPT-401") and "Electronics" in file_name:
        key = "phymj61"
    elif code.startswith("BPT-501"):
        key = "phymj42"
    elif code.startswith("BPT-502"):
        key = "phymj52"
    elif code.startswith("BPT-503"):
        key = "phymj51"
    elif code.startswith("BPT-504"):
        key = "phymj32"
    elif code.startswith("BPT-505"):
        key = "phymj41"
    elif code.startswith("BPT-601"):
        key = "phymj53"
    elif code.startswith("BPT-602"):
        key = "phymj62"
    elif code.startswith("BPT-603"):
        key = "phymj64"
    elif code.startswith("BPT-604") or code.startswith("BPE-601"):
        key = "phymj63"
    elif code.startswith("BPE-602"):
        key = "phymj75"
    elif code.startswith("BSC-07A") or code == "PHYSICS":
        key = "phymj41"
        
    if not key:
        continue
        
    if key not in subjects_raw_questions:
        subjects_raw_questions[key] = []
        
    qs = parse_tex_file(os.path.join('aaa/PHYSICS OUT', file_name))
    subjects_raw_questions[key].extend(qs)

# Load existing exams database
with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

# Major/minor mapping
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

print("Populating physics questions from transcribed TeX papers...")
for unique_key, active_list in unique_to_active.items():
    raw_qs = subjects_raw_questions.get(unique_key, [])
    standard_qs = SUBJECT_SYLLABI[unique_key]["standard_questions"]
    
    # Remove duplicates
    seen = set()
    final_questions = []
    for q_text in raw_qs:
        q_norm = q_text.lower().strip()
        if q_norm not in seen and len(q_text) > 25:
            seen.add(q_norm)
            final_questions.append(q_text)
            
    # Pad with syllabus standard questions if fewer than 50
    std_idx = 0
    while len(final_questions) < 50 and std_idx < len(standard_qs):
        q_text, unit = standard_qs[std_idx]
        q_norm = q_text.lower().strip()
        if q_norm not in seen:
            seen.add(q_norm)
            final_questions.append((q_text, unit))
        std_idx += 1
        
    # If still fewer than 50, pad with general questions
    fallback_idx = 1
    while len(final_questions) < 50:
        q_text = f"Discuss advanced theoretical foundations and experimental methodologies of {SUBJECT_SYLLABI[unique_key]['title']} (Part {fallback_idx})."
        final_questions.append((q_text, "V"))
        fallback_idx += 1
        
    # Slice to exactly 50 questions
    final_questions = final_questions[:50]
    
    formatted_questions = []
    for idx, item in enumerate(final_questions):
        q_id = idx + 1
        if isinstance(item, tuple):
            q_text = item[0]
            unit = item[1]
        else:
            q_text = item
            unit_num = (idx // 10) + 1
            unit_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
            unit = unit_romans.get(unit_num, "V")
            
        ans_key = get_custom_answer_key(unique_key, q_text)
        
        formatted_questions.append({
            "id": q_id,
            "unit": unit,
            "question": q_text,
            "answerKey": ans_key
        })
        
    # Inject into active subjects
    for active_key in active_list:
        orig = EXAMS.get(active_key, {})
        EXAMS[active_key] = {
            "id": active_key,
            "title": orig.get("title", SUBJECT_SYLLABI[unique_key]["title"]),
            "module": orig.get("module", unique_key.upper()),
            "duration": 60,
            "type": "theory",
            "comingSoon": False,
            "questions": formatted_questions
        }

# 4. Cleanup unwrapped LaTeX in Mathematics subjects (matmj43, matmn41)
math_replacements = {
    r"Find the general solution of the first-order linear differential equation: \frac{dy}{dx} + y\cot x = 2x\csc x.":
        r"Find the general solution of the first-order linear differential equation: $\frac{dy}{dx} + y\cot x = 2x\csc x$.",
        
    r"Find the singular solution of the Clairaut's equation: y = px + a\sqrt{1+p^2}, where p = \frac{dy}{dx} and a is a constant.":
        r"Find the singular solution of the Clairaut's equation: $y = px + a\sqrt{1+p^2}$, where $p = \frac{dy}{dx}$ and $a$ is a constant.",
        
    r"Find the envelope of the family of straight lines y = mx + \frac{a}{m}, where m is a parameter and a is a constant.":
        r"Find the envelope of the family of straight lines $y = mx + \frac{a}{m}$, where $m$ is a parameter and $a$ is a constant.",
        
    r"Find the general solution of the second-order linear differential equation with constant coefficients: \frac{d^2y}{dx^2} - 5\frac{dy}{dx} + 6y = e^{4x}.":
        r"Find the general solution of the second-order linear differential equation with constant coefficients: $\frac{d^2y}{dx^2} - 5\frac{dy}{dx} + 6y = e^{4x}$.",
        
    r"Solve the differential equation with constant coefficients: \frac{d^2y}{dx^2} + 4y = \sin 2x.":
        r"Solve the differential equation with constant coefficients: $\frac{d^2y}{dx^2} + 4y = \sin 2x$.",
        
    r"Solve the Cauchy-Euler homogeneous linear differential equation: x^2\frac{d^2y}{dx^2} - 3x\frac{dy}{dx} + 4y = 0 for x > 0.":
        r"Solve the Cauchy-Euler homogeneous linear differential equation: $x^2\frac{d^2y}{dx^2} - 3x\frac{dy}{dx} + 4y = 0$ for $x > 0$.",
        
    r"Find the general solution of the Euler-Cauchy equation: x^2\frac{d^2y}{dx^2} - x\frac{dy}{dx} - 3y = x^5.":
        r"Find the general solution of the Euler-Cauchy equation: $x^2\frac{d^2y}{dx^2} - x\frac{dy}{dx} - 3y = x^5$.",
        
    r"Find the Particular Integral of the differential equation: \frac{d^3y}{dx^3} - \frac{dy}{dx} = e^x + \cos x.":
        r"Find the Particular Integral of the differential equation: $\frac{d^3y}{dx^3} - \frac{dy}{dx} = e^x + \cos x$.",
        
    r"Use the method of Variation of Parameters to find the particular integral of the differential equation: \frac{d^2y}{dx^2} + y = \sec x.":
        r"Use the method of Variation of Parameters to find the particular integral of the differential equation: $\frac{d^2y}{dx^2} + y = \sec x$.",
        
    r"Transform the differential equation to normal form (removal of first derivative) and solve: \frac{d^2y}{dx^2} - 2\tan x \frac{dy}{dx} + 5y = 0.":
        r"Transform the differential equation to normal form (removal of first derivative) and solve: $\frac{d^2y}{dx^2} - 2\tan x \frac{dy}{dx} + 5y = 0$.",
        
    r"Find the series solution of the differential equation about the ordinary point x=0: \frac{d^2y}{dx^2} + x y = 0.":
        r"Find the series solution of the differential equation about the ordinary point $x=0$: $\frac{d^2y}{dx^2} + x y = 0$.",
        
    r"Explain the qualitative behavior of solutions to the autonomous differential equation \frac{dy}{dt} = y(2-y). Find the equilibrium solutions and determine their stability.":
        r"Explain the qualitative behavior of solutions to the autonomous differential equation $\frac{dy}{dt} = y(2-y)$. Find the equilibrium solutions and determine their stability.",
        
    r"Solve the first-order linear partial differential equation using Lagrange's method: yz p + zx q = xy, where p = \frac{\partial z}{\partial x} and q = \frac{\partial z}{\partial y}.":
        r"Solve the first-order linear partial differential equation using Lagrange's method: $yz p + zx q = xy$, where $p = \frac{\partial z}{\partial x}$ and $q = \frac{\partial z}{\partial y}$.",
        
    r"Find the general solution of the homogeneous linear second-order PDE: \frac{\partial^2 z}{\partial x^2} - 3\frac{\partial^2 z}{\partial x \partial y} + 2\frac{\partial^2 z}{\partial y^2} = 0.":
        r"Find the general solution of the homogeneous linear second-order PDE: $\frac{\partial^2 z}{\partial x^2} - 3\\frac{\partial^2 z}{\partial x \partial y} + 2\frac{\partial^2 z}{\partial y^2} = 0$.",
        
    r"Find the Particular Integral of (D^2 - D'^2)z = \cos(x + y) where D = \frac{\partial}{\partial x}, D' = \frac{\partial}{\partial y}.":
        r"Find the Particular Integral of $(D^2 - D'^2)z = \cos(x + y)$ where $D = \frac{\partial}{\partial x}$, $D' = \frac{\partial}{\partial y}$.",
        
    r"Solve the variable coefficient PDE reducible to constant coefficients (Euler-type PDE): x^2 \frac{\partial^2 z}{\partial x^2} - y^2 \frac{\partial^2 z}{\partial y^2} = 0.":
        r"Solve the variable coefficient PDE reducible to constant coefficients (Euler-type PDE): $x^2 \frac{\partial^2 z}{\partial x^2} - y^2 \frac{\partial^2 z}{\partial y^2} = 0$.",
        
    r"Solve the partial differential equation: z \frac{\partial z}{\partial x} = -y.":
        r"Solve the partial differential equation: $z \frac{\partial z}{\partial x} = -y$.",
        
    r"Find the complete integral of z = px + qy + p^2 + q^2, where p = \partial z/\partial x, q = \partial z/\partial y.":
        r"Find the complete integral of $z = px + qy + p^2 + q^2$, where $p = \partial z/\partial x$, $q = \partial z/\partial y$.",
        
    r"Solve (D_x^3 - 4D_x^2D_y + 4D_xD_y^2)z = 0, where D_x \equiv \partial/\partial x, D_y \equiv \partial/\partial y.":
        r"Solve $(D_x^3 - 4D_x^2D_y + 4D_xD_y^2)z = 0$, where $D_x \equiv \partial/\partial x$, $D_y \equiv \partial/\partial y$.",
        
    r"Find the general solution of r + p - q = z, where r = \frac{\partial^2 z}{\partial x^2}, p = \frac{\partial z}{\partial x}, q = \frac{\partial z}{\partial y}.":
        r"Find the general solution of $r + p - q = z$, where $r = \frac{\partial^2 z}{\partial x^2}$, $p = \frac{\partial z}{\partial x}$, $q = \frac{\partial z}{\partial y}$.",
        
    r"Solve xr + p = 9x^2y^2, where r = \frac{\partial^2 z}{\partial x^2} and p = \frac{\partial z}{\partial x}.":
        r"Solve $xr + p = 9x^2y^2$, where $r = \frac{\partial^2 z}{\partial x^2}$ and $p = \frac{\partial z}{\partial x}$.",
        
    r"Obtain the general integral of the partial differential equation: p + 3q = 5z + \tan(y - 3x), where p = \frac{\partial z}{\partial x}, q = \frac{\partial z}{\partial y}.":
        r"Obtain the general integral of the partial differential equation: $p + 3q = 5z + \tan(y - 3x)$, where $p = \frac{\partial z}{\partial x}$, $q = \frac{\partial z}{\partial y}$.",
        
    r"Find the general integral of the equation r + s - 6t = y \cos x (where r = z_{xx}, s = z_{xy}, t = z_{yy}).":
        r"Find the general integral of the equation $r + s - 6t = y \cos x$ (where $r = z_{xx}$, $s = z_{xy}$, $t = z_{yy}$).",
        
    r"Reduce the equation x^2 \frac{\partial^2 z}{\partial x^2} - 4xy \frac{\partial^2 z}{\partial x \partial y} + 4y^2 \frac{\partial^2 z}{\partial y^2} + 6y \frac{\partial z}{\partial y} = x^2 y^3 to linear equation with constant coefficients and then solve it.":
        r"Reduce the equation $x^2 \frac{\partial^2 z}{\partial x^2} - 4xy \frac{\partial^2 z}{\partial x \partial y} + 4y^2 \frac{\partial^2 z}{\partial y^2} + 6y \frac{\partial z}{\partial y} = x^2 y^3$ to linear equation with constant coefficients and then solve it.",
        
    r"Solve the partial differential equation: yz - p = x^2 y^2 \cos(xy), where p = \frac{\partial z}{\partial x}.":
        r"Solve the partial differential equation: $yz - p = x^2 y^2 \cos(xy)$, where $p = \frac{\partial z}{\partial x}$.",
        
    r"Reduce the following equation to canonical form and solve it: y^2 \frac{\partial^2 z}{\partial x^2} - 2xy \frac{\partial^2 z}{\partial x \partial y} + x^2 \frac{\partial^2 z}{\partial y^2} = \frac{y^2}{x} \frac{\partial z}{\partial x} + \frac{x^2}{y} \frac{\partial z}{\partial y}.":
        r"Reduce the following equation to canonical form and solve it: $y^2 \frac{\partial^2 z}{\partial x^2} - 2xy \frac{\partial^2 z}{\partial x \partial y} + x^2 \frac{\partial^2 z}{\partial y^2} = \frac{y^2}{x} \frac{\partial z}{\partial x} + \frac{x^2}{y} \frac{\partial z}{\partial y}$.",
        
    r"Use the method of separation of variables to solve the heat equation: \frac{\partial u}{\partial t} = \alpha^2 \frac{\partial^2 u}{\partial x^2}, 0 < x < 1, t > 0, subject to boundary conditions u(x,0) = x^2 - x, u(0,t) = u(1,t) = 0.":
        r"Use the method of separation of variables to solve the heat equation: $\frac{\partial u}{\partial t} = \alpha^2 \frac{\partial^2 u}{\partial x^2}$, $0 < x < 1$, $t > 0$, subject to boundary conditions $u(x,0) = x^2 - x$, $u(0,t) = u(1,t) = 0$.",
        
    r"Solve the wave equation \frac{\partial^2 u}{\partial t^2} = a^2 \frac{\partial^2 u}{\partial x^2} using the method of separation of variables.":
        r"Solve the wave equation $\frac{\partial^2 u}{\partial t^2} = a^2 \frac{\partial^2 u}{\partial x^2}$ using the method of separation of variables."
}

print("Cleaning up math questions in matmj43 and matmn41...")
for math_key in ["matmj43", "matmn41"]:
    exam = EXAMS.get(math_key)
    if not exam or "questions" not in exam:
        continue
    for q in exam["questions"]:
        orig = q["question"]
        if orig in math_replacements:
            q["question"] = math_replacements[orig]

# Write unified exams data back to js/exams-data.js
output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
with open("js/exams-data.js", "w", encoding="utf-8") as f:
    f.write(output_str)

print("Unified populate and cleanup complete! exams-data.js has been updated.")
