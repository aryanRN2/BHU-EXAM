import json
import re
import os

# 1. Define Geography Syllabi and standard questions for padding to 50
GEOGRAPHY_SYLLABI = {
    "ggrmj11": {
        "title": "Physical Geography",
        "standard_questions": [
            ("Describe the solar system, including the characteristics of inner and outer planets.", "I"),
            ("Explain the earth's rotation and its physical relevance, including day/night and Coriolis effect.", "I"),
            ("Discuss the composition and vertical structure of the atmosphere with a neat diagram.", "II"),
            ("Explain the concept of heat budget of the earth and the factors influencing insolation.", "II"),
            ("What is weathering? Differentiate between mechanical and chemical weathering with examples.", "III"),
            ("Present a detailed account of the landforms produced by river erosion and deposition.", "III"),
            ("Discuss the plate tectonics theory and its role in mountain building and earthquakes.", "IV"),
            ("Explain the distribution of temperature and salinity in oceanic waters.", "IV"),
            ("Describe the ocean currents of the Indian Ocean and explain how they change with monsoons.", "V"),
            ("Discuss the origin and characteristics of tropical and temperate cyclones.", "II"),
            ("Explain the continental drift theory of Alfred Wegener and the evidence supporting it.", "IV"),
            ("Discuss the rock cycle and the process of formation of igneous, sedimentary, and metamorphic rocks.", "III"),
            ("Explain the origin of tides and the difference between spring and neap tides.", "V"),
            ("Discuss the tetrahedral theory of Lowthian Green regarding the distribution of land and water.", "I"),
            ("Describe the landforms created by wind action in arid and semi-arid regions.", "III")
        ]
    },
    "ggrmj21": {
        "title": "Human Geography",
        "standard_questions": [
            ("Discuss the meaning, nature, and scope of Human Geography.", "I"),
            ("Critically examine the concept of Environmental Determinism with examples.", "I"),
            ("Explain the concept of Possibilism and Neo-Determinism (Stop-and-Go Determinism).", "I"),
            ("Classify the major human races of the world and discuss their physical traits.", "II"),
            ("Discuss the distribution, habitat, economy, and society of the Bushman tribe.", "II"),
            ("Explain the push and pull factors of human migration with relevant examples.", "III"),
            ("Describe Ravenstein's laws of migration and their relevance in the modern world.", "III"),
            ("Discuss the causes and consequences of world population growth in recent decades.", "IV"),
            ("Explain the demographic transition theory and discuss its different stages.", "IV"),
            ("Describe the major types and regional patterns of rural settlements.", "V"),
            ("Discuss the environmental factors influencing rural house types in India.", "V"),
            ("Explain the functional classification of towns as proposed by Harris and others.", "V"),
            ("Discuss the global distribution of human population and factors affecting density.", "IV"),
            ("Explain the social and economic characteristics of Eskimo adaptation to cold environment.", "II"),
            ("Describe the sector model of urban structure proposed by Homer Hoyt.", "V")
        ]
    },
    "ggrse11": {
        "title": "Man and Environment",
        "standard_questions": [
            ("Define ecosystem and explain the flow of energy through different trophic levels.", "I"),
            ("Explain the dynamic relationship between man and environment over different historical stages.", "I"),
            ("Discuss the causes, consequences, and control measures of deforestation.", "II"),
            ("Describe the phenomenon of global warming and its impact on the global climate.", "III"),
            ("Explain the concept of sustainable development and suggest measures for its achievement.", "IV"),
            ("Discuss the impact of industrialization and urbanization on water resources.", "II"),
            ("Describe the structure and functions of food chains and food webs in an ecosystem.", "I"),
            ("Explain the causes and mitigation strategies for desertification in arid regions.", "II"),
            ("Discuss the concept of acid rain, its sources, and its ecological consequences.", "III"),
            ("Explain the biogeochemical cycles, focusing on the carbon and nitrogen cycles.", "I"),
            ("Discuss environmental ethics and the role of local communities in biodiversity conservation.", "IV"),
            ("Describe the causes and impact of air pollution on human health in urban areas.", "II"),
            ("Explain the concept of carrying capacity of the environment.", "IV"),
            ("Discuss the major environmental challenges associated with modern agricultural practices.", "II"),
            ("Describe the ozone layer depletion mechanism and the international protocols to control it.", "III")
        ]
    },
    "ggrmj31": {
        "title": "Economic Geography",
        "standard_questions": [
            ("Discuss the meaning, scope, and approaches of Economic Geography.", "I"),
            ("Classify natural resources and discuss the importance of resource conservation.", "I"),
            ("Critically examine von Thünen's theory of agricultural location and land rent.", "II"),
            ("Discuss the factors influencing the location of iron and steel industries in the world.", "III"),
            ("Critically analyze Alfred Weber's theory of industrial location.", "III"),
            ("Describe the major agricultural systems of the world as classified by Whittlesey.", "II"),
            ("Discuss the impact of globalization on international trade and economic development.", "IV"),
            ("Explain the role of transportation networks in regional economic growth.", "IV"),
            ("Discuss the distribution and production of coal and petroleum in the world.", "I"),
            ("Describe the characteristics and distribution of plantation agriculture.", "II"),
            ("Explain the concept of resource appraisal and how technology affects resource availability.", "I"),
            ("Discuss the location factors and distribution of cotton textile industries.", "III"),
            ("Explain the Rostow model of stages of economic growth.", "IV"),
            ("Discuss the spatial patterns of commercial dairy farming in the world.", "II"),
            ("Explain the WTO's role in regulating international trade and its impact on developing nations.", "V")
        ]
    },
    "ggrmj52": {
        "title": "World Regional Geography",
        "standard_questions": [
            ("Divide the United States of America into major physiographic regions and describe them.", "I"),
            ("Discuss the agricultural belts of the USA and explain their economic significance.", "II"),
            ("Describe the location, growth, and characteristics of the Manufacturing Belt of the USA.", "III"),
            ("Provide a detailed physiographic division of the People's Republic of China.", "I"),
            ("Discuss the agricultural regions of China and their productivity patterns.", "II"),
            ("Explain the growth and spatial distribution of heavy industries in China.", "III"),
            ("Provide a comparative study of the demographic characteristics of the USA and China.", "IV"),
            ("Discuss the regional disparities and economic planning models in China.", "V"),
            ("Describe the mineral and energy resource base of the USA.", "I"),
            ("Explain the significance of the Great Lakes region in the industrial development of North America.", "III"),
            ("Discuss the urban-industrial development of the Yangtze Valley region.", "III"),
            ("Describe the climate zones and soil types of the USA.", "I"),
            ("Discuss the development and distribution of the electronics industry in the Silicon Valley.", "III"),
            ("Explain the agricultural reforms in China since 1978 and their impact on regional development.", "V"),
            ("Provide an account of the regional geography of the Appalachian region.", "I")
        ]
    },
    "ggrmj43": {
        "title": "Geomorphology",
        "standard_questions": [
            ("Discuss the interior structure of the earth based on seismological evidence.", "I"),
            ("Critically examine Wegener's theory of Continental Drift and its evidence.", "I"),
            ("Explain the concept of Isostasy as proposed by Pratt and Airy.", "II"),
            ("Discuss the plate tectonics theory, explaining convergent, divergent, and transform boundaries.", "III"),
            ("Critically examine Kober's geosynclinal theory of mountain building.", "II"),
            ("Discuss Holmes' thermal convection current theory of mountain building.", "II"),
            ("Differentiate between endogenetic and exogenetic earth movements with examples.", "IV"),
            ("Describe the cycle of erosion as proposed by William Morris Davis.", "IV"),
            ("Explain the Penckian model of landform development and compare it with Davis' model.", "IV"),
            ("Describe the landforms associated with karst (groundwater) topography.", "V"),
            ("Discuss the mechanism of glacier movement and the landforms formed by glacial erosion.", "V"),
            ("Explain the formation of fold mountains with appropriate diagrams.", "II"),
            ("Describe the characteristics and distribution of major plate boundaries in the world.", "III"),
            ("Discuss the geomorphic processes involved in the development of arid (aeolian) landscapes.", "V"),
            ("Explain the causes and classification of faults and associated landforms.", "IV")
        ]
    },
    "ggrmj33": {
        "title": "Geography of India",
        "standard_questions": [
            ("Divide India into major physiographic regions and discuss the features of the Great Himalayas.", "I"),
            ("Provide a comparative account of the Himalayan and Peninsular river systems of India.", "I"),
            ("Discuss the origin, mechanism, and characteristics of the Indian Summer Monsoon.", "II"),
            ("Classify the soils of India and discuss the problems and conservation of Indian soils.", "II"),
            ("Discuss the distribution and classification of natural vegetation in India.", "II"),
            ("Explain the problems, prospects, and regional distribution of rice cultivation in India.", "III"),
            ("Discuss the production, distribution, and conservation of iron ore resources in India.", "IV"),
            ("Explain the distribution and growth patterns of population in India.", "IV"),
            ("Discuss the location and factors responsible for the concentration of cotton textile industry in Mumbai and Gujarat.", "V"),
            ("Explain the concept of regional planning in India and the role of river valley projects.", "V"),
            ("Describe the features and significance of the Indo-Gangetic Plains.", "I"),
            ("Discuss the origin and characteristics of tropical cyclones affecting the Indian coasts.", "II"),
            ("Explain the problems and regional impact of the Green Revolution in India.", "III"),
            ("Discuss the distribution, reserves, and production of coal in India.", "IV"),
            ("Describe the characteristics and issues of urbanization in India.", "IV")
        ]
    },
    "ggrmj62": {
        "title": "Oceanography",
        "standard_questions": [
            ("Describe the general bottom topography of the Atlantic Ocean.", "I"),
            ("Discuss the factors influencing the horizontal and vertical distribution of salinity in oceans.", "II"),
            ("Describe the currents of the Pacific Ocean and explain their impact on regional climate.", "III"),
            ("Explain the origin and features of ocean tides.", "III"),
            ("Critically examine Darwin's subsidence theory of the origin of coral reefs.", "IV"),
            ("Explain Daly's glacial control theory of the origin of coral reefs.", "IV"),
            ("Classify marine deposits based on their origin and discuss pelagic deposits.", "V"),
            ("Describe the bottom topography of the Indian Ocean.", "I"),
            ("Discuss the factors affecting the temperature distribution of ocean waters.", "II"),
            ("Explain the phenomenon of upwelling and its biological significance.", "V"),
            ("Discuss the ecological conditions required for the growth of coral reefs.", "IV"),
            ("Describe the warm and cold currents of the Atlantic Ocean.", "III"),
            ("Explain the concept of deep sea trenches and their association with subduction zones.", "I"),
            ("Differentiate between terrigenous and pelagic deposits.", "V"),
            ("Discuss the potential of marine resources (living and non-living) for the future.", "V")
        ]
    },
    "ggrmj53": {
        "title": "Population Geography",
        "standard_questions": [
            ("Discuss the nature, scope, and development of Population Geography.", "I"),
            ("Explain the global factors influencing the uneven distribution and density of population.", "I"),
            ("Critically analyze Malthusian theory of population growth and its criticisms.", "II"),
            ("Explain the Demographic Transition Theory and discuss its stages and applicability.", "II"),
            ("Discuss the trends and consequences of rapid population growth in developing nations.", "III"),
            ("Discuss the age-sex composition of population and its socioeconomic implications.", "III"),
            ("Define migration and explain Lee's push-pull theory of migration.", "IV"),
            ("Discuss the causes, trends, and patterns of rural-urban migration in developing countries.", "IV"),
            ("Discuss the concept of overpopulation, underpopulation, and optimum population.", "V"),
            ("Describe the population policies of India and discuss their achievements.", "V"),
            ("Explain the concept of demographic dividend and how it can be utilized.", "III"),
            ("Discuss the measurement of mortality and fertility indicators.", "II"),
            ("Describe the characteristics of population distribution in Asia.", "I"),
            ("Discuss the social and economic impact of brain drain (migration of skilled labor).", "IV"),
            ("Explain the classification of population pyramids and their shapes.", "III")
        ]
    },
    "ggrmj83f": {
        "title": "Agriculture Geography",
        "standard_questions": [
            ("Discuss the nature, scope, and significance of Agricultural Geography.", "I"),
            ("Explain the physical and socio-economic determinants of agricultural land use.", "I"),
            ("Critically analyze von Thünen's model of agricultural location.", "II"),
            ("Discuss the Whittlesey classification of major agricultural regions of the world.", "II"),
            ("Explain the concept of agricultural productivity and techniques to measure it.", "III"),
            ("Discuss the regional characteristics and problems of subsistence crop farming.", "IV"),
            ("Explain the features, distribution, and problems of plantation agriculture in the tropics.", "IV"),
            ("Discuss the concept of agricultural regionalization and its methods.", "V"),
            ("Discuss the environmental impacts of the Green Revolution, including soil degradation and groundwater depletion.", "V"),
            ("Explain the concept of food security and discuss global challenges to food availability.", "III"),
            ("Discuss the characteristics and distribution of nomadic herding in the world.", "II"),
            ("Explain the methods of land use survey and land capability classification.", "I"),
            ("Discuss the role of irrigation in changing agricultural patterns in dry regions.", "V"),
            ("Describe the features of commercial grain farming in temperate grasslands.", "IV"),
            ("Explain the concept of agricultural diversification and its measurement.", "III")
        ]
    },
    "ggrmj51": {
        "title": "Climatology",
        "standard_questions": [
            ("Discuss the composition and vertical structure of the atmosphere.", "I"),
            ("Explain the concept of insolation and the factors affecting its distribution on earth.", "I"),
            ("Describe the global pressure belts and planetary wind systems of the earth.", "II"),
            ("Discuss the origin, mechanism, and distribution of monsoons.", "II"),
            ("Explain the concept of air masses, their classification, and source regions.", "III"),
            ("Discuss the structure, origin, and weather conditions associated with temperate cyclones.", "III"),
            ("Critically analyze Koppen's scheme of world climatic classification.", "IV"),
            ("Discuss Thornthwaite's climatic classification scheme of 1948.", "IV"),
            ("Explain the heat budget of the earth with a detailed diagram.", "I"),
            ("Describe the formation and types of fronts (warm, cold, stationary, occluded).", "III"),
            ("Discuss the differences between tropical and temperate cyclones.", "III"),
            ("Explain the greenhouse effect and discuss the role of greenhouse gases in global climate change.", "V"),
            ("Describe the vertical temperature distribution in the atmosphere and temperature inversion.", "I"),
            ("Discuss the concept of atmospheric moisture, condensation, and types of precipitation.", "V"),
            ("Explain the El Niño Southern Oscillation (ENSO) and its impact on global weather patterns.", "V")
        ]
    },
    "ggrmj41": {
        "title": "Evolution of Geographical Thought",
        "standard_questions": [
            ("Discuss the contributions of ancient Greek geographers in the development of geography.", "I"),
            ("Provide an account of the contribution of Roman geographers, focusing on Strabo and Ptolemy.", "I"),
            ("Describe the contributions of Arab scholars during the medieval period in geography.", "II"),
            ("Critically evaluate Alexander von Humboldt as a founder of modern geography.", "III"),
            ("Discuss Carl Ritter's contributions and his teleological approach to geography.", "III"),
            ("Explain the French school of geography, focusing on Vidal de la Blache and Possibilism.", "IV"),
            ("Discuss the German school of geography, focusing on Friedrich Ratzel and Anthropogeography.", "IV"),
            ("Explain the concept of dichotomy/dualism in geography, particularly physical vs. human and systematic vs. regional.", "IV"),
            ("Discuss the Quantitative Revolution in geography, its merits, and limitations.", "V"),
            ("Discuss the evolution of geographical studies in India during ancient and modern times.", "V"),
            ("Describe the concept of areal differentiation proposed by Richard Hartshorne.", "V"),
            ("Discuss the environmental determinism of Ellen Churchill Semple.", "IV"),
            ("Explain the behavioral and radical approaches in modern geographical thought.", "V"),
            ("Discuss the contribution of Hecataeus and Herodotus to geography.", "I"),
            ("Provide an account of the development of geography during the Age of Discovery.", "II")
        ]
    },
    "ggrmj74d": {
        "title": "Regional Planning",
        "standard_questions": [
            ("Define region and discuss the classification of formal, functional, and planning regions.", "I"),
            ("Explain the concept, objectives, and scope of Regional Planning.", "I"),
            ("Critically examine Perroux's Growth Pole Theory and its modifications.", "II"),
            ("Discuss Myrdal's Cumulative Causation Theory and its relevance to regional disparities.", "II"),
            ("Describe the regional development models of John Friedmann (core-periphery model).", "III"),
            ("Explain the methods of measuring regional disparities in a country.", "III"),
            ("Discuss the regional planning policies and disparities in India.", "IV"),
            ("Explain the concept of sustainable regional development with suitable examples.", "V"),
            ("Describe the role of growth centers and growth service centers in rural development.", "IV"),
            ("Discuss the planning of backward areas, focusing on drought-prone and hill areas.", "V"),
            ("Explain the concept of decentralization in planning (panchayati raj system in India).", "IV"),
            ("Discuss the concept of agro-climatic regional planning in India.", "V"),
            ("Provide a critical analysis of Albert Hirschman's theory of unbalanced growth.", "II"),
            ("Explain the role of metropolitan regions in national economic planning.", "I"),
            ("Describe the resource-based regional planning approach.", "V")
        ]
    },
    "ggrmj65b": {
        "title": "Geography of Settlement",
        "standard_questions": [
            ("Discuss the definition, nature, and scope of Settlement Geography.", "I"),
            ("Differentiate between rural and urban settlements in terms of structure and function.", "I"),
            ("Discuss the physical and socio-economic factors affecting the location of rural settlements.", "II"),
            ("Describe the major types (clustered, dispersed, semi-sprinkled) and geometric patterns of rural settlements.", "II"),
            ("Critically examine Walter Christaller's Central Place Theory (marketing, transport, and administrative principles).", "III"),
            ("Discuss August Lösch's modification of the Central Place Theory.", "III"),
            ("Describe the concentric zone model of urban land use proposed by E.W. Burgess.", "IV"),
            ("Explain the multiple nuclei model of urban structure proposed by Harris and Ullman.", "IV"),
            ("Discuss the characteristics and environmental problems of slums in developing countries.", "V"),
            ("Explain the concept of rural-urban fringe, its characteristics, and planning issues.", "V"),
            ("Discuss the house types in rural India and their relationship with local environment.", "II"),
            ("Describe the urban hierarchy based on the rank-size rule.", "III"),
            ("Explain the concept of smart cities and the urban planning challenges in India.", "V"),
            ("Describe the geographic factors influencing the morphology of Indian cities.", "IV"),
            ("Discuss the issues of rural settlement transformation under economic development.", "II")
        ]
    },
    "ggrse21": {
        "title": "Basics of Remote Sensing",
        "standard_questions": [
            ("Define Remote Sensing and explain the physical principles of Electromagnetic Radiation (EMR).", "I"),
            ("Describe the interaction mechanism of Electromagnetic Radiation with the atmosphere.", "I"),
            ("Explain how EMR interacts with different earth surface features (water, vegetation, soil).", "II"),
            ("Classify sensors used in remote sensing (active vs. passive, imaging vs. non-imaging).", "II"),
            ("Explain the characteristics of different remote sensing platforms (balloon, aircraft, satellite).", "III"),
            ("Explain the concept of orbital characteristics, differentiating between sun-synchronous and geostationary orbits.", "III"),
            ("Differentiate between spatial, spectral, radiometric, and temporal resolutions with examples.", "IV"),
            ("Discuss the elements of visual image interpretation (tone, texture, pattern, shape, size).", "IV"),
            ("Explain the digital image processing techniques, focusing on image enhancement and classification.", "V"),
            ("Discuss the applications of remote sensing in forest resource management and environmental monitoring.", "V"),
            ("Explain Rayleigh and Mie scattering and their effect on remote sensing data.", "I"),
            ("Describe the characteristics of IRS (Indian Remote Sensing) satellites and sensors.", "III"),
            ("Explain the applications of remote sensing in agriculture and crop yield estimation.", "V"),
            ("Differentiate between oblique and vertical aerial photographs.", "IV"),
            ("Discuss the role of Geographic Information Systems (GIS) in integration with remote sensing data.", "V")
        ]
    }
}

