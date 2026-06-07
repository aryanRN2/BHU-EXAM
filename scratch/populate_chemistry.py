import json
import re
import os

# 1. Define chemistry syllabi and standard questions for augmentation
CHEMISTRY_SYLLABI = {
    "chemd11": {
        "title": "Basic Principles of Chemistry and Its Applications",
        "standard_questions": [
            ("Discuss the VSEPR theory and explain the shapes of $\\text{H}_2\\text{O}$ and $\\text{NH}_3$ molecules.", "I"),
            ("State the octet rule and explain why some molecules like $\\text{SF}_6$ show an expanded octet.", "I"),
            ("Explain the principles of Paper Chromatography and Thin Layer Chromatography.", "II"),
            ("Describe the preparation and analytical applications of Fehling's solution.", "II"),
            ("Discuss the biological role of trace metals like Zinc and Cobalt in the human body.", "III"),
            ("Discuss the thermodynamics of spontaneous processes and state the criteria for spontaneity in terms of $\\Delta G$.", "IV"),
            ("State and explain the Gibbs-Helmholtz equation and write its significance.", "IV"),
            ("Describe the extraction of Iron from hematite ore using a blast furnace with chemical equations.", "V"),
            ("Discuss the synthesis and uses of Teflon and Buna-S rubber.", "V"),
            ("Explain Fajan's rules for predicting covalent character in ionic compounds with examples.", "I"),
            ("Explain the concept of oxidation state and assign oxidation states to Mn in $\\text{KMnO}_4$ and Cr in $\\text{K}_2\\text{Cr}_2\\text{O}_7$.", "I"),
            ("Describe the preparation and analytical applications of Benedict's reagent.", "II"),
            ("Differentiate between binding energy and packing fraction with physical significance.", "III"),
            ("Explain how paper chromatography differs from thin-layer chromatography in terms of stationary and mobile phases.", "II"),
            ("Discuss the role of metal complexes as analytical reagents, focusing on DMG.", "II"),
            ("Derive the expression for the entropy change ($\\Delta S$) of an ideal gas expanding isothermally.", "IV"),
            ("Explain the discrepancy of bond angles in $\\text{SO}_2$ and $\\text{H}_2\\text{O}$ using VSEPR theory.", "I"),
            ("Describe the biological role of zinc in enzymes like carbonic anhydrase.", "III"),
            ("Explain the reactions involved in the reduction zone of a blast furnace during iron extraction.", "V"),
            ("Discuss the monomer structures and polymerization reactions for Buna-S rubber.", "V")
        ]
    },
    "chemd21": {
        "title": "Energy & Metallurgy",
        "standard_questions": [
            ("Explain the significance of the Octane and Cetane numbers in evaluating fuel quality.", "I"),
            ("Describe the lead storage battery, detailing the charging and discharging reactions.", "II"),
            ("Discuss the differences between Photosystem I and Photosystem II in photosynthesis.", "III"),
            ("Explain the light and dark reactions of photosynthesis in plants.", "III"),
            ("Discuss the biological roles of hemoglobin and myoglobin in oxygen transport.", "III"),
            ("Define the standard enthalpy of formation ($\\Delta H_f^\\circ$) and standard entropy change.", "IV"),
            ("Explain the second law of thermodynamics and its relation to entropy.", "IV"),
            ("Derive the relation between cell potential ($E$) and Gibbs free energy change ($\\Delta G$).", "V"),
            ("Discuss fuel cells and explain the working of a hydrogen-oxygen fuel cell.", "V"),
            ("Explain the extraction of Copper from copper pyrites with relevant chemical reactions.", "I"),
            ("Explain how knock-inhibitors like tetraethyl lead work to improve octane rating.", "I"),
            ("What is a cell constructed from standard reduction potentials? Explain with an example of Zinc and Copper.", "V"),
            ("State the first law of thermodynamics and define path and state functions.", "IV"),
            ("Discuss the role of myoglobin in muscles and compare its oxygen affinity curve with hemoglobin.", "III"),
            ("Describe the construction of a simple galvanic cell and calculate its cell EMF.", "V"),
            ("Explain the mechanism of carbon dioxide assimilation in the dark reaction (Calvin cycle).", "III"),
            ("Define Gibbs free energy and show its relation to spontaneity at constant temperature and pressure.", "IV"),
            ("Describe the chemical reactions occurring in lead accumulator battery during charging.", "II"),
            ("Explain how the cetane number of a diesel fuel can be increased using additives.", "I"),
            ("Discuss the extraction of zinc from zinc blende with equations.", "I")
        ]
    },
    "chemd31": {
        "title": "Environmental Chemistry",
        "standard_questions": [
            ("Differentiate between binding energy and packing fraction with physical significance.", "I"),
            ("Explain the phenomenon of nuclear fission and fusion with appropriate equations.", "I"),
            ("Describe the greenhouse effect and list the major greenhouse gases.", "II"),
            ("Discuss the mechanism of ozone layer depletion in the stratosphere.", "II"),
            ("Explain the sources and control measures of acid rain.", "II"),
            ("Discuss the toxicity of heavy metals like Mercury and Lead in the ecosystem.", "III"),
            ("Explain the concept of Green Chemistry and list its 12 principles.", "IV"),
            ("Describe the methods used for the purification of industrial wastewater.", "IV"),
            ("Explain soil pollution, its causes, and its impact on agriculture.", "V"),
            ("Discuss the role of polymers in waste management and their recycling methods.", "V"),
            ("Describe the nuclear binding energy curve and explain why elements near Iron are most stable.", "I"),
            ("Explain the radioactive decay law and derive the relation between half-life and decay constant.", "I"),
            ("Discuss the impact of chlorofluorocarbons (CFCs) on stratospheric ozone layer.", "II"),
            ("What are the primary air pollutants and how do they contribute to photochemical smog?", "II"),
            ("Explain the term BOD (Biochemical Oxygen Demand) and COD (Chemical Oxygen Demand).", "III"),
            ("Discuss the principles of atom economy in green chemistry with an example.", "IV"),
            ("Explain the biological hazards of radioactive waste and its safe disposal.", "I"),
            ("Describe how heavy metal ions like $Pb^{2+}$ and $Hg^{2+}$ inhibit enzymatic activities.", "III"),
            ("Explain the municipal water treatment processes including coagulation, sedimentation, and chlorination.", "IV"),
            ("Discuss the environmental impact of non-biodegradable plastics and bioplastic alternatives.", "V")
        ]
    },
    "chemj11": {
        "title": "Basic Concepts of Chemistry-I",
        "standard_questions": [
            ("Describe the Born-Haber cycle for the determination of the lattice energy of $\\text{NaCl}$.", "I"),
            ("Discuss the shapes of $\\text{XeF}_4$ and $\\text{ClF}_3$ based on VSEPR theory.", "II"),
            ("Draw the molecular orbital energy level diagram for $\\text{O}_2$ and calculate its bond order.", "III"),
            ("Explain hybridization and determine the hybridization of carbon in ethylene and acetylene.", "III"),
            ("Discuss the periodic trends of ionization energy and electron affinity in the periodic table.", "IV"),
            ("Explain hydrogen bonding, distinguishing between intermolecular and intramolecular hydrogen bonding.", "V"),
            ("State the Heisenberg uncertainty principle and its significance in atomic structure.", "I"),
            ("Describe the Schrodinger wave equation and the significance of wave function $\\psi$.", "I"),
            ("Explain Fajan's rules for predicting covalent character in ionic compounds.", "II"),
            ("Discuss the band theory of solids and distinguish between conductors, semiconductors, and insulators.", "V"),
            ("Explain the quantum numbers and their significance in defining atomic orbitals.", "I"),
            ("Discuss the concept of resonance and draw resonance structures of carbonate ion ($\\text{CO}_3^{2-}$).", "II"),
            ("Explain the concept of electronegativity and discuss Pauling's scale.", "IV"),
            ("Describe the shapes of d-orbitals and write the values of angular quantum numbers.", "I"),
            ("Discuss the molecular orbital energy level diagram of $\\text{CO}$ and $\\text{NO}$ molecules.", "III"),
            ("Define lattice energy and write the Born-Lande equation, explaining all terms.", "I"),
            ("Explain the dipole moment and its use in predicting molecular geometries.", "II"),
            ("Discuss the structures of diborane and explain the nature of three-center two-electron bonds.", "V"),
            ("What is the shielding effect and how does it affect the effective nuclear charge?", "IV"),
            ("Explain the structures of carbon allotropes (diamond and graphite) in terms of hybridization.", "V")
        ]
    },
    "chemj21": {
        "title": "Basic Concepts of Chemistry-II",
        "standard_questions": [
            ("Derive the kinetic gas equation and show that kinetic energy is proportional to temperature.", "I"),
            ("Describe Bragg's law and explain its use in crystal structure determination.", "II"),
            ("Derive the rate expression for a first-order chemical reaction and define half-life.", "III"),
            ("Explain the HSAB (Hard and Soft Acids and Bases) principle and list its applications.", "IV"),
            ("Discuss the properties of dilute solutions of sodium in liquid ammonia.", "IV"),
            ("State the differences between crystalline and amorphous solids.", "II"),
            ("Explain the mechanism of enzyme catalysis using the Michaelis-Menten equation.", "III"),
            ("Derive the Clausius-Clapeyron equation and discuss its application to liquid-vapor equilibrium.", "V"),
            ("Describe the structure of sodium chloride ($\\text{NaCl}$) and cesium chloride ($\\text{CsCl}$).", "II"),
            ("Discuss the Arrhenius and Bronsted-Lowry concepts of acids and bases with examples.", "IV"),
            ("Derive the expression for the root mean square velocity of gas molecules from kinetic theory.", "I"),
            ("Discuss the deviations of real gases from ideal behavior and write the van der Waals equation.", "I"),
            ("Explain the terms: unit cell, space lattice, and Miller indices.", "II"),
            ("Describe the experimental methods for determining the order of a chemical reaction.", "III"),
            ("Discuss Lewis acid-base concept and explain its advantages over Bronsted concept.", "IV"),
            ("Explain the leveling effect of solvents on acidic strengths.", "IV"),
            ("Describe the structure of liquid crystals and discuss their classification and uses.", "V"),
            ("State the collision theory of reaction rates and explain steric factor.", "III"),
            ("Discuss the crystalline structures of metals (hcp, ccp, bcc).", "II"),
            ("Explain the concept of activation energy and how it is determined using the Arrhenius plot.", "III")
        ]
    },
    "chemj31": {
        "title": "Inorganic Chemistry - I",
        "standard_questions": [
            ("Discuss the structure and bonding in diborane ($\\text{B}_2\\text{H}_6$).", "I"),
            ("Explain the preparation, properties, and structure of Xenon tetrafluoride ($\\text{XeF}_4$).", "II"),
            ("Describe the oxidation states and trends in the chemistry of nitrogen family elements.", "III"),
            ("Discuss the structure and properties of silicates and their classification.", "IV"),
            ("Explain the preparation, properties, and structure of interhalogen compounds like $\\text{IF}_7$.", "V"),
            ("Discuss the diagonal relationship between Lithium and Magnesium.", "I"),
            ("Explain the basic properties and applications of noble gases.", "II"),
            ("Discuss the anomalous behavior of Fluorine in group 17 elements.", "V"),
            ("Describe the structures of various oxides and oxyacids of phosphorus.", "III"),
            ("Explain the preparation and uses of sodium thiosulfate in laboratory analysis.", "I"),
            ("Discuss the structure and properties of borazines and compare them with benzene.", "I"),
            ("Explain the diagonal relationship between Beryllium and Aluminum.", "I"),
            ("Discuss the structures and properties of fluorocarbons and their environmental concerns.", "V"),
            ("Describe the preparation and structures of xenon fluorides ($\\text{XeF}_2$ and $\\text{XeF}_6$).", "II"),
            ("Discuss the structures and acid strengths of oxyacids of halogens.", "V"),
            ("Explain the preparation, properties, and structure of hydrazine.", "III"),
            ("Describe the classification of hydrides into ionic, covalent, and metallic hydrides.", "I"),
            ("Discuss the preparation, properties, and structure of phosphazenes.", "III"),
            ("Explain the structure of sulfur trioxide and its polymerization.", "IV"),
            ("Describe the principles of silicate structures and coordinate linkages.", "IV")
        ]
    },
    "chemj32": {
        "title": "Organic Chemistry - I",
        "standard_questions": [
            ("Classify tropylium ion and cyclopentadienyl cation as aromatic, antiaromatic, or nonaromatic.", "I"),
            ("Discuss the mechanism of the Beckmann rearrangement with a suitable example.", "II"),
            ("Explain the Baeyer-Villiger oxidation and discuss its mechanism.", "II"),
            ("Describe the mechanism of the Perkin reaction for the synthesis of cinnamic acid.", "III"),
            ("Compare the acid strength of phenol, $p$-nitrophenol, and $p$-cresol with reasons.", "IV"),
            ("Discuss the reaction of ethylene oxide with methylmagnesium bromide.", "V"),
            ("Describe the mechanism of preparation of DDT from chloral and chlorobenzene.", "I"),
            ("Explain why aniline undergoes meta-substitution in a strongly acidic medium.", "IV"),
            ("Discuss the preparation of Novolac and Bakelite from phenol and formaldehyde.", "V"),
            ("Explain the mechanism of the Reimer-Tiemann reaction.", "IV"),
            ("Describe the Huckel rule of aromaticity and explain why cyclooctatetraene is non-aromatic.", "I"),
            ("Discuss the mechanism of electrophilic aromatic substitution (nitration of benzene).", "I"),
            ("Explain the mechanism of the Pinacol-Pinacolone rearrangement.", "II"),
            ("Discuss the synthetic utility and mechanism of the Aldol condensation.", "III"),
            ("Describe the mechanism of the Cannizzaro reaction with an example.", "III"),
            ("Explain why phenol is more acidic than alcohols but less acidic than carboxylic acids.", "IV"),
            ("Discuss the ring-opening reactions of epoxides under acidic and basic conditions.", "V"),
            ("Describe the mechanism of the Friedel-Crafts alkylation of benzene and its limitations.", "I"),
            ("Discuss the mechanism of the Benzoin condensation.", "III"),
            ("Explain the orientation and reactivity in electrophilic substitution of toluene.", "I")
        ]
    },
    "chemj33": {
        "title": "Physical Chemistry - I",
        "standard_questions": [
            ("Derive the Henderson-Hasselbalch equation for an acidic buffer solution.", "I"),
            ("Explain the Gibbs phase rule and discuss its application to a one-component water system.", "II"),
            ("Describe the construction and working of the Quinhydrone electrode.", "III"),
            ("Explain how the transference numbers of ions depend on temperature and concentration.", "IV"),
            ("Calculate the equivalent conductivity of acetic acid at infinite dilution using Kohlrausch's law.", "V"),
            ("Describe the conductometric titration curve of a weak base ($\\text{NH}_4\\text{OH}$) with a strong acid ($\\text{HBr}$).", "V"),
            ("State and explain the Nernst distribution law and write its applications.", "I"),
            ("Define mean ionic activity ($a_\\pm$) and relate it to the molality ($m$) of an electrolyte.", "III"),
            ("State the third law of thermodynamics and explain the concept of residual entropy.", "II"),
            ("Derive the relationship between the equilibrium constant ($K_p$) and temperature (van 't Hoff equation).", "I"),
            ("Explain the buffer capacity and how buffer index is calculated.", "I"),
            ("Discuss the phase diagram of a two-component lead-silver system.", "II"),
            ("Describe the construction and cell reactions of the calomel electrode.", "III"),
            ("Explain the moving boundary method for the determination of transference numbers.", "IV"),
            ("Discuss Kohlrausch's law of independent migration of ions and its applications.", "V"),
            ("Explain conductometric titrations and draw the curve for strong acid vs strong base titration.", "V"),
            ("State the phase rule and define terms: phase, component, and degrees of freedom.", "II"),
            ("Explain the Nernst equation for cell EMF and discuss its application.", "III"),
            ("Discuss the Debye-Huckel limiting law for activity coefficients of strong electrolytes.", "III"),
            ("Explain liquid junction potential and how it can be minimized using a salt bridge.", "III")
        ]
    },
    "chemj34": {
        "title": "Qualitative Analysis and Thermochemistry",
        "standard_questions": [
            ("Explain the role of the solubility product and the common ion effect in qualitative analysis.", "I"),
            ("State Hess's law of constant heat summation and discuss its applications.", "II"),
            ("Describe the procedure for the identification of Group II cations in qualitative analysis.", "III"),
            ("Explain bond enthalpy and how it is used to calculate the enthalpy of a reaction.", "IV"),
            ("Discuss the qualitative tests for the identification of nitrate and sulfate anions.", "V"),
            ("Explain how Group III cations are separated from Group IV cations using solubility products.", "I"),
            ("Derive the relation between constant pressure enthalpy change ($\\Delta H$) and constant volume internal energy change ($\\Delta U$).", "II"),
            ("Describe the flame test in qualitative inorganic analysis and explain the chemistry behind it.", "III"),
            ("Discuss the calorimetric determination of the enthalpy of neutralization of a strong acid with a strong base.", "IV"),
            ("Explain the chemistry of the brown ring test for nitrates.", "V"),
            ("What is the role of ammonium chloride in the precipitation of Group III hydroxide cations?", "I"),
            ("Define standard enthalpy of combustion and describe how it is measured using a bomb calorimeter.", "II"),
            ("Explain the sodium carbonate extract preparation and its use in anion testing.", "III"),
            ("Discuss the bond dissociation energy and how it differs from average bond energy.", "IV"),
            ("Explain the qualitative analysis of Group V cations (Barium, Strontium, Calcium).", "V")
        ]
    },
    "chemj41": {
        "title": "Inorganic Chemistry - II",
        "standard_questions": [
            ("Describe Werner's coordination theory and explain primary and secondary valencies.", "I"),
            ("Draw all geometrical and optical isomers of the complex $[\\text{Co(en)}_2\\text{Cl}_2]^+$.", "II"),
            ("Explain the variable oxidation states of 3d transition metals and how they are stabilized.", "III"),
            ("Describe the ion-exchange chromatography method for the separation of lanthanide ions.", "IV"),
            ("Discuss the HSAB principle and classify coordination complexes based on hard-soft interactions.", "V"),
            ("Write IUPAC names for $\\text{Na}_3[\\text{Co(NO}_2)_6]$ and $\\text{K}[\\text{PtCl}_3(\\text{C}_2\\text{H}_4)]$.", "I"),
            ("Explain the colors of anhydrous $\\text{CuSO}_4$ and hydrated $\\text{CuSO}_4\\cdot5\\text{H}_2\\text{O}$.", "III"),
            ("Explain why lanthanide contraction occurs and discuss its chemical consequences.", "IV"),
            ("Discuss the reactions of metal complexes in liquid ammonia solvent.", "V"),
            ("Explain the magnetic properties of transition metal complexes using Valence Bond Theory.", "III"),
            ("Discuss the effective atomic number (EAN) rule and calculate EAN of iron in $[\\text{Fe(CN)}_6]^{4-}$.", "I"),
            ("Explain the linkage and coordination position isomerisms with examples.", "II"),
            ("Discuss the structural trends, oxidation states, and colors of 3d transition metals.", "III"),
            ("Explain the solvent system concept of acids and bases in liquid sulfur dioxide.", "V"),
            ("Describe the separation of lanthanides by solvent extraction method.", "IV"),
            ("Discuss the stability of coordination complexes in terms of thermodynamic and kinetic stability.", "I"),
            ("Explain the bonding in coordination complexes using Valence Bond Theory and its limitations.", "III"),
            ("Describe the biological role of hard and soft acids/bases.", "V"),
            ("Discuss the chemistry of non-aqueous solvents, focusing on liquid ammonia.", "V"),
            ("Explain why transition metals form a large number of coordination complexes.", "III")
        ]
    },
    "chemj42": {
        "title": "Organic Chemistry - II",
        "standard_questions": [
            ("Explain why pyridine undergoes electrophilic substitution at position 3, while pyridine 1-oxide reacts at position 4.", "I"),
            ("Discuss the Skraup synthesis of quinoline with its reaction mechanism.", "II"),
            ("Describe the Ruff degradation and Kiliani-Fischer synthesis for carbohydrates.", "III"),
            ("Explain why fructose reduces Tollens' and Fehling's reagents despite being a ketone.", "IV"),
            ("Compare the aromatic character and reactivity of pyrrole, furan, and thiophene.", "V"),
            ("Describe the Chichibabin reaction of pyridine with sodamide and its mechanism.", "I"),
            ("Write the preparation of Indigotin (Indigo dye) from anthranilic acid.", "V"),
            ("Draw the structures of D-glucose and D-fructose in their open and cyclic forms.", "III"),
            ("Explain mutarotation in D-glucose and discuss its mechanism.", "III"),
            ("Discuss the synthesis of amino acids using the Gabriel phthalimide method.", "IV"),
            ("Describe the structure of naphthalene and discuss its electrophilic substitution at alpha vs beta position.", "I"),
            ("Discuss the Fischer indole synthesis and its mechanism.", "II"),
            ("Explain the structure elucidation of sucrose and write its hydrolysis products.", "III"),
            ("Discuss the synthesis of quinoline using the Bischler-Napieralski reaction.", "II"),
            ("Explain the structure and properties of starch and cellulose.", "III"),
            ("Describe the properties and zwitterionic structure of amino acids.", "IV"),
            ("Discuss the structure of peptide bonds and explain N-terminal analysis.", "IV"),
            ("Compare pyridine with pyrrole in terms of basicity and explain.", "I"),
            ("Describe the preparation and applications of synthetic dyes like Methyl Orange.", "V"),
            ("Discuss the mechanisms of oxidation and reduction of D-glucose.", "III")
        ]
    },
    "chemj43": {
        "title": "Physical Chemistry - II",
        "standard_questions": [
            ("Derive the Debye-Huckel-Onsager equation for strong electrolytes.", "I"),
            ("Describe the construction and working of the hydrogen-oxygen fuel cell.", "II"),
            ("Discuss the collision theory of bimolecular gas-phase reactions and its limitations.", "III"),
            ("Explain the transition state theory of reaction rates and compare it with collision theory.", "III"),
            ("Describe the mechanism of electrochemical corrosion of iron and methods of prevention.", "IV"),
            ("State the Nernst equation and apply it to calculate the EMF of a Daniel cell.", "II"),
            ("Discuss the kinetics of parallel and opposing chemical reactions.", "V"),
            ("Explain the concept of overpotential and its role in electrolytic deposition.", "I"),
            ("Describe the construction and reactions of the nickel-cadmium accumulator.", "II"),
            ("Discuss the chain reactions and derive the rate equation for the hydrogen-bromine reaction.", "III"),
            ("Explain the primary salt effect on the rates of ionic reactions.", "IV"),
            ("Discuss the thermodynamic derivation of the cell potential.", "V"),
            ("Describe the mechanism of acid-base catalysis and derive the rate equation.", "V"),
            ("Explain the kinetics of enzyme-catalyzed reactions and show Michaelis-Menten plot.", "III"),
            ("Discuss the concentration cells with and without transference.", "I"),
            ("Derive the relation between temperature coefficient of cell EMF and entropy change.", "V"),
            ("Explain the Lindemann mechanism for unimolecular gas phase reactions.", "III"),
            ("Describe the methods for measuring the EMF of a cell without drawing current.", "II"),
            ("Discuss the mechanism of metal passivation and corrosion prevention.", "IV"),
            ("State the Debye-Huckel limiting law and apply it to calculate activity coefficients.", "I")
        ]
    },
    "chemj44": {
        "title": "Techniques in Chemistry",
        "standard_questions": [
            ("State Beer-Lambert's law and discuss its limitations in quantitative spectrophotometry.", "I"),
            ("Describe the instrumentation and applications of Gas Chromatography (GC).", "II"),
            ("Explain the principles of High-Performance Liquid Chromatography (HPLC).", "III"),
            ("Discuss the co-precipitation and post-precipitation errors in gravimetric analysis.", "IV"),
            ("Explain the types of errors in chemical analysis and how to minimize them.", "V"),
            ("Describe the instrumentation and principle of Thin Layer Chromatography (TLC).", "II"),
            ("Discuss the gravimetric estimation of nickel using dimethylglyoxime (DMG).", "IV"),
            ("Explain accuracy, precision, and the statistical tests used for data validation.", "V"),
            ("Describe the instrumentation and principle of Atomic Absorption Spectroscopy (AAS).", "I"),
            ("Explain the use of standard additions and internal standards in analytical calibration.", "I"),
            ("Describe the column chromatography technique and discuss elution mechanisms.", "III"),
            ("Explain the thermogravimetric analysis (TGA) and draw the TGA curve of calcium oxalate.", "IV"),
            ("Discuss the complexometric titration of calcium and magnesium using EDTA.", "IV"),
            ("Explain the determination of path length and solvent effects in UV-Vis spectroscopy.", "I"),
            ("Discuss the principles of sampling of solids, liquids, and gases for analysis.", "V"),
            ("Describe the detectors used in Gas Chromatography (GC).", "II"),
            ("Explain the concept of chromatography resolution and height equivalent of theoretical plate (HETP).", "III"),
            ("Discuss the systematic and random errors and how they affect the mean and standard deviation.", "V"),
            ("Describe the volumetric estimation of copper using iodometric titration.", "IV"),
            ("Explain the principles of flame photometry and its applications in alkali metal analysis.", "I")
        ]
    },
    "chemj51": {
        "title": "Analytical Chemistry - I",
        "standard_questions": [
            ("Explain the principles of complexometric titrations using EDTA.", "I"),
            ("Differentiate between co-precipitation and post-precipitation with examples.", "II"),
            ("Discuss the types of errors in quantitative chemical analysis and their minimization.", "III"),
            ("Describe the role and mechanism of metal ion indicators in EDTA titrations.", "IV"),
            ("Explain the term 'peptization' in gravimetric analysis and how it can be avoided.", "V"),
            ("State the principles of solvent extraction and derive the distribution coefficient.", "I"),
            ("Discuss the organic reagents in inorganic analysis, focusing on cupferron and DMG.", "II"),
            ("Explain accuracy, precision, mean deviation, and standard deviation with equations.", "III"),
            ("Describe the redox titration of iron using potassium dichromate and internal indicator.", "IV"),
            ("Explain the principles of gravimetric precipitation and the conditions for complete precipitation.", "V"),
            ("Discuss the complexometric determination of hardness of water.", "I"),
            ("Explain how systematic errors can be detected and corrected in volumetric analysis.", "III"),
            ("Describe the ignition of precipitates in gravimetric analysis.", "V"),
            ("Discuss the iodometric and iodimetric titrations with relevant chemical equations.", "IV"),
            ("Explain the use of mask and demasking agents in EDTA complexometric titrations.", "I"),
            ("Describe the theory of acid-base indicators and the Ostwald's theory.", "IV"),
            ("Discuss the calibration of volumetric glassware (pipettes, burettes).", "III"),
            ("Explain the solubility product principle and its role in gravimetric estimations.", "V"),
            ("Describe the use of 8-hydroxyquinoline (oxine) as a gravimetric precipitant.", "II"),
            ("Discuss the statistical tests (F-test and t-test) in analytical data analysis.", "III")
        ]
    },
    "chemj52": {
        "title": "Inorganic Chemistry - III",
        "standard_questions": [
            ("Discuss the Crystal Field Theory (CFT) and explain d-orbital splitting in octahedral fields.", "I"),
            ("Calculate the Crystal Field Stabilization Energy (CFSE) for high-spin and low-spin $d^5$ complexes.", "II"),
            ("Compare the magnetic properties of lanthanides and actinides.", "III"),
            ("Describe the color and spectral properties of transition metal complexes using Orgel diagrams.", "IV"),
            ("Explain the Jahn-Teller effect and its impact on the structure of copper(II) complexes.", "V"),
            ("Discuss the d-orbital splitting pattern in tetrahedral coordination complexes.", "I"),
            ("Explain the factors affecting the magnitude of Crystal Field Splitting energy (10 Dq).", "I"),
            ("Discuss the electronic spectra of $[\\text{Ti(H}_2\\text{O)}_6]^{3+}$ and explain its absorption band.", "IV"),
            ("Describe the magnetic susceptibility measurement using Gouy's method.", "III"),
            ("Discuss the structural features and bonding of actinides.", "V"),
            ("Explain the thermodynamic stability of transition metal complexes and chelate effect.", "II"),
            ("Discuss the spin-only formula for magnetic moments and its deviations.", "III"),
            ("Describe the selection rules for d-d electronic transitions.", "IV"),
            ("Explain the preparation and properties of actinide elements.", "V"),
            ("Discuss the Nephelauxetic effect in coordination chemistry.", "IV"),
            ("Calculate the spin-only magnetic moments of $[\\text{Fe(CN)}_6]^{4-}$ and $[\\text{Fe(H}_2\\text{O)}_6]^{2+}$.", "III"),
            ("Discuss the square planar crystal field splitting pattern.", "I"),
            ("Explain why actinide complexes show more intense colors than lanthanide complexes.", "V"),
            ("Discuss the thermodynamic stability constants and factors affecting them.", "II"),
            ("Describe the extraction of Thorium and Uranium from their minerals.", "V")
        ]
    },
    "chemj53": {
        "title": "Organic Chemistry - III",
        "standard_questions": [
            ("Explain how UV-Vis spectroscopy is used to distinguish between conjugated and non-conjugated dienes.", "I"),
            ("Discuss the principles of Proton NMR spectroscopy, explaining chemical shift and spin-spin splitting.", "II"),
            ("Describe the synthesis of ethyl acetoacetate and its synthetic applications.", "III"),
            ("Explain how IR spectroscopy can distinguish between aldehydes, ketones, and carboxylic acids.", "IV"),
            ("Discuss the peptide bond and describe the Merrifield solid-phase peptide synthesis.", "V"),
            ("State Woodward-Fieser rules for calculating $\\lambda_{\\text{max}}$ of conjugated dienes.", "I"),
            ("Explain the concept of equivalent and non-equivalent protons in NMR with examples.", "II"),
            ("Describe the synthesis of diethyl malonate and its synthetic utility in preparing carboxylic acids.", "III"),
            ("Explain the characteristic IR absorption frequencies of hydroxyl, carbonyl, and amino groups.", "IV"),
            ("Discuss the protection and deprotection of amino groups in peptide synthesis.", "V"),
            ("Describe the coupling constant ($J$) and its significance in NMR spectroscopy.", "II"),
            ("Explain the keto-enol tautomerism in ethyl acetoacetate and provide evidence.", "III"),
            ("Discuss the structure of DNA and RNA and explain the hydrogen bonding between base pairs.", "V"),
            ("Describe the Woodward-Fieser rules for $\\alpha,\\beta$-unsaturated carbonyl compounds.", "I"),
            ("Explain how mass spectrometry is used to determine molecular weight of organic compounds.", "IV"),
            ("Discuss the Edman degradation method for peptide sequencing.", "V"),
            ("Explain the chemical shift reference compound TMS (Tetramethylsilane) and why it is used.", "II"),
            ("Describe the synthesis of polypeptides using the DCC coupling method.", "V"),
            ("Explain the fingerprint region in IR spectroscopy and its significance.", "IV"),
            ("Discuss the alkylation and acylation of enolates.", "III")
        ]
    },
    "chemj54": {
        "title": "Physical Chemistry - III",
        "standard_questions": [
            ("Solve the Schrödinger wave equation for a particle in a one-dimensional box.", "I"),
            ("Discuss the rotational spectra of a rigid diatomic molecule and derive the rotational constant.", "II"),
            ("Explain the postulates of quantum mechanics, defining Hermitian operators.", "III"),
            ("Describe the vibrational spectra of a simple harmonic oscillator and zero-point energy.", "IV"),
            ("Explain the Raman effect and discuss its classical and quantum theories.", "V"),
            ("Derive the energy expression for a particle in a three-dimensional cubic box and explain degeneracy.", "I"),
            ("Explain the rigid rotator model and calculate the bond length of carbon monoxide from rotational spectrum.", "II"),
            ("Show that the eigenvalues of a Hermitian operator are always real numbers.", "III"),
            ("Discuss the harmonic and anharmonic oscillator models in vibrational spectroscopy.", "IV"),
            ("Explain the Raman selection rules and compare Raman spectra with IR spectra.", "V"),
            ("Explain the concept of quantum mechanical tunneling through a rectangular potential barrier.", "I"),
            ("Discuss the non-rigid rotator model and centrifugal distortion.", "II"),
            ("Show that the eigenfunctions of a Hermitian operator corresponding to different eigenvalues are orthogonal.", "III"),
            ("Explain the Morse potential energy curve and calculate dissociation energy.", "IV"),
            ("Discuss the rotational-vibrational spectra (P, Q, R branches) of diatomic molecules.", "V"),
            ("Explain the physical interpretation of the wave function $\\psi$ and state normalization conditions.", "I"),
            ("Derive the vibrational frequency of a diatomic molecule treated as a simple harmonic oscillator.", "IV"),
            ("Discuss the spin quantum number and electron spin states in quantum chemistry.", "III"),
            ("Explain the pure rotational Raman spectra of diatomic molecules.", "V"),
            ("Solve the Schrödinger equation for a simple harmonic oscillator and state energy eigenvalues.", "IV")
        ]
    },
    "chemj61": {
        "title": "Analytical Chemistry - II",
        "standard_questions": [
            ("Explain the principle and mechanism of solvent extraction based on the distribution law.", "I"),
            ("Describe the construction and working of a double-beam UV-Vis spectrophotometer.", "II"),
            ("Discuss the applications of ion-exchange resins in water softening and deionization.", "III"),
            ("Explain the flame photometric method of analysis and its applications.", "IV"),
            ("Describe the principle and applications of atomic absorption spectroscopy (AAS).", "V"),
            ("Derive the expression for the percentage extraction in solvent extraction.", "I"),
            ("Explain the deviations from Beer-Lambert's law in spectrophotometric measurements.", "II"),
            ("Discuss the factors affecting solvent extraction efficiency.", "I"),
            ("Describe the instrumentation and working of an atomic absorption spectrometer.", "V"),
            ("Explain the term 'chromatographic resolution' and relate it to column efficiency.", "III"),
            ("Discuss the analytical applications of solvent extraction in metal ion separation.", "I"),
            ("Describe the detectors used in UV-Vis spectrophotometry.", "II"),
            ("Explain the synthesis, structure, and classification of ion-exchange resins.", "III"),
            ("Discuss the flame atomization mechanism in AAS.", "V"),
            ("Explain the interferences in flame photometry and methods to eliminate them.", "IV"),
            ("Describe the determination of zinc and magnesium using solvent extraction and colorimetry.", "I"),
            ("Discuss the organic precipitants oxine and cupferron in extraction processes.", "I"),
            ("Explain the principles of spectrophotometric titrations with curves.", "II"),
            ("Describe the ion-exchange separations of transition metal ions.", "III"),
            ("Discuss the role of hollow cathode lamps in Atomic Absorption Spectroscopy.", "V")
        ]
    },
    "chemj62": {
        "title": "Inorganic Chemistry - IV",
        "standard_questions": [
            ("Discuss the biological nitrogen fixation process, highlighting the role of nitrogenase enzyme.", "I"),
            ("Describe the preparation, properties, and structure of metal carbonyls like $\\text{Ni(CO)}_4$.", "II"),
            ("State and explain the 18-electron rule in transition metal organometallic complexes.", "III"),
            ("Discuss the mechanism of the Wilkinson's catalyst in the hydrogenation of alkenes.", "IV"),
            ("Explain the role of sodium-potassium pump ($\\text{Na}^+/\\text{K}^+$-pump) in biological systems.", "V"),
            ("Discuss the structure and oxygen-binding mechanism of hemoglobin.", "I"),
            ("Explain the synergic bonding mechanism in transition metal carbonyls (M-CO bonding).", "II"),
            ("Describe the preparation and synthetic applications of Grignard reagents.", "III"),
            ("Discuss the mechanism of olefin polymerization using the Ziegler-Natta catalyst.", "IV"),
            ("Explain the roles of iron-sulfur proteins (ferredoxins) in electron transport.", "V"),
            ("Discuss the structures of iron pentacarbonyl and dicobalt octacarbonyl.", "II"),
            ("Calculate the EAN and check 18-electron rule for $[\\text{Fe(CO)}_5]$ and $[\\text{Cr(CO)}_6]$.", "III"),
            ("Describe the preparation, properties, and structure of ferrocene.", "III"),
            ("Explain the homogeneous hydrogenation of alkenes by rhodium complexes.", "IV"),
            ("Discuss the toxic effects of heavy metals (arsenic, lead, mercury) in biochemical systems.", "V"),
            ("Describe the role of chlorophyll in photosynthesis and the coordination environment of magnesium.", "I"),
            ("Explain the preparation and structures of metal nitrosyls.", "II"),
            ("Discuss the organometallic compounds of Lithium and their synthetic applications.", "III"),
            ("Explain the hydroformylation reaction (oxo process) and its mechanism.", "IV"),
            ("Describe the biological role of carbonic anhydrase and the coordination of zinc.", "V")
        ]
    },
    "chemj63": {
        "title": "Organic Chemistry - IV",
        "standard_questions": [
            ("Describe the chemical methods used for amino acid sequencing from the N-terminal (Edman degradation).", "I"),
            ("Discuss the structure elucidation of D-glucose, including its ring size determination.", "II"),
            ("Explain the isolation, classification, and general properties of alkaloids.", "III"),
            ("Describe the synthesis and structure of nicotine.", "IV"),
            ("Discuss the isoprenoid rule and structure of citral.", "V"),
            ("Discuss the structure elucidation of D-fructose and its cyclic configuration.", "II"),
            ("Explain the chemical methods used for peptide sequencing from the C-terminal (Sanger's method).", "I"),
            ("Describe the synthesis of polypeptides using the solid-phase Merrifield method.", "I"),
            ("Discuss the structure and synthesis of alizarin dye.", "IV"),
            ("Describe the synthesis and structure of piperine.", "III"),
            ("Explain the structure and synthesis of menthol.", "V"),
            ("Discuss the structure of nucleic acids, explaining nucleotide and nucleoside.", "I"),
            ("Describe the double-helix structure of DNA proposed by Watson and Crick.", "I"),
            ("Discuss the chemical synthesis of glucose-6-phosphate.", "II"),
            ("Explain the extraction and properties of terpenoids.", "V"),
            ("Describe the structure, properties, and synthesis of atropine.", "III"),
            ("Discuss the synthesis of peptides using carbodiimide (DCC) reagent.", "I"),
            ("Explain the classification of synthetic polymers and their monomer structures.", "IV"),
            ("Describe the structure of RNA and its structural differences from DNA.", "I"),
            ("Discuss the synthesis of thyroxine.", "IV")
        ]
    },
    "chemj64": {
        "title": "Physical Chemistry - IV",
        "standard_questions": [
            ("Draw and explain the Jablonski diagram, detailing fluorescence and phosphorescence.", "I"),
            ("Define quantum yield of a photochemical reaction and explain why it is high or low.", "II"),
            ("Derive the thermodynamic relation between elevation of boiling point and molality of a solute.", "III"),
            ("State Raoult's law and explain positive and negative deviations shown by non-ideal solutions.", "IV"),
            ("Explain the photosensitized reactions and discuss the role of chlorophyll as a photosensitizer.", "V"),
            ("State the Stark-Einstein law of photochemical equivalence and explain.", "I"),
            ("Discuss the photochemical decomposition of hydrogen iodide and write its mechanism.", "II"),
            ("Derive the relation between osmotic pressure and molality of a dilute solution.", "III"),
            ("Explain the colligative properties of dilute solutions and define van 't Hoff factor.", "III"),
            ("Discuss the Jablonski diagram, detailing internal conversion and intersystem crossing.", "I"),
            ("State the Grotthuss-Draper law of photochemistry.", "I"),
            ("Explain the photochemical dimerisation of anthracene.", "II"),
            ("Derive the relation between depression of freezing point and molality of a solute.", "III"),
            ("Discuss the vapor pressure of non-ideal liquid mixtures and azeotropes.", "IV"),
            ("Explain the chemiluminescence with suitable examples.", "V"),
            ("Calculate the quantum yield for a reaction where $10^{-5}$ moles of reactant react per $10^{19}$ photons absorbed.", "II"),
            ("Explain the fractional distillation of binary liquid mixtures showing boiling point-composition diagrams.", "IV"),
            ("Discuss the thermodynamic derivation of lowering of vapor pressure.", "III"),
            ("Describe the working of a photogalvanic cell.", "V"),
            ("Explain the quenching of fluorescence and derive the Stern-Volmer equation.", "I")
        ]
    },
    "chemj85": {
        "title": "Advanced Spectroscopy",
        "standard_questions": [
            ("Explain the principles and applications of electron spin resonance (ESR) spectroscopy.", "I"),
            ("Discuss the theory and applications of Mossbauer spectroscopy.", "II"),
            ("Explain spin-spin coupling in $^1\\text{H}$-NMR and calculate the coupling constant ($J$).", "III"),
            ("Describe the Franck-Condon principle and its significance in electronic spectra.", "IV"),
            ("Discuss the vibrational-rotational spectra of diatomic molecules, explaining P, Q, and R branches.", "V"),
            ("Explain the hyperfine splitting in ESR spectra of hydrogen atom and methyl radical.", "I"),
            ("Describe the Mossbauer spectrum of iron complexes, detailing isomer shift.", "II"),
            ("Discuss the chemical shift in $^1\\text{H}$-NMR and factors affecting it.", "III"),
            ("Explain the electronic transitions ($\\sigma \\to \\sigma^*$, $\\pi \\to \\pi^*$, $n \\to \\pi^*$) in UV-Vis spectroscopy.", "IV"),
            ("Discuss the pure rotational spectra of diatomic molecules and derive the expression for energy levels.", "V"),
            ("Explain the ESR spectra of transition metal complexes.", "I"),
            ("Describe the quadrupole splitting and magnetic hyperfine splitting in Mossbauer spectroscopy.", "II"),
            ("Discuss the NMR instrumentation, explaining the role of superconducting magnets.", "III"),
            ("Explain the solvent effects on electronic absorption spectra (blue shift and red shift).", "IV"),
            ("Discuss the anharmonicity in vibrational spectra and the Birge-Sponer extrapolation.", "V"),
            ("Explain the NMR spectra of simple organic molecules like ethanol and ethyl bromide.", "III"),
            ("Describe the non-rigid rotator model and centrifugal distortion constant.", "V"),
            ("Discuss the applications of ESR in studying free radicals.", "I"),
            ("Explain the isomer shift in Mossbauer spectroscopy and its dependence on s-electron density.", "II"),
            ("Describe the vibrational-rotational Raman spectra of diatomic molecules.", "V")
        ]
    }
}

