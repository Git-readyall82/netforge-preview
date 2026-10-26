
"""NETFORGE — Cisco IOS Command Library API.

Provides searchable Cisco IOS command references and explanations.
"""

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
BASE_DIR = __import__("pathlib").Path(__file__).parent

CATEGORIES = [
    {"id": "basic-security", "title": "Basic Device & Security Setup"},
    {"id": "interfaces-wan", "title": "Interface & WAN Configuration"},
    {"id": "dhcp", "title": "DHCP Server, Client & Relay"},
    {"id": "switch-routing", "title": "Switch Management & Static Routing"},
    {"id": "dhcp-snooping", "title": "DHCP Snooping Security"},
    {"id": "ssh", "title": "SSH Secure Remote Access"},
    {"id": "vlan", "title": "VLANs & Router-on-a-Stick"},
    {"id": "nat", "title": "OSPF Routing & PAT (NAT Overload)"},
    {"id": "ospf", "title": "OSPF Area 0"},
]

COMMANDS = [
    {
        "id": "hostname",
        "category": "basic-security",
        "title": "Configure a Hostname",
        "command": "hostname R1",
        "mode": "Global configuration",
        "purpose": "Sets the device hostname to R1.",
        "explanation": "The hostname identifies the router in the CLI prompt and helps distinguish devices.",
        "example": "Router(config)# hostname R1\nR1(config)#",
        "caution": "Run this command in global configuration mode."
    },
    {
        "id": "motd",
        "category": "basic-security",
        "title": "Message of the Day Banner",
        "command": "banner motd #Authorized access only#",
        "mode": "Global configuration",
        "purpose": "Displays a login banner to users accessing the device.",
        "explanation": "The character # marks the beginning and end of the banner text. Choose a delimiter that does not appear in the message.",
        "example": "R1(config)# banner motd #Authorized access only#",
        "caution": "Use wording approved for your network environment."
    },
    {
        "id": "disable-dns-lookup",
        "category": "basic-security",
        "title": "Disable DNS Lookup",
        "command": "no ip domain-lookup",
        "mode": "Global configuration",
        "purpose": "Stops the device from trying to resolve mistyped CLI commands as hostnames.",
        "explanation": "This can prevent delays after a command is entered incorrectly.",
        "example": "R1(config)# no ip domain-lookup",
        "caution": "This disables the device's CLI DNS lookup behavior; it is not a general DNS security control."
    },
    {
        "id": "enable-secret",
        "category": "basic-security",
        "title": "Set an Enable Secret",
        "command": "enable secret YOUR_STRONG_SECRET",
        "mode": "Global configuration",
        "purpose": "Sets the secret used to enter privileged EXEC mode.",
        "explanation": "The enable secret is stored in a protected form by IOS. Use a unique, strong secret rather than a sample password.",
        "example": "R1(config)# enable secret YOUR_STRONG_SECRET",
        "caution": "Do not reuse passwords from examples in production."
    },
    {
        "id": "console-security",
        "category": "basic-security",
        "title": "Configure Console Access",
        "command": "line console 0\nlogin\nlogging synchronous",
        "mode": "Line configuration",
        "purpose": "Configures console access and keeps system messages from disrupting typed commands.",
        "explanation": "The login command requires the configured line authentication method. logging synchronous redisplays the command prompt after log messages.",
        "example": "R1(config)# line console 0\nR1(config-line)# password YOUR_CONSOLE_PASSWORD\nR1(config-line)# login\nR1(config-line)# logging synchronous",
        "caution": "For stronger deployments, prefer supported user-based authentication and access controls."
    },
    {
        "id": "show-ip-interface-brief",
        "category": "interfaces-wan",
        "title": "Summarize IP Interfaces",
        "command": "show ip interface brief",
        "mode": "Privileged EXEC",
        "purpose": "Shows interface names, IP addresses, and interface and line protocol status.",
        "explanation": "Use this command for a quick check after configuring interfaces or troubleshooting connectivity.",
        "example": "R1# show ip interface brief",
        "caution": "An interface can have an IP address configured and still be down."
    },
    {
        "id": "serial-interface",
        "category": "interfaces-wan",
        "title": "Configure a Serial Interface",
        "command": "interface serial 0/0/0\nip address 192.168.2.1 255.255.255.0\nno shutdown",
        "mode": "Global configuration, then interface configuration",
        "purpose": "Assigns an IPv4 address to a serial interface and enables it.",
        "explanation": "The interface identifier depends on the installed hardware and device model. The description command can document the remote endpoint.",
        "example": "R1(config)# interface serial 0/0/0\nR1(config-if)# description Connected To R2\nR1(config-if)# ip address 192.168.2.1 255.255.255.0\nR1(config-if)# no shutdown",
        "caution": "A clock rate is normally configured on the DCE end of a supported serial link. Verify the actual interface and cable."
    },
    {
        "id": "dhcp-pool",
        "category": "dhcp",
        "title": "Create a DHCP Pool",
        "command": "ip dhcp pool MY_LAN",
        "mode": "Global configuration",
        "purpose": "Creates a DHCP pool for dynamically assigning client network settings.",
        "explanation": "Inside the pool configuration, define the network and subnet mask, default gateway, and optional DNS server.",
        "example": "R1(config)# ip dhcp excluded-address 192.168.1.1\nR1(config)# ip dhcp pool MY_LAN\nR1(dhcp-config)# network 192.168.1.0 255.255.255.0\nR1(dhcp-config)# default-router 192.168.1.1\nR1(dhcp-config)# dns-server 8.8.8.8",
        "caution": "Exclude addresses that must remain statically assigned. Ensure the pool matches the actual LAN."
    },
    {
        "id": "dhcp-binding",
        "category": "dhcp",
        "title": "View DHCP Bindings",
        "command": "show ip dhcp binding",
        "mode": "Privileged EXEC",
        "purpose": "Lists DHCP address bindings maintained by the device's DHCP server.",
        "explanation": "Use it to inspect leased IP addresses and associated client identifiers.",
        "example": "R1# show ip dhcp binding",
        "caution": "This displays bindings on the local DHCP server, not every DHCP lease in the network."
    },
    {
        "id": "dhcp-helper",
        "category": "dhcp",
        "title": "Configure a DHCP Relay",
        "command": "ip helper-address 192.168.2.100",
        "mode": "Interface configuration",
        "purpose": "Forwards supported UDP broadcasts, including DHCP requests, toward a specified server.",
        "explanation": "A relay allows clients and a DHCP server to communicate across different IP subnets.",
        "example": "R1(config)# interface gigabitEthernet 0/0\nR1(config-if)# ip helper-address 192.168.2.100",
        "caution": "Use the real DHCP server address and verify routing between the relay and server."
    },
    {
        "id": "switch-management",
        "category": "switch-routing",
        "title": "Configure a Management SVI",
        "command": "interface vlan 1\nip address 192.168.1.100 255.255.255.0\nno shutdown",
        "mode": "Interface configuration",
        "purpose": "Assigns a management IP address to a switch virtual interface.",
        "explanation": "The switch's management IP enables IP-based management when the SVI is operational. A Layer 2 switch may also need an IP default gateway.",
        "example": "SW1(config)# interface vlan 1\nSW1(config-if)# ip address 192.168.1.100 255.255.255.0\nSW1(config-if)# no shutdown\nSW1(config)# ip default-gateway 192.168.1.1",
        "caution": "VLAN 1 is used in the supplied reference. A dedicated management VLAN may be preferable in a designed network."
    },
    {
        "id": "static-route",
        "category": "switch-routing",
        "title": "Configure a Static Route",
        "command": "ip route 192.168.1.0 255.255.255.0 10.10.10.1",
        "mode": "Global configuration",
        "purpose": "Adds a route to 192.168.1.0/24 through next-hop address 10.10.10.1.",
        "explanation": "The command format is destination network, subnet mask, and next-hop address.",
        "example": "R2(config)# ip route 192.168.1.0 255.255.255.0 10.10.10.1\nR2# show ip route",
        "caution": "Confirm the next hop is reachable and the destination and mask are correct."
    },
    {
        "id": "dhcp-snooping",
        "category": "dhcp-snooping",
        "title": "Enable DHCP Snooping",
        "command": "ip dhcp snooping\nip dhcp snooping vlan 1",
        "mode": "Global configuration",
        "purpose": "Enables DHCP snooping and activates it for VLAN 1.",
        "explanation": "DHCP snooping can help protect against rogue DHCP servers by controlling which switch ports are trusted to send server messages.",
        "example": "SW1(config)# ip dhcp snooping\nSW1(config)# ip dhcp snooping vlan 1\nSW1(config)# interface gigabitEthernet 0/1\nSW1(config-if)# ip dhcp snooping trust",
        "caution": "Only trust ports that lead to legitimate DHCP servers or trusted relay infrastructure. Verify platform support and topology."
    },
    {
        "id": "dhcp-snooping-rate",
        "category": "dhcp-snooping",
        "title": "Limit DHCP Message Rate",
        "command": "ip dhcp snooping limit rate 2",
        "mode": "Interface configuration",
        "purpose": "Limits DHCP packet rate on an interface when DHCP snooping is supported and active.",
        "explanation": "Rate limits can help reduce DHCP message abuse on untrusted access ports.",
        "example": "SW1(config)# interface fastEthernet 0/1\nSW1(config-if)# ip dhcp snooping limit rate 2",
        "caution": "Choose limits appropriate to the interface role and client behavior."
    },
    {
        "id": "ssh-domain",
        "category": "ssh",
        "title": "Configure a Domain Name for SSH",
        "command": "ip domain-name example.com",
        "mode": "Global configuration",
        "purpose": "Sets the domain name used by IOS in SSH key generation workflows.",
        "explanation": "The supplied reference uses jensen.se; example.com is a placeholder for this library entry.",
        "example": "R1(config)# ip domain-name example.com",
        "caution": "Replace the example domain with the intended domain for your lab."
    },
    {
        "id": "ssh-user",
        "category": "ssh",
        "title": "Create a Local SSH User",
        "command": "username admin privilege 15 secret YOUR_STRONG_SECRET",
        "mode": "Global configuration",
        "purpose": "Creates a local user with privileged access.",
        "explanation": "When VTY lines use login local, IOS checks the local username database.",
        "example": "R1(config)# username admin privilege 15 secret YOUR_STRONG_SECRET\nR1(config)# line vty 0 15\nR1(config-line)# login local\nR1(config-line)# transport input ssh",
        "caution": "Privilege level 15 grants extensive access. Use strong credentials and restrict management access."
    },
    {
        "id": "ssh-version",
        "category": "ssh",
        "title": "Enable SSH Version 2",
        "command": "ip ssh version 2",
        "mode": "Global configuration",
        "purpose": "Configures IOS to use SSH version 2 where supported.",
        "explanation": "SSH provides encrypted remote management, unlike Telnet, which transmits session data without SSH encryption.",
        "example": "R1(config)# ip domain-name example.com\nR1(config)# crypto key generate rsa\nR1(config)# ip ssh version 2\nR1(config)# line vty 0 15\nR1(config-line)# login local\nR1(config-line)# transport input ssh",
        "caution": "Use a suitable RSA key size supported by the platform and current security requirements."
    },
    {
        "id": "vlan-create",
        "category": "vlan",
        "title": "Create a VLAN",
        "command": "vlan 10\nname Google",
        "mode": "Global configuration, then VLAN configuration",
        "purpose": "Creates VLAN 10 and assigns it a descriptive name.",
        "explanation": "VLANs separate a switched network into logical Layer 2 broadcast domains.",
        "example": "Switch(config)# vlan 10\nSwitch(config-vlan)# name Google",
        "caution": "The name is a label only. Choose VLAN IDs and names that match the network design."
    },
    {
        "id": "access-port",
        "category": "vlan",
        "title": "Assign an Access Port to a VLAN",
        "command": "switchport mode access\nswitchport access vlan 10",
        "mode": "Interface configuration",
        "purpose": "Configures a switch port as an access port in VLAN 10.",
        "explanation": "Access ports typically connect end devices to a single VLAN.",
        "example": "Switch(config)# interface fastEthernet 0/1\nSwitch(config-if)# switchport mode access\nSwitch(config-if)# switchport access vlan 10",
        "caution": "Ensure VLAN 10 exists and the port connects to the intended endpoint."
    },
    {
        "id": "trunk-port",
        "category": "vlan",
        "title": "Configure a Trunk Port",
        "command": "switchport mode trunk",
        "mode": "Interface configuration",
        "purpose": "Configures a switch port to carry traffic for multiple VLANs.",
        "explanation": "Trunk links commonly use IEEE 802.1Q VLAN tagging between switches or between a switch and a router.",
        "example": "Switch(config)# interface fastEthernet 0/24\nSwitch(config-if)# switchport mode trunk\nSwitch# show interfaces trunk",
        "caution": "Confirm the platform's trunk encapsulation behavior and allowed VLAN list."
    },
    {
        "id": "router-on-a-stick",
        "category": "vlan",
        "title": "Configure a Router Subinterface",
        "command": "encapsulation dot1Q 10\nip address 199.199.199.1 255.255.255.0",
        "mode": "Subinterface configuration",
        "purpose": "Associates a router subinterface with VLAN 10 and assigns its gateway address.",
        "explanation": "Router-on-a-stick uses multiple router subinterfaces over one physical router interface to route between VLANs.",
        "example": "Router(config)# interface gigabitEthernet 0/0.10\nRouter(config-subif)# encapsulation dot1Q 10\nRouter(config-subif)# ip address 199.199.199.1 255.255.255.0",
        "caution": "The switch link must be a compatible trunk, and each VLAN's IP subnet must be correctly planned."
    },
    {
        "id": "nat-overload",
        "category": "nat",
        "title": "Configure PAT (NAT Overload)",
        "command": "ip nat inside source list 1 interface gigabitEthernet 0/0/1 overload",
        "mode": "Global configuration",
        "purpose": "Translates matching inside addresses using the outside interface address and port numbers.",
        "explanation": "PAT allows multiple internal hosts to share one outside IPv4 address. The referenced ACL defines which source addresses are eligible for translation.",
        "example": "HQ-Router(config)# access-list 1 permit 192.168.10.0 0.0.0.255\nHQ-Router(config)# ip nat inside source list 1 interface gigabitEthernet 0/0/1 overload",
        "caution": "The relevant interfaces must be marked ip nat inside or ip nat outside, and a usable upstream route is needed."
    },
    {
        "id": "default-route",
        "category": "nat",
        "title": "Configure a Default Route",
        "command": "ip route 0.0.0.0 0.0.0.0 203.0.113.1",
        "mode": "Global configuration",
        "purpose": "Creates a route used when no more specific route matches the destination.",
        "explanation": "The supplied reference uses 203.0.113.1 as the next hop. This address belongs to a documentation-only IPv4 range and is an example, not a real public internet gateway.",
        "example": "HQ-Router(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1",
        "caution": "Replace the example next hop with the actual reachable upstream gateway in your lab."
    },
    {
        "id": "ospf-process",
        "category": "ospf",
        "title": "Enable OSPF Process 1",
        "command": "router ospf 1",
        "mode": "Global configuration",
        "purpose": "Enters OSPF router configuration for process ID 1.",
        "explanation": "OSPF is a link-state routing protocol. The process ID is locally significant on the router.",
        "example": "Router-KB(config)# router ospf 1\nRouter-KB(config-router)# network 10.0.0.0 0.0.0.3 area 0\nRouter-KB(config-router)# network 172.16.1.0 0.0.0.255 area 0",
        "caution": "Ensure wildcard masks match the intended interfaces and area design."
    },
    {
        "id": "ospf-passive",
        "category": "ospf",
        "title": "Configure a Passive OSPF Interface",
        "command": "passive-interface gigabitEthernet 0/0/1",
        "mode": "OSPF router configuration",
        "purpose": "Prevents OSPF hello packets from being sent out the specified interface while allowing the connected network to be advertised, subject to the OSPF configuration.",
        "explanation": "This is often useful on LANs with end-user devices where no OSPF neighbor is expected.",
        "example": "Router-KB(config)# router ospf 1\nRouter-KB(config-router)# passive-interface gigabitEthernet 0/0/1",
        "caution": "Use the correct interface name for your router and verify the resulting OSPF behavior."
    },
    {
        "id": "ospf-neighbor",
        "category": "ospf",
        "title": "Verify OSPF Neighbors",
        "command": "show ip ospf neighbor",
        "mode": "Privileged EXEC",
        "purpose": "Displays OSPF neighbor relationships.",
        "explanation": "Use it to check whether OSPF routers have formed neighbor adjacencies.",
        "example": "Router-KB# show ip ospf neighbor",
        "caution": "No neighbor can indicate a link, addressing, area, timer, authentication, or OSPF configuration issue."
    },
    {
        "id": "save-config",
        "category": "switch-routing",
        "title": "Save the Running Configuration",
        "command": "copy running-config startup-config",
        "mode": "Privileged EXEC",
        "purpose": "Copies the active configuration into the startup configuration.",
        "explanation": "This preserves configuration changes across a restart on devices that use this configuration model.",
        "example": "SW1# copy running-config startup-config",
        "caution": "Verify your configuration before saving it."
    },
    {
        "id": "show-dhcp-snooping",
        "category": "dhcp-snooping",
        "title": "Verify DHCP Snooping",
        "command": "show ip dhcp snooping",
        "mode": "Privileged EXEC",
        "purpose": "Displays DHCP snooping status and configuration details.",
        "explanation": "Use it to verify that snooping is enabled for the intended VLANs and inspect trusted interface settings.",
        "example": "SW1# show ip dhcp snooping",
        "caution": "Available fields and command behavior vary by IOS platform and release."
    }
]


