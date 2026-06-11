import json
import re
import os

# 1. Define Geology Syllabi and standard questions for padding to 50
GEOLOGY_SYLLABI = {
    "glbmj11": {
        "title": "Elementary Physical and Structural Geology",
        "standard_questions": [
            ("Discuss the physical and chemical weathering processes and their role in soil formation.", "I"),
            ("Explain the formation of river terraces, meanders, and oxbow lakes with neat sketches.", "I"),
            ("Describe the continental drift theory of Alfred Wegener and list the geological evidences supporting it.", "I"),
            ("Explain the interior of the Earth based on seismological data, describing the crust, mantle, and core.", "II"),
            ("Define plate tectonics. Describe the features associated with divergent and convergent boundaries.", "II"),
            ("Differentiate between a fold and a fault. Explain the parts of a fold with a diagram.", "III"),
            ("Classify faults based on the relative movement of the blocks.", "III"),
            ("Explain the geological work of wind in desert areas, highlighting deflation hollows and sand dunes.", "IV"),
            ("Describe the types and geomorphic significance of glaciers.", "IV"),
            ("What is an unconformity? Explain the differences between angular unconformity and disconformity.", "V"),
            ("Discuss the concept of plate movement driving force (mantle convection).", "II"),
            ("Describe the features of a volcanic eruption and classify volcanic landforms.", "I"),
            ("Explain the geological work of oceans, describing wave-cut platforms and spits.", "IV"),
            ("Discuss the causes, types, and mitigation of landslides.", "V"),
            ("Define joints in rocks. Explain the difference between tectonic and cooling joints.", "III")
        ]
    },
    "glbmj21": {
        "title": "Elements of Mineralogy and Crystallography",
        "standard_questions": [
            ("Define a mineral. Discuss the physical properties used for mineral identification, focusing on cleavage, hardness, and luster.", "I"),
            ("Discuss the crystal chemistry and classification of silicates, explaining the structure of orthosilicates and sheet silicates.", "I"),
            ("Explain the physical, chemical, and optical properties of the Quartz group of minerals.", "II"),
            ("Describe the chemical composition, physical properties, and geological occurrences of the Feldspar group.", "II"),
            ("Differentiate between isomorphism and polymorphism with appropriate mineralogical examples.", "I"),
            ("Explain the 32 classes of crystal symmetry and how they are grouped into the six crystal systems.", "III"),
            ("Define Miller indices. Explain how axial ratios and parameters are determined for crystal faces.", "III"),
            ("Discuss the symmetry elements and forms of the Normal Class of the Isometric System.", "IV"),
            ("Describe the optical properties of uniaxial minerals under a petrological microscope.", "V"),
            ("Explain the difference between isotropic and anisotropic minerals under crossed polars.", "V"),
            ("Describe the structures and compositions of Pyroxene and Amphibole groups.", "II"),
            ("Explain the concept of solid solution in plagioclase feldspars.", "II"),
            ("Describe the symmetry elements of the Tetragonal System (Normal Class).", "IV"),
            ("Explain twinning in crystals, detailing the contact and penetration twins.", "III"),
            ("Discuss the optical indicatrix of biaxial minerals.", "V")
        ]
    },
    "glbmj31": {
        "title": "Petrology and Economic Geology",
        "standard_questions": [
            ("Define magma. Explain Bowen's Reaction Series and its significance in igneous petrogenesis.", "I"),
            ("Discuss the processes of magmatic differentiation and crustal assimilation.", "I"),
            ("Classify igneous rocks based on mineralogical composition, texture, and mode of occurrence.", "I"),
            ("What is clastic texture? Discuss the texture and structures of sedimentary rocks.", "II"),
            ("Explain the formation of sedimentary rocks, detailing diagenesis, compaction, and cementation.", "II"),
            ("Classify sedimentary rocks, explaining the characteristics of Sandstone, Shale, and Limestone.", "II"),
            ("Define metamorphism. Discuss the agents (temperature, pressure, chemically active fluids) of metamorphism.", "III"),
            ("Differentiate between thermal, dynamic, and regional metamorphism.", "III"),
            ("Describe the textures of metamorphic rocks, focusing on schistose and gneissose structures.", "III"),
            ("Explain the concept of metamorphic facies and describe the Greenschist facies.", "III"),
            ("Classify ore deposits, detailing the processes of magmatic concentration.", "IV"),
            ("Explain the hydrothermal process of ore formation, describing cavity filling and replacement deposits.", "IV"),
            ("Discuss the origin, composition, and distribution of coal deposits in India.", "V"),
            ("Describe the geological conditions necessary for the accumulation of petroleum, focusing on source, reservoir, and trap rocks.", "V"),
            ("Write notes on the mode of occurrence, uses, and Indian distribution of Iron and Manganese ores.", "IV")
        ]
    },
    "glbmj41": {
        "title": "Palaeontology and Stratigraphy",
        "standard_questions": [
            ("Discuss the conditions necessary for fossilization and describe the modes of fossil preservation.", "I"),
            ("Describe the morphological features and geological distribution of Trilobites.", "I"),
            ("Explain the morphological features and classification of Graptolites.", "I"),
            ("Discuss the morphology and evolutionary trends in Brachiopods.", "II"),
            ("Describe the morphological characters of Gastropods and differentiate them from Cephalopods.", "II"),
            ("Explain the morphology and geological significance of Echinoids.", "II"),
            ("Discuss the Gondwana flora of India and its palaeoclimatic significance.", "III"),
            ("Define correlation. Differentiate between lithostratigraphic and biostratigraphic correlation.", "IV"),
            ("Describe the Geological Time Scale, detailing the major eras, periods, and epochs.", "IV"),
            ("Explain the principles and laws of Stratigraphy (Superposition, Original Horizontality, Lateral Continuity).", "IV"),
            ("Describe the stratigraphy and fossil content of the Gondwana Supergroup.", "V"),
            ("Discuss the stratigraphy, age, and economic importance of the Vindhyan Supergroup.", "V"),
            ("Describe the Triassic succession of Spiti (Lilang Group).", "V"),
            ("Explain the Jurassic succession of Kutch.", "V"),
            ("Discuss the Cretaceous of Trichinopoly and its biostratigraphy.", "V")
        ]
    },
    "glbmj51": {
        "title": "Physical and Structural Geology",
        "standard_questions": [
            ("Discuss the mechanical behavior of rocks under stress, explaining elastic, plastic, and brittle deformation.", "I"),
            ("Describe stress and strain ellipsoids and their relationship to rock structures.", "I"),
            ("Explain the genetic classification of folds and outline the mechanics of folding.", "II"),
            ("Describe the geometric classification of folds, highlighting cylindrical and non-cylindrical types.", "II"),
            ("Discuss the mechanics of faulting and explain Anderson's theory of faulting.", "III"),
            ("Describe shear zones, mylonites, and their tectonic significance in shear deformation.", "III"),
            ("Define joints. Discuss their geometric and genetic classifications in igneous and sedimentary rocks.", "III"),
            ("Explain the criteria used for the recognition of faults in the field.", "IV"),
            ("Discuss the concept of unconformity and its tectonic significance in geological history.", "IV"),
            ("Describe structural controls on ore localization and groundwater accumulation.", "V"),
            ("Discuss stereographic projection in structural geology and its application to solving dip and strike problems.", "V"),
            ("Differentiate between cleavage, schistosity, and foliation.", "III"),
            ("Discuss tectonic styles in fold-and-thrust belts.", "II"),
            ("Explain the structures formed by gravity-driven tectonics.", "V"),
            ("Describe the physical geology of rift valleys and passive margins.", "I")
        ]
    },
    "glbmj52": {
        "title": "Igneous Petrology, Mineralogy and Crystallography",
        "standard_questions": [
            ("Explain phase rule and discuss the crystallization of a two-component eutectic system (e.g., Diopside-Anorthite).", "I"),
            ("Describe the crystallization of a binary system showing solid solution with a minimum (e.g., Albite-Anorthite).", "I"),
            ("Explain crystallization behavior in ternary systems, focusing on Diopside-Anorthite-Albite.", "I"),
            ("Discuss the classification of igneous rocks proposed by IUGS.", "II"),
            ("Describe petrographic characteristics and origin of granites and basalts.", "II"),
            ("Explain the origin and tectonic settings of ophiolite suites.", "II"),
            ("Describe the structural chemistry and optical properties of Pyroxene group minerals.", "III"),
            ("Describe chemical composition, classification, and structures of Amphibole group minerals.", "III"),
            ("Discuss composition, structure, and occurrences of the Feldspathoid group.", "III"),
            ("Explain the 14 Bravais lattices and the derivation of the 32 point groups.", "IV"),
            ("Discuss the optical properties of biaxial crystals, explaining optic axial angle (2V) and optic sign.", "V"),
            ("Describe the use of the Michel-Lévy chart to determine plagioclase composition.", "V"),
            ("Discuss crystallization of magma in layered mafic intrusions (e.g., Bushveld Complex).", "I"),
            ("Explain optical properties of accessory minerals like zircon, tourmaline, and sphene.", "V"),
            ("Describe the symmetry and forms of the Hexagonal system.", "IV")
        ]
    },
    "glbmj53": {
        "title": "Sedimentary and Metamorphic Petrology",
        "standard_questions": [
            ("Discuss fluid dynamics of sediment transport, explaining Hjulström's diagram and flow regimes.", "I"),
            ("Describe textures of sedimentary rocks, focusing on grain size parameters, sorting, and roundness.", "I"),
            ("Explain sedimentary structures, describing cross-bedding, ripple marks, and graded bedding.", "I"),
            ("Classify sandstones based on mineralogical maturity (Pettijohn classification).", "II"),
            ("Describe the depositional environments of carbonate rocks and the Dunham classification of limestones.", "II"),
            ("Discuss diagenetic processes, detailing compaction, cementation, and authigenesis.", "II"),
            ("Discuss the concept of metamorphic zones, index minerals, and isograds (Barrow-Tilley concept).", "III"),
            ("Explain ACF and AKF diagram representation of metamorphic mineral assemblages.", "III"),
            ("Describe mineralogical changes during progressive metamorphism of pelitic rocks.", "IV"),
            ("Discuss regional metamorphism of basic igneous rocks, describing the greenstone to granulite transition.", "IV"),
            ("Explain paired metamorphic belts and their plate tectonic significance.", "V"),
            ("Describe the textures of contact metamorphism, highlighting hornfelsic and granoblastic textures.", "III"),
            ("Discuss the role of fluids in metamorphism and metasomatism.", "V"),
            ("Explain the origin of sedimentary chert and evaporite deposits.", "II"),
            ("Describe thermal metamorphism of impure limestones and dolomites.", "IV")
        ]
    },
    "glbmj61": {
        "title": "Palaeontology",
        "standard_questions": [
            ("Discuss the origin of life and Precambrian micropalaeontology.", "I"),
            ("Describe the morphological features and evolutionary history of Ammonoids.", "I"),
            ("Explain evolutionary trends in Trilobites through the Palaeozoic.", "I"),
            ("Discuss the evolutionary history of Equidae (horses) with major morphological adaptations.", "II"),
            ("Describe the morphology, classification, and evolutionary trends in Graptoloidea.", "II"),
            ("Explain the microfossil groups: Foraminifera, Ostracoda, and Conodonts and their biostratigraphic applications.", "III"),
            ("Discuss the application of micropalaeontology in petroleum exploration.", "III"),
            ("Describe the morphological characters, classification, and ecology of Gastropoda.", "IV"),
            ("Discuss the classification, shell structure, and morphological features of Bivalvia (Lamellibranchs).", "IV"),
            ("Describe the plant fossils of Lower Gondwana (Glossopteris flora) and Upper Gondwana (Ptilophyllum flora).", "V"),
            ("Explain the significance of trace fossils in palaeoenvironmental reconstruction.", "V"),
            ("Discuss evolutionary trends in Hominids (human evolution).", "II"),
            ("Describe the functional morphology of Brachiopods and their ecological niches.", "IV"),
            ("Explain the Gondwana fauna and its correlation across Southern Hemisphere landmasses.", "V"),
            ("Describe the methods of extraction and study of microfossils.", "III")
        ]
    },
    "glbmj62": {
        "title": "Stratigraphy",
        "standard_questions": [
            ("Discuss the principles of sequence stratigraphy, detailing base-level changes, system tracts, and key bounding surfaces.", "I"),
            ("Describe the chronostratigraphic, lithostratigraphic, and biostratigraphic classification units.", "I"),
            ("Discuss Precambrian stratigraphy of Dharwar craton, describing its greenstone belts and economic deposits.", "II"),
            ("Describe the geology, correlation, and age of the Cuddapah Supergroup.", "II"),
            ("Explain the Vindhyan Supergroup, detailing its subdivisions, age, and fossil content.", "II"),
            ("Describe the stratigraphy and age of the Palaeozoic of Spiti valley.", "III"),
            ("Discuss the Gondwana Supergroup, describing its divisions, climatic changes, and distribution in India.", "III"),
            ("Describe the Jurassic of Kutch, detailing its stratigraphic succession and cephalopod fauna.", "IV"),
            ("Discuss the Cretaceous succession of Trichinopoly, describing its subdivisions and fossil assemblages.", "IV"),
            ("Describe the Siwalik Group, detailing its lithology, vertebrate fauna, and Siwalik boundary problems.", "V"),
            ("Discuss the Deccan Volcanics, describing their distribution, age, and intertrappean beds.", "V"),
            ("Explain the stratigraphic and tectonic history of the Himalaya.", "I"),
            ("Describe the geology and stratigraphic position of the Singhbhum Craton.", "II"),
            ("Discuss the boundary problems: Permian-Triassic (P-T) and Cretaceous-Palaeogene (K-Pg) boundary in India.", "V"),
            ("Describe the Quaternary stratigraphy and climate of India.", "V")
        ]
    },
    "glbmj63": {
        "title": "Hydrogeology, Environmental Geology and Exploration",
        "standard_questions": [
            ("Discuss the vertical distribution of groundwater and define the water table and capillary fringe.", "I"),
            ("State and explain Darcy's Law. Discuss its validity and limitations in groundwater flow.", "I"),
            ("Differentiate between porosity, permeability, specific yield, and specific retention.", "I"),
            ("Explain aquifer parameters: transmissivity ($T$) and storage coefficient ($S$).", "II"),
            ("Describe the types of aquifers: unconfined, confined, semi-confined, and perched.", "II"),
            ("Discuss groundwater exploration methods, focusing on electrical resistivity (VES) surveys.", "III"),
            ("Describe seismic refraction exploration methods and their application in geological mapping.", "III"),
            ("Discuss the geological and environmental impact of large dam construction.", "IV"),
            ("Explain groundwater pollution, focusing on arsenic and fluoride contamination in India.", "IV"),
            ("Discuss natural disasters, detailing landslides, mitigation strategies, and early warning systems.", "V"),
            ("Describe remote sensing and GIS applications in environmental management and groundwater mapping.", "V"),
            ("Discuss the hydrological cycle and explain groundwater balance equations.", "I"),
            ("Describe gravity and magnetic methods of geophysical exploration.", "III"),
            ("Discuss coastal erosion, sea-level changes, and their environmental management.", "V"),
            ("Explain water quality standards for drinking and agricultural uses (WHO, BIS).", "IV")
        ]
    },
    "glbmj64": {
        "title": "Economic Geology",
        "standard_questions": [
            ("Define ore, gangue, tenor, and mineral resource. Classify ore deposits.", "I"),
            ("Explain the process of magmatic concentration, detailing early and late magmatic deposits.", "I"),
            ("Discuss pegmatitic deposits and describe the pegmatites of Bihar and Rajasthan.", "I"),
            ("Describe hydrothermal ore-forming processes, detailing cavity filling and metasomatic replacement.", "II"),
            ("Explain contact metasomatic deposits and the minerals associated with them.", "II"),
            ("Discuss sedimentation processes in ore deposit formation, detailing iron and manganese formations.", "III"),
            ("Explain supergene sulphide enrichment, detailing the zones of gossan, oxidation, and supergene enrichment.", "III"),
            ("Describe placer deposits, explaining the origin of alluvial, beach, and eluvial placers.", "IV"),
            ("Discuss the origin, occurrence, and Indian distribution of Gold deposits.", "IV"),
            ("Describe the geology, mineralogy, and distribution of Copper deposits in India (Singhbum/Khetri).", "IV"),
            ("Discuss the Lead-Zinc deposits of Zawar, Rajasthan.", "V"),
            ("Describe the geological occurrence, origin, and distribution of Bauxite deposits in India.", "V"),
            ("Discuss the origin, composition, and coal reserves of Gondwana and Tertiary coalfields in India.", "V"),
            ("Describe the geological occurrences and source-reservoir-trap systems of major oil fields in India.", "V"),
            ("Discuss the national mineral policy and conservation of mineral resources in India.", "I")
        ]
    }
}

