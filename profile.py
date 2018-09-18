"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 # Instantiate the amount of nodes in the cluster
num_nodes = 4

# Create a list to hold the nodes to be placed in the cluster
list_nodes = list()

# Create the links for clusters to be used later
link = request.LAN("lan")

# Create all 4 nodes and their individual names
for x in range(num_nodes):
    list_nodes.append(request.XenVM("node-"+str(x+1)))
  
y=1
for node in list_nodes:
     node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
     node.addService(pg.Execute(shell="sh", command="sudo local/repository/silly.sh"))
   
     # Conditional to allow only node-1 to be able to connect to the internet
     if y == 1:
         node.routable_control_ip = "true"
         y == 0
        
# Create empty list for interfaces
interfaces = list()
ifaces_len = len(list_nodes)
for z in range(0, ifaces_len):
    interfaces.append(list_nodes[z].addInterface("if1"))
    interfaces[z].component_id = "eth1"
    interfaces[z].addAddress(pg.IPv4Address("192.168.1."+str(z+1),"255.255.255.0"))
    link.addInterface(interfaces[z])
                                                 
pc.printRequestRSpec(request)
                            
