#****************************************************************************
#* test_mem_access.py
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

class TestMemAccess(TestBase):

    def test_smoke(self):
        writes = []
        async def write32(addr, data):
            nonlocal writes
            writes.append((addr, data))

        content = """
        import addr_reg_pkg::*;

        component pss_top {
            action Entry {
                exec body {
                    write32(4, 1000);
                }
            }
        }
        """
        self.enableDebug(False)
        self.loadContent(content)
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0][0], 4)
        self.assertEqual(writes[0][1], 1000)

    def test_access_mem_hndl(self):
        writes = []
        async def write32(addr, data):
            nonlocal writes
            print("write32 0x%08x 0x%08x" % (addr, data))
            writes.append((addr, data))

        async def doit():
            print("doit")

        content = """
import std_pkg::*;
import addr_reg_pkg::*;

import function void doit();
pure component my_regs : reg_group_c {
    reg_c<bit[32]>         r1;
    reg_c<bit[32]>         r2;

    function bit[64] get_offset_of_instance(string name) {
        if (name == "r1") {
            return 0;
        } else if (name == "r2") {
            return 4;
        }
        return 0xFFFF_FFFF_FFFF_FFFF;
    }

    function bit[64] get_offset_of_instance_array(string name, int index) {
        return 0xFFFF_FFFF_FFFF_FFFF;
    }
}

component pss_top {
    transparent_addr_space_c<>      aspace;
    addr_handle_t                   base_h;
    my_regs                         regs;
                 
    exec init_down {
        transparent_addr_region_s<>  region;
        region.addr= 0x0001;
        region.size = 0x1000;
        base_h = aspace.add_nonallocatable_region(region);
        regs.set_handle(base_h);
    }

    action Entry {
        exec post_solve {
            print("Hello World!");
        }
        exec body {
            doit();
            write32(comp.base_h, 1);
            comp.regs.r1.write_val(1);
            comp.regs.r2.write_val(2);
        }
    }
}
"""
        self.enableDebug(False)
        self.loadContent(content)
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

#        self.assertEqual(len(writes), 1)
#        self.assertEqual(writes[0][0], 4)
#        self.assertEqual(writes[0][1], 1000)
