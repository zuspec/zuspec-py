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