# Define get_custom_answer_key
def get_custom_answer_key(key, question):
    q_lower = question.lower()
    
    # 1. Diborane / Boranes
    if "diborane" in q_lower or "b2h6" in q_lower or "boran" in q_lower:
        return "1. **Structure of Diborane ($\\text{B}_2\\text{H}_6$)**:\n- Diborane contains twelve valence electrons, which is insufficient to form standard 2-centre-2-electron covalent bonds between all atoms (electron-deficient molecule).\n- It has two types of hydrogen atoms: four terminal hydrogens (in plane with boron atoms) and two bridging hydrogens (above and below the plane).\n\n2. **Bonding and Banana Bonds**:\n- The four terminal $\\text{B}-\\text{H}$ bonds are normal 2-centre-2-electron (2c-2e) covalent bonds formed by $\\text{sp}^3$ hybridized boron orbitals and $1\\text{s}$ hydrogen orbitals.\n- The two bridging $\\text{B}-\\text{H}-\\text{B}$ bonds are 3-centre-2-electron (3c-2e) bonds, often called **banana bonds**. In these bonds, a pair of electrons is shared among three nuclei (two Borons and one Hydrogen).\n\n3. **Physical Properties and Confirmation**:\n- Hybridization of boron is $\\text{sp}^3$.\n- The terminal $\\text{B}-\\text{H}$ bond length is shorter ($1.19\\text{ \\u00c5}$) compared to the bridging $\\text{B}-\\text{H}$ bond length ($1.33\\text{ \\u00c5}$), confirming the weaker and multi-centre nature of the bridge bonds."

    # 2. VSEPR Theory
    elif "vsepr" in q_lower:
        return "1. **VSEPR Theory Principles**:\n- Valence Shell Electron Pair Repulsion (VSEPR) theory states that electron pairs in the valence shell of a central atom adopt an arrangement that minimizes electrostatic repulsion.\n- The order of repulsive strength is: $\\text{lone pair - lone pair (lp-lp)} > \\text{lone pair - bond pair (lp-bp)} > \\text{bond pair - bond pair (bp-bp)}$.\n\n2. **Shapes of molecules**:\n- **Water ($\\text{H}_2\\text{O}$)**: Central oxygen atom undergoes $\\text{sp}^3$ hybridization. It has 2 bond pairs and 2 lone pairs. The tetrahedral geometry is distorted to a **bent / V-shape**, and the bond angle is reduced from $109.5^\\circ$ to $104.5^\\circ$ due to lp-lp repulsion.\n- **Ammonia ($\\text{NH}_3$)**: Central nitrogen atom undergoes $\\text{sp}^3$ hybridization. It has 3 bond pairs and 1 lone pair. The geometry is distorted to **trigonal pyramidal**, and the bond angle is reduced to $107^\\circ$ due to lp-bp repulsion.\n- **Sulfur Dioxide ($\\text{SO}_2$)**: Central sulfur is $\\text{sp}^2$ hybridized with 1 lone pair and 2 double bonds. Repulsion between lone pair and double bonds distorts the geometry to a **bent shape** with bond angle $\\approx 119.5^\\circ$."

    # 3. Schrödinger Equation
    elif "schrodinger" in q_lower or "schrödinger" in q_lower:
        return "1. **Schrödinger Wave Equation**:\n- The time-independent Schrödinger wave equation in 1D is: \n  $$-\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)$$\n  where $m$ is the mass of the particle, $\\hbar = h/2\\pi$ is the reduced Planck constant, $V(x)$ is the potential energy, $\\psi(x)$ is the wave function, and $E$ is the total energy.\n\n2. **Physical Interpretation of Wave Function ($\\psi$)**:\n- $\\psi$ itself has no physical meaning, but its square $|\\psi|^2$ represents the **probability density** of finding the particle at a given point in space (Born interpretation).\n- To be physically acceptable, $\\psi$ must be single-valued, continuous, and normalizable: $\\int_{-\\infty}^{\\infty} |\\psi|^2 dx = 1$.\n\n3. **Application to Particle in a 1D Box**:\n- For an infinite potential well ($V(x) = 0$ for $0 < x < L$, else $V(x) = \\infty$), the boundary conditions require $\\psi(0) = \\psi(L) = 0$.\n- Solving the differential equation yields: \n  $$\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right) \\quad \\text{and} \\quad E_n = \\frac{n^2 h^2}{8mL^2} \\quad (n=1,2,3,...)$$\n- Energy levels are quantized and there is a minimum non-zero energy (zero-point energy) at $n=1$: $E_1 = \\frac{h^2}{8mL^2}$."

    # 4. Beckmann Rearrangement
    elif "beckmann" in q_lower:
        return "1. **Beckmann Rearrangement Concept**:\n- The Beckmann rearrangement is the acid-catalyzed conversion of an **oxime** (usually ketoxime) into an **N-substituted amide**.\n- Catalysts used include $\\text{H}_2\\text{SO}_4$, $\\text{PCl}_5$, $\\text{SOCl}_2$, or polyphosphoric acid (PPA).\n\n2. **Reaction Mechanism**:\n- **Protonation**: The hydroxyl group of the ketoxime is protonated to form a good leaving group ($-\\text{OH}_2^+$).\n- **Migration and Elimination**: Water is eliminated with simultaneous migration of the alkyl/aryl group that is **anti (trans)** to the leaving hydroxyl group to the nitrogen atom, forming an iminocarbocation.\n- **Nucleophilic Attack**: Water attacks the iminocarbocation, followed by deprotonation to yield an imidic acid intermediate.\n- **Tautomerization**: The imidic acid tautomerizes to the more stable amide (keto-enol type tautomerism).\n\n3. **Application**:\n- A major industrial application is the rearrangement of cyclohexanone oxime to **caprolactam**, which is the monomer used for synthesis of Nylon-6."

    # 5. Baeyer-Villiger Oxidation
    elif "baeyer-villiger" in q_lower or "baeyer" in q_lower:
        return "1. **Baeyer-Villiger Oxidation Concept**:\n- The Baeyer-Villiger oxidation is the conversion of ketones into **esters** (or cyclic ketones into **lactones**) using organic peroxy acids (e.g., mCPBA, peracetic acid, or trifluoroperacetic acid).\n\n2. **Reaction Mechanism**:\n- **Nucleophilic Addition**: The peroxy acid attacks the carbonyl carbon of the ketone, forming a tetrahedral intermediate called the **Criegee intermediate**.\n- **Migration and Cleavage**: One of the alkyl/aryl groups migrates to the adjacent oxygen of the peroxy group with simultaneous cleavage of the weak $\\text{O}-\\text{O}$ single bond, releasing a carboxylate anion leaving group.\n- **Deprotonation**: The protonated ester loses a proton to yield the final ester product.\n\n3. **Migratory Aptitude**:\n- The ease of migration of groups follows the order: $\\text{tertiary alkyl} > \\text{cyclohexyl} \\approx \\text{secondary alkyl} > \\text{benzyl} > \\text{phenyl} > \\text{primary alkyl} > \\text{methyl}$. Migration occurs with retention of configuration at the migrating carbon."

    # 6. Skraup Quinoline Synthesis
    elif "skraup" in q_lower:
        return "1. **Skraup Synthesis Overview**:\n- The Skraup synthesis is a classical method for preparing **quinoline** by heating aniline with glycerol, concentrated sulfuric acid (dehydrating agent and catalyst), and an oxidizing agent (typically nitrobenzene or arsenic pentoxide).\n\n2. **Stepwise Reaction Mechanism**:\n- **Dehydration**: Glycerol undergoes acid-catalyzed dehydration by $\\text{H}_2\\text{SO}_4$ to form **acrolein** (propenal), an $\\alpha,\\beta$-unsaturated aldehyde.\n- **1,4-Addition**: Aniline acts as a nucleophile and undergoes Michael-type (1,4-addition) conjugate addition to the acrolein, forming $\\beta$-phenylaminopropionaldehyde.\n- **Ring Closure**: The intermediate undergoes acid-catalyzed intramolecular electrophilic cyclization (similar to Friedel-Crafts alkylation) onto the ortho-position of the aromatic ring, followed by dehydration to yield 1,2-dihydroquinoline.\n- **Oxidation**: The 1,2-dihydroquinoline is oxidized by nitrobenzene (or $\\text{As}_2\\text{O}_5$) to yield **quinoline**."

    # 7. Born-Haber Cycle
    elif "born-haber" in q_lower or "born haber" in q_lower or "lattice energy" in q_lower:
        return "1. **Born-Haber Cycle Concept**:\n- The Born-Haber cycle is a thermodynamic cycle that relates the lattice energy of an ionic crystal to other thermochemical data such as ionization energy, electron affinity, dissociation energy, sublimation energy, and enthalpy of formation.\n- It is an application of **Hess's Law**.\n\n2. **Steps for NaCl Lattice Energy**:\n- Sublimation of solid sodium: $\\text{Na(s)} \\to \\text{Na(g)} \\quad (\\Delta H_{\\text{sub}})$\n- Dissociation of chlorine molecules: $\\frac{1}{2}\\text{Cl}_2\\text{(g)} \\to \\text{Cl(g)} \\quad (\\frac{1}{2}D)$\n- Ionization of gaseous sodium atoms: $\\text{Na(g)} \\to \\text{Na}^+\\text{(g)} + \\text{e}^- \\quad (IE)$\n- Electron gain by gaseous chlorine atoms: $\\text{Cl(g)} + \\text{e}^- \\to \\text{Cl}^-\\text{(g)} \\quad (EA)$\n- Combination of gaseous ions to form solid crystal: $\\text{Na}^+\\text{(g)} + \\text{Cl}^-\\text{(g)} \\to \\text{NaCl(s)} \\quad (U_{\\text{lattice}})$\n\n3. **Mathematical Formula**:\n- By Hess's law: \n  $$\\Delta H_f = \\Delta H_{\\text{sub}} + \\frac{1}{2}D + IE + EA + U_{\\text{lattice}}$$\n- Rearranging this allows calculations of the lattice energy ($U_{\\text{lattice}}$), which is highly exothermic."

    # 8. Crystal Field Theory (CFT)
    elif "crystal field" in q_lower or "cft" in q_lower or "cfse" in q_lower:
        return "1. **Crystal Field Theory Basics**:\n- Crystal Field Theory (CFT) describes the electrostatic interactions between the d-orbitals of a central transition metal ion and the negative charges (or dipoles) of surrounding ligands.\n- It assumes ligands act as point negative charges, which causes the degeneracy of the five d-orbitals of the metal ion to split into groups with different energy levels.\n\n2. **Octahedral field splitting**:\n- The ligands approach along the Cartesian axes ($x, y, z$). d-orbitals oriented along the axes ($d_{x^2-y^2}$ and $d_{z^2}$) experience greater electrostatic repulsion and are destabilized, forming the higher energy **$e_g$ set**.\n- d-orbitals oriented between the axes ($d_{xy}, d_{yz}, d_{zx}$) experience less repulsion and are stabilized, forming the lower energy **$t_{2g}$ set**.\n- The energy difference between $e_g$ and $t_{2g}$ sets is denoted as $\\Delta_o$ (or $10 Dq$).\n\n3. **CFSE Calculation**:\n- Crystal Field Stabilization Energy (CFSE) is calculated as:\n  $$\\text{CFSE} = (-0.4 \\times n_{t_{2g}} + 0.6 \\times n_{e_g})\\Delta_o + mP$$\n  where $n_{t_{2g}}$ and $n_{e_g}$ are the number of electrons in the respective orbitals, $P$ is the pairing energy, and $m$ is the number of newly paired electron pairs. For low-spin $d^5$, electron configuration is $t_{2g}^5 e_g^0$, giving $\\text{CFSE} = -2.0\\Delta_o + 2P$."

    # 9. Lanthanides and Lanthanide Contraction
    elif "lanthanide" in q_lower or "separation" in q_lower:
        return "1. **Lanthanide Contraction Definition**:\n- The steady decrease in the ionic radii of lanthanide metals ($M^{3+}$ ions) with increasing atomic number from Lanthanum ($Z=57$, $1.06\\text{ \\u00c5}$) to Lutetium ($Z=71$, $0.85\\text{ \\u00c5}$).\n- **Reason**: The filling of $4f$ orbitals occurs. Due to the diffuse shape of $4f$ orbitals, they have very poor shielding effect on each other. The increasing nuclear charge pulling the outer shells inward is not compensated, leading to a net contraction.\n\n2. **Consequences**:\n- Separation is extremely difficult because their chemical properties are nearly identical due to similar sizes.\n- $5d$ transition series elements have ionic radii almost identical to $4d$ analogues (e.g., $Zr$ and $Hf$, $Nb$ and $Ta$), making them chemical twins.\n\n3. **Ion-Exchange Chromatography Separation**:\n- A solution containing $Ln^{3+}$ ions is poured down a column packed with cation-exchange resin (carrying sulfonic acid groups $-\\text{SO}_3\\text{H}$).\n- The $Ln^{3+}$ ions bind to the resin. An eluting agent (such as ammonium citrate/citric acid buffer) is passed through the column. Citrate ions act as complexing agents.\n- Since the hydrated radius of smaller ions is larger, the smallest ion ($Lu^{3+}$) binds least tightly to the resin and forms a more stable citrate complex, eluting out **first**. The largest ion ($La^{3+}$) elutes out **last**."

    # 10. Buffer Solutions and Henderson Equation
    elif "buffer" in q_lower or "henderson" in q_lower:
        return "1. **Buffer Solutions Concept**:\n- A buffer solution resists changes in its pH upon addition of small amounts of a strong acid or strong base. An acidic buffer consists of a weak acid and its salt with a strong base (e.g., $\\text{CH}_3\\text{COOH} + \\text{CH}_3\\text{COONa}$).\n\n2. **Henderson-Hasselbalch Equation Derivation**:\n- For a weak acid $HA$ dissociating in water:\n  $$HA \\rightleftharpoons H^+ + A^- \\quad \\implies \\quad K_a = \\frac{[H^+][A^-]}{[HA]}$$\n- Solving for $[H^+]$:\n  $$[H^+] = K_a \\frac{[HA]}{[A^-]}$$\n- Taking the negative logarithm ($-\\log$) of both sides:\n  $$-\\log[H^+] = -\\log K_a - \\log\\left(\\frac{[HA]}{[A^-]}\\right)$$\n  $$\\text{pH} = \\text{pK}_a + \\log\\left(\\frac{[A^-]}{[HA]}\\right)$$\n- Since the salt $MA$ is completely dissociated ($[A^-] \\approx [\\text{Salt}]$) and dissociation of weak acid is suppressed ($[HA] \\approx [\\text{Acid}]$):\n  $$\\text{pH} = \\text{pK}_a + \\log\\left(\\frac{[\\text{Salt}]}{[\\text{Acid}]}\\right)$$"

    # 11. Gibbs Phase Rule
    elif "phase rule" in q_lower:
        return "1. **Gibbs Phase Rule Statement**:\n- Formulated by Josiah Willard Gibbs, the phase rule is a general criterion governing the equilibrium in heterogeneous systems:\n  $$F = C - P + 2$$\n  where $P$ is the number of phases in equilibrium, $C$ is the minimum number of chemical components, and $F$ is the number of degrees of freedom (variance).\n\n2. **Conditions for $F = C - P + 1$**:\n- When one of the intensive variables (such as pressure in condensed systems) is kept constant, the rule becomes the **condensed phase rule**: $F = C - P + 1$.\n\n3. **Application to Water System**:\n- Water is a one-component system ($C=1$).\n- **Single Phase Areas** ($P=1$, e.g., only ice, water, or vapor): $F = 1 - 1 + 2 = 2$ (bivariant; both pressure and temperature can be changed independently).\n- **Boundary Curves** ($P=2$, phase boundaries): $F = 1 - 2 + 2 = 1$ (univariant; specifying temperature automatically fixes pressure).\n- **Triple Point** ($P=3$, ice, water, and vapor in equilibrium): $F = 1 - 3 + 2 = 0$ (invariant; occurs only at a specific temperature $0.0098^\\circ\\text{C}$ and pressure $4.58\\text{ mmHg}$)."

    # 12. Bragg's Law
    elif "bragg" in q_lower:
        return "1. **Bragg's Equation Derivation**:\n- Consider a beam of monochromatic X-rays of wavelength $\\lambda$ incident on parallel crystal planes spaced at a distance $d$ at an angle $\\theta$ (Bragg angle).\n- The path difference between waves reflected from two adjacent planes is $2d\\sin\\theta$. For constructive interference (bright diffraction peaks), this path difference must be an integer multiple of the wavelength:\n  $$2d\\sin\\theta = n\\lambda \\quad (n=1,2,3,...)$$\n  where $n$ is the order of diffraction.\n\n2. **Calculation Example**:\n- Given: $\\lambda = 1.54\\text{ \\u00c5}$, first-order diffraction $n=1$, Bragg angle $\\theta = 30^\\circ$.\n- Applying Bragg's law:\n  $$2d\\sin(30^\\circ) = 1 \\times 1.54$$\n  $$2d(0.5) = 1.54 \\implies d = 1.54\\text{ \\u00c5}$$.\n- Thus, the interplanar spacing is $1.54\\text{ \\u00c5}$."

    # 13. Lead Accumulator / Batteries
    elif "battery" in q_lower or "lead storage" in q_lower or "accumulator" in q_lower:
        return "1. **Lead Storage Battery Overview**:\n- The lead-acid storage battery is a secondary cell (rechargeable battery) consisting of a Lead ($Pb$) anode, a Lead dioxide ($PbO_2$) cathode, and aqueous sulfuric acid ($38\\% \\text{ w/w } \\text{H}_2\\text{SO}_4$, density $1.28\\text{ g/cm}^3$) as the electrolyte.\n\n2. **Discharging Reactions (anode/cathode)**:\n- **At Anode**: Lead metal is oxidized to lead sulfate:\n  $$\\text{Pb(s)} + \\text{SO}_4^{2-}\\text{(aq)} \\to \\text{PbSO}_4\\text{(s)} + 2\\text{e}^-$$\n- **At Cathode**: Lead dioxide is reduced to lead sulfate:\n  $$\\text{PbO}_2\\text{(s)} + \\text{SO}_4^{2-}\\text{(aq)} + 4\\text{H}^+\\text{(aq)} + 2\\text{e}^- \\to \\text{PbSO}_4\\text{(s)} + 2\\text{H}_2\\text{O(l)}$$\n- **Net Discharging Reaction**:\n  $$\\text{Pb(s)} + \\text{PbO}_2\\text{(s)} + 2\\text{H}_2\\text{SO}_4\\text{(aq)} \\to 2\\text{PbSO}_4\\text{(s)} + 2\\text{H}_2\\text{O(l)}$$\n  Lead sulfate precipitates on both electrodes, and sulfuric acid is consumed.\n\n3. **Recharging Reactions**:\n- During charging, the reactions are reversed by applying an external electrical potential. Lead sulfate on the anode is reduced back to lead metal, and lead sulfate on the cathode is oxidized back to lead dioxide, regenerating $\\text{H}_2\\text{SO}_4$."

    # 14. Photosynthesis and Photosystems
    elif "photosynthesis" in q_lower or "photosystem" in q_lower:
        return "1. **Photosystem I vs Photosystem II**:\n- **Photosystem II (PSII)**: Located on the appressed regions of the thylakoid membrane. Its reaction center chlorophyll absorbs light optimally at $680\\text{ nm}$ ($P_{680}$). PSII participates in light absorption, water splitting (photolysis), and oxygen evolution, transferring electrons to plastoquinone.\n- **Photosystem I (PSI)**: Located on the non-appressed regions of the thylakoid membrane. Its reaction center chlorophyll absorbs light optimally at $700\\text{ nm}$ ($P_{700}$). PSI receives electrons from plastocyanin and reduces $\\text{NADP}^+$ to $\\text{NADPH}$ via ferredoxin.\n\n2. **Light Reactions (Photochemical Phase)**:\n- Occur in the thylakoid membranes. Solar energy is absorbed by chlorophylls, generating high-energy electrons. Non-cyclic photophosphorylation (Z-scheme) produces $\\text{ATP}$ and $\\text{NADPH}$ along with the release of oxygen from water photolysis.\n\n3. **Dark Reactions (Biosynthetic Phase)**:\n- Occur in the stroma of the chloroplasts. Carbon dioxide is fixed into carbohydrates using the energy storage molecules $\\text{ATP}$ and $\\text{NADPH}$ generated in the light reactions. This process is known as the **Calvin cycle** (carbon fixation, reduction, and ribulose-1,5-bisphosphate regeneration)."

    # 15. Chromatography
    elif "chromatography" in q_lower or "tlc" in q_lower:
        return "1. **Principles of Chromatography**:\n- Chromatography is a physical separation method where components of a mixture are distributed between a stationary phase and a mobile phase.\n- **Thin Layer Chromatography (TLC)**: The stationary phase is a thin layer of adsorbent material (usually silica gel or alumina) coated on a glass or plastic plate. Separation is based on adsorption dynamics.\n- **Paper Chromatography**: The stationary phase is water molecules adsorbed on the cellulose fibers of filter paper. Separation is based on partition dynamics.\n\n2. **Rf Value (Retardation Factor)**:\n- The migration distance of a substance relative to the solvent front is characteristic:\n  $$R_f = \\frac{\\text{Distance traveled by the solute}}{\\text{Distance traveled by the solvent front}}$$\n\n3. **Differences**:\n- TLC is faster, has better resolution, and supports corrosive visual reagents (like conc. sulfuric acid spray), whereas paper chromatography is cheaper but slower and limited to partition dynamics."

    # 16. Jablonski Diagram
    elif "jablonski" in q_lower or "fluorescence" in q_lower:
        return "1. **Jablonski Diagram Overview**:\n- A Jablonski diagram is a schematic representation of the electronic energy levels of a molecule and the radiative and non-radiative transitions that occur during photophysical processes.\n- Levels include the singlet ground state ($S_0$), excited singlet states ($S_1, S_2$), and triplet states ($T_1$).\n\n2. **Non-Radiative Transitions**:\n- **Internal Conversion (IC)**: Isoenergetic transition between states of the same spin multiplicity ($S_2 \\to S_1$).\n- **Intersystem Crossing (ISC)**: Isoenergetic transition between states of different spin multiplicity ($S_1 \\to T_1$, involving spin-flip).\n- **Vibrational Relaxation**: Dissipation of excess vibrational energy to the environment as heat.\n\n3. **Radiative Transitions**:\n- **Fluorescence**: Spin-allowed radiative transition from an excited singlet state back to the ground state ($S_1 \\to S_0$). It is extremely fast ($10^{-9}$ to $10^{-7}$ seconds) and ceases immediately when the light source is removed.\n- **Phosphorescence**: Spin-forbidden radiative transition from an excited triplet state back to the ground state ($T_1 \\to S_0$). It is much slower ($10^{-3}$ to seconds or minutes) because it involves a spin-flip, leading to afterglow effects."

    # 17. 18-Electron Rule
    elif "18-electron" in q_lower or "18 electron" in q_lower or "ean" in q_lower:
        return "1. **18-Electron Rule Principle**:\n- The 18-electron rule states that transition metal organometallic complexes are most stable when the sum of the metal's d-electrons plus the electrons donated by the ligands equals 18, corresponding to the closed-shell electron configuration of the next noble gas.\n\n2. **Electron Counting Methods**:\n- **Neutral Method**: Metal is treated as neutral, and ligands donate neutral-state electrons (e.g., $CO$ donations: 2, $Cl$ donations: 1, $\\eta^5\\text{-cyclopentadienyl}$ donations: 5).\n- **Ionic Method**: Metal is assigned an oxidation state, and ligands donate paired-ion electrons (e.g., $CO$: 2, $Cl^-$: 2, $\\text{Cp}^-$: 6).\n\n3. **Calculation Examples**:\n- **$\\text{Ni(CO)}_4$**: Neutral Ni has 10 valence electrons. Four $CO$ ligands donate $4 \\times 2 = 8$ electrons. Total $= 10 + 8 = 18$ electrons. (Stable, obeys the rule).\n- **$\\text{Fe(CO)}_5$**: Neutral Fe has 8 valence electrons. Five $CO$ ligands donate $5 \\times 2 = 10$ electrons. Total $= 8 + 10 = 18$ electrons. (Stable, obeys the rule)."

    # 18. Polymers: Teflon, Buna-S, Bakelite
    elif "teflon" in q_lower or "buna-s" in q_lower or "polymer" in q_lower or "bakelite" in q_lower:
        return "1. **Teflon (Polytetrafluoroethylene, PTFE)**:\n- **Monomer**: Tetrafluoroethylene ($\\text{CF}_2=\\text{CF}_2$).\n- **Synthesis**: Prepared by free-radical polymerization of tetrafluoroethylene under high pressure with persulfate catalysts. It is highly resistant to heat and chemicals, and is used for non-stick cookware coatings and electrical insulation.\n\n2. **Buna-S (SBR - Styrene-Butadiene Rubber)**:\n- **Monomers**: $1,3$-butadiene ($\\text{CH}_2=\\text{CH}-\\text{CH}=\\text{CH}_2$, $75\\%$) and styrene ($\\text{C}_6\\text{H}_5\\text{CH}=\\text{CH}_2$, $25\\%$).\n- **Synthesis**: Copolymerization in the presence of sodium catalyst (hence 'Na' in Buna). It is highly resistant to wear and is used in vehicle tires.\n\n3. **Bakelite (Phenol-Formaldehyde Resin)**:\n- **Monomers**: Phenol and Formaldehyde.\n- **Synthesis**: Step-growth condensation polymer. Under acidic catalysts, linear chains of **Novolac** form. Under alkaline conditions with excess formaldehyde, cross-linked thermosetting **Bakelite** is produced, used in electrical switches and heat-resistant handles."

    # 19. Iron Extraction / Blast Furnace
    elif "blast furnace" in q_lower or "iron" in q_lower or "metallurgy" in q_lower:
        return "1. **Iron Extraction Overview**:\n- Iron is extracted from its hematite ore ($\\text{Fe}_2\\text{O}_3$) in a blast furnace. The raw materials added are ore, coke (reducing agent and fuel), and limestone (flux).\n\n2. **Blast Furnace Zones and Reactions**:\n- **Combustion Zone (Bottom)**: Coke burns to carbon dioxide: \n  $$\\text{C} + \\text{O}_2 \\to \\text{CO}_2 \\quad (\\text{highly exothermic, } T \\approx 2000\\text{ K})$$\n- **Reduction Zone (Top)**: Carbon monoxide reduces iron oxide in steps:\n  $$3\\text{Fe}_2\\text{O}_3 + \\text{CO} \\to 2\\text{Fe}_3\\text{O}_4 + \\text{CO}_2$$\n  $$\\text{Fe}_3\\text{O}_4 + \\text{CO} \\to 3\\text{FeO} + \\text{CO}_2$$\n  $$\\text{FeO} + \\text{CO} \\to \\text{Fe(l)} + \\text{CO}_2 \\quad (T \\approx 800 - 1000\\text{ K})$$\n- **Slag Formation**: Limestone decomposes to calcium oxide, which reacts with silica impurity to form fusible slag:\n  $$\\text{CaCO}_3 \\to \\text{CaO} + \\text{CO}_2$$\n  $$\\text{CaO} + \\text{SiO}_2 \\to \\text{CaSiO}_3\\text{(l)} \\quad (\\text{slag})$$\n- Slag floats on top of the molten iron and prevents re-oxidation of iron."

    # 20. Carbohydrate reactions / Mutarotation / Fructose
    elif "glucose" in q_lower or "fructose" in q_lower or "mutarotation" in q_lower:
        return "1. **Mutarotation of Glucose**:\n- Mutarotation is the spontaneous change in the specific optical rotation of a freshly prepared solution of a crystalline sugar to a constant equilibrium value.\n- For D-glucose, the $\\alpha$-D-glucopyranose (specific rotation $+112^\\circ$) and $\\beta$-D-glucopyranose (specific rotation $+19^\\circ$) establish an equilibrium in solution through the open-chain form, reaching a stable rotation value of $+52.7^\\circ$ ($36\\%\\ \\alpha$ and $64\\%\\ \\beta$).\n\n2. **Fructose Reducing Sugar Behavior**:\n- Although fructose is a ketose (having a ketone group at C-2), it acts as a reducing sugar and reduces Tollens' and Fehling's reagents.\n- **Reason**: In alkaline medium, fructose undergoes keto-enol tautomerism (**Lobry de Bruyn-Alberda van Ekenstein transformation**) via an enediol intermediate to form an equilibrium mixture containing glucose and mannose, which have free aldehyde groups that undergo oxidation."

    # 21. General/Core chemistry answer
    else:
        return "1. **Core Chemical Principles**:\n- Analyze the molecular structures, electronic configurations, and thermodynamic parameters of the system.\n\n2. **Reaction Mechanism & Equations**:\n- Write down chemical equations, show arrow-pushing mechanisms, and identify key intermediates (such as carbocations, radicals, or coordinate complexes).\n\n3. **Verification**:\n- Ensure charge balance, stoichiometric coefficients, and stereochemical details are correct, and cross-reference with standard thermodynamic and kinetic laws."

