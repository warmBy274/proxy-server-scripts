apt update -y && apt upgrade -y
apt install certbot -y
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

read -p "Enter bridge domain: " domain
certbot certonly --standalone -d $domain
chmod u+x -R /etc/letsencrypt/
chmod g+x -R /etc/letsencrypt/
chmod o+x -R /etc/letsencrypt/

curl -L -o /usr/local/etc/xray/config.json https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/bridge.json
sed -i "s/BRIDGE_DOMAIN/${domain}/g" /usr/local/etc/xray/config.json
fullchain="/etc/letsencrypt/live/${domain}/fullchain.pem"
sed -i "s/CERTIFICATE_FULLCHAIN/${fullchain}/g" /usr/local/etc/xray/config.json
privkey="/etc/letsencrypt/live/${domain}/privkey.pem"
sed -i "s/CERTIFICATE_PRIVATE/${privkey}/g" /usr/local/etc/xray/config.json
read -p "Enter exit IP: " exitip
sed -i "s/EXIT_IP/${exitip}/g" /usr/local/etc/xray/config.json
read -p "Enter exit client id: " client
sed -i "s/EXIT_CLIENT/${client}/g" /usr/local/etc/xray/config.json
read -p "Enter exit short id: " shortid
sed -i "s/EXIT_SHORT_ID/${shortid}/g" /usr/local/etc/xray/config.json
read -p "Enter exit public key: " pubkey
sed -i "s/EXIT_PUBLIC_KEY/${pubkey}/g" /usr/local/etc/xray/config.json

systemctl restart --now xray
