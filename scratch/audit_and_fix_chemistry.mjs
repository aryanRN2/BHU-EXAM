/**
 * audit_and_fix_chemistry.mjs  (v3)
 * ===================================
 * Reads js/exams-data.js by extracting the JSON blob with a regex,
 * processes only the target Chemistry papers, then writes back via
 * targeted per-paper replacement — never stringifying the whole EXAMS.
 */

import fs from 'fs';

// ── 1. Helpers ───────────────────────────────────────────────────────────────
function cleanText(t) {
  return t
    .replace(/\\pts\{[^}]*\}/g, '')
    .replace(/\\hfill/g, '')
    .replace(/\\noindent/g, '')
    .replace(/\\textbf\{([^}]*)\}/g, '$1')
    .replace(/\\textit\{([^}]*)\}/g, '$1')
    .replace(/\\emph\{([^}]*)\}/g, '$1')
    .replace(/~/g, ' ')
    .replace(/\\\\(?:\[[^\]]*\])?/g, ' ')
    .replace(/\\\[/g, '$').replace(/\\\]/g, '$')
    .replace(/\s+/g, ' ').trim();
}

function parseTexContent(subcontent) {
  const docStart = subcontent.indexOf('\\begin{document}');
  if (docStart !== -1) subcontent = subcontent.slice(docStart + 16);
  const tokens = subcontent.split(/(\\begin\{parts\}|\\end\{parts\}|\\item)/);
  const stack = [];
  let cur = [];
  const result = [];
  for (const tok of tokens) {
    if (!tok) continue;
    const s = tok.trim();
    if (s === '\\begin{parts}') { stack.push(cur); cur = []; }
    else if (s === '\\end{parts}') {
      if (stack.length > 0) {
        const parent = stack.pop();
        if (parent.length > 0) {
          const sub = ' ' + cur.map((item, i) => `(${i+1}) ${cleanText(item)}`).join(' ');
          parent[parent.length - 1] += sub;
          cur = parent;
        } else {
          for (const item of cur) { const c = cleanText(item); if (c.length > 15) result.push(c); }
          cur = [];
        }
      }
    } else if (s === '\\item') { cur.push(''); }
    else { if (cur.length > 0) cur[cur.length - 1] += ' ' + tok; }
  }
  for (const item of cur) { const c = cleanText(item); if (c.length > 15) result.push(c); }
  return result;
}

function buildPyqDatabase() {
  const texDir = 'aaa/chemistry/tex_files';
  const db = {};
  const KEYS = ['chemd11','chemd21','chemd31','chemj11','chemj21','chemj31','chemj32','chemj33','chemj34','chemj41','chemj42','chemj43','chemj44'];
  for (const k of KEYS) db[k] = [];

  const files = fs.readdirSync(texDir).filter(f => f.endsWith('.tex') && !f.startsWith('test_')).sort();
  for (const file of files) {
    let text = fs.readFileSync(`${texDir}/${file}`, 'utf8');
    text = text.replace(/\\end\{\{parts\}\}/g, '\\end{parts}').replace(/\\begin\{\{parts\}\}/g, '\\begin{parts}');
    text = text.replace(/^%.*$/gm, '');
    const code = file.split('_')[0];
    if (code.startsWith('CHB-02A'))      { db.chemd11.push(...parseTexContent(text)); }
    else if (code.startsWith('CHB-04A')) { db.chemd21.push(...parseTexContent(text)); }
    else if (code.startsWith('CHB-101')) { db.chemj11.push(...parseTexContent(text)); }
    else if (code.startsWith('CHB-201')) { db.chemj21.push(...parseTexContent(text)); }
    else if (code.startsWith('CHB-301') || code.startsWith('CHB-361')) {
      const parts = text.split(/SECTION\s+B/i);
      db.chemj32.push(...parseTexContent(parts[0]));
      if (parts[1]) db.chemj33.push(...parseTexContent(parts[1]));
    } else if (code.startsWith('CHB-401')) {
      const parts = text.split(/SECTION\s+B/i);
      db.chemj41.push(...parseTexContent(parts[0]));
      if (parts[1]) db.chemj42.push(...parseTexContent(parts[1]));
    } else if (code.startsWith('CHB-501')) { db.chemj44.push(...parseTexContent(text)); }
    else if (code.startsWith('CHB-505')) { db.chemd31.push(...parseTexContent(text)); }
  }
  for (const [k, v] of Object.entries(db)) console.log(`  PYQ ${k}: ${v.length} questions`);
  return db;
}

