"""Photoreal shot list. Grounded hard sci-fi: practical light, real materials, anamorphic."""

STYLE = (
    "photorealistic cinematic film still from a hard science fiction feature film, "
    "shot on 35mm anamorphic lenses, practical in-camera lighting, volumetric atmospheric haze, "
    "realistic weathered metal and scorched composite panels, accurate physical materials, "
    "restrained desaturated color grade, deep inky blacks, subtle anamorphic lens flare, "
    "shallow depth of field, fine natural film grain, extremely detailed, 8k, "
    "no text, no logo, no watermark, no subtitles"
)

NEG = ("ground, floor, sand, desert, horizon line, water, ocean, beach, landscape, cartoon, anime, illustration, painting, drawing, concept art, cgi render, videogame, "
       "plastic, toy, oversaturated, neon, text, watermark, logo, signature, blurry, low quality, "
       "deformed, extra limbs, distorted faces")

# scene_id -> (prompt, seed)
SHOTS = {
    "title_card": (
        "almost entirely empty deep space, pure black void, a very faint dim nebula low in the "
        "far distance, sparse cold stars, no bright light source, vast emptiness and negative space, "
        "extremely dark and minimal, ominous stillness", 3301),

    "void_hunter": (
        "the immense armored hull of an alien predator warship looming in interstellar darkness, "
        "kilometers long, ribbed organic-mechanical plating, sparse faint green sensor apertures, "
        "hard raking starlight along the hull, overwhelming sense of scale, cold void", 2201),

    "graveyard": (
        "dozens of shattered derelict starship hulls floating weightless in the black void of outer space, "
        "tumbling at random angles with no ground and no horizon, one huge broken hull torn open in the "
        "foreground, wrecks receding into pure blackness, frozen debris suspended in zero gravity, "
        "starfield behind, one small amber emergency beacon on a distant hull, orbital space graveyard", 3312),

    "arrival": (
        "a lone angular human warship emerging from a blinding blue-white tear in space, "
        "scarred grey ablative armor plating, hull markings, engines glowing, "
        "a distant derelict ship far ahead in the dark, wide establishing shot, epic scale", 2203),

    "deathworld": (
        "Earth seen from low orbit as a violent deathworld, colossal cyclonic storm systems, "
        "lightning flashing in chains across the night terminator, scorched ochre continents, "
        "impossibly thin fragile atmosphere glowing at the limb, beautiful and hostile", 2204),

    "hud_signal": (
        "interior of a darkened military spacecraft bridge, a soldier in fatigues silhouetted "
        "against a large holographic waveform and spectrogram analysis display, cold blue "
        "instrument glow on their face, banks of worn physical switches, moody practical lighting", 2205),

    "turn_toward": (
        "a huge human capital warship seen from directly behind in the absolute blackness of deep space, "
        "four enormous engine bells igniting brilliant blue-white, long ion exhaust plumes, "
        "scarred grey armored hull receding away from camera, cold starfield all around, "
        "a single tiny green beacon far ahead in the dark, no atmosphere, no planet", 3303),

    "decloak": (
        "three mountain-sized alien carriers decloaking in deep space, rippling optical distortion "
        "sliding off their enormous hulls as they become visible, a single tiny human ship "
        "dwarfed in the foreground for scale, sickly green running lights, ominous and overwhelming", 2207),

    "corridor": (
        "brutal close quarters firefight inside a cramped derelict spaceship corridor, "
        "human soldiers in matte black powered armor moving fast, blinding orange plasma cutter glare, "
        "showers of sparks, smoke and floating debris, harsh backlighting, "
        "gritty handheld combat cinematography, motion blur", 2208),

    "core": (
        "cavernous alien starship reactor chamber, a towering column of contained green plasma, "
        "industrial catwalks, immense cabling and coolant conduits, "
        "tiny human soldiers silhouetted on a gantry for scale, heavy volumetric light shafts", 2209),

    "broadcast": (
        "a derelict starship transmitting an enormous beacon pulse into deep space, "
        "concentric rings of energy expanding outward, distant human warships converging from all "
        "directions with long engine trails, warm amber light against absolute black", 2210),

    "swarm": (
        "an immense alien battle fleet engulfed in a vast glittering cloud of millions of tiny drones, "
        "sensor masts and antenna arrays stripped bare, capital ships going dark one by one, "
        "cold blue drone haze, apocalyptic scale, silent horror", 2211),

    "buried": (
        "a ruined Earth city skyline half buried under grey ash dunes, dying red sun through thick haze, "
        "a colossal armored vault door partially excavated from the debris, "
        "cold blue light spilling out from within, post apocalyptic archaeology, awe and dread", 2212),

    "admiral": (
        "low angle portrait of a towering alien fleet admiral in heavy dark ceremonial armor, "
        "elongated chitinous armored skull, one cold glowing amber eye, backlit by dim green bridge light, "
        "imposing and predatory, deep shadow, shallow focus, menacing authority", 3304),

    "promise": (
        "extreme close up of a human soldier's battle scarred helmet visor, "
        "the reflection of a burning alien warship filling the curved visor glass, "
        "faint green HUD reticle, scratches and soot on the armor, intense and still", 2214),

    "finale": (
        "the Milky Way galactic core seen from deep space, immense luminous star clouds and dark dust lanes, "
        "one tiny human ship silhouetted heading outward, warm distant light, "
        "overwhelming vastness, awe, hope", 2215),

    "end_card": (
        "a quiet dark starfield, one faint distant nebula, deep black empty space, "
        "minimal, still, contemplative", 2216),
}
