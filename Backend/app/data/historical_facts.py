"""
Historical facts database for our characters
This will be loaded into the vector database
"""

ROMAN_GLADIATOR_FACTS = [
    {
        "text": "Gladiators trained at specialized schools called ludus. The largest was the Ludus Magnus in Rome, connected to the Colosseum by underground tunnels.",
        "category": "training",
        "source": "Archaeological evidence from Colosseum excavations"
    },
    {
        "text": "Most gladiators were slaves, prisoners of war, or condemned criminals, though some free men voluntarily became gladiators for fame and money.",
        "category": "social_status", 
        "source": "Roman historical records by Tacitus"
    },
    {
        "text": "Gladiators fought with different weapon combinations: retiarius used net and trident, secutor had sword and shield, thraex fought with curved sword.",
        "category": "weapons",
        "source": "Roman mosaics and historical accounts"
    },
    {
        "text": "Training began at dawn with wooden weapons called rudis. Only experienced gladiators earned real steel weapons.",
        "category": "training",
        "source": "Gladiator training manuals from Pompeii"
    },
    {
        "text": "The doctores were retired gladiators who became trainers. They were respected for their combat knowledge and survival skills.",
        "category": "training",
        "source": "Roman inscriptions from gladiator schools"
    },
    {
        "text": "Gladiators had a special diet rich in barley and beans to build muscle mass. They were called 'hordearii' (barley eaters) by Romans.",
        "category": "daily_life",
        "source": "Analysis of gladiator bones from Ephesus cemetery"
    },
    {
        "text": "The thumbs up or down gesture is a myth. Romans used 'pollice verso' (turned thumb) but the exact meaning is debated by historians.",
        "category": "arena_combat",
        "source": "Roman art analysis and historical texts"
    },
    {
        "text": "Successful gladiators could earn freedom through a wooden sword ceremony called rudis. Some became trainers or bodyguards for wealthy Romans.",
        "category": "freedom",
        "source": "Roman manumission records"
    },
    {
        "text": "The Colosseum could hold 50,000-80,000 spectators. It had a complex system of elevators and tunnels called the hypogeum beneath the arena floor.",
        "category": "colosseum",
        "source": "Modern archaeological surveys"
    },
    {
        "text": "Gladiator fights usually lasted 10-15 minutes. Death was not the primary goal - trained gladiators were expensive investments.",
        "category": "arena_combat",
        "source": "Analysis of Roman gladiator games records"
    }
]

MUGHAL_ARCHITECT_FACTS = [
    {
        "text": "The Taj Mahal took approximately 22 years to complete (1632-1654) and required over 20,000 skilled craftsmen from across the Mughal Empire.",
        "category": "construction",
        "source": "Mughal court chronicles and architectural records"
    },
    {
        "text": "Mughal architecture combines Islamic, Persian, Turkish and Indian architectural styles. The four-garden (charbagh) design represents paradise in Islamic tradition.",
        "category": "design_philosophy",
        "source": "Mughal architectural treatises"
    },
    {
        "text": "The main dome of the Taj Mahal is actually a double dome - an inner dome provides proper interior proportions while the outer dome creates the iconic silhouette.",
        "category": "engineering", 
        "source": "Architectural analysis of Mughal monuments"
    },
    {
        "text": "Pietra dura (stone inlay work) was brought from Italy and perfected by Mughal craftsmen. Semi-precious stones form intricate floral patterns on marble.",
        "category": "decoration",
        "source": "Mughal craft traditions documentation"
    },
    {
        "text": "Shah Jahan built the Taj Mahal as a tomb for his beloved wife Mumtaz Mahal, who died during childbirth in 1631.",
        "category": "history",
        "source": "Mughal court historians like Abdul Hamid Lahori"
    },
    {
        "text": "Mughal architects used precise mathematical proportions. The main gateway is exactly half the height of the main dome, creating perfect visual harmony.",
        "category": "mathematics",
        "source": "Geometric analysis of Mughal monuments"
    },
    {
        "text": "The minarets of the Taj Mahal lean slightly outward so that in case of earthquake, they would fall away from the main tomb structure.",
        "category": "engineering",
        "source": "Structural engineering studies of Mughal architecture"
    },
    {
        "text": "Master craftsmen came from as far as Damascus, Shiraz, and Bukhara. Local Indian artisans learned and adapted these international techniques.",
        "category": "craftsmen",
        "source": "Mughal workshop organization records"
    },
    {
        "text": "Red sandstone was quarried from Fatehpur Sikri, while white marble came from Makrana in Rajasthan, transported by elephant and ox-cart.",
        "category": "materials",
        "source": "Mughal construction logistics records"
    },
    {
        "text": "The Taj Mahal changes color throughout the day - pinkish in morning, white at midday, and golden at sunset, due to the translucent marble properties.",
        "category": "materials",
        "source": "Modern photometric analysis of Makrana marble"
    }
]

EGYPTIAN_SCRIBE_FACTS = [
    {
        "text": "Egyptian scribes used hieroglyphic, hieratic, and demotic scripts. Hieroglyphs were for monuments, hieratic for religious texts, demotic for daily records.",
        "category": "writing_systems",
        "source": "Ancient Egyptian papyri and stone inscriptions"
    },
    {
        "text": "Scribes wrote on papyrus made from papyrus plant stems. The process involved cutting, laying in strips, pressing, and drying under heavy stones.",
        "category": "writing_materials",
        "source": "Ancient Egyptian papyrus manufacturing texts"
    },
    {
        "text": "The god Thoth was the patron deity of scribes. He was depicted with an ibis head and was believed to record the deeds of the dead.",
        "category": "religion",
        "source": "Ancient Egyptian religious texts and tomb paintings"
    },
    {
        "text": "Scribes held high social status in ancient Egypt. They were exempt from taxes and physical labor, serving in temples, courts, and government.",
        "category": "social_status",
        "source": "Ancient Egyptian administrative records"
    },
    {
        "text": "The Rosetta Stone contains the same text in hieroglyphic, demotic, and ancient Greek, which allowed scholars to decode hieroglyphs.",
        "category": "decipherment",
        "source": "Egyptological research on the Rosetta Stone"
    },
    {
        "text": "Scribes used reed pens made from rushes, with black ink made from carbon and gum, and red ink made from ochre for emphasis and corrections.",
        "category": "tools",
        "source": "Analysis of ancient Egyptian writing implements"
    },
    {
        "text": "The House of Life was the ancient Egyptian institution where scribes copied religious texts, medical treatises, and maintained libraries.",
        "category": "education",
        "source": "Ancient Egyptian temple records"
    },
    {
        "text": "Egyptian mathematics used a decimal system but with hieroglyphic symbols. Scribes calculated areas, volumes, and tax assessments.",
        "category": "mathematics",
        "source": "Ancient Egyptian mathematical papyri like the Rhind Papyrus"
    },
    {
        "text": "Medical texts like the Edwin Smith Papyrus show scribes recorded surgical procedures, diagnoses, and treatments with remarkable precision.",
        "category": "medicine",
        "source": "Ancient Egyptian medical papyri"
    },
    {
        "text": "Scribes played a crucial role in the afterlife judgment. They recorded the heart weighing ceremony where souls were judged by Ma'at.",
        "category": "afterlife",
        "source": "Book of the Dead and tomb paintings"
    }
]

# Dictionary to easily access facts by character
HISTORICAL_KNOWLEDGE = {
    "roman_gladiator": ROMAN_GLADIATOR_FACTS,
    "mughal_architect": MUGHAL_ARCHITECT_FACTS, 
    "egyptian_scribe": EGYPTIAN_SCRIBE_FACTS
}
