import edge_tts
import asyncio
import nest_asyncio
import os
import tkinter as tk
from tkinter import messagebox
import pygame
from main import get_translation
from langdetect import detect, DetectorFactory




# فعال‌سازی nest_asyncio برای استفاده از asyncio.run()
nest_asyncio.apply()




async def main(text, target_lang):
    model_path = r"E:\University\master\mbaheseVijeh\project_AI\Translate_\Translate_Models\models"

    # ترجمه متن
    translated_text = get_translation(model_path, text, target_lang)

    # نمایش ترجمه
    if translated_text:
        print(f"متن اصلی: {text}")
        print(f"ترجمه به زبان گفتار: {translated_text}")

    return translated_text

class TextToSpeechApp:
    def __init__(self,master,  text):
        self.master = master
        master.title("Text to Speech")
        self.text = text # دریافت متن از ورودی

        self.output_file = "output_farid5.mp3"

        self.label = tk.Label(master, text="تبدیل متن به گفتار")
        self.label.pack()

        self.play_button = tk.Button(master, text="پخش صدا", command=self.play_audio)
        self.play_button.pack()

        self.download_button = tk.Button(master, text="دانلود صدا", command=self.download_audio)
        self.download_button.pack()

        asyncio.run(self.generate_audio(self.text))  # تولید صدا و پخش خودکار هنگام شروع برنامه

        asyncio.run(self.generate_audio(self.text)) # تولید صدا و پخش خودکار هنگام شروع برنامه


    async def generate_audio(self,text,voice="fa-IR-faridNeural"):
        # استفاده از صدای FaridNeural
        self.text_speech=text
        self.voice_speech=voice
        communicate = edge_tts.Communicate(self.text_speech,self.voice_speech)
        try:
            await communicate.save(self.output_file)
            print("File saved successfully.")
            self.play_audio() # پخش خودکار صدا پس از تولید
        except Exception as e:
            print("Error saving file:", e)

    def play_audio(self):
        if os.path.exists(self.output_file):
            try:
                # پخش فایل صوتی با استفاده از pygame
                pygame.mixer.init()
                pygame.mixer.music.load(self.output_file)
                pygame.mixer.music.play()
                print("Audio is playing...")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading or playing audio: {e}")
        else:
            messagebox.showwarning("File Not Found", "File does not exist.")

    def download_audio(self):
        if os.path.exists(self.output_file):
            try:
                import shutil
                shutil.copy(self.output_file, os.path.expanduser("~/Downloads"))
                messagebox.showinfo("Download", "File downloaded to Downloads folder.")
            except Exception as e:
                messagebox.showerror("Error", f"Error downloading file: {e}")
        else:
            messagebox.showwarning("File Not Found", "File does not exist.")


class LanguageSelector:
    def __init__(self):
        """ایجاد یک شیء جدید از کلاس LanguageSelector."""
        self.languages = [
            {'fa': 'fa-IR-faridNeural'},
            {'en': 'en-US-faridNeural'},
            {'fr': 'fr-FR-faridNeural'},
            {'de': 'de-DE-faridNeural'},
            {'it': 'it-IT-faridNeural'}
        ]
        self.selected_language = None  # متغیر برای ذخیره زبان انتخاب شده

    def main(self):

        # نمایش مقادیر دیکشنری‌ها به کاربر بدون نمایش کلیدها
        # print("مقادیر موجود در دیکشنری‌ها:")
        # for d in self.languages:
        #    for value in d.values():
        #        print(value)

        print("تمایل دارید پایختان را به چه زبانی دریافت کنید؟ از بین زبان ها انتخاب نمایید:")
        print("en-US-faridNeural, fa-IR-faridNeural, fr-FR-faridNeural, de-DE-faridNeural, it-IT-faridNeural")
        # دریافت مقدار انتخابی از کاربر
        self.target_lang_ = input("\nاز بین زبان های نام برده شده انتخاب نمایید: ")

        # جستجو در لیست دیکشنری‌ها
        self.selected_language = None  # برای ذخیره کلید یافت‌شده

        for d in self.languages:
            for key, value in d.items():
                if value == self.target_lang_:
                    self.selected_language = key
                    break
            if self.selected_language:  # اگر کلید پیدا شد، از حلقه خارج می‌شویم
                break

        # چاپ کلید مربوط به مقدار واردشده
        if self.selected_language:
            print("نوع زبان مدنظر شما جهت گفتار:", self.selected_language)
        else:#اگر نوع زبان گفتار پیدا نشد به طور پیش فرض فارسی در نظر گرفته شود
            self.selected_language='fa'
            print("زبانی که مدنظر شما است به زودی پشتیبانی می شود در حال حاضر این زبان توسط تیم پشتیبانی نشده است.")




