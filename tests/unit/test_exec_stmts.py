#****************************************************************************
#* test_exec_stmts.py
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
from .test_base import TestBase

class TestExecStmts(TestBase):

    def test_str_if_else(self):
        content = """
        import std_pkg::*;
        function int tst(string s) {
            if (s == "a") {
              return 1;
            } else {
              return 2;
            }
        }

        component pss_top {
            action Entry {
                exec post_solve {
                    print("val: %d", tst("a"));
                    print("val: %d", tst("b"));
                }
            }
        }
        """
        self.enableDebug(False)
        self.loadContent(content)

        out = io.StringIO()

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

#        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 1\nval: 2")

    def test_early_return(self):
        content = """
        import std_pkg::*;
        function int tst(string s) {
            return 1;
            return 2;
        }

        component pss_top {
            action Entry {
                exec post_solve {
                    print("val: %d", tst("a"));
                    print("val: %d", tst("b"));
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

        self.assertEqual(result, "val: 1\nval: 1")

    def test_repeat_count(self):
        content = """
        import std_pkg::*;

        component pss_top {
            action Entry {
                exec post_solve {
                    repeat (i : 2) {
                        print("val: %d", i);
                    }
                }
            }
        }
        """
        self.enableDebug(False)
        self.loadContent(content)

        out = io.StringIO()

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

#        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 0\nval: 1")

    def test_exec_local_var(self):
        content = """
        import std_pkg::*;

        component pss_top {
            action Entry {
                exec post_solve {
                    int a;
                    a = 5;
                    print("val: %d", a);
                }
            }
        }
        """
        self.enableDebug(False)
        self.loadContent(content)

        out = io.StringIO()

        actor = zspy.Actor("pss_top", "pss_top::Entry")
        actor.outfp = out
        self.runActor(actor)

#        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 5")

    def test_exec_local_aggregate_var(self):
        content = """
        import std_pkg::*;

        struct S { int a; }

        component pss_top {
            action Entry {
                exec post_solve {
                    S s;
                    s.a = 5;
                    print("val: %d", s.a);
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

#        print("Output:\n%s" % out.getvalue())
        result = out.getvalue().strip()

        self.assertEqual(result, "val: 5")