UNIQUE_TO_ACTIVE = {
    "glbmj11": ["glbmj11", "glbmn11", "glbmd11"],
    "glbmj21": ["glbmj21", "glbmn21"],
    "glbmj31": ["glbmj31"],
    "glbmj41": ["glbmj41"],
    "glbmj51": ["glbmj51"],
    "glbmj52": ["glbmj52"],
    "glbmj53": ["glbmj53"],
    "glbmj61": ["glbmj61"],
    "glbmj62": ["glbmj62"],
    "glbmj63": ["glbmj63"],
    "glbmj64": ["glbmj64"]
}

# Mapping of file names to unique keys
def get_glb_mapping(filename):
    fn = filename.upper()
    if "PHYSICALSTRUCTURALGEOLOGY" in fn or "ELEMENTARYPHYSICALSTRUCTURALGEOLOGY" in fn:
        if "SEMI_" in fn: return "glbmj11"
        if "SEMV_" in fn: return "glbmj51"
    if "MINERALOGYCRYSTALLOGRAPHY" in fn or "ELEMENTSOFMINERALOGYCRYSTALLOGRAPHY" in fn or "ELEMENTSOFGEOLOGYI" in fn:
        if "SEMII_" in fn: return "glbmj21"
        if "SEMV_" in fn: return "glbmj52"
    if "PETROLOGYECONOMICGEOLOGY" in fn: return "glbmj31"
    if "PALAEONTOLOGYSTRATIGRAPHY" in fn or "ELEMENTSOFGEOLOGYII" in fn: return "glbmj41"
    if "SEDIMENTARYMETAMORPHICPETROLOGY" in fn: return "glbmj53"
    if "ELEMENTSOFEARTHSCIENCE" in fn:
        if "SEMII_" in fn: return "glbmj21"
        if "SEMV_" in fn: return "glbmj53"
    if "PALAEONTOLOGY" in fn: return "glbmj61"
    if "STRATIGRAPHY" in fn:
        if "SEMIV_" in fn: return "glbmj41"
        if "SEMVI_" in fn: return "glbmj62"
    if "HYDROGEOLOGY" in fn: return "glbmj63"
    if "ECONOMICGEOLOGY" in fn: return "glbmj64"
    return None

