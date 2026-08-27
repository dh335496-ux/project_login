#!/usr/bin/env python3
import subprocess
import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, font
import webbrowser

# تعيين اتجاه النص للعربية
os.environ['LANG'] = 'ar_EG.UTF-8'
os.environ['LC_ALL'] = 'ar_EG.UTF-8'

class LoginProjectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 مشروع تسجيل الدخول")
        self.root.geometry("700x550")
        self.root.configure(bg='#1e1e2f')
        
        # إعداد الخط الذي يدعم العربية
        self.arabic_font = font.Font(family="DejaVu Sans", size=11)
        
        # عنوان
        title = tk.Label(root, text="🚀 مشروع تسجيل الدخول", 
                         font=("DejaVu Sans", 18, "bold"), 
                         fg="#00ccff", bg="#1e1e2f")
        title.pack(pady=10)
        
        # حالة المشروع
        self.status_label = tk.Label(root, text="⏳ جاري التحضير...", 
                                     font=("DejaVu Sans", 12), 
                                     fg="#ffcc00", bg="#1e1e2f")
        self.status_label.pack(pady=5)
        
        # مربع النص لعرض المخرجات (مع دعم النسخ والعربية)
        text_frame = tk.Frame(root, bg="#1e1e2f")
        text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            text_frame, 
            height=15, 
            bg="#2a2a4a", 
            fg="#00ff88",
            font=("DejaVu Sans", 10),
            wrap=tk.WORD,
            selectbackground="#444466",
            selectforeground="white",
            insertbackground="white"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # قائمة السياق للنسخ (زر الفأرة الأيمن)
        self.create_context_menu()
        
        # إطار الأزرار
        button_frame = tk.Frame(root, bg="#1e1e2f")
        button_frame.pack(pady=10)
        
        # زر التشغيل
        self.start_btn = tk.Button(button_frame, text="▶ تشغيل المشروع", 
                                   command=self.start_project,
                                   bg="#00ccff", fg="white", 
                                   font=("DejaVu Sans", 12, "bold"), padx=20, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # زر فتح المتصفح
        self.browser_btn = tk.Button(button_frame, text="🌐 فتح المتصفح", 
                                     command=self.open_browser,
                                     bg="#ffcc00", fg="black", 
                                     font=("DejaVu Sans", 12, "bold"), padx=20, pady=5,
                                     state=tk.DISABLED)
        self.browser_btn.pack(side=tk.LEFT, padx=5)
        
        # زر عرض البيانات
        self.logins_btn = tk.Button(button_frame, text="📁 عرض البيانات", 
                                    command=self.show_logins,
                                    bg="#ff8800", fg="white", 
                                    font=("DejaVu Sans", 12, "bold"), padx=20, pady=5,
                                    state=tk.DISABLED)
        self.logins_btn.pack(side=tk.LEFT, padx=5)
        
        # زر الإيقاف
        self.stop_btn = tk.Button(button_frame, text="⏹ إيقاف", 
                                  command=self.stop_project,
                                  bg="#ff4466", fg="white", 
                                  font=("DejaVu Sans", 12, "bold"), padx=20, pady=5,
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # زر نسخ النص
        self.copy_btn = tk.Button(button_frame, text="📋 نسخ النص", 
                                  command=self.copy_text,
                                  bg="#aa66ff", fg="white", 
                                  font=("DejaVu Sans", 12, "bold"), padx=20, pady=5)
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # زر مسح النص
        self.clear_btn = tk.Button(button_frame, text="🗑️ مسح النص", 
                                   command=self.clear_text,
                                   bg="#666666", fg="white", 
                                   font=("DejaVu Sans", 12, "bold"), padx=20, pady=5)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # متغيرات التشغيل
        self.processes = []
        self.running = False
        self.tunnel_url = ""
        
        self.output_text.insert(tk.END, "📌 اضغط 'تشغيل المشروع' لبدء الخادم\n")
    
    def create_context_menu(self):
        """إنشاء قائمة السياق للنسخ"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="نسخ", command=self.copy_text)
        self.context_menu.add_command(label="تحديد الكل", command=self.select_all)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="مسح النص", command=self.clear_text)
        
        # ربط زر الفأرة الأيمن
        self.output_text.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """عرض قائمة السياق"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def copy_text(self):
        """نسخ النص المحدد أو كامل النص"""
        try:
            selected = self.output_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.status_label.config(text="✅ تم النسخ", fg="#00ff88")
            self.root.after(2000, lambda: self.status_label.config(text="✅ المشروع يعمل" if self.running else "⏳ جاري التحضير..."))
        except tk.TclError:
            # إذا لم يكن هناك نص محدد، انسخ كل النص
            all_text = self.output_text.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(all_text)
            self.status_label.config(text="✅ تم نسخ كل النص", fg="#00ff88")
            self.root.after(2000, lambda: self.status_label.config(text="✅ المشروع يعمل" if self.running else "⏳ جاري التحضير..."))
    
    def select_all(self):
        """تحديد كل النص"""
        self.output_text.tag_add(tk.SEL, "1.0", tk.END)
        self.output_text.mark_set(tk.INSERT, "1.0")
        self.output_text.see(tk.INSERT)
    
    def clear_text(self):
        """مسح النص"""
        self.output_text.delete("1.0", tk.END)
        self.status_label.config(text="🗑️ تم مسح النص", fg="#ffcc00")
        self.root.after(2000, lambda: self.status_label.config(text="✅ المشروع يعمل" if self.running else "⏳ جاري التحضير..."))
    
    def log(self, message):
        """إضافة نص إلى مربع المخرجات"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def start_project(self):
        """تشغيل المشروع بالكامل"""
        if self.running:
            return
        
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.browser_btn.config(state=tk.DISABLED)
        self.logins_btn.config(state=tk.DISABLED)
        self.status_label.config(text="🔄 جاري التشغيل...", fg="#ffcc00")
        
        self.log("")
        self.log("=" * 50)
        self.log("🚀 بدء تشغيل المشروع...")
        
        # الذهاب إلى مجلد المشروع
        os.chdir(os.path.expanduser("~/Desktop/project_login"))
        
        # تشغيل الخادم
        try:
            self.log("📡 تشغيل الخادم...")
            server_process = subprocess.Popen(
                ["python3", "server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8'
            )
            self.processes.append(server_process)
            self.log("✅ الخادم يعمل على http://localhost:8080")
        except Exception as e:
            self.log(f"❌ خطأ في تشغيل الخادم: {e}")
            self.running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            return
        
        # التحقق من وجود Cloudflare
        if not os.path.exists("cloudflared-linux-amd64"):
            self.log("📥 تحميل Cloudflare Tunnel...")
            subprocess.run(["wget", "-q", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"])
            subprocess.run(["chmod", "+x", "cloudflared-linux-amd64"])
            self.log("✅ تم التحميل")
        
        # تشغيل النفق بعد ثانية
        threading.Thread(target=self.start_tunnel, daemon=True).start()
        
        # تحديث الواجهة بعد فترة
        self.root.after(3000, self.update_buttons)
    
    def start_tunnel(self):
        """تشغيل النفق العام"""
        time.sleep(2)
        try:
            self.log("🌐 تشغيل النفق العام...")
            tunnel_process = subprocess.Popen(
                ["./cloudflared-linux-amd64", "tunnel", "--url", "http://localhost:8080"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8'
            )
            self.processes.append(tunnel_process)
            
            # قراءة المخرجات للحصول على الرابط
            for line in tunnel_process.stdout:
                if "trycloudflare.com" in line:
                    self.tunnel_url = line.strip()
                    self.log(f"🌍 {self.tunnel_url}")
                    self.root.after(0, self.browser_btn.config, {'state': tk.NORMAL})
                    self.root.after(0, self.logins_btn.config, {'state': tk.NORMAL})
                elif "INF" in line:
                    self.log(f"   {line.strip()}")
        except Exception as e:
            self.log(f"⚠️ خطأ في النفق: {e}")
    
    def update_buttons(self):
        """تحديث حالة الأزرار"""
        self.status_label.config(text="✅ المشروع يعمل", fg="#00ff88")
    
    def open_browser(self):
        """فتح المتصفح"""
        webbrowser.open("http://localhost:8080")
        self.log("🌐 فتح المتصفح...")
        self.status_label.config(text="🌐 تم فتح المتصفح", fg="#00ccff")
        self.root.after(2000, lambda: self.status_label.config(text="✅ المشروع يعمل" if self.running else "⏳ جاري التحضير..."))
    
    def show_logins(self):
        """عرض البيانات المسجلة"""
        logins_file = os.path.expanduser("~/Desktop/project_login/logins.txt")
        try:
            with open(logins_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if content.strip():
                self.log("")
                self.log("=" * 50)
                self.log("📁 البيانات المسجلة:")
                self.log(content.strip())
            else:
                self.log("📁 لا توجد بيانات مسجلة بعد")
        except FileNotFoundError:
            self.log("📁 لا توجد بيانات مسجلة بعد")
    
    def stop_project(self):
        """إيقاف المشروع"""
        self.log("")
        self.log("⏹ جاري إيقاف المشروع...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=3)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        self.processes.clear()
        self.running = False
        self.tunnel_url = ""
        
        self.status_label.config(text="⏹ متوقف", fg="#ff4466")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.browser_btn.config(state=tk.DISABLED)
        self.logins_btn.config(state=tk.DISABLED)
        
        self.log("✅ تم إيقاف المشروع")
        self.log("=" * 50)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginProjectGUI(root)
    root.mainloop()
