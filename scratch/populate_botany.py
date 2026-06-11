import json
import re
import os

# =============================================================================
# 1. Botany Syllabi with standard questions for padding to 50
# =============================================================================
BOTANY_SYLLABI = {
    "bobmj11": {
        "title": "Cryptogams",
        "module": "BOBMJ11",
        "standard_questions": [
            ("Describe the morphology and reproduction in Chlamydomonas, emphasizing the sexual cycle.", "I"),
            ("Give a detailed account of the life cycle of Ulva with the alternation of generations.", "I"),
            ("Describe the characteristic features of Chlorophyceae with suitable examples.", "I"),
            ("Explain the cell structure, reproduction and economic importance of Volvox.", "I"),
            ("Describe the structure and reproduction in Ectocarpus.", "II"),
            ("Give an illustrated account of the morphology and reproduction in Sargassum.", "II"),
            ("Describe the general features of Phaeophyceae and their alternation of generations.", "II"),
            ("Describe the thallus organization and reproduction in Polysiphonia.", "II"),
            ("Give an account of the economic importance of red algae (Rhodophyceae).", "II"),
            ("Describe the occurrence, structure and reproduction of Nostoc.", "I"),
            ("Write notes on the morphology and reproduction of Oscillatoria.", "I"),
            ("Describe the distinguishing characters of Cyanophyceae (Cyanobacteria).", "I"),
            ("Give an illustrated account of the sexual reproduction in Oedogonium.", "I"),
            ("Describe the structure and reproduction in Vaucheria.", "I"),
            ("Explain heterocyst formation and nitrogen fixation in Cyanobacteria.", "I"),
            ("Describe the vegetative, asexual and sexual reproduction in Rhizopus.", "III"),
            ("Describe the life cycle of Puccinia graminis, explaining the role of alternate hosts.", "III"),
            ("Give an illustrated account of the morphology and reproduction in Penicillium.", "III"),
            ("Describe the general characters of Ascomycotina with examples.", "III"),
            ("Describe the structural organization and reproduction of Agaricus.", "III"),
            ("Explain the economic importance of fungi in agriculture and industry.", "III"),
            ("Describe the various types of spore formation in Ustilago.", "III"),
            ("Give a comparative account of the thallus structure of Riccia and Marchantia.", "IV"),
            ("Describe the morphology and reproduction in Marchantia with labeled diagrams.", "IV"),
            ("Describe the sporophyte structure and function in Anthoceros.", "IV"),
            ("Explain the classification of Bryophyta. Describe the general characters of Musci.", "IV"),
            ("Give an illustrated account of the structure and reproduction in Funaria.", "IV"),
            ("Describe the water-conducting system in mosses.", "IV"),
            ("Explain the morphology and anatomy of Equisetum stem.", "V"),
            ("Describe the structure and reproduction of Selaginella.", "V"),
            ("Give an account of the morphological and anatomical features of Pteris.", "V"),
            ("Describe the life cycle of Lycopodium.", "V"),
            ("Explain the stelar evolution in Pteridophytes.", "V"),
            ("Write on the economic importance of Pteridophytes.", "V"),
            ("Describe the habitat, external morphology and internal structure of Psilotum.", "V"),
        ]
    },
    "imbmj11": {
        "title": "Microbial Physiology, Biochemistry, Genetics and Molecular Biology",
        "module": "IMBMJ11",
        "standard_questions": [
            ("Describe the structure of the bacterial cell wall and explain the difference between Gram-positive and Gram-negative bacteria.", "I"),
            ("Explain the different types of microbial nutrition — autotrophy, heterotrophy, and lithotrophy.", "I"),
            ("Describe the phases of bacterial growth curve with the mathematical model of exponential growth.", "I"),
            ("Explain the mechanism of oxidative phosphorylation and the chemiosmotic hypothesis.", "II"),
            ("Describe the TCA (Krebs) cycle with all intermediates and the net energy yield.", "II"),
            ("Explain the Embden-Meyerhof-Parnas (EMP) pathway of glycolysis.", "II"),
            ("Compare aerobic and anaerobic respiration in microorganisms.", "II"),
            ("Describe the mechanism of enzyme action and factors affecting enzyme activity.", "II"),
            ("Explain the structure and types of RNA and their roles in protein synthesis.", "III"),
            ("Describe the mechanism of DNA replication in prokaryotes (Okazaki fragments, proofreading).", "III"),
            ("Explain the process of transcription in prokaryotes — initiation, elongation, and termination.", "III"),
            ("Describe the process of translation, explaining the role of ribosomes and tRNAs.", "III"),
            ("Explain the lac operon model of gene regulation in E. coli.", "III"),
            ("Describe the various types of mutations and the molecular basis of UV-induced mutations.", "IV"),
            ("Explain the mechanism of transduction in bacteria.", "IV"),
            ("Describe conjugation in bacteria, including the role of the F factor.", "IV"),
            ("Explain transformation in bacteria, detailing the competence state.", "IV"),
            ("Describe transposable elements and their mechanism of transposition.", "IV"),
            ("Explain the structure and types of plasmids and their significance.", "IV"),
            ("Describe the SOS response in bacteria as a DNA repair mechanism.", "IV"),
            ("Explain the central dogma of molecular biology.", "III"),
            ("Describe the structure of the nucleosome and chromatin.", "III"),
            ("Explain gene amplification and rDNA technology in microorganisms.", "V"),
            ("Describe the biochemistry of photosynthesis in photosynthetic bacteria.", "II"),
            ("Explain purine and pyrimidine biosynthesis.", "II"),
        ]
    },
    "bobmj21": {
        "title": "Microbiology, Plant Pathology, Cytology and Genetics",
        "module": "BOBMJ21",
        "standard_questions": [
            ("Describe the general morphological and structural features of viruses.", "I"),
            ("Explain the lytic and lysogenic cycles in bacteriophage.", "I"),
            ("Describe the structure and replication of TMV (Tobacco Mosaic Virus).", "I"),
            ("Explain Koch's Postulates and their significance in plant pathology.", "II"),
            ("Describe the symptoms, causal organism and disease cycle of late blight of potato.", "II"),
            ("Describe the symptoms, cause and management of loose smut of wheat.", "II"),
            ("Explain the physiological races of Puccinia and the gene-for-gene hypothesis.", "II"),
            ("Describe the symptoms, causal agent and control of citrus canker.", "II"),
            ("Explain the integrated pest management (IPM) strategies.", "II"),
            ("Describe the ultra-structure of the nucleus, mitochondrion, and chloroplast.", "III"),
            ("Explain the cell cycle. Describe the stages of mitosis with diagrams.", "III"),
            ("Describe the stages of meiosis with diagrams. Explain the significance of chiasmata.", "III"),
            ("Explain the structure of chromosomes — lampbrush and polytene chromosomes.", "III"),
            ("Describe the molecular structure of DNA (Watson-Crick model).", "III"),
            ("Explain Mendel's laws of inheritance with examples.", "IV"),
            ("Describe the concept of linkage and crossing over.", "IV"),
            ("Explain sex-linked inheritance with examples (colour blindness, haemophilia).", "IV"),
            ("Describe the chromosomal theory of sex determination.", "IV"),
            ("Explain multiple allelism with the example of ABO blood groups.", "IV"),
            ("Describe polygenic inheritance with the example of skin colour.", "IV"),
            ("Explain incomplete dominance and co-dominance.", "IV"),
            ("Describe the significance of recombination and gene mapping.", "IV"),
            ("Explain the mutation theory and types of chromosomal aberrations.", "V"),
            ("Describe the characteristics and uses of viroids and prions.", "I"),
            ("Explain the symptoms and control of blast disease of rice.", "II"),
        ]
    },
    "bobmn21": {
        "title": "Ancillary Botany I",
        "module": "BOBMN21",
        "standard_questions": [
            ("Describe the morphology and reproduction in Spirogyra.", "I"),
            ("Give a brief account of Rhodophyceae with examples.", "I"),
            ("Describe the life cycle of Aspergillus.", "II"),
            ("Give a comparative account of Hepaticae and Anthocerotae.", "II"),
            ("Describe the structure and reproduction in Lycopsida.", "III"),
            ("Explain the alternation of generations in Pteridophytes.", "III"),
            ("Describe the general classification of Gymnosperms.", "IV"),
            ("Give an account of Mendel's laws of segregation and independent assortment.", "IV"),
            ("Explain the chromosomal theory of inheritance.", "V"),
            ("Describe sex-linked inheritance with examples.", "V"),
            ("Describe the general characters of Xanthophyceae.", "I"),
            ("Explain the structure and reproduction in Volvox.", "I"),
            ("Give a brief account of the economic importance of Algae.", "I"),
            ("Describe the vegetative and asexual reproduction in Rhizopus.", "II"),
            ("Explain the significance of heterosis (hybrid vigour).", "V"),
            ("Describe the concept of multiple allelism.", "IV"),
            ("Give an account of the ultra-structure of a plant cell.", "III"),
            ("Explain mitosis and its biological significance.", "III"),
            ("Describe the stages of meiosis in brief.", "III"),
            ("Explain extra-nuclear inheritance with cytoplasmic male sterility.", "V"),
            ("Describe the general characters and reproduction in Musci.", "II"),
            ("Give an account of the morphology and anatomy of Equisetum.", "III"),
            ("Explain the economic importance of Gymnosperms.", "IV"),
            ("Describe linkage and its types.", "IV"),
            ("Explain polyploidy and its role in crop improvement.", "V"),
        ]
    },
    "imbmj21": {
        "title": "Environmental Microbiology and Biotechnology",
        "module": "IMBMJ21",
        "standard_questions": [
            ("Describe the role of microorganisms in the nitrogen cycle.", "I"),
            ("Explain biological nitrogen fixation by Rhizobium and free-living organisms.", "I"),
            ("Describe the carbon cycle, emphasizing microbial decomposition.", "I"),
            ("Explain microbial processes involved in the sulphur cycle.", "I"),
            ("Describe the concept of biological oxygen demand (BOD) in water pollution.", "II"),
            ("Explain the conventional primary, secondary, and tertiary treatment of sewage.", "II"),
            ("Describe the role of microorganisms in bioremediation of oil spills.", "II"),
            ("Explain composting as a solid waste management technique.", "II"),
            ("Describe the principles and applications of recombinant DNA technology.", "III"),
            ("Explain the polymerase chain reaction (PCR) with its steps and applications.", "III"),
            ("Describe gel electrophoresis and its role in molecular biology.", "III"),
            ("Explain the vectors used in gene cloning (plasmids, bacteriophages).", "III"),
            ("Describe the production of antibiotics (penicillin) by fermentation.", "IV"),
            ("Explain the production and industrial applications of enzyme immobilization.", "IV"),
            ("Describe microbial production of vitamins and amino acids.", "IV"),
            ("Explain the production of single-cell protein (SCP) from microorganisms.", "IV"),
            ("Describe the types and applications of biofertilizers.", "I"),
            ("Explain the principles of biogas production from biomass.", "II"),
            ("Describe the concept of biosensors and their applications.", "V"),
            ("Explain the applications of microorganisms in bioleaching of ores.", "V"),
            ("Describe the techniques for detection of microbial water pollution.", "II"),
            ("Explain DNA fingerprinting and its forensic applications.", "III"),
            ("Describe the concept and applications of metagenomics.", "V"),
            ("Explain the ecological role of microorganisms in phosphorus cycle.", "I"),
            ("Describe production of lactic acid by microbial fermentation.", "IV"),
        ]
    },
    "bobmj31": {
        "title": "Plant Ecology and Physiology",
        "module": "BOBMJ31",
        "standard_questions": [
            ("Describe the concept of ecological niche. Explain the Hutchinsonian niche.", "I"),
            ("Explain interspecific competition, describing the Lotka-Volterra equations.", "I"),
            ("Describe the different types of symbiosis: mutualism, commensalism and parasitism.", "I"),
            ("Describe the adaptations of Halophytes to saline environments.", "I"),
            ("Explain the concept of biomass pyramids, pyramid of numbers, and pyramid of energy.", "II"),
            ("Describe the process of decomposition and nutrient recycling in a forest ecosystem.", "II"),
            ("Explain the mechanisms of water absorption in roots. Discuss the role of aquaporins.", "III"),
            ("Describe the mechanism of stomatal opening and closing, emphasizing the K+ pump hypothesis.", "III"),
            ("Explain the mechanism of phloem transport (Pressure Flow/Mass Flow hypothesis).", "III"),
            ("Describe the role of essential mineral elements. Explain symptoms of N, P, and K deficiency.", "III"),
            ("Explain the light reaction of photosynthesis, focusing on the Z-scheme.", "III"),
            ("Describe the Calvin (C3) cycle of carbon fixation in detail.", "III"),
            ("Explain the mechanism of seed germination and the role of hormones.", "IV"),
            ("Describe the role of Auxins in cell elongation (Acid Growth Hypothesis).", "IV"),
            ("Explain the role of Cytokinins in delaying leaf senescence.", "IV"),
            ("Describe the mechanism of action of Abscisic Acid (ABA) in seed dormancy.", "IV"),
            ("Explain the biological clock and circadian rhythms in plants.", "V"),
            ("Describe the photoperiodic response: classify plants by SDP, LDP, and DNP.", "V"),
            ("Explain the role of Phytochrome in photoperiodism.", "V"),
            ("Describe the biochemical mechanisms of vernalization.", "V"),
        ]
    },
    "imbmj31": {
        "title": "Agricultural and Food Microbiology",
        "module": "IMBMJ31",
        "standard_questions": [
            ("Describe the role of soil microorganisms in maintaining soil fertility.", "I"),
            ("Explain biological nitrogen fixation with emphasis on the nitrogenase enzyme.", "I"),
            ("Describe mycorrhizal associations and their role in nutrient uptake by plants.", "I"),
            ("Explain the role of phosphate-solubilizing bacteria in agriculture.", "I"),
            ("Describe the principles and methods of disease management in crops.", "II"),
            ("Explain the disease cycle of crown gall disease caused by Agrobacterium tumefaciens.", "II"),
            ("Describe the role of plant growth-promoting rhizobacteria (PGPR).", "II"),
            ("Explain the mechanisms of biocontrol using Bacillus and Trichoderma.", "II"),
            ("Describe the microbiology of bread fermentation by yeast.", "III"),
            ("Explain the production of vinegar by microbial fermentation.", "III"),
            ("Describe the production of cheese and its ripening by microorganisms.", "III"),
            ("Explain the production of beer and wine by Saccharomyces cerevisiae.", "III"),
            ("Describe food spoilage — physical, chemical, and microbiological causes.", "IV"),
            ("Explain food preservation methods — canning, pasteurization, irradiation.", "IV"),
            ("Describe Foodborne illnesses caused by Salmonella, Staphylococcus, and Clostridium.", "IV"),
            ("Explain HACCP (Hazard Analysis and Critical Control Points) in food safety.", "IV"),
            ("Describe the microbiology of fermented foods — idli, dosa, yoghurt.", "III"),
            ("Explain the application of probiotics and prebiotics in food industry.", "IV"),
            ("Describe the role of lactic acid bacteria in food fermentation.", "III"),
            ("Explain the role of enzymes (amylase, protease, lipase) in food processing.", "V"),
            ("Describe microbial production of organic acids — citric acid and acetic acid.", "V"),
            ("Explain the role of microorganisms in composting food waste.", "I"),
            ("Describe biofungicides as alternatives to chemical pesticides.", "II"),
            ("Explain the detection of pathogens by ELISA and PCR in food testing.", "V"),
            ("Describe the production of microbial insecticides (Bt toxin).", "II"),
        ]
    },
    "bobmj41": {
        "title": "Phanerogams",
        "module": "BOBMJ41",
        "standard_questions": [
            ("Describe the general characters of Gymnosperms. Give the classification of Gymnosperms.", "I"),
            ("Describe the morphology, anatomy and reproduction of Cycas.", "I"),
            ("Give an illustrated account of microsporogenesis and microgametogenesis in Pinus.", "I"),
            ("Describe the structure of seed and seedling development in Gymnosperms.", "I"),
            ("Explain the economic importance of Gymnosperms.", "I"),
            ("Give a comparative account of the vegetative characters of monocots and dicots.", "II"),
            ("Describe the systems of angiosperm classification proposed by Engler and Prantl.", "II"),
            ("Describe the family Malvaceae with floral formula, floral diagram and economic importance.", "II"),
            ("Describe the family Leguminosae (Fabaceae) with floral formula and economic importance.", "II"),
            ("Describe the family Solanaceae with floral formula, floral diagram and economic importance.", "II"),
            ("Describe the family Liliaceae with floral formula and economic importance.", "II"),
            ("Describe the family Poaceae (Gramineae) with floral formula and economic importance.", "II"),
            ("Describe the family Asteraceae (Compositae) with floral formula and types of florets.", "II"),
            ("Explain the types of placentation in angiosperms with diagrams.", "III"),
            ("Describe the types of inflorescence in angiosperms with examples.", "III"),
            ("Explain the types of aestivation and their taxonomic significance.", "III"),
            ("Describe the development of male gametophyte in angiosperms.", "III"),
            ("Describe the development of female gametophyte (Polygonum type) in angiosperms.", "III"),
            ("Explain double fertilization and its significance in angiosperms.", "III"),
            ("Describe the development and types of endosperm in angiosperms.", "IV"),
            ("Explain the structure of a dicot and monocot seed.", "IV"),
            ("Describe seed dormancy and methods of breaking dormancy.", "IV"),
            ("Explain the origin, types and modifications of roots.", "IV"),
            ("Describe the primary anatomy of a dicot root and monocot root.", "IV"),
            ("Explain the secondary growth in dicot root with diagrams.", "V"),
            ("Describe anomalous secondary growth in Bignonia stem.", "V"),
            ("Describe the primary and secondary anatomy of a dicot stem.", "V"),
            ("Explain the anatomy of a monocot stem (maize) in detail.", "V"),
            ("Describe the anatomy of a xerophytic leaf (Nerium).", "V"),
            ("Explain the concept of the Bentham and Hooker's classification of angiosperms.", "II"),
        ]
    },
    "bobmn41": {
        "title": "Ancillary Botany II",
        "module": "BOBMN41",
        "standard_questions": [
            ("Give an account of the life cycle of Cycas with labeled diagrams.", "I"),
            ("Describe the external morphology and internal anatomy of Pinus needle.", "I"),
            ("Describe the family Ranunculaceae with floral formula and economic importance.", "II"),
            ("Describe the family Cruciferae (Brassicaceae) with examples.", "II"),
            ("Explain the types of fruits in angiosperms with examples.", "III"),
            ("Describe the development of the embryo in a dicot plant.", "III"),
            ("Explain the primary anatomy of a dicot stem (sunflower).", "IV"),
            ("Describe the structure of a C4 leaf (maize leaf anatomy).", "IV"),
            ("Describe plant succession in terrestrial habitats (Xerosere).", "V"),
            ("Explain the concept of a biome. Describe tropical rainforest biome.", "V"),
            ("Describe the economic importance of the family Euphorbiaceae.", "II"),
            ("Give an account of the family Cucurbitaceae with floral formula.", "II"),
            ("Explain vernalization and its application in agriculture.", "III"),
            ("Describe the role of Gibberellins in plant growth.", "III"),
            ("Explain the significance of secondary metabolites in plants.", "IV"),
            ("Describe the habitat and ecological adaptations of hydrophytes.", "V"),
            ("Explain energy flow through an ecosystem.", "V"),
            ("Describe the roles of Gymnosperms in forest ecosystem.", "I"),
            ("Give a brief account of the anatomy of a monocot leaf.", "IV"),
            ("Explain the mechanism of action of Ethylene as a plant hormone.", "III"),
            ("Describe the family Rubiaceae with its floral formula and examples.", "II"),
            ("Explain the concept of soil profile and soil formation processes.", "V"),
            ("Describe the classification of plants proposed by A.L. de Jussieu.", "II"),
            ("Explain phytoremediation and its applications.", "V"),
            ("Describe the ultrastructure of a chloroplast.", "IV"),
        ]
    },
    "bobmj51": {
        "title": "Comparative Studies of Cryptogams",
        "module": "BOBMJ51",
        "standard_questions": [
            ("Give a comparative account of the vegetative thallus structure in Chlorophyceae and Phaeophyceae.", "I"),
            ("Describe the classification of Algae up to class level with diagnostic characters.", "I"),
            ("Give a comparative account of the sexual reproduction in Spirogyra, Oedogonium and Cladophora.", "I"),
            ("Describe the cell structure and pigment composition of different algal classes.", "I"),
            ("Give a comparative account of life cycles in Ectocarpus, Laminaria and Polysiphonia.", "II"),
            ("Describe the economic importance of algae — agar, carrageenan, food and fertilizer.", "II"),
            ("Compare the thallus organization in different classes of Fungi.", "III"),
            ("Give a comparative account of sexual reproduction in Phycomycetes, Ascomycetes and Basidiomycetes.", "III"),
            ("Describe the role of fungi in causing plant diseases. Give two examples.", "III"),
            ("Explain the classification of Fungi and their evolutionary significance.", "III"),
            ("Give a comparative account of sporophyte in Riccia, Pellia, and Marchantia.", "IV"),
            ("Describe the differences between Hepaticae, Anthocerotae, and Musci.", "IV"),
            ("Give a comparative account of the sporophyte structure in Lycopodium, Selaginella, and Equisetum.", "V"),
            ("Describe the stele types observed in Pteridophytes.", "V"),
            ("Explain the concept of heterospory and its significance.", "V"),
            ("Describe the fossil Pteridophytes and their evolutionary significance.", "V"),
            ("Give a comparative account of the gametophyte in Pteridophytes.", "V"),
            ("Describe the economic importance of Pteridophytes.", "V"),
            ("Explain the origin and evolution of land plants from algal ancestors.", "I"),
            ("Describe the different types of lichens and their ecological role.", "III"),
        ]
    },
    "bobmj52": {
        "title": "Comparative Studies of Phanerogams",
        "module": "BOBMJ52",
        "standard_questions": [
            ("Give a comparative account of the male and female strobili of Cycas, Pinus, and Gnetum.", "I"),
            ("Explain the evolutionary significance of Gymnosperms in the plant kingdom.", "I"),
            ("Describe the classification of Angiosperms proposed by Cronquist.", "II"),
            ("Give a comparative account of different types of ovules in angiosperms.", "II"),
            ("Describe the types and evolutionary significance of pollination mechanisms.", "II"),
            ("Explain the embryology of the family Solanaceae.", "III"),
            ("Describe the various types of embryo development patterns in dicots.", "III"),
            ("Give a comparative account of dicot and monocot leaf anatomy.", "III"),
            ("Explain secondary growth in dicot stem with vascular cambium activity.", "IV"),
            ("Describe the types of wood in dicots (ring-porous vs. diffuse-porous).", "IV"),
            ("Give a comparative account of the anatomy of water-storing plants.", "IV"),
            ("Describe the types of secretory structures in plants (glands, ducts, latex).", "IV"),
            ("Explain chemical systematics and its role in plant taxonomy.", "V"),
            ("Describe numerical taxonomy and its advantages and limitations.", "V"),
            ("Explain the concept of cladistics and phylogenetic systematics.", "V"),
            ("Describe the use of scanning electron microscopy (SEM) in plant systematics.", "V"),
            ("Explain the application of DNA barcoding in plant identification.", "V"),
            ("Describe the general characters and systematic position of Ephedra.", "I"),
            ("Give an account of the family Apiaceae with floral diagram and examples.", "II"),
            ("Describe the diagnostic characters of family Myrtaceae with examples.", "II"),
        ]
    },
    "bobmj53": {
        "title": "Plant Ecology, Environmental Pollution and Toxicology",
        "module": "BOBMJ53",
        "standard_questions": [
            ("Describe the ecological factors — climate, edaphic, biotic — and their effects on plants.", "I"),
            ("Explain the concept of minimum, maximum, and optimum for ecological factors.", "I"),
            ("Describe the diversity indices (Shannon-Weiner, Simpson's) used in ecology.", "I"),
            ("Explain the types and causes of air pollution and their effects on plants.", "II"),
            ("Describe the effects of ozone depletion on plants and ecosystems.", "II"),
            ("Explain the causes and effects of acid rain on vegetation.", "II"),
            ("Describe the sources and effects of heavy metal pollution on plants.", "II"),
            ("Explain the concept of bioaccumulation and biomagnification.", "II"),
            ("Describe the methods for phytoremediation of contaminated soils.", "III"),
            ("Explain the toxic effects of pesticides on non-target organisms.", "III"),
            ("Describe the concept of eutrophication and its impact on aquatic ecosystems.", "III"),
            ("Explain noise pollution and its biological effects.", "III"),
            ("Describe the methods for measuring air quality index (AQI).", "II"),
            ("Explain the role of plants as bioindicators of environmental pollution.", "IV"),
            ("Describe the acute and chronic toxicity testing of pollutants using plants.", "IV"),
            ("Explain the concept of EC50 and LD50 in environmental toxicology.", "IV"),
            ("Describe the concept of wetlands and their ecological services.", "V"),
            ("Explain the conservation strategies for biodiversity hotspots.", "V"),
            ("Describe the concept of carbon sequestration and its role in climate change mitigation.", "V"),
            ("Explain the International agreements for environmental protection: CBD, CITES, Kyoto Protocol.", "V"),
            ("Describe the IUCN red list categories and criteria.", "V"),
            ("Explain the role of in-situ and ex-situ conservation in plant biodiversity.", "V"),
            ("Describe the structure and function of mangrove ecosystems.", "I"),
            ("Explain the concept of ecological footprint and sustainable development.", "I"),
            ("Describe the effects of global warming on plant distribution.", "II"),
        ]
    },
    "bobmj61": {
        "title": "Plant Metabolism, Biochemistry and Biotechnology",
        "module": "BOBMJ61",
        "standard_questions": [
            ("Describe the complete light reactions of photosynthesis including Photosystems I and II.", "I"),
            ("Explain the Calvin cycle (C3 cycle) with all the enzymes and intermediates.", "I"),
            ("Describe the C4 pathway of CO2 fixation and Kranz anatomy.", "I"),
            ("Explain photorespiration (C2 cycle) and its economic significance.", "I"),
            ("Describe fatty acid synthesis (de novo biosynthesis) in plants.", "II"),
            ("Explain the beta-oxidation of fatty acids and its energy yield.", "II"),
            ("Describe the biosynthesis of amino acids — the shikimate pathway.", "II"),
            ("Explain the urea cycle and its role in nitrogen metabolism in plants.", "II"),
            ("Describe the enzymes of nitrogen assimilation: nitrate reductase, nitrite reductase, GS-GOGAT.", "II"),
            ("Explain the structure and biosynthesis of chlorophylls.", "I"),
            ("Describe the principles and applications of plant tissue culture.", "III"),
            ("Explain somatic hybridization and its applications in plant biotechnology.", "III"),
            ("Describe the role of Agrobacterium tumefaciens in plant transformation.", "III"),
            ("Explain Bt crops — mechanism and applications.", "III"),
            ("Describe the techniques used in molecular markers: RFLP, RAPD, SSR.", "IV"),
            ("Explain the use of DNA fingerprinting in plant variety protection.", "IV"),
            ("Describe the process of somatic embryogenesis and organogenesis.", "III"),
            ("Explain the RNA interference (RNAi) technology in plants.", "IV"),
            ("Describe the biosynthesis and functions of secondary metabolites: alkaloids, terpenes.", "V"),
            ("Explain the concept of metabolic flux and metabolic engineering in plants.", "V"),
            ("Describe the production of pharmaceutical compounds through plant cell culture.", "V"),
            ("Explain the structure and role of phytohormones in fruit ripening.", "IV"),
            ("Describe chloroplast and mitochondrial genomes and their significance.", "I"),
            ("Explain transposons and their role in plant genome evolution.", "IV"),
            ("Describe the biosynthesis of cell wall components: cellulose and lignin.", "II"),
        ]
    },
    "bobmj62": {
        "title": "Microbiology and Plant Pathology",
        "module": "BOBMJ62",
        "standard_questions": [
            ("Describe the morphology and ultra-structure of bacteria.", "I"),
            ("Explain the mechanisms of bacterial pathogenesis in plants.", "I"),
            ("Describe the types and properties of plant viruses.", "I"),
            ("Explain the disease cycle of bacterial wilt of tomato.", "I"),
            ("Describe the symptoms, etiology and control of damping off disease.", "II"),
            ("Explain the epidemiology and management of powdery mildew.", "II"),
            ("Describe the disease cycle and management strategies for downy mildew.", "II"),
            ("Explain the concept of pathogen virulence and host resistance.", "II"),
            ("Describe the biochemical basis of host-pathogen interaction.", "III"),
            ("Explain the hypersensitive response (HR) and systemic acquired resistance (SAR).", "III"),
            ("Describe the role of phytoalexins in disease resistance.", "III"),
            ("Explain the mechanism of action of fungicides.", "III"),
            ("Describe the principles of biological control of plant diseases.", "IV"),
            ("Explain the role of induced systemic resistance (ISR).", "IV"),
            ("Describe the etiology and management of Karnal bunt of wheat.", "IV"),
            ("Explain the disease management of root rot in crops.", "IV"),
            ("Describe the role of mycoplasma-like organisms in plant diseases.", "I"),
            ("Explain the concept of plant quarantine and disease exclusion.", "V"),
            ("Describe the principles and methods of plant disease forecasting.", "V"),
            ("Explain the types and applications of antifungal compounds.", "III"),
            ("Describe the symptoms and management of Fusarium wilt of banana.", "IV"),
            ("Explain the genetics of disease resistance in plants.", "II"),
            ("Describe the types and significance of endophytic fungi.", "I"),
            ("Explain the mechanism of toxin production by plant pathogens.", "II"),
            ("Describe the use of biotechnology in the development of disease-resistant plants.", "V"),
        ]
    },
    "bobmj63": {
        "title": "Cytogenetics and Evolutionary Processes",
        "module": "BOBMJ63",
        "standard_questions": [
            ("Describe the structure of eukaryotic chromosome — centromere, telomere, and satellite.", "I"),
            ("Explain the molecular basis of chromosome condensation during mitosis.", "I"),
            ("Describe the various types of chromosomal aberrations (deletions, duplications, inversions, translocations).", "I"),
            ("Explain the genetic consequences of chromosomal inversions.", "I"),
            ("Describe euploidy and aneuploidy with examples from plants.", "II"),
            ("Explain the origin and significance of polyploidy in plant evolution.", "II"),
            ("Describe allopolyploidy with examples (Raphanobrassica, wheat).", "II"),
            ("Explain the concept of B-chromosomes and their effects.", "II"),
            ("Describe the molecular structure of repetitive DNA sequences.", "III"),
            ("Explain the C-value paradox and the organization of the plant genome.", "III"),
            ("Describe the process of chromosome banding techniques (G-banding, C-banding).", "III"),
            ("Explain the mechanism and significance of gene duplication.", "III"),
            ("Describe Darwin's theory of natural selection with evidence.", "IV"),
            ("Explain the Hardy-Weinberg equilibrium and its importance in population genetics.", "IV"),
            ("Describe the concept of genetic drift and the founder effect.", "IV"),
            ("Explain speciation — allopatric and sympatric mechanisms.", "IV"),
            ("Describe adaptive radiation with examples from plants.", "IV"),
            ("Explain the molecular clock hypothesis.", "IV"),
            ("Describe the evidence for evolution from fossil records and comparative anatomy.", "V"),
            ("Explain horizontal gene transfer and its role in evolution.", "V"),
            ("Describe the endosymbiotic theory of chloroplast and mitochondria origin.", "V"),
            ("Explain the origin of angiosperms from a phylogenetic perspective.", "V"),
            ("Describe coevolution with examples of plant-pollinator interactions.", "V"),
            ("Explain genetic erosion and its implications for crop breeding.", "III"),
            ("Describe the chromosomal evolution and karyotype changes in plants.", "I"),
        ]
    },
    "bobmj64": {
        "title": "Plant and Microbial Techniques",
        "module": "BOBMJ64",
        "standard_questions": [
            ("Describe the principles and steps of plant tissue culture technique.", "I"),
            ("Explain the preparation and sterilization of culture media for plant tissue culture.", "I"),
            ("Describe the technique of anther culture and its application in plant breeding.", "I"),
            ("Explain the technique of protoplast isolation, culture and fusion.", "I"),
            ("Describe the light microscopy — compound microscope, fluorescence microscopy.", "II"),
            ("Explain the principles and applications of electron microscopy (TEM and SEM).", "II"),
            ("Describe the technique of chromatography — TLC, column, and HPLC.", "II"),
            ("Explain gel electrophoresis — agarose and polyacrylamide gel electrophoresis (PAGE).", "II"),
            ("Describe the technique of DNA extraction from plant material.", "III"),
            ("Explain the Southern blotting technique.", "III"),
            ("Describe the Western blotting technique and its applications.", "III"),
            ("Explain the PCR technique — steps, variations, and applications.", "III"),
            ("Describe the principles and applications of DNA sequencing (Sanger method).", "IV"),
            ("Explain next-generation sequencing (NGS) techniques.", "IV"),
            ("Describe microbial culturing techniques — solid and liquid media.", "IV"),
            ("Explain the differential staining techniques for bacteria (Gram stain, acid-fast stain).", "IV"),
            ("Describe the haemocytometer and methods of counting microbial populations.", "IV"),
            ("Explain fermentation technology — batch, fed-batch, and continuous culture.", "V"),
            ("Describe the principles of centrifugation and ultracentrifugation.", "V"),
            ("Explain spectrophotometry and its applications in quantifying biological molecules.", "V"),
            ("Describe the ELISA technique and its applications in detection.", "V"),
            ("Explain flow cytometry and its applications in plant biology.", "V"),
            ("Describe the technique of confocal laser scanning microscopy (CLSM).", "II"),
            ("Explain FISH (Fluorescence In Situ Hybridization) in chromosome mapping.", "III"),
            ("Describe the technique of radioactive labeling and autoradiography.", "III"),
        ]
    }
}