# Add minor and re-registered keys that inherit the same database
UNIQUE_TO_ACTIVE = {
    "ggrmj11": ["ggrmj11", "ggrmn11", "ggrmd11"],
    "ggrmj21": ["ggrmj21", "ggrmn21"],
    "ggrse11": ["ggrse11"],
    "ggrmj31": ["ggrmj31"],
    "ggrmj52": ["ggrmj52"],
    "ggrmj43": ["ggrmj43", "ggrmj83i"],
    "ggrmj33": ["ggrmj33"],
    "ggrmj62": ["ggrmj62"],
    "ggrmj53": ["ggrmj53", "ggrmj74b", "ggrmj7r4b"],
    "ggrmj83f": ["ggrmj83f"],
    "ggrmj51": ["ggrmj51"],
    "ggrmj41": ["ggrmj41", "ggrmj74a", "ggrmj7r4a"],
    "ggrmj74d": ["ggrmj74d", "ggrmj7r4d"],
    "ggrmj65b": ["ggrmj65b"],
    "ggrse21": ["ggrse21"]
}

# Custom detailed answer keys matching keywords in questions
def get_custom_answer_key(key, question):
    q_lower = question.lower()
    
    # 1. Basics of Remote Sensing / EMR
    if "scattering" in q_lower or "rayleigh" in q_lower or "mie" in q_lower:
        return (
            "1. **Atmospheric Scattering**:\n"
            "- Occurs when electromagnetic radiation (EMR) interacts with gases, dust, and aerosols in the atmosphere, deflecting it from its path.\n"
            "- **Rayleigh Scattering**: Occurs when particles are much smaller than EMR wavelength (e.g., nitrogen and oxygen molecules). Intensity is inversely proportional to the fourth power of wavelength ($I \\propto 1/\\lambda^4$). This explains why the sky is blue (shorter blue wavelengths scatter more) and orange/red at sunset (longer path length filters out blue).\n"
            "- **Mie Scattering**: Occurs when particles are roughly equal in size to EMR wavelength (e.g., water droplets, dust, pollen). Affects longer wavelengths more than Rayleigh scattering; causes clouds/haze to appear white/grey because all visible wavelengths are scattered equally.\n"
            "- **Non-Selective Scattering**: Occurs when particles are much larger than EMR wavelength (e.g., large water droplets, ice crystals). Scatters all wavelengths non-selectively.\n"
            "2. **Impact on Remote Sensing**:\n"
            "- Scattering reduces contrast in satellite images, producing an atmospheric 'haze' that must be corrected using digital image processing before analysis."
        )
        
    elif "sensor" in q_lower or "resolution" in q_lower or "platform" in q_lower:
        return (
            "1. **Remote Sensing Sensors**:\n"
            "- **Active Sensors**: Provide their own energy source for illumination (e.g., RADAR, LiDAR, SONAR). Can operate day and night and penetrate clouds.\n"
            "- **Passive Sensors**: Detect natural energy (reflected sunlight or thermal emission) from the Earth's surface (e.g., multispectral cameras, radiometers). Restricted to daylight and clear weather.\n"
            "2. **Resolutions in Remote Sensing**:\n"
            "- **Spatial Resolution**: The size of the smallest object distinguishable on the ground (pixel size, e.g., 10m vs. 30m).\n"
            "- **Spectral Resolution**: The ability of a sensor to define fine wavelength intervals (number and width of spectral bands).\n"
            "- **Radiometric Resolution**: The sensitivity of the sensor to small differences in electromagnetic energy (measured in bits, e.g., 8-bit = 256 levels, 11-bit = 2048 levels).\n"
            "- **Temporal Resolution**: The revisit time (revisit frequency) of the satellite over the same geographic location (e.g., every 16 days).\n"
            "3. **Platforms**:\n"
            "- Air-borne (balloons, UAVs/drones, aircraft) for local high-resolution surveys.\n"
            "- Space-borne (satellites in Sun-synchronous or Geostationary orbits) for regional and global monitoring."
        )

    elif "electromagnetic" in q_lower or "emr" in q_lower or "interaction" in q_lower:
        return (
            "1. **Electromagnetic Radiation (EMR)**:\n"
            "- EMR is a dynamic form of energy propagating through space as wave-particle packets (photons). Governed by wave equations where velocity is speed of light ($c = \\nu \\lambda$).\n"
            "2. **Atmospheric Interaction**:\n"
            "- **Absorption**: Major atmospheric gases ($CO_2$, $H_2O$, $O_3$) absorb specific EMR wavelengths, creating 'absorption bands'. Wavelength bands where EMR passes unabsorbed are called **Atmospheric Windows** (essential for sensors).\n"
            "- **Scattering**: Redirection of EMR by particles (Rayleigh, Mie, non-selective).\n"
            "3. **Earth Surface Interaction**:\n"
            "- When EMR hits earth features, it is divided into: **Reflection** ($R$), **Absorption** ($A$), and **Transmission** ($T$). So, $I = R + A + T$.\n"
            "- **Spectral Signatures**: Different materials reflect energy differently across wavelengths. E.g., healthy green vegetation reflects strongly in the Near-Infrared (NIR) band due to mesophyll structure, but absorbs Red light for photosynthesis. Water absorbs almost all NIR radiation, making it appear black."
        )

    # 2. Climatology / Meteorology
    elif "atmosphere" in q_lower or "lapse rate" in q_lower:
        return (
            "1. **Atmospheric Composition**:\n"
            "- Major gases: Nitrogen ($78.08\\%$), Oxygen ($20.95\\%$), Argon ($0.93\\%$), Carbon Dioxide ($0.04\\%$).\n"
            "- Variable components: Water vapor, aerosols, ozone.\n"
            "2. **Vertical Thermal Structure**:\n"
            "- **Troposphere**: Lowest layer (0-12 km). Temperature decreases with height at the Normal Lapse Rate of $6.5^\\circ\\text{C}$ per km. Contains $99\\%$ of water vapor and all weather phenomena.\n"
            "- **Stratosphere**: Extends to 50 km. Temperature increases with height due to UV absorption by the ozone layer (ozonosphere). Very stable, ideal for jet aircraft.\n"
            "- **Mesosphere**: Extends to 80 km. Temperature decreases to the lowest levels ($-90^\\circ\\text{C}$). Meteors burn up here.\n"
            "- **Thermosphere / Ionosphere**: Extends to 600 km. Temperature rises rapidly due to X-ray and UV absorption. Contains ionized particles that reflect radio waves.\n"
            "- **Exosphere**: Merges into outer space."
        )
        
    elif "insolation" in q_lower or "heat budget" in q_lower:
        return (
            "1. **Insolation (Incoming Solar Radiation)**:\n"
            "- Solar energy reaching the Earth's surface as short-wave radiation.\n"
            "- **Factors Influencing Distribution**: Angle of incidence (sun's rays are vertical at equator, oblique at poles), duration of daylight (day length), atmospheric transparency (clouds, dust), and land-sea distribution.\n"
            "2. **Heat Budget of the Earth**:\n"
            "- The balance between incoming solar radiation (short-wave) and outgoing terrestrial radiation (long-wave).\n"
            "- Assuming 100 units of solar energy reach the top of the atmosphere:\n"
            "  - **Albedo (Reflected directly)**: 35 units (27 from clouds, 6 from atmosphere, 2 from snow/land). This energy does not heat the Earth.\n"
            "  - **Absorbed by Atmosphere**: 14 units.\n"
            "  - **Absorbed by Earth's Surface**: 51 units.\n"
            "  - **Terrestrial Radiation (Outgoing)**: The earth radiates back 51 units (17 directly to space, 34 absorbed by atmosphere which is eventually radiated back into space). Balance is maintained at $0$ net gain, preserving stable global temperatures."
        )

    elif "cyclone" in q_lower or "anticyclone" in q_lower:
        return (
            "1. **Cyclones (Low-Pressure Systems)**:\n"
            "- Low-pressure centers with winds blowing inward in a spiral fashion (counter-clockwise in Northern Hemisphere, clockwise in Southern Hemisphere due to Coriolis force).\n"
            "- **Tropical Cyclones**: Form over warm oceans ($>27^\\circ\\text{C}$); driven by latent heat of condensation. Have a calm central 'eye', violent winds, and torrential rains. No fronts.\n"
            "- **Temperate (Frontal) Cyclones**: Form in mid-latitudes due to the convergence of warm tropical and cold polar air masses, creating distinct warm and cold fronts. Cover large areas and cause gradual rainfall.\n"
            "2. **Anticyclones (High-Pressure Systems)**:\n"
            "- High-pressure centers with winds blowing outward (clockwise in Northern Hemisphere, counter-clockwise in Southern Hemisphere). Characterized by sinking air, dry conditions, clear skies, and calm weather."
        )

    # 3. Geomorphology / Earth movements
    elif "weathering" in q_lower or "erosion" in q_lower:
        return (
            "1. **Weathering**: The in-situ disintegration and decomposition of rocks without transport.\n"
            "- **Mechanical Weathering**: Physical breakdown. Includes frost action (freeze-thaw cycle), thermal expansion/contraction (exfoliation), and pressure release (sheeting).\n"
            "- **Chemical Weathering**: Alteration of mineral composition. Includes carbonation (carbonic acid dissolving limestone), oxidation (rusting of iron-rich minerals), hydrolysis (water reacting with feldspar to form clay), and hydration.\n"
            "- **Biological Weathering**: Disintegration caused by plant roots, burrowing animals, and organic acids from lichens/mosses.\n"
            "2. **Erosion**: The active wearing away and transportation of rock materials by agents like running water, wind, glaciers, and waves.\n"
            "3. **Soil Formation**: Weathering is the first step in soil development, creating the parent material (regolith)."
        )

    elif "volcano" in q_lower or "plate tectonics" in q_lower or "drift" in q_lower:
        return (
            "1. **Wegener's Continental Drift Theory (1912)**:\n"
            "- Proposed that all landmasses were once joined in a supercontinent called **Pangaea**, surrounded by the ocean **Panthalassa**.\n"
            "- Pangaea broke up during the Mesozoic era; fragments drifted to form current continents.\n"
            "- **Evidence**: Jigsaw fit of South America and Africa, matching fossil distributions (Mesosaurus, Glossopteris), geological match of rock strata across oceans, and paleoclimatic data (tillites in India/Africa).\n"
            "2. **Plate Tectonics Theory**:\n"
            "- Describes the earth's lithosphere as broken into major and minor rigid plates floating on the semi-fluid asthenosphere.\n"
            "- **Plate Boundaries**:\n"
            "  - *Divergent (Constructive)*: Plates move apart, creating mid-ocean ridges and new crust (e.g., Mid-Atlantic Ridge).\n"
            "  - *Convergent (Destructive)*: Plates collide, causing subduction and trench formation, or folding to form fold mountains (e.g., Himalayas).\n"
            "  - *Transform (Conservative)*: Plates slide past each other, causing strike-slip faulting and earthquakes (e.g., San Andreas Fault).\n"
            "3. **Volcanism**: Magma rising through fractures in the crust. Associated primarily with convergent subduction zones (Pacific Ring of Fire) and divergent plate boundaries."
        )

    elif "tetrahedral" in q_lower:
        return (
            "1. **Lowthian Green's Tetrahedral Theory (1875)**:\n"
            "- A historical geomorphological theory attempting to explain the distribution of land and water bodies on the earth's surface.\n"
            "2. **Key Concepts**:\n"
            "- Assumes that as the Earth cooled and contracted, the outer crust collapsed inward over a shrinking core.\n"
            "- Since a sphere has the largest volume for a given surface area, and a tetrahedron has the smallest, a contracting sphere would naturally tend to deform toward a tetrahedral shape.\n"
            "- The four corners (vertices) of the tetrahedron remained as high landmasses (shields), while the flat faces formed the depressions where water collected to become oceans.\n"
            "- Explains why oceans are antipodal to landmasses (e.g., Arctic ocean antipodal to Antarctica).\n"
            "3. **Scientific Criticism**:\n"
            "- Discarded in modern geology because the Earth's gravity prevents it from maintaining a non-spherical tetrahedral shape, and the theory ignores isostasy and continental drift."
        )

    # 4. Human Geography
    elif "determinism" in q_lower or "possibilism" in q_lower:
        return (
            "1. **Environmental Determinism**:\n"
            "- The school of thought that physical environment (climate, topography, soil) strictly controls and shapes human behavior, culture, and capabilities.\n"
            "- Key proponents: Friedrich Ratzel, Ellen Churchill Semple, Ellsworth Huntington.\n"
            "- View: Humans are passive products of nature (e.g., hot climates produce lazy populations, temperate climates produce active minds).\n"
            "2. **Possibilism**:\n"
            "- Developed as a reaction to determinism, arguing that the environment sets limits but humans have choices and can adapt, modify, and conquer constraints using technology.\n"
            "- Key proponents: Lucien Febvre, Paul Vidal de la Blache.\n"
            "- View: 'There are no necessities, but everywhere possibilities; and man, as master of these possibilities, is the judge of their use.'\n"
            "3. **Neo-Determinism (Stop-and-Go Determinism)**:\n"
            "- Proposed by Griffith Taylor. A middle path stating that man is like a traffic controller: he can accelerate, slow down, or direct development, but cannot change the natural laws of the environment entirely. Promotes environmental sustainability."
        )

    elif "race" in q_lower or "bushman" in q_lower or "migration" in q_lower:
        return (
            "1. **Human Races Classification**:\n"
            "- A race is a biological group sharing inheritable physical characteristics.\n"
            "- **Indicators**: Skin color, stature, head shape (Cephalic Index), nasal index, hair form, eye shape.\n"
            "- **Major World Groups**: Caucasoid (Europe/West Asia), Mongoloid (East Asia/Americas), Negroid (Africa), Australoid.\n"
            "2. **The Bushmen (San Tribe)**:\n"
            "- Indigenous hunter-gatherers of the Kalahari Desert in Southern Africa.\n"
            "- **Adaptation**: Highly adapted to arid environments. Live in small nomadic bands. Diet consists of wild game, roots, and water-rich melons (tsama). Use poison-tipped arrows. Shelter in temporary windbreaks.\n"
            "3. **Human Migration**:\n"
            "- The movement of people from one place to another.\n"
            "- **Push Factors**: Drive people away (war, famine, lack of jobs, natural disasters).\n"
            "- **Pull Factors**: Attract people (higher wages, political stability, better education, pleasant climate)."
        )

    # 5. Economic & Industrial Geography
    elif "weber" in q_lower:
        return (
            "1. **Alfred Weber's Theory of Industrial Location (1909)**:\n"
            "- Attempts to explain the location of manufacturing industries based on minimizing costs (least-cost location).\n"
            "2. **Key Concepts**:\n"
            "- **Material Index ($MI$)**: Ratio of raw material weight to finished product weight. $MI = \\text{Weight of Raw Materials} / \\text{Weight of Finished Product}$.\n"
            "  - If $MI > 1$ (weight-losing material, e.g., iron ore, sugarcane), the factory locates near the raw material source.\n"
            "  - If $MI < 1$ (pure/ubiquitous material, e.g., water), the factory locates near the market.\n"
            "- **Transport Costs**: The primary determinant of location, calculated using the 'Locational Triangle'.\n"
            "- **Labor Cost Correction**: Factories may deviate from the point of least transport cost to an area of cheap labor if the labor savings exceed the additional transport costs (measured using **Isodapanes** - lines of equal total transport cost deviation).\n"
            "- **Agglomeration**: Industries may cluster together to share infrastructure and reduce costs, causing another locational shift."
        )
        
    elif "von thunen" in q_lower or "thunen" in q_lower:
        return (
            "1. **von Thünen's Agricultural Location Theory (1826)**:\n"
            "- Explains the spatial pattern of agricultural land use surrounding a central market city.\n"
            "2. **Key Assumptions**:\n"
            "- An 'Isolated State' with one central market city, surrounded by a flat, featureless plain (isotropic surface).\n"
            "- Transportation is by horse/wagon, and costs are proportional to distance and weight.\n"
            "- Farmers seek to maximize profit ($R = Y(P - C) - YFm$, where $R$ is locational rent, $m$ is distance, $F$ is transport rate).\n"
            "3. **Concentric Zones**:\n"
            "- **Zone 1 (Market Gardening & Milk)**: Highly perishable, heavy products with high transport costs, located closest to city.\n"
            "- **Zone 2 (Forestry/Firewood)**: Timber is heavy and expensive to transport, located near the city for fuel.\n"
            "- **Zone 3 (Grain Farming)**: Less perishable, lighter transport cost.\n"
            "- **Zone 4 (Three-field system)**: Extensive arable crops.\n"
            "- **Zone 5 (Three-field fallow)**: Extensive agriculture.\n"
            "- **Zone 6 (Livestock Ranching)**: Animal herds transport themselves to market, locating furthest away where land is cheap."
        )

    # 6. Geography of India
    elif "monsoon" in q_lower:
        return (
            "1. **Indian Monsoon Origin**:\n"
            "- A seasonal reversal of winds accompanied by corresponding changes in precipitation.\n"
            "2. **Mechanisms and Theories**:\n"
            "- **Thermal Concept (Halley)**: Differential heating of land and sea. In summer, the Asian landmass heats up, forming a low-pressure zone, while the Indian Ocean is high pressure, causing winds to blow from sea to land (South-West Monsoon).\n"
            "- **Dynamic Concept (Flohn)**: Shift of the Inter-Tropical Convergence Zone (ITCZ) northward to the plains in summer, pulling equatorial winds.\n"
            "- **Jet Stream Theory (Yin / Koteswaram)**: The northward shift of the Subtropical Westerly Jet Stream behind the Himalayas allows the Tropical Easterly Jet Stream to establish over India, initiating the monsoon surge.\n"
            "- **ENSO / El Niño**: Warm waters in eastern Pacific weaken the Indian monsoon, whereas **La Niña** enhances it."
        )

    # 7. Evolution of Geographical Thought
    elif "humboldt" in q_lower or "ritter" in q_lower:
        return (
            "1. **Alexander von Humboldt (1769-1859)**:\n"
            "- German naturalist and founder of modern geography. Traveled extensively in Central/South America.\n"
            "- Author of *Kosmos*, describing the universe as a unified whole. Developed the concept of **Isotherms** to compare temperatures globally, studied vegetation zones by altitude, and emphasized empirical fieldwork.\n"
            "2. **Carl Ritter (1779-1859)**:\n"
            "- Contemporary of Humboldt and first Professor of Geography at Berlin University. Author of *Erdkunde*.\n"
            "- Emphasized a regional approach and adopted a **Teleological** view (believing the earth was designed by God as a perfect home for humans). Focused on historical relationships between nature and human history."
        )

    # 8. Settlement Geography / Central Place
    elif "christaller" in q_lower:
        return (
            "1. **Walter Christaller's Central Place Theory (1933)**:\n"
            "- Explains the size, spacing, and functional hierarchy of towns and service settlements in a region.\n"
            "2. **Core Concepts**:\n"
            "- **Central Place**: A settlement providing goods and services to its surrounding tributary area.\n"
            "- **Range of a Good**: The maximum distance a consumer is willing to travel to purchase a service.\n"
            "- **Threshold**: The minimum population/market size required to make a business profitable.\n"
            "- **Hexagonal Market Areas**: Overlapping circles deform into hexagons to cover space efficiently without gaps or overlap.\n"
            "3. **Hierarchical Principles**:\n"
            "- **$K=3$ (Marketing Principle)**: Lower-order centers serve $1/3$ of the market area of surrounding centers. The network hierarchy is $1, 3, 9, 27...$\n"
            "- **$K=4$ (Transport Principle)**: Lower-order centers lie along the main transport routes connecting higher-order centers, serving $1/2$ of their market. Hierarchy: $1, 4, 16, 64...$\n"
            "- **$K=7$ (Administrative Principle)**: The administrative boundary of lower-order centers is completely enclosed within the higher-order region to prevent administrative disputes. Hierarchy: $1, 7, 49, 343...$"
        )

    elif "composition" in q_lower or "demographic transition" in q_lower:
        return (
            "1. **Demographic Transition Theory**:\n"
            "- Describes the transition from high birth and death rates to low birth and death rates as a country develops economically.\n"
            "2. **Stages of Transition**:\n"
            "- **Stage 1 (High Stationary)**: High birth and death rates due to poor health care and lack of family planning. Population grows slowly.\n"
            "- **Stage 2 (Early Expanding)**: Death rates fall rapidly due to medical improvements, but birth rates remain high. Population explodes.\n"
            "- **Stage 3 (Late Expanding)**: Birth rates begin to fall due to urbanization, literacy, and family planning. Population growth slows.\n"
            "- **Stage 4 (Low Stationary)**: Low birth and death rates. Stable, slow population growth.\n"
            "- **Stage 5 (Declining)**: Death rates exceed birth rates, leading to population decline (e.g., Japan, Germany)."
        )

    elif "disparity" in q_lower or "growth pole" in q_lower:
        return (
            "1. **Perroux's Growth Pole Theory (1955)**:\n"
            "- States that economic development does not appear everywhere at once, but rather at specific 'growth poles' (centers) with key industries, and eventually diffuses outward.\n"
            "- **Trickle-Down Effect**: Spread of growth to surrounding regions through demand for raw materials and labor.\n"
            "- **Polarization Effect**: Concentration of capital, skilled labor, and resources from backward regions into the growth center, increasing regional disparity.\n"
            "2. **Myrdal's Cumulative Causation**: States that market forces tend to increase regional inequalities rather than decrease them, through backwash and spread effects."
        )

    # Fallback default answer
    else:
        return (
            "1. **Core Geographical Analysis**:\n"
            "- Examine the spatial patterns, physical processes, and human interactions shaping the geographical feature or region under study.\n"
            "2. **Physical and Human Dynamics**:\n"
            "- Analyze variables such as climate, geologic forces, and resources, and relate them to human activities, settlement patterns, and economic organizations.\n"
            "3. **Verification**:\n"
            "- Ensure spatial relationships, map references, and structural hierarchies are consistent, and cross-reference with established geographical models and theories."
        )

