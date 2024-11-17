# cloud-wiz-fmops
FMOops platform that can be used in real life through generative AI

# Install & Start
```
sudo npm install && sudo npm start
```
# Fast API Docs
### local
http://localhost:8000/docs#/

### prod
https://be.cloudwiz-ai.com/docs#

# GIT
### connection
```
git remote add origin https://github.com/easyooops/cloud-wiz-fmops.git

git remote -v
```
### create branch
```
# git checkout -b [new branch]
git checkout -b feature-suyeong

git branch
```
### Pull Request
```
git add .

# git commit -m "[comment]"
git commit -m "Save current changes before pulling latest updates"

# git push origin [new branch]
git push origin feature-suyeong
```
### Pull Main
```
git status

git add .

git commit -m "Save current changes before pulling latest updates"

git stash

git pull origin main

```

# alembic

### 마이그레이션 생성
```
alembic revision --autogenerate -m "edit agent table"
```

### 마이그레이션 적용
```
alembic upgrade head
```