@app.get("/")
def home():
    return send_from_directory(BASE_DIR / "static", "index.html")


@app.get("/api")
def api_info():
    return jsonify(
        name="NETFORGE Cisco IOS Command Library",
        description="Search and learn Cisco IOS configuration and verification commands.",
        endpoints=[
            "GET /api/health",
            "GET /api/categories",
            "GET /api/commands",
            "GET /api/commands/<id>",
        ],
    )


@app.get("/api/health")
def health():
    return jsonify(status="ok", categories=len(CATEGORIES), commands=len(COMMANDS))


@app.get("/api/categories")
def categories():
    result = []
    for category in CATEGORIES:
        count = sum(c["category"] == category["id"] for c in COMMANDS)
        result.append({**category, "count": count})
    return jsonify(count=len(result), categories=result)


@app.get("/api/commands")
def list_commands():
    category = request.args.get("category", "").strip().lower()
    query = request.args.get("q", "").strip().lower()

    results = COMMANDS
    if category:
        results = [c for c in results if c["category"] == category]
    if query:
        results = [
            c for c in results
            if query in c["title"].lower()
            or query in c["command"].lower()
            or query in c["purpose"].lower()
            or query in c["explanation"].lower()
            or query in c["category"].lower()
        ]

    return jsonify(count=len(results), commands=results)


@app.get("/api/commands/<command_id>")
def command_detail(command_id):
    command = next((c for c in COMMANDS if c["id"] == command_id), None)
    if command is None:
        return jsonify(error="Command not found"), 404
    return jsonify(command)


@app.errorhandler(404)
def not_found(_error):
    return jsonify(error="Not found"), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify(error="Method not allowed"), 405


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
