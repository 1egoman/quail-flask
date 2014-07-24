# -*- coding: utf-8 -*-

###############################################################################
#
# StudentCharges
# Returns tuition information for colleges and universities.
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

class StudentCharges(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the StudentCharges Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        super(StudentCharges, self).__init__(temboo_session, '/Library/DeptOfEducation/CollegesAndUniversities/StudentCharges')


    def new_input_set(self):
        return StudentChargesInputSet()

    def _make_result_set(self, result, path):
        return StudentChargesResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return StudentChargesChoreographyExecution(session, exec_id, path)

class StudentChargesInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the StudentCharges
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_InstitutionID(self, value):
        """
        Set the value of the InstitutionID input for this Choreo. ((optional, string) Specify an institutionID to return data on a specific institution. These ids can be retrieved from the LookupSchool Choreo.)
        """
        super(StudentChargesInputSet, self)._set_input('InstitutionID', value)
    def set_MaxRows(self, value):
        """
        Set the value of the MaxRows input for this Choreo. ((optional, integer) Limits the number of rows returned. Defaults to 20.)
        """
        super(StudentChargesInputSet, self)._set_input('MaxRows', value)
    def set_ResponseFormat(self, value):
        """
        Set the value of the ResponseFormat input for this Choreo. ((optional, string) The format that the response should be in. Valid values are: xml (the default) and json.)
        """
        super(StudentChargesInputSet, self)._set_input('ResponseFormat', value)

class StudentChargesResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the StudentCharges Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """

    def getJSONFromString(self, str):
        return json.loads(str)

    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Data.ed.gov.)
        """
        return self._output.get('Response', None)

class StudentChargesChoreographyExecution(ChoreographyExecution):

    def _make_result_set(self, response, path):
        return StudentChargesResultSet(response, path)