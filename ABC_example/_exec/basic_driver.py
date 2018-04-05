#! /usr/bin/env python

"""
Version 1.0 (Batchelor 3/11/2018)
Simplified driver adapted from generic_driver.py, but eliminating reference to many
features specific to plasma physics.  The immediate application is to simple, example
simulations which do not make use of the SWIM Plasma State system.  The IPS framework uses
the terminology plasma state to refer to all state files.  But the SWIM Plasma State need
not be used at all.

This also uses David Green's approach of iterating on the PORTS.  Thus PORTS are instantiated,
initialized, and stepped in the order they appear in the PORTS list, rather than explicitly
named and ordered as they are in generic_driver.py.  In that sense this is more generic
than generic_driver.py.  But Caveat Utilitor, sometimes components need to be initialized
in a different order from that of being stepped in the time loop.

To terminate simulation after INIT phase, set optional DRIVER config 
parameter INIT_ONLY = True.

""" 

import sys
import os
import simple_assignment_file_edit as edit
from component import Component

class basic_driver(Component):

    def __init__(self, services, config):
        Component.__init__(self, services, config)
        print 'Created %s' % (self.__class__)

# ------------------------------------------------------------------------------
#
# init function
#
# ------------------------------------------------------------------------------

    def init(self, timestamp=0):
      # Driver initialization ? nothing to be done
        return

# ------------------------------------------------------------------------------
#
# step function
#
# ------------------------------------------------------------------------------

    def step(self, timestamp=0):

        services = self.services
        services.stage_plasma_state()
        services.stage_input_files(self.INPUT_FILES)

      # get list of ports
#        ports = services.getGlobalConfigParameter('PORTS')
        ports = self.get_config_param(services,'PORTS')
        port_names = ports['NAMES'].split()
        print 'PORTS =', port_names
        port_dict = {}
        port_id_list = []

      # Instantiate components in port_names list, except DRIVER itself which is done
      # by the framework
        print (' ')

        for port_name in port_names:
            if port_name in ["DRIVER"]: continue
            port = services.get_port(port_name) 
            if(port == None):
                logMsg = 'Error accessing '+port_name+' component'
                services.error(logMsg)
                raise Exception(logMsg)
            port_dict[port_name] = port
            port_id_list.append(port)
            print (' ')


      # Is this a simulation startup or restart
        sim_mode = self.get_config_param(services,'SIMULATION_MODE')

      # Get timeloop for simulation
        timeloop = services.get_time_loop()
        tlist_str = ['%.3f'%t for t in timeloop]
        t = tlist_str[0]

      # Initialize components in PORTS list for startup or restart
        print (' ')
        
        init_mode = 'init'
        if sim_mode == 'RESTART' : init_mode = 'restart'

        for port_name in port_names:
            if port_name in ['INIT','DRIVER']: continue 
            self.component_call(services,port_name,port_dict[port_name],init_mode,t)

      # Get state files into driver work directory
        services.stage_plasma_state()
        cur_state_file = services.get_config_param('CURRENT_STATE')
        
       # Get Portal RUNID and save to a file
        run_id = self.get_config_param(services,'PORTAL_RUNID')
        sym_root = self.get_config_param(services,'SIM_ROOT')
        path = os.path.join(sym_root, 'PORTAL_RUNID')
        runid_file = open(path, 'a')
        runid_file.writelines(run_id + '\n')
        runid_file.close()

        # Check if there is a config parameter CURRENT_STATE and add data if so.
        # In this case set t0 = t1 = tinit
        cur_state_file = self.get_config_param(services, 'CURRENT_STATE', optional = True)
        if cur_state_file != None and len(cur_state_file) > 0:
            timeloop = services.get_time_loop()
            variable_dict = {'t0' : timeloop[0], 't1' : timeloop[0]}
            if sim_mode == 'NORMAL' :
                edit.add_variables_to_output_file(variable_dict, cur_state_file)
            if sim_mode == 'RESTART' :
                edit.modify_variables_in_file(variable_dict, cur_state_file)
            if sim_mode not in ['NORMAL', 'RESTART']:
                message = 'Unknown Simulation mode ' + sim_mode
                print message
                services.exception(message)
                raise
            
            services.update_plasma_state()

       # Post init processing: stage plasma state, stage output
        services.stage_output_files(t, self.OUTPUT_FILES)

        print ' init sequence complete--ready for time loop'

        INIT_ONLY = self.get_component_param(services, 'INIT_ONLY', optional = True)
        if INIT_ONLY in [True, 'true', 'True', 'TRUE']:   
            message = 'INIT_ONLY: Intentional stop after INIT phase'
            print message
            return
 