# Unique keys to primary mapping (only one set of questions per course)
UNIQUE_TO_ACTIVE = {
    "bobmj11": ["bobmj11"],
    "imbmj11": ["imbmj11"],
    "bobmj21": ["bobmj21"],
    "bobmn21": ["bobmn21"],
    "imbmj21": ["imbmj21"],
    "bobmj31": ["bobmj31"],
    "imbmj31": ["imbmj31"],
    "bobmj41": ["bobmj41"],
    "bobmn41": ["bobmn41"],
    "bobmj51": ["bobmj51"],
    "bobmj52": ["bobmj52"],
    "bobmj53": ["bobmj53"],
    "bobmj61": ["bobmj61"],
    "bobmj62": ["bobmj62"],
    "bobmj63": ["bobmj63"],
    "bobmj64": ["bobmj64"],
}

# LaTeX file -> exam key mapping
FILE_TO_KEY = {
    "BOB-101": "bobmj11",
    "IMB-101": "imbmj11",
    "BOB-201": "bobmj21",
    "BOB-203A": "bobmn21",
    "IMB-201": "imbmj21",
    "BOB-301": "bobmj31",
    "IMB-301": "imbmj31",
    "BOB-401": "bobmj41",
    "BOB-403A": "bobmn41",
    "BOB-501": "bobmj51",
    "BOB-502": "bobmj52",
    "BOB-503": "bobmj53",
    "BOB-601": "bobmj61",
    "BOB-602": "bobmj62",
    "BOB-603": "bobmj63",
    "BOB-604": "bobmj64",
}