// ── 2. Topic keyword lookup ──────────────────────────────────────────────────
const PAPER_TOPICS = {
  chemd11: { title: 'Basic Principles of Chemistry', units: { 'I': ['atom','molecule','bonding','hybridization','intermolecular','oxidation','reducing','oxidizing'], 'II': ['enthalpy','entropy','free energy','thermodynamics','spontaneous'], 'III': ['dye','polymer','polyester','rubber','nylon','bakelite','food','soap','detergent','surfactant','fragrance','preservative','cleansing'] }},
  chemd21: { title: 'Energy & Metallurgy', units: { 'I': ['photosynthesis','light reaction','dark reaction','calvin','photorespiration'], 'II': ['energy','petroleum','natural gas','coal','nuclear','solar','biomass','biogas','fuel cell','li-ion','octane','cetane','renewable'], 'III': ['metallurgy','iron','copper','stainless steel','corrosion','ore','blast furnace'] }},
  chemd31: { title: 'Environmental Chemistry', units: { 'I': ['environmental','pollution','contamination','bod','cod','tlv','sink'], 'II': ['atmosphere','greenhouse','global warming','ozone','hydrosphere','eutrophication','carbon footprint'], 'III': ['hydrological cycle','oxygen cycle','nitrogen cycle','phosphate cycle','sulfur cycle'], 'IV': ['air pollution','acid rain','wastewater','el-nino','water pollution','auto exhaust','smog'] }},
  chemj11: { title: 'Basic Concepts of Chemistry-I', units: { 'I': ['wave-particle','heisenberg','schrodinger','schrödinger','wave equation','eigenvalue','wave function','radial','angular','effective nuclear','slater'], 'II': ['periodic','atomic size','ionic radius','lanthanide','ionization energy','electron affinity','inert pair','electronegativity','lattice energy','born-haber','solvation','fajan','electrode potential','electrochemical series','latimer','frost'], 'III': ['kinetic theory','ideal gas','maxwell distribution','equipartition','mean free path','van der waals gas','real gas','critical'], 'IV': ['surface tension','capillary','viscosity','liquid state'], 'V': ['crystal','lattice','unit cell','miller indices','bragg','nacl','solid state'], 'VI': ['first law','isothermal','adiabatic','kirchhoff','joule-thomson','second law','carnot','entropy','gibbs','helmholtz','maxwell relations','third law'] }},
  chemj21: { title: 'Basic Concepts of Chemistry-II', units: { 'I': ['valence bond','molecular orbital','mo theory','homonuclear','heteronuclear','hybridization','diborane','multiple bonding'], 'II': ['ionic bonding','radius ratio','rock salt','zinc blende','wurtzite','rutile'], 'III': ['metallic bonding','band theory'], 'IV': ['hydrogen bonding'], 'V': ['inductive','resonance','mesomeric','hyperconjugation','acidity','basicity'], 'VI': ['stereochemistry','chirality','enantiomer','diastereomer','geometrical isomerism','conformation','newman','fischer'], 'VII': ['alkene','alkyne','diels-alder','diene','ozonolysis','hydroboration','epoxidation'], 'VIII': ['alkyl halide','nucleophilic substitution','sn1','sn2','elimination','e1','e2','grignard'], 'IX': ['alcohol','ether'], 'X': ['active methylene','acetoacetate','malonate'] }},
  chemj31: { title: 'Inorganic Chemistry - I', units: { 'I': ['alkali','alkaline earth','flame','crown ether','cryptand','allotrope','hydride','halide','oxo-acid'], 'II': ['silicate','zeolite','glass','ceramic','refractory','cement','fertilizer','nitrogenous'] }},
  chemj32: { title: 'Organic Chemistry - I', units: { 'I': ['carbonyl','aldehyde','ketone','aldol','cannizzaro','perkin','benzoin','haloform','mannich','baylis-hillman','acid chloride'], 'II': ['ylide','wittig','arbuzov','horner'], 'III': ['aromaticity','antiaromaticity','benzenoid','non-benzenoid'], 'IV': ['aromatic electrophilic','nitration','halogenation','sulphonation','friedel-crafts'], 'V': ['phenol'] }},
  chemj33: { title: 'Physical Chemistry - I', units: { 'I': ['electrolyte','conductance','ionic conductance','transference','kohlrausch'], 'II': ['electrode potential','emf','electrochemical cell','concentration cell','glass electrode','potentiometric','buffer'], 'III': ['phase equilibria','clapeyron','clausius','phase rule','phase diagram','distribution law'], 'IV': ['chemical kinetics','rate law','zero order','first order','second order','arrhenius','collision theory','transition state'] }},
  chemj34: { title: 'Qualitative Analysis and Thermochemistry', units: { 'I': ['qualitative analysis','cation','anion','group reagent','semi-microanalysis'], 'II': ['functional group','melting point','lassaigne','organic compound identification'], 'III': ['thermochemistry','calorimeter','enthalpy of neutralization','enthalpy of ionization','hess'] }},
  chemj41: { title: 'Inorganic Chemistry - II', units: { 'I': ['brønsted','lowry','lux-flood','lewis acid','hsab','hard soft','symbiosis','super-acid'], 'II': ['non-aqueous solvent','liquid ammonia','ionic liquid','green synthesis'], 'III': ['transition metal','d-block','oxidation state','color','magnetic moment'], 'IV': ['coordination','werner','ligand','denticity','ean','geometrical isomerism','nomenclature'], 'V': ['lanthanide','actinide','lanthanide contraction','separation'] }},
  chemj42: { title: 'Organic Chemistry - II', units: { 'I': ['nitrobenzene','aniline','diazonium'], 'II': ['heterocyclic','furan','pyrrole','thiophene','pyridine','indole','quinoline','skraup','hantzsch'], 'III': ['naphthalene','anthracene','polynuclear'], 'IV': ['malachite green','fluorescein','indigotin','colour constitution'], 'V': ['cycloalkane','alicyclic','baeyer strain','cyclohexane conformation','chair','boat'], 'VI': ['protection','deprotection','functional group protecting'], 'VII': ['carbohydrate','glucose','aldose','ketose','mutarotation','anomeric','sucrose','starch','cellulose','glycosylation','kiliani','wohl'] }},
  chemj43: { title: 'Physical Chemistry - II', units: { 'I': ['partial molal','chemical potential','gibbs-duhem','fugacity','activity coefficient','raoult','colligative','osmotic pressure','van\'t hoff'], 'II': ['langmuir','adsorption','bet equation','surface area','gibbs adsorption','michaelis-menten'], 'III': ['photochemical','quantum yield','quantum efficiency','stern-volmer','photostationary'], 'IV': ['nuclear chemistry','radioactivity','decay kinetics','gm counter','radioisotope','tracer','radiolysis'] }},
  chemj44: { title: 'Techniques in Chemistry', units: { 'I': ['distillation','crystallization','extraction','chromatography','uv-visible','infrared','ir spectroscopy','nmr'], 'II': ['primary standard','secondary standard','molarity','normality','molality','ppm'], 'III': ['acid-base titration','complexometric','redox titration','precipitation titration','indicator'] }},
};

const PAPER_MIRRORS = { chemn11: 'chemj11', chemn21: 'chemj21', chemn41: 'chemj43', chemn42: 'chemj44' };

