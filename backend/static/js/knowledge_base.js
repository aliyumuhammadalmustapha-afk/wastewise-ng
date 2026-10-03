/**
 * knowledge_base.js — WasteWise NG Knowledge Base
 * Complete material guidance for all 9 waste categories
 */
window.WASTE_KNOWLEDGE = {
    'E-Waste': {
        name: 'E-Waste',
        category: 'E-Waste',
        nigerian_examples: ['Old phones', 'Chargers', 'Small appliances', 'Circuit boards', 'Inverter batteries'],
        material: 'Electrical and electronic equipment containing recoverable metals (copper, gold, aluminium), plastics, and batteries.',
        danger_level: 'Hazardous',
        danger_color: 'red',
        decomposition_time: 'Components persist for decades or centuries; heavy metals never biodegrade.',
        environmental_impact: 'Informal dumping or burning releases lead, cadmium, and mercury into Nigerian communities and waterways like Lagos Lagoon.',
        disposal_steps: [
            'Keep the item intact, dry, and away from children and heat sources.',
            'Store leaking or damaged batteries separately in a non-metal box.',
            'Deliver to a formal e-waste take-back centre or certified electronics recycler (e.g. EPRON in Nigeria).'
        ],
        recycling_tips: 'Specialist recyclers extract precious metals and safely handle toxins. Never burn cables or smash cathode-ray tubes.',
        reuse_ideas: 'Repair, resell, or donate working devices. Strip working parts for DIY repairs before discarding.',
        fertilizer_use: null,
        fun_fact: 'Nigeria generates over 500,000 tonnes of e-waste annually. Computer Village in Ikeja, Lagos, is one of the world\'s largest informal electronics repair and refurbishing hubs.'
    },
    'General': {
        name: 'General',
        category: 'General Waste',
        nigerian_examples: ['Disposable diapers', 'Styrofoam packs', 'Mixed residue', 'Contaminated wrappers'],
        material: 'Residual composite materials and contaminated items that cannot currently be separated or recycled.',
        danger_level: 'Moderate',
        danger_color: 'amber',
        decomposition_time: 'Varies widely; synthetic components take up to 500 years to fragment.',
        environmental_impact: 'Unsorted general waste clogs open drainage channels, contributes to urban flooding, and fills overburdened dumpsites like Olusosun in Lagos.',
        disposal_steps: [
            'Separate any clean recyclables, food scraps, and hazardous chemicals first.',
            'Bag residual waste securely in a durable trash bag.',
            'Place in designated waste bins for municipal collection (e.g. LAWMA in Lagos).'
        ],
        recycling_tips: 'Mixed residual waste cannot be recycled directly. Source separation at home is key to diverting useful material.',
        reuse_ideas: 'Repurpose sturdy containers for storage or cleaning before discarding.',
        fertilizer_use: null,
        fun_fact: 'In major Nigerian cities, more than 60% of municipal dumpsite volume consists of materials that could have been composted or recycled if separated at source.'
    },
    'Glass': {
        name: 'Glass',
        category: 'Glass',
        nigerian_examples: ['Star/Guinness beer bottles', 'Soft drink bottles', 'Ogogoro spirit bottles', 'Food jars'],
        material: '100% recyclable soda-lime silicate glass. 100% non-porous and infinitely recyclable without loss of quality.',
        danger_level: 'Moderate',
        danger_color: 'amber',
        decomposition_time: 'Over 1,000,000 years. Glass never truly decomposes in the environment.',
        environmental_impact: 'Discarded glass poses sharp physical injury hazards to waste handlers, pedestrians, and animals, but produces zero toxic chemical leachate.',
        disposal_steps: [
            'Return intact beer and soft drink bottles to neighborhood retailers for your deposit refund.',
            'Rinse out food and sauce jars with water.',
            'Wrap broken glass in heavy paper or a box and label clearly as "Broken Glass" before disposal.'
        ],
        recycling_tips: 'Returnable glass bottles are washed and refilled up to 30 times by Nigerian breweries before being crushed for cullet.',
        reuse_ideas: 'Store home-made zobo, palm oil, groundnuts, spices, or use as flower vases and water carafes.',
        fertilizer_use: null,
        fun_fact: 'Nigerian breweries operate one of the most efficient returnable glass bottle systems in Africa, circulating millions of bottles every week.'
    },
    'Hazardous': {
        name: 'Hazardous',
        category: 'Hazardous Waste',
        nigerian_examples: ['Pesticide containers', 'Used engine oil cans', 'Kerosene cans', 'Expired medicines', 'Paint drums'],
        material: 'Toxic, flammable, corrosive, or chemically reactive compounds and their contaminated packaging.',
        danger_level: 'Hazardous',
        danger_color: 'red',
        decomposition_time: 'Persistent chemical residues can contaminate soil and aquifers indefinitely.',
        environmental_impact: 'Pouring chemicals or engine oil into gutters contaminates groundwater used for boreholes and poisons municipal water supplies.',
        disposal_steps: [
            'Keep substances sealed in original containers with warning labels intact.',
            'Never pour used engine oil, solvents, or agrochemicals down drains or on bare soil.',
            'Deliver used motor oil to certified mechanic workshops with collection drums.'
        ],
        recycling_tips: 'Used motor oil can be re-refined into base lubricating oils by licensed industrial recyclers.',
        reuse_ideas: 'Never reuse chemical, pesticide, or fuel containers for storing food, cooking oil, or drinking water.',
        fertilizer_use: null,
        fun_fact: 'A single litre of used motor oil poured into a storm drain can contaminate up to one million litres of fresh water.'
    },
    'Metal': {
        name: 'Metal',
        category: 'Metal',
        nigerian_examples: ['Tomato paste tins', 'Peak milk cans', 'Milo tins', 'Aluminium beverage cans', 'Scrap metal'],
        material: 'Ferrous steel tinplate and non-ferrous aluminium alloys. Highly recyclable with strong commercial scrap value.',
        danger_level: 'Moderate',
        danger_color: 'amber',
        decomposition_time: 'Aluminium cans: 80–200 years; Steel cans: 50–100 years before corroding away.',
        environmental_impact: 'Recycling aluminium uses 95% less energy than mining and smelting virgin bauxite ore.',
        disposal_steps: [
            'Rinse out tomato paste, condensed milk, and food residue.',
            'Carefully push lid into the can or crush cans flat to save space.',
            'Collect clean cans and scrap metal for local scrap collectors or scrap buyers ("buka").'
        ],
        recycling_tips: 'Clean, sorted aluminium cans command premium cash prices from local scrap dealers across Nigeria.',
        reuse_ideas: 'Use Milo and Peak milk tins as kitchen measuring units ("one tin of rice"), pen holders, or seedling planters.',
        fertilizer_use: null,
        fun_fact: 'In Nigerian markets, the 70g tomato paste tin is widely used as a standard volumetric measurement unit for buying rice, beans, and garri.'
    },
    'Organic': {
        name: 'Organic',
        category: 'Organic Waste',
        nigerian_examples: ['Cassava peels', 'Yam peels', 'Palm kernel shells', 'Plantain skins', 'Kitchen scraps'],
        material: 'Biodegradable plant matter, food scraps, and agricultural biomass rich in carbon, nitrogen, and minerals.',
        danger_level: 'Safe',
        danger_color: 'green',
        decomposition_time: '2 to 6 weeks in a warm, moist tropical compost pile.',
        environmental_impact: 'When trapped in anaerobic dumpsites, organic waste produces potent methane gas and toxic leachate. When composted, it enriches depleted soil.',
        disposal_steps: [
            'Separate kitchen and food waste from plastics and wrappers at source.',
            'Add plant peels and raw scraps to your home compost pile or garden bed.',
            'Feed suitable raw peels (cassava, yam, plantain) to local livestock or poultry if safe.'
        ],
        recycling_tips: 'Organic waste converts into rich organic fertilizer (compost) or biogas fuel via simple biodigesters.',
        reuse_ideas: 'Use dried cassava and yam peels as livestock feed. Use palm kernel shells for landscape mulching or clean boiler fuel.',
        fertilizer_use: 'Excellent for compost. Mix green food scraps with brown dried leaves to produce nutrient-rich organic soil amendment for crops and vegetable gardens.',
        fun_fact: 'Nigeria produces over 30 million metric tonnes of cassava annually; converting its peel waste into animal feed is now a major green agribusiness sector.'
    },
    'Paper': {
        name: 'Paper',
        category: 'Paper & Cardboard',
        nigerian_examples: ['Delivery cartons', 'Newspapers', 'Office paper', 'Suya wrap paper', 'Paper bags'],
        material: 'Cellulose plant fibres from softwood and recycled pulp. Biodegradable and recyclable 5–7 times.',
        danger_level: 'Safe',
        danger_color: 'green',
        decomposition_time: '2 to 6 weeks for uncoated paper; 2 to 4 months for corrugated cardboard boxes.',
        environmental_impact: 'Recycling 1 tonne of cardboard saves 17 trees, 26,000 litres of water, and 4,000 kWh of electrical energy.',
        disposal_steps: [
            'Flatten all corrugated shipping boxes to reduce bulk.',
            'Keep paper dry and free from cooking oil, gravy, or grease stains.',
            'Bundle clean paper and boxes together for recyclers (e.g. RecyclePoints).'
        ],
        recycling_tips: 'Keep paper dry. Heavily grease-soaked paper (like suya wraps) cannot be recycled and should be composted instead.',
        reuse_ideas: 'Use delivery boxes for household storage. Reuse single-sided office sheets as scrap note paper. Use shredded paper as packaging cushion.',
        fertilizer_use: 'Clean, unprinted shredded cardboard and newspaper can be added as carbon "browns" in organic composting piles.',
        fun_fact: 'Friday editions of Nigerian national newspapers are commonly passed around among 5 to 10 readers before ending up as packaging material in food markets.'
    },
    'Plastic': {
        name: 'Plastic',
        category: 'Plastic',
        nigerian_examples: ['Pure water sachets', 'PET drink bottles', 'Nylon carrier bags', 'Ghana-must-go bags'],
        material: 'Low-density polyethylene (LDPE sachet film), Polyethylene terephthalate (PET bottles), and Polypropylene (woven bags).',
        danger_level: 'Moderate',
        danger_color: 'amber',
        decomposition_time: '400 to 1,000 years. Plastic fragments into hazardous microplastics that enter the food chain.',
        environmental_impact: 'Discarded sachets and bottles choke city gutters, causing severe flooding in Lagos, Port Harcourt, and Aba during the rains. Never burn plastics.',
        disposal_steps: [
            'Rinse empty PET bottles and flatten them to reduce volume.',
            'Keep pure water sachets collected in a dedicated dry collection bag.',
            'Take bags of clean plastics to aggregators (Wecyclers, RecyclePoints, or local scrap drop-offs).'
        ],
        recycling_tips: 'PET bottles and LDPE sachets are shredded into flakes and pelletised to make polyester textile fibers, paving tiles, and drainage pipes.',
        reuse_ideas: 'Cut PET bottles to make seedling nursery planters, drip-irrigation dispensers, or funnels. Reuse Ghana-must-go bags for durable storage.',
        fertilizer_use: null,
        fun_fact: 'Over 60 million pure water sachets are consumed daily in Nigeria. Innovative recyclers are now transforming them into eco-friendly building paving bricks.'
    },
    'Textile': {
        name: 'Textile',
        category: 'Textile',
        nigerian_examples: ['Ankara wax-print scraps', 'Okrika secondhand clothes', 'Head-ties (gele)', 'Tailoring offcuts'],
        material: 'Natural cotton fibres, synthetic polyester/nylon blends, rayon, and wax-resist dyes.',
        danger_level: 'Safe',
        danger_color: 'green',
        decomposition_time: '100% cotton: 5–6 months; Synthetic polyester textiles: 20 to 200 years.',
        environmental_impact: 'Discarded synthetic fabrics shed microplastic fibres when washed and occupy huge volume in landfills if thrown into general waste.',
        disposal_steps: [
            'Keep clean, usable garments separate from wet household waste.',
            'Donate wearable clothes to charities, orphanages, or community clothing drives.',
            'Collect tailoring offcuts for artisans, weavers, or mattress stuffing makers.'
        ],
        recycling_tips: 'Cotton textile scraps can be shredded and repurposed for upholstery cushioning, industrial cleaning rags, or rag rugs.',
        reuse_ideas: 'Use Ankara fabric scraps for patchwork quilts, tote bags, hair scrunchies, or household cleaning dusters.',
        fertilizer_use: null,
        fun_fact: 'Nigeria\'s bustling tailoring industry generates tonnes of colourful Ankara fabric offcuts weekly, sparking a growing trend of eco-fashion upcycling.'
    }
};
