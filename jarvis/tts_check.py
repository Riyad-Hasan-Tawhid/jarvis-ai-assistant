"""TTS diagnostic helper for Windows.

Run this to check pyttsx3 init, list voices, and try speaking.
It will also attempt a SAPI fallback via win32com if pyttsx3 fails.
"""
import time

def main():
    print("TTS Diagnostic Script")
    print("---------------------")
    try:
        import pyttsx3
    except Exception as e:
        print("pyttsx3 import failed:", e)
        pyttsx3 = None

    try:
        import win32com.client as win32
    except Exception as e:
        win32 = None

    if pyttsx3 is not None:
        try:
            print("Initializing pyttsx3...")
            e = pyttsx3.init()
            print("pyttsx3 init OK")
            try:
                voices = e.getProperty('voices')
                print(f"Found {len(voices)} voices via pyttsx3")
                for i, v in enumerate(voices):
                    print(i, getattr(v, 'name', ''), getattr(v, 'id', ''))
            except Exception as ve:
                print("Could not enumerate voices:", ve)

            try:
                print("Attempting to speak via pyttsx3...")
                e.say("This is a pyttsx3 test. If you hear this, pyttsx3 is working.")
                e.runAndWait()
                print("pyttsx3 speak attempted")
            except Exception as se:
                print("pyttsx3 speak failed:", se)
        except Exception as ie:
            print("pyttsx3 init failed:", ie)

    # Try SAPI fallback if available
    if win32 is not None:
        try:
            print("Attempting SAPI (win32com) fallback...")
            sapi = win32.Dispatch("SAPI.SpVoice")
            # list SAPI voices
            try:
                vcoll = sapi.GetVoices()
                print(f"Found {vcoll.Count} SAPI voices")
                for i in range(vcoll.Count):
                    try:
                        print(i, vcoll.Item(i).GetDescription())
                    except Exception:
                        print(i, repr(vcoll.Item(i)))
            except Exception as le:
                print("Could not enumerate SAPI voices:", le)

            try:
                sapi.Speak("This is a S A P I test. If you hear this, S A P I is working.")
                print("SAPI speak attempted")
            except Exception as se:
                print("SAPI speak failed:", se)
        except Exception as e:
            print("SAPI initialization failed:", e)

    if pyttsx3 is None and win32 is None:
        print("No TTS engines available. Install pyttsx3 and pypiwin32/comtypes.")

    print("Diagnostic complete.")


if __name__ == '__main__':
    main()
