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
import io
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
            print("write64 0x%08x %d" % (addr, data))

        async def read64(addr):
            print("read64 %d" % addr)
            return 21

        content = """
        import addr_reg_pkg::*;
        import std_pkg::*;

        component my_regs : reg_group_c {

            reg_c<bit[64]>      r1;
            reg_c<bit[64]>      r2;
            pure function bit[64] get_offset_of_instance(string name) {
                if (name == "r1") {
                    return 0;
                } else if (name == "r2") {
                    return 4;
                }
                return 0xFFFF_FFFF_FFFF_FFFF;
            }

            pure function bit[64] get_offset_of_instance_array(string name, int index) {
                return 0xFFFF_FFFF_FFFF_FFFF;
            }
        }

        component pss_top {
            transparent_addr_space_c<>      aspace;
            my_regs                         xxx;

            exec init_down {
                transparent_addr_region_s<> region;
                addr_handle_t reg_region;

                region.addr = 0x1000_0000;
                region.size = 0x0000_1000;
//                reg_region = aspace.add_nonallocatable_region(region);
                reg_region = aspace.add_nonallocatable_region(region);

//                print("init_down running");
                xxx.set_handle(reg_region);
            }

            action Entry {
                exec body {
                    bit[32]     val;

                    comp.xxx.r2.write_val(25);
                    comp.xxx.r1.write_val(20);
                    val = comp.xxx.r1.read_val();
                    print("val: %d", val);
                }
/*
 */
            }
        }
        """
        self.enableDebug(False)
        self.loadContent(content)
        out = io.StringIO()
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.out_fp = out
        self.runActor(actor)

        print("Output:\n%s" % out.getvalue())

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