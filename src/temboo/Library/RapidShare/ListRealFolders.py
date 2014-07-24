# -*- coding: utf-8 -*-

###############################################################################
#
# ListRealFolders
# Returns all existing RealFolders
#
# Python versions 2.6, 2.7, 3.x
#
# Copyright 2014, Temboo Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class ListRealFolders(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the ListRealFolders Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(ListRealFolders, self).__init__(temboo_session, '/Library/RapidShare/ListRealFolders')


    def new_input_set(self):
        return ListRealFoldersInputSet()

    def _make_result_set(self, result, path):
        return ListRealFoldersResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return ListRealFoldersChoreographyExecution(session, exec_id, path)

class ListRealFoldersInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the ListRealFolders
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_Login(self, value):
        """
        Set the value of the Login input for this Choreo. ((required, string) Your RapidShare username)
        """
        super(ListRealFoldersInputSet, self)._set_input('Login', value)
    def set_Password(self, value):
        """
        Set the value of the Password input for this Choreo. ((required, password) Your RapidShare password)
        """
        super(ListRealFoldersInputSet, self)._set_input('Password', value)

class ListRealFoldersResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the ListRealFolders Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((string) The response from RapidShare formatted in commas separated values.)
        """
        return self._output.get('Response', None)

class ListRealFoldersChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return ListRealFoldersResultSet(response, path)