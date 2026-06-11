"""
audit_and_fix_chemistry.py
==========================
Audits all live Chemistry exams in js/exams-data.js for Semesters 1-4 against
chemistry_syllabus.json. Replaces out-of-syllabus and placeholder questions with
syllabus-aligned questions sourced from PYQ tex files, then fills remaining gaps
with generated questions.
"""

import json
import re
import os

# ───────────────────────────────────────────────────────────────────────────────
# 1. Syllabus topic definitions (keywords for each paper/unit)
# ───────────────────────────────────────────────────────────────────────────────

PAPER_TOPICS = {
    "chemd11": {
        "title": "Basic Principles of Chemistry and Its Applications in Daily Life",
        "units": {
            "I":  ["atoms", "molecules", "electronic structure", "chemical bonding", "hybridization",
                   "intermolecular forces", "bond formation", "oxidation number", "reducing agent",
                   "oxidizing agent"],
            "II": ["thermodynamics", "enthalpy", "entropy", "free energy", "chemical reactions",
                   "exothermic", "endothermic", "spontaneous"],
            "III": ["dyes", "pigments", "polymers", "polyester", "rubber", "nylon", "bakelite",
                    "biopolymer", "food preservative", "adulteration", "fragrance", "soap",
                    "detergent", "surfactant", "cleansing", "polymer"],
        }
    },
    "chemd21": {
        "title": "Energy & Metallurgy",
        "units": {
            "I":  ["photosynthesis", "light reaction", "dark reaction", "calvin cycle",
                   "photorespiration", "artificial photosynthesis"],
            "II": ["energy", "renewable", "non-renewable", "petroleum", "natural gas", "coal",
                   "nuclear energy", "solar energy", "biomass", "biogas", "fuel cell", "li-ion battery",
                   "octane", "cetane"],
            "III": ["metallurgy", "iron", "copper", "stainless steel", "corrosion", "ore",
                    "blast furnace", "metal extraction"],
        }
    },
    "chemd31": {
        "title": "Environmental Chemistry",
        "units": {
            "I":  ["environmental chemistry", "pollution", "contamination", "do", "bod", "cod",
                   "tlv", "receptor", "sink", "pollutant"],
            "II": ["atmosphere", "greenhouse", "global warming", "ozone", "hydrosphere",
                   "eutrophication", "lithosphere", "soil", "biosphere", "carbon footprint"],
            "III": ["hydrological cycle", "oxygen cycle", "nitrogen cycle", "phosphate cycle",
                    "sulfur cycle", "natural cycle"],
            "IV": ["air pollution", "auto exhaust", "water pollution", "acid rain",
                   "wastewater treatment", "effluent", "el-nino"],
        }
    },
    "chemj11": {
        "title": "Basic Concepts of Chemistry-I",
        "units": {
            "I":  ["wave-particle duality", "heisenberg", "uncertainty", "schrödinger", "schrodinger",
                   "wave equation", "eigenvalue", "eigenfunction", "wave function", "psi",
                   "radial", "angular", "effective nuclear charge", "slater"],
            "II": ["periodic table", "atomic size", "covalent radius", "ionic radius", "van der waals",
                   "lanthanide contraction", "ionization energy", "electron affinity", "inert pair",
                   "electronegativity", "pauling", "mulliken", "allred rochow",
                   "lattice energy", "born-haber", "born lande", "solvation", "hydration",
                   "fajan", "redox", "electrode potential", "electrochemical series", "latimer", "frost"],
            "III": ["kinetic theory", "ideal gas", "maxwell distribution", "equipartition",
                    "collision", "mean free path", "van der waals gas", "real gas", "critical"],
            "IV": ["surface tension", "capillary", "viscosity", "liquid state"],
            "V":  ["crystal", "lattice", "unit cell", "miller indices", "bragg", "nacl", "graphite",
                   "diamond", "solid state"],
            "VI": ["first law thermodynamics", "isothermal", "adiabatic", "kirchhoff", "joule",
                   "joule-thomson", "second law", "carnot", "entropy", "free energy", "gibbs",
                   "helmholtz", "maxwell relations", "third law"],
        }
    },
    "chemj21": {
        "title": "Basic Concepts of Chemistry-II",
        "units": {
            "I":  ["valence bond", "molecular orbital", "mo theory", "homonuclear", "heteronuclear",
                   "homo", "lumo", "hybridization", "bent's rule", "vsepr", "multi-center",
                   "diborane", "multiple bonding", "pi-pi", "pi-d"],
            "II": ["ionic bonding", "crystal packing", "radius ratio", "rock salt", "zinc blende",
                   "wurtzite", "rutile", "brookite", "anatase"],
            "III": ["metallic bonding", "free electron", "band theory", "valence bond metal"],
            "IV": ["hydrogen bonding", "weak interaction", "intermolecular"],
            "V":  ["electronic effect", "inductive", "resonance", "mesomeric", "hyperconjugation",
                   "steric", "acidity", "basicity"],
            "VI": ["stereochemistry", "fischer", "newman", "chirality", "optical activity",
                   "enantiomer", "diastereomer", "configuration", "r/s", "d/l", "geometrical isomerism",
                   "e/z", "conformation", "butane"],
            "VII": ["alkene", "alkyne", "addition reactions", "hydration", "hydroboration",
                    "epoxidation", "ozonolysis", "diels-alder", "diene", "electrophilic",
                    "free radical", "conjugated"],
            "VIII": ["alkyl halide", "nucleophilic substitution", "sn1", "sn2", "sni",
                     "elimination", "e1", "e2", "e1cb", "grignard"],
            "IX": ["alcohol", "ether", "primary", "secondary", "tertiary"],
            "X":  ["active methylene", "ethyl acetoacetate", "diethyl malonate"],
        }
    },
    "chemj31": {
        "title": "Inorganic Chemistry - I",
        "units": {
            "I":  ["main group", "alkali", "alkaline earth", "flame coloration", "complexes",
                   "crown ether", "cryptand", "electride", "metalloid", "allotrope",
                   "hydride", "halide", "hydroxide", "oxo-acid", "oxide"],
            "II": ["silicate", "zeolite", "glass", "ceramic", "refractory", "cement",
                   "fertilizer", "nitrogenous", "phosphate fertilizer"],
        }
    },
    "chemj32": {
        "title": "Organic Chemistry - I",
        "units": {
            "I":  ["carbonyl", "aldehyde", "ketone", "aldol", "cannizzaro", "perkin",
                   "benzoin", "haloform", "mannich", "baylis-hillman", "acid chloride",
                   "acid anhydride", "amide", "ester", "hvz", "reactivity"],
            "II": ["phosphorus ylide", "sulfur ylide", "wittig", "arbuzov", "horner"],
            "III": ["aromaticity", "antiaromaticity", "homoaromaticity", "benzene",
                    "benzenoid", "non-benzenoid", "alternant"],
            "IV": ["aromatic electrophilic substitution", "nitration", "halogenation",
                   "sulphonation", "friedel-crafts", "alkylation", "acylation", "substituent",
                   "ortho", "para", "orientation"],
            "V":  ["phenol", "preparation", "reactions"],
        }
    },
    "chemj33": {
        "title": "Physical Chemistry - I",
        "units": {
            "I":  ["electrolyte", "conductance", "ionic conductance", "transference",
                   "transport number", "kohlrausch", "ionic mobility", "conductometric"],
            "II": ["electrode", "electrode potential", "emf", "electrochemical cell",
                   "concentration cell", "liquid junction", "salt bridge", "glass electrode",
                   "pH", "potentiometric", "buffer", "indicator"],
            "III": ["phase equilibria", "clapeyron", "clausius", "phase rule", "phase diagram",
                    "water system", "phenol-water", "pb-ag", "distribution law"],
            "IV": ["chemical kinetics", "rate law", "zero order", "first order", "second order",
                   "pseudo", "steady state", "arrhenius", "collision theory", "transition state"],
        }
    },
    "chemj34": {
        "title": "Qualitative Analysis and Thermochemistry",
        "units": {
            "I":  ["qualitative analysis", "cation", "anion", "group", "systematic",
                   "semi-microanalysis", "inorganic salt"],
            "II": ["organic compound", "functional group", "melting point", "element detection",
                   "preliminary test"],
            "III": ["thermochemistry", "calorimeter", "enthalpy", "neutralization", "ionization",
                    "solution", "heat of"],
        }
    },
    "chemj41": {
        "title": "Inorganic Chemistry - II",
        "units": {
            "I":  ["acid", "base", "brønsted", "lowry", "lux-flood", "lewis acid", "hsab",
                   "hard soft", "symbiosis", "super-acid", "frustrated"],
            "II": ["non-aqueous solvent", "liquid ammonia", "ionic liquid", "green synthesis",
                   "solvent-free", "dielectric constant", "dipole moment"],
            "III": ["transition metal", "d-block", "oxidation state", "color", "magnetic moment",
                    "complex formation", "catalytic"],
            "IV": ["coordination", "werner", "ligand", "denticity", "ean", "valence bond theory",
                   "geometrical isomerism", "optical isomerism", "nomenclature"],
            "V":  ["lanthanide", "actinide", "lanthanide contraction", "separation",
                   "electronic configuration", "ionic radii", "oxidation state complex"],
        }
    },
    "chemj42": {
        "title": "Organic Chemistry - II",
        "units": {
            "I":  ["nitrogen compound", "nitrobenzene", "aniline", "diazonium"],
            "II": ["heterocyclic", "furan", "pyrrole", "thiophene", "pyridine", "indole",
                   "quinoline", "synthesis", "reactions"],
            "III": ["naphthalene", "anthracene", "polynuclear"],
            "IV": ["malachite green", "fluorescein", "indigotin", "colour constitution", "dye"],
            "V":  ["cycloalkane", "alicyclic", "baeyer strain", "cyclohexane", "conformation",
                   "chair", "boat", "disubstituted"],
            "VI": ["protection", "deprotection", "functional group", "nh group", "oh group",
                   "diol", "carbonyl group", "carboxyl"],
            "VII": ["carbohydrate", "glucose", "aldose", "ketose", "mutarotation", "anomeric",
                    "sucrose", "starch", "cellulose", "glycosylation", "iminosugar", "sialic acid"],
        }
    },
    "chemj43": {
        "title": "Physical Chemistry - II",
        "units": {
            "I":  ["partial molal", "chemical potential", "gibbs-duhem", "fugacity",
                   "activity coefficient", "lewis-randall", "mixing", "ideal solution",
                   "duhem-margules", "henry", "raoult", "colligative", "osmotic pressure",
                   "freezing point", "boiling point", "van't hoff"],
            "II": ["langmuir", "adsorption", "bet equation", "surface area", "gibbs adsorption",
                   "surface reaction", "enzyme kinetics", "michaelis-menten"],
            "III": ["photochemical", "quantum efficiency", "kinetics", "h2-br2", "hi decomposition",
                    "photostationary", "anthracene dimerisation", "stern-volmer"],
            "IV": ["nuclear chemistry", "radioactivity", "decay kinetics", "artificial radioactivity",
                   "gm counter", "nuclear reaction", "radioisotope", "tracer", "age determination",
                   "radiolysis", "radiation chemistry"],
        }
    },
    "chemj44": {
        "title": "Techniques in Chemistry",
        "units": {
            "I":  ["distillation", "crystallization", "precipitation", "extraction",
                   "chromatography", "uv-visible", "infrared", "ir spectroscopy", "nmr"],
            "II": ["analysis", "stoichiometric", "primary standard", "secondary standard",
                   "molarity", "normality", "molality", "ppm", "percentage"],
            "III": ["acid-base equilibria", "acids", "bases", "ph", "titration",
                    "complexometric", "redox titration", "precipitation titration", "indicator"],
        }
    },
}

