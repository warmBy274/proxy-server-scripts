from paramiko import *
from requests import get
from uuid import uuid4
from cryptography.hazmat.primitives.asymmetric import x25519
from base64 import urlsafe_b64encode
from secrets import token_hex

def generate_x25519():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    return (urlsafe_b64encode(private_key.private_bytes_raw()).decode().removesuffix("="), urlsafe_b64encode(public_key.public_bytes_raw()).decode().removesuffix("="))

def configure_exit(client: SSHClient):
    _, stdout, stderr = client.exec_command("apt update && apt upgrade -y")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
    print(stdout.read().decode())
    print(stderr.read().decode())

    config = str(get("https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/exit.json").text)
    bridge_client_id = str(uuid4())
    sni = input("Enter SNI for exit server: ")
    private_key, public_key = generate_x25519()
    short_id = token_hex(4)

    config = config.replace("BRIDGE_CLIENT_ID", bridge_client_id)
    config = config.replace("SNI", sni)
    config = config.replace("PRIVATE_KEY", private_key)
    config = config.replace("SHORT_ID", short_id)

    sftp = client.open_sftp()
    with sftp.open("/usr/local/etc/xray/config.json", "w") as file:
        file.write(config)
    sftp.close()

    _, stdout, stderr = client.exec_command("systemctl restart --now xray")
    print(stdout.read().decode())
    print(stderr.read().decode())

    return (bridge_client_id, public_key, sni, short_id)

def configure_bridge(client: SSHClient, exit_ip, bridge_client_id, public_key, sni, short_id):
    _, stdout, stderr = client.exec_command("apt update && apt upgrade -y")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("apt install certbot -y")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
    print(stdout.read().decode())
    print(stderr.read().decode())

    create_test_client = True if input("Create test client? y/N: ") == "y" else False
    config = str(get("https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/bridge.json").text)
    if create_test_client:
        config = str(get("https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/bridge_with_test_client.json").text)
    domain = input("Enter bridge server domain: ")
    test_client_id = str(uuid4())
    try:
        with open(input("Enter fallback html file path: "), "r") as file:
            html_data = file.read()
    except:
        html_data = ""

    config = config.replace("TEST_CLIENT_ID", test_client_id)
    config = config.replace("DOMAIN", domain)
    config = config.replace("CERTIFICATE_FULLCHAIN", f"/etc/letsencrypt/live/{domain}/fullchain.pem")
    config = config.replace("CERTIFICATE_PRIVATE", f"/etc/letsencrypt/live/{domain}/privkey.pem")
    config = config.replace("EXIT_IP", exit_ip)
    config = config.replace("BRIDGE_CLIENT_ID", bridge_client_id)
    config = config.replace("PUBLIC_KEY", public_key)
    config = config.replace("SNI", sni)
    config = config.replace("SHORT_ID", short_id)

    _, stdout, stderr = client.exec_command(f"certbot certonly --standalone -d {domain} -n --agree-tos --register-unsafely-without-email")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("chmod o+x -R /etc/letsencrypt/")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("chmod o+r -R /etc/letsencrypt/")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("apt install nginx -y")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("touch /var/www/html/index.html")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("touch /etc/nginx/sites-available/fallback")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("ln /etc/nginx/sites-available/fallback /etc/nginx/sites-enabled/")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("rm /etc/nginx/sites-enabled/default")
    print(stdout.read().decode())
    print(stderr.read().decode())

    sftp = client.open_sftp()
    with sftp.open("/usr/local/etc/xray/config.json", "w") as file:
        file.write(config)
    with sftp.open("/var/www/html/index.html", "w") as file:
        file.write(html_data)
    with sftp.open("/etc/nginx/sites-available/fallback", "w") as file:
        file.write(str(get("https://raw.githubusercontent.com/warmBy274/proxy-server-scripts/refs/heads/main/nginx.config").text))
    sftp.close()

    _, stdout, stderr = client.exec_command("systemctl restart --now xray")
    print(stdout.read().decode())
    print(stderr.read().decode())
    _, stdout, stderr = client.exec_command("systemctl restart --now nginx")
    print(stdout.read().decode())
    print(stderr.read().decode())

    if create_test_client:
        print("Test client ID:", test_client_id)

def main():
    exit_ip = input("Enter exit ip: ")
    bridge_ip = input("Enter bridge ip: ")

    exit_client = SSHClient()
    exit_client.set_missing_host_key_policy(AutoAddPolicy())
    exit_client.connect(exit_ip, 22, "root")

    bridge_client = SSHClient()
    bridge_client.set_missing_host_key_policy(AutoAddPolicy())
    bridge_client.connect(bridge_ip, 22, "root")

    bridge_client_id, public_key, sni, short_id = configure_exit(exit_client)
    configure_bridge(bridge_client, exit_ip, bridge_client_id, public_key, sni, short_id)

    input("Servers successfully configured!\nPress enter to close the window")

if __name__ == "__main__":
    main()
