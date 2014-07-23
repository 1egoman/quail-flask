# -*- coding: utf-8 -*-

###############################################################################
#
# CreateDatabase
# Creates a new database in your account.
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

class CreateDatabase(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateDatabase Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(CreateDatabase, self).__init__(temboo_session, '/Library/MongoHQ/Databases/CreateDatabase')


    def new_input_set(self):
        return CreateDatabaseInputSet()

    def _make_result_set(self, result, path):
        return CreateDatabaseResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateDatabaseChoreographyExecution(session, exec_id, path)

class CreateDatabaseInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateDatabase
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_APIToken(self, value):
        """
        Set the value of the APIToken input for this Choreo. ((required, string) The API Token provided by MongoHQ.)
        """
        super(CreateDatabaseInputSet, self)._set_input('APIToken', value)
    def set_DatabaseName(self, value):
        """
        Set the value of the DatabaseName input for this Choreo. ((required, string) The name of the database to create.)
        """
        super(CreateDatabaseInputSet, self)._set_input('DatabaseName', value)
    def set_Type(self, value):
        """
        Set the value of the Type input for this Choreo. ((required, string) The type of database to create (e.g., sandbox, small, large))
        """
        super(CreateDatabaseInputSet, self)._set_input('Type', value)

class CreateDatabaseResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateDatabase Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. ((json) The response from MongoHQ.)
        """
        return self._output.get('Response', None)

class CreateDatabaseChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return CreateDatabaseResultSet(response, path)
