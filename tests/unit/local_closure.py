#****************************************************************************
#* local_closure.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
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
import inspect

class LocalClosure(object):
    def __init__(self, level=0):
        frame = inspect.currentframe().f_back
        self.locals = {}
        self.globals = {}
        il = 0
        while frame is not None:
            if il == level:
                for k,v in frame.f_locals.items():
                    self.locals[k] = v
                for k in frame.f_globals.keys():
                    self.globals[k] = v
                break
            frame = frame.f_back

    def __getattr__(self, name: str):
        if name in self.locals.keys():
            return self.locals[name]
        elif name in self.globals.keys():
            return self.globals[name]

        return None


