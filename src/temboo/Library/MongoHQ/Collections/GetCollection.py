# -*- coding: utf-8 -*-

###############################################################################
#
# GetCollection
# Retrieves a specific collection within a database.
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

class GetCollection(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the GetCollection Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(GetCollection, self).__init__(temboo_session, '/Library/MongoHQ/Collections/GetCollection')


    def new_input_set(self):
        return GetCollectionInputSet()

    def _make_result_set(self, result, path):
        return GetCollectionResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return GetCollectionChoreographyExecution(session, exec_id, path)

class GetCollectionInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the GetCollection
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_APIToken(self, value):
        """
        Set the value of the APIToken input for this Choreo. ((required, string) The API Token provided by MongoHQ.)
        """
        super(GetCollectionInputSet, self)._set_input('APIToken', value)
    def set_CollectionName(self, value):
        """
        Set the value of the CollectionName input for this Choreo. ((required, string) The name of the collection to retrieve.)
        """
        super(GetCollectionInputSet, self)._set_input('CollectionName', value)
    def set_DatabaseName(self, value):
        """
        Set the value of the DatabaseName input for this Choreo. ((required, string) The name of the database that contains the collection to retrieve.)
        """
        super(GetCollectionInputSet, self)._set_input('DatabaseName', value)

class GetCollectionResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the GetCollection Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from MongoHQ.)
        """
        return self._output.get('Response', None)

class GetCollectionChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return GetCollectionResultSet(response, path)
