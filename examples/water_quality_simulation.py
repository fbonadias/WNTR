import wntr
import matplotlib.pyplot as plt

# Create a water network model and setup simulation
inp_file = 'networks/Net3.inp'
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)

# Run chemical concentration scenario and plot results
wn.options.quality = 'CHEMICAL'
wn.add_pattern('SourcePattern', start_time=2*3600, end_time=15*3600)
wn.add_source('Source1', '121', 'SETPOINT', 1000, 'SourcePattern')
wn.add_source('Source2', '123', 'SETPOINT', 1000, 'SourcePattern')
results = sim.run_sim()
CHEM_at_5hr = results.node.loc['quality', 5*3600, :]
wntr.graphics.draw_graph(wn, node_attribute=CHEM_at_5hr, node_size=20, 
                      title='Chemical concentration, time = 5 hours')
CHEM_at_node = results.node.loc['quality', :, '208']
plt.figure()
CHEM_at_node.plot(title='Chemical concentration, node 208')

# Run age scenario and plot results
wn.options.quality = 'AGE'
results = sim.run_sim()
AGE_at_5hr = results.node.loc['quality', 5*3600, :]/3600.0 # convert to hours
wntr.graphics.draw_graph(wn, node_attribute=AGE_at_5hr, node_size=20, 
                      title='Water age (hrs), time = 5 hours')
AGE_at_node = results.node.loc['quality', :, '208']/3600.0
plt.figure()
AGE_at_node.plot(title='Water age, node 208')

# Run trace scenario and plot results
wn.options.quality = 'TRACE'
wn.options.quality_value = '111'
results = sim.run_sim()
TRACE_at_5hr = results.node.loc['quality', 5*3600, :]
wntr.graphics.draw_graph(wn, node_attribute=TRACE_at_5hr, node_size=20, 
                      title='Trace percent, time = 5 hours')
TRACE_at_node = results.node.loc['quality', :, '208']
plt.figure()
TRACE_at_node.plot(title='Trace percent, node 208')

# Run a hydraulic simulation only
wn.options.quality = 'NONE'
results = sim.run_sim()

# To run water quality simulation with pressure-driven demands, 
# reset demands in the water network using demands computed using the 
# WNTRSimulator.
sim = wntr.sim.WNTRSimulator(wn)
results = sim.run_sim()
wn.reset_demand(results.node['demand'], 'PDD')
sim = wntr.sim.EpanetSimulator(wn)
results_withPDdemands = sim.run_sim()