# ------------------------------------------------------------------------------
#
# Start Physics Layer
#
# ------------------------------------------------------------------------------


        # Iterate through the timeloop
        for t in tlist_str[1:len(timeloop)]:
            print (' ')
            print 'Driver: step to time = ', t
            services.update_time_stamp(t)

        # pre_step_logic
        # It is sometimes necessary to do some tasks before starting a new time step.
        # This could entail evaluating logic based on results of last time step, or 
        # calculations not part of any of the components.  If there is a current state
        # file it usually at least involves setting the start time of this time step, t0,
        # equal to the end time of the last step, t1, and setting t1 = t.

        # call pre_step_logic
            services.stage_plasma_state()
            self.pre_step_logic(services,float(t))
            services.update_plasma_state()
            print (' ')

       # Call step for each component

            print (' ')
            for port_name in port_names:
                if port_name in ['INIT','DRIVER']: continue 
                self.component_call(services,port_name,port_dict[port_name],'step',t)

            services.stage_plasma_state()

         # Post step processing: stage plasma state, checkpoint components and self
            services.stage_output_files(t, self.OUTPUT_FILES)
            services.checkpoint_components(port_id_list, t)
            self.checkpoint(t)

# ------------------------------------------------------------------------------
#
# End of Physics Layer
#
# ------------------------------------------------------------------------------

      # Post simulation: call checkpoint on each component

        services.checkpoint_components(port_id_list, t, Force = True)
        self.checkpoint(t)
      
      # Post simulation: call finalize on each component
        print (' ')
        for port_name in port_names:
            if port_name in ['INIT','DRIVER']: continue 
            self.component_call(services, port_name, port_dict[port_name], 'finalize', t)


# ------------------------------------------------------------------------------
#
# checkpoint function
#
# Does nothing
# ------------------------------------------------------------------------------

    def checkpoint(self, timestamp=0.0):
        print 'generic_driver.checkpoint() called'
        

# ------------------------------------------------------------------------------
#
# finalize function 
#
# ------------------------------------------------------------------------------

    def finalize(self, timestamp = 0):
      # Driver finalize - nothing to be done
        pass

# ------------------------------------------------------------------------------
#
# "Private"  methods
#
# ------------------------------------------------------------------------------

    # Component call - wraps the exception handling for all component calls
    def component_call(self, services, port_name, comp, mode, time):
        comp_mode_string = port_name + ' ' + mode
        print '\n', comp_mode_string

        try:
            services.call(comp, mode, time)
        except Exception:
            message = comp_mode_string + ' failed'
            print message
            services.exception(message)
            raise
        
        return
    
    
    # Pre Step Logic
    def pre_step_logic(self, services, timeStamp):

    # Check if there is a config parameter CURRENT_STATE and update t0, t1 if so.
        cur_state_file = self.get_config_param(services, 'CURRENT_STATE', optional = True)
        print 'pre-step-logic: cur_state_file = ', cur_state_file
        if cur_state_file != None and len(cur_state_file) > 0:
            state_dict = edit.input_file_to_variable_dict(cur_state_file)
            change_dict = {'t0':state_dict['t1'], 't1':timeStamp}
            edit.modify_variables_in_file(change_dict, cur_state_file)
        return

    # Try to get config parameter - wraps the exception handling for get_config_parameter()
    def get_config_param(self, services, param_name, optional=False):

        try:
            value = services.get_config_param(param_name)
            print param_name, ' = ', value
        except Exception :
            if optional: 
                print 'config parameter ', param_name, ' not found'
                value = None
            else:
                message = 'required config parameter ', param_name, ' not found'
                print message
                services.exception(message)
                raise
        
        return value

    # Try to get component specific config parameter - wraps the exception handling
    def get_component_param(self, services, param_name, optional=False):

        if hasattr(self, param_name):
            value = getattr(self, param_name)
            print param_name, ' = ', value
        elif optional:
            print 'optional config parameter ', param_name, ' not found'
            value = None
        else:
            message = 'required component config parameter ', param_name, ' not found'
            print message
            services.exception(message)
            raise
        
        return value