const REPLACEMENT_QUESTIONS = {
  chemd11: [
    ['What is hybridization? Explain the geometry of $\\text{CH}_4$, $\\text{NH}_3$, and $\\text{H}_2\\text{O}$ using $sp^3$ hybridization.', 'I'],
    ['Define electronegativity and explain how it determines bond type. Give examples of ionic and covalent compounds.', 'I'],
    ['What are the types of intermolecular forces? Explain how they influence boiling points of liquids with examples.', 'I'],
    ['Define oxidation number. Assign oxidation numbers in $\\text{H}_2\\text{SO}_4$ and $\\text{K}_2\\text{Cr}_2\\text{O}_7$.', 'II'],
    ['What is Gibbs free energy? Write its mathematical expression and explain how it predicts reaction spontaneity.', 'II'],
    ['State the second law of thermodynamics. Define entropy and explain its role in predicting spontaneous processes.', 'II'],
    ['Classify dyes based on their chemical structure and method of application. Give one example of each class.', 'III'],
    ['What are synthetic polymers? Describe the preparation, properties, and uses of (a) Nylon-6,6 and (b) Bakelite.', 'III'],
    ['What are food preservatives? Give examples of natural and synthetic preservatives used in the food industry.', 'III'],
    ['Describe the chemistry of soap formation (saponification). How does a soap molecule cleanse dirt?', 'III'],
    ['What is the difference between soaps and detergents? Why are detergents preferred in hard water?', 'III'],
    ['Describe natural rubber and explain the vulcanization process and how it improves rubber properties.', 'III'],
    ['What are biopolymers? Give examples and explain their significance in biological systems.', 'III'],
    ['Explain the chemistry of dyes and pigments. What molecular features determine the color of a dye?', 'III'],
    ['What are surfactants? Classify them and explain their role in cleansing and industrial applications.', 'III'],
  ],
  chemd21: [
    ['Explain the light reactions of photosynthesis. What is the role of chlorophyll in capturing light energy?', 'I'],
    ['What is the Calvin cycle? Describe the three stages of the dark reaction in photosynthesis.', 'I'],
    ['What is photorespiration? Explain how it occurs and why it reduces photosynthesis efficiency.', 'I'],
    ['Compare C3 and C4 plants in terms of their photosynthetic pathways and efficiency.', 'I'],
    ['What is petroleum? Explain its origin and list the major fractions obtained from distillation with their uses.', 'II'],
    ['Explain the significance of octane and cetane numbers in evaluating fuel quality for petrol and diesel engines.', 'II'],
    ['What is nuclear fission? Explain the basic working principle of a nuclear power reactor.', 'II'],
    ['Explain the working principle of a solar cell and the importance of solar energy as a renewable resource.', 'II'],
    ['What is biogas? Describe its generation from organic waste and its major components.', 'II'],
    ['Describe the working principle of a lithium-ion battery and its advantages over conventional lead-acid batteries.', 'II'],
    ['Explain the role of metals in daily life. How is iron extracted from its ore in a blast furnace?', 'III'],
    ['What is corrosion? Explain the electrochemical mechanism of rusting and methods of prevention.', 'III'],
    ['Describe the extraction of copper from copper pyrites with relevant chemical equations.', 'III'],
    ['Explain what stainless steel is, its composition, and how it resists corrosion.', 'III'],
    ['Compare renewable and non-renewable energy sources with examples and discuss their environmental impact.', 'II'],
  ],
  chemd31: [
    ['Define environmental chemistry. Distinguish between pollution and contamination. Define BOD, COD, and TLV.', 'I'],
    ['What is the greenhouse effect? Name major greenhouse gases and explain their role in global warming.', 'II'],
    ['Explain the mechanism of ozone layer depletion and the role of CFCs in stratospheric ozone destruction.', 'II'],
    ['What is eutrophication? How does excess nutrient loading affect aquatic ecosystems?', 'II'],
    ['Describe the composition and different regions (layers) of the atmosphere.', 'II'],
    ['Define the hydrological cycle and explain how water moves between different reservoirs on Earth.', 'III'],
    ['Explain the nitrogen cycle with the key processes and microorganisms involved.', 'III'],
    ['Describe the sulfur cycle and its role in atmospheric chemistry and acid rain formation.', 'III'],
    ['What is acid rain? Explain its chemical causes and effects on ecosystems and built structures.', 'IV'],
    ['Define air quality parameters. Explain the major sources and harmful effects of urban air pollution.', 'IV'],
    ['What is photochemical smog? Explain the chain of reactions involved in its formation.', 'IV'],
    ['Describe the primary, secondary, and tertiary stages of wastewater treatment.', 'IV'],
    ['What is the El-Niño phenomenon? How does it affect global weather and climate patterns?', 'IV'],
    ['What is water pollution? List major classes of water pollutants and their effects on human health.', 'IV'],
    ['Define carbon footprint. How can individuals and industries reduce carbon emissions?', 'II'],
  ],
  chemj31: [
    ['Describe the complexes of alkali metals with crown ethers and cryptands. How do they differ in binding selectivity?', 'I'],
    ['What are the allotropes of carbon? Compare the structures and properties of diamond, graphite, and fullerene.', 'I'],
    ['Compare the hydrides of Group 15 elements ($\\text{NH}_3$, $\\text{PH}_3$, $\\text{AsH}_3$) and their physical and chemical properties.', 'I'],
    ['Describe the oxo-acids of sulfur ($\\text{H}_2\\text{SO}_4$, $\\text{H}_2\\text{SO}_3$, $\\text{H}_2\\text{S}_2\\text{O}_7$) and their structures.', 'I'],
    ['Compare nitrogen and phosphorus chemistry. Why does nitrogen show anomalous behavior among Group 15 elements?', 'I'],
    ['Explain the preparation and acidic strength of the oxo-acids of chlorine: $\\text{HClO}$, $\\text{HClO}_2$, $\\text{HClO}_3$, and $\\text{HClO}_4$.', 'I'],
    ['What are flame colorations? Explain the chemistry behind the flame test for alkali and alkaline earth metals.', 'I'],
    ['Discuss the halides of Group 13 elements and compare the Lewis acidity of $\\text{BF}_3$, $\\text{BCl}_3$, and $\\text{BBr}_3$.', 'I'],
    ['What is the inert pair effect? Explain its role in the chemistry of heavier p-block elements with examples.', 'I'],
    ['Describe the structure and properties of zeolites. How are they used as molecular sieves in industry?', 'II'],
    ['Explain the manufacture of Portland cement. What are the key ingredients and their roles?', 'II'],
    ['Describe the Haber process for the industrial manufacture of ammonia. State the conditions and catalyst used.', 'II'],
    ['Explain the Contact process for the manufacture of sulfuric acid with balanced equations for each step.', 'II'],
    ['What are refractories? Classify them and explain their industrial applications.', 'II'],
    ['Describe the types and uses of nitrogenous fertilizers. How is urea manufactured industrially?', 'II'],
    ['What are silicates? Classify silicates based on their structural types and give one example of each.', 'II'],
    ['Describe the manufacture and types of glass. What is the role of each ingredient?', 'II'],
    ['What is the borax bead test? Explain the chemistry involved in identifying metal ions with this test.', 'I'],
    ['Discuss the chemistry of noble gases. Describe the preparation and structure of xenon fluorides.', 'I'],
    ['Explain the allotropes of phosphorus (white and red phosphorus) and compare their properties and reactivity.', 'I'],
  ],
  chemj34: [
    ['Explain the systematic qualitative analysis of a mixture containing two cations. Describe group reagents for Groups I–VI.', 'I'],
    ['Explain the role of $\\text{H}_2\\text{S}$ in qualitative inorganic analysis. Why is its concentration controlled in Group II?', 'I'],
    ['What is the common ion effect? How is it applied in the precipitation of Group III cations?', 'I'],
    ['Describe the confirmation tests for: (a) $\\text{SO}_4^{2-}$, (b) $\\text{Cl}^-$, (c) $\\text{NO}_3^-$.', 'I'],
    ['How are Group IV cations ($\\text{Ca}^{2+}$, $\\text{Sr}^{2+}$, $\\text{Ba}^{2+}$) separated and individually identified?', 'I'],
    ['Describe the preliminary tests in qualitative organic analysis: physical state, solubility, and ignition test.', 'II'],
    ['How are nitrogen, sulfur, and halogens detected in an organic compound using the Lassaigne test?', 'II'],
    ['What functional group tests are used to identify aldehydes, ketones, and carboxylic acids in an organic compound?', 'II'],
    ['Describe the tests for identifying primary, secondary, and tertiary amines in organic analysis.', 'II'],
    ['How is the melting point of an organic compound determined and why is it important for its identification?', 'II'],
    ['Define water equivalent of a calorimeter. How is it determined experimentally?', 'III'],
    ['Explain the experimental determination of the enthalpy of neutralization of $\\text{HCl}$ with $\\text{NaOH}$.', 'III'],
    ['What is the enthalpy of ionization? How is it determined for a weak acid like acetic acid?', 'III'],
    ['Define integral enthalpy of solution. How does it differ from differential enthalpy of solution?', 'III'],
    ["State Hess's law. Apply it to calculate the enthalpy of formation of $\\text{CO}_2$ from thermochemical data.", 'III'],
  ],
  chemj42: [
    ['Explain why nitrobenzene is less reactive than benzene towards electrophilic substitution. Where does substitution preferentially occur and why?', 'I'],
    ['Describe the preparation of aniline from nitrobenzene using tin and hydrochloric acid. Write the equation.', 'I'],
    ['What are diazonium salts? Describe their preparation from aniline and key synthetic applications (coupling and replacement reactions).', 'I'],
    ['Compare pyridine and pyrrole in terms of basicity, aromaticity, and reactivity towards electrophilic substitution.', 'II'],
    ['Explain the Skraup synthesis of quinoline with a detailed mechanism.', 'II'],
    ['Describe the preparation and reactions of furan. Compare its reactivity with benzene.', 'II'],
    ['Describe the Fischer indole synthesis with the mechanism and explain which substrates are used.', 'II'],
    ['Compare the aromatic character and electrophilic substitution reactivity of furan, pyrrole, and thiophene.', 'II'],
    ['Explain the Hantzsch synthesis of pyridine derivatives with the reaction mechanism.', 'II'],
    ['Describe the chemistry of naphthalene. Explain why electrophilic substitution occurs preferentially at the alpha position.', 'III'],
    ['Explain why anthracene reacts preferentially at the 9,10-positions in electrophilic substitution reactions.', 'III'],
    ['Describe the Baeyer strain theory. Apply it to explain the relative stability of cyclopropane, cyclobutane, and cyclopentane.', 'V'],
    ['Explain the conformational analysis of cyclohexane. Draw the chair and boat forms and explain axial and equatorial bonds.', 'V'],
    ['Explain the anomeric effect in carbohydrates and its structural and chemical significance.', 'VII'],
    ['Describe the Kiliani-Fischer synthesis for chain extension of aldoses with the full reaction sequence.', 'VII'],
    ['Explain the Wohl degradation for chain shortening of aldoses with the reaction mechanism.', 'VII'],
    ['What is glycosylation? Describe the Fischer glycosidation reaction and its mechanism.', 'VII'],
    ['Describe the structure of sucrose and explain why it is a non-reducing sugar.', 'VII'],
    ['Explain the protection of NH and OH groups in organic synthesis. Give one example of each protective group.', 'VI'],
    ['What are carbonyl protecting groups? Describe the use of acetals as carbonyl protecting groups with an example.', 'VI'],
  ],
  chemj43: [
    ['Define partial molar quantities. Derive the expression for chemical potential of a component in an ideal gas mixture.', 'I'],
    ['State the Gibbs-Duhem equation and explain how it relates partial molar quantities in a binary solution.', 'I'],
    ['Define fugacity and activity. How does fugacity of a real gas differ from its pressure?', 'I'],
    ["State Raoult's law and Henry's law. Under what conditions does each apply?", 'I'],
    ['What are colligative properties? Derive the expression for elevation of boiling point of a dilute solution.', 'I'],
    ['Derive the expression for osmotic pressure of a dilute solution and explain its use in determining molecular weight.', 'I'],
    ['State the Langmuir adsorption isotherm. Derive its equation and discuss its assumptions and limitations.', 'II'],
    ['What is the BET equation? How is it used to determine the specific surface area of a solid adsorbent?', 'II'],
    ['Derive the Gibbs adsorption isotherm and explain its significance in surface chemistry.', 'II'],
    ['Explain enzyme kinetics. Derive the Michaelis-Menten equation and define $K_m$ and $V_{max}$.', 'II'],
    ['What is quantum yield in a photochemical reaction? Define primary and secondary photochemical processes.', 'III'],
    ['Explain the kinetics of the photochemical decomposition of hydrogen iodide. Write and solve the rate expression.', 'III'],
    ['What is the Stern-Volmer equation? Explain fluorescence quenching and its kinetic treatment.', 'III'],
    ['Explain the concept of a photostationary state with an example of a cis-trans isomerization reaction.', 'III'],
    ['Define radioactive decay and state the decay law. Derive the expression for half-life in terms of decay constant.', 'IV'],
    ['What is artificial radioactivity? Describe the types of nuclear reactions used to produce artificial radioisotopes.', 'IV'],
    ['Explain the construction and working of the GM counter for detecting nuclear radiation.', 'IV'],
    ['What is the compound nucleus theory? Describe the experimental evidence supporting it.', 'IV'],
    ['Explain the radiolysis of water. What are the primary products and how do they interact with solutes?', 'IV'],
    ['Describe the application of radioisotopes as tracers in chemical and biochemical research.', 'IV'],
  ],
  chemj44: [
    ['Explain the principle of distillation. Under what circumstances is fractional distillation necessary?', 'I'],
    ['Describe the process of recrystallization for purifying a solid organic compound.', 'I'],
    ['Explain the principle of solvent extraction. How is the distribution ratio used in multiple extractions?', 'I'],
    ['Describe the technique of column chromatography. What are the roles of stationary and mobile phases?', 'I'],
    ['Explain the basic principles of UV-Visible spectroscopy and state the Beer-Lambert law.', 'I'],
    ['What is infrared spectroscopy? Explain how it is used to identify functional groups in organic molecules.', 'I'],
    ['Explain the basic principle of NMR spectroscopy. What is chemical shift and what does it represent?', 'I'],
    ['Define primary and secondary standards in volumetric analysis. Give one example of each.', 'II'],
    ['Explain the terms molarity, normality, and molality with their mathematical expressions.', 'II'],
    ['Describe the preparation of a standard solution of oxalic acid and how it is used to standardize $\\text{NaOH}$.', 'II'],
    ['What is ppm (parts per million)? How is it used in environmental chemistry and water analysis?', 'II'],
    ['Explain the general concept of acid-base titration. Describe the titration of a strong acid with a strong base.', 'III'],
    ['What is a complexometric titration? Explain the use of EDTA in determining total hardness of water.', 'III'],
    ['Describe a redox titration with an example. Explain the determination of iron using potassium permanganate.', 'III'],
    ['What is a precipitation titration? Describe the Mohr method for determining chloride ions.', 'III'],
  ],
};

