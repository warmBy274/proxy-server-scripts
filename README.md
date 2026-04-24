For setup exit and bridge servers for each other you need:
1. On exit server enter: `xray x25519`
2. Copy private key
3. Enter `bash -c "$(curl -L https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/exit.sh)"`
4. Enter SNI, remember it
5. Enter copied private key
6. In terminal printed client id and short id, remember it
7. On bridge server enter `bash -c "$(curl -L https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/bridge.sh)"`
8. Enter domain that you are buyed for bridge server
9. Enter exit server ip
10. Enter client id from step 6
11. Enter short id from step 6
12. Enter public key/password from step 1
13. Done! Use api for creating clients and managing them
