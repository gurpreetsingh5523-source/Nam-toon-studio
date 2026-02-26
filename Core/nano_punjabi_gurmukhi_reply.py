"""
Nano Punjabi/Gurmukhi reply module.
Uses indic-transliteration to convert answers to Gurmukhi script.
No bloat: code <10KB, memory use minimal.
"""

from indic_transliteration.sanscript import transliterate, GURMUKHI

# Reply module: English, Punjabi (simple akhar), or Punjabi (Gurmukhi motey akhar)
def reply(text, lang="gurmukhi", font_size=60):
    # Default: Gurmukhi motey akhar, adjustable font size, proper Unicode
    gurmukhi_text = transliterate(text, 'itrans', GURMUKHI)
    gurmukhi_text = gurmukhi_text.encode('utf-8').decode('utf-8')
    if lang == "english":
        return text
    elif lang == "punjabi":
        return text
    elif lang == "gurmukhi":
        return f'<span style="font-size:{font_size}px">{gurmukhi_text}</span>'
    else:
        return f'<span style="font-size:{font_size}px">{gurmukhi_text}</span>'

if __name__ == "__main__":
    gurmukhi_text = "tUsI kivEM ho? main gurmukhi lipi vich jawab de sakadA hAM."
    # Example: Maximum font size for weak eyesight, proper Unicode
    print("Gurmukhi reply:", reply(gurmukhi_text, font_size=60))