# 3. Smart LaTeX Parser
def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comment lines
    content = re.sub(r'(?m)^%.*$', '', content)
    
    parts_questions = []
    
    # Extract Question 1 sub-questions from parts block
    parts_match = re.search(r'\\begin\{parts\}(.*?)\\end\{parts\}', content, re.DOTALL)
    if parts_match:
        parts_content = parts_match.group(1)
        items = re.split(r'\\item', parts_content)
        for item in items[1:]:
            cleaned = clean_text(item)
            if len(cleaned) > 10:
                parts_questions.append(cleaned)
                
    # Extract Questions 2 to 9
    main_questions = []
    matches = re.findall(r'\\textbf\{\s*Question\s*([2-9])\.\}\s*(.*?)(?=\\pts|\\hfill|\\medskip|\\noindent|\\vfill|\\begin\{center\}|\Z)', content, re.DOTALL)
    for q_num, q_text in matches:
        cleaned = clean_text(q_text)
        if len(cleaned) > 10:
            main_questions.append(cleaned)
            
    return parts_questions + main_questions

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
    # Replace LaTeX bracket math with $ delimiters
    text = text.replace(r'\[', '$')
    text = text.replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 4. Map File Names to GGR unique keys
def get_ggr_mapping(filename):
    filename_upper = filename.upper()
    if "PHYSICALBASIS" in filename_upper:
        return "ggrmj11"
    elif "HUMANGEOGRAPHY" in filename_upper:
        return "ggrmj21"
    elif "MANANDENVIRONMENT" in filename_upper:
        return "ggrse11"
    elif "ECONOMICGEOGRAPHY" in filename_upper:
        return "ggrmj31"
    elif "REGIONALGEOGRAPHY" in filename_upper:
        return "ggrmj52"
    elif "GEOMORPHOLOGY" in filename_upper:
        return "ggrmj43"
    elif "GEOGRAPHYOFINDIA" in filename_upper:
        return "ggrmj33"
    elif "OCEANOGRAPHY" in filename_upper:
        return "ggrmj62"
    elif "POPULATIONGEOGRAPHY" in filename_upper:
        return "ggrmj53"
    elif "AGRICULTURALGEOGRAPHY" in filename_upper:
        return "ggrmj83f"
    elif "CLIMATOLOGY" in filename_upper:
        return "ggrmj51"
    elif "EVOLUTIONOFGEOGRAPHICALTHOUGHT" in filename_upper:
        return "ggrmj41"
    elif "REGIONALDEVELOPMENT" in filename_upper or "REGIONALPLANNING" in filename_upper:
        return "ggrmj74d"
    elif "SETTLEMENTGEOGRAPHY" in filename_upper:
        return "ggrmj65b"
    elif "BASICSOFREMOTESENSING" in filename_upper:
        return "ggrse21"
    return None

