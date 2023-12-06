#****************************************************************************
#* test_registers.py
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
import zspy
from .test_base import TestBase
from .local_closure import LocalClosure

class TestRegisters(TestBase):

    def test_smoke(self):
        async def doit(i : int) -> int:
            print("doit: %s" % str(i))
#            print("doit: ")
            return i+1
            pass

        async def write64(addr, data):
            print("write64 %d %d" % (addr, data))

        content = """
        import addr_reg_pkg::*;

        /*
        function bit[64] get_offset(string name) {
            if (name == "r1") {
                return 0;
            } else if (name == "r2") {
                return 4;
            }
            return 0xFFFF_FFFF;
        }
         */

        component my_regs : reg_group_c {
            reg_c<bit[64]>      r1;
            reg_c<bit[64]>      r2;
            pure function bit[64] get_offset_of_instance(string name) {
                if (name == "r1") {
                    return 0;
                } 
                if (name == "r2") {
                    return 4;
                }
                return 0xFFFF_FFFF_FFFF_FFFF;
            }

            pure function bit[64] get_offset_of_instance_array(string name, int index) {
                return 5;
            }
        }

        component pss_top {
            my_regs     xxx;

            action Entry {
                exec body {
                    comp.xxx.r1.write_val(0);
//                    get_offset("r1");
                }
            }
        }
        """
        self.enableDebug(True)
        self.loadContent(content)
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

    def test_func_impl(self):
        async def doit(i : int) -> int:
            print("doit: %s" % str(i))
#            print("doit: ")
            return i+1
            pass

        content = """
        component my_regs {
            pure function bit[64] get_offset_of_instance(string name) {
                if (name == "r1") {
                    return 5;
                }
            }
        }

        component pss_top {
            my_regs     xxx;

            action Entry {
                exec body {
                }
            }
        }
        """
        self.enableDebug(True)
        self.loadContent(content, False)
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)