# Clean LaTeX text formatting
def clean_text(text):
    text = re.sub(r'\\pts\{[^\}]*\}', '', text)
    text = re.sub(r'\\hfill', '', text)
    text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
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

# Extract questions from LaTeX
def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comment lines
    content = re.sub(r'(?m)^%.*$', '', content)
    
    parts_questions = []
    
    # Extract questions inside parts environment
    parts_matches = re.finditer(r'\\begin\{(parts|romanparts)\}(.*?)\\end\{\1\}', content, re.DOTALL)
    for match in parts_matches:
        parts_content = match.group(2)
        items = re.split(r'\\item', parts_content)
        for item in items[1:]:
            cleaned = clean_text(item)
            if len(cleaned) > 10:
                parts_questions.append(cleaned)
                
    # Extract Questions
    main_questions = []
    matches = re.findall(r'\\textbf\{\s*Question\s*([0-9]+)\.\}\s*(.*?)(?=\\pts|\\hfill|\\medskip|\\noindent|\\vfill|\\begin\{center\}|\Z)', content, re.DOTALL)
    for q_num, q_text in matches:
        cleaned = clean_text(q_text)
        if len(cleaned) > 10 and "comment on" not in cleaned.lower() and "short notes on" not in cleaned.lower() and "attempt any" not in cleaned.lower():
            main_questions.append(cleaned)
            
    return parts_questions + main_questions