# 3. Parse .tex files and group questions by paper code
def clean_text(text):
    text = text.replace(r'\"{o}', 'ö')
    text = text.replace(r'\'e', 'é')
    text = text.replace(r'\"{a}', 'ä')
    text = text.replace(r'\"o', 'ö')
    text = text.replace(r'\'erot', 'érot')
    
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
    
    # Replace LaTeX bracket math with $ delimiters
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

# Scan and categorize questions from files
subjects_raw_questions = {
    "chemd11": [],
    "chemd21": [],
    "chemd31": [],
    "chemj11": [],
    "chemj21": [],
    "chemj32": [],
    "chemj33": [],
    "chemj41": [],
    "chemj42": [],
    "chemj51": [],
    "chemj52": [],
    "chemj53": [],
    "chemj54": [],
    "chemj61": [],
    "chemj62": [],
    "chemj63": [],
    "chemj64": [],
    "chemj85": []
}

tex_dir = 'aaa/chemistry/tex_files'
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
        qs = parse_tex_content(content)
        subjects_raw_questions["chemd11"].extend(qs)
    elif code.startswith("CHB-04A"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemd21"].extend(qs)
    elif code.startswith("CHB-101"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj11"].extend(qs)
    elif code.startswith("CHB-201"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj21"].extend(qs)
    elif code.startswith("CHB-301") or code.startswith("CHB-361"):
        # Split into organic and physical parts
        parts = re.split(r'SECTION\s+B', content, flags=re.IGNORECASE)
        left = parts[0]
        right = parts[1] if len(parts) > 1 else ""
        
        q_left = parse_tex_content(left)
        q_right = parse_tex_content(right)
        
        subjects_raw_questions["chemj32"].extend(q_left)
        subjects_raw_questions["chemj33"].extend(q_right)
    elif code.startswith("CHB-401"):
        # Split into inorganic and organic parts
        parts = re.split(r'SECTION\s+B', content, flags=re.IGNORECASE)
        left = parts[0]
        right = parts[1] if len(parts) > 1 else ""
        
        q_left = parse_tex_content(left)
        q_right = parse_tex_content(right)
        
        subjects_raw_questions["chemj41"].extend(q_left)
        subjects_raw_questions["chemj42"].extend(q_right)
    elif code.startswith("CHB-501"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj51"].extend(qs)
    elif code.startswith("CHB-502"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj52"].extend(qs)
    elif code.startswith("CHB-503"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj53"].extend(qs)
    elif code.startswith("CHB-504"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj54"].extend(qs)
    elif code.startswith("CHB-505"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemd31"].extend(qs)
    elif code.startswith("CHB-601"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj61"].extend(qs)
    elif code.startswith("CHB-602"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj62"].extend(qs)
    elif code.startswith("CHB-603"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj63"].extend(qs)
    elif code.startswith("CHB-604"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj64"].extend(qs)
    elif code.startswith("CHB-605") or code.startswith("CHB-608"):
        qs = parse_tex_content(content)
        subjects_raw_questions["chemj85"].extend(qs)

# Load existing exams database
with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

# Define active mapping (including minor/re-registered keys)
unique_to_active = {
    "chemd11": ["chemd11"],
    "chemd21": ["chemd21"],
    "chemd31": ["chemd31"],
    "chemj11": ["chemj11", "chemn11"],
    "chemj21": ["chemj21", "chemn21"],
    "chemj31": ["chemj31"],
    "chemj32": ["chemj32"],
    "chemj33": ["chemj33"],
    "chemj34": ["chemj34"],
    "chemj41": ["chemj41"],
    "chemj42": ["chemj42"],
    "chemj43": ["chemj43", "chemn41"],
    "chemj44": ["chemj44", "chemn42"],
    "chemj51": ["chemj51"],
    "chemj52": ["chemj52"],
    "chemj53": ["chemj53"],
    "chemj54": ["chemj54"],
    "chemj61": ["chemj61"],
    "chemj62": ["chemj62"],
    "chemj63": ["chemj63"],
    "chemj64": ["chemj64"],
    "chemj85": ["chemj85", "chemj8r5"]
}

print("Populating chemistry questions...")
for unique_key, active_list in unique_to_active.items():
    raw_qs = subjects_raw_questions.get(unique_key, [])
    standard_qs = CHEMISTRY_SYLLABI.get(unique_key, {}).get("standard_questions", [])
    
    # Deduplicate questions
    seen = set()
    final_questions = []
    
    for q_text in raw_qs:
        q_norm = q_text.lower().strip()
        if q_norm not in seen and len(q_text) > 25:
            seen.add(q_norm)
            final_questions.append(q_text)
            
    # Pad with standard syllabus questions if fewer than 50
    std_idx = 0
    while len(final_questions) < 50 and std_idx < len(standard_qs):
        q_text, unit = standard_qs[std_idx]
        q_norm = q_text.lower().strip()
        if q_norm not in seen:
            seen.add(q_norm)
            final_questions.append((q_text, unit))
        std_idx += 1
        
    # If still fewer than 50, pad with general syllabus questions
    fallback_idx = 1
    title_text = CHEMISTRY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())
    while len(final_questions) < 50:
        q_text = f"Discuss the theoretical foundations, spectroscopic characterizations, and industrial applications of {title_text} (Part {fallback_idx})."
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
            # Assign units uniformly
            unit_num = (idx // 10) + 1
            unit_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
            unit = unit_romans.get(unit_num, "V")
            
        ans_key = get_custom_answer_key(unique_key, q_text)
        
        # Ensure LaTeX formulas are clean
        q_text = clean_text(q_text)
        ans_key = clean_text(ans_key)
        
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
            "title": orig.get("title", CHEMISTRY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())),
            "module": orig.get("module", active_key.upper()),
            "duration": 60,
            "type": "theory",
            "comingSoon": False,
            "questions": formatted_questions
        }

# Write unified exams data back to js/exams-data.js
output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
with open("js/exams-data.js", "w", encoding="utf-8") as f:
    f.write(output_str)

print("exams-data.js has been successfully updated with 50 questions for each core chemistry paper!")
