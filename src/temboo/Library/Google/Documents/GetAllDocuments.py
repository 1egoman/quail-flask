# -*- coding: utf-8 -*-

###############################################################################
#
# GetAllDocuments
# Retrieves a list of all documents, files, and collections in a Google account.
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

class GetAllDocuments(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the GetAllDocuments Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(GetAllDocuments, self).__init__(temboo_session, '/Library/Google/Documents/GetAllDocuments')


    def new_input_set(self):
        return GetAllDocumentsInputSet()

    def _make_result_set(self, result, path):
        return GetAllDocumentsResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return GetAllDocumentsChoreographyExecution(session, exec_id, path)

class GetAllDocumentsInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the GetAllDocuments
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_Deleted(self, value):
        """
        Set the value of the Deleted input for this Choreo. ((optional, boolean) Returns deleted documents when set to "true" (the default). Skips deleted documents when set to "false".)
        """
        super(GetAllDocumentsInputSet, self)._set_input('Deleted', value)
    def set_Password(self, value):
        """
        Set the value of the Password input for this Choreo. ((required, password) Your Google account password.)
        """
        super(GetAllDocumentsInputSet, self)._set_input('Password', value)
    def set_Username(self, value):
        """
        Set the value of the Username input for this Choreo. ((required, string) Your full Google email address e.g., martha.temboo@gmail.com.)
        """
        super(GetAllDocumentsInputSet, self)._set_input('Username', value)

class GetAllDocumentsResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the GetAllDocuments Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((xml) The response from the Google Documents API.)
        """
        return self._output.get('Response', None)

class GetAllDocumentsChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return GetAllDocumentsResultSet(response, path)
