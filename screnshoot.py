import pyscreenshot as ImageGrab
import datetime
import cv2
import numpy as np
import pyautogui
import time
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.paused = False
        self.video_writer = None
        self.fps = 20.0
        self.output_file = None
        self.screen_size = None
        
    def screenshot(self, area=None):
        """Ambil screenshot"""
        try:
            if area:
                # Screenshot area tertentu
                img = ImageGrab.grab(bbox=area)
            else:
                # Screenshot full screen
                img = ImageGrab.grab()
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            img.save(filename)
            
            print(f"✅ Screenshot saved as: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None

    def start_recording(self, filename=None, area=None, fps=20):
        """Mulai rekam layar"""
        try:
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.mp4"
            
            self.fps = fps
            self.output_file = filename
            
            # Tentukan ukuran layar
            if area:
                self.screen_size = (area[2] - area[0], area[3] - area[1])
            else:
                screen = pyautogui.size()
                self.screen_size = (screen.width, screen.height)
            
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                filename, 
                fourcc, 
                self.fps, 
                self.screen_size
            )
            
            self.recording = True
            self.paused = False
            
            print(f"🎥 Recording started: {filename}")
            print(f"📐 Resolution: {self.screen_size[0]}x{self.screen_size[1]}")
            print(f"⏱️ Press 'q' to stop recording")
            
            # Mulai thread recording
            self.recording_thread = threading.Thread(target=self._record_loop, args=(area,))
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            return True
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return False

    def _record_loop(self, area=None):
        """Loop rekaman layar"""
        while self.recording:
            if not self.paused:
                try:
                    # Capture layar
                    if area:
                        screenshot = pyautogui.screenshot(region=area)
                    else:
                        screenshot = pyautogui.screenshot()
                    
                    # Convert PIL to numpy array
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # Tulis ke video
                    self.video_writer.write(frame)
                    
                    # Delay sesuai FPS
                    time.sleep(1.0 / self.fps)
                except Exception as e:
                    print(f"Recording loop error: {e}")
                    break
            
        # Stop recording
        if self.video_writer:
            self.video_writer.release()
        print(f"✅ Recording saved as: {self.output_file}")

    def stop_recording(self):
        """Hentikan rekaman"""
        self.recording = False
        if self.video_writer:
            self.video_writer.release()
        print("⏹️ Recording stopped")

    def pause_recording(self):
        """Pause rekaman"""
        self.paused = True
        print("⏸️ Recording paused")

    def resume_recording(self):
        """Lanjutkan rekaman"""
        self.paused = False
        print("▶️ Recording resumed")

def select_area():
    """Pilih area dengan mouse"""
    print("📐 Silakan pilih area dengan mouse...")
    try:
        # Simple area selection using tkinter
        root = tk.Tk()
        root.title("Select Area")
        root.attributes('-alpha', 0.3)
        root.geometry("200x100")
        
        result = []
        def on_click():
            root.destroy()
            # Simulasi select area (gunakan pyautogui untuk capture)
            print("Klik OK, lalu drag untuk memilih area...")
            # Di sini kita bisa menggunakan pyautogui untuk select area
            result.append((0, 0, 800, 600))  # Contoh area
            
        btn = tk.Button(root, text="Select Area", command=on_click, font=("Arial", 14))
        btn.pack(expand=True)
        root.mainloop()
        return result[0] if result else None
    except:
        return None

def main():
    recorder = ScreenRecorder()
    
    print("\n" + "="*50)
    print("        📸 SCREENSHOOT - Advanced Tool")
    print("="*50)
    print("1. Screenshot Full Screen")
    print("2. Screenshot Area")
    print("3. Record Screen (Full)")
    print("4. Record Screen (Area)")
    print("5. Screenshot dengan Timer")
    print("6. Exit")
    print("="*50)
    
    while True:
        choice = input("\nPilih menu (1-6): ")
        
        if choice == '1':
            # Screenshot full
            recorder.screenshot()
            
        elif choice == '2':
            # Screenshot area
            print("📐 Klik OK di window yang muncul, lalu pilih area...")
            # Simplified: capture full screen with delay
            time.sleep(2)
            recorder.screenshot()
            
        elif choice == '3':
            # Record full screen
            recorder.start_recording(fps=20)
            input("\nTekan Enter untuk berhenti rekaman...")
            recorder.stop_recording()
            
        elif choice == '4':
            # Record area
            print("📐 Masukkan koordinat area (x1 y1 x2 y2)")
            try:
                coords = input("Contoh: 0 0 800 600\n").split()
                if len(coords) == 4:
                    area = tuple(map(int, coords))
                    recorder.start_recording(area=area, fps=20)
                    input("\nTekan Enter untuk berhenti rekaman...")
                    recorder.stop_recording()
                else:
                    print("❌ Format koordinat salah!")
            except:
                print("❌ Input tidak valid!")
                
        elif choice == '5':
            # Screenshot dengan timer
            try:
                delay = int(input("Masukkan delay (detik): "))
                print(f"⏱️ Screenshot akan diambil dalam {delay} detik...")
                time.sleep(delay)
                recorder.screenshot()
            except:
                print("❌ Input tidak valid!")
                
        elif choice == '6':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()
