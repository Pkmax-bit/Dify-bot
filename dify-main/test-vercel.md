# Deploy Dify Web lên Vercel (Miễn phí)

## Bước 1: Prepare Code
```bash
# Tạo file vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install"
}
```

## Bước 2: Deploy
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy từ thư mục web/
cd web
vercel

# Follow prompts:
# - Project name: dify-web
# - Framework: Next.js
# - Root directory: ./
```

## Bước 3: Configure Environment
```bash
# Add environment variables in Vercel dashboard
NEXT_PUBLIC_API_PREFIX=https://your-api-url.com
NEXT_PUBLIC_EDITION=SELF_HOSTED
```

## Kết quả
- Web: https://dify-web-username.vercel.app
- Auto-deploy từ Git commits
- Global CDN
- Free SSL

## Ưu điểm
✅ Hoàn toàn miễn phí
✅ Deploy tự động từ Git  
✅ Global CDN nhanh
✅ Custom domain
✅ SSL miễn phí