# 5. Populate and write unified exams data back to js/exams-data.js
def main():
    tex_dir = "aaa/geography"
    if not os.path.exists(tex_dir):
        print(f"Geography folder not found at {tex_dir}")
        return

    # Initialize raw question lists
    raw_questions = {k: [] for k in GEOGRAPHY_SYLLABI.keys()}

    # Parse questions from all LaTeX geography files
    files = [f for f in os.listdir(tex_dir) if f.endswith(".tex")]
    files.sort()

    print(f"Reading and parsing {len(files)} LaTeX files...")
    for file_name in files:
        filepath = os.path.join(tex_dir, file_name)
        gkey = get_ggr_mapping(file_name)
        if gkey:
            qs = parse_tex_file(filepath)
            raw_questions[gkey].extend(qs)
            print(f" - Parsed {len(qs)} questions from {file_name} -> Mapped to {gkey}")

    # Load existing exams database
    exams_js_path = "js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    json_start = js_content.find("{")
    json_end = js_content.rfind("}")
    EXAMS = json.loads(js_content[json_start:json_end+1])

    # Populate active geography keys
    print("Populating and padding questions to 50...")
    for unique_key, active_list in UNIQUE_TO_ACTIVE.items():
        raw_qs = raw_questions.get(unique_key, [])
        standard_qs = GEOGRAPHY_SYLLABI.get(unique_key, {}).get("standard_questions", [])
        
        # Deduplicate raw questions
        seen = set()
        final_questions = []
        for q_text in raw_qs:
            q_norm = q_text.lower().strip()
            if q_norm not in seen and len(q_text) > 15:
                seen.add(q_norm)
                final_questions.append(q_text)

        # Pad with standard syllabus questions
        std_idx = 0
        while len(final_questions) < 50 and std_idx < len(standard_qs):
            q_text, unit = standard_qs[std_idx]
            q_norm = q_text.lower().strip()
            if q_norm not in seen:
                seen.add(q_norm)
                final_questions.append((q_text, unit))
            std_idx += 1

        # Fallback pad if still fewer than 50
        fallback_idx = 1
        title_text = GEOGRAPHY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())
        while len(final_questions) < 50:
            q_text = f"Discuss the spatial distributions, theoretical frameworks, and research methodologies of {title_text} (Part {fallback_idx})."
            final_questions.append((q_text, "V"))
            fallback_idx += 1

        # Slice to exactly 50
        final_questions = final_questions[:50]

        # Structure questions array
        formatted_questions = []
        for idx, item in enumerate(final_questions):
            q_id = idx + 1
            if isinstance(item, tuple):
                q_text = item[0]
                unit = item[1]
            else:
                q_text = item
                # Distribute units evenly
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

        # Inject into active exams-data.js keys and mark comingSoon as False
        for active_key in active_list:
            orig = EXAMS.get(active_key, {})
            EXAMS[active_key] = {
                "id": active_key,
                "title": orig.get("title", GEOGRAPHY_SYLLABI.get(unique_key, {}).get("title", unique_key.upper())),
                "module": orig.get("module", active_key.upper()),
                "duration": 60,
                "type": "theory",
                "comingSoon": False,
                "questions": formatted_questions
            }
            print(f" - Key: {active_key} populated successfully. (Live: True)")

    # Save back to js/exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)

    print("js/exams-data.js successfully populated and updated with Geography papers!")

if __name__ == "__main__":
    main()
