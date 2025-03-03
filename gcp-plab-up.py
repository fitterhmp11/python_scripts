from netmiko import ConnectHandler

def enable_interfaces():
    fortigate = {
        "device_type": "fortinet",
        "host": "192.168.4.75",
        "username": "plab",
        "password": "!a#n76VZdw3Y^yXi*!op",
    }

    INTERFACES = ["prod", "to-gcp"]
    VDOM = "root"  # Specify the VDOM name

    try:
        conn = ConnectHandler(**fortigate)
        
        # Switch to the correct VDOM
        commands = [
            f"config vdom",  # Enter VDOM configuration mode
            f"edit {VDOM}",  # Select the "root" VDOM
            "config system interface",  # Enter interface configuration mode
        ]
        
        for interface in INTERFACES:
            commands.append(f"edit {interface}")
            commands.append("set status up")
            commands.append("next")
        
        commands.append("end")  # Exit interface configuration mode
        commands.append("end")  # Exit VDOM configuration mode

        output = conn.send_config_set(commands)
        print(f"Enabled interfaces {INTERFACES} in VDOM '{VDOM}':\n{output}")
        
        conn.disconnect()
    except Exception as e:
        print(f"Failed to enable interfaces: {e}")

if __name__ == "__main__":
    enable_interfaces()