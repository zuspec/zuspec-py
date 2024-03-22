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
import os
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
            print("write64 0x%08x %d" % (addr, data), flush=True)

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
/*
//                reg_region = aspace.add_nonallocatable_region(region);
 */
                reg_region = aspace.add_nonallocatable_region(region);

                print("init_down running");
                xxx.set_handle(reg_region);
                /*
                 */
            }

            action Entry {
                exec body {
                    bit[32]     val;

                    comp.xxx.r2.write_val(25);
                    comp.xxx.r1.write_val(20);
                    /*
                    val = comp.xxx.r1.read_val();
                    print("val: %d", val);
                     */
                }
/*
 */
            }
        }
        """
        self.enableDebug(True)
        self.loadContent(content)
        out = io.StringIO()
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

        print("Output:\n%s" % out.getvalue(), flush=True)

    def test_reg_array(self):

        async def write64(addr, data):
            print("write64 0x%08x %d" % (addr, data))

        async def read64(addr):
            print("read64 %d" % addr)
            return 21

        content = """
        import addr_reg_pkg::*;
        import std_pkg::*;

        pure component reg_blk : reg_group_c {
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

        component my_regs : reg_group_c {
            reg_blk             blks[4];

            pure function bit[64] get_offset_of_instance(string name) {
                return 0xFFFF_FFFF_FFFF_FFFF;
            }

            pure function bit[64] get_offset_of_instance_array(string name, int index) {
                if (name == "blks") {
                    return 0x100*index;
                }
                return 0xFFFF_FFFF_FFFF_FFFF;
            }
            /*
             */
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
                /*
                 */
            }

            action Entry {
                exec body {
                    bit[32]     val;

                    comp.xxx.blks[0].r2.write_val(25);
                    comp.xxx.blks[1].r2.write_val(25);
                    comp.xxx.blks[0].r1.write_val(20);
                    comp.xxx.blks[3].r1.write_val(25);
                    /*
                    comp.xxx.blks[3].r1.write_val(20);
                    val = comp.xxx.blks[0].r1.read_val();
                    print("val: %d", val);
                     */
                }
/*
 */
            }
        }
        """
        self.enableDebug(True)
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

    def test_fwperiph_dma_regs(self):
        async def write32(addr, data):
            print("write32: 0x%08x 0x%08x" % (addr, data), flush=True)
            pass

        content = """
import addr_reg_pkg::*;
component pss_top {
    transparent_addr_space_c<>      aspace;
    addr_handle_t                   base;
    fwperiph_dma_map                regs;

    exec init_down {
        transparent_addr_region_s<>     region;

        region.addr = 0x0;
        region.size = 0x1_0000_0000;
        base = aspace.add_nonallocatable_region(region);
        regs.set_handle(base);
    }

    action Entry {
        exec body {
            comp.regs.int_msk_a.write_val(32);
            comp.regs.int_msk_b.write_val(64);
        }
    }
}
"""

        files = [
            os.path.join(self.datadir, "registers/fwperiph_dma_ral.pss"),
            content
        ]

        self.enableDebug(False)
        self.loadContent(files, load_stdlib=True)

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

