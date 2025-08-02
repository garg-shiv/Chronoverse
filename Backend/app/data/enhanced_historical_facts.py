from typing import Dict, List

ENHANCED_HISTORICAL_FACTS = {
    "roman_gladiator": {
        "character_info": {
            "name": "Marcus Quintus",
            "period": "1st-2nd Century CE",
            "background": "Veteran gladiator, fought for 8 years, survived 47 matches"
        },
        "facts": [
            {
                "text": "Gladiator training began before dawn with wooden practice swords called rudis, which were deliberately heavier than real weapons to build strength and endurance.",
                "category": "training",
                "subcategory": "weapons",
                "historical_accuracy": "high",
                "source": "Pliny the Elder, Natural History"
            },
            {
                "text": "The four fundamental gladiator fighting stances were prima, secunda, tertia, and quarta, each designed for different combat situations and weapon combinations.",
                "category": "combat_techniques",
                "subcategory": "stances",
                "historical_accuracy": "high",
                "source": "Archaeological evidence from Pompeii"
            },
            {
                "text": "Murmillo gladiators like myself wore a distinctive fish-crested helmet and fought with gladius and scutum shield, often matched against retiarii with nets and tridents.",
                "category": "equipment",
                "subcategory": "armor",
                "historical_accuracy": "high",
                "source": "Gladiator mosaics from Villa Borghese"
            },
            {
                "text": "Gladiator schools called ludi were run by lanistae who owned and trained fighters, with the most famous being the Ludus Magnus connected to the Colosseum by underground tunnel.",
                "category": "training",
                "subcategory": "facilities",
                "historical_accuracy": "high",
                "source": "Suetonius, Lives of the Caesars"
            },
            {
                "text": "A gladiator's diet consisted mainly of barley, beans, and vegetables - we were called hordearii meaning barley eaters, as meat was reserved for special occasions before important fights.",
                "category": "daily_life",
                "subcategory": "nutrition",
                "historical_accuracy": "high",
                "source": "Galen, medical writings"
            },
            {
                "text": "The wooden sword rudis was not just for training but also the symbol of freedom - gladiators who earned their freedom received a wooden rudis as proof of manumission.",
                "category": "culture",
                "subcategory": "freedom",
                "historical_accuracy": "high",
                "source": "Martial, Epigrams"
            },
            {
                "text": "Gladiator matches followed strict rules overseen by the editor who organized games, with specific gestures like thumbs up or down determining a defeated fighter's fate.",
                "category": "arena_politics",
                "subcategory": "rules",
                "historical_accuracy": "medium",
                "source": "Tertullian, De Spectaculis"
            },
            {
                "text": "Medical care for gladiators was sophisticated, with specialized doctors called medici who understood combat injuries and used advanced surgical techniques for the time.",
                "category": "medical_care",
                "subcategory": "treatment",
                "historical_accuracy": "high",
                "source": "Galen's gladiator medical records"
            },
            {
                "text": "Gladiator barracks were prison-like with cells, but successful fighters could earn privileges like better food, private rooms, and conjugal visits.",
                "category": "daily_life",
                "subcategory": "living_conditions",
                "historical_accuracy": "high",
                "source": "Pompeii gladiator barracks excavations"
            },
            {
                "text": "Female gladiators called gladiatrices existed and fought in the arena, though they were rarer and often considered novelty acts by Roman society.",
                "category": "culture",
                "subcategory": "gender",
                "historical_accuracy": "medium",
                "source": "Relief from Halicarnassus"
            },
            {
                "text": "Gladiator fights were timed by water clocks, and matches could last from minutes to over an hour depending on the skill and stamina of the fighters.",
                "category": "combat_techniques",
                "subcategory": "duration",
                "historical_accuracy": "high",
                "source": "Seneca, Letters"
            },
            {
                "text": "The crowd's favor could save a defeated gladiator's life - popular fighters who showed courage earned the audience's protection through loud cheering.",
                "category": "arena_politics",
                "subcategory": "crowd_influence",
                "historical_accuracy": "high",
                "source": "Cassius Dio, Roman History"
            },
            {
                "text": "Successful gladiators became celebrities with fan clubs, endorsement deals for olive oil and wine, and their images on pottery and mosaics throughout the empire.",
                "category": "culture",
                "subcategory": "fame",
                "historical_accuracy": "high",
                "source": "Pompeii graffiti and mosaics"
            },
            {
                "text": "Gladiator schools taught not just combat but also showmanship - how to engage the crowd, dramatic gestures, and theatrical fighting techniques.",
                "category": "training",
                "subcategory": "performance",
                "historical_accuracy": "medium",
                "source": "Tacitus, Annals"
            },
            {
                "text": "The mortality rate in gladiator games was around 10-20%, much lower than Hollywood depicts, as dead gladiators were expensive to replace.",
                "category": "arena_politics",
                "subcategory": "survival_rates",
                "historical_accuracy": "high",
                "source": "Modern archaeological analysis"
            }
        ]
    },
    
    "mughal_architect": {
        "character_info": {
            "name": "Ustad Ahmad Lahauri",
            "period": "17th Century CE (1580-1649)",
            "background": "Master architect, designed Taj Mahal under Shah Jahan"
        },
        "facts": [
            {
                "text": "The Taj Mahal's dome uses a double-shell construction technique - an inner dome for interior proportion and an outer dome for external magnificence, connected by a complex framework.",
                "category": "architecture",
                "subcategory": "dome_construction",
                "historical_accuracy": "high",
                "source": "Architectural analysis and Mughal construction records"
            },
            {
                "text": "The perfect symmetry of the Taj Mahal was achieved using mathematical principles based on the golden ratio and Islamic geometric patterns called hasht-bihisht.",
                "category": "mathematics",
                "subcategory": "proportions",
                "historical_accuracy": "high",
                "source": "Persian architectural treatises"
            },
            {
                "text": "White Makrana marble was transported over 300 kilometers using a specially built ramp system and teams of elephants, buffalo, and oxen working in coordinated shifts.",
                "category": "construction",
                "subcategory": "materials",
                "historical_accuracy": "high",
                "source": "Mughal court chronicles"
            },
            {
                "text": "The Taj Mahal's minarets are built with a slight outward lean so that in case of earthquake, they would fall away from the main tomb structure.",
                "category": "engineering",
                "subcategory": "safety",
                "historical_accuracy": "high",
                "source": "Archaeological surveys and engineering analysis"
            },
            {
                "text": "Over 20,000 artisans from across the Mughal Empire and beyond worked on the Taj Mahal, including master craftsmen from Persia, Central Asia, and Europe.",
                "category": "workforce",
                "subcategory": "artisans",
                "historical_accuracy": "high",
                "source": "Mughal administrative records"
            },
            {
                "text": "The intricate inlay work called pietra dura uses over 40 different types of precious and semi-precious stones cut into thin slices and fitted into marble.",
                "category": "decoration",
                "subcategory": "inlay_work",
                "historical_accuracy": "high",
                "source": "Craftsman guild records and material analysis"
            },
            {
                "text": "The Taj Mahal's acoustic properties were deliberately designed so that recitation of Quranic verses would resonate for exactly 28 seconds in the main chamber.",
                "category": "architecture",
                "subcategory": "acoustics",
                "historical_accuracy": "medium",
                "source": "Modern acoustic analysis and historical accounts"
            },
            {
                "text": "Water for the Taj Mahal complex was supplied through an ingenious hydraulic system using Persian wheels and underground channels called karez.",
                "category": "engineering",
                "subcategory": "water_systems",
                "historical_accuracy": "high",
                "source": "Archaeological excavations and Mughal engineering texts"
            },
            {
                "text": "The changing colors of the Taj Mahal throughout the day were intentional, achieved by the translucent quality of Makrana marble and strategic window placement.",
                "category": "architecture",
                "subcategory": "lighting",
                "historical_accuracy": "high",
                "source": "Architectural studies and contemporary Persian accounts"
            },
            {
                "text": "The four gardens of the Taj Mahal represent the Islamic concept of paradise with four rivers, using sophisticated irrigation and drainage systems.",
                "category": "landscape",
                "subcategory": "gardens",
                "historical_accuracy": "high",
                "source": "Islamic garden design treatises"
            },
            {
                "text": "Construction of the Taj Mahal required developing new mortar techniques using lime, egg whites, and fruit juice to ensure the structure's longevity.",
                "category": "construction",
                "subcategory": "techniques",
                "historical_accuracy": "medium",
                "source": "Material analysis of Mughal monuments"
            },
            {
                "text": "The calligraphy on the Taj Mahal appears uniform in size from ground level due to a mathematical technique called optical correction, with letters increasing in size with height.",
                "category": "decoration",
                "subcategory": "calligraphy",
                "historical_accuracy": "high",
                "source": "Calligraphic analysis and Islamic art studies"
            },
            {
                "text": "The entire Taj Mahal complex sits on a massive foundation of wells filled with stone and mortar to create a stable platform above the floodplain of the Yamuna River.",
                "category": "engineering",
                "subcategory": "foundation",
                "historical_accuracy": "high",
                "source": "Geological surveys and construction analysis"
            },
            {
                "text": "The Taj Mahal's construction employed advanced scaffolding systems using interlocking wooden beams, allowing workers to build the dome from the inside out.",
                "category": "construction",
                "subcategory": "scaffolding",
                "historical_accuracy": "medium",
                "source": "Reconstruction studies and Mughal architectural practices"
            },
            {
                "text": "The red sandstone mosque and guest house flanking the Taj Mahal were built first to establish the complex's proportions and serve as construction workshops.",
                "category": "planning",
                "subcategory": "construction_sequence",
                "historical_accuracy": "high",
                "source": "Archaeological evidence and construction timeline analysis"
            }
        ]
    },
    
    "egyptian_scribe": {
        "character_info": {
            "name": "Khaemwaset",
            "period": "New Kingdom, 19th Dynasty (c. 1295-1186 BCE)",
            "background": "Royal scribe in the House of Life, served under Ramesses II"
        },
        "facts": [
            {
                "text": "Hieroglyphic writing contained over 700 individual signs that could function as logograms representing whole words, phonograms representing sounds, or determinatives clarifying meaning.",
                "category": "writing_systems",
                "subcategory": "hieroglyphs",
                "historical_accuracy": "high",
                "source": "Gardiner's Egyptian Grammar and papyrus studies"
            },
            {
                "text": "The House of Life was both library and scriptorium where scribes copied religious texts, medical treatises, and administrative documents on papyrus made from Nile reeds.",
                "category": "institutions",
                "subcategory": "house_of_life",
                "historical_accuracy": "high",
                "source": "Papyrus Chester Beatty and temple inscriptions"
            },
            {
                "text": "Egyptian scribes underwent years of training starting at age five, learning to read and write hieroglyphs, hieratic script, and later demotic script for different purposes.",
                "category": "education",
                "subcategory": "training",
                "historical_accuracy": "high",
                "source": "Educational papyri and scribal school ostraca"
            },
            {
                "text": "The god Thoth, depicted with an ibis head, was patron of scribes and writing, and we invoked his blessing before beginning important documents.",
                "category": "religion",
                "subcategory": "patron_deities",
                "historical_accuracy": "high",
                "source": "Temple reliefs and scribal prayers"
            },
            {
                "text": "Papyrus production involved cutting reed stems into strips, laying them perpendicular, pressing and drying them to create sheets up to 40 centimeters long.",
                "category": "materials",
                "subcategory": "papyrus_making",
                "historical_accuracy": "high",
                "source": "Papyrus production studies and ancient descriptions"
            },
            {
                "text": "Egyptian mathematics used a decimal system without zero, representing fractions as sums of unit fractions, essential for calculating temple offerings and land surveys.",
                "category": "mathematics",
                "subcategory": "number_systems",
                "historical_accuracy": "high",
                "source": "Rhind Papyrus and Moscow Mathematical Papyrus"
            },
            {
                "text": "Royal scribes like myself held high social status, exempt from manual labor and taxation, often advancing to positions as viziers or high priests.",
                "category": "social_status",
                "subcategory": "privileges",
                "historical_accuracy": "high",
                "source": "Biographical inscriptions and administrative papyri"
            },
            {
                "text": "The Egyptian calendar had 365 days divided into 12 months of 30 days plus 5 extra days, with scribes calculating religious festivals and agricultural seasons.",
                "category": "timekeeping",
                "subcategory": "calendar",
                "historical_accuracy": "high",
                "source": "Calendar papyri and astronomical texts"
            },
            {
                "text": "Mummification records were meticulously kept by scribes, documenting the 70-day process including removal of organs, desiccation with natron salt, and wrapping procedures.",
                "category": "funerary_practices",
                "subcategory": "mummification",
                "historical_accuracy": "high",
                "source": "Mummification papyri and burial records"
            },
            {
                "text": "Egyptian medical papyri recorded surgical procedures, medicinal recipes, and anatomical knowledge, with scribes copying texts like the Edwin Smith Surgical Papyrus.",
                "category": "medicine",
                "subcategory": "medical_texts",
                "historical_accuracy": "high",
                "source": "Medical papyri including Edwin Smith and Ebers Papyrus"
            },
            {
                "text": "The weighing of the heart ceremony required precise scribal records, as the deceased's heart was weighed against the feather of Ma'at to determine worthiness for the afterlife.",
                "category": "afterlife_beliefs",
                "subcategory": "judgment",
                "historical_accuracy": "high",
                "source": "Book of the Dead and tomb paintings"
            },
            {
                "text": "Temple archives maintained by scribes contained birth records, marriage contracts, property deeds, and legal proceedings, serving as ancient Egypt's bureaucratic backbone.",
                "category": "administration",
                "subcategory": "record_keeping",
                "historical_accuracy": "high",
                "source": "Temple archives from Kanais and Wilbour Papyrus"
            },
            {
                "text": "Scribal palettes made of wood or ivory held reed pens and cakes of black and red ink, with compartments for different colored pigments used in illuminated texts.",
                "category": "tools",
                "subcategory": "writing_equipment",
                "historical_accuracy": "high",
                "source": "Archaeological finds and tomb paintings depicting scribes"
            },
            {
                "text": "The Rosetta Stone, carved during the Ptolemaic period, contains the same text in hieroglyphic, demotic, and Greek scripts, showcasing the evolution of Egyptian writing.",
                "category": "writing_systems",
                "subcategory": "multilingual_texts",
                "historical_accuracy": "high",
                "source": "Rosetta Stone analysis and bilingual inscriptions"
            },
            {
                "text": "Egyptian love poetry and literature were preserved by scribes, including works like the Story of Sinuhe and love songs comparing beloveds to goddesses and natural beauty.",
                "category": "literature",
                "subcategory": "poetry",
                "historical_accuracy": "high",
                "source": "Literary papyri including Papyrus Harris 500"
            }
        ]
    }
}

def get_character_facts(character_id: str) -> Dict:
    """Get enhanced facts for a specific character"""
    return ENHANCED_HISTORICAL_FACTS.get(character_id, {})

def get_all_facts_by_category(character_id: str, category: str) -> List[Dict]:
    """Get facts filtered by category"""
    character_data = ENHANCED_HISTORICAL_FACTS.get(character_id, {})
    if not character_data or "facts" not in character_data:
        return []
    
    return [fact for fact in character_data["facts"] if fact.get("category") == category]

def get_fact_categories(character_id: str) -> List[str]:
    """Get all available categories for a character"""
    character_data = ENHANCED_HISTORICAL_FACTS.get(character_id, {})
    if not character_data or "facts" not in character_data:
        return []
    
    categories = set(fact.get("category", "general") for fact in character_data["facts"])
    return sorted(list(categories))
