#!/bin/sh

git clone https://absarails@dev.azure.com/absarails/CVM-Automation/_git/web_connectedBanking
cd web_connectedBanking

git checkout -b JSON_Models
git checkout JSON_Models

git branch --set-upstream-to=origin/main JSON_Models
git pull 

git add /Users/pmerrill/Documents/ABSA Work/models.json
git add /Users/pmerrill/Documents/ABSA Work/critical_models.json
git commit -m "Adding JSON representations for DAI models"
git push origin JSON_Models -f

