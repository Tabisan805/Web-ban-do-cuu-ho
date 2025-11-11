# cuuho

Ngắn: hướng dẫn nhanh để đẩy project lên GitHub.

Các bước cơ bản:
1. Mở terminal tại `e:\BaiTap\CDS\cuuho`
2. Khởi tạo và commit:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Tạo remote và đẩy lên GitHub:
   ```
   git branch -M main
   git remote add origin https://github.com/<USERNAME>/<REPO>.git
   git push -u origin main
   ```
   Hoặc dùng GitHub CLI:
   ```
   gh repo create <USERNAME>/<REPO> --public --source=. --remote=origin --push
   ```

Nếu đã commit `data/` trước khi thêm `.gitignore`, loại bỏ nó khỏi index:
```
git rm -r --cached data
git commit -m "Remove data from repo"
git push
```
