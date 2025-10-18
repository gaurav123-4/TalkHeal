from googletrans import Translator

# Dictionary of major Indian languages and their codes
indian_languages = {
    "hindi": "hi",
    "bengali": "bn",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "urdu": "ur"
}

def translate_text(text, target_language_code):
    translator = Translator()
    translation = translator.translate(text, dest=target_language_code)
    return translation.text

if __name__ == "__main__":
    print("\n🗣️ Choose an Indian language to translate to:\n")
    for lang in indian_languages:
        print(f"• {lang.capitalize()}")
    
    choice = input("\nEnter language name: ").strip().lower()

    if choice not in indian_languages:
        print("\n❌ Sorry, that language is not supported yet.")
    else:
        text = input("Enter the text to translate: ")
        target_code = indian_languages[choice]
        translated = translate_text(text, target_code)
        print(f"\n✅ Translated in {choice.capitalize()}: {translated}")