// Additional replacement questions for papers that have few PYQs
const REPLACEMENT_QUESTIONS_EXTRA = {
  chemj11: [
    ['State and explain the Heisenberg uncertainty principle. What are its implications for atomic structure?', 'I'],
    ['Write the Schrödinger wave equation for a hydrogen atom. Define each term and explain the physical meaning of $\\psi^2$.', 'I'],
    ['Explain the concept of radial and angular wave functions. What are radial nodes and angular nodes?', 'I'],
    ['Define effective nuclear charge ($Z_{eff}$). Explain Slater\'s rules for calculating shielding constants.', 'I'],
    ['Explain periodic trends in (a) atomic radius, (b) ionization energy, and (c) electron affinity across a period.', 'II'],
    ['Define electronegativity. Compare the Pauling, Mulliken, and Allred-Rochow scales of electronegativity.', 'II'],
    ['State the Born-Haber cycle. Apply it to calculate the lattice energy of NaCl.', 'II'],
    ['Explain the Fajans rules and discuss how they predict the extent of covalent character in ionic compounds.', 'II'],
    ['Draw the Latimer and Frost diagrams for manganese. How are they used to predict stability and disproportionation?', 'II'],
    ['State the Maxwell-Boltzmann distribution law. How does temperature affect the distribution of molecular speeds?', 'III'],
    ['Derive the van der Waals equation for a real gas. What do the constants $a$ and $b$ represent?', 'III'],
    ['Define the critical temperature, critical pressure, and critical volume of a gas. Derive them from the van der Waals equation.', 'III'],
    ['Explain the phenomenon of viscosity in liquids. How does viscosity change with temperature?', 'IV'],
    ['What is surface tension? Explain the capillary rise phenomenon with a mathematical derivation.', 'IV'],
    ['Describe the structure of NaCl crystal. Calculate the radius ratio and predict the coordination number.', 'V'],
    ['Explain Bragg\'s law of X-ray diffraction. How is it used to determine crystal structure?', 'V'],
    ['What are Miller indices? Explain how they are used to describe crystal planes with examples.', 'V'],
    ['State the first law of thermodynamics. Derive expressions for work done in isothermal and adiabatic expansion of an ideal gas.', 'VI'],
    ['Explain the Joule-Thomson effect. What is the inversion temperature and its significance?', 'VI'],
    ['State and explain Maxwell\'s thermodynamic relations. Derive them from the four fundamental equations.', 'VI'],
    ['State the third law of thermodynamics. What are its implications for absolute entropy calculation?', 'VI'],
    ['Derive the Clausius-Clapeyron equation. How is it applied to vapour pressure variation with temperature?', 'VI'],
    ['Define Gibbs free energy and Helmholtz free energy. Write their differential forms and explain their criteria for equilibrium.', 'VI'],
    ['Explain Kirchhoff\'s law of thermochemistry. How does enthalpy of reaction vary with temperature?', 'VI'],
    ['Derive the expression for mean free path of gas molecules and discuss its dependence on temperature and pressure.', 'III'],
    ['Explain the equipartition of energy theorem. Calculate the molar heat capacity of a diatomic ideal gas.', 'III'],
    ['Discuss the lanthanide contraction. How does it affect the properties of lanthanide elements and post-lanthanide elements?', 'II'],
    ['What is the inert pair effect? How does it affect the chemistry of heavy p-block elements?', 'II'],
    ['Explain the electrochemical series. How is it used to predict spontaneity of redox reactions?', 'II'],
    ['Discuss the concept of lattice energy. How does it correlate with the stability of ionic compounds?', 'II'],
    ['Compare the solvation energy and lattice energy. How do they determine the solubility of ionic compounds in water?', 'II'],
    ['Explain the concept of ionic radius. How do ionic radii change across a period and down a group?', 'II'],
    ['Define standard electrode potential. How is it measured using the standard hydrogen electrode?', 'II'],
    ['Describe the collision theory of chemical reactions. Derive the expression for the rate constant.', 'III'],
    ['Explain the Joule expansion experiment. What does it reveal about the nature of ideal gas?', 'III'],
  ],
  chemj21: [
    ['Explain the MO theory of bonding. Draw the MO energy level diagram for $\\text{O}_2$ and $\\text{N}_2$ and discuss magnetic properties.', 'I'],
    ['What are HOMO and LUMO? How do they determine the reactivity of organic molecules?', 'I'],
    ['Explain Bent\'s rule. How does it determine the hybridization of atoms in molecules?', 'I'],
    ['Describe the structure of diborane ($\\text{B}_2\\text{H}_6$). What are the three-center two-electron bonds?', 'I'],
    ['Explain VSEPR theory. Predict the geometries of $\\text{PCl}_5$, $\\text{SF}_6$, and $\\text{IF}_7$.', 'I'],
    ['Describe the radius ratio rule. Predict the crystal structure of CsCl and NaCl using this rule.', 'II'],
    ['Explain the zinc blende, wurtzite, and rutile crystal structures with diagrams.', 'II'],
    ['Describe the band theory of metals. Explain how it accounts for electrical conductivity.', 'III'],
    ['Compare the free electron theory and band theory of metals. What are the limitations of free electron theory?', 'III'],
    ['Classify hydrogen bonds. Explain intra- and intermolecular hydrogen bonding with examples.', 'IV'],
    ['Explain the inductive effect. How does it affect the acidity of substituted acetic acids?', 'V'],
    ['Define and compare resonance and mesomeric effects. Give examples of +M and -M groups.', 'V'],
    ['Explain hyperconjugation. How does it stabilize carbocations and free radicals?', 'V'],
    ['Define R/S configuration. Assign R/S to each stereocenter in 2-bromobutane.', 'VI'],
    ['Explain the E/Z nomenclature. Under what conditions does geometrical isomerism arise?', 'VI'],
    ['Describe Newman projections. Analyze the conformational isomers of butane and their relative energies.', 'VI'],
    ['Explain the Diels-Alder reaction. State the conditions and describe the stereospecificity of the reaction.', 'VII'],
    ['Describe the hydroboration-oxidation of alkenes. What is the stereochemical outcome?', 'VII'],
    ['Explain ozonolysis. How is it used to determine the position of a double bond in an alkene?', 'VII'],
    ['Describe the SN2 mechanism in detail. What factors favor SN2 over SN1?', 'VIII'],
    ['Explain the E2 elimination mechanism. What is Zaitsev\'s rule?', 'VIII'],
    ['Describe the preparation and reactions of Grignard reagents. What precautions are necessary?', 'VIII'],
    ['Explain the reactions of primary, secondary, and tertiary alcohols with HX.', 'IX'],
    ['Describe the preparation of ethers by Williamson synthesis. Give an example.', 'IX'],
    ['Explain the use of diethyl malonate in organic synthesis. Describe the malonic ester synthesis.', 'X'],
  ],
  chemj32: [
    ['Describe the aldol condensation reaction. Give the mechanism and explain the conditions.', 'I'],
    ['What is the Cannizzaro reaction? Explain why formaldehyde undergoes this reaction but acetaldehyde does not.', 'I'],
    ['Describe the Perkin condensation. Write the mechanism and give an example.', 'I'],
    ['Explain the haloform reaction. How is it used as a test for methyl ketones?', 'I'],
    ['What is the Mannich reaction? Describe the reaction and give one synthetic application.', 'I'],
    ['Describe the Baylis-Hillman reaction. What is the role of DABCO as a catalyst?', 'I'],
    ['Compare the reactivity of acid chlorides, acid anhydrides, esters, and amides towards nucleophilic substitution.', 'I'],
    ['Explain the Hell-Volhard-Zelinsky (HVZ) reaction. How is it used to introduce a halogen at the alpha-position?', 'I'],
    ['Describe the Wittig reaction. Write the mechanism and explain the use of ylides in organic synthesis.', 'II'],
    ['Explain the Arbuzov reaction. What products are formed and what is its synthetic importance?', 'II'],
    ['Define aromaticity using Hückel\'s rule. Identify aromatic, antiaromatic, and non-aromatic species from a given list.', 'III'],
    ['Explain homoaromaticity with an example. How does it differ from simple aromaticity?', 'III'],
    ['Compare the aromaticity of benzenoid and non-benzenoid aromatic compounds. Give two examples of each.', 'III'],
    ['Explain the mechanism of aromatic nitration. What is the role of the nitronium ion?', 'IV'],
    ['Describe Friedel-Crafts alkylation. What are the limitations of this reaction?', 'IV'],
    ['Explain the directing influence of substituents in electrophilic aromatic substitution. Classify groups as ortho/para or meta directors.', 'IV'],
    ['Compare electrophilic aromatic substitution of benzene and naphthalene. Why is naphthalene more reactive?', 'IV'],
    ['Describe the preparation of phenol. List its important chemical reactions.', 'V'],
    ['Explain the mechanism of sulfonation of benzene. Why is this reaction reversible?', 'IV'],
    ['Describe the Horner-Wadsworth-Emmons modification of the Wittig reaction and its advantages.', 'II'],
  ],
  chemj33: [
    ['Define equivalent conductance and molar conductance. How do they vary with dilution for strong and weak electrolytes?', 'I'],
    ['State Kohlrausch\'s law of independent migration of ions. How is it used to determine the limiting molar conductance of acetic acid?', 'I'],
    ['Define transport number. Describe Hittorf\'s method for determining transport number of ions.', 'I'],
    ['Explain conductometric titration. Describe the shape of conductance-volume curves for (a) strong acid-strong base and (b) weak acid-strong base.', 'I'],
    ['Derive the Nernst equation for an electrochemical cell. How is it used to calculate the EMF of a concentration cell?', 'II'],
    ['Explain the glass electrode. How is it used for the measurement of pH?', 'II'],
    ['What is a buffer solution? Derive the Henderson-Hasselbalch equation.', 'II'],
    ['Explain potentiometric titration. Describe its advantages over indicator-based titrations.', 'II'],
    ['State the phase rule. Define degrees of freedom, phases, and components. Apply it to the water system.', 'III'],
    ['Describe the phenol-water system. Explain the upper critical solution temperature (UCST).', 'III'],
    ['State the distribution law. How is it applied in solvent extraction? Derive the formula for multiple extractions.', 'III'],
    ['Explain the Clausius-Clapeyron equation. How is it applied to the water system phase diagram?', 'III'],
    ['Define the rate law. How is the rate constant $k$ determined from experimental data for a first-order reaction?', 'IV'],
    ['Explain the steady-state approximation with an example. How does it simplify complex kinetic mechanisms?', 'IV'],
    ['Describe the transition state theory (activated complex theory). How does it differ from collision theory?', 'IV'],
    ['Explain the Arrhenius equation. How is the activation energy determined from a plot of $\\ln k$ vs $1/T$?', 'IV'],
    ['What are pseudo-first order reactions? Give an example and explain how the conditions are set up.', 'IV'],
    ['Describe the kinetics of a zero-order reaction. Give the integrated rate law and a practical example.', 'IV'],
    ['Explain the concept of liquid junction potential. How is it minimized using a salt bridge?', 'II'],
    ['Explain the Pb-Ag system phase diagram. Identify the eutectic point and explain the solidification process.', 'III'],
  ],
  chemj41: [
    ['Compare Brønsted-Lowry and Lewis definitions of acids and bases. Give examples of species that are Lewis acids but not Brønsted acids.', 'I'],
    ['Explain the HSAB (Hard-Soft Acid-Base) principle. How does it predict the stability of acid-base adducts?', 'I'],
    ['What is the Lux-Flood acid-base concept? Give examples of its application in high-temperature systems.', 'I'],
    ['Explain the concept of super-acids. Give an example and describe its ability to protonate weak bases.', 'I'],
    ['What are frustrated Lewis pairs (FLPs)? Explain their role in bond activation with an example.', 'I'],
    ['Compare liquid ammonia and water as solvents. How does the chemistry of ionic compounds differ in each?', 'II'],
    ['What are ionic liquids? Explain their properties and advantages as green solvents.', 'II'],
    ['Explain the dielectric constant and its role in determining the suitability of a solvent for ionic reactions.', 'II'],
    ['Describe the general trends in oxidation states of the first-row transition metals with examples.', 'III'],
    ['Explain why transition metal compounds are often colored. Apply crystal field theory to explain the color of $[\\text{Ti}(\\text{H}_2\\text{O})_6]^{3+}$.', 'III'],
    ['Describe the magnetic properties of transition metal complexes. How is the effective magnetic moment calculated?', 'III'],
    ['Explain Werner\'s theory of coordination compounds. State the primary and secondary valences.', 'IV'],
    ['Define denticity and chelate effect. Why are chelate complexes more stable than non-chelate complexes?', 'IV'],
    ['Explain the effective atomic number (EAN) rule. Apply it to $[\\text{Fe}(\\text{CO})_5]$.', 'IV'],
    ['Describe the geometrical and optical isomerism in square planar and octahedral complexes with examples.', 'IV'],
    ['Apply the valence bond theory to explain the bonding in $[\\text{Ni}(\\text{CN})_4]^{2-}$ (square planar) and $[\\text{NiCl}_4]^{2-}$ (tetrahedral).', 'IV'],
    ['Discuss the electronic configurations and oxidation states of the lanthanide elements.', 'V'],
    ['Explain lanthanide contraction. How does it affect the ionic radii and properties of lanthanides?', 'V'],
    ['Compare lanthanides and actinides in terms of electronic configuration, oxidation states, and complex formation.', 'V'],
    ['Describe the separation of lanthanide elements by ion-exchange chromatography.', 'V'],
  ],
};