class LanguageDetector:
    def __init__(self):
        pass

    def detect_language(self, text):
        """تشخیص زبان یک متن و برگرداندن آن
        :param text: متنی که زبان آن باید شناسایی شود
        :return: زبان تشخیص داده شده
        """
        if not text: # بررسی اینکه آیا متن ورودی خالی است
            print("متن ورودی خالی است.")
            return None

        try:
            language = detect(text) # تشخیص زبان
            return language # برگرداندن زبان تشخیص داده شده
        except Exception as e:
            print(f"خطا در تشخیص زبان: {e}")
            return None # در صورت خطا، None برگردانده می‌شود

class Speech:
    def __init__(self, select_voice_type_=None):
        self.select_voice_type_ = select_voice_type_


    def compression(self):
        self.class_detector_instance = LanguageDetector()
        text_type = self.class_detector_instance.detect_language(generated_text)
        if text_type:  # اگر زبان تشخیص داده شده وجود داشته باشد
            print(f"زبان متن: {text_type}")  # چاپ زبان تشخیص داده شده
        else:
            print("تشخیص زبان ناموفق بود.")  # در صورت عدم موفقیت در تشخیص

    def print_speech_type(self):
        if self.select_voice_type_:
            print(f"نوع زبان گفتار: {self.select_voice_type_}")

            self.translated_text = asyncio.run(main(generated_text, self.select_voice_type_))

            return self.translated_text

        else:
            return 0
            # اگز نوع زبان گفتار مشخص نشد.
            # select_voice_type='fa'
            # ابتدا بررسی می شود نوع زبان متن چیست
            #یعنی لازم است کلاس detector فراخوانی بشود
            #برای اینکه از یک کلاس یک متد از کلاس دیگر فراخوانی شود باید نمونه بسازی




# اجرای برنامه و ارسال متن تولید شده به کلاس
if __name__ == "__main__":

    generated_text = "Je me lève à sept heures du matin."
    # این متن از قطعه کد قبلی دریافت می‌شود


    #برای انتخاب نوع زبان گفتارclassLanguageSelector
    selector = LanguageSelector()
    selector.main()
    # می‌توانیم زبان انتخاب شده را در اینجا نیز چاپ کنیم
    select_voice_type=selector.selected_language
    #print("==>",select_voice_type)

    #اگر نوع زبان گفتار مشخص شد
    #  باید متن به زبان انتخابی ترجمه شود

    speech1 = Speech(select_voice_type)
    translated_text_speech1=speech1.print_speech_type()
    #print("====>",speech1.print_speech_type())

    #صدا تولید شو
    root = tk.Tk()
    app = TextToSpeechApp( root,translated_text_speech1)


    #اگز نوع زبان گفتار مشخص نشد.
    #select_voice_type='fa'
    #ابتدا بررسی می شود نوع زبان متن چیست

    detector = LanguageDetector()
    text_type=detector.detect_language(generated_text)
    if text_type:  # اگر زبان تشخیص داده شده وجود داشته باشد
        print(f"زبان متن: {text_type}")  # چاپ زبان تشخیص داده شده
    else:
        print("تشخیص زبان ناموفق بود.")  # در صورت عدم موفقیت در تشخیص


    #اگر نوع زبان متن فارسی باشد نیاز به ترجمه نیست
    # چون سیستم به طور پیش فرض صدای فارسی پخش می کند
    #اگر نوع زبان متن غیرفارسی بود متن باید ترجمه شود به فارسی چون سیستم پیش فرض فارسی صحبت می کند.

    root.mainloop()