# Clean LaTeX text
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

def get_code_from_filename(filename):
    """Extract course code like BOB-101 or IMB-301 from filename."""
    m = re.search(r'(BOB-\d+[A-Z]?|IMB-\d+[A-Z]?)', filename.upper())
    return m.group(1) if m else None

def parse_tex_file(filepath):
    """Parse LaTeX file and extract main questions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'(?m)^%.*$', '', content)

    parts_questions = []
    parts_matches = re.finditer(r'\\begin\{(parts|romanparts)\}(.*?)\\end\{\1\}', content, re.DOTALL)
    for match in parts_matches:
        parts_content = match.group(2)
        items = re.split(r'\\item', parts_content)
        for item in items[1:]:
            cleaned = clean_text(item)
            if len(cleaned) > 20:
                parts_questions.append(cleaned)

    main_questions = []
    matches = re.findall(
        r'\\textbf\{\s*Question\s*([0-9]+)\.\}\s*(.*?)(?=\\pts|\\hfill|\\medskip|\\noindent|\\vfill|\\begin\{center\}|\Z)',
        content, re.DOTALL
    )
    for q_num, q_text in matches:
        cleaned = clean_text(q_text)
        short_notes_phrases = ["short notes on", "attempt any", "define or answer", "write notes on any"]
        skip = any(ph in cleaned.lower() for ph in short_notes_phrases)
        if len(cleaned) > 20 and not skip:
            main_questions.append(cleaned)

    return main_questions + parts_questions

def get_answer_key(subject_key, q_text):
    """Generate a rich markdown answer key for a Botany question."""
    q_lower = q_text.lower()
    title = BOTANY_SYLLABI.get(subject_key, {}).get("title", "Botany")

    # --- Cryptogams / Algae ---
    if "chlamydomonas" in q_lower:
        return ("1. **Habitat & Structure**: *Chlamydomonas* is a unicellular, biflagellate green alga found in freshwater, soil, and moist places. The cell has a cup-shaped chloroplast with a pyrenoid and a single nucleus.\n"
                "2. **Asexual Reproduction**: By zoospores or aplanospores formed inside the parent cell.\n"
                "3. **Sexual Reproduction**:\n- **Isogamy** (in some species): Morphologically identical gametes fuse.\n- **Anisogamy**: Gametes of different sizes fuse.\n- **Oogamy**: Large non-motile egg fused with small motile sperm.\n- The zygote forms a thick-walled zygospore that germinates under favourable conditions by meiosis, producing 4 haploid zoospores.")
    elif "volvox" in q_lower:
        return ("1. **Structure**: *Volvox* is a colonial green alga. The colony (coenobium) is a hollow sphere of thousands of biflagellate cells embedded in gelatinous matrix, connected by cytoplasmic strands.\n"
                "2. **Asexual Reproduction**: By daughter coenobia formed inside the parent colony. Special reproductive cells (gonidia) undergo repeated divisions.\n"
                "3. **Sexual Reproduction**: Oogamous. Antherozoids from antheridial cells fertilize a large, non-motile egg in the oogonium. The resulting zygote secretes a spiny wall and is released upon colony death.")
    elif "nostoc" in q_lower or "cyanobacter" in q_lower or "cyanophyceae" in q_lower or "cyanophyta" in q_lower:
        return ("1. **General Characters**: Cyanobacteria (blue-green algae) are prokaryotic. They lack membrane-bound organelles, possess phycobiliproteins (phycocyanin, phycoerythrin) as accessory pigments and chlorophyll *a*.\n"
                "2. **Nostoc Structure**: Filamentous; trichomes are unbranched and embedded in a gelatinous sheath. Contains vegetative cells and specialized **heterocysts** at intervals.\n"
                "3. **Heterocysts & Nitrogen Fixation**: Heterocysts are thick-walled, oxygen-free microenvironments housing the enzyme **nitrogenase**, which converts atmospheric N₂ to ammonia (NH₃), fixing nitrogen for plant use.\n"
                "4. **Reproduction**: By fragmentation (hormogonia) and akinetes (thick-walled resting spores).")
    elif "puccinia" in q_lower or "rust" in q_lower:
        return ("1. **Classification**: *Puccinia graminis* (black stem rust of wheat) is a Basidiomycete. It is an obligate parasite requiring **two alternate hosts**: wheat (*Triticum*) and barberry (*Berberis*).\n"
                "2. **Spore Stages (Life Cycle)**:\n- **Pycniospores (Spermatia)**: On barberry leaves. Receptive hyphae are fertilized by pycniospores.\n- **Aeciospores**: Dikaryotic (n+n) spores produced in aecia on barberry; infect wheat.\n- **Uredospores (repeating stage)**: Dikaryotic spores produced in uredinia on wheat; cause summer spread.\n- **Teliospores**: Two-celled, thick-walled resting spores on wheat; overwinter.\n- **Basidiospores**: Haploid; produced after karyogamy and meiosis; infect barberry.\n"
                "3. **Significance**: Causes massive wheat yield losses globally. Control via barberry eradication and resistant wheat varieties.")
    elif "marchantia" in q_lower:
        return ("1. **Morphology**: *Marchantia* is a thallose liverwort. Thallus is flat, dichotomously branched, dark green, with a midrib. **Air pores** open into photosynthetic chambers. Ventral scales and rhizoids anchor it.\n"
                "2. **Asexual Reproduction**: By gemmae produced in cup-shaped **gemma cups** on the dorsal surface. Gemmae are lens-shaped propagules dispersed by rain.\n"
                "3. **Sexual Reproduction**:\n- **Antheridiophore**: Umbrella-like male receptacle bearing antheridia.\n- **Archegoniophore**: Stalked, star-shaped female receptacle bearing archegonia.\n- Fertilization produces a zygote that develops into the sporophyte, consisting of foot, seta, and capsule.\n- The capsule dehisces to release elaters and haploid spores.")
    elif "selaginella" in q_lower:
        return ("1. **External Morphology**: Dorsiventral, branched stem with small leaves (microphylls) in four rows — two lateral rows of larger leaves and two median rows of smaller leaves. Rhizophores bear roots.\n"
                "2. **Strobili**: Cones with microsporophylls (bearing microsporangia with microspores) and megasporophylls (bearing megasporangia with 4 megaspores). This is **heterospory**.\n"
                "3. **Gametophyte**: The microspore develops into a male gametophyte entirely within the microspore wall (endosporous). The megaspore produces a female gametophyte bearing archegonia.\n"
                "4. **Significance**: *Selaginella* is an important phylogenetic link, showing the incipient stage of **seed habit** (retained megaspore germinating on parent plant).")
    elif "rhizopus" in q_lower:
        return ("1. **Structure**: *Rhizopus* (bread mold) is a coenocytic fungus (Phycomycetes). Hyphae are non-septate, bearing three types: stolons, rhizoids, and erect sporangiophores.\n"
                "2. **Asexual Reproduction**: Sporangiophores produce **sporangia** containing numerous haploid **sporangiospores** dispersed by wind.\n"
                "3. **Sexual Reproduction**: Zygosporic. Two compatible mating strains (+) and (-) form **progametangia** that fuse to form a **zygospore** (2n). The zygospore germinates to produce a sporangiophore with sporangiospores after meiosis.")
    elif "agaricus" in q_lower or "basidiomycet" in q_lower:
        return ("1. **Structure**: *Agaricus* (mushroom) has a mycelium of septate, dikaryotic (n+n) hyphae in the substrate. The **basidiocarp** has a pileus (cap), stipe (stalk), gills (lamellae), and annulus (ring).\n"
                "2. **Basidium**: Club-shaped fertile cell bearing 4 **basidiospores** on sterigmata after karyogamy and meiosis.\n"
                "3. **Life Cycle**: Primary (monokaryotic) mycelium + Primary mycelium → Secondary (dikaryotic) mycelium via plasmogamy → **Clamp connections** maintain dikaryon → Basidiocarp formation → Basidiospore discharge.")
    elif "equisetum" in q_lower:
        return ("1. **External Morphology**: *Equisetum* (horsetail) has jointed, ribbed, hollow stems with whorled, scale-like leaves. Strobili are terminal cones.\n"
                "2. **Anatomy of Internode**:\n- **Epidermis**: Silica-impregnated with stomata.\n- **Cortex**: Contains **chlorenchyma** (outer) and **carinal canals** (protoxylem canals associated with vascular bundles) and **vallecular canals** (air cavities).\n- **Vascular Bundles**: Conjunctive, in a ring around the **central canal** (pith lacuna).\n3. **Ecological & Evolutionary Significance**: A living fossil; once dominated Carboniferous coal forests. Xerophytic adaptations: reduced leaves, silicified epidermis, sunken stomata.")
    # --- Plant Physiology ---
    elif "stomata" in q_lower or "guard cell" in q_lower:
        return ("1. **Guard Cell Mechanism**: Guard cells are kidney-shaped (dicots) or dumbbell-shaped (monocots) cells that flank the stomatal pore.\n"
                "2. **K⁺ Pump Hypothesis (Levitt, 1974)**:\n- In **light**: Blue light activates H⁺-ATPase pumps in guard cell membrane → H⁺ pumped out → membrane hyperpolarizes → K⁺ channels open → K⁺ and Cl⁻ accumulate in guard cells → water potential decreases → water enters by osmosis → guard cells become turgid → pore **opens**.\n- In **dark**: K⁺ and Cl⁻ leave → guard cells become flaccid → pore **closes**.\n"
                "3. **ABA Role**: During water stress, ABA triggers Ca²⁺ release → K⁺ channels close → stomatal closure to reduce transpiration.")
    elif "c4 pathway" in q_lower or "hatch-slack" in q_lower or "c4 plant" in q_lower:
        return ("1. **Kranz Anatomy**: C4 plants (maize, sugarcane) have two concentric layers of photosynthetic cells: **mesophyll cells** and **bundle sheath cells**.\n"
                "2. **Mechanism**:\n- **Mesophyll (carboxylation)**: CO₂ is fixed by PEP carboxylase onto Phosphoenolpyruvate (PEP) to form Oxaloacetate (OAA, C4), then Malate.\n  `PEP + CO₂ → OAA → Malate`\n- **Transport**: Malate moves to bundle sheath cells via plasmodesmata.\n- **Bundle Sheath (decarboxylation)**: Malate is decarboxylated, releasing CO₂ for the Calvin cycle, and Pyruvate returns to mesophyll cells.\n- **Regeneration**: ATP consumed (by PPDK) to convert Pyruvate back to PEP.\n"
                "3. **Significance**: CO₂ is concentrated near RuBisCO → eliminates photorespiration → high photosynthetic efficiency at high temperatures and light intensities.")
    elif "auxin" in q_lower or "acid growth" in q_lower:
        return ("1. **Auxin (IAA)**: Synthesized in shoot apical meristems, young leaves, and seeds. Promotes cell elongation.\n"
                "2. **Acid Growth Hypothesis (Hager, 1971)**:\n- Auxin activates **H⁺-ATPase** in the plasma membrane.\n- H⁺ ions are pumped into the cell wall → cell wall **acidifies** (pH drops to ~5).\n- Acid pH activates wall-loosening enzymes (**expansins**) → hydrogen bonds in cellulose microfibrils are broken → cell wall extensibility increases.\n- Increased water potential gradient → water enters → **turgor pressure increases** → cell elongates.\n"
                "3. **Phototropism**: Unilateral light causes lateral auxin redistribution (Cholodny-Went theory) → higher auxin on shaded side → elongation on shaded side → shoot bends toward light.")
    elif "abscisic acid" in q_lower or "aba" in q_lower or "dormancy" in q_lower:
        return ("1. **ABA (Abscisic Acid)**: A terpenoid plant hormone synthesized in chloroplasts from xanthoxin. Called the 'stress hormone'.\n"
                "2. **Seed Dormancy**:\n- ABA accumulates in maturing seeds, inducing dormancy by suppressing germination-promoting proteins and inducing storage protein synthesis.\n- ABA inhibits water uptake and promotes accumulation of late embryogenesis abundant (LEA) proteins.\n"
                "3. **Breaking Dormancy**: Dormancy is broken when ABA levels fall and Gibberellin (GA) levels rise. GA promotes synthesis of α-amylase that mobilizes starch reserves.\n"
                "4. **Other Roles**: Stomatal closure during drought (via K⁺ channel modulation in guard cells), promotion of leaf senescence, and promotion of root growth under stress.")
    elif "phloem" in q_lower or "pressure flow" in q_lower:
        return ("1. **Mass Flow / Pressure Flow Hypothesis (Münch, 1930)**:\n"
                "2. **Loading at Source**: Photosynthetically active leaves load sucrose into sieve tubes via companion cells (symplastic or apoplastic pathway) → solute concentration in sieve element rises → water enters from xylem by osmosis → high hydrostatic pressure builds.\n"
                "3. **Unloading at Sink**: Sucrose is unloaded in sinks (roots, fruits) → concentration falls → water moves back to xylem → low hydrostatic pressure.\n"
                "4. **Pressure Gradient**: High pressure at source + low pressure at sink drives **bulk flow** of phloem sap from source to sink.\n"
                "5. **Evidence**: Aphid stylets inserted in sieve tubes exude sap under pressure. Girdling experiments confirm bidirectional flow above and below the girdle.")
    # --- Genetics ---
    elif "mendel" in q_lower or "law of segregation" in q_lower:
        return ("1. **Law of Segregation (1st Law)**: Individuals have two alleles for each trait. During gamete formation, the allele pairs separate and each gamete receives only one allele. Example: Monohybrid cross Tt × Tt → 1:2:1 (TT:Tt:tt) genotypic ratio, 3:1 phenotypic ratio.\n"
                "2. **Law of Independent Assortment (2nd Law)**: Alleles of different genes assort independently into gametes (for unlinked genes). Example: Dihybrid cross TtYy × TtYy → 9:3:3:1 phenotypic ratio.\n"
                "3. **Chromosome Basis (Sutton-Boveri)**: Chromosomes are the physical bearers of Mendelian factors. Segregation = separation of homologous chromosomes at Meiosis I. Independent assortment = random orientation of bivalents at metaphase I.")
    elif "linkage" in q_lower or "crossing over" in q_lower:
        return ("1. **Linkage**: Tendency of genes located on the same chromosome to remain together during inheritance; violates Mendel's Law of Independent Assortment.\n"
                "2. **Crossing Over**: Physical exchange of segments between non-sister chromatids of homologous chromosomes at the **chiasma** during pachytene of meiosis I, producing recombinant gametes.\n"
                "3. **Recombination Frequency**: `RF = (Recombinants / Total offspring) × 100%`. 1% RF = 1 centiMorgan (cM).\n"
                "4. **Chromosome Mapping**: RF values are used to construct genetic maps (Morgan). Mapping function (Haldane or Kosambi) corrects for double crossovers.")
    elif "polyploidy" in q_lower:
        return ("1. **Definition**: Polyploidy is the condition of having more than two complete sets of chromosomes.\n"
                "2. **Types**:\n- **Autopolyploidy**: Chromosome sets from the same species (e.g., triploid banana 3n=33; tetraploid potato 4n=48).\n- **Allopolyploidy**: Chromosome sets from different species combined by hybridization + chromosome doubling (e.g., *Raphanobrassica* from Raphanus + Brassica; bread wheat *T. aestivum* = 6n = 42, AABBDD).\n"
                "3. **Significance in Evolution**: Most angiosperm species have experienced ancient polyploidy events. Polyploidy gives new gene copies that can diverge in function → major driver of plant evolution and speciation.\n"
                "4. **Application**: Colchicine (spindle inhibitor) is used to induce polyploidy in crop breeding.")
    # --- Ecology ---
    elif "succession" in q_lower and "hydrosere" in q_lower:
        return ("1. **Ecological Succession**: Orderly, directional, and predictable replacement of plant communities in a specific area over time, leading to a stable **climax community**.\n"
                "2. **Hydrosere (Hydrarch Succession)**: Succession in an aquatic habitat (pond):\n- **Phytoplankton Stage**: Pioneer; tiny algae colonize open water.\n- **Submerged Macrophyte Stage**: Rooted plants like *Vallisneria*, *Hydrilla* colonize. Organic sediment accumulates.\n- **Floating Macrophyte Stage**: *Nymphaea*, *Nelumbo* shade out submerged species.\n- **Reed-Swamp Stage**: Emergent plants like *Typha* colonize; bogs form.\n- **Sedge-Meadow Stage**: *Carex* and grasses colonize drying bog.\n- **Woodland Stage**: Shrubs and trees like *Salix* colonize.\n- **Climax Forest Stage**: Stable mesophytic forest community.")
    elif "nitrogen cycle" in q_lower or "nitrogen fixation" in q_lower:
        return ("1. **Atmospheric Nitrogen (N₂)**: Constitutes ~78% of atmosphere; unavailable to most organisms.\n"
                "2. **Nitrogen Fixation**:\n- **Biological**: Carried out by free-living bacteria (*Azotobacter*, *Clostridium*) and symbiotic bacteria (*Rhizobium* in root nodules of legumes). Enzyme **nitrogenase** (requires Mo, Fe, O₂-free conditions) converts N₂ → NH₃.\n  `N₂ + 8H⁺ + 8e⁻ + 16ATP → 2NH₃ + H₂ + 16ADP + 16Pᵢ`\n- **Industrial (Haber-Bosch)**: N₂ + 3H₂ → 2NH₃ (high temperature/pressure, Fe catalyst).\n"
                "3. **Nitrification**: NH₃ → NO₂⁻ (*Nitrosomonas*) → NO₃⁻ (*Nitrobacter*).\n"
                "4. **Denitrification**: NO₃⁻ → N₂ by *Pseudomonas* under anaerobic conditions, completing the cycle.")
    elif "pollution" in q_lower or "air pollution" in q_lower:
        return ("1. **Primary Pollutants**: SO₂, NOₓ, CO, particulates, hydrocarbons — directly emitted from combustion sources.\n"
                "2. **Effects on Plants**:\n- **SO₂**: Reacts with water → sulphurous acid → chlorophyll degradation, necrosis. *Lichens* are sensitive bioindicators.\n- **Ozone (O₃)**: Secondary pollutant; damages membranes, accelerates senescence (stippling and tip-burn).\n- **Acid Rain (pH < 5.6)**: Formed by SO₂ + NOₓ + water → leaches nutrients from soil, damages cuticle.\n- **Particulates**: Block stomata, reduce photosynthesis.\n"
                "3. **Bioindicators**: Species sensitive to pollutants (lichens, mosses) are used as biological indicators of air quality.")
    elif "tissue culture" in q_lower or "somatic embryogenesis" in q_lower:
        return ("1. **Totipotency**: Each somatic cell retains the genetic information to regenerate into a complete organism. This is the basis of tissue culture.\n"
                "2. **Basic Protocol**:\n- **Explant** (leaf disc, shoot tip, root tip) is surface-sterilized.\n- Cultured on **MS (Murashige-Skoog) medium** with appropriate auxin/cytokinin ratio.\n- High auxin:cytokinin → callus / root induction.\n- Low auxin:cytokinin → shoot induction (organogenesis).\n"
                "3. **Somatic Embryogenesis**: Callus or single cells develop into somatic embryos (resembling zygotic embryos) and regenerate into plants.\n"
                "4. **Applications**: Rapid clonal propagation, disease-free plantlets (meristem culture), embryo rescue, germplasm conservation, and production of secondary metabolites.")
    elif "polymerase chain reaction" in q_lower or "pcr" in q_lower:
        return ("1. **Purpose**: *In vitro* amplification of specific DNA sequences using thermostable DNA polymerase (*Taq* polymerase).\n"
                "2. **Steps (Thermal Cycling)**:\n- **Denaturation**: 94-96°C — double-stranded DNA melts into single strands.\n- **Annealing**: 50-65°C — specific primers (short oligonucleotides) bind to complementary template sequences.\n- **Extension**: 72°C — Taq polymerase extends primers, synthesizing new DNA strand.\n- Each cycle doubles the amount of target DNA. After **30-35 cycles**, >10⁹-fold amplification.\n"
                "3. **Applications**: DNA diagnostics, forensic DNA profiling, genotyping, gene cloning, detecting pathogens (RT-PCR for RNA viruses), and genetic engineering.")
    elif "agrobacterium" in q_lower:
        return ("1. **Pathogenesis**: *Agrobacterium tumefaciens* causes **Crown Gall disease**. The Ti (Tumour-inducing) plasmid carries T-DNA (transferred DNA) which is stably integrated into the host plant chromosome.\n"
                "2. **Mechanism of Transformation**:\n- VirD2/VirD1 proteins nick the T-DNA borders, excising single-stranded T-DNA.\n- T-DNA–VirE2 (sssDNA binding protein) complex enters the plant cell via the type IV secretion system.\n- T-DNA integrates randomly into the plant nuclear genome.\n- T-DNA encodes: auxin and cytokinin synthesis genes (cause tumor) + opine synthesis genes (nutritional benefit to Agrobacterium).\n"
                "3. **Biotechnology**: Ti plasmid is disarmed (disease-causing T-DNA removed) and used as a natural vector to deliver foreign genes into plant cells for creating **transgenic plants**.")
    # Generic Botany Fallback
    else:
        return (
            f"1. **Core Concept**:\n"
            f"- Covers an important topic within {title}.\n"
            f"2. **Key Definitions & Mechanisms**:\n"
            f"- Define the central concept with precise botanical terminology.\n"
            f"- Describe the structural, physiological, or genetic mechanism involved.\n"
            f"3. **Diagrams**: Draw and label the relevant structures (e.g., cell organelles, life cycle stages, anatomical cross-sections) to support the answer.\n"
            f"4. **Significance / Applications**:\n"
            f"- Explain the ecological, evolutionary, or applied significance of the concept in the context of Plant Sciences."
        )


def main():
    tex_dir = "aaa/BOTANY"
    if not os.path.exists(tex_dir):
        print(f"ERROR: Botany folder not found at {tex_dir}")
        return

    # 1. Initialize raw question dictionaries
    raw_questions = {k: [] for k in BOTANY_SYLLABI.keys()}

    # 2. Scan and parse all LaTeX files
    files = sorted([f for f in os.listdir(tex_dir) if f.endswith(".tex")])
    print(f"Scanning {len(files)} Botany LaTeX files...")

    for file_name in files:
        code = get_code_from_filename(file_name)
        if not code:
            print(f"  SKIP (no code): {file_name}")
            continue
        ekey = FILE_TO_KEY.get(code)
        if not ekey:
            print(f"  SKIP (no mapping for {code}): {file_name}")
            continue
        filepath = os.path.join(tex_dir, file_name)
        qs = parse_tex_file(filepath)
        raw_questions[ekey].extend(qs)
        print(f"  Parsed {len(qs)} questions from {file_name} -> {ekey}")

    # 3. Load exams-data.js
    exams_js_path = "js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])

    # 4. Generate 50 questions per key
    print("\nBuilding question banks (50 questions per course)...")
    for unique_key, active_list in UNIQUE_TO_ACTIVE.items():
        syllabus = BOTANY_SYLLABI.get(unique_key, {})
        raw_qs = raw_questions.get(unique_key, [])
        standard_qs = syllabus.get("standard_questions", [])

        seen = set()
        final_questions = []
        for q_text in raw_qs:
            q_norm = q_text.lower().strip()
            if q_norm not in seen and len(q_text) > 20:
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

        # Fallback pad
        fallback_idx = 1
        title_text = syllabus.get("title", unique_key.upper())
        while len(final_questions) < 50:
            q_text = f"Describe the fundamental principles, experimental methods, and significance of {title_text} (Part {fallback_idx})."
            final_questions.append((q_text, "V"))
            fallback_idx += 1

        final_questions = final_questions[:50]

        # Format questions
        formatted_questions = []
        for idx, item in enumerate(final_questions):
            q_id = idx + 1
            if isinstance(item, tuple):
                q_text, unit = item
            else:
                q_text = item
                unit_num = (idx // 10) + 1
                unit_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
                unit = unit_romans.get(unit_num, "V")

            ans_key = get_answer_key(unique_key, q_text)
            formatted_questions.append({
                "id": q_id,
                "unit": unit,
                "question": q_text,
                "answerKey": ans_key
            })

        # Inject into EXAMS for all active keys
        for active_key in active_list:
            orig = EXAMS.get(active_key, {})
            EXAMS[active_key] = {
                "id": active_key,
                "title": orig.get("title") or syllabus.get("title", active_key.upper()),
                "module": syllabus.get("module", active_key.upper()),
                "duration": 60,
                "type": "theory",
                "comingSoon": False,
                "questions": formatted_questions
            }
            print(f"  {active_key}: populated with {len(formatted_questions)} questions")

    # 5. Save exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)
    print("\njs/exams-data.js updated successfully!")

    # 6. Build EXAM_PYQS block for subjects.html
    print("\nBuilding subjects.html EXAM_PYQS mappings for Botany...")
    subjects_path = "subjects.html"
    with open(subjects_path, "r", encoding="utf-8") as f:
        subjects_content = f.read()

    # Build botany pyqs entries
    pyq_entries = {}
    for file_name in sorted(files):
        code = get_code_from_filename(file_name)
        if not code:
            continue
        ekey = FILE_TO_KEY.get(code)
        if not ekey:
            continue
        file_path = f"aaa/BOTANY/{file_name}"
        # Year extraction
        year_m = re.search(r'(\d{4}[-_]\d{2,4}|\d{4})', file_name)
        year = year_m.group(1) if year_m else "Unknown"
        title = BOTANY_SYLLABI.get(ekey, {}).get("title", code)
        entry = {
            "title": f"{title} {year} LaTeX Code",
            "file": file_path,
            "description": f"Official {code} {title} {year} LaTeX Paper"
        }
        if ekey not in pyq_entries:
            pyq_entries[ekey] = []
        pyq_entries[ekey].append(entry)

    # Build the JS snippet to inject
    new_pyq_block_lines = []
    for key, entries in sorted(pyq_entries.items()):
        serialized_entries = json.dumps(entries, indent=8)
        # Fix indentation
        serialized_entries = serialized_entries.replace('\n', '\n        ')
        new_pyq_block_lines.append(f'        "{key}": {serialized_entries}')

    new_pyq_block = ",\n".join(new_pyq_block_lines)

    # Find the end of EXAM_PYQS block (closing };) and inject before it
    start_marker = 'const EXAM_PYQS = {'
    end_marker = '\n    };'

    start_idx = subjects_content.find(start_marker)
    if start_idx == -1:
        print("ERROR: Could not find EXAM_PYQS in subjects.html")
        return

    # Find first occurrence of end_marker after start_idx
    end_idx = subjects_content.find(end_marker, start_idx)
    if end_idx == -1:
        print("ERROR: Could not find end of EXAM_PYQS in subjects.html")
        return

    # Check if botany keys already exist
    botany_already = 'bobmj11' in subjects_content
    if botany_already:
        print("Botany entries already present in subjects.html — skipping injection.")
    else:
        # Insert before the closing };
        insert_point = end_idx
        new_entries_str = ",\n" + new_pyq_block
        subjects_content = subjects_content[:insert_point] + new_entries_str + subjects_content[insert_point:]
        print(f"  Injected {sum(len(v) for v in pyq_entries.values())} Botany PYQ entries into subjects.html")

    # 7. Update isTargetDept to include bob and imb
    old_target = "key.startsWith('mat') || key.startsWith('phy') || key.startsWith('chem') || key.startsWith('sta') || key.startsWith('ggr');"
    new_target = "key.startsWith('mat') || key.startsWith('phy') || key.startsWith('chem') || key.startsWith('sta') || key.startsWith('ggr') || key.startsWith('bob') || key.startsWith('imb');"
    if old_target in subjects_content:
        subjects_content = subjects_content.replace(old_target, new_target)
        print("  Updated isTargetDept filter to include Botany/IMB keys.")
    else:
        print("  NOTE: isTargetDept may already be updated or not found.")

    with open(subjects_path, "w", encoding="utf-8") as f:
        f.write(subjects_content)
    print("subjects.html updated successfully!")

    print("\n=== All Done! ===\n")
    print("Next steps (manual):")
    print("  1. Update js/nep-data.js with Botany paper metadata")
    print("  2. Update nep-papers.html deptLabels and NEP_COURSE_NAMES")
    print("  3. Update nep-science.html to activate the Botany button")

if __name__ == "__main__":
    main()