# Generate styled answer key
def get_custom_answer_key(subject_key, q_text):
    q_lower = q_text.lower()
    
    # Weathering & Erosion
    if "weathering" in q_lower:
        return (
            "1. **Mechanical (Physical) Weathering**:\n"
            "- Disintegration of rocks without chemical changes. Examples include:\n"
            "  - **Frost wedging**: Water freezing in cracks expansion pushes rock apart.\n"
            "  - **Thermal expansion**: Outer layers expand and contract due to temperature changes, leading to exfoliation.\n"
            "  - **Exfoliation (Unloading)**: Pressure release when overlying rocks are eroded, causing sheets of rock to peel away.\n"
            "2. **Chemical Weathering**:\n"
            "- Chemical alteration of minerals. Key processes include:\n"
            "  - **Hydration & Hydrolysis**: Chemical reaction with water converting minerals to clay.\n"
            "  - **Carbonation**: Carbonic acid in rain dissolving carbonate minerals (limestone).\n"
            "  - **Oxidation**: Oxygen reacting with iron-bearing minerals creating iron rust ($Fe_2O_3$).\n"
            "3. **Biological Weathering**:\n"
            "- Action of plant roots, burrowing animals, and lichens that secrete organic acids.\n"
            "4. **Soil Role**: Weathering provides the raw loose regolith parent material essential for soil horizon development."
        )
    elif "river" in q_lower or "terrace" in q_lower or "meander" in q_lower:
        return (
            "1. **River Terraces**:\n"
            "- Bench-like steps bordering a valley floor. Formed when a river rejuvenates and cuts vertically into its own floodplain.\n"
            "2. **Meanders**:\n"
            "- S-shaped loops along a river course. Formed in low gradients where lateral erosion occurs on the outer bank (*cut bank*) and deposition occurs on the inner bank (*point bar*).\n"
            "3. **Oxbow Lakes**:\n"
            "- Crescent-shaped water bodies. Formed when lateral erosion cuts through the narrow neck of a meander loop, bypassing the loop which gets sealed off by silt deposition.\n"
            "4. **Sketches**: Depicting cut-offs, deposition zones, and step-like terraces in cross-section."
        )
    elif "drift" in q_lower or "wegener" in q_lower:
        return (
            "1. **Continental Drift Theory (Alfred Wegener, 1912)**:\n"
            "- States that all continents were once assembled in a single supercontinent named **Pangaea**, surrounded by a giant ocean called **Panthalassa**.\n"
            "- During the Mesozoic era, Pangaea fragmented, and pieces drifted away to form modern continents.\n"
            "2. **Evidence**:\n"
            "- **Jigsaw Fit**: Match of continental margins (e.g., South America and Africa).\n"
            "- **Fossil Correlation**: Identical fossils like *Glossopteris* (plant) and *Mesosaurus* (freshwater reptile) across disconnected oceans.\n"
            "- **Rock Sequences**: Continuous mountain belts and identical geological strata across South America, Africa, and India.\n"
            "- **Palaeoclimatic data**: Permian glacial tillite deposits found in tropical regions like India, Africa, and Australia."
        )
    elif "interior" in q_lower or "seismological" in q_lower or "crust" in q_lower:
        return (
            "1. **Crust**:\n"
            "- Outermost layer. Continental crust is thick (30-70 km), granitic, and light (*Sial*). Oceanic crust is thin (5-10 km), basaltic, and dense (*Sima*). Bounded at base by the **Mohorovičić Discontinuity**.\n"
            "2. **Mantle**:\n"
            "- Extends to 2900 km. Primarily composed of silicate rocks rich in iron and magnesium (peridotite).\n"
            "  - **Asthenosphere**: Upper plastic layer (100-250 km) where magma generates and lithospheric plates float.\n"
            "- Bounded at base by the **Gutenberg Discontinuity**.\n"
            "3. **Core**:\n"
            "- Dense metallic center (Nickel-Iron, *Nife*).\n"
            "  - **Outer Core**: Liquid metal (inferred because S-waves cannot pass through it), generating Earth's magnetic field.\n"
            "  - **Inner Core**: Solid metal due to extreme lithostatic pressure."
        )
    elif "plate tectonics" in q_lower or "boundary" in q_lower or "boundaries" in q_lower:
        return (
            "1. **Plate Tectonics Theory**:\n"
            "- Proposes that Earth's outer lithosphere is divided into several major and minor rigid plates floating on the asthenosphere.\n"
            "2. **Divergent (Constructive) Boundaries**:\n"
            "- Plates pull apart. Magma rises to fill the gap, cooling to form new crust. Features include mid-ocean ridges (e.g., Mid-Atlantic Ridge) and continental rift valleys (e.g., East African Rift).\n"
            "3. **Convergent (Destructive) Boundaries**:\n"
            "- Plates collide. Subduction occurs if one is oceanic, forming deep trenches and volcanic arcs. Continental collisions fold sediment into mountain ranges (e.g., Himalayas).\n"
            "4. **Transform (Conservative) Boundaries**:\n"
            "- Plates slide horizontally past each other. Crust is neither created nor destroyed. Causes shallow earthquakes (e.g., San Andreas Fault)."
        )
    elif "fold" in q_lower or "anticline" in q_lower:
        return (
            "1. **Definition**:\n"
            "- Folds are wave-like bends in rock strata caused by compressive tectonic stress.\n"
            "2. **Parts of a Fold**:\n"
            "- **Hinge**: The line of maximum curvature on a folded surface.\n"
            "- **Limbs**: The sides/flanks of the fold on either side of the hinge.\n"
            "- **Axial Plane**: An imaginary bisecting plane dividing the fold symmetrically.\n"
            "- **Crest & Trough**: Highest and lowest points of the fold.\n"
            "3. **Classification**:\n"
            "- **Anticline**: Up-arched fold with oldest beds in the core.\n"
            "- **Syncline**: Down-warped fold with youngest beds in the core.\n"
            "- **Symmetrical / Asymmetrical**: limbs dipping at equal or unequal angles.\n"
            "- **Overturned**: One limb tilted past vertical.\n"
            "- **Recumbent**: Axial plane is horizontal."
        )
    elif "fault" in q_lower or "faulting" in q_lower:
        return (
            "1. **Definition**:\n"
            "- Fractures in rock strata along which relative displacement has occurred.\n"
            "2. **Anderson's Classification of Faults**:\n"
            "- **Normal Faults**: Caused by tensional stress. Hanging wall moves down relative to footwall.\n"
            "- **Reverse/Thrust Faults**: Caused by compressional stress. Hanging wall moves up relative to footwall. Thrust faults dip $<45^\\circ$.\n"
            "- **Strike-Slip Faults**: Caused by shear stress. Lateral movement parallel to fault strike (sinistral or dextral).\n"
            "3. **Field Recognition**: Offset layers, fault breccia, fault gouge, slickensides (grooves showing movement direction), and fault scarps."
        )
    
    # Mineralogy & Crystallography
    elif "mineral" in q_lower or "cleavage" in q_lower:
        return (
            "1. **Mineral Definition**:\n"
            "- Naturally occurring, inorganic, homogeneous solid, with a definite chemical composition and an ordered internal atomic structure.\n"
            "2. **Physical Properties**:\n"
            "- **Cleavage**: Tendency to split along flat planes of weak atomic bonds. Described by directions and quality (e.g., basal cleavage in mica, cubic cleavage in galena).\n"
            "- **Hardness**: Resistance to scratching. Measured on **Mohs Hardness Scale** from 1 (Talc) to 10 (Diamond).\n"
            "- **Luster**: Appearance of mineral surface in reflected light. Grouped into Metallic (e.g., pyrite) and Non-metallic (e.g., vitreous quartz, pearly talc).\n"
            "- **Color & Streak**: Color is variable, but streak (color of mineral powder on ceramic plate) is constant."
        )
    elif "silicate" in q_lower or "nesosilicate" in q_lower:
        return (
            "1. **Silicate unit**: Built of silicon-oxygen tetrahedra ($SiO_4^{4-}$).\n"
            "2. **Classification based on linkage**:\n"
            "- **Orthosilicates (Nesosilicates)**: Isolated tetrahedra linked by cations. Ratio $Si:O = 1:4$ (e.g., Olivine, Garnet).\n"
            "- **Sorosilicates**: Double tetrahedra sharing one oxygen. Ratio $Si:O = 2:7$ (e.g., Epidote).\n"
            "- **Inosilicates (Chain)**:\n"
            "  - Single chains: sharing two oxygens. Ratio $Si:O = 1:3$ (e.g., Pyroxenes).\n"
            "  - Double chains: sharing alternatively two and three oxygens. Ratio $Si:O = 4:11$ (e.g., Amphiboles).\n"
            "- **Phyllosilicates (Sheet)**: Sharing three oxygens. Ratio $Si:O = 2:5$ (e.g., Mica, Talc, Clay).\n"
            "- **Tektosilicates (Framework)**: Sharing all four oxygens in 3D networks. Ratio $Si:O = 1:2$ (e.g., Quartz, Feldspars)."
        )
    elif "feldspar" in q_lower or "plagioclase" in q_lower:
        return (
            "1. **Composition**:\n"
            "- Framework aluminosilicates represented by the ternary system: Orthoclase ($KAlSi_3O_8$), Albite ($NaAlSi_3O_8$), and Anorthite ($CaAl_2Si_2O_8$).\n"
            "2. **Subgroups**:\n"
            "- **Alkali Feldspars**: Solid solution between $K$-feldspar and $Na$-feldspar (e.g., Orthoclase, Microcline, Sanidine). Show perthitic exsolution under slow cooling.\n"
            "- **Plagioclase Feldspars**: Isomorphous series between Albite ($Ab$) and Anorthite ($An$) (classified as Oligoclase, Andesine, Labradorite, Bytownite). Exhibit characteristic polysynthetic twinning.\n"
            "3. **Properties**: Hardness 6, two perpendicular cleavage directions, white/pink color. Weather into kaolinite clay."
        )
    elif "isomorphism" in q_lower or "polymorphism" in q_lower:
        return (
            "1. **Isomorphism**:\n"
            "- Minerals with different chemical compositions but identical crystal structures. Cations substitute for each other if ionic radii are within $15\\%$.\n"
            "- Example: The Plagioclase series ($NaAlSi_3O_8$ to $CaAl_2Si_2O_8$) or Olivine series (Forsterite $Mg_2SiO_4$ to Fayalite $Fe_2SiO_4$).\n"
            "2. **Polymorphism**:\n"
            "- One chemical composition existing in different crystal structures due to different pressure-temperature conditions.\n"
            "- Examples:\n"
            "  - Carbon ($C$): Diamond (isometric, high pressure) vs. Graphite (hexagonal, low pressure).\n"
            "  - Calcium Carbonate ($CaCO_3$): Calcite (trigonal) vs. Aragonite (orthorhombic).\n"
            "  - Aluminium Silicate ($Al_2SiO_5$): Kyanite (high P), Sillimanite (high T), Andalusite (low P/T)."
        )
    elif "symmetry" in q_lower or "crystal system" in q_lower:
        return (
            "1. **Symmetry Elements**:\n"
            "- **Center of Symmetry** ($i$): Imaginary central point through which faces match antipodally.\n"
            "- **Axes of Symmetry** ($g$-fold): Line around which rotation by $360^\\circ/n$ repeats form (2, 3, 4, or 6 fold).\n"
            "- **Planes of Symmetry** ($m$): Divides crystal into mirror images.\n"
            "2. **Six Crystal Systems**:\n"
            "- **Isometric**: $a=b=c$, $\\alpha=\\beta=\\gamma=90^\\circ$ (e.g., Halite).\n"
            "- **Tetragonal**: $a=b\\neq c$, $\\alpha=\\beta=\\gamma=90^\\circ$ (e.g., Zircon).\n"
            "- **Orthorhombic**: $a\\neq b\\neq c$, $\\alpha=\\beta=\\gamma=90^\\circ$ (e.g., Baryte).\n"
            "- **Hexagonal / Trigonal**: $a=b\\neq c$, $\\alpha=\\beta=90^\\circ, \\gamma=120^\\circ$ (e.g., Quartz, Calcite).\n"
            "- **Monoclinic**: $a\\neq b\\neq c$, $\\alpha=\\gamma=90^\\circ, \\beta\\neq 90^\\circ$ (e.g., Gypsum).\n"
            "- **Triclinic**: $a\\neq b\\neq c$, $\\alpha\\neq \\beta\\neq \\gamma\\neq 90^\\circ$ (e.g., Kyanite)."
        )
    
    # Petrology
    elif "magma" in q_lower or "bowen" in q_lower:
        return (
            "1. **Magma**: Molten rock material beneath the Earth's surface consisting of liquid melt, dissolved gases, and crystals.\n"
            "2. **Bowen's Reaction Series**:\n"
            "- Explains the sequence of mineral crystallization from cooling basaltic magma.\n"
            "- **Discontinuous Series**: Iron-magnesium silicates. Olivine $\\rightarrow$ Pyroxene $\\rightarrow$ Amphibole $\\rightarrow$ Biotite. React with liquid to form the next mineral.\n"
            "- **Continuous Series**: Plagioclase feldspars. Calcic plagioclase (Anorthite) continuously changes to sodic plagioclase (Albite) by ion exchange.\n"
            "- **Final Stages**: Crystallization of Orthoclase, Muscovite, and finally Quartz at lowest temperatures.\n"
            "3. **Significance**: Predicts mineral assemblages in igneous rocks and index mineral weathering susceptibility."
        )
    elif "igneous" in q_lower or "granite" in q_lower or "basalt" in q_lower:
        return (
            "1. **Origin**: Formed from cooling and consolidation of molten magma (plutonic) or volcanic lava.\n"
            "2. **Textures**:\n"
            "- **Phaneritic**: Coarse-grained, plutonic cooling (e.g., Granite, Gabbro).\n"
            "- **Aphanitic**: Fine-grained, rapid volcanic cooling (e.g., Basalt, Rhyolite).\n"
            "- **Porphyritic**: Two distinct grain sizes representing two stages of cooling (phenocrysts in groundmass).\n"
            "- **Glassy**: Quenched cooling without crystals (e.g., Obsidian).\n"
            "3. **Structures**: Vescular, amygdaloidal, columnar joints, pillow structures.\n"
            "4. **Tectonic Setting**: Subduction zones, mid-ocean ridges, mantle plumes."
        )
    elif "sedimentary" in q_lower or "sandstone" in q_lower or "clastic" in q_lower:
        return (
            "1. **Formation**: Weathering products of pre-existing rocks are transported, deposited in basins, and lithified via diagenesis (compaction and mineral cementation).\n"
            "2. **Clastic vs. Non-clastic**:\n"
            "- **Clastic**: Built of rock fragments and mineral grains (e.g., Sandstone, Shale, Conglomerate).\n"
            "- **Non-clastic (Chemical/Organic)**: Formed by chemical precipitation (e.g., rock salt, gypsum) or organic accumulation (e.g., limestone from shells, coal).\n"
            "3. **Sedimentary Structures**:\n"
            "- **Bedding/Stratification**: Horizontal deposition planes.\n"
            "- **Cross-bedding**: Inclined layers representing migrating dunes or ripples.\n"
            "- **Ripple Marks**: Wave-like ripples on bedding surfaces (current or wave types).\n"
            "- **Graded Bedding**: Coarser particles at bottom, grading to fine on top (turbidity currents)."
        )
    elif "metamorphism" in q_lower or "metamorphic" in q_lower or "facies" in q_lower:
        return (
            "1. **Definition**:\n"
            "- Mineralogical and structural changes in pre-existing rocks under elevated Temperature, Pressure, and Chemically active fluids without melting.\n"
            "2. **Agents**:\n"
            "- **Temperature**: Recrystallizes minerals, drives chemical reactions.\n"
            "- **Pressure**: Uniform (lithostatic) pressure causes density increase; directed (shear) stress aligns flaky minerals.\n"
            "3. **Kinds**:\n"
            "- **Thermal/Contact**: Driven by magmatic heat. Forms Hornfels.\n"
            "- **Dynamic**: Driven by fault zone stress. Forms Mylonite.\n"
            "- **Regional**: Large scale, combined heat and directed pressure (orogeny). Forms Schist and Gneiss.\n"
            "4. **Facies**: Mineral assemblages indicative of specific P-T fields (e.g., Zeolite, Greenschist, Amphibolite, Granulite, Eclogite facies)."
        )
    
    # Palaeontology & Stratigraphy
    elif "fossil" in q_lower or "fossilization" in q_lower:
        return (
            "1. **Conditions for Fossilization**:\n"
            "- Rapid burial in sediment to protect from scavengers and weathering.\n"
            "- Presence of hard skeletal parts (bones, shells, wood).\n"
            "- Low-oxygen (anoxic) conditions to prevent bacterial decay.\n"
            "2. **Modes of Preservation**:\n"
            "- **Permineralization**: Minerals fill internal pore spaces of bones/wood.\n"
            "- **Replacement**: Molecule-by-molecule replacement of original material (e.g., silicification, pyritization).\n"
            "- **Carbonization**: Volatiles are squeezed out, leaving a thin carbon film (e.g., plant leaves).\n"
            "- **Molds & Casts**: Internal or external impressions left in rock.\n"
            "- **Unaltered Preservation**: In freezing ice, amber, or tar pits."
        )
    elif "trilobite" in q_lower:
        return (
            "1. **Morphology**:\n"
            "- Exoskeleton divided into three parts longitudinally (axial lobe, two pleural lobes) and transversely (cephalon/head, thorax/segments, pygidium/tail).\n"
            "- **Cephalon**: Glabella, cheeks (free and fixed), compound eyes, and facial sutures (proparian, gonatoparian, opisthoparian).\n"
            "2. **Genal Angle**: Corner of cephalon, often extending into genal spines.\n"
            "3. **Geological distribution**: Strictly Palaeozoic (Cambrian to Permian). Index fossils for Cambrian stratigraphy."
        )
    elif "gondwana" in q_lower:
        return (
            "1. **Tectonic Settings**: Intracratonic rift basins in peninsular India (Damodar, Mahanadi, Godavari valleys).\n"
            "2. **Flora**:\n"
            "- **Lower Gondwana (Permian)**: Glossopteris, Gangamopteris, Noeggerathiopsis. Indicates cold, humid climate (glacial deposits at base - Talchir).\n"
            "- **Upper Gondwana (Triassic-Cretaceous)**: Ptilophyllum, Dicroidium, Cycadites. Indicates warm, dry to warm, humid conditions.\n"
            "3. **Economic Significance**: Hosts over $98\\%$ of India's metallurgical coal reserves (Raniganj, Jharia coalfields)."
        )
    elif "correlation" in q_lower or "stratigraphy" in q_lower:
        return (
            "1. **Correlation Principles**:\n"
            "- Proving the equivalence of rock units in different geographic areas.\n"
            "- **Lithostratigraphic**: Based on rock types, marker beds, and sequence of beds.\n"
            "- **Biostratigraphic**: Based on assemblage zones, range zones, and index fossils.\n"
            "2. **Laws of Stratigraphy**:\n"
            "- **Superposition**: In an undisturbed sequence, oldest layer is at bottom.\n"
            "- **Original Horizontality**: Sediments are deposited in flat, horizontal layers.\n"
            "- **Lateral Continuity**: Sedimentary layers extend laterally in all directions.\n"
            "- **Faunal Succession**: Fossil organisms succeed each other in a definite, determinable order."
        )
    
    # Economic Geology, Hydrogeology & Exploration
    elif "ore" in q_lower or "magmatic" in q_lower:
        return (
            "1. **Definitions**:\n"
            "- **Ore**: Rock containing minerals of economic value that can be extracted for profit.\n"
            "- **Gangue**: Valueless waste minerals associated with ore in a deposit.\n"
            "- **Tenor**: Grade or metal content of the ore.\n"
            "2. **Magmatic Concentration Processes**:\n"
            "- **Early Magmatic**: Minerals crystallize and accumulate early.\n"
            "  - **Dissemination**: Spaced out crystals (e.g., diamond in kimberlite).\n"
            "  - **Segregation**: Settling of early crystals (e.g., chromite bands).\n"
            "- **Late Magmatic**: Residual melts rich in volatiles crystallize last (e.g., pegmatites, magnetite injections)."
        )
    elif "hydrothermal" in q_lower or "vein" in q_lower:
        return (
            "1. **Definition**: Deposition of minerals from hot aqueous fluids derived from cooling magmas.\n"
            "2. **Cavity Filling Deposits**:\n"
            "- Minerals precipitate in fractures, fissures, or pores. Forms veins (fissure veins, stockworks, saddle reefs). Show symmetrical bandings.\n"
            "3. **Metasomatic Replacement**:\n"
            "- Chemical exchange of host rock minerals with hydrothermal ions, forming new minerals (e.g., skarns in limestones).\n"
            "4. **Classifications**: Hypothermal (hot, deep), Mesothermal (medium), Epithermal (shallow, low temperature)."
        )
    elif "groundwater" in q_lower or "darcy" in q_lower or "aquifer" in q_lower:
        return (
            "1. **Aquifer Types**:\n"
            "- **Unconfined**: Water table forms upper boundary. Exposed to atmosphere.\n"
            "- **Confined**: Bounded above and below by impermeable beds (aquicludes). Water is under pressure.\n"
            "2. **Parameters**:\n"
            "- **Porosity**: Percentage of void space in rock.\n"
            "- **Permeability**: Capacity of rock to transmit fluids.\n"
            "3. **Darcy's Law**:\n"
            "- $$Q = -K \\cdot A \\cdot \\frac{dh}{dl}$$\n"
            "- Where $Q$ is discharge, $K$ is hydraulic conductivity, $A$ is cross-sectional area, and $dh/dl$ is hydraulic gradient.\n"
            "4. **Resistivity Exploration**: Vertical Electrical Sounding (VES) using Schlumberger or Wenner arrays to locate aquifers based on low resistivity zones."
        )
    
    # Fallback
    return (
        f"1. **Core Concept**:\n"
        f"- Represents a major topic in {GEOLOGY_SYLLABI.get(subject_key, {}).get('title', 'Geology')}.\n"
        f"2. **Geological Context**:\n"
        f"- Weathering, metamorphic alteration, or tectonic deformation plays a major role.\n"
        f"- Studied through petrographic microscopy, structural mapping, or stratigraphic correlation.\n"
        f"3. **Significance**:\n"
        f"- Essential for resource exploration, hazard mitigation, or reconstructing Earth's geological history."
    )

