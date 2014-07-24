# -*- coding: utf-8 -*-

###############################################################################
#
# CreateCollection
# Creates a new collection within a database.
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

class CreateCollection(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateCollection Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateCollection, self).__init__(temboo_session, '/Library/MongoHQ/Collections/CreateCollection')


    def new_input_set(self):
        return CreateCollectionInputSet()

    def _make_result_set(self, result, path):
        return CreateCollectionResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateCollectionChoreographyExecution(session, exec_id, path)

class CreateCollectionInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateCollection
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_APIToken(self, value):
        """
        Set the value of the APIToken input for this Choreo. ((required, string) The API Token provided by MongoHQ.)
        """
        super(CreateCollectionInputSet, self)._set_input('APIToken', value)
    def set_CollectionName(self, value):
        """
        Set the value of the CollectionName input for this Choreo. ((required, string) The name of the collection to create.)
        """
        super(CreateCollectionInputSet, self)._set_input('CollectionName', value)
    def set_DatabaseName(self, value):
        """
        Set the value of the DatabaseName input for this Choreo. ((required, string) The name of the database to create the collection under.)
        """
        super(CreateCollectionInputSet, self)._set_input('DatabaseName', value)

class CreateCollectionResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateCollection Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from MongoHQ.)
        """
        return self._output.get('Response', None)

class CreateCollectionChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateCollectionResultSet(response, path)