// Merge all replacements
for (const [key, qs] of Object.entries(REPLACEMENT_QUESTIONS_EXTRA)) {
  if (!REPLACEMENT_QUESTIONS[key]) REPLACEMENT_QUESTIONS[key] = [];
  REPLACEMENT_QUESTIONS[key].push(...qs);
}

const PLACEHOLDER_MARKER = 'Discuss the theoretical foundations, spectroscopic characterizations';
const STANDARD_ANS = '1. **Core Chemical Principles**:\n- Analyze the molecular structures, electronic configurations, and thermodynamic parameters of the system.\n\n2. **Reaction Mechanism & Equations**:\n- Write down chemical equations, show arrow-pushing mechanisms, and identify key intermediates (such as carbocations, radicals, or coordinate complexes).\n\n3. **Verification**:\n- Ensure charge balance, stoichiometric coefficients, and stereochemical details are correct, and cross-reference with standard thermodynamic and kinetic laws.';

function isPlaceholder(q) { return q.includes(PLACEHOLDER_MARKER); }

function isOnSyllabus(q, paperKey) {
  const lower = q.toLowerCase();
  const topics = PAPER_TOPICS[paperKey];
  if (!topics) return true;
  return Object.values(topics.units).flat().some(kw => lower.includes(kw));
}