# Mirror papers
PAPER_MIRRORS = {
    "chemn11": "chemj11",
    "chemn21": "chemj21",
    "chemn41": "chemj43",
    "chemn42": "chemj44",
}

# ───────────────────────────────────────────────────────────────────────────────
# 2. Generated replacement questions for each paper
# ───────────────────────────────────────────────────────────────────────────────

REPLACEMENT_QUESTIONS = {
    "chemd11": [
        ("What is hybridization? Explain the geometry of methane ($\\text{CH}_4$), ammonia ($\\text{NH}_3$), and water ($\\text{H}_2\\text{O}$) using $sp^3$ hybridization.", "I"),
        ("Define electronegativity. How does it determine the bond type (ionic, covalent, or polar covalent) in a molecule? Give examples.", "I"),
        ("What are the types of intermolecular forces? Explain how they influence the boiling point of liquids with examples.", "I"),
        ("Define oxidation number. Assign oxidation numbers to all atoms in $\\text{H}_2\\text{SO}_4$ and $\\text{K}_2\\text{Cr}_2\\text{O}_7$.", "II"),
        ("What is enthalpy? Define standard enthalpy of formation and write its expression for the formation of water.", "II"),
        ("State the second law of thermodynamics. Define entropy and explain how it relates to the spontaneity of a process.", "II"),
        ("What is Gibbs free energy? Write its mathematical expression and explain how it predicts spontaneity of a reaction.", "II"),
        ("Classify dyes based on their chemical structure and method of application. Give one example of each class.", "III"),
        ("What are synthetic polymers? Describe the preparation, properties, and uses of (a) Nylon-6,6 and (b) Bakelite.", "III"),
        ("What are food preservatives? Give examples of natural and synthetic preservatives used in the food industry.", "III"),
        ("Describe the chemistry of soaps. How does a soap molecule cleanse dirt from surfaces?", "III"),
        ("What is the difference between soaps and detergents? Why are detergents preferred in hard water?", "III"),
        ("Describe natural rubber and explain the vulcanization process. How does vulcanization improve the properties of rubber?", "III"),
        ("What are biopolymers? Give examples and explain their significance in biological systems.", "III"),
        ("Define fragrance compounds. Classify them and describe the chemistry behind how they produce scent.", "III"),
    ],
    "chemd21": [
        ("Explain the light reactions of photosynthesis. What is the role of chlorophyll in capturing light energy?", "I"),
        ("What is the Calvin cycle? Describe the three stages of the dark reaction in photosynthesis.", "I"),
        ("What is photorespiration? Explain how it occurs and why it reduces the efficiency of photosynthesis.", "I"),
        ("Compare C3 and C4 plants in terms of their photosynthetic pathways and efficiency.", "I"),
        ("What is petroleum? Explain its origin and list the major fractions obtained from petroleum distillation along with their uses.", "II"),
        ("Explain the significance of octane and cetane numbers in evaluating fuel quality for petrol and diesel engines.", "II"),
        ("What is coal? Describe its types (peat, lignite, bituminous, anthracite) and their carbon content.", "II"),
        ("What is nuclear fission? Explain the basic principle of a nuclear power reactor with a diagram.", "II"),
        ("Explain solar energy. Describe the working principle of a solar cell.", "II"),
        ("What is biogas? Describe the process of biogas generation from organic waste and its composition.", "II"),
        ("What is a fuel cell? Explain the working of a hydrogen-oxygen fuel cell with electrode reactions.", "II"),
        ("Describe the working principle of a lithium-ion battery and its advantages over conventional batteries.", "II"),
        ("Explain the role of metals in daily life. How is iron extracted from its ore in a blast furnace?", "III"),
        ("What is corrosion? Explain the electrochemical mechanism of iron rusting and methods of prevention.", "III"),
        ("Describe the extraction of copper from copper pyrites. Write the relevant chemical equations.", "III"),
    ],
    "chemd31": [
        ("Define environmental chemistry. What is the difference between pollution and contamination? Define BOD and COD.", "I"),
        ("What is the greenhouse effect? Name the major greenhouse gases and explain their role in global warming.", "II"),
        ("Explain the mechanism of ozone layer depletion. What is the role of CFCs in stratospheric ozone destruction?", "II"),
        ("What is eutrophication? How does it affect aquatic ecosystems?", "II"),
        ("Describe the composition and structure of the atmosphere. What are the different atmospheric regions?", "II"),
        ("Define the hydrological cycle. Explain how water moves between different reservoirs on Earth.", "III"),
        ("Explain the nitrogen cycle. What are the key processes and microorganisms involved?", "III"),
        ("Describe the sulfur cycle and its role in atmospheric chemistry and acid rain formation.", "III"),
        ("What is acid rain? Explain its causes and effects on ecosystems and infrastructure.", "IV"),
        ("Define air quality parameters. Explain the major sources and effects of air pollution in urban areas.", "IV"),
        ("What is photochemical smog? Explain the reactions involved in its formation.", "IV"),
        ("Describe the methods used for treating domestic wastewater. What are the stages of water treatment?", "IV"),
        ("What is the El-Niño phenomenon? How does it affect weather patterns globally?", "IV"),
        ("What is water pollution? List major pollutants and explain their effects on human health.", "IV"),
        ("Define TLV (Threshold Limit Value) and explain its significance in environmental and occupational health.", "I"),
    ],
    "chemj31": [
        ("Describe the complexes of alkali metals with crown ethers and cryptands. How do they differ in their binding selectivity?", "I"),
        ("What are the allotropes of carbon? Compare the structures and properties of diamond, graphite, and fullerene.", "I"),
        ("Explain the chemistry of hydrides of Group 15 elements ($\\text{NH}_3$, $\\text{PH}_3$, $\\text{AsH}_3$) and compare their properties.", "I"),
        ("Describe the oxo-acids of sulfur ($\\text{H}_2\\text{SO}_4$, $\\text{H}_2\\text{SO}_3$, $\\text{H}_2\\text{S}_2\\text{O}_7$) and their structures.", "I"),
        ("Compare the chemistry of nitrogen and phosphorus. Why does nitrogen show anomalous behavior compared to other Group 15 elements?", "I"),
        ("Explain the preparation and acidic properties of the oxo-acids of chlorine: $\\text{HClO}$, $\\text{HClO}_2$, $\\text{HClO}_3$, and $\\text{HClO}_4$.", "I"),
        ("What are flame colorations? Explain the chemistry behind flame tests for alkali and alkaline earth metals.", "I"),
        ("Discuss the halides of Group 13 elements. Compare the Lewis acidity of $\\text{BF}_3$, $\\text{BCl}_3$, and $\\text{BBr}_3$.", "I"),
        ("What is the inert pair effect? Explain its role in the chemistry of heavier p-block elements with examples.", "I"),
        ("Describe the structure and properties of zeolites. How are they used as molecular sieves in industry?", "II"),
        ("Explain the manufacture of Portland cement. What are the key ingredients and their roles?", "II"),
        ("Describe the Haber process for the manufacture of ammonia. What are the conditions and catalyst used?", "II"),
        ("Explain the manufacture of sulfuric acid by the Contact process. Write balanced equations for each step.", "II"),
        ("What are refractories? Classify them and explain their industrial applications.", "II"),
        ("Describe the types and uses of nitrogenous fertilizers. How is urea manufactured industrially?", "II"),
        ("What are silicates? Classify silicates based on their structural types and give one example of each.", "II"),
        ("Explain the preparation and properties of phosphate fertilizers. What is the role of superphosphate?", "II"),
        ("Describe the structure of ordinary glass. How is it manufactured and what are its types?", "II"),
        ("What is the borax bead test? Explain the chemistry involved in identifying metal ions using this test.", "I"),
        ("Discuss the chemistry of noble gases. Why are they relatively unreactive? Describe the preparation and structure of xenon fluorides.", "I"),
    ],
    "chemj34": [
        ("Explain the systematic qualitative analysis of a mixture containing two cations. Describe the group reagents for Groups I to VI.", "I"),
        ("Explain the role of $\\text{H}_2\\text{S}$ in qualitative inorganic analysis. Why is its concentration controlled in Group II analysis?", "I"),
        ("What is the common ion effect? How is it used in the precipitation of Group III cations?", "I"),
        ("Describe the confirmation tests for the following anions: (a) $\\text{SO}_4^{2-}$, (b) $\\text{Cl}^-$, (c) $\\text{NO}_3^-$.", "I"),
        ("How are Group IV cations (Ca$^{2+}$, Sr$^{2+}$, Ba$^{2+}$) separated and identified in qualitative analysis?", "I"),
        ("Describe the preliminary tests in qualitative organic analysis: (a) physical state, (b) solubility, (c) ignition test.", "II"),
        ("How are nitrogen, sulfur, and halogens detected in an organic compound? Describe the Lassaigne's test in detail.", "II"),
        ("What functional group tests are used to identify aldehydes, ketones, and carboxylic acids in an organic compound?", "II"),
        ("Describe the tests for identifying primary, secondary, and tertiary amines in organic analysis.", "II"),
        ("How is the melting point of an organic compound determined and why is it important in identification?", "II"),
        ("Define water equivalent of a calorimeter. How is it determined experimentally?", "III"),
        ("Explain the experimental determination of the enthalpy of neutralization of $\\text{HCl}$ with $\\text{NaOH}$ using a calorimeter.", "III"),
        ("What is the enthalpy of ionization? How is it determined for a weak acid like acetic acid?", "III"),
        ("Define integral enthalpy of solution. How does it differ from differential enthalpy of solution?", "III"),
        ("State Hess's law. Apply it to calculate the enthalpy of formation of $\\text{CO}_2$ from given thermochemical data.", "III"),
    ],
    "chemj42": [
        ("Explain why nitrobenzene is less reactive than benzene towards electrophilic substitution. What position does substitution occur at and why?", "I"),
        ("Describe the preparation of aniline from nitrobenzene. What is the role of tin and hydrochloric acid in the reduction?", "I"),
        ("What are diazonium salts? Describe their preparation from aniline and their synthetic applications (coupling, replacement reactions).", "I"),
        ("Compare pyridine and pyrrole in terms of basicity, aromaticity, and reactivity towards electrophilic substitution.", "II"),
        ("Explain the Skraup synthesis of quinoline. Write the mechanism in detail.", "II"),
        ("Describe the preparation and reactions of furan. Compare its reactivity with benzene.", "II"),
        ("Describe the Fischer indole synthesis with the mechanism and explain what substrates are used.", "II"),
        ("Compare the aromatic character and electrophilic substitution reactivity of furan, pyrrole, and thiophene.", "II"),
        ("Explain the Hantzsch synthesis of pyridine derivatives. Write the mechanism.", "II"),
        ("Describe the chemistry of naphthalene. Explain why electrophilic substitution occurs preferentially at the alpha position.", "III"),
        ("Explain why anthracene reacts preferentially at the 9,10-positions in electrophilic substitution reactions.", "III"),
        ("Describe the Baeyer strain theory. Apply it to explain the relative stability of cyclopropane, cyclobutane, and cyclopentane.", "V"),
        ("Explain the conformational analysis of cyclohexane. Draw the chair and boat forms and explain the concepts of axial and equatorial bonds.", "V"),
        ("Explain the anomeric effect in carbohydrates. What is its structural and chemical significance?", "VII"),
        ("Describe the Kiliani-Fischer synthesis for chain extension of aldoses. Write the reaction sequence.", "VII"),
        ("Explain the Wohl degradation for chain shortening of aldoses with the reaction mechanism.", "VII"),
        ("What is glycosylation? Describe the Fischer glycosidation reaction and its mechanism.", "VII"),
        ("Describe the structure of sucrose and explain why it is a non-reducing sugar.", "VII"),
        ("Explain the protection of NH and OH groups in organic synthesis. Give one example of each protective group used.", "VI"),
        ("What are carbonyl protecting groups? Describe the use of acetals as carbonyl protecting groups.", "VI"),
    ],
    "chemj43": [
        ("Define partial molar quantities. Derive the expression for the chemical potential of a component in an ideal gas mixture.", "I"),
        ("State the Gibbs-Duhem equation. How is it used to relate partial molar quantities of the components of a binary solution?", "I"),
        ("Define fugacity and activity. How does fugacity of a real gas differ from its pressure?", "I"),
        ("State Raoult's law and Henry's law. Under what conditions does each apply?", "I"),
        ("What are colligative properties? Derive the expression for the elevation of boiling point of a dilute solution.", "I"),
        ("Derive the expression for the osmotic pressure of a dilute solution. Explain how it is used to determine the molecular weight of macromolecules.", "I"),
        ("State the Langmuir adsorption isotherm. Derive its equation and discuss its limitations.", "II"),
        ("What is the BET equation? How is it used to determine the specific surface area of a solid?", "II"),
        ("Derive the Gibbs adsorption isotherm and explain its significance in surface chemistry.", "II"),
        ("Explain enzyme kinetics. Derive the Michaelis-Menten equation and define $K_m$ and $V_{max}$.", "II"),
        ("What is quantum yield in a photochemical reaction? Define primary and secondary photochemical processes.", "III"),
        ("Explain the kinetics of the photochemical decomposition of hydrogen iodide. Write and solve the rate expression.", "III"),
        ("What is the Stern-Volmer equation? Explain fluorescence quenching and its kinetic treatment.", "III"),
        ("Explain the concept of photostationary state with an example of a cis-trans isomerization reaction.", "III"),
        ("Define radioactive decay and state the decay law. Derive the expression for half-life in terms of decay constant.", "IV"),
        ("What is artificial radioactivity? Describe the types of nuclear reactions used to produce artificial radioisotopes.", "IV"),
        ("Explain the construction and working of the GM counter for detecting radiation.", "IV"),
        ("What is the compound nucleus theory? Describe the experimental evidence that supports it.", "IV"),
        ("Explain the radiolysis of water. What are the primary products and how do they interact with solutes?", "IV"),
        ("Describe the application of radioisotopes as tracers in chemistry and biochemistry.", "IV"),
    ],
    "chemj44": [
        ("Explain the principle of distillation. Under what circumstances is fractional distillation necessary?", "I"),
        ("Describe the process of recrystallization for purifying a solid organic compound.", "I"),
        ("Explain the principle and technique of solvent extraction. How is the distribution ratio used in multiple extractions?", "I"),
        ("Describe the technique of column chromatography. What is the role of the stationary phase and mobile phase?", "I"),
        ("Explain the basic principles of UV-Visible spectroscopy. State and explain the Beer-Lambert law.", "I"),
        ("What is infrared spectroscopy? Explain how it is used to identify functional groups in organic molecules.", "I"),
        ("Explain the basic principle of NMR spectroscopy. What is chemical shift and what does it represent?", "I"),
        ("Define primary and secondary standards in volumetric analysis. Give one example of each and explain the difference.", "II"),
        ("Explain the terms molarity, normality, and molality. Give the mathematical expressions and interconversions.", "II"),
        ("Describe the preparation of a standard solution of oxalic acid. How is it used to standardize NaOH?", "II"),
        ("What is ppm (parts per million)? How is it used in environmental chemistry and water analysis?", "II"),
        ("Explain the general concept of acid-base titration. Describe the titration of a strong acid with a strong base and draw the titration curve.", "III"),
        ("What is a complexometric titration? Explain the use of EDTA in determining the total hardness of water.", "III"),
        ("Describe a redox titration with an example. Explain the determination of iron using potassium permanganate.", "III"),
        ("What is a precipitation titration? Describe the Mohr method for determining chloride ions.", "III"),
    ],
}

