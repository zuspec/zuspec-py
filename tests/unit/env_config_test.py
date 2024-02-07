#****************************************************************************
#* env_config_test.py
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
import zsp_be_py
from zsp_be_py.impl.runner_backend_async_io import RunnerBackendAsyncIO
import zsp_arl_dm.core as arl_dm
import zsp_fe_parser.core as zsp_fe_parser
import zsp_parser.core as zspp
from zspy.impl.loader import Loader

from zspy.impl.env_config_provider import EnvConfigProvider

class EnvConfigTest(EnvConfigProvider):

    def __init__(self):
        self._backend = RunnerBackendAsyncIO()
        self._context = None
        pass

    def getRunnerBackend(self):
        return self._backend
    
    def getContext(self):
        if self._context is None:
            raise Exception("No content loaded")
        return self._context

    def loadContent(self, content, load_stdlib=True):
        loader = Loader()
        if isinstance(content, list):
            self._context = loader.load(load_stdlib, *content)
        else:
            self._context = loader.load(load_stdlib, content)

    @classmethod
    def create(cls):
        return EnvConfigTest()


