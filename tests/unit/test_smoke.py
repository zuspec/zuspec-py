#****************************************************************************
#* test_smoke.py
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
import zspy
from .test_base import TestBase

class TestSmoke(TestBase):

    def test_smoke(self):

        async def doit(i : int) -> int:
            print("doit: %s" % str(i))
#            print("doit: ")
            return i+1
            pass

        content = """
        function void doit(int i);
        import target function doit;

        component pss_top {
            action Entry {
                rand int i = 2, j;
                exec body {
                    i = 2;
                    j = doit(i);
                    doit(j);
                }

            }
        }
        """
        self.enableDebug(True)
        self.loadContent(content)
        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

        pass