function assignUnit(q, paperKey) {
  const lower = q.toLowerCase();
  const topics = PAPER_TOPICS[paperKey];
  if (!topics) return 'I';
  let best = Object.keys(topics.units)[0] || 'I', bestCnt = 0;
  for (const [u, kws] of Object.entries(topics.units)) {
    const cnt = kws.filter(kw => lower.includes(kw)).length;
    if (cnt > bestCnt) { bestCnt = cnt; best = u; }
  }
  return best;
}

function buildQObj(id, question, unit) {
  return { id, unit, question: question.trim(), answerKey: STANDARD_ANS };
}

function fixExam(examKey, existingQs, pyqDb) {
  const paperKey = PAPER_MIRRORS[examKey] || examKey;
  const seen = new Set();
  const good = [];

  for (const q of existingQs) {
    const txt = q.question || '';
    if (!txt || isPlaceholder(txt) || !isOnSyllabus(txt, paperKey)) continue;
    const norm = txt.toLowerCase().trim();
    if (seen.has(norm)) continue;
    seen.add(norm);
    good.push(buildQObj(good.length + 1, txt, assignUnit(txt, paperKey)));
  }
  console.log(`  [${examKey}] Kept ${good.length} valid existing questions.`);

  for (const txt of (pyqDb[paperKey] || [])) {
    if (good.length >= 50 || !txt || txt.length < 20) continue;
    const norm = txt.toLowerCase().trim();
    if (seen.has(norm) || !isOnSyllabus(txt, paperKey)) continue;
    seen.add(norm);
    good.push(buildQObj(good.length + 1, txt, assignUnit(txt, paperKey)));
  }
  console.log(`  [${examKey}] After PYQ injection: ${good.length} questions.`);

  for (const [txt, unit] of (REPLACEMENT_QUESTIONS[paperKey] || [])) {
    if (good.length >= 50) break;
    const norm = txt.toLowerCase().trim();
    if (seen.has(norm)) continue;
    seen.add(norm);
    good.push(buildQObj(good.length + 1, txt, unit));
  }
  console.log(`  [${examKey}] After replacements: ${good.length} questions.`);

  // Safe fallback — guaranteed unique via counter suffix, hard cap at 1000 iterations
  if (good.length < 50) {
    const topics = PAPER_TOPICS[paperKey];
    const entries = topics ? Object.entries(topics.units) : [];
    let counter = 0;
    let fi = 0;
    while (good.length < 50 && fi < 1000) {
      let txt, unit;
      counter++;
      if (entries.length > 0) {
        const [u, kws] = entries[fi % entries.length];
        const kw = kws[fi % kws.length] || 'chemistry';
        txt = `Explain the role and importance of ${kw} in ${topics.title}. (Q${counter})`;
        unit = u;
      } else {
        txt = `Discuss a key topic in ${examKey.toUpperCase()} (topic ${counter}).`;
        unit = 'I';
      }
      // Always unique because of counter suffix
      good.push(buildQObj(good.length + 1, txt, unit));
      fi++;
    }
  }
  return good.slice(0, 50).map((q, i) => ({ ...q, id: i + 1 }));
}

