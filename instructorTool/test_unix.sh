#curl -u "$1:$5" https://api.github.com/user/repos -d "{\"name\":\"$4\",\"private\":\"True\"}"
cd /home/ec2-user/SER_517_Software_Factory_group5-master
git clone https://github.com/amehlhase316/memoranda.git
cd memoranda
rm -rf .git
cd ..
git clone https://$1@github.com/$2/$3.git
cd $3
cp -r ../memoranda/* .
git add .
git commit -m "Initializing the folder structure"
git push
rm -rf ../memoranda
rm -rf ../$3 