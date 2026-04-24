apt update -y && apt upgrade -y
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

curl -L -o /usr/local/etc/xray/config.json https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/exit.json
clientid = xray uuid
sed -i "s/CLIENT_ID/${clientid}/g" /usr/local/etc/xray/config.json
read -p "Enter exit SNI: " sni
sed -i "s/SNI/${sni}/g" /usr/local/etc/xray/config.json
read -p "Enter exit private key: " privkey
sed -i "s/PRIVATE_KEY/${privkey}/g" /usr/local/etc/xray/config.json
shortid = openssl rand -hex 2
sed -i "s/SHORT_ID/${shortid}/g" /usr/local/etc/xray/config.json

echo "Bridge client id: ${clientid}"
echo "Short id: ${shortid}"
systemctl restart --now xray
