#****************************************************************************
#* actor.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
from .impl.env_config import EnvConfig
from zsp_be_py.impl.runner import Runner

class Actor(object):

    def __init__(self, comp_t, action_t):
        self._comp_t = comp_t
        self._action_t = action_t
        self._pymodules = {}
        self._out_fp = None

    def addPyModule(self, name, obj):
        self._pymodules[name] = obj

    @property
    def outfp(self):
        return self._out_fp
    
    @outfp.setter
    def outfp(self, fp):
        self._out_fp = fp

    async def run(self, seed=None):
        # Get the active configuration, probing the
        # environment if necessary
        envcfg = EnvConfig.inst()


        runner = Runner(
            self._comp_t,
            None,
            ctxt=envcfg.getContext(),
            backend=envcfg.getRunnerBackend())
        runner.setMsgFP(self._out_fp)
        
        for key,val in self._pymodules.items():
            runner.addPyModule(key, val)

        if seed is not None:
            # Explicitly seeded
            randstate = runner.mkRandState(seed)
        else:
            # Implicitly seeded
            randstate = runner.mkRandState("0")
            pass

        await runner.run(self._action_t, randstate)
