#****************************************************************************
#* test_function_native.py
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
import io
from .local_closure import LocalClosure
from .test_base import TestBase

class TestFunctionNative(TestBase):

    def test_smoke(self):
        content = """
        pyimport local;
        function int doit(int i) {
//            int j = i + 1;
            i = i + 1;
            return 1;
        }

        component pss_top {
            action Entry {
                rand int i = 2, j;
                exec post_solve {
//                    i = 2;
//                    j = doit(i);
                    doit(1);
//                    i = local::doit(j);
//                    j = local::doit(i);
                }
            }
        }
        """

        self.enableDebug(True)
        self.loadContent(content)

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.addPyModule("local", LocalClosure())
        self.runActor(actor)

    def test_return_int(self):
        content = """
        import std_pkg::*;
        function int inc(int i) {
            return i+1;
        }

        component pss_top {
            action Entry {
                exec post_solve {
                    print("val: %d", inc(2));
                }
            }
        }
        """

        self.enableDebug(True)
        self.loadContent(content)

        out = io.StringIO()

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 3")

    def test_local_var_int(self):
        content = """
        import std_pkg::*;
        function int inc(int i) {
            int j;
            j = i;
            return j+1;
        }

        component pss_top {
            action Entry {
                exec post_solve {
                    print("val: %d", inc(2));
                }
            }
        }
        """

        self.enableDebug(True)
        self.loadContent(content)

        out = io.StringIO()

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 3")