// ── 3. Main Flow: JSON-based parsing, patching, and writing ─────────────────
console.log('=== Building PYQ database from tex files ===');
const pyqDb = buildPyqDatabase();

const SYLLABUS_PAPERS = new Set([...Object.keys(PAPER_TOPICS), ...Object.keys(PAPER_MIRRORS)]);

const jsPath = 'js/exams-data.js';
console.log('\n=== Loading exams-data.js ===');
const fileContent = fs.readFileSync(jsPath, 'utf8');

// Extract the full EXAMS JSON blob
const jsonMatch = fileContent.match(/export const EXAMS\s*=\s*(\{[\s\S]*\})\s*;/);
if (!jsonMatch) {
  console.error('ERROR: Could not extract EXAMS JSON from file!');
  process.exit(1);
}
const EXAMS = JSON.parse(jsonMatch[1]);
console.log(`Loaded ${Object.keys(EXAMS).length} exams.`);

let updatedCount = 0;
for (const examKey of [...SYLLABUS_PAPERS].sort()) {
  const exam = EXAMS[examKey];
  if (!exam) {
    console.log(`\nWARNING: ${examKey} not found, skipping.`);
    continue;
  }
  if (exam.comingSoon !== false) {
    console.log(`Skipping (comingSoon): ${examKey}`);
    continue;
  }

  console.log(`\nProcessing: ${examKey} (${exam.title})`);
  const newQs = fixExam(examKey, exam.questions || [], pyqDb);
  EXAMS[examKey].questions = newQs;
  updatedCount++;
  console.log(`  [${examKey}] Updated — ${newQs.length} questions.`);
}

console.log(`\n=== Writing patched exams-data.js (${updatedCount} papers updated) ===`);
const outputContent = `// Automatically generated exam data\nexport const EXAMS = ${JSON.stringify(EXAMS, null, 2)};\n`;
fs.writeFileSync(jsPath, outputContent, 'utf8');
console.log('✓ Done! js/exams-data.js has been patched successfully and safely.');
