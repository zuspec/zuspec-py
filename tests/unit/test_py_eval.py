#****************************************************************************
#* test_py_eval.py
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
from .local_closure import LocalClosure
from .test_base import TestBase

class TestPyEval(TestBase):

    def test_smoke(self):
        content = """
        import std_pkg::*;
        pyimport local;
//                rand int i = 2, j;
//                    pyobj fn = local::get_fn();
//                    pyobj fn;
//                    fn  = local::get_fn();
//                    j = fn(); 

        component pss_top {
            action Entry {
                exec post_solve {
                    int j = 1;
                    pyobj fn = local::get_fn();
//                    pyobj fn;
                    fn  = local::get_fn();
                    j = fn(); 
                    print("post_solve");
                }
            }
        }
        """

        def doit():
            print("Hello from DOIT", flush=True)
            return 20

        def get_fn():
            return doit

        self.enableDebug(False)
        self.loadContent(content)

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.addPyModule("local", LocalClosure())
        self.runActor(actor)

    def test_access_aggregate(self):
        content = """
        import std_pkg::*;
        pyimport local;

        struct S {
          int a, b, c, d;
        }

        component pss_top {
            action Entry {
                exec post_solve {
                    S sv;
                    sv.a = 1;
                    sv.b = 2;
                    sv.c = 3;
                    sv.d = 4;
                    local::doit(sv);
                }
            }
        }
        """

        def doit(sv):
            print("Hello from DOIT", flush=True)
            return 20

        self.enableDebug(False)
        self.loadContent(content)

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.addPyModule("local", LocalClosure())
        self.runActor(actor)
