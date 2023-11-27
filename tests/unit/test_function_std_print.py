#****************************************************************************
#* test_function_std_print.py
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

class TestFunctionStdPrint(TestBase):

    def test_smoke(self):
        content = """
        import std_pkg::*;

        component pss_top {
            action Entry {
                exec post_solve {
                    print("Hello World %d", 20);
                }
            }
        }
        """

        self.enableDebug(True)
        self.loadContent(content)

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        self.runActor(actor)