# Main script
def main():
    tex_dir = "aaa/geology"
    if not os.path.exists(tex_dir):
        print(f"Geology folder not found at {tex_dir}")
        return

    # 1. Initialize question dictionaries
    raw_questions = {k: [] for k in GEOLOGY_SYLLABI.keys()}

    # 2. Scan and parse all LaTeX files
    files = [f for f in os.listdir(tex_dir) if f.endswith(".tex")]
    files.sort()

    print(f"Scanning {len(files)} Geology LaTeX files...")
    for file_name in files:
        filepath = os.path.join(tex_dir, file_name)
        gkey = get_glb_mapping(file_name)
        if gkey:
            qs = parse_tex_file(filepath)
            raw_questions[gkey].extend(qs)
            print(f" - Parsed {len(qs)} questions from {file_name} -> Mapped to {gkey}")

    # 3. Load active exams database
    exams_js_path = "js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])

    # 4. Generate 50 questions for each unique key
    print("\nProcessing and padding questions to 50 for each Geology syllabus...")
    for unique_key, active_list in UNIQUE_TO_ACTIVE.items():
        raw_qs = raw_questions.get(unique_key, [])
        standard_qs = GEOLOGY_SYLLABI.get(unique_key, {}).get("standard_questions", [])
        
        # Deduplicate raw questions
        seen = set()
        final_questions = []
        for q_text in raw_qs:
            q_norm = q_text.lower().strip()
            if q_norm not in seen and len(q_text) > 15:
                seen.add(q_norm)
                final_questions.append(q_text)

        # Pad with standard questions
        std_idx = 0
        while len(final_questions) < 50 and std_idx < len(standard_qs):
            q_text, unit = standard_qs[std_idx]
            q_norm = q_text.lower().strip()
            if q_norm not in seen:
                seen.add(q_norm)
                final_questions.append((q_text, unit))
            std_idx += 1

        # Fallback pad if still under 50
        fallback_idx = 1
        title_text = GEOLOGY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())
        while len(final_questions) < 50:
            q_text = f"Describe the fundamental principles, theoretical models, and experimental studies of {title_text} (Part {fallback_idx})."
            final_questions.append((q_text, "V"))
            fallback_idx += 1

        # Slice to exactly 50
        final_questions = final_questions[:50]

        # Format questions array
        formatted_questions = []
        for idx, item in enumerate(final_questions):
            q_id = idx + 1
            if isinstance(item, tuple):
                q_text = item[0]
                unit = item[1]
            else:
                q_text = item
                # Distribute units evenly (Units I to V)
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

        # 5. Inject into exams dictionary for all active codes
        for active_key in active_list:
            orig = EXAMS.get(active_key, {})
            EXAMS[active_key] = {
                "id": active_key,
                "title": orig.get("title", GEOLOGY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())),
                "module": orig.get("module", active_key.upper()),
                "duration": 60,
                "type": "theory",
                "comingSoon": False,
                "questions": formatted_questions
            }
            print(f" - Key: {active_key} populated successfully. (Live: True, Questions: {len(formatted_questions)})")

    # 6. Save back to js/exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)

    print("\njs/exams-data.js has been successfully updated with 50 questions for each Geology paper!")

if __name__ == "__main__":
    main()