# ───────────────────────────────────────────────────────────────────────────────
# 3. LaTeX parsing utilities (from populate_chemistry.py)
# ───────────────────────────────────────────────────────────────────────────────

def clean_text(text):
    text = text.replace(r'\"{o}', 'ö')
    text = text.replace(r'\'e', 'é')
    text = text.replace(r'\"{a}', 'ä')
    text = text.replace(r'\"o', 'ö')
    text = re.sub(r'\\pts\{[^\}]*\}', '', text)
    text = re.sub(r'\\hfill', '', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
    text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
    text = text.replace('~', ' ')
    text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
    text = text.replace(r'\[', '$')
    text = text.replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_tex_content(subcontent):
    doc_start = subcontent.find(r'\begin{document}')
    if doc_start != -1:
        subcontent = subcontent[doc_start + len(r'\begin{document}'):]
    pattern = r'(\\begin\{parts\}|\\end\{parts\}|\\item)'
    tokens = re.split(pattern, subcontent)
    stack = []
    current_items = []
    all_questions = []
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
                    last_parent = parent_items[-1]
                    sub_text = " " + " ".join(f"({idx+1}) {clean_text(item)}" for idx, item in enumerate(current_items))
                    parent_items[-1] = last_parent + sub_text
                    current_items = parent_items
                else:
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
    for item in current_items:
        cleaned = clean_text(item)
        if len(cleaned) > 15:
            all_questions.append(cleaned)
    return all_questions

# ───────────────────────────────────────────────────────────────────────────────
# 4. Build PYQ database from tex files
# ───────────────────────────────────────────────────────────────────────────────

def build_pyq_database():
    """Returns dict mapping exam_key -> list of cleaned question strings from .tex PYQ files"""
    tex_dir = 'aaa/chemistry/tex_files'
    pyq_db = {
        "chemd11": [], "chemd21": [], "chemd31": [],
        "chemj11": [], "chemj21": [], "chemj31": [], "chemj32": [],
        "chemj33": [], "chemj34": [], "chemj41": [], "chemj42": [],
        "chemj43": [], "chemj44": [],
    }
    files = [f for f in os.listdir(tex_dir) if f.endswith('.tex') and not f.startswith('test_')]
    files.sort()
    for file_name in files:
        filepath = os.path.join(tex_dir, file_name)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(r'\end{{parts}}', r'\end{parts}')
        content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
        content = re.sub(r'(?m)^%.*$', '', content)
        code = file_name.split("_")[0]
        if code.startswith("CHB-02A"):
            pyq_db["chemd11"].extend(parse_tex_content(content))
        elif code.startswith("CHB-04A"):
            pyq_db["chemd21"].extend(parse_tex_content(content))
        elif code.startswith("CHB-101"):
            pyq_db["chemj11"].extend(parse_tex_content(content))
        elif code.startswith("CHB-201"):
            pyq_db["chemj21"].extend(parse_tex_content(content))
        elif code.startswith("CHB-301") or code.startswith("CHB-361"):
            parts = re.split(r'SECTION\s+B', content, flags=re.IGNORECASE)
            left = parts[0]
            right = parts[1] if len(parts) > 1 else ""
            pyq_db["chemj32"].extend(parse_tex_content(left))
            pyq_db["chemj33"].extend(parse_tex_content(right))
        elif code.startswith("CHB-401"):
            parts = re.split(r'SECTION\s+B', content, flags=re.IGNORECASE)
            left = parts[0]
            right = parts[1] if len(parts) > 1 else ""
            pyq_db["chemj41"].extend(parse_tex_content(left))
            pyq_db["chemj42"].extend(parse_tex_content(right))
        elif code.startswith("CHB-501"):
            pyq_db["chemj44"].extend(parse_tex_content(content))  # Techniques -> mapped to j44
        elif code.startswith("CHB-505"):
            pyq_db["chemd31"].extend(parse_tex_content(content))
    return pyq_db

# ───────────────────────────────────────────────────────────────────────────────
# 5. Topic relevance check
# ───────────────────────────────────────────────────────────────────────────────

PLACEHOLDER_MARKER = "Discuss the theoretical foundations, spectroscopic characterizations"

def is_placeholder(q_text):
    return PLACEHOLDER_MARKER in q_text

def is_on_syllabus(q_text, paper_key):
    """Simple keyword-based check if a question is on-syllabus for this paper."""
    q_lower = q_text.lower()
    topics = PAPER_TOPICS.get(paper_key, {})
    all_keywords = []
    for unit_keywords in topics.get("units", {}).values():
        all_keywords.extend(unit_keywords)
    if not all_keywords:
        return True  # No topic data → assume on-syllabus
    # A question is on-syllabus if at least one keyword matches
    return any(kw in q_lower for kw in all_keywords)

def assign_unit(q_text, paper_key):
    """Assign the best unit label for a question based on keyword matching."""
    q_lower = q_text.lower()
    topics = PAPER_TOPICS.get(paper_key, {})
    best_unit = "I"
    best_count = 0
    for unit_label, keywords in topics.get("units", {}).items():
        count = sum(1 for kw in keywords if kw in q_lower)
        if count > best_count:
            best_count = count
            best_unit = unit_label
    return best_unit

# Standard answer key for all questions
STANDARD_ANS_KEY = ("1. **Core Chemical Principles**:\n"
    "- Analyze the molecular structures, electronic configurations, and thermodynamic parameters of the system.\n\n"
    "2. **Reaction Mechanism & Equations**:\n"
    "- Write down chemical equations, show arrow-pushing mechanisms, and identify key intermediates "
    "(such as carbocations, radicals, or coordinate complexes).\n\n"
    "3. **Verification**:\n"
    "- Ensure charge balance, stoichiometric coefficients, and stereochemical details are correct, "
    "and cross-reference with standard thermodynamic and kinetic laws.")

# ───────────────────────────────────────────────────────────────────────────────
# 6. Main audit and fix routine
# ───────────────────────────────────────────────────────────────────────────────

def build_question_obj(idx, q_text, unit):
    return {
        "id": idx + 1,
        "unit": unit,
        "question": q_text.strip(),
        "answerKey": STANDARD_ANS_KEY,
    }

def fix_exam(exam_key, exam_data, pyq_db):
    """Rebuild 50 questions for a given exam, replacing placeholders and OOS questions."""
    paper_key = PAPER_MIRRORS.get(exam_key, exam_key)
    existing_qs = exam_data.get("questions", [])

    # Step 1: Keep valid (on-syllabus, non-placeholder) existing questions
    good_qs = []
    seen_norms = set()
    for q_obj in existing_qs:
        q_text = q_obj.get("question", "")
        if not q_text or is_placeholder(q_text):
            continue
        if not is_on_syllabus(q_text, paper_key):
            print(f"  [OOS] Removing: {q_text[:80]}")
            continue
        norm = q_text.lower().strip()
        if norm in seen_norms:
            continue
        seen_norms.add(norm)
        # Re-assign unit based on content
        unit = assign_unit(q_text, paper_key)
        good_qs.append(build_question_obj(len(good_qs), q_text, unit))

    print(f"  [{exam_key}] Kept {len(good_qs)} valid questions from existing set.")

    # Step 2: Add PYQ questions that are on-syllabus
    raw_pyqs = pyq_db.get(paper_key, [])
    for q_text in raw_pyqs:
        if len(good_qs) >= 50:
            break
        if not q_text or len(q_text) < 20:
            continue
        norm = q_text.lower().strip()
        if norm in seen_norms:
            continue
        if not is_on_syllabus(q_text, paper_key):
            continue
        seen_norms.add(norm)
        unit = assign_unit(q_text, paper_key)
        good_qs.append(build_question_obj(len(good_qs), q_text, unit))

    print(f"  [{exam_key}] After PYQ injection: {len(good_qs)} questions.")

    # Step 3: Fill remaining slots with generated replacement questions
    replacements = REPLACEMENT_QUESTIONS.get(paper_key, [])
    for q_text, unit in replacements:
        if len(good_qs) >= 50:
            break
        norm = q_text.lower().strip()
        if norm in seen_norms:
            continue
        seen_norms.add(norm)
        good_qs.append(build_question_obj(len(good_qs), q_text, unit))

    print(f"  [{exam_key}] After replacements: {len(good_qs)} questions.")

    # Step 4: Final fallback — generate topic-based questions from syllabus units
    if len(good_qs) < 50:
        topics = PAPER_TOPICS.get(paper_key, {})
        units = topics.get("units", {})
        unit_list = list(units.items())
        fallback_idx = 0
        while len(good_qs) < 50:
            if not unit_list:
                q_text = f"Discuss the theoretical principles and applications of {topics.get('title', paper_key.upper())} - topic {fallback_idx + 1}."
                unit = "I"
            else:
                u_label, u_keywords = unit_list[fallback_idx % len(unit_list)]
                topic = u_keywords[fallback_idx % len(u_keywords)] if u_keywords else "chemistry"
                q_text = f"Explain the concept of {topic} as covered in {topics.get('title', paper_key.upper())}."
                unit = u_label
            norm = q_text.lower().strip()
            if norm not in seen_norms:
                seen_norms.add(norm)
                good_qs.append(build_question_obj(len(good_qs), q_text, unit))
            fallback_idx += 1

    # Renumber IDs
    final_qs = []
    for i, q_obj in enumerate(good_qs[:50]):
        q_obj["id"] = i + 1
        final_qs.append(q_obj)

    return final_qs

# ───────────────────────────────────────────────────────────────────────────────
# 7. Execute
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Building PYQ database from tex files ===")
    pyq_db = build_pyq_database()
    for key, qs in pyq_db.items():
        print(f"  PYQ: {key} -> {len(qs)} raw questions")

    print("\n=== Loading exams-data.js ===")
    with open("js/exams-data.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])

    # Papers to audit: only those defined in the syllabus JSON (Sems 1-4)
    SYLLABUS_PAPERS = set(PAPER_TOPICS.keys()) | set(PAPER_MIRRORS.keys())
    
    print(f"\n=== Auditing {len(SYLLABUS_PAPERS)} Chemistry papers ===")
    
    updated_count = 0
    for exam_key in sorted(SYLLABUS_PAPERS):
        if exam_key not in EXAMS:
            print(f"  WARNING: {exam_key} not found in EXAMS database, skipping.")
            continue
        exam_data = EXAMS[exam_key]
        if exam_data.get("comingSoon") != False:
            print(f"  Skipping (comingSoon): {exam_key}")
            continue
        
        print(f"\nProcessing: {exam_key} ({exam_data.get('title')})")
        new_qs = fix_exam(exam_key, exam_data, pyq_db)
        EXAMS[exam_key]["questions"] = new_qs
        updated_count += 1

    print(f"\n=== Writing updated exams-data.js ({updated_count} papers updated) ===")
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2, ensure_ascii=False)};\n"
    with open("js/exams-data.js", "w", encoding="utf-8") as f:
        f.write(output_str)

    print("Done! js/exams-data.js has been